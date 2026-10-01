"""只读采集 CE 手动断点现场的寄存器与启发式栈候选，并原子生成 Markdown 报告。"""
# exp.
# cd D:\cebuild\ce-custom
# python Scripts\get_stacktrace_register_at_breakpoint.py

import argparse
import html
import json
import re
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

from ce_mcp_client import McpClient, ToolError, TransportError
from opcode_report import atomic_text, md

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_GATEWAY = ROOT / "McpExternals/CheatEngine.Mcp-2.0.0-beta.2-win-x64/CheatEngine.Mcp.Gateway.exe"
DEFAULT_OUTPUT = ROOT / "Output"
STACK_DEPTH = 128
# 固定兼容查询只读当前调试上下文；不接受外部源码，也不修改 CE 全局函数。
STATUS_COMPAT_SOURCE = """
local attached = debug_isDebugging()
assert(type(attached) == 'boolean', 'Invalid attached state')
local context = attached and debug_getCurrentContextTable(false) or nil
local broken = type(context) == 'table'
local is64Bit = targetIs64Bit()
assert(type(is64Bit) == 'boolean', 'Invalid target architecture')
local active = nil
if attached then
    local interfaces = {[1]='windows', [2]='veh', [3]='kernel'}
    active = interfaces[debug_getCurrentDebuggerInterface()]
    assert(active ~= nil, 'Unsupported debugger interface')
end
local result = {stateValid=true, attached=attached, broken=broken, activeInterface=active, is64Bit=is64Bit}
if broken then
    local ip = context[is64Bit and 'RIP' or 'EIP']
    local sp = context[is64Bit and 'RSP' or 'ESP']
    assert(math.type(ip) == 'integer' and ip ~= 0, 'Invalid stopped instruction pointer')
    assert(math.type(sp) == 'integer', 'Invalid stopped stack pointer')
    result.instructionPointer = string.format('%X',ip)
    result.stackPointer = string.format('%X',sp)
end
return result
"""
STATUS_COMPAT_CHUNK = "streg_readonly_status_compat"
READ_ONLY_TOOLS = frozenset({
    "instance_list", "runtime_get_info", "runtime_get_overview",
    "debugger_get_status", "debugger_get_context", "debugger_get_stack_trace",
})
ARGUMENT_ERRORS = {"invalid_argument", "capability_disabled", "unsupported", "not_found"}
SESSION_ERRORS = {
    "not_attached", "invalid_state", "target_changed", "stopping",
    "instance_unavailable", "cancelled",
}


class CaptureError(RuntimeError):
    def __init__(self, message, code=2):
        """保存采集错误与退出码；参数为英文诊断和退出码，无返回值。"""
        super().__init__(message)
        self.code = code


def now() -> str:
    """获取采集时间；无参数，返回带时区的 UTC ISO 文本。"""
    return datetime.now(timezone.utc).isoformat()


def positive_timeout(text) -> int:
    """校验超时参数；参数为命令行文本，返回正整数秒数。"""
    try:
        value = int(text)
    except (ValueError, TypeError) as exc:
        raise argparse.ArgumentTypeError("timeout must be a positive integer") from exc
    if value <= 0:
        raise argparse.ArgumentTypeError("timeout must be a positive integer")
    return value


def normalize_address(value: object) -> str:
    """校验停止地址以安全构造文件名；参数为整数或十六进制文本，返回无前缀大写地址。"""
    if type(value) is int:
        number = value
    elif isinstance(value, str) and re.fullmatch(r"(?:0[xX])?[0-9a-fA-F]{1,16}", value):
        number = int(value, 16)
    else:
        raise CaptureError("invalid hexadecimal instruction address")
    if not 0 < number < 2**64:
        raise CaptureError("instruction address outside uint64 range")
    return f"{number:X}"


def field(mapping, key, expected):
    """校验必填字段及精确类型；参数为字典、键和类型，返回字段值。"""
    if not isinstance(mapping, dict) or key not in mapping or type(mapping[key]) is not expected:
        raise CaptureError(f"missing or invalid field: {key}")
    return mapping[key]


