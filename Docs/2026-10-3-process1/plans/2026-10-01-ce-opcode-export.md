# CE 经 MCP 批量导出 opcode 实施方案

我将使用 writing-plans 能力生成完整实施方案。

> **面向自动化执行人员：必须配套子能力：使用 superpowers:executing-plans 逐任务执行本方案。步骤使用复选框（`- [ ]`）用于进度跟踪。**

**目标：** 完成 `Docs/goal1.md`：对脚本头部固化的 9 个指令地址（来源为 `Docs/testdata-2026-10-1-10-58.md` 的两个 “The following opcodes accessed …” 段落），经当前 CE 的 MCP 接口导出每个地址前 100 条、目标 1 条、后 100 条 opcode，各写一个 `opcode_<ADDRESS>.md` 文件。运行时不再读取或解析报告文件。

**架构方案：** Python 标准库脚本启动现有 Gateway，通过 stdio JSON-RPC/MCP 发现 CE 实例、确认用户已手动附加 victoria3，再逐地址调用 `code_decode` 和 `code_disassemble`。CE 完成反汇编，Python 负责固化列表校验、结果校验、残留核对与本地文件写入。无需修改 CE、MCP 插件或现有 Lua 入口，也无需额外的 CE Lua 导出器。

**技术栈：** Windows x64、已安装的 Cheat Engine 7.7、CheatEngine.Mcp 2.0.0-beta.2 分发包、Python 3.11+ 标准库、MCP stdio、UTF-8 Markdown/JSON、unittest。

## 全局约束

- 使用中文进行对话输出。
- 使用中文进行代码注释，但是不要使用中文日志。
- CheatEngine 7.7 安装路径在 `C:\Program Files\Cheat Engine`。
- 用户原始需求：`Docs\testdata-2026-10-1-10-58.md` 里有本次启动 victoria3.exe 进程时新获取的地址数据。请先以完成一个自动化脚本。可以通过 CE 获取所有 “The following opcodes accessed XXX“ 下面的地址附近前后100行的opcode。并且每个输出一个文件，例如 "opcode_7FF71C8D9218.md" 中存放 7FF71C8D9218 地址附近前后100行的 opcode。
- 本轮交付是重写实施计划；以下未勾选任务属于后续实施范围，不表示脚本已经实现或真实导出已经完成。
- 目标地址与原始机器码固化在 `Scripts/run_opcode_export.py` 头部的 `TARGETS` 列表（9 对，来源为本次报告）。运行时不读取、不解析报告文件，不通过 glob 自动选择其他报告；游戏重启后地址失效时，需重新采集报告并手动更新该列表。“行”按完整反汇编指令计数，不按字节或 Markdown 物理行计数。
- 仅采集代码上下文；不重新捕获访问事件、不设置断点、不修改游戏内存、不暂停游戏、不注入 Lua/AA，不进行贸易容量因果分析。
- 脚本全程仅调用只读工具（`code_decode`、`code_disassemble`、`instance_list`、`runtime_get_info`、`runtime_get_overview`），并在代码中作为显式常量 `READ_ONLY_TOOLS` 维护；不写内存、不设断点、不注入、不分配、不附加/分离。所有失败路径都不需要也不执行补偿性写操作，因为从未产生内存修改。attach 改为手动后，原计划中唯一改变 CE 状态的操作（`process_attach` 超时后无法确认是否已附加）已被消除；不自动回收用户资源。
- 启动和回收的子进程仅为本脚本的 Gateway；不启动、关闭或重启 CE/游戏，不回收用户原有 Gateway。
- 脚本不附加、不切换、不分离；CE 必须已由用户手动附加到 victoria3，否则以退出码 2 失败。
- 导出前从 `runtime_get_overview` 记录 `resourceCount/jobCount`（manifest 字段 `ceResourcesBefore`）；所有退出路径都在 main 的统一收尾中、关闭客户端之前恰好执行一次残留核对，结构化结果写入 manifest 字段 `residueCheck`（unchanged/changed/unavailable/skipped，含 before/after/时间/原因）：变化时打 WARN 但退出码语义不变；无法确认且数据全成功时退出码 0 升为 3；中断/连接失效记 skipped 原因，不重连、不阻塞。只读工具不会产生 CE 资源，变化来源交由验收人工核查。
- 不硬编码当前 instanceId、游戏 PID 或后端 HTTP 端口，不直接读取实例注册目录中的认证信息。
- 绝对地址和原始机器码必须在当前进程重新验证；字节匹配是防止使用过期地址的检查，不是证明与报告生成时为同一进程的证据。
- 前置指令边界来自 CE 的估计。成功文件必须声明这一点；连续性检查也不能证明这些字节曾作为真实控制流执行。
- 所有成功窗口必须严格为 201 条、目标在零基索引 100。失败不能用“最多 100 条”、填充假数据或仅导出后半窗口冒充完成。
- 使用每次运行独立子目录和原子写文件，避免上一次的成功文件掩盖本次失败。

---

## 1. 已核实事实与实现依据

### 1.1 2026-10-01 本轮只读连接核验

通过仓库中的 `McpExternals/CheatEngine.Mcp-2.0.0-beta.2-win-x64/CheatEngine.Mcp.Gateway.exe` 实际执行初始化、`tools/list`、`instance_list`、`runtime_get_overview` 和 `process_list`：

| 项目 | 实际结果 |
| --- | --- |
| MCP 协议 | `2025-06-18` |
| 网关 | `CheatEngine.Mcp.Gateway 2.0.0.0` |
| CE 实例 | `ce-72480-42f4ba0154dd4fbd8087223e0f808fda` |
| CE PID | `72480` |
| 实例发现 | 1 个，`discoveryIncomplete=false` |
| CE 当前目标 | `process.isOpen=false` |
| 游戏枚举 | `processId=43884`，`processName=victoria3` |
| 保留资源 / 作业 | `resourceCount=0`，`jobCount=0` |

上述标识仅记录本轮事实，不能写入默认配置。这里只证明连接和枚举可用；历史核验时未执行 `process_attach`，未对游戏进行实际窗口导出。现方案已改为手动附加：脚本不再枚举进程、不调用 `process_attach`，也不再使用 `process_list`；`victoria3` 与 `victoria3.exe` 按可选扩展名规范化比较（仅用于确认 CE 已手动附加的目标）。

### 1.2 直接使用已存在的接口

源码依据位于外部源码树，仅供核对，不在本项目修改：

- `D:\cebuild\CheatEngine.Mcp\srcs\CheatEngine.Mcp.Tools\Code\CodeTools.cs`：`Disassemble`、`Decode`。
- `D:\cebuild\CheatEngine.Mcp\srcs\CheatEngine.Mcp.Tools\Code\CodeRecords.cs`：`CodeDisassembly`、`CodeInstruction`、`CodeDecodeResult`。
- `D:\cebuild\CheatEngine.Mcp\srcs\CheatEngine.Mcp.Hosting\Gateway\InstanceListResult.cs`。
- `D:\cebuild\CheatEngine.Mcp\libs\CheatEngine.Mcp.Core\Contract\ToolFailureMapping.cs`。
- 本仓库分发包 `README.md`：必须通过 Gateway stdio 连接；插件启用不等于附加游戏。

实际 `tools/list` 与源码一致：

```json
{
  "name": "code_disassemble",
  "arguments": {
    "instanceId": "<本次 instance_list 返回的唯一或显式指定实例>",
    "address": "7FF777D19218",
    "before": 100,
    "count": 101
  }
}
```

这里 `count` 是从目标开始的前向指令数，包含目标自身；总条数为 `before + count = 201`。实现先估计前置起点，再从起点连续解码 201 条，所以仍必须验证目标确实落在第 101 行。单次上限为 `before + count <= 1024`。

响应读取 `result.structuredContent`，得到：

```text
code_disassemble -> {address: str, instructions: list[Instruction]}
code_decode      -> {instruction: Instruction, length: int}
Instruction      -> {address, addressText, opcode, extra, text, bytes: str, size: int}
```

`address`、`bytes` 均为大写十六进制，无 `0x`；`bytes` 没有分隔符。展示时再为 bytes 插入空格。JSON-RPC `error` 和 MCP `result.isError` 都是失败，不能把它们当成空的成功窗口。

### 1.3 地址基线与固化列表

固化列表的来源与回归基线：目标地址不再由运行时解析报告得到，而是固化在 `Scripts/run_opcode_export.py` 的 `TARGETS` 列表中。下表为最后读取到的 6 + 3 条记录，`goal1` 中旧地址仅为命名示例。

所有地址按报告原文保留，包括 `7FF7777927334`、`7FF7777CED5C9`、`7FF7777CED5BB`、`7FF7777927358`；不根据其他地址的长度擅自删减十六进制位。若 CE 读取失败或 bytes 不匹配，要求重新采集报告并手动更新 `TARGETS`，不能自动猜测替换地址。

标题中的 `3A484D9F8B8`、`3A484D9F8BC` 是被访问的**数据地址**，只作为来源背景记录，不进入脚本或 `TARGETS`；不能拿它们做反汇编导出目标。Count、中文分组说明、UI 访问以及暂停后增加一次的记录都不能导致指令被漏掉，分组关系已体现在下表。

