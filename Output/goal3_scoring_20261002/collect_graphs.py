"""只读采集指定函数的控制流与反汇编，并验证暂停现场和磁盘展开信息。"""
import json
import struct
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
sys.path.insert(0, str(ROOT / "Scripts"))
from ce_mcp_client import McpClient
from get_stacktrace_register_at_breakpoint import DEFAULT_GATEWAY, select_instance, read_status, require_stopped


def file_offset(module, rva):
    """转换文件偏移；输入模块信息和相对地址，返回对应文件偏移。"""
    base = int(module["base"], 16)
    for section in module["sections"]:
        begin = int(section["address"], 16) - base
        if begin <= rva < begin + section["size"]:
            return int(section["fileOffset"], 16) + rva - begin
    raise ValueError(f"Unmapped RVA: {rva:X}")


def main():
    """采集函数及校验；输入为命令行函数地址列表，输出证据文件，无返回值。"""
    module = json.loads((ROOT / "Output/goal3_static_20261002" / "module.json").read_text())
    base = int(module["base"], 16)
    disk = Path(module["path"]).read_bytes()
    frames = json.loads((ROOT / "Output/goal3_static_20261002" / "unwind_frames.json").read_text())
    addresses = sys.argv[1:] or [frame["entry"] for frame in frames]
    client = McpClient([str(DEFAULT_GATEWAY)], 60, OUT / "graphs.stderr.log").start()
    audit = {}
    try:
        iid = select_instance(client, None)
        status = read_status(client, iid, compat_available=True)
        require_stopped(status)
        assert status["instructionPointer"] == "7FF777CED5C9"
        assert status["stackPointer"] == "8C5DE8D870"
        audit["before"] = client.call("runtime_get_overview", {"instanceId": iid})
        checks = []
        for frame in frames:
            data = client.call("memory_read", {"instanceId": iid, "address": f'{base + int(frame["unwindRva"],16):X}', "valueType": "bytes", "size": len(frame["unwindBytes"]) // 2})
            assert bytes.fromhex(data["value"]).hex() == frame["unwindBytes"]
            checks.append({"entry": frame["entry"], "unwindMatchesDisk": True})
        audit["unwindChecks"] = checks
        for address in addresses:
            graph = client.call("code_get_function_graph", {"instanceId": iid, "address": address, "maxInstructions": 4096, "maxBytes": 65536, "includeInstructions": True})
            stem = f'function_{graph["entry"]}'
            (OUT / (stem + ".json")).write_text(json.dumps(graph, indent=2), encoding="utf-8")
            rows = sorted((instruction for block in graph["blocks"] for instruction in block.get("instructions", [])), key=lambda item: int(item["address"], 16))
            matches = all(disk[file_offset(module, int(row["address"], 16)-base):file_offset(module, int(row["address"], 16)-base)+row["size"]] == bytes.fromhex(row["bytes"]) for row in rows)
            lines = [f'# Function {graph["entry"]}', '', f'- Instructions: {graph["instructionCount"]}', f'- Truncated: {graph["truncated"]}', f'- All decoded bytes match disk: {matches}', '', '```text']
            lines.extend(f'+{int(row["address"],16)-base:X} {row["address"]}: {row["opcode"]} {row["extra"]}' for row in rows)
            lines.append('```')
            (OUT / (stem + ".md")).write_text('\n'.join(lines)+'\n', encoding="utf-8")
            print(f'{stem}: instructions={len(rows)} truncated={graph["truncated"]} diskMatch={matches}')
        final = read_status(client, iid, compat_available=True)
        require_stopped(final)
        assert final["instructionPointer"] == status["instructionPointer"]
        assert final["stackPointer"] == status["stackPointer"]
        audit["after"] = client.call("runtime_get_overview", {"instanceId": iid})
        audit["statusBefore"] = status
        audit["statusAfter"] = final
    finally:
        (OUT / "graph_audit.json").write_text(json.dumps(audit, indent=2), encoding="utf-8")
        client.close()


if __name__ == "__main__":
    main()
