"""为两个原子命令提供文本编码、一次 MCP 请求、现场校验及 JSON 证据保存。"""

import argparse
import hashlib
import json
import math
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

from ce_mcp_client import McpClient, ToolError, TransportError
from get_stacktrace_register_at_breakpoint import (
    DEFAULT_GATEWAY, STATUS_COMPAT_CHUNK, CaptureError, check_status_context,
    fingerprint, normalize_address, read_status, require_stopped, select_instance,
    validate_runtime,
)
from opcode_report import atomic_text

TOOL_PARAMETERS = {
    "instance_list": set(), "runtime_get_info": {"instanceId"},
    "runtime_get_overview": {"instanceId"},
    "lua_execute": {"instanceId", "source", "chunkName"},
    "debugger_get_status": {"instanceId"},
    "debugger_get_context": {"instanceId", "includeExtraRegisters"},
}


def read_text(source, file):
    """读取请求文本；入参为互斥源码和路径，返回规范化的非空 UTF-8 文本。"""
    if (source is None) == (file is None):
        raise ValueError("exactly one text input is required")
    text = source if file is None else file.read_text(encoding="utf-8-sig")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    if not text.strip() or "\0" in text or len(text.encode("utf-8")) > 65536:
        raise ValueError("invalid or oversized source text")
    return text


def lua_quote(text):
    """编码安全 Lua 字符串；入参为文本，返回按 UTF-8 字节转义的带引号字面量。"""
    return '"' + "".join(f"\\{byte:03d}" for byte in text.encode("utf-8")) + '"'


def execute_once(client, instance_id, source, chunk_name, report):
    """执行一次请求且不重试；入参为客户端、实例、源码、块名及报告，返回原始响应。"""
    report["actionAttempted"] = True
    report["hostEffect"] = "unknown"
    try:
        response = client.call("lua_execute", {
            "instanceId": instance_id, "source": source, "chunkName": chunk_name,
        })
    except ToolError as error:
        report["businessToolError"] = error.payload
        raise
    report["luaResponse"] = response
    if not isinstance(response, dict):
        raise ValueError("invalid Lua response object")
    report["hostEffect"] = response.get("hostEffect", "unknown")
    # 先保存业务对象，即使复制合同或后续校验失败仍保留部分完成证据。
    report["result"] = response.get("returnValues")
    if response.get("ok") is not True or response.get("hostEffect") != "completed":
        raise ValueError("Lua execution failed or host effect is unconfirmed")
    if type(response.get("droppedOpaqueCount")) is not int or response["droppedOpaqueCount"] != 0:
        raise ValueError("invalid or incomplete Lua copy metadata")
    if not isinstance(response.get("returnValues"), list):
        raise ValueError("invalid Lua return values")
    return response


def make_parser(description):
    """创建公共参数解析器；入参为英文描述，返回解析器。"""
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--instance-id")
    parser.add_argument("--gateway", type=Path, default=DEFAULT_GATEWAY)
    parser.add_argument("--timeout", type=float, default=30)
    parser.add_argument("--output", type=Path, default=Path("Output/cycle_count"))
    return parser


def utc_now():
    """获取 UTC 时间；无入参，返回 ISO 时间文本。"""
    return datetime.now(timezone.utc).isoformat()


def save_report(path, report):
    """原子保存 UTF-8 JSON；入参为路径和报告，无返回值。"""
    atomic_text(path, json.dumps(report, ensure_ascii=False, indent=2) + "\n")


def validate_tools(catalog, operation):
    """检查当前工具参数合同；入参为目录和操作类型，无返回值。"""
    required = set(TOOL_PARAMETERS)
    if operation == "lua":
        required -= {"debugger_get_status", "debugger_get_context"}
    for name in required:
        if not isinstance(catalog, dict) or name not in catalog:
            raise ValueError("required tool missing: " + name)
        tool = catalog[name]
        schema = tool.get("inputSchema") if isinstance(tool, dict) else None
        properties = schema.get("properties") if isinstance(schema, dict) else None
        if not isinstance(properties, dict) or not TOOL_PARAMETERS[name] <= properties.keys():
            raise ValueError("tool input schema changed: " + name)