| 来源数据地址（背景） | 固化的指令地址 | 原始机器码（expected_bytes） |
| --- | --- | --- |
| `3A484D9F8B8`（6 个） | `7FF777D19218` | `496385581D0000` |
|  | `7FF777D1B9C7` | `8986581D0000` |
|  | `7FF777D1BA8E` | `442BBE581D0000` |
|  | `7FF7777927334` | `486390581D0000` |
|  | `7FF7777CED5C9` | `418B86581D0000` |
|  | `7FF777D01346` | `486387581D0000` |
| `3A484D9F8BC`（3 个） | `7FF777D1B9DA` | `89865C1D0000` |
|  | `7FF7777CED5BB` | `418B865C1D0000` |
|  | `7FF7777927358` | `2B905C1D0000` |

## 2. 文件职责和交付边界

本轮仅替换本计划。实施时新增下列文件，不修改空的 `Scripts/main.lua`、现有断点脚本、`AGENTS.md` 或用户的 `Docs/mcp_setup.md`。

| 文件 | 职责 |
| --- | --- |
| `Scripts/ce_mcp_client.py` | 同步 stdio MCP 客户端；握手、工具目录、请求 ID、超时、错误和 Gateway 生命周期 |
| `Scripts/opcode_report.py` | 机器码和窗口校验、Markdown 渲染、原子文件写入（不解析报告） |
| `Scripts/run_opcode_export.py` | CLI、固化目标列表与只读工具常量、实例选择、会话一致性、逐地址采集、统一收尾（残留核对）、汇总和退出码 |
| `Scripts/tests/test_ce_mcp_client.py` | 使用本地假 stdio 服务验证传输，不需要 CE |
| `Scripts/tests/test_opcode_report.py` | 窗口、锚点与原子写的离线边界测试（不读取报告） |
| `Scripts/tests/test_opcode_export.py` | 假 MCP 的固化列表一致性、手动附加前提、失败继续、会话变化、只读调用、统一收尾残留状态、文件与退出码测试 |
| `Docs/opcode_export.md` | 安装前提、执行命令、输出说明和故障处理 |
| `Output/opcodes/<UTC时间_随机后缀>/` | 运行产物：9 个目标 Markdown、`index.md`、`manifest.json`、`gateway.stderr.log` |

不新增 JSON 配置、不增加 pip 依赖，不在计划中要求提交运行产物。

## 3. 实施任务

### 任务1：交付可独立测试的 Gateway stdio 客户端

**涉及文件：** 新建 `Scripts/ce_mcp_client.py`、`Scripts/tests/test_ce_mcp_client.py`。

**接口依赖：**
- 输入：`argv: list[str]`、`timeout: float`（每个请求的绝对截止时间）、`log_path: Path`。
- 输出：`McpClient.start() -> McpClient`、`tools() -> dict[str, dict]`、`call(name: str, arguments: dict) -> dict`、`close() -> None`。
- 错误类型：`TransportError` 表示连接不可继续；`ToolError` 保存 `payload` 与可读取的 `kind`，表示服务返回的工具错误。

**执行步骤：**

- [x] 新建以下文件。客户端只允许一个在途请求，逐行读取 stdio JSON；stderr 单独落盘，不能阻塞 stdout。通知不占请求 ID，未知服务端请求返回 `-32601`；超时、EOF、无效响应使连接失效，不复用连接或盲目重发请求。

#### 文件：Scripts/ce_mcp_client.py

```python
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
        self.payload = payload
        detail = payload.get("error", payload)
        self.kind = detail.get("kind", "tool_error") if isinstance(detail, dict) else "tool_error"
        super().__init__(json.dumps(payload, ensure_ascii=True))


class McpClient:
    def __init__(self, argv: list[str], timeout: float, log_path: Path):
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
        if self.broken:
            raise TransportError("MCP connection is unusable")
        try:
            self.process.stdin.write(json.dumps(message, ensure_ascii=True) + "\n")
            self.process.stdin.flush()
        except (OSError, ValueError) as exc:
            self.broken = True
            raise TransportError("gateway stdin closed") from exc

    def rpc(self, method: str, params: dict) -> dict:
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
```

- [x] 新建下面的测试文件。假服务覆盖握手、通知、目录分页、结构化结果、文本 JSON 兼容、工具错误、请求超时、EOF 和异常请求 ID；测试只启动自己的 Python 子进程。

#### 文件：Scripts/tests/test_ce_mcp_client.py

```python
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ce_mcp_client import McpClient, ToolError, TransportError

SERVER = r'''
import json, sys, time
for line in sys.stdin:
    request = json.loads(line)
    if "id" not in request:
        continue
    method, params = request["method"], request["params"]
    if method == "initialize":
        result = {"protocolVersion": "2025-06-18"}
    elif method == "tools/list":
        result = {"tools": [{"name": "b"}]} if params else {
            "tools": [{"name": "a"}], "nextCursor": "page2"}
    else:
        name = params["name"]
        if name == "slow":
            time.sleep(3)
        if name == "eof":
            sys.exit(0)
        if name == "error":
            result = {"isError": True, "structuredContent": {
                "error": {"kind": "memory_read_failed", "message": "unreadable"}}}
        elif name == "text":
            result = {"content": [{"type": "text", "text": "{\"ok\":true}"}]}
        else:
            result = {"structuredContent": {"ok": True}}
        if name == "wrong_id":
            request["id"] += 1
    print(json.dumps({"jsonrpc": "2.0", "method": "notifications/message"}), flush=True)
    print(json.dumps({"jsonrpc": "2.0", "id": request["id"], "result": result}), flush=True)
'''


class ClientTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        server = root / "server.py"
        server.write_text(SERVER, encoding="utf-8")
        self.client = McpClient([sys.executable, str(server)], 2, root / "stderr.log")
        self.addCleanup(self.client.close)
        self.client.start()

    def test_handshake_pagination_and_results(self):
        self.assertEqual(set(self.client.tools()), {"a", "b"})
        self.assertEqual(self.client.call("ok", {}), {"ok": True})
        self.assertEqual(self.client.call("text", {}), {"ok": True})

    def test_tool_failure(self):
        with self.assertRaises(ToolError) as caught:
            self.client.call("error", {})
        self.assertEqual(caught.exception.kind, "memory_read_failed")
        self.assertEqual(self.client.call("ok", {}), {"ok": True})

    def test_timeout_invalidates_connection(self):
        self.client.timeout = 0.05
        with self.assertRaisesRegex(TransportError, "timed out"):
            self.client.call("slow", {})
        with self.assertRaises(TransportError):
            self.client.call("ok", {})

    def test_eof(self):
        with self.assertRaises(TransportError):
            self.client.call("eof", {})

    def test_wrong_id(self):
        with self.assertRaisesRegex(TransportError, "response id"):
            self.client.call("wrong_id", {})


if __name__ == "__main__":
    unittest.main()
```

- [x] 运行 `python -m unittest discover -s Scripts/tests -p test_ce_mcp_client.py -v`，预期全部通过。
- [x] 独立产出判定：不用启动 CE 即可验证传输；连接真实 Gateway 时能完成 `tools/list` 和 `instance_list`，关闭客户端后 CE/游戏仍在运行。


### 任务2：交付窗口校验和文件渲染

**涉及文件：** 新建 `Scripts/opcode_report.py`、`Scripts/tests/test_opcode_report.py`。

**接口依赖：**
- 输入：CE 返回的结构化对象；此模块不连接 CE，也不读取报告文件。
- 输出：`Target(address: str, expected_bytes: str)`（固化列表的元素类型）。
- `validate_anchor(target: Target, payload: dict) -> None` 检查 `code_decode` 结果。
- `validate_window(target: Target, payload: dict) -> list[dict]` 返回严格校验后的 201 条指令。
- `render_target(target: Target, record: dict, rows: list[dict], metadata: dict) -> str`；`atomic_text(path: Path, text: str) -> None`。
- `hex_address(value) / hex_bytes(value) -> str` 供固化列表校验复用。
- `ValueError` 表示输入或采集结果不能满足完整窗口合同；由编排层决定退出还是记录单地址失败。

**执行步骤：**

- [x] 新建以下文件。模块内不做报告解析、不读取任何输入文件；只做机器码/窗口校验、Markdown 渲染与原子写文件。

#### 文件：Scripts/opcode_report.py