def tool_failure(exc, name, collecting):
    """按工具错误合同分类；参数为异常、工具名及采集中标志，返回采集异常。"""
    detail = exc.payload.get("error", exc.payload)
    effect = detail.get("hostEffect") if isinstance(detail, dict) else None
    kind = exc.kind
    diagnostic = f"tool={name} kind={kind} hostEffect={effect}; detail={ascii(str(exc))}"
    diagnostic = diagnostic.encode("ascii", errors="backslashreplace").decode("ascii")
    if not isinstance(effect, str) or effect not in {"not_started", "started"} or not isinstance(kind, str):
        return CaptureError("WARN: host state unconfirmed; " + diagnostic, 3)
    if kind in ARGUMENT_ERRORS:
        return CaptureError(diagnostic, 2)
    if kind in SESSION_ERRORS:
        return CaptureError(diagnostic, 3)
    if kind == "host_refused":
        return CaptureError(diagnostic, 3 if collecting else 2)
    return CaptureError("WARN: host state unconfirmed; " + diagnostic, 3)


def read_tool(client, name, instance_id=None, *, collecting=False, **extra):
    """执行白名单只读工具；参数为客户端、工具、实例及附加参数，返回响应字典。"""
    if name not in READ_ONLY_TOOLS:
        raise CaptureError("tool is outside the read-only allowlist")
    if name != "instance_list" and (not isinstance(instance_id, str) or not instance_id):
        raise CaptureError("read-only tool requires a discovered instanceId")
    if client.broken:
        raise TransportError("MCP connection is unusable")
    arguments = {} if name == "instance_list" else {"instanceId": instance_id}
    arguments.update(extra)
    try:
        result = client.call(name, arguments)
    except ToolError as exc:
        raise tool_failure(exc, name, collecting) from exc
    if not isinstance(result, dict):
        raise CaptureError(f"invalid response object: {name}")
    return result


def validate_catalog(client):
    """校验工具目录；参数为客户端，返回固定 Lua 兼容查询是否可用。"""
    try:
        catalog = client.tools()
        if not isinstance(catalog, dict) or not READ_ONLY_TOOLS <= catalog.keys():
            raise CaptureError("required read-only tools are missing")
        for name in READ_ONLY_TOOLS:
            schema = field(catalog[name], "inputSchema", dict)
            properties = field(schema, "properties", dict)
            required = set() if name == "instance_list" else {"instanceId"}
            if name == "debugger_get_context":
                required.add("includeExtraRegisters")
            if name == "debugger_get_stack_trace":
                required.add("depth")
            if not required <= properties.keys():
                raise CaptureError(f"tool input schema changed: {name}")
        lua = catalog.get("lua_execute", {})
        schema = lua.get("inputSchema", {}) if isinstance(lua, dict) else {}
        properties = schema.get("properties", {}) if isinstance(schema, dict) else {}
        return isinstance(properties, dict) and {"instanceId", "source", "chunkName"} <= properties.keys()
    except (KeyError, TypeError, AttributeError) as exc:
        raise CaptureError("invalid tool catalog or input schema") from exc


def select_instance(client, wanted: str | None) -> str:
    """选择唯一 CE 实例；参数为客户端和可选精确实例 ID，返回实例 ID。"""
    listing = read_tool(client, "instance_list")
    if field(listing, "discoveryIncomplete", bool):
        raise CaptureError("instance discovery incomplete; retry after checking CE")
    items = field(listing, "instances", list)
    identifiers = [field(item, "instanceId", str) for item in items]
    if any(not identifier for identifier in identifiers):
        raise CaptureError("empty CE instance identity")
    matches = identifiers if wanted is None else [item for item in identifiers if item == wanted]
    if len(matches) != 1:
        raise CaptureError("select exactly one available CE instance with --instance-id")
    return matches[0]


