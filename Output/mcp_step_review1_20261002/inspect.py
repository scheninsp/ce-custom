# 功能：单步采集计划审查的只读探测；读取工具目录、合同注解与当前调试现场，不调用任何写类工具。
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "Scripts"))
from ce_mcp_client import McpClient, ToolError, TransportError

OUT = Path(__file__).resolve().parent
GATEWAY = ROOT / "McpExternals/CheatEngine.Mcp-2.0.0-beta.2-win-x64/CheatEngine.Mcp.Gateway.exe"

WANT = {
    "instance_list", "runtime_get_info", "runtime_get_overview",
    "debugger_get_status", "debugger_get_context", "debugger_list_breakpoints",
    "memory_read", "memory_read_batch", "code_decode", "code_disassemble",
    "module_get", "module_list",
    "lua_execute", "debugger_step", "debugger_continue", "debugger_run_to",
    "debugger_break_thread", "debugger_attach", "debugger_detach",
    "debugger_start_trace", "debugger_start_capture", "runtime_stop_job",
    "debugger_set_breakpoint", "debugger_delete_breakpoint", "debugger_set_register",
    "memory_write", "memory_write_batch",
}


def save(name, payload):
    """保存探测载荷到输出目录；参数为文件名与 JSON 载荷，无返回值。"""
    (OUT / (name + ".json")).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def readable(tool):
    """判断工具注解是否为只读；参数为工具定义，返回布尔值。"""
    annotations = tool.get("annotations") or {}
    return annotations.get("readOnlyHint") is True


def probe(client, calls, name, arguments, *, read_only_only=True, catalog=None):
    """按注解约束调用工具并记录结果；参数为客户端、记录列表、工具名、参数、只读约束与目录，返回响应或 None。"""
    if read_only_only and (catalog is None or not readable(catalog.get(name, {}))):
        calls.append({"tool": name, "arguments": arguments, "result": "skipped: not readOnlyHint"})
        return None
    try:
        payload = client.call(name, arguments)
    except ToolError as exc:
        detail = exc.payload.get("error", exc.payload)
        calls.append({"tool": name, "arguments": arguments,
                      "error": {"kind": exc.kind, "detail": detail}})
        return None
    except (TransportError, json.JSONDecodeError) as exc:
        calls.append({"tool": name, "arguments": arguments, "error": {"transport": str(exc)}})
        return None
    calls.append({"tool": name, "arguments": arguments, "result": "ok"})
    save(name.replace("/", "_"), payload)
    return payload


def main():
    """执行只读探测并输出摘要；无参数，返回退出码。"""
    calls = []
    client = McpClient([str(GATEWAY)], 30, OUT / "gateway.stderr.log")
    try:
        client.start()
        catalog = client.tools()
        print("TOOL_COUNT", len(catalog))
        missing = sorted(WANT - set(catalog))
        print("MISSING", missing)
        subset = {name: catalog[name] for name in sorted(WANT & set(catalog))}
        save("tools_subset", subset)
        for name in sorted(subset):
            annotations = subset[name].get("annotations") or {}
            print("ANNOT", name,
                  "ro=", annotations.get("readOnlyHint"),
                  "destructive=", annotations.get("destructiveHint"),
                  "idempotent=", annotations.get("idempotentHint"),
                  "class=", (subset[name].get("_meta") or {}).get("cheatengine/dispatchClass"),
                  "requires=", (subset[name].get("_meta") or {}).get("cheatengine/requires"))

        listing = probe(client, calls, "instance_list", {}, catalog=catalog)
        iid = None
        if listing and listing.get("instances"):
            iid = listing["instances"][0]["instanceId"]
        print("INSTANCE", iid)
        if not iid:
            save("calls", calls)
            return 0

        before = probe(client, calls, "runtime_get_overview", {"instanceId": iid}, catalog=catalog)
        probe(client, calls, "runtime_get_info", {"instanceId": iid}, catalog=catalog)
        status = probe(client, calls, "debugger_get_status", {"instanceId": iid}, catalog=catalog)
        print("STATUS", json.dumps(status, ensure_ascii=False) if status else None)
        context = probe(client, calls, "debugger_get_context",
                        {"instanceId": iid, "includeExtraRegisters": True}, catalog=catalog)
        breakpoints = probe(client, calls, "debugger_list_breakpoints", {"instanceId": iid}, catalog=catalog)
        if breakpoints:
            save("breakpoints_summary", {k: breakpoints.get(k) for k in ("total", "truncated")})
            print("BREAKPOINTS", breakpoints.get("total"), breakpoints.get("truncated"))
        module = probe(client, calls, "module_get", {"instanceId": iid, "module": "victoria3.exe"}, catalog=catalog)
        if module:
            print("MODULE_BASE", module.get("base"), "STAMP", (module.get("pe") or {}).get("timeDateStamp"))

        decode = probe(client, calls, "code_decode",
                       {"instanceId": iid, "address": "victoria3.exe+11FD5C9"}, catalog=catalog)
        if decode:
            instruction = decode.get("instruction") or {}
            print("DECODE_C9", instruction.get("bytes"), instruction.get("opcode"), instruction.get("extra"),
                  "len", decode.get("length"))
        window = probe(client, calls, "code_disassemble",
                       {"instanceId": iid, "address": "victoria3.exe+11FD5C9", "before": 0, "count": 2},
                       catalog=catalog)
        if window:
            for row in window.get("instructions", []):
                print("DISASM", row.get("address"), row.get("opcode"), row.get("extra"), row.get("bytes"))

        if context and isinstance(context.get("registers"), dict):
            registers = context["registers"]
            items, labels = [], []
            for label, register, offset, value_type in (
                    ("r14_1d58", "R14", 0x1D58, "uint32"),
                    ("r14_1d5c", "R14", 0x1D5C, "uint32"),
                    ("rsp_50", "RSP", 0x50, "uint32"),
                    ("rsp_330", "RSP", 0x330, "uint32")):
                value = registers.get(register)
                if not isinstance(value, str):
                    print("REGISTER_MISSING", register)
                    continue
                labels.append(label)
                items.append({"address": f"{int(value, 16) + offset:X}", "valueType": value_type})
            if items:
                reads = probe(client, calls, "memory_read_batch", {"instanceId": iid, "items": items}, catalog=catalog)
                if reads:
                    print("MEM_READ failed=", reads.get("failed"))
                    for label, item in zip(labels, reads.get("items", [])):
                        print("MEM_ITEM", label, json.dumps(item, ensure_ascii=False))

        after = probe(client, calls, "runtime_get_overview", {"instanceId": iid}, catalog=catalog)
        if before and after:
            comparison = {
                "resources": (before.get("resourceCount"), after.get("resourceCount")),
                "jobs": (before.get("jobCount"), after.get("jobCount")),
                "epoch": ((before.get("runtime") or {}).get("epoch"), (after.get("runtime") or {}).get("epoch")),
                "process": (before.get("process") == after.get("process")),
            }
            print("RESIDUE", json.dumps(comparison, ensure_ascii=False))
            save("residue", comparison)
        save("calls", calls)
    finally:
        client.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