```python
import os
import re
import tempfile
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Target:
    address: str
    expected_bytes: str


def hex_address(value: str) -> str:
    if not isinstance(value, str) or not re.fullmatch(r"(?:0x)?[0-9A-Fa-f]+", value):
        raise ValueError("invalid hexadecimal address")
    number = int(value, 16)
    if not 0 < number < 2**64:
        raise ValueError("address outside uint64 range")
    return f"{number:X}"


def hex_bytes(value: str) -> str:
    value = re.sub(r"\s+", "", value).upper()
    if not re.fullmatch(r"(?:[0-9A-F]{2}){1,15}", value):
        raise ValueError("invalid x86 instruction bytes")
    return value


def checked_instruction(row: dict) -> tuple[int, int]:
    address = int(hex_address(row["address"]), 16)
    size = row["size"]
    if type(size) is not int or not 1 <= size <= 15:
        raise ValueError("invalid instruction size")
    if len(hex_bytes(row["bytes"])) != size * 2:
        raise ValueError("instruction bytes and size disagree")
    for key in ("addressText", "opcode", "extra", "text"):
        if not isinstance(row[key], str):
            raise ValueError(f"invalid instruction field: {key}")
    opcode = row["opcode"].strip().lower()
    if not opcode or opcode.split()[0] in {"db", "??", "???", "invalid", "(bad)"}:
        raise ValueError("undecodable instruction")
    if address + size >= 2**64:
        raise ValueError("instruction address overflow")
    return address, size


def validate_anchor(target: Target, payload: dict) -> None:
    row = payload["instruction"]
    address, size = checked_instruction(row)
    if address != int(target.address, 16) or payload["length"] != size:
        raise ValueError("anchor address or length mismatch")
    if hex_bytes(row["bytes"]) != target.expected_bytes:
        raise ValueError("source bytes mismatch; refresh the source report")


def validate_window(target: Target, payload: dict) -> list[dict]:
    if hex_address(payload["address"]) != target.address:
        raise ValueError("response address mismatch")
    rows = payload["instructions"]
    if not isinstance(rows, list) or len(rows) != 201:
        raise ValueError("expected exactly 201 instructions")
    positions, previous_end = [], None
    for index, row in enumerate(rows):
        address, size = checked_instruction(row)
        if previous_end is not None and address != previous_end:
            raise ValueError("instruction window is not contiguous")
        previous_end = address + size
        if address == int(target.address, 16):
            positions.append(index)
    if positions != [100]:
        raise ValueError("target must occur exactly once at index 100")
    if hex_bytes(rows[100]["bytes"]) != target.expected_bytes:
        raise ValueError("target bytes changed or source report is stale")
    return rows


def md(value) -> str:
    return str(value).replace("\r", " ").replace("\n", " ").replace("|", r"\|")


def render_target(target: Target, record: dict, rows: list[dict], metadata: dict) -> str:
    lines = [
        f"# Opcode window {target.address}", "",
        f"- Status: {record['status']}",
        f"- Run: {metadata['runId']}",
        f"- CE instance: {metadata['instanceId']}",
        f"- Target PID: {metadata['processId']}",
        f"- Captured at: {record['capturedAt']}",
        "- Requested: 100 before + target + 100 after",
        "- Boundary method: CE estimated predecessors; continuity checked on success",
        "- Capture mode: live reads, not an atomic process snapshot",
        "- Expected target bytes: " + target.expected_bytes, "",
    ]
    if record["status"] != "success":
        return "\n".join(lines + ["## Failure", "", md(record["error"]), ""])
    if len(rows) != 201:
        raise ValueError("refusing to render an incomplete successful window")
    lines += ["## Instructions", "",
              "| Offset | Address | CE address | Bytes | Opcode | Extra | Marker |",
              "| ---: | --- | --- | --- | --- | --- | --- |"]
    for index, row in enumerate(rows):
        byte_text = " ".join(f"{b:02X}" for b in bytes.fromhex(row["bytes"]))
        marker = "TARGET" if index == 100 else ""
        values = [index - 100, row["address"], row["addressText"],
                  byte_text, row["opcode"], row["extra"], marker]
        lines.append("| " + " | ".join(md(value) for value in values) + " |")
    return "\n".join(lines) + "\n"


def atomic_text(path: Path, text: str) -> None:
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", newline="\n",
            dir=path.parent, prefix=path.name + ".", suffix=".tmp", delete=False,
        ) as handle:
            temporary = Path(handle.name)
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
```

- [x] 新建下面的单元测试。不读取真实报告文件；固化列表一致性回归放在 `test_opcode_export.py`，微型边界样本内联在测试中。

#### 文件：Scripts/tests/test_opcode_report.py

```python
import copy
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from opcode_report import Target, atomic_text, validate_anchor, validate_window


def window(address="1064"):
    center = int(address, 16)
    return {
        "address": address,
        "instructions": [
            {"address": f"{center - 100 + i:X}", "addressText": f"test.exe+{i:X}",
             "opcode": "nop", "extra": "", "text": "nop", "bytes": "90", "size": 1}
            for i in range(201)
        ],
    }


class WindowTests(unittest.TestCase):
    def test_valid_window(self):
        self.assertEqual(len(validate_window(Target("1064", "90"), window())), 201)

    def test_bad_windows(self):
        base = window()
        variants = []
        short = copy.deepcopy(base)
        short["instructions"].pop()
        variants.append(short)
        for field, value in (("size", 0), ("bytes", "9090"), ("opcode", "db 90"),
                             ("address", "1064")):
            bad = copy.deepcopy(base)
            bad["instructions"][0][field] = value
            variants.append(bad)
        changed = copy.deepcopy(base)
        changed["instructions"][100]["bytes"] = "CC"
        variants.append(changed)
        shifted = window("1065")
        shifted["address"] = "1064"
        variants.append(shifted)
        for bad in variants:
            with self.subTest(bad=bad["instructions"][0]), self.assertRaises(ValueError):
                validate_window(Target("1064", "90"), bad)

    def test_anchor_validation(self):
        row = window()["instructions"][100]
        validate_anchor(Target("1064", "90"), {"instruction": row, "length": 1})
        cases = (
            {"instruction": {**row, "address": "1065"}, "length": 1},
            {"instruction": {**row, "bytes": "CC"}, "length": 1},
            {"instruction": {**row, "size": 2}, "length": 2},
            {"instruction": row, "length": 2},
        )
        for payload in cases:
            with self.subTest(payload=payload), self.assertRaises(ValueError):
                validate_anchor(Target("1064", "90"), payload)

    def test_atomic_write_failure_keeps_old_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "opcode_1064.md"
            atomic_text(path, "old")
            with patch("opcode_report.os.replace", side_effect=PermissionError):
                with self.assertRaises(PermissionError):
                    atomic_text(path, "new")
            self.assertEqual(path.read_text(encoding="utf-8"), "old")
            self.assertEqual(list(Path(directory).glob("*.tmp")), [])


if __name__ == "__main__":
    unittest.main()
```

- [x] 运行 `python -m unittest discover -s Scripts/tests -p test_opcode_report.py -v`，预期全部通过。
- [x] 独立产出判定：离线校验 201 条窗口；对 200 条、错位目标、机器码变化、锚点不一致、非连续地址、无效解码拒绝生成成功窗口。


### 任务3：交付一条命令完成导出的编排器

**涉及文件：** 新建 `Scripts/run_opcode_export.py`、`Scripts/tests/test_opcode_export.py`、`Docs/opcode_export.md`。

**接口依赖：**
- 依赖 `McpClient`、`TransportError`、`ToolError`。
- 依赖 `Target`、`hex_address`、`hex_bytes`、`validate_anchor`、`validate_window`、`render_target`、`atomic_text`。
- 输出：`TARGETS` 固化列表与 `load_targets() -> list[Target]`；`select_instance(client, wanted: str | None) -> str`；`bind_target(client, instance_id: str) -> tuple[dict, dict]`（会话 baseline 与 `resourceCount/jobCount` 基线）；`run_exports(client, instance_id: str, baseline: dict, targets: list[Target], output: Path, metadata: dict) -> int`；`main(argv=None) -> int`。
- 常量：`TARGETS`（固化目标）、`REQUIRED_TOOLS`（工具与必需参数）、`READ_ONLY_TOOLS`（只读工具白名单，集成测试据此断言调用集合）。
- `baseline` 是 `runtimeEpoch/processId/selectionEpoch/pointerSize` 字典。插件重启、目标切换或失去目标均停止后续 MCP 采集。
- 退出码：`0` 全部完整成功且收尾残留核对已取得结论（unchanged/changed）；`1` 至少一个地址校验或工具采集失败；`2` 固化列表/配置/实例/未附加/目标错误/文件系统失败；`3` MCP 传输失效、运行期间会话改变，或收尾残留核对未能完成（数据可能已全部成功）；`130` 用户中断。

**执行步骤：**

- [x] 新建以下文件。所有默认路径基于 `__file__` 定位仓库，不依赖启动目录。目标来自脚本头部 `TARGETS` 固化列表，连接 CE 前先校验格式；不附加、不切换、不分离，CE 必须已由用户手动附加 victoria3；多个 CE 用 `--instance-id` 消除歧义，不能选择“第一个”。

#### 文件：Scripts/run_opcode_export.py