def fingerprint(overview):
    """校验已附加进程的会话身份；参数为运行概览，返回会话指纹字典。"""
    runtime = field(overview, "runtime", dict)
    process = field(overview, "process", dict)
    if field(process, "isOpen", bool) is not True:
        raise CaptureError("no target attached; select the target manually in CE")
    epoch = field(runtime, "epoch", int)
    pid = field(process, "processId", int)
    selection = field(process, "selectionEpoch", int)
    pointer = field(process, "pointerSize", int)
    if epoch < 0 or pid <= 0 or selection < 0 or pointer not in {4, 8}:
        raise CaptureError("target session identity or pointer width is unavailable")
    if process.get("processName") is not None and not isinstance(process["processName"], str):
        raise CaptureError("invalid processName")
    return {"runtimeEpoch": epoch, "processId": pid, "selectionEpoch": selection, "pointerSize": pointer}


def resources(overview):
    """校验 CE 资源及作业计数；参数为运行概览，返回两个非负计数字典。"""
    counts = {key: field(overview, key, int) for key in ("resourceCount", "jobCount")}
    if any(value < 0 for value in counts.values()):
        raise CaptureError("negative CE resource or job count")
    return counts


def validate_runtime(client, instance_id) -> dict:
    """读取运行健康信息和基线；参数为客户端和实例 ID，返回原始响应、指纹及计数。"""
    info = read_tool(client, "runtime_get_info", instance_id)
    overview = read_tool(client, "runtime_get_overview", instance_id)
    identity = fingerprint(overview)
    if field(info, "epoch", int) != identity["runtimeEpoch"]:
        raise CaptureError("runtime changed while establishing baseline", 3)
    return {"info": info, "overview": overview, "fingerprint": identity, "resources": resources(overview)}


def require_stopped(status: dict) -> None:
    """检查可读取的停止现场；参数为状态响应，成功时无返回值。"""
    if isinstance(status.get("error"), str) and status["error"]:
        raise CaptureError("debugger host error: " + ascii(status["error"]))
    for key in ("stateValid", "attached", "broken"):
        if field(status, key, bool) is not True:
            raise CaptureError(f"debugger must be stopped: {key}=false; check CE manually")
    for key in ("activeInterface", "error"):
        if status.get(key) is not None and not isinstance(status[key], str):
            raise CaptureError(f"invalid debugger status field: {key}")
    if status.get("error"):
        raise CaptureError("debugger host error: " + ascii(status["error"]))


def read_status(client, instance_id, *, collecting=False, compat_available=False):
    """读取停止状态并处理已知 CE 返回类型缺陷；参数为客户端、实例及阶段和能力标志，返回状态。"""
    original = read_tool(client, "debugger_get_status", instance_id, collecting=collecting)
    error = original.get("error")
    known_error = isinstance(error, str) and re.fullmatch(
        r"CheatEngine\.Mcp/debugger_get_status:[0-9]+: debug_isBroken did not return a boolean debugger state", error
    )
    if original.get("stateValid") is not False or not known_error:
        return original
    if not compat_available:
        raise CaptureError("debug_isBroken is incompatible and lua_execute status fallback is unavailable")
    if client.broken:
        raise TransportError("MCP connection is unusable")
    # 通用 Lua 工具不属于只读白名单；此处单独限制为固定、无参数插值的查询。
    try:
        payload = client.call("lua_execute", {
            "instanceId": instance_id, "source": STATUS_COMPAT_SOURCE, "chunkName": STATUS_COMPAT_CHUNK,
        })
    except ToolError as exc:
        raise tool_failure(exc, "lua_execute(status compatibility query)", collecting) from exc
    if not isinstance(payload, dict) or payload.get("ok") is not True or payload.get("hostEffect") != "completed":
        raise CaptureError("WARN: status compatibility query failed or host effect unconfirmed: " + ascii(str(payload)), 3)
    if field(payload, "droppedOpaqueCount", int) != 0:
        raise CaptureError("status compatibility query returned opaque data")
    values = field(payload, "returnValues", list)
    if len(values) != 1 or not isinstance(values[0], dict):
        raise CaptureError("status compatibility query must return exactly one object")
    status = dict(values[0])
    for key in ("stateValid", "attached", "broken", "is64Bit"):
        field(status, key, bool)
    if status["broken"]:
        normalize_address(field(status, "instructionPointer", str))
        normalize_address(field(status, "stackPointer", str))
    status.update(statusSource="lua_execute_fixed_query", originalStatus=original, luaResponse=payload)
    print("INFO: Using fixed read-only Lua status query for the debug_isBroken compatibility issue.", file=sys.stderr)
    return status