def stopped_snapshot(client, instance_id, evidence, collecting=False):
    """保存并核对停止状态；入参为客户端、实例、证据和阶段，返回规范化 RIP/RSP。"""
    # 代理仅记录响应，不改写既有固定查询和错误匹配逻辑。
    recorder = StatusRecorder(client, evidence)
    status = read_status(recorder, instance_id, collecting=collecting, compat_available=True)
    evidence["status"] = status
    require_stopped(status)
    context = client.call("debugger_get_context", {"instanceId": instance_id, "includeExtraRegisters": False})
    evidence["context"] = context
    if not isinstance(context, dict) or context.get("is64Bit") is not True:
        raise ValueError("64-bit stopped context required")
    if context.get("includesExtraRegisters") is not False:
        raise ValueError("unexpected context register option")
    registers = context.get("registers")
    if not isinstance(registers, dict):
        raise ValueError("missing stopped registers")
    ip = normalize_address(registers.get("RIP"))
    sp = normalize_address(registers.get("RSP"))
    check_status_context(status, context, ip)
    return {"RIP": ip, "RSP": sp}


class StatusRecorder:
    def __init__(self, client, evidence):
        """创建兼容查询证据代理；入参为客户端及证据字典，无返回值。"""
        self.client, self.evidence = client, evidence

    @property
    def broken(self):
        """读取连接状态；无入参，返回布尔值。"""
        return self.client.broken

    def call(self, name, arguments):
        """记录状态原始回执再返回；入参为工具与参数，返回原始响应。"""
        try:
            response = self.client.call(name, arguments)
        except ToolError as error:
            self.evidence[name + "Error"] = error.payload
            raise
        self.evidence[name] = response
        return response


def failure_code(report, error):
    """按已证明效果分类失败；入参为报告和异常，返回退出码。"""
    if isinstance(error, ToolError):
        report["toolError"] = error.payload
        detail = error.payload.get("error", error.payload)
        if (isinstance(detail, dict) and (not report["actionAttempted"] or "businessToolError" in report)
                and (detail.get("hostEffect") == "not_started"
                     or (detail.get("phase") == "compile" and detail.get("hostEffect") == "not_applied"))):
            report["hostEffect"] = detail["hostEffect"]
            return 2
    response = report.get("luaResponse")
    if isinstance(response, dict):
        if response.get("ok") is False and response.get("phase") == "compile" and response.get("hostEffect") == "not_applied":
            return 2
        result = report.get("result")
        if (report["operation"] == "condition" and isinstance(result, dict)
                and result.get("ok") is False and result.get("phase") == "preflight"
                and result.get("created") is False and result.get("backend") == "native-ui"
                and result.get("conditionReadbackMatched") is False
                and result.get("conditionType") == report["request"]["conditionType"]
                and result.get("condition") == report["request"]["source"]
                and isinstance(result.get("error"), str) and bool(result["error"])):
            return 2
    if report["actionAttempted"] or isinstance(error, TransportError):
        return 3
    return error.code if isinstance(error, CaptureError) else 2


