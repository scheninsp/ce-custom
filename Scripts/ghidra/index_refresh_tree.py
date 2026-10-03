# 功能：复用已有函数命名，并将 Refresh 的 Ghidra 导出整理成项目 AI 可检索的索引。
# 入参：--prepare-names 仅生成命名表；无参数生成索引并验证导出覆盖率；返回：退出码。

import argparse
import collections
import hashlib
import json
import re
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "Output/ghidra_refresh_20261003"
CODE = ROOT / "FakeCode/ghidra_refresh_20261003"


# 功能：从既有分析中提取真实函数地址和名称；入参：无；返回：地址到名称的映射。
def prepare_names():
    names = {}
    sources = [*sorted((ROOT / "FakeCode/2026-10-3-process1").glob("*.md")),
               *sorted((ROOT / "Docs/2026-10-3-process01").rglob("*.md"))]
    pattern = re.compile(
        r"// 地址：[^\n]*victoria3\.exe\+([0-9A-Fa-f]+)([^\n]*)\n"
        r"(?:\s*//[^\n]*\n)*\s*[\w:<>,*& ]+?\s+(\w+)\s*\(")
    for path in sources:
        for match in pattern.finditer(path.read_text(encoding="utf-8-sig")):
            if any(word in match[0].splitlines()[0] for word in ("内联", "调用点", "至", "片段")):
                continue
            names.setdefault(match[1].upper(), match[3])
    # 旧骨架的这些名称使用了错误 RVA，按机器码调用目标对应到同一语义函数。
    names.update({"11FBDA0": "Refresh", "7C96A0": "Resolve",
                  "13C1A10": "InitTempContext", "1226080": "WrapNumericContext",
                  "1226160": "FillGoodsDirectionContext", "1228B90": "BuildMarketTradeFraction",
                  "13C2350": "NormalizeAdvantage", "1027760": "UpdateAdvantageCache"})
    duplicates = collections.defaultdict(list)
    for address, name in names.items():
        duplicates[name].append(address)
    # 对旧文档中同名但不同地址的记录，优先保留最新正确地址，其他地址沿用 Ghidra 名称。
    for addresses in duplicates.values():
        if len(addresses) > 1:
            for address in addresses[:-1]:
                del names[address]
    target = ROOT / "Scripts/ghidra/refresh_names.tsv"
    target.write_text("".join(f"{address}\t{name}\n" for address, name in sorted(names.items())), encoding="utf-8")
    print(f"NAMES {len(names)}")
    return names


# 功能：读取单个函数导出状态；入参：RVA；返回：状态字典，缺失时返回 pending。
def read_status(address):
    path = EVIDENCE / f"status_{address}.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"status": "pending"}