def check_status_context(status, context, address):
    """核对兼容状态与寄存器现场；参数为状态、上下文及地址，一致时无返回值。"""
    if status.get("statusSource") != "lua_execute_fixed_query":
        return
    stack_register = "RSP" if context["is64Bit"] else "ESP"
    stack_pointer = normalize_address(field(context["registers"], stack_register, str))
    if (status["is64Bit"] != context["is64Bit"]
            or normalize_address(status["instructionPointer"]) != address
            or normalize_address(status["stackPointer"]) != stack_pointer):
        raise CaptureError("stopped instruction or stack pointer changed during capture", 3)


def validate_context(context, pointer_size):
    """校验寄存器及架构；参数为上下文响应和指针字节数，返回规范化停止地址。"""
    is64 = field(context, "is64Bit", bool)
    if (8 if is64 else 4) != pointer_size:
        raise CaptureError("context architecture disagrees with target pointer size")
    if field(context, "includesExtraRegisters", bool) is not True:
        raise CaptureError("context did not include the requested extra-register option")
    registers = field(context, "registers", dict)
    if any(not isinstance(key, str) or not isinstance(value, str) for key, value in registers.items()):
        raise CaptureError("registers must map names to strings")
    address = normalize_address(field(registers, "RIP" if is64 else "EIP", str))
    if not is64 and (int(address, 16) >= 2**32 or "RIP" in registers):
        raise CaptureError("instruction register disagrees with 32-bit context")
    if context.get("activeInterface") is not None and not isinstance(context["activeInterface"], str):
        raise CaptureError("invalid context activeInterface")
    return address


def validate_stacktrace(stacktrace, pointer_size):
    """校验启发式栈响应；参数为栈响应和目标指针字节数，成功时无返回值。"""
    field(stacktrace, "stackPointer", str)
    if field(stacktrace, "pointerSize", int) != pointer_size:
        raise CaptureError("stacktrace pointer size disagrees with target")
    slots = field(stacktrace, "scannedSlots", int)
    if not 0 <= slots <= STACK_DEPTH:
        raise CaptureError("stacktrace scannedSlots outside requested depth 128")
    for frame in field(stacktrace, "frames", list):
        field(frame, "stackAddress", str)
        field(frame, "returnAddress", str)
        for key, expected in (("callInstruction", str), ("isHeuristic", bool)):
            if key in frame:
                field(frame, key, expected)