```python
import argparse
import json
import sys
import uuid
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from ce_mcp_client import McpClient, ToolError, TransportError
from opcode_report import (
    Target, atomic_text, hex_address, hex_bytes, md, render_target,
    validate_anchor, validate_window,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_GATEWAY = (
    ROOT / "McpExternals/CheatEngine.Mcp-2.0.0-beta.2-win-x64/CheatEngine.Mcp.Gateway.exe"
)
# 目标地址与原始机器码（地址, expected_bytes）。由用户手动维护，来源为本次报告
# Docs/testdata-2026-10-1-10-58.md；游戏重启后地址失效时，重新采集报告并手动更新本列表。
TARGETS = [
    ("7FF777D19218", "496385581D0000"),
    ("7FF777D1B9C7", "8986581D0000"),
    ("7FF777D1BA8E", "442BBE581D0000"),
    ("7FF7777927334", "486390581D0000"),
    ("7FF7777CED5C9", "418B86581D0000"),
    ("7FF777D01346", "486387581D0000"),
    ("7FF777D1B9DA", "89865C1D0000"),
    ("7FF7777CED5BB", "418B865C1D0000"),
    ("7FF7777927358", "2B905C1D0000"),
]
REQUIRED_TOOLS = {
    "instance_list": set(),
    "runtime_get_info": {"instanceId"},
    "runtime_get_overview": {"instanceId"},
    "code_decode": {"instanceId", "address"},
    "code_disassemble": {"instanceId", "address", "before", "count"},
}
# 只读工具白名单：脚本只允许调用这些工具，集成测试断言真实调用集合是其子集。
READ_ONLY_TOOLS = frozenset({
    "instance_list", "runtime_get_info", "runtime_get_overview",
    "code_decode", "code_disassemble",
})
SESSION_ERRORS = {"target_changed", "not_attached", "stopping", "invalid_state"}


class SessionChanged(RuntimeError):
    pass


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def process_name(value) -> str:
    return (value or "").replace("\\", "/").rsplit("/", 1)[-1].casefold().removesuffix(".exe")


def fingerprint(overview: dict) -> dict:
    process = overview["process"]
    if not process["isOpen"] or process_name(process.get("processName")) != "victoria3":
        raise SessionChanged("victoria3 is not the selected process")
    if process.get("pointerSize") != 8 or process.get("selectionEpoch") is None:
        raise SessionChanged("target bitness or selection identity is unavailable")
    return {
        "runtimeEpoch": overview["runtime"]["epoch"],
        "processId": process["processId"],
        "selectionEpoch": process["selectionEpoch"],
        "pointerSize": process["pointerSize"],
    }


def resources(overview: dict) -> dict:
    # 只读工具不会产生 CE 资源；仅记录计数用于运行期残留核对。
    return {"resourceCount": overview["resourceCount"], "jobCount": overview["jobCount"]}


def load_targets() -> list[Target]:
    # 在连接 CE 前校验固化列表；非法条目以 ValueError 失败，不接触 CE。
    targets = [Target(hex_address(address), hex_bytes(expected)) for address, expected in TARGETS]
    if not targets:
        raise ValueError("TARGETS list is empty")
    if len({target.address for target in targets}) != len(targets):
        raise ValueError("duplicate address in TARGETS list")
    return sorted(targets, key=lambda target: int(target.address, 16))


def select_instance(client, wanted):
    listing = client.call("instance_list", {})
    if listing["discoveryIncomplete"]:
        raise ValueError("instance discovery incomplete; run again")
    items = listing["instances"]
    if wanted is not None:
        items = [item for item in items if item["instanceId"] == wanted]
    if len(items) != 1:
        raise ValueError("select exactly one CE instance with --instance-id")
    return items[0]["instanceId"]


def bind_target(client, instance_id):
    # CE 已由用户手动附加：这里只做健康检查，不附加、不切换、不分离。
    arguments = {"instanceId": instance_id}
    client.call("runtime_get_info", arguments)
    overview = client.call("runtime_get_overview", arguments)
    process = overview["process"]
    if not process["isOpen"]:
        raise ValueError("victoria3.exe is not attached in CE; attach it manually in Cheat Engine first")
    if process_name(process.get("processName")) != "victoria3":
        raise ValueError("CE is attached to a different target; the script does not switch targets")
    return fingerprint(overview), resources(overview)


def check_session(client, instance_id, baseline):
    current = fingerprint(client.call("runtime_get_overview", {"instanceId": instance_id}))
    if current != baseline:
        raise SessionChanged("CE runtime or target selection changed")


def check_residue(client, instance_id, metadata, interrupted):
    # 统一收尾残留核对：至多执行一次 overview 读取，从不重连，恒返回结构化结果供 manifest 落盘。
    # state：unchanged=计数一致；changed=计数变化；unavailable=尝试核对但失败；skipped=未执行（原因见 reason）。
    result = {
        "state": "skipped", "before": metadata.get("ceResourcesBefore"),
        "after": None, "checkedAt": now(), "reason": None,
    }
    if result["before"] is None:
        result["reason"] = "no resource baseline was established"
        return result
    if client is None:
        result["reason"] = "MCP client was not started"
        return result
    if client.broken:
        result["reason"] = "MCP connection is unusable"
        return result
    if interrupted:
        # 中断可能打断在途请求；复用同一连接不安全：不重连、不阻塞，只记录跳过原因。
        result["reason"] = "interrupted by user"
        return result
    try:
        result["after"] = resources(client.call("runtime_get_overview", {"instanceId": instance_id}))
    except (TransportError, ToolError) as exc:
        result.update(state="unavailable", reason=ascii(str(exc)))
        return result
    except KeyboardInterrupt:
        # 核对期间再次中断：记录不可确认后立即交给收尾清理。
        result.update(state="unavailable", reason="interrupted during residue check")
        return result
    if result["after"] == result["before"]:
        result["state"] = "unchanged"
    else:
        result["state"] = "changed"
        result["reason"] = "read-only tools cannot create CE resources; verify manually"
        print("WARN: CE resourceCount/jobCount changed during export")
    return result


def save_progress(output, metadata, records, status):
    success = sum(record["status"] == "success" for record in records)
    document = {
        **metadata, "status": status, "updatedAt": now(),
        "successCount": success, "failedCount": len(records) - success,
        "processedCount": len(records), "instructionCount": success * 201,
        "results": records,
    }
    atomic_text(output / "manifest.json", json.dumps(document, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# Opcode export index", "",
        f"- Run: {metadata['runId']}", f"- Status: {status}",
        f"- Expected: {metadata['expectedCount']}; success: {success}; failed: {len(records) - success}",
        "", "| Target | Status | File | Error |", "| --- | --- | --- | --- |",
    ]
    for record in records:
        filename = record["file"]
        lines.append(
            f"| {record['address']} | {record['status']} | "
            f"[{filename}]({filename}) | {md(record.get('error', ''))} |"
        )
    atomic_text(output / "index.md", "\n".join(lines) + "\n")


def run_exports(client, instance_id, baseline, targets, output, metadata):
    records, aborted = [], None
    for target in targets:
        rows = []
        record = {
            **asdict(target), "file": f"opcode_{target.address}.md",
            "status": "failed", "capturedAt": now(),
            "beforeCount": 0, "afterCount": 0, "instructionCount": 0,
        }
        try:
            if aborted is not None:
                raise SessionChanged("not attempted after abort: " + aborted)
            check_session(client, instance_id, baseline)
            arguments = {"instanceId": instance_id, "address": target.address}
            validate_anchor(target, client.call("code_decode", arguments))
            payload = client.call("code_disassemble", {
                **arguments, "before": 100, "count": 101,
            })
            rows = validate_window(target, payload)
            validate_anchor(target, client.call("code_decode", arguments))
            check_session(client, instance_id, baseline)
            record.update(status="success", beforeCount=100, afterCount=100, instructionCount=201)
        except (TransportError, SessionChanged) as exc:
            if aborted is None:
                aborted = str(exc)
            record["error"] = str(exc)
        except ToolError as exc:
            record["error"] = str(exc)
            if exc.kind in SESSION_ERRORS:
                aborted = str(exc)
        except (ValueError, KeyError, TypeError) as exc:
            record["error"] = "invalid opcode result: " + str(exc)
        record["capturedAt"] = now()
        atomic_text(output / record["file"], render_target(target, record, rows, metadata))
        records.append(record)
        save_progress(output, metadata, records, "running")
        print(f"INFO: {target.address} {record['status']}")
    # 残留核对不在此处执行：统一收尾（main）覆盖成功、失败与中断等全部退出路径，且恰好执行一次。
    failed = any(record["status"] != "success" for record in records)
    status = "aborted" if aborted else ("failed" if failed else "complete")
    save_progress(output, metadata, records, status)
    return 3 if aborted else (1 if failed else 0)


def positive_int(text):
    value = int(text)
    if value <= 0:
        raise argparse.ArgumentTypeError("value must be positive")
    return value


def main(argv=None):
    parser = argparse.ArgumentParser(description="Export CE opcode windows through MCP")
    parser.add_argument("--output", type=Path, default=ROOT / "Output/opcodes")
    parser.add_argument("--gateway", type=Path, default=DEFAULT_GATEWAY)
    parser.add_argument("--instance-id")
    parser.add_argument("--timeout", type=positive_int, default=30)
    args = parser.parse_args(argv)
    client, output, metadata, instance_id = None, None, None, None
    code, reason = 0, None
    try:
        # 先校验固化列表格式；失败时不创建运行目录、不接触 CE。
        targets = load_targets()
        gateway = args.gateway.resolve()
        if not gateway.is_file():
            raise ValueError("gateway executable does not exist")
        run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ") + "_" + uuid.uuid4().hex[:8]
        output = args.output.resolve() / run_id
        output.mkdir(parents=True, exist_ok=False)
        metadata = {
            "runId": run_id, "startedAt": now(), "expectedCount": len(targets),
            "before": 100, "after": 100,
        }
        save_progress(output, metadata, [], "starting")
        # 先保存客户端对象再启动：启动阶段失败或中断时，finally 仍能回收本次 Gateway。
        client = McpClient([str(gateway)], args.timeout, output / "gateway.stderr.log")
        client.start()
        catalog = client.tools()
        for name, properties in REQUIRED_TOOLS.items():
            if name not in catalog:
                raise ValueError("required MCP tool is missing: " + name)
            available = set(catalog[name]["inputSchema"].get("properties", {}))
            if not properties <= available:
                raise ValueError("incompatible MCP tool schema: " + name)
        instance_id = select_instance(client, args.instance_id)
        baseline, resources_before = bind_target(client, instance_id)
        # 记录 CE 资源基线，供统一收尾中的残留核对使用。
        metadata.update(instanceId=instance_id, ceResourcesBefore=resources_before, **baseline)
        code = run_exports(client, instance_id, baseline, targets, output, metadata)
        print("INFO: output directory " + ascii(str(output)))
    except KeyboardInterrupt:
        code, reason = 130, "interrupted by user"
    except (TransportError, SessionChanged) as exc:
        code, reason = 3, str(exc)
    except (OSError, ValueError, ToolError, KeyError, TypeError) as exc:
        code, reason = 2, str(exc)
    finally:
        # 统一收尾：所有退出路径都在关闭客户端之前执行一次残留核对；核对不得覆盖原始退出码。
        residue = None
        try:
            if metadata is not None:
                residue = check_residue(client, instance_id, metadata, interrupted=(code == 130))
        except BaseException as exc:
            # 收尾自身异常（含再次 Ctrl+C）只记录不可确认状态，不覆盖原始退出原因。
            residue = {
                "state": "unavailable", "before": metadata.get("ceResourcesBefore"),
                "after": None, "checkedAt": now(),
                "reason": "residue check crashed: " + ascii(str(exc)),
            }
            print("ERROR: residue check failed: " + ascii(str(exc)), file=sys.stderr)
        if metadata is not None:
            metadata["residueCheck"] = residue
            if code == 0 and residue["state"] == "unavailable":
                # 数据已完整导出但残留无法确认：不以 0 结束，按传输失效语义返回 3，不重连。
                code = 3
                print("ERROR: residue check could not be completed; CE resources are unverified",
                      file=sys.stderr)
        if client is not None:
            client.close()
    if reason is not None:
        print("ERROR: export stopped: " + ascii(reason), file=sys.stderr)
    if output is not None and metadata is not None:
        try:
            # 保留已有逐地址结果，并入统一收尾的残留核对结果；失败路径同时更新失败状态。
            path = output / "manifest.json"
            saved = json.loads(path.read_text(encoding="utf-8")) if path.exists() else metadata
            saved["residueCheck"] = metadata["residueCheck"]
            if reason is not None:
                saved.update(status="interrupted" if code == 130 else "aborted", error=reason)
            saved["updatedAt"] = now()
            atomic_text(path, json.dumps(saved, ensure_ascii=False, indent=2) + "\n")
            save_progress(output, saved, saved.get("results", []), saved["status"])
        except (OSError, ValueError):
            print("ERROR: unable to persist final run status", file=sys.stderr)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
```

