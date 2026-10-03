# 功能：结合 Ghidra 静态调用图与历史 opcode，生成 Refresh 四层完整伪代码及证据索引。
# 入参：无；返回：生成文件到 FakeCode/ghidra_disassembly，验证失败时抛出异常。

import collections
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "FakeCode/ghidra_refresh_20261003"
EVIDENCE = ROOT / "Output/ghidra_refresh_20261003"
DEST = ROOT / "FakeCode/ghidra_disassembly"
ROOT_RVA = "11FBDA0"
MAX_DEPTH = 4

# 只采用此前已登记的函数名；参数名是局部阅读别名，不是恢复出的类定义。
SEMANTICS = {
    "11FBDA0": ("刷新候选数量和方向优势，更新短缺与收益，再尾跳计算评分。", "candidate 为候选对象，context 为共享评估上下文；返回：无，候选原位写回。", {"param_1": "candidate", "param_2": "context"}),
    "7C96A0": ("按引用低 24 位索引和完整引用标识校验解析对象，失败返回全局后备对象。", "reference 指向 32 位引用；返回：解析对象地址或全局后备对象地址。", {"param_1": "reference", "uVar1": "referenceId", "lVar2": "resolvedObject"}),
    "122AB50": ("商品基础数量乘以州数量修正倍率，按全局最小数量取下限。", "state 为州对象地址，outQuantity 为输出槽，goods 为商品地址；返回：outQuantity。", {"param_1": "state", "param_2": "outQuantity", "param_3": "goods"}),
    "1026630": ("检查商品索引合法性；保留初始化和报告路径。", "参数原型及返回宽度遵循 Ghidra；调用者消费 AL 作为合法性标志。", {}),
    "13C1A10": ("初始化临时数值上下文及其成员。", "temp 为临时上下文地址，第二参数保留 Ghidra 类型；返回值按下列原型。", {"param_1": "temp"}),
    "1226080": ("向数值上下文加入全局输入，随后清理临时包装对象和字符串存储。", "ignoredRcx 不被函数体使用，temp 通过 RDX 传入；返回：无。", {"param_1": "ignoredRcx", "param_2": "temp"}),
    "1226160": ("向临时上下文加入商品和方向相关输入；保留全部分支与清理过程。", "related 为州关联对象，temp 为临时上下文，goods 为商品，direction 为方向编号；返回类型以原型为准。", {"param_1": "related", "param_2": "temp", "param_3": "goods", "param_4": "direction"}),
    "1228B90": ("构造市场贸易比例并加入临时上下文。", "related 为关联对象，temp 为临时上下文；返回类型以原型为准。", {"param_1": "related", "param_2": "temp"}),
    "13C2350": ("合并数值上下文的基数和加项，应用倍率、最小非零处理与上下限。", "temp 为按 64 位字段观察的上下文，outValue 为输出槽；返回：outValue。", {"param_1": "temp", "param_2": "outValue"}),
    "C48D10": ("清理临时上下文成员；其子路径见调用表。", "member 为需要清理的成员地址；返回类型以原型为准。", {"param_1": "member"}),
    "1027760": ("原位写入商品缓存，维护存在位并删除对应的延迟记录；零值分支也保留。", "table 为商品表地址，goods 为商品地址，value 为定点值；返回：无。", {"param_1": "table", "param_2": "goods", "param_3": "value"}),
    "11FBA60": ("仅对方向 0 的合格商品计算有效供需比和短缺项，写入候选 +0x30。", "candidate 为候选，context 为共享上下文；返回：无。", {"param_1": "candidate", "param_2": "context"}),
    "11FC080": ("增加模式复制八张商品表并加入候选数量，计算净单位收益及基础收益。", "candidate 为候选，context 为共享上下文；返回：无，写入 +0x18 和 +0x10。", {"param_1": "candidate", "param_2": "context"}),
    "11FC320": ("检查数量限制并合成基础收益、政策差值、数量比例和短缺加分，写入 +0x20。", "candidate 为候选，context 为共享上下文；返回：无。完整公式以下列控制流为准。", {"param_1": "candidate", "param_2": "context"}),
    "1027970": ("按商品累加定点值并维护商品表的存在位和记录。", "table 为商品表，goods 为商品，delta 为增量；返回类型以原型为准。", {"param_1": "table", "param_2": "goods", "param_3": "delta"}),
    "1207860": ("按商品基价计算关税成本与补助收益，返回税补后的净单位收益。", "statePart 为州内部子对象（调用者传入州 +0x18），outProfit 为输出槽，goods 为商品，direction 为方向，priceDelta 为税补前价差；返回：outProfit。", {"param_1": "statePart", "param_2": "outProfit", "param_3": "goods", "param_4": "direction", "param_5": "priceDelta"}),
    "13A5280": ("按全局权重将相对优势向 1 收缩，再按方向选择正向倍率或倒数。", "outMultiplier 为输出槽，relativeAdvantage 为定点相对优势，direction 为分支标志；返回：outMultiplier。", {"param_1": "outMultiplier", "param_2": "relativeAdvantage", "param_3": "direction"}),
}