def capture_snapshot(client, instance_id, runtime) -> dict:
    """采集停止现场并复核会话；参数为客户端、实例与运行基线，返回完整快照。"""
    compat = runtime.get("statusCompatAvailable", False)
    status = read_status(client, instance_id, compat_available=compat)
    require_stopped(status)
    captured_at = now()
    context = read_tool(client, "debugger_get_context", instance_id, collecting=True, includeExtraRegisters=True)
    pointer_size = runtime["fingerprint"]["pointerSize"]
    address = validate_context(context, pointer_size)
    check_status_context(status, context, address)
    stacktrace = read_tool(client, "debugger_get_stack_trace", instance_id, collecting=True, depth=STACK_DEPTH)
    validate_stacktrace(stacktrace, pointer_size)
    final_status = read_status(client, instance_id, collecting=True, compat_available=compat)
    try:
        require_stopped(final_status)
    except CaptureError as exc:
        raise CaptureError("stopped context lost during capture: " + str(exc), 3) from exc
    check_status_context(final_status, context, address)
    if any(item.get("statusSource") == "lua_execute_fixed_query" for item in (status, final_status)):
        stack_register = "RSP" if context["is64Bit"] else "ESP"
        if normalize_address(stacktrace["stackPointer"]) != normalize_address(context["registers"][stack_register]):
            raise CaptureError("stacktrace stack pointer changed during capture", 3)
    try:
        final_overview = read_tool(client, "runtime_get_overview", instance_id, collecting=True)
    except (CaptureError, TransportError, json.JSONDecodeError) as exc:
        raise CaptureError(
            "residueCheck=unavailable; final overview failed: " + str(exc),
            exc.code if isinstance(exc, CaptureError) else 3,
        ) from exc
    try:
        final_identity = fingerprint(final_overview)
        final_resources = resources(final_overview)
    except CaptureError as exc:
        raise CaptureError("residueCheck=unavailable; final session check failed: " + str(exc), 3) from exc
    if final_identity != runtime["fingerprint"]:
        raise CaptureError("target session changed during capture; report discarded", 3)
    if final_resources != runtime["resources"]:
        raise CaptureError("WARN: residueCheck=changed; CE resourceCount/jobCount changed; verify manually", 3)
    return {
        "instanceId": instance_id, "capturedAt": captured_at, "address": address,
        "process": runtime["overview"]["process"], "runtime": runtime,
        "status": status, "context": context, "stacktrace": stacktrace,
        "finalStatus": final_status, "finalOverview": final_overview,
        "finalFingerprint": final_identity,
        "residueCheck": {"state": "unchanged", "before": runtime["resources"], "after": final_resources},
    }


def safe_cell(value) -> str:
    """清洗 Markdown 文本及控制字符；参数为任意值，返回安全单行文本。"""
    text = "".join(" " if unicodedata.category(char).startswith("C") else char for char in str(value))
    text = html.escape(text, quote=False).replace("\\", "&#92;").replace("`", "&#96;")
    return md(text).replace("*", "&#42;").replace("_", "&#95;")


def filter_report_snapshot(value):
    """递归移除报告副本中的 evidence、capabilities、hostVersion 和 platform 字段；参数为任意 JSON 值，返回清理后的副本。"""
    if isinstance(value, dict):
        return {
            key: filter_report_snapshot(item)
            for key, item in value.items()
            if key not in {"evidence", "capabilities", "hostVersion", "platform"}
        }
    if isinstance(value, list):
        return [filter_report_snapshot(item) for item in value]
    return value


def render_report(snapshot) -> str:
    """渲染寄存器与栈候选报告；参数为已校验快照，返回 UTF-8 文件所需的 LF 文本。"""
    process, status = snapshot["process"], snapshot["status"]
    context, stack = snapshot["context"], snapshot["stacktrace"]
    lines = [
        f"# Stacktrace and Registers at Breakpoint {snapshot['address']}", "",
        f"- Captured at: {safe_cell(snapshot['capturedAt'])}",
        f"- CE instance: {safe_cell(snapshot['instanceId'])}",
        f"- Process: {safe_cell(process.get('processName') or 'unavailable')} (PID {process['processId']})",
        f"- Pointer width: {process['pointerSize']} bytes ({process['pointerSize'] * 8} bits)",
        f"- Active debugger interface: {safe_cell(status.get('activeInterface') or 'unavailable')}",
        f"- Status source: {safe_cell(status.get('statusSource', 'debugger_get_status'))}",
        f"- Final status source: {safe_cell(snapshot['finalStatus'].get('statusSource', 'debugger_get_status'))}",
        "- Status: stopped", "- includeExtraRegisters=true", "- Stack depth: 128 slots",
        "- residueCheck: unchanged", "", "## Registers", "",
        "All returned registers are preserved; unavailable FP/XMM registers are not inferred.",
        "FP/XMM byte sequences are in memory order, little-endian (least significant byte first).", "",
        "| Register | Value |", "| --- | --- |",
    ]
    for name, value in sorted(context["registers"].items()):
        lines.append(f"| {safe_cell(name)} | {safe_cell(value)} |")
    lines += ["", "## Stacktrace", "", f"Stack pointer: {safe_cell(stack['stackPointer'])}",
              f"Scanned slots: {stack['scannedSlots']} (maximum 128).", "",
              "| Index | Stack slot address | Return address | Call instruction | isHeuristic |",
              "| ---: | --- | --- | --- | --- |"]
    for index, frame in enumerate(stack["frames"]):
        values = [index, frame["stackAddress"], frame["returnAddress"],
                  frame.get("callInstruction", "unavailable"),
                  str(frame["isHeuristic"]).lower() if "isHeuristic" in frame else "unavailable"]
        lines.append("| " + " | ".join(safe_cell(value) for value in values) + " |")
    if not stack["frames"]:
        lines += ["", "No heuristic candidate frames were returned."]
    lines += ["", "## Capture Contract", "",
              "Captured using read-only debugger queries, with a fixed Lua query for the known status compatibility issue when needed.",
              "Keep CE stopped throughout capture. Original status errors and compatibility query results are preserved below.",
              "The address is the current RIP/EIP, which may differ from a registered breakpoint address.",
              "Stacktrace frames are heuristic candidates, not a symbolicated or confirmed call chain.",
              "Call instructions are optional candidate information; verify against the breakpoint scene and disassembly.",
              "Before/after stopped-state and session checks cannot detect a resume/re-break between calls.",
              "No attach, breakpoint changes, continue, or target memory writes are performed.",
              "", "## Raw MCP Snapshot", ""]
    raw = json.dumps(filter_report_snapshot(snapshot), ensure_ascii=True, indent=2, sort_keys=True)
    fence = "`" * max(3, 1 + max((len(item) for item in re.findall(r"`+", raw)), default=0))
    return "\n".join(lines + [fence + "json", raw, fence, ""])