- [x] 新建集成测试文件；所有目标读写均使用假对象。注意“导出过程中 CE 被切到其他目标”与“单地址无法读取”必须有不同的行为：前者终止后续 MCP 调用，后者继续处理其他目标。另加固化列表一致性测试（`EXPECTED` 副本对照 `TARGETS`）与只读调用集合子集断言。

#### 文件：Scripts/tests/test_opcode_export.py

```python
import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ce_mcp_client import ToolError, TransportError
from opcode_report import Target, atomic_text
from run_opcode_export import (
    READ_ONLY_TOOLS, TARGETS, bind_target, check_residue, load_targets, main,
    run_exports, select_instance,
)
from test_opcode_report import window

# 固化列表的测试内独立副本：与 run_opcode_export.TARGETS 不一致即视为误改。
EXPECTED = [
    ("7FF777D19218", "496385581D0000"),
    ("7FF777D1B9C7", "8986581D0000"),
    ("7FF777D1BA8E", "442BBE581D0000"),
    ("7FF7777927334", "486390581D0000"),
    ("7FF7777CED5C9", "418B86581D0000"),
    ("7FF777D01346", "486387581D0000"),
    ("7FF777D1B9DA", "89865C1D0000"),
    ("7FF7777CED5BB", "418B865C1D0000"),
    ("7FF7777927358", "2B905C1D0000"),
]


class FakeMcp:
    def __init__(self):
        self.calls = []
        self.broken = False
        self.open = True
        self.pid = 42
        self.name = "victoria3"
        self.epoch = 1
        self.fail = None
        self.timeout = None
        self.change = None
        self.stale = None
        self.interrupt = None
        self.overview_calls = 0
        self.overview_fail_at = None
        self.resource_change_at = None
        self.instances = [{"instanceId": "ce-test"}]
        self.resources = {"resourceCount": 0, "jobCount": 0}

    def tools(self):
        properties = {"instanceId": {}, "address": {}, "before": {}, "count": {}}
        return {
            name: {"inputSchema": {"properties": dict(properties)}}
            for name in READ_ONLY_TOOLS
        }

    def overview(self):
        self.overview_calls += 1
        if self.overview_fail_at == self.overview_calls:
            self.broken = True  # 模拟真实客户端：传输超时后连接失效。
            raise TransportError("MCP request timed out")
        if self.resource_change_at == self.overview_calls:
            self.resources = {"resourceCount": 1, "jobCount": 0}
        return {
            "runtime": {"epoch": 1},
            "process": {
                "isOpen": self.open, "processId": self.pid, "processName": self.name,
                "pointerSize": 8, "selectionEpoch": self.epoch,
            },
            "resourceCount": self.resources["resourceCount"],
            "jobCount": self.resources["jobCount"],
        }

    def call(self, name, arguments):
        self.calls.append((name, dict(arguments)))
        if name == "instance_list":
            return {"instances": self.instances, "discoveryIncomplete": False}
        if name == "runtime_get_info":
            return {}
        if name == "runtime_get_overview":
            return self.overview()
        if self.interrupt is not None and arguments.get("address") == self.interrupt:
            raise KeyboardInterrupt()
        address = arguments["address"]
        if name == "code_decode":
            row = window(address)["instructions"][100]
            if address == self.stale:
                row["bytes"] = "CC"
            return {"instruction": row, "length": 1}
        if name == "code_disassemble":
            assert arguments["before"] == 100 and arguments["count"] == 101
            if address == self.timeout:
                self.broken = True
                raise TransportError("MCP request timed out")
            if address == self.fail:
                raise ToolError({"error": {"kind": "memory_read_failed", "message": "unreadable"}})
            if address == self.change:
                self.epoch += 1
            return window(address)
        raise AssertionError("unexpected tool: " + name)


class Starter:
    # 替代 run_opcode_export.McpClient：把假客户端接入完整 main 流程，并记录启动/关闭。
    def __init__(self, client):
        self.client = client
        self.started = False
        self.closed = False

    @property
    def broken(self):
        return self.client.broken

    def start(self):
        self.started = True
        return self

    def tools(self):
        return self.client.tools()

    def call(self, name, arguments):
        return self.client.call(name, arguments)

    def close(self):
        self.closed = True


class FakePipe:
    # 仅在启动中断测试中替代真实管道：记录关闭调用，不启动真实进程。
    def __init__(self):
        self.closed = False

    def write(self, text):
        pass

    def flush(self):
        pass

    def close(self):
        self.closed = True

    def __iter__(self):
        return iter(())


class FakeGatewayProcess:
    def __init__(self):
        self.stdin = FakePipe()
        self.stdout = FakePipe()
        self.wait_calls = 0
        self.terminate_calls = 0
        self.kill_calls = 0

    def wait(self, timeout=None):
        self.wait_calls += 1
        return 0

    def terminate(self):
        self.terminate_calls += 1

    def kill(self):
        self.kill_calls += 1
        return None


class ExportTests(unittest.TestCase):
    def export(self, client):
        baseline, resources_before = bind_target(client, "ce-test")
        targets = [Target("1064", "90"), Target("2064", "90")]
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            metadata = {
                "runId": "test-run", "instanceId": "ce-test", "processId": 42,
                "expectedCount": 2, "ceResourcesBefore": resources_before,
            }
            code = run_exports(client, "ce-test", baseline, targets, output, metadata)
            manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
            files = {p.name: p.read_text(encoding="utf-8") for p in output.glob("opcode_*.md")}
            self.assertEqual(len(files), 2)
            self.assertEqual(list(output.glob("*.tmp")), [])
            return code, manifest, files

    def run_main(self, client, targets=(("1064", "90"),)):
        # 以假客户端走完整 main：统一收尾、manifest 与退出码都在覆盖范围内。
        starter = Starter(client)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            gateway = root / "gateway.exe"
            gateway.write_text("fake", encoding="utf-8")
            with patch("run_opcode_export.McpClient", return_value=starter), \
                    patch("run_opcode_export.TARGETS", list(targets)):
                code = main(["--gateway", str(gateway), "--output", str(root / "out")])
            manifests = list((root / "out").glob("*/manifest.json"))
            self.assertEqual(len(manifests), 1)
            manifest = json.loads(manifests[0].read_text(encoding="utf-8"))
        return code, manifest, starter

    def test_fixed_target_list_matches_report(self):
        self.assertEqual(list(TARGETS), EXPECTED)
        targets = load_targets()
        self.assertEqual(len(targets), 9)
        self.assertEqual({t.address for t in targets}, {a for a, _ in EXPECTED})
        self.assertEqual(
            next(t.expected_bytes for t in targets if t.address == "7FF777D19218"),
            "496385581D0000",
        )

    def test_invalid_fixed_list_rejected_before_ce(self):
        for invalid in ([], [("ZZZZ", "90")], [("1064", "90"), ("1064", "90")]):
            with self.subTest(invalid=invalid), patch("run_opcode_export.TARGETS", invalid):
                with self.assertRaises(ValueError):
                    load_targets()

    def test_success(self):
        code, result, files = self.export(FakeMcp())
        self.assertEqual(code, 0)
        self.assertEqual(result["status"], "complete")
        self.assertEqual(result["instructionCount"], 402)
        self.assertEqual(result["successCount"], 2)
        for text in files.values():
            self.assertEqual(text.count("| TARGET |"), 1)
            self.assertEqual(sum(line.startswith("| ") for line in text.splitlines()), 203)
            self.assertIn("CE estimated predecessors", text)
            self.assertNotIn("## Sources", text)

    def test_one_bad_address_does_not_block_next(self):
        client = FakeMcp()
        client.fail = "1064"
        code, result, files = self.export(client)
        self.assertEqual(code, 1)
        self.assertEqual(result["successCount"], 1)
        self.assertNotIn("## Instructions", files["opcode_1064.md"])
        self.assertIn("## Instructions", files["opcode_2064.md"])

    def test_stale_bytes_skip_window_call(self):
        client = FakeMcp()
        client.stale = "1064"
        code, result, _ = self.export(client)
        self.assertEqual(code, 1)
        self.assertEqual(result["successCount"], 1)
        self.assertFalse(any(
            name == "code_disassemble" and args["address"] == "1064"
            for name, args in client.calls
        ))

    def test_transport_and_session_abort_remaining_reads(self):
        for field in ("timeout", "change"):
            client = FakeMcp()
            setattr(client, field, "1064")
            code, result, _ = self.export(client)
            self.assertEqual(code, 3)
            self.assertEqual(result["status"], "aborted")
            self.assertEqual(result["successCount"], 0)
            self.assertFalse(any(args.get("address") == "2064" for _, args in client.calls))

    def test_manual_attach_is_required(self):
        client = FakeMcp()
        client.open = False
        with self.assertRaises(ValueError) as caught:
            bind_target(client, "ce-test")
        self.assertIn("attach it manually", str(caught.exception))
        self.assertFalse(any(name == "process_attach" for name, _ in client.calls))
        client.open = True
        baseline, resources_before = bind_target(client, "ce-test")
        self.assertEqual(baseline["processId"], 42)
        self.assertEqual(resources_before, {"resourceCount": 0, "jobCount": 0})

    def test_other_target_is_not_switched(self):
        client = FakeMcp()
        client.name = "notepad.exe"
        with self.assertRaises(ValueError):
            bind_target(client, "ce-test")
        client.name = "victoria3.exe"
        self.assertEqual(bind_target(client, "ce-test")[0]["processId"], 42)
        self.assertFalse(any(name in ("process_attach", "process_list") for name, _ in client.calls))

    def test_multiple_instances_require_selection(self):
        client = FakeMcp()
        client.instances.append({"instanceId": "ce-second"})
        with self.assertRaises(ValueError):
            select_instance(client, None)
        self.assertEqual(select_instance(client, "ce-second"), "ce-second")

    def test_success_calls_stay_read_only(self):
        client = FakeMcp()
        code, _, _ = self.export(client)
        self.assertEqual(code, 0)
        self.assertTrue(client.calls)
        self.assertLessEqual({name for name, _ in client.calls}, set(READ_ONLY_TOOLS))

    def test_resource_change_reports_changed_state(self):
        client = FakeMcp()
        client.resources = {"resourceCount": 1, "jobCount": 0}
        check = check_residue(client, "ce-test", {
            "ceResourcesBefore": {"resourceCount": 0, "jobCount": 0},
        }, interrupted=False)
        self.assertEqual(check["state"], "changed")
        self.assertEqual(check["after"], {"resourceCount": 1, "jobCount": 0})

    def test_success_records_unchanged_residue(self):
        client = FakeMcp()
        code, manifest, starter = self.run_main(client)
        self.assertEqual(code, 0)
        self.assertEqual(manifest["status"], "complete")
        check = manifest["residueCheck"]
        self.assertEqual(check["state"], "unchanged")
        self.assertEqual(check["before"], check["after"])
        self.assertEqual(client.overview_calls, 4)
        self.assertTrue(starter.started and starter.closed)

    def test_final_overview_failure_is_unavailable_and_exit_3(self):
        client = FakeMcp()
        client.overview_fail_at = 4
        buffer = io.StringIO()
        with contextlib.redirect_stderr(buffer):
            code, manifest, _ = self.run_main(client)
        self.assertEqual(code, 3)
        self.assertEqual(manifest["status"], "complete")
        self.assertEqual(manifest["residueCheck"]["state"], "unavailable")
        self.assertIsNone(manifest["residueCheck"]["after"])
        self.assertIn("residue check could not be completed", buffer.getvalue())

    def test_write_failure_still_checks_residue(self):
        client = FakeMcp()
        original = atomic_text

        def failing(path, text):
            if path.name.startswith("opcode_"):
                raise PermissionError("denied")
            return original(path, text)

        with patch("run_opcode_export.atomic_text", side_effect=failing):
            code, manifest, _ = self.run_main(client)
        self.assertEqual(code, 2)
        self.assertEqual(manifest["status"], "aborted")
        self.assertEqual(manifest["residueCheck"]["state"], "unchanged")
        self.assertEqual(client.overview_calls, 4)

    def test_interrupt_skips_check_without_extra_rpc(self):
        client = FakeMcp()
        client.interrupt = "1064"
        code, manifest, _ = self.run_main(client)
        self.assertEqual(code, 130)
        self.assertEqual(manifest["status"], "interrupted")
        self.assertEqual(manifest["residueCheck"]["state"], "skipped")
        self.assertEqual(manifest["residueCheck"]["reason"], "interrupted by user")
        self.assertEqual(client.overview_calls, 2)

    def test_transport_failure_records_skipped(self):
        client = FakeMcp()
        client.timeout = "1064"
        code, manifest, _ = self.run_main(client)
        self.assertEqual(code, 3)
        self.assertEqual(manifest["status"], "aborted")
        self.assertEqual(manifest["residueCheck"]["state"], "skipped")
        self.assertEqual(manifest["residueCheck"]["reason"], "MCP connection is unusable")

    def test_missing_baseline_records_skipped(self):
        client = FakeMcp()
        client.open = False
        code, manifest, _ = self.run_main(client)
        self.assertEqual(code, 2)
        self.assertEqual(manifest["residueCheck"]["state"], "skipped")
        self.assertEqual(
            manifest["residueCheck"]["reason"], "no resource baseline was established")

    def test_resource_change_warns_and_still_exits_0(self):
        client = FakeMcp()
        client.resource_change_at = 4
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            code, manifest, _ = self.run_main(client)
        self.assertEqual(code, 0)
        check = manifest["residueCheck"]
        self.assertEqual(check["state"], "changed")
        self.assertEqual(check["after"], {"resourceCount": 1, "jobCount": 0})
        self.assertIn("WARN: CE resourceCount/jobCount changed", buffer.getvalue())

    def test_interrupt_during_start_reclaims_gateway(self):
        # 初始化握手期间 Ctrl+C：main 仍须回收本次启动的 Gateway 子进程。
        fake = FakeGatewayProcess()
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as directory:
            root = Path(directory)
            gateway = root / "gateway.exe"
            gateway.write_text("fake", encoding="utf-8")
            with patch("ce_mcp_client.subprocess.Popen", return_value=fake), \
                    patch("ce_mcp_client.McpClient.rpc", side_effect=KeyboardInterrupt):
                code = main(["--gateway", str(gateway), "--output", str(root / "out")])
            self.assertEqual(code, 130)
            self.assertTrue(fake.stdin.closed, "gateway stdin pipe was not closed")
            self.assertEqual(fake.kill_calls, 0)
            self.assertGreater(fake.wait_calls + fake.terminate_calls, 0,
                               "gateway child process was never waited for or terminated")
            manifest = json.loads(
                next((root / "out").glob("*/manifest.json")).read_text(encoding="utf-8"))
            self.assertEqual(manifest["status"], "interrupted")


if __name__ == "__main__":
    unittest.main()
```