def run_cli(args, operation, request, source, client_factory=McpClient, result_validator=None):
    """执行一次完整会话；入参为参数、操作、请求、源码及依赖，返回退出码并保存证据。"""
    report = {
        "schemaVersion": 1, "operation": operation, "instanceId": None,
        "request": request, "actionAttempted": False, "hostEffect": "not_started",
        "baseline": {}, "status": {}, "luaResponse": None, "result": None,
        "finalOverview": None, "manualVerificationRequired": True, "error": None,
        "exitCode": 2, "startedAt": utc_now(), "sourceSha256": hashlib.sha256(source.encode("utf-8")).hexdigest(),
        "gatewayClose": {"attempted": False, "ok": None},
    }
    if operation == "condition":
        report.update(resourceOwner="ce-lua-untracked", uiSideEffects={
            "possibleBreakpointListOpened": True, "temporaryConditionDialogsAndTimer": True,
            "manualWindowAndResidualBreakpointCheckRequired": True,
        })
    client, path = None, None
    try:
        if not math.isfinite(args.timeout) or args.timeout <= 0 or (operation == "condition" and args.timeout < 10):
            raise ValueError("timeout must be finite and positive (condition requires at least 10 seconds)")
        if not args.gateway.is_file():
            raise ValueError("gateway file does not exist")
        args.output.mkdir(parents=True, exist_ok=True)
        prefix = operation + "_" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ") + "_" + uuid.uuid4().hex[:12]
        path = args.output / (prefix + ".json")
        report["reportPath"] = str(path)
        report["gatewayLog"] = str(args.output / (prefix + ".gateway.log"))
        # 请求发送前确认报告可写，先留下动作尚未开始的证据。
        save_report(path, report)
        client = client_factory([str(args.gateway)], timeout=args.timeout, log_path=Path(report["gatewayLog"]))
        client.start()
        validate_tools(client.tools(), operation)
        instance = select_instance(client, args.instance_id)
        report["instanceId"] = instance
        baseline = validate_runtime(client, instance)
        report["baseline"] = baseline
        gates = baseline["info"].get("gates")
        if not isinstance(gates, dict) or gates.get("unsafeLua") is not True:
            raise ValueError("unsafeLua gate is disabled or unavailable")
        if operation == "condition":
            process = baseline["overview"]["process"]
            process_name = process.get("processName")
            if (not isinstance(process_name, str)
                    or process_name.casefold() not in {"victoria3", "victoria3.exe"}
                    or process.get("pointerSize") != 8):
                raise ValueError("64-bit victoria3.exe target required")
            before = stopped_snapshot(client, instance, report["status"])
        save_report(path, report)
        response = execute_once(client, instance, source,
                                "cycle_user_lua" if operation == "lua" else "cycle_native_condition", report)
        if operation == "condition":
            values = response["returnValues"]
            report["result"] = values[0] if len(values) == 1 else values
            report["result"] = result_validator(response, request)
        overview = client.call("runtime_get_overview", {"instanceId": instance})
        report["finalOverview"] = overview
        if fingerprint(overview) != baseline["fingerprint"]:
            raise ValueError("target session changed after request")
        if operation == "condition":
            report["finalStatus"] = {}
            after = stopped_snapshot(client, instance, report["finalStatus"], collecting=True)
            if before != after:
                raise ValueError("stopped instruction or stack pointer changed")
        report["exitCode"] = 0
    except KeyboardInterrupt:
        report["error"] = "interrupted"
        report["exitCode"] = 130
    except (OSError, ValueError, TypeError, KeyError, AttributeError, CaptureError, ToolError, TransportError) as error:
        report["error"] = str(error)
        report["exitCode"] = failure_code(report, error)
        print("ERROR: " + ascii(str(error)), file=sys.stderr)
    finally:
        if client is not None:
            report["gatewayClose"]["attempted"] = True
            try:
                client.close()
                report["gatewayClose"]["ok"] = True
            except (Exception, KeyboardInterrupt) as error:
                report["gatewayClose"].update(ok=False, error=str(error))
                if report["exitCode"] != 130:
                    report["exitCode"] = 130 if isinstance(error, KeyboardInterrupt) else 3 if report["actionAttempted"] else 2
                print("ERROR: Gateway close failed: " + ascii(str(error)), file=sys.stderr)
        report["finishedAt"] = utc_now()
        report["finalState"] = ("completed" if report["exitCode"] == 0 else "interrupted" if report["exitCode"] == 130
                                else "preflight_failed" if report["exitCode"] == 2 else "failed_or_unconfirmed")
        if path is not None:
            try:
                save_report(path, report)
            except (OSError, ValueError, TypeError) as error:
                if report["exitCode"] != 130:
                    report["exitCode"] = 3 if report["actionAttempted"] else 2
                print("ERROR: Report write failed: " + ascii(str(error)), file=sys.stderr)
    if path is not None:
        print("INFO: Report: " + ascii(str(path)))
    if operation == "condition" and report["actionAttempted"] and report["exitCode"] != 0:
        print("WARN: Inspect CE windows and possible residual breakpoint manually before retrying.", file=sys.stderr)
    return report["exitCode"]
