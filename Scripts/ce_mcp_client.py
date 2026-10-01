"""通过标准输入输出与 Cheat Engine MCP 网关通信的客户端实现。"""

import json
import os
import queue
import subprocess
import threading
import time
from pathlib import Path


class TransportError(RuntimeError):
    pass


class ToolError(RuntimeError):
    def __init__(self, payload):
        """保存工具错误载荷并提取错误类型；参数为工具返回的错误字典，无返回值。"""
        self.payload = payload
        detail = payload.get("error", payload)
        self.kind = detail.get("kind", "tool_error") if isinstance(detail, dict) else "tool_error"
        super().__init__(json.dumps(payload, ensure_ascii=True))


class McpClient:
    def __init__(self, argv: list[str], timeout: float, log_path: Path):
        """初始化 MCP 客户端；参数为网关命令、超时秒数和 stderr 日志路径，无返回值。"""
        if timeout <= 0:
            raise ValueError("timeout must be positive")
        self.argv, self.timeout, self.log_path = argv, timeout, log_path
        self.process = None
        self.log = None
        self.reader = None
        self.messages = queue.Queue()
        self.request_id = 0
        self.broken = False

    def start(self):
        """启动网关并完成 MCP 握手；无参数，返回已启动的客户端实例。"""
        self.log = self.log_path.open("w", encoding="utf-8")
        try:
            self.process = subprocess.Popen(
                self.argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                stderr=self.log, text=True, encoding="utf-8", bufsize=1,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
            )
            self.reader = threading.Thread(target=self._read, daemon=True)
            self.reader.start()
            result = self.rpc("initialize", {
                "protocolVersion": "2025-06-18", "capabilities": {},
                "clientInfo": {"name": "ce-opcode-export", "version": "1.0"},
            })
            if result.get("protocolVersion") != "2025-06-18":
                raise TransportError("unsupported negotiated MCP protocol")
            self._send({"jsonrpc": "2.0", "method": "notifications/initialized"})
            return self
        except BaseException:
            # 包括 KeyboardInterrupt 在内：任何失败都要先回收本次启动的子进程。
            try:
                self.close()
            except Exception:
                pass  # 清理失败不得掩盖原始异常
            raise

    def _read(self):
        """后台读取网关输出并放入消息队列；无参数和返回值。"""
        try:
            for line in self.process.stdout:
                item = json.loads(line)
                if not isinstance(item, dict):
                    raise ValueError("MCP frame must be an object")
                self.messages.put(item)
        except Exception:
            self.messages.put(TransportError("invalid gateway stdout"))
        finally:
            self.messages.put(TransportError("gateway stdout closed"))

    def _send(self, message):
        """向网关发送 JSON-RPC 消息；参数为消息字典，无返回值。"""
        if self.broken:
            raise TransportError("MCP connection is unusable")
        try:
            self.process.stdin.write(json.dumps(message, ensure_ascii=True) + "\n")
            self.process.stdin.flush()
        except (OSError, ValueError) as exc:
            self.broken = True
            raise TransportError("gateway stdin closed") from exc

    def rpc(self, method: str, params: dict) -> dict:
        """发送并等待 JSON-RPC 响应；参数为方法名和参数字典，返回结果字典。"""
        self.request_id += 1
        request_id = self.request_id
        self._send({"jsonrpc": "2.0", "id": request_id, "method": method, "params": params})
        deadline = time.monotonic() + self.timeout
        try:
            while True:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise TransportError("MCP request timed out")
                try:
                    response = self.messages.get(timeout=remaining)
                except queue.Empty as exc:
                    raise TransportError("MCP request timed out") from exc
                if isinstance(response, Exception):
                    raise response
                if response.get("jsonrpc") != "2.0":
                    raise TransportError("invalid JSON-RPC version")
                if "method" in response:
                    if "id" in response:
                        self._send({
                            "jsonrpc": "2.0", "id": response["id"],
                            "error": {"code": -32601, "message": "Client method not supported"},
                        })
                    continue
                if response.get("id") != request_id:
                    raise TransportError("unexpected JSON-RPC response id")
                if "error" in response:
                    raise ToolError(response["error"])
                result = response.get("result")
                if not isinstance(result, dict):
                    raise TransportError("invalid JSON-RPC result")
                return result
        except TransportError:
            self.broken = True
            raise

    def tools(self) -> dict:
        """分页获取网关工具目录；无参数，返回工具名到定义的映射。"""
        result, params, seen = {}, {}, set()
        while True:
            page = self.rpc("tools/list", params)
            for tool in page["tools"]:
                result[tool["name"]] = tool
            cursor = page.get("nextCursor")
            if not cursor:
                return result
            if cursor in seen:
                raise TransportError("repeated tools/list cursor")
            seen.add(cursor)
            params = {"cursor": cursor}

    def call(self, name: str, arguments: dict) -> dict:
        """调用 MCP 工具并解析结构化结果；参数为工具名和参数，返回结果字典。"""
        result = self.rpc("tools/call", {"name": name, "arguments": arguments})
        payload = result.get("structuredContent")
        if payload is None:
            texts = [p["text"] for p in result.get("content", []) if p.get("type") == "text"]
            try:
                payload = json.loads("".join(texts))
            except (ValueError, TypeError) as exc:
                raise TransportError("tool result is not structured JSON") from exc
        if not isinstance(payload, dict):
            raise TransportError("tool result must be an object")
        if result.get("isError"):
            raise ToolError(payload)
        return payload

    def close(self):
        """关闭网关进程、线程和日志文件；无参数和返回值。"""
        if self.process is not None:
            try:
                if self.process.stdin:
                    self.process.stdin.close()
            except (OSError, ValueError):
                pass
            try:
                self.process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.process.terminate()
                try:
                    self.process.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    self.process.kill()
                    self.process.wait(timeout=3)
            if self.reader:
                self.reader.join(timeout=1)
            if self.process.stdout:
                self.process.stdout.close()
            self.process = None
        if self.log is not None:
            self.log.close()
            self.log = None