- [x] 执行 `python -m unittest discover -s Scripts/tests -p "test_*.py" -v`，三个测试文件全部通过。
- [x] 执行 `python Scripts/run_opcode_export.py --help`，确认参数仅包含 `--output`、`--gateway`、`--instance-id`、`--timeout`（无 `--input`、`--pid`、`--attach`）。
- [x] 独立产出判定：假会话能生成独立文件和 manifest；任何一个目标失败均不返回 0；传输超时/会话改变不再读取剩余地址，也不回收 CE/游戏；成功运行的完整调用集合仅含只读工具。


## 4. 真实会话验收与操作说明（任务3的交付组成）

### 4.1 写入操作说明

- [x] 新建 `Docs/opcode_export.md`，写入下列操作内容。实际运行前游戏与 CE 保持打开，CE 插件已启用，并由用户在 CE 中手动附加 victoria3.exe（脚本不代附加）；Gateway 和 CE 由同一 Windows 用户运行。默认包路径已在仓库中，Python 3.11+ 无需安装第三方包。

```markdown
# 导出固化列表中的 opcode 窗口

运行前先在 CE 中手动附加 victoria3.exe；脚本不会自动附加、切换或分离目标。

在 D:\cebuild\ce-custom 中运行：

    python Scripts/run_opcode_export.py

CE 未附加 victoria3，或已附加其他程序时，脚本以退出码 2 停止。
目标地址与原始机器码固化在 Scripts/run_opcode_export.py 的 TARGETS 列表（9 对，来源为 Docs/testdata-2026-10-1-10-58.md）。
游戏重启后地址失效：重新采集报告并手动更新 TARGETS；脚本不读取也不解析报告文件。

自定义输出根目录：

    python Scripts/run_opcode_export.py --output Output/opcodes

多个 CE 实例时，用本次 instance_list 结果提供 --instance-id。
该参数不保存为跨重启默认值。
--timeout 控制单次 MCP 请求的超时秒数，默认 30。
--gateway 可指定另一个同版本 Gateway 可执行文件的完整路径。

脚本最后打印本次输出目录。每次都建立独立子目录，包含：
- opcode_<大写十六进制地址>.md：每个唯一指令地址一个文件。
- index.md：本次所有目标的状态与相对链接。
- manifest.json：实例、目标 PID、选择代次、条数、CE 资源计数基线、收尾核对结果（residueCheck）和错误。
- gateway.stderr.log：本次 Gateway 的诊断输出。

成功文件包含前 100 条、目标指令、后 100 条，共 201 条。
目标标记为 TARGET，Offset 从 -100 到 +100。
CE 前置边界属于估计；结果通过连续性和目标机器码检查，
并不证明实际执行路径，也不是暂停进程得到的原子快照。

退出码 0 表示全部目标完整成功，且收尾残留核对已取得结论（unchanged/changed）。
1 表示至少一个地址失败；2 表示固化列表、配置、实例选择、未附加或文件系统失败；
3 表示传输失效、CE 会话变化，或残留核对未能完成；130 表示用户中断。
manifest 的 status=starting/running 表示未完整结束，不能用于宣告成功。
失败文件只记录错误，不携带冒充完整窗口的指令表。
脚本全程只调用只读工具，不写内存、不设断点、不注入、不附加/分离；
任何失败都不会留下对 CE/游戏内存或状态的修改。
manifest 中的 residueCheck 记录收尾核对状态：changed 表示运行前后 CE 的 resourceCount/jobCount
发生变化，需人工核查；unavailable/skipped 表示无法确认，按 reason 字段排查。

常见处理：
- 无 CE 实例：确认插件仍为 Enabled，并确认 Gateway/CE 为同一用户。
- CE 未附加：先在 CE 中手动附加 victoria3.exe，再重新运行；脚本不会代为附加。
- 多实例：提供当次的 --instance-id。
- 源机器码不一致或地址不可读：重新采集当前游戏的报告，手动更新 TARGETS 列表。
- 第 101 行不是目标或连续性失败：在 CE 内存查看器核对边界；
  本次保持失败，不通过缩短窗口、修改机器码基线或切换解码器掩盖问题。
- 请求超时：检查 CE 是否正在显示模态窗口/忙于操作；确认状态后重新运行。
  脚本不会自动重发请求，也不会结束用户的 CE/游戏。
- manifest 的 residueCheck.state 非 unchanged：changed 时核对 CE 的 resourceCount/jobCount
  变化来源（只读工具本身不会产生 CE 资源）；unavailable/skipped 时按 reason 字段排查。
- 输出不可写：换用可写的 --output 目录，不修改 MCP 文件权限设置。

文件写入由本地 Python 完成，无需启用 MCP 的 Files:AllowedRoots，
也无需启用 unsafe Lua、AA、代码注入或内核能力。
```