def main(argv=None) -> int:
    """执行命令行采集并清理网关；参数为可选参数列表，返回约定退出码。"""
    client = None
    code = 0
    try:
        parser = argparse.ArgumentParser(description="Read registers and heuristic stacktrace from a manually stopped CE target.")
        parser.add_argument("--gateway", type=Path, default=DEFAULT_GATEWAY)
        parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT,
                            help="output directory; only one capture may use a directory at a time")
        parser.add_argument("--instance-id")
        parser.add_argument("--timeout", type=positive_timeout, default=30)
        args = parser.parse_args(argv)
        if not args.gateway.is_file():
            raise CaptureError("Gateway executable does not exist: " + ascii(str(args.gateway)))
        args.output.mkdir(parents=True, exist_ok=True)
        client = McpClient([str(args.gateway.resolve())], args.timeout, args.output / "streg_gateway.stderr.log")
        client.start()
        compat_available = validate_catalog(client)
        instance_id = select_instance(client, args.instance_id)
        runtime = validate_runtime(client, instance_id)
        runtime["statusCompatAvailable"] = compat_available
        snapshot = capture_snapshot(client, instance_id, runtime)
        report = args.output / f"streg_{snapshot['address']}.md"
        atomic_text(report, render_report(snapshot))
        print("Saved report: " + ascii(str(report)))
    except SystemExit as exc:
        code = exc.code
    except KeyboardInterrupt:
        print("Interrupted by user; any already committed report is complete.", file=sys.stderr)
        code = 130
    except CaptureError as exc:
        print("ERROR: " + str(exc), file=sys.stderr)
        code = exc.code
    except ToolError as exc:
        failure = tool_failure(exc, "MCP startup/catalog", False)
        print("ERROR: " + str(failure), file=sys.stderr)
        code = failure.code
    except (TransportError, json.JSONDecodeError) as exc:
        print("ERROR: MCP transport failed: " + ascii(str(exc)), file=sys.stderr)
        code = 3
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print("ERROR: invalid response or local file operation failed: " + ascii(str(exc)), file=sys.stderr)
        code = 2
    finally:
        if client is not None:
            try:
                client.close()
            except KeyboardInterrupt:
                code = 130
            except Exception as exc:
                print("WARN: Gateway cleanup failed: " + ascii(str(exc)), file=sys.stderr)
                if code == 0:
                    code = 3
    return code


if __name__ == "__main__":
    sys.exit(main())