# 功能：核对磁盘 PE、历史字节和 Refresh 直接调用图；入参：调用图；返回：核对结果字典。
def verify_root(graph):
    executable = Path(graph["executable_path"].lstrip("/"))
    data = executable.read_bytes()
    pe = struct.unpack_from("<I", data, 0x3C)[0]
    section_count = struct.unpack_from("<H", data, pe + 6)[0]
    optional_size = struct.unpack_from("<H", data, pe + 20)[0]
    image_base = struct.unpack_from("<Q", data, pe + 48)[0]
    sections = []
    for index in range(section_count):
        start = pe + 24 + optional_size + index * 40
        virtual_size, virtual_address, raw_size, raw_offset = struct.unpack_from("<IIII", data, start + 8)
        sections.append((virtual_address, max(virtual_size, raw_size), raw_offset))
    # 功能：将模块 RVA 转成磁盘位置；入参：RVA；返回：文件偏移。
    def file_offset(rva):
        for start, size, raw in sections:
            if start <= rva < start + size:
                return raw + rva - start
        raise ValueError(f"RVA outside sections: {rva:X}")
    history = ROOT / "Output/2026-10-3-process1/check_trade_advantages1_20261003/function_11FBDA0.asm"
    mismatches = []
    expected_edges = []
    instructions = 0
    for line in history.read_text(encoding="utf-8-sig").splitlines():
        match = re.match(r"\+([0-9A-F]+)\s+([0-9A-F]+)\s", line)
        if not match:
            continue
        address = int(match[1], 16)
        opcode = bytes.fromhex(match[2])
        instructions += 1
        if data[file_offset(address):file_offset(address) + len(opcode)] != opcode:
            mismatches.append(match[1])
        if len(opcode) == 5 and opcode[0] in (0xE8, 0xE9):
            target = address + 5 + struct.unpack_from("<i", opcode, 1)[0]
            if opcode[0] == 0xE8 or not 0x11FBDA0 <= target < 0x11FC07C:
                expected_edges.append((match[1], f"{target:X}", "call" if opcode[0] == 0xE8 else "tail_or_external_jump"))
    actual_edges = [(e["site"], e.get("to"), e["kind"]) for e in graph["edges"] if e["from"] == "11FBDA0"]
    sha256 = hashlib.sha256(data).hexdigest()
    result = {"executable": str(executable), "sha256": sha256,
              "ghidra_hash_matches_disk": sha256 == graph["executable_sha256"],
              "pe_timestamp": hex(struct.unpack_from("<I", data, pe + 8)[0]),
              "image_base": hex(image_base), "ghidra_base_matches_pe": image_base == int(graph["image_base"], 16),
              "historical_instructions_checked": instructions, "byte_mismatch_rvas": mismatches,
              "root_calls_checked": len(expected_edges), "root_callgraph_matches_machine_code": expected_edges == actual_edges}
    (EVIDENCE / "verification.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


# 功能：建立调用图、分片索引并检查覆盖率；入参：无；返回：统计字典。
def build_index():
    graph = json.loads((EVIDENCE / "callgraph.json").read_text(encoding="utf-8"))
    nodes = {node["rva"]: node for node in graph["nodes"]}
    outgoing = collections.defaultdict(list)
    incoming = collections.defaultdict(list)
    for edge in graph["edges"]:
        outgoing[edge["from"]].append(edge)
        if edge.get("to"):
            incoming[edge["to"]].append(edge)
    counts = collections.Counter()
    manifest = []
    problems = []
    warnings = []
    for address, node in nodes.items():
        status = {"status": "external_no_body"} if node["external"] else read_status(address)
        counts[status["status"]] += 1
        row = dict(node, **status)
        row["callees"] = sorted({e["to"] for e in outgoing[address] if e.get("to")})
        row["callers"] = sorted({e["from"] for e in incoming[address]})
        for filename in row.get("files", []):
            path = CODE / filename
            if not path.exists():
                problems.append(f"Missing file: {filename}")
                continue
            text = path.read_text(encoding="utf-8")
            lines = text.splitlines()
            if len(lines) > 2000:
                problems.append(f"Oversized file: {filename}: {len(lines)}")
            if f"victoria3.exe+{address}" not in text:
                problems.append(f"Missing address: {filename}")
            for line_number, line in enumerate(lines, 1):
                if any(term in line for term in ("Bad instruction", "Could not recover jumptable", "UNRECOVERED_JUMPTABLE")):
                    warnings.append({"rva": address, "file": filename, "line": line_number, "warning": line.strip()})
        manifest.append(row)
    # 全量 JSON 可按 RVA 精确查询；Markdown 索引每份最多 250 个函数。
    (EVIDENCE / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    sorted_rows = sorted(manifest, key=lambda item: (item["depth"], item["rva"]))
    index_files = []
    for offset in range(0, len(sorted_rows), 250):
        filename = f"index_{offset // 250 + 1:02d}.md"
        lines = [f"# Refresh 调用树索引 {offset // 250 + 1}", "",
                 "深度是从 Refresh 到该函数的最短静态路径；名称是分析标签或 Ghidra 原名称。", "",
                 "| RVA | 名称 | 深度 | 状态 | 伪代码 |", "| --- | --- | ---: | --- | --- |"]
        for row in sorted_rows[offset:offset + 250]:
            links = "、".join(f"[分片 {i + 1}]({filename})" for i, filename in enumerate(row.get("files", [])))
            label = row["rva"] if row["external"] else "+" + row["rva"]
            lines.append(f"| `{label}` | `{row['name']}` | {row['depth']} | {row['status']} | {links} |")
        (CODE / filename).write_text("\n".join(lines) + "\n", encoding="utf-8")
        index_files.append(filename)
    unresolved = [edge for edge in graph["edges"] if not edge.get("to")]
    (EVIDENCE / "unresolved_edges.json").write_text(json.dumps(unresolved, indent=2), encoding="utf-8")
    (EVIDENCE / "decompiler_warnings.json").write_text(json.dumps(warnings, indent=2), encoding="utf-8")
    verification = verify_root(graph)
    if not verification["ghidra_hash_matches_disk"] or not verification["ghidra_base_matches_pe"] or verification["byte_mismatch_rvas"] or not verification["root_callgraph_matches_machine_code"]:
        problems.append("PE or root callgraph verification failed")
    # 调用位置同样分片保存，保证 AI 可按地址打开小文件而不必读取整个调用图。
    for offset in range(0, len(sorted_rows), 100):
        lines = ["# Refresh 调用关系", ""]
        for row in sorted_rows[offset:offset + 100]:
            lines += [f"## `+{row['rva']}` `{row['name']}`", "",
                      "| 调用点 RVA | 类型 | 目标 RVA / 名称 |", "| --- | --- | --- |"]
            for edge in outgoing[row["rva"]]:
                child = nodes.get(edge.get("to"))
                label = child["rva"] if child and child["external"] else "+" + child["rva"] if child else ""
                target = f"`{label}` `{child['name']}`" if child else f"未解析：`{edge['instruction']}`"
                lines.append(f"| `+{edge['site']}` | {edge['kind']} | {target} |")
            lines.append("")
        # 某些函数调用极多，继续按 1800 行分片。
        for part, start in enumerate(range(0, len(lines), 1800), 1):
            (CODE / f"calls_{offset // 100 + 1:02d}_{part}.md").write_text(
                "\n".join(lines[start:start + 1800]) + "\n", encoding="utf-8")
    summary = {"functions": len(nodes), "edges": len(graph["edges"]), "status_counts": dict(counts),
               "unresolved_edges": len(unresolved), "max_depth": max(row["depth"] for row in manifest),
               "decompiler_warning_functions": len({warning["rva"] for warning in warnings}),
               "validation_errors": problems, "index_files": index_files}
    (EVIDENCE / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=True))
    return summary


# 功能：根据命令行选择命名准备或索引生成；入参：命令行；返回：无。
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prepare-names", action="store_true")
    args = parser.parse_args()
    if args.prepare_names:
        prepare_names()
    else:
        build_index()


if __name__ == "__main__":
    main()