### 4.2 从当前实际状态执行

本轮 CE 已打开但未附加；正式实施后先由用户在 CE 中手动附加 victoria3.exe，再运行：

```powershell
Set-Location -LiteralPath 'D:\cebuild\ce-custom'
python -m unittest discover -s Scripts/tests -p "test_*.py" -v
python Scripts/run_opcode_export.py
$LASTEXITCODE
```

自动流程应为：

1. 校验脚本头部 `TARGETS` 固化列表（9 对地址与原始 bytes），非法条目直接以退出码 2 失败，不接触 CE。
2. Gateway `initialize → notifications/initialized → tools/list`。
3. `instance_list → runtime_get_info → runtime_get_overview`；要求 CE 已手动附加 victoria3，否则以退出码 2 失败（不自动附加、不切换、不分离）。
4. 记录运行身份（baseline）与 `ceResourcesBefore`。
5. 每个地址依次执行 `overview → code_decode → code_disassemble(before=100,count=101) → code_decode → overview`。
6. 校验当前地址、201 条、目标索引 100、每条 bytes/size、连续性、目标原始 bytes、会话身份。
7. 统一收尾（覆盖成功、失败与中断等全部退出路径）：在关闭 Gateway 之前恰好核对一次 `resourceCount/jobCount`，结果写入 manifest 的 `residueCheck`；changed 打 WARN 且退出码语义不变；核对不可用且数据全成功时退出码 0 升为 3；中断或连接失效记 skipped 原因，不重连、不阻塞。
8. 写每地址文件和逐步更新的 manifest/index；收尾把 `residueCheck` 并入 manifest，再返回反映全批结果的退出码。
9. 先核对、后关闭本次 Gateway；CE 和游戏继续运行。

前后窗口有重叠也要分别生成文件；不跨目标合并窗口。出现单地址错误后继续其他地址；会话变化或传输不可继续时，将剩余目标记为未尝试并结束采集。无失败时才满足 goal1。

### 4.3 全量验收代码

- [ ] 先通过全部离线测试，并在 CE 中手动附加 victoria3.exe，再用下面的 PowerShell/Python 验收运行两次真实导出。代码在本机执行已有脚本，检查本次新增目录，绝不以“最后一个旧 index.md”作为证据。两次都成功才验证重复运行；失败时保留产物并按文档定位，不把失败改成成功。第一次运行结束后记录其目录的文件名集合与内容哈希，第二次运行结束后重读第一次目录核对（整文件哈希仅用于同一目录的前后自比较；manifest/index/opcode 文件头含 runId 或时间戳，不能用于两次运行之间的文件对比）。两次运行的 9 个文件指令表内容比较保留为附加一致性检查，前提是两次背靠背、同一 CE 会话，且期间未改动 CE 注释/符号/显示；CE 地址与 extra 列的显示变化需先核对来源再判定失败。

```powershell
@'
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

root = Path.cwd()
sys.path.insert(0, str(root / "Scripts/tests"))
from test_opcode_export import EXPECTED

output_root = root / "Output/opcodes"


def snapshot(directory):
    # 只用于同一目录的前后自比较；跨运行比整文件哈希会因 runId/时间戳必然不同。
    return {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in directory.iterdir()}


runs, first_tables, first_snapshot = [], None, None
for attempt in range(2):
    previous = set(output_root.iterdir()) if output_root.exists() else set()
    result = subprocess.run(
        [sys.executable, str(root / "Scripts/run_opcode_export.py")],
        cwd=root, check=False,
    )
    assert result.returncode == 0, f"export failed with exit code {result.returncode}"
    created = set(output_root.iterdir()) - previous
    assert len(created) == 1, "expected exactly one new run directory"
    run = created.pop()
    manifest = json.loads((run / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["status"] == "complete"
    assert manifest["expectedCount"] == manifest["processedCount"] == 9
    assert manifest["successCount"] == 9 and manifest["failedCount"] == 0
    assert manifest["instructionCount"] == 1809
    check = manifest["residueCheck"]
    assert check["state"] == "unchanged", check
    assert check["before"] == check["after"], check
    assert {(r["address"], r["expected_bytes"]) for r in manifest["results"]} == set(EXPECTED)
    assert {p.name for p in run.glob("opcode_*.md")} == {
        f"opcode_{address}.md" for address, _ in EXPECTED
    }
    index = (run / "index.md").read_text(encoding="utf-8")
    tables = {}
    for record in manifest["results"]:
        assert record["status"] == "success"
        assert (record["beforeCount"], record["afterCount"], record["instructionCount"]) == (100, 100, 201)
        path = run / record["file"]
        text = path.read_text(encoding="utf-8")
        rows = [line for line in text.splitlines() if line.startswith("| ")]
        assert len(rows) == 203, f"invalid table length: {path.name}"
        assert text.count("| TARGET |") == 1
        assert "CE estimated predecessors" in text
        assert f"]({path.name})" in index
        tables[record["address"]] = rows[2:]
    assert not list(run.glob("*.tmp")), "temporary files were not cleaned"
    if attempt == 0:
        first_tables = tables
        first_snapshot = snapshot(run)
    else:
        assert tables == first_tables, "instruction rows differ between runs"
        assert snapshot(runs[0]) == first_snapshot, "first run directory changed after second run"
    runs.append(run)
assert runs[0] != runs[1]

# 反例自检：第一次目录被改写时必须被快照核对发现（用副本验证，不动真实产物）。
with tempfile.TemporaryDirectory() as scratch:
    probe = Path(scratch) / "run_0_copy"
    shutil.copytree(runs[0], probe)
    (probe / "opcode_7FF777D19218.md").write_text("CORRUPTED OLD EXPORT", encoding="utf-8")
    try:
        assert snapshot(probe) == first_snapshot, "first run directory changed after second run"
    except AssertionError:
        pass
    else:
        raise AssertionError("corruption counter-example was not detected")

print("PASS: 9 windows, 1809 instructions per run, identical windows, "
      "isolated repeated exports (first run unchanged)")
'@ | python -
```