# 功能：读取 JSON 证据；入参：路径；返回：解析后的对象。
def read_json(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


# 功能：输出结构化索引和证据；入参：文件名、对象；返回：无。
def write_json(filename, value):
    (DEST / filename).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


# 功能：输出生成的 Markdown；入参：文件名和行列表；返回：无。
def write_md(filename, lines):
    assert len(lines) <= 2000, f"Oversized output: {filename}"
    (DEST / filename).write_text("\n".join(lines) + "\n", encoding="utf-8")


# 功能：独立计算最短静态调用深度；入参：图；返回：RVA 到深度的字典。
def compute_depths(graph):
    outgoing = collections.defaultdict(list)
    for edge in graph["edges"]:
        if edge.get("to"):
            outgoing[edge["from"]].append(edge["to"])
    depths = {ROOT_RVA: 0}
    queue = collections.deque([ROOT_RVA])
    while queue:
        parent = queue.popleft()
        for child in outgoing[parent]:
            if child not in depths:
                depths[child] = depths[parent] + 1
                queue.append(child)
    return depths


# 功能：拼接导出分片并去除源文件的通用头注释；入参：函数记录；返回：完整正文。
def source_body(row):
    blocks = []
    for filename in row["files"]:
        text = (SOURCE / filename).read_text(encoding="utf-8")
        block = re.search(r"```cpp\n(.*?)\n```", text, re.S)
        assert block, f"Missing code block: {filename}"
        lines = block[1].splitlines()
        assert lines[0].startswith("// 功能：")
        assert lines[2].startswith("// 地址：")
        blocks.extend(lines[4:])
    return "\n".join(blocks)


# 功能：对明确的局部参数进行单词替换；入参：正文、名称映射；返回：替换后的正文。
def rename_tokens(body, mapping):
    if not mapping:
        return body
    pattern = r"\b(" + "|".join(map(re.escape, mapping)) + r")\b"
    return re.sub(pattern, lambda match: mapping[match[0]], body)


# 功能：修正根函数尾跳展开与包装上下文漏参；入参：原始正文、根反汇编；返回：修正正文。
def correct_root(body, assembly):
    marker = "  uStack_70 = 0x1411fc33d;"
    assert body.count(marker) == 1
    assert "+11FC077 JMP 0x1411fc320" in assembly
    assert "+11FBE9F LEA RDX,[RSP + 0x40]" in assembly
    assert "+11FBF1E LEA RDX,[RSP + 0x40]" in assembly
    prefix = body.split(marker)[0]
    assert prefix.count("WrapNumericContext();") == 2
    prefix = prefix.replace("WrapNumericContext();", "WrapNumericContext(0,auStack_78);")
    return prefix + "  // 地址 +11FC077：真实指令尾跳 victoria3.exe+11FC320，此调用写法表示尾调用。\n  CalculateDesirability(param_1,param_2);\n  return;\n}"


# 功能：生成函数调用点索引；入参：函数 RVA、边、全部节点、输出文件索引；返回：Markdown 行。
def call_lines(address, edges, nodes, files):
    lines = [f"# 调用点：victoria3.exe+{address}", "", "| 调用点 RVA | 类型 | 目标与范围 |", "| --- | --- | --- |"]
    for edge in edges:
        target = nodes.get(edge.get("to"))
        if target is None:
            label = "未解析：`" + edge["instruction"].replace("|", "\\|") + "`"
        elif target["external"]:
            label = f"外部导入 `{target['name']}`；当前项目无 DLL 函数体"
        elif target["rva"] in files:
            label = f"[+{target['rva']} {target['name']}]({files[target['rva']][0]})，深度 {target['depth']}"
        else:
            source = target["rva"]
            source_file = target["files"][0]
            label = f"[+{source} {target['name']}](../ghidra_refresh_20261003/{source_file})，深度 {target['depth']}，超出本次范围"
        lines.append(f"| `+{edge['site']}` | `{edge['kind']}` | {label} |")
    return lines


# 功能：生成全部四层函数体、调用索引和验证报告；入参：无；返回：统计字典。
def build():
    DEST.mkdir(parents=True, exist_ok=True)
    graph = read_json(EVIDENCE / "callgraph.json")
    manifest = read_json(EVIDENCE / "manifest.json")
    nodes = {row["rva"]: row for row in manifest}
    depths = compute_depths(graph)
    assert all(depths[row["rva"]] == row["depth"] for row in manifest)
    selected = sorted((row for row in manifest if depths[row["rva"]] <= MAX_DEPTH), key=lambda row: (row["depth"], int(row["rva"], 16) if not row["external"] else 0))
    selected_ids = {row["rva"] for row in selected}
    internal = [row for row in selected if not row["external"]]
    edges = [edge for edge in graph["edges"] if edge["from"] in selected_ids]
    unresolved = [edge for edge in edges if not edge.get("to")]
    boundary = [edge for edge in edges if edge.get("to") and edge["to"] not in selected_ids]
    warnings = [row for row in read_json(EVIDENCE / "decompiler_warnings.json") if row["rva"] in selected_ids]
    warned = {row["rva"] for row in warnings}
    outgoing = collections.defaultdict(list)
    for edge in edges:
        outgoing[edge["from"]].append(edge)
    files = {}
    transformed = {}
    roundtrip = []
    source_hashes = {}
    assembly = (EVIDENCE / "function_11FBDA0.asm").read_text(encoding="utf-8")
    for row in internal:
        address = row["rva"]
        assert row["status"] == "ok"
        body = source_body(row)
        source_hashes[address] = hashlib.sha256(body.encode("utf-8")).hexdigest()
        if address == ROOT_RVA:
            body = correct_root(body, assembly)
        mapping = SEMANTICS.get(address, (None, None, {}))[2]
        changed = rename_tokens(body, mapping)
        assert rename_tokens(changed, {new: old for old, new in mapping.items()}) == body
        roundtrip.append(address)
        transformed[address] = changed.splitlines()
        count = max(1, (len(transformed[address]) + 1399) // 1400)
        files[address] = [f"function_{address}.md" if count == 1 else f"function_{address}_part{part + 1}.md" for part in range(count)]
    # 函数代码与调用点表分离，避免大量调用使一个文件超过行数上限。
    output_manifest = []
    for row in internal:
        address = row["rva"]
        description, params, mapping = SEMANTICS.get(address, ("按原始 Ghidra 控制流保留完整函数体；业务用途尚未独立确认。", "原型中的参数和返回类型均为 Ghidra 推断；未确认部分不赋予业务含义。", {}))
        calls = call_lines(address, outgoing[address], nodes, files)
        call_files = []
        for part, offset in enumerate(range(0, len(calls), 1700), 1):
            filename = f"calls_{address}_{part}.md"
            write_md(filename, calls[offset:offset + 1700])
            call_files.append(filename)
        for part, filename in enumerate(files[address]):
            source_links = "、".join(f"[源分片 {index + 1}](../ghidra_refresh_20261003/{name})" for index, name in enumerate(row["files"]))
            lines = [f"# `{row['name']}`（`victoria3.exe+{address}`）", "", f"最短静态调用深度：{row['depth']}；Ghidra 地址：`0x{row['address']}`；函数边界：`{row['body']}`。", "", f"原始证据：{source_links}。", "", "调用点：" + "、".join(f"[表 {index + 1}]({name})" for index, name in enumerate(call_files)) + "。", "", "本页为完整控制流伪代码；类型、栈槽与未确认的变量保持 Ghidra 记法。"]
            if mapping:
                lines += ["", "局部名称映射：" + "；".join(f"`{old}` → `{new}`" for old, new in mapping.items()) + "。"]
            if address in warned:
                lines += ["", "**证据缺口：该函数存在跳转表或坏指令警告，以下正文不能视为全部路径已恢复。见 [警告清单](decompiler_warnings.json)。**"]
            if address == ROOT_RVA:
                lines += ["", "根入口在 `+11FC077` 尾跳；下列正文移除 Ghidra 展开的评分函数，单独调用评分入口。两处包装调用依据 RDX 补入临时上下文，首参 0 仅表示该参数未使用。断言报告的零参数显示仍是 Ghidra 原型缺口，不能当作真实零参数 ABI。"]
            if len(files[address]) > 1:
                lines += ["", f"函数正文分片 {part + 1}/{len(files[address])}；各分片按顺序连接，续片不是独立函数。", "、".join(f"[分片 {index + 1}]({name})" for index, name in enumerate(files[address]))]
            lines += ["", "```cpp", f"// 功能：{description}", f"// 入参及返回：{params}", f"// 地址：victoria3.exe+{address}；沿用既有函数名 {row['name']}。", ""]
            lines += transformed[address][part * 1400:(part + 1) * 1400] + ["```"]
            write_md(filename, lines)
        output_manifest.append(dict(row, files=files[address], source_files=row["files"], call_files=call_files, parameter_aliases=mapping, has_warning=address in warned))
    index_files = []
    for offset in range(0, len(internal), 150):
        filename = f"index_{offset // 150 + 1:02d}.md"
        lines = ["# Refresh 四层函数索引", "", "| RVA | 既有名称 | 深度 | 完整正文 | 证据警告 |", "| --- | --- | ---: | --- | --- |"]
        for row in internal[offset:offset + 150]:
            address = row["rva"]
            links = "、".join(f"[分片 {index + 1}]({name})" for index, name in enumerate(files[address]))
            lines.append(f"| `+{address}` | `{row['name']}` | {row['depth']} | {links} | {'有' if address in warned else '无已登记警告'} |")
        write_md(filename, lines)
        index_files.append(filename)
    write_json("manifest.json", output_manifest)
    write_json("callgraph.json", dict(graph, nodes=selected, edges=edges, max_requested_depth=MAX_DEPTH, edge_scope="all outgoing edges of selected nodes; boundary targets are not expanded"))
    write_json("unresolved_edges.json", unresolved)
    write_json("boundary_edges.json", boundary)
    write_json("external_symbols.json", [row for row in selected if row["external"]])
    write_json("decompiler_warnings.json", warnings)
    summary = {"root_rva": ROOT_RVA, "max_depth": MAX_DEPTH, "internal_functions": len(internal), "external_symbols": len(selected) - len(internal), "depth_counts": dict(collections.Counter(row["depth"] for row in internal)), "source_body_lines": sum(row["lines"] for row in internal), "generated_code_files": sum(map(len, files.values())), "outgoing_edges": len(edges), "boundary_edges": len(boundary), "unresolved_kind_counts": dict(collections.Counter(edge["kind"] for edge in unresolved)), "warning_functions": len(warned), "index_files": index_files}
    write_json("summary.json", summary)
    write_readme(summary)
    # 重新从落盘分片提取正文，验证生成完整性，而非仅检查内存中的字符串。
    for row in internal:
        reconstructed = []
        for filename in files[row["rva"]]:
            text = (DEST / filename).read_text(encoding="utf-8")
            code = re.search(r"```cpp\n(.*?)\n```", text, re.S)[1].splitlines()[4:]
            reconstructed.extend(code)
        assert reconstructed == transformed[row["rva"]], f"Body mismatch: {row['rva']}"
    checked_links = 0
    max_lines = 0
    for path in DEST.glob("*.md"):
        text = path.read_text(encoding="utf-8")
        max_lines = max(max_lines, len(text.splitlines()))
        assert len(text.splitlines()) <= 2000, f"Oversized: {path}"
        for link in re.findall(r"\]\(([^)]+)\)", text):
            # 验证报告在全部检查通过后写入，最后独立检查该链接存在。
            if path.name == "README.md" and link == "verification.json":
                continue
            assert (path.parent / link.split("#")[0]).exists(), f"Broken link: {path}: {link}"
            checked_links += 1
    assert len(roundtrip) == len(internal) == 333
    assert len(selected) - len(internal) == 19
    verification = {"validation_errors": [], "bfs_matches_original_manifest": True, "all_generated_code_reassembled_matches_transform": True, "all_parameter_aliases_roundtrip": True, "functions_checked": len(roundtrip), "links_checked": checked_links, "max_markdown_lines": max_lines, "source_body_sha256": source_hashes, "root_corrections": ["split tail-expanded CalculateDesirability at PE boundary", "restore ignored RCX and RDX temp arguments in two WrapNumericContext calls"], "executable_sha256": graph["executable_sha256"], "original_verification": read_json(EVIDENCE / "verification.json")}
    write_json("verification.json", verification)
    assert (DEST / "verification.json").exists()
    print(json.dumps(summary, ensure_ascii=True))
    return summary


# 功能：生成阅读入口和证据边界；入参：统计字典；返回：无。
def write_readme(summary):
    lines = ["# Refresh 四层伪代码", "", "入口：`victoria3.exe+11FBDA0`，分析日期：2026-10-03。", "", f"已生成 **{summary['internal_functions']} 个内部函数**的完整可用 Ghidra 函数体，另记录 **{summary['external_symbols']} 个外部导入**。正文覆盖原始导出约 {summary['source_body_lines']} 行，不是只列函数名或简化业务骨架。", "", "深度定义：Refresh 为 0，直接调用/尾跳为 1，最多沿 4 条已解析静态边。BFS 按最短路径去重；共享函数和循环只输出一次。深度 4 的函数也输出完整正文，其继续调用的深度 5 目标列入边界表，不递归展开。", "", "| 内部函数深度 | 数量 |", "| --- | ---: |"]
    lines += [f"| {depth} | {count} |" for depth, count in sorted(summary["depth_counts"].items())]
    lines += ["", "- [Refresh 正文](function_11FBDA0.md)", "- [业务语义与历史 opcode 对照](semantic_notes.md)"]
    lines += [f"- [函数索引 {index + 1}]({filename})" for index, filename in enumerate(summary["index_files"])]
    lines += ["- [机器可读函数清单](manifest.json)", "- [范围内函数的全部出边](callgraph.json)", "- [深度边界出边](boundary_edges.json)", "- [未解析调用及跳转](unresolved_edges.json)", "- [外部符号](external_symbols.json)", "- [反编译警告](decompiler_warnings.json)", "- [验证结果](verification.json)", "", f"当前范围有 {summary['unresolved_kind_counts'].get('unresolved_indirect_call', 0)} 处未解析间接调用、{summary['unresolved_kind_counts'].get('unresolved_computed_jump', 0)} 处未解析计算跳转，{summary['warning_functions']} 个函数带警告。因此能覆盖的是已解析静态边范围；无法声称恢复了所有运行时相关代码。外部符号没有当前项目内的 DLL 函数体。", "", "类型仍采用 Ghidra 的 `longlong/undefined*/CONCAT*/SUB*/SEXT*` 记法，定点运算的溢出阈值、拆分乘除、清理、异常和报告路径完整保留。尚未确认的函数沿用 `FUN_...` 名称，不虚构游戏类或业务接口。源代码中的英文警告作为原始 Ghidra 证据逐字保留，新加分析注释为中文。", "", "Refresh 的两项显式修正：按 PE 与 opcode 将尾跳评分恢复为独立调用；按 RDX 恢复两处 WrapNumericContext 的上下文参数。其余函数仅做明确的局部名称替换；验证已对名称反向还原、正文落盘再拼接及链接逐项核对。伪代码可用性并不代表 ABI 和所有反编译语义已确认。", "", "源证据入口：[静态导出说明](../ghidra_refresh_20261003/README.md)、[根函数定位及证据边界](../../Docs/ghidra_refresh_20261003.md)。", "", "复现：在仓库根执行 `python Scripts/ghidra/build_refresh_depth4.py`。脚本不操作游戏进程、不改写 Ghidra 项目，仅读取已有证据并生成本目录文件。"]
    write_md("README.md", lines)


if __name__ == "__main__":
    build()
