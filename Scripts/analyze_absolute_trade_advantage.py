# 功能：只读解析 Victoria 3 的 PE，导出绝对贸易优势的配置交叉引用及字段访问证据。
from __future__ import annotations

import argparse
import hashlib
import json
import re
import struct
from pathlib import Path

import capstone
import pefile


# 功能：读取 PE、定位 RIP 相对引用并保存证据；入参：命令行路径；返回：无。
def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--exe", default=r"D:\Games\Victoria3\Victoria 3\binaries\victoria3.exe")
    parser.add_argument("--output", default="Output/2026-10-4-process2/absolute_trade_advantage")
    args = parser.parse_args()
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    raw = Path(args.exe).read_bytes()
    pe = pefile.PE(data=raw, fast_load=True)
    base = pe.OPTIONAL_HEADER.ImageBase
    decoder = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    decoder.detail = True
    strings = {}
    pattern = rb"(?:state_(?:max_)?(?:trade|import|export)_advantage[a-z_]*|power_bloc_trade_advantage_add|TRADE_(?:CENTER_)?[A-Z_]*ADVANTAGE[A-Z_]*|ADVANTAGE_[A-Z_]+)\x00"
    for match in re.finditer(pattern, raw):
        strings[base + pe.get_rva_from_offset(match.start())] = match.group()[:-1].decode("ascii")
    entries = []
    for entry in pe.parse_exceptions_directory(pe.OPTIONAL_HEADER.DATA_DIRECTORY[3].VirtualAddress, pe.OPTIONAL_HEADER.DATA_DIRECTORY[3].Size):
        entries.append((entry.struct.BeginAddress, entry.struct.EndAddress))

    # 功能：按异常表获取所属函数边界；入参：RVA；返回：起止 RVA 或短窗口。
    def bounds(rva: int) -> tuple[int, int]:
        for begin, end in entries:
            if begin <= rva < end:
                return begin, end
        return rva, rva + 256

    # 功能：格式化指令及字符串目标；入参：指令；返回：一行证据文本。
    def line(ins) -> str:
        labels = []
        for operand in ins.operands:
            if operand.type == capstone.CS_OP_MEM and operand.mem.base == capstone.x86.X86_REG_RIP:
                target = ins.address + ins.size + operand.mem.disp
                labels.append(f"RIP_TARGET=+{target-base:X}")
                if target in strings:
                    labels.append(strings[target])
        return f"+{ins.address-base:X}\t{ins.bytes.hex().upper()}\t{ins.mnemonic} {ins.op_str}" + ("\t" + " | ".join(labels) if labels else "")

    xrefs = []
    functions = {0x1226160, 0x1228B90, 0x13C2350, 0x1226080, 0x13C1A10, 0xC3CAC0, 0x1229C50}
    field_access = []
    for section in pe.sections:
        if not section.Characteristics & 0x20000000:
            continue
        data = section.get_data()
        section_base = base + section.VirtualAddress
        for match in re.finditer(rb"[\x48-\x4f][\x8d\x8b\x89][\x05\x0d\x15\x1d\x25\x2d\x35\x3d]....", data, re.DOTALL):
            pos = match.start()
            target = section_base + pos + 7 + struct.unpack_from("<i", data, pos + 3)[0]
            if target in strings:
                rva = section.VirtualAddress + pos
                begin, end = bounds(rva)
                xrefs.append({"string": strings[target], "string_rva": f"{target-base:X}", "xref_rva": f"{rva:X}", "function_rva": f"{begin:X}"})
                if "advantage" in strings[target].lower():
                    functions.add(begin)
        # 寻找容量缓存字段，先匹配位移再解码所属函数，避免全模块解码。
        for match in re.finditer(re.escape(struct.pack("<i", 0x1D58)), data):
            begin, end = bounds(section.VirtualAddress + match.start())
            if end - begin > 200000:
                continue
            for ins in decoder.disasm(pe.get_data(begin, end-begin), base+begin):
                if any(op.type == capstone.CS_OP_MEM and op.mem.disp == 0x1D58 for op in ins.operands):
                    field_access.append({"function_rva": f"{begin:X}", "instruction": line(ins)})
                    functions.add(begin)
    for begin in sorted(functions):
        begin, end = bounds(begin)
        if end - begin > 300000:
            continue
        instructions = decoder.disasm(pe.get_data(begin, end-begin), base+begin)
        (output / f"function_{begin:X}.asm").write_text("\n".join(line(ins) for ins in instructions) + "\n", encoding="utf-8")
    # 配置注册函数在字符串引用后保存数值或修正类型编号，保留邻近写操作。
    registrations = []
    for ref in xrefs:
        if not ref["string"].startswith(("state_", "power_bloc_", "TRADE_")):
            continue
        rva = int(ref["xref_rva"], 16)
        stores = []
        for ins in decoder.disasm(pe.get_data(rva, 1300), base+rva):
            if ins.mnemonic == "mov" and ins.operands and ins.operands[0].type == capstone.CS_OP_MEM and ins.operands[0].mem.base == capstone.x86.X86_REG_RIP:
                stores.append(line(ins))
        registrations.append({**ref, "nearby_global_stores": stores})
    evidence = {"exe": args.exe, "sha256": hashlib.sha256(raw).hexdigest(), "image_base": hex(base), "string_xrefs": xrefs, "registrations": registrations, "capacity_field_access": list({v["instruction"]: v for v in field_access}.values())}
    (output / "evidence.json").write_text(json.dumps(evidence, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Exported {len(functions)} functions, {len(xrefs)} string references")


if __name__ == "__main__":
    main()