- [ ] 在 CE 内存查看器人工抽查两组各一个目标：`7FF777D19218` 和 `7FF777D1B9DA`。比较目标 bytes/opcode、紧邻前后指令与导出文件，确认 CE 使用同一 PID。人工抽查用于检查展示一致性，不能代替全量结构校验。
- [x] 使用离线测试覆盖错误注入；不要为测试而破坏正在运行的游戏：机器码不匹配、短窗口、目标错位、字节长度异常、单地址失败、超时、会话改变、多个实例、未附加/目标错误、固化列表非法条目、原子替换失败、仅最终 overview 失败（`residueCheck=unavailable` 且退出码 0→3）、写文件失败后的统一收尾、Ctrl+C 收尾、连接失效/无基线收尾、启动握手期间 Ctrl+C 的 Gateway 回收。
- [ ] 检查本次脚本只回收自己创建的 Gateway，原 CE 和 victoria3 仍在（含启动握手期间中断的场合）；确认没有新断点、内存写入、注入脚本或修改 CE 设置；核对 manifest：`residueCheck.state=unchanged` 且 `before/after` 计数一致（见 4.4）。
- [ ] 实施者记录本次实际退出码、输出目录、9/9 成功数、1809 条总数，以及人工抽查结果。若当前游戏已重启导致地址失效，记录真实失败，重新采集报告并手动更新 `TARGETS` 后再验收；不能宣告 goal1 完成。

### 4.4 失败残留分析（任何步骤失败都不产生不可逆残留）

脚本全程只调用只读 MCP 工具（常量 `READ_ONLY_TOOLS`：`instance_list`、`runtime_get_info`、`runtime_get_overview`、`code_decode`、`code_disassemble`），不写内存、不设断点、不注入、不分配、不附加/分离。因此不存在“补偿性写操作”：所有失败路径都无需回滚，因为从未产生内存或 CE 状态修改。attach 改为手动后，原计划中唯一改变 CE 状态的操作（`process_attach` 超时后无法确认是否已附加）已被消除。

| 失败点 | 退出码 | 仅可能产生的残留 | 对 CE/游戏的影响 |
| --- | --- | --- | --- |
| 未连接 / 无 CE 实例 | 2 | 本地运行目录、`gateway.stderr.log` | 无 |
| Gateway 启动失败 | 2 | 部分本地运行目录 | 无 |
| 实例选择失败 | 2 | 本地运行目录、已启动 Gateway（finally 中终止） | 无 |
| 未附加 / 目标不是 victoria3 | 2 | 同上 | 无；脚本不附加、不切换 |
| 单地址读取失败 | 1 | 失败文件与 manifest 记录 | 无 |
| 超时 / 传输断开 | 3 | 剩余目标记为未尝试 | 无；不重试、不重发 |
| 会话变化 | 3 | 同上 | 无 |
| Ctrl+C | 130 | manifest 标记 interrupted，`residueCheck=skipped`（含启动握手期间中断；Gateway 由 start 内清理与 finally 回收） | 无 |
| 写文件失败 | 2 | 旧文件保留；`*.tmp` 由 `atomic_text` 的 finally 清理；客户端可用时统一收尾核对仍执行 | 无 |
| 收尾资源核对失败 | 3（数据可能已全部成功） | manifest `residueCheck=unavailable` | 无；不重连、不重试 |

残留清理边界：脚本只终止自己启动的 Gateway 子进程；不关闭 CE/游戏、不分离用户已手动建立的目标、不删除用户断点或 CE 资源。运行目录与其中的 Markdown/manifest 由验收人员自行保留或清理。统一收尾在关闭客户端前核对一次 `resourceCount/jobCount` 并写入 manifest 的 `residueCheck`：changed 时打印 WARN 交人工核查（只读工具不会产生 CE 资源）；unavailable 时若数据全成功则退出码由 0 升为 3；skipped 时 reason 注明原因（中断、连接失效或未建立基线）。manifest 的结构化记录为尽力保存；磁盘不可写时以 stderr 诊断为准。

## 本次实施记录（2026-10-01）

- 已新增 3 个实现模块、3 个测试文件及操作说明；28 项离线测试通过，CLI 参数核验通过。真实 Gateway 完成初始化、工具目录和实例发现。
- 首次真实导出退出码为 1，成功 5/9，成功窗口共 1005 条指令。产物目录：`Output/opcodes/20261001T111936909271Z_09d8369e/`。
- 地址 `7FF7777927334`、`7FF7777927358`、`7FF7777CED5BB`、`7FF7777CED5C9` 返回 `memory_read_failed`。按原文保留地址，未猜测或删减十六进制位；需重新采集或核实这 4 个指令地址后手动更新 `TARGETS`。
- 收尾核对 `residueCheck.state=unchanged`，运行前后 resourceCount/jobCount 均为 0/0。原 CE PID 72480 和游戏 PID 43884 在运行后仍存在。
- 首次验收失败，第二次真实导出、重复运行一致性验收和 CE 内存查看器人工抽查尚未完成。goal1 尚未完成，相关复选框保持未勾选。

## 5. 完成标准与覆盖自检

后续修正记录（2026-10-01）：用户确认 `7FF777927334` 后，已通过只读解码确认四个失败地址均为报告中多了一位 `7`。现已同步修正 `Scripts/run_opcode_export.py` 的 `TARGETS` 和测试 `EXPECTED`；28 项离线测试再次通过。`7FF777927334` 已在 `Output/opcodes/20261001T113450443706Z_76a020f9/` 单独成功导出 201 条。剩余三个目标 `7FF777927358`、`7FF777CED5BB`、`7FF777CED5C9` 已在 `Output/opcodes/20261001T114219239448Z_dfa3881b/` 成功导出，共 603 条，退出码 0，资源计数前后均为 0/0。旧失败产物保留；两次完整九目标验收及人工抽查仍未完成。

| goal1 / 易错点 | 对应实现或验收 |
| --- | --- |
| 目标地址固定可维护 | `TARGETS` 固化 9 对地址+机器码于脚本头部；一致性测试（`EXPECTED` 副本）防止误改；失效时重新采集报告手动更新 |
| 导出全部 9 个目标 | TARGETS 覆盖 6 + 3 两个来源分组（含 UI/暂停分类）；验收断言地址与 `expected_bytes` 集合 |
| 不误用标题数据地址 | `3A484D9F8B8`/`3A484D9F8BC` 仅作为 1.3 来源背景，从不进入脚本或 TARGETS |
| 前后各 100 行 opcode | before=100、count=101；201 条且目标在索引 100 |
| 每个地址独立文件 | opcode_<大写HEX>.md；全量验收检查文件名集合 |
| 使用已经连通的 MCP | 真实 Gateway stdio，不保留旧 Lua 注入/命令行启动 CE 方案 |
| x86/x64 可变长度边界 | CE 估计前置边界 + 目标位置与连续性校验 + 明示估计性质 |
| 本次进程和地址有效性 | 要求 CE 已手动附加 victoria3（未附加即退出码 2，不自动附加/切换/分离）、会话指纹、导出前后原始 bytes 检查 |
| 只读与无不可逆残留 | `READ_ONLY_TOOLS` 常量 + 集成测试调用集合子集断言；`ceResourcesBefore` + 统一收尾 `residueCheck` 核对；4.4 失败残留分析 |
| 自动化与失败可见 | 单命令、英文日志、结构化 manifest、明确退出码 |
| 重复运行不混旧数据 | 独立目录、文件原子替换、两次真实运行校验（第一次目录快照复核 + 指令表内容比较 + 篡改反例自检） |
| 无多余功能 | 不引入菜单、独立配置、Lua、断点、AOB 重定位或新的反汇编器 |
| 计划可执行 | 文件边界、接口、完整核心代码、离线测试和真实验收代码均已给出 |

未覆盖的需求：无。实时导出尚未发生，不把本轮连接核验、示例代码或离线测试通过当作 goal1 已完成。

本轮计划校验记录（2026-10-01，修订版 3）：已从本文提取 6 个 Python 文件代码块，在系统临时目录完成 `python -m py_compile`（6/6 通过）与 `python -m unittest discover -s Scripts/tests -p "test_*.py" -v`（28 项离线测试全部通过：传输 5、窗口/锚点/原子写 4、编排 19）。测试不启动 CE、不读取报告文件；固化列表一致性测试校验 9 对地址与机器码（含 7FF777D19218 = 496385581D0000），并验证未附加时以退出码 2 失败、空/重复/非法固化条目在接触 CE 前拒绝、成功运行调用集合仅含只读工具。修订版 3 依据审查报告 R1/R2/R3/R5（R4 不处理）补齐：统一收尾残留核对（状态 unchanged/changed/unavailable/skipped，最终核对失败且数据全成功时退出码 0 升为 3；覆盖写文件失败、Ctrl+C、连接失效、无基线路径）、启动握手期间中断仍回收 Gateway、重复运行验收恢复第一次目录快照复核并内置篡改反例自检。临时验证产物未写入项目的 Scripts 或 Output 目录。上述结果验证计划示例代码，不替代真实 CE 反汇编验收。

实施结束后只提交源码、测试和操作文档；本计划中的复选框据实际结果更新。提交前检查 `git diff --check`，保留用户原有 `AGENTS.md`、`Docs/testdata-2026-10-1-10-58.md` 修改和未跟踪的 `Docs/mcp_setup.md`，不要执行广泛的 `git add .`。
