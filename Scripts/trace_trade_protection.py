# 功能：只读扫描游戏磁盘 PE，核对保护期绕过调用者并导出指令及字符串证据。
import bisect
import hashlib
import json
import re
import struct
from pathlib import Path

import capstone
import pefile


# 功能：追溯指定函数的直接调用者并保存证据；入参：无；返回：无。
def main():
    source = Path(r'D:\Games\Victoria3\Victoria 3\binaries\victoria3.exe')
    raw = source.read_bytes()
    pe = pefile.PE(data=raw, fast_load=True)
    base = pe.OPTIONAL_HEADER.ImageBase
    entries = [(e.struct.BeginAddress, e.struct.EndAddress) for e in
               pe.parse_exceptions_directory(pe.OPTIONAL_HEADER.DATA_DIRECTORY[3].VirtualAddress,
                                            pe.OPTIONAL_HEADER.DATA_DIRECTORY[3].Size)]
    starts = [v[0] for v in entries]
    decoder = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    decoder.detail = True
    output = Path('Output/2026-10-4-process2/trade_protection')
    output.mkdir(parents=True, exist_ok=True)

    # 功能：获取异常表中的函数范围；入参：RVA；返回：起止 RVA。
    def bounds(rva):
        pos = bisect.bisect_right(starts, rva) - 1
        if pos >= 0 and entries[pos][0] <= rva < entries[pos][1]:
            return entries[pos]
        return rva, rva + 256

    calls = []
    for section in pe.sections:
        if not section.Characteristics & 0x20000000:
            continue
        data = section.get_data()
        for match in re.finditer(rb'\xe8....', data, re.DOTALL):
            site = section.VirtualAddress + match.start()
            target = site + 5 + struct.unpack_from('<i', data, match.start() + 1)[0]
            calls.append((site, target))
    roots = {0x122AC50, 0x122BD40, 0x122B9A0, 0x17B53F0, 0x17B5570}
    functions = set(roots)
    edges = []
    frontier = roots
    for depth in range(2):
        following = set()
        for site, target in calls:
            if target not in frontier:
                continue
            begin, end = bounds(site)
            decoded = list(decoder.disasm(pe.get_data(begin, end - begin), base + begin))
            if not any(i.address == base + site and i.mnemonic == 'call' for i in decoded):
                continue
            edges.append({'caller': f'{begin:X}', 'site': f'{site:X}', 'target': f'{target:X}'})
            following.add(begin)
        functions.update(following)
        frontier = following - roots
    for rva in sorted(functions):
        begin, end = bounds(rva)
        lines = []
        for ins in decoder.disasm(pe.get_data(begin, end - begin), base + begin):
            labels = []
            for op in ins.operands:
                if op.type == capstone.CS_OP_MEM and op.mem.base == capstone.x86.X86_REG_RIP:
                    target = ins.address + ins.size + op.mem.disp - base
                    labels.append(f'RIP=+{target:X}')
                    value = pe.get_data(target, 240).split(b'\0')[0]
                    if len(value) >= 4 and all(32 <= c < 127 for c in value):
                        labels.append(value.decode('ascii'))
            lines.append(f'+{ins.address-base:X}\t{ins.bytes.hex()}\t{ins.mnemonic} {ins.op_str}\t' + ' | '.join(labels))
        (output / f'function_{begin:X}.asm').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    evidence = {'sha256': hashlib.sha256(raw).hexdigest(), 'edges': edges}
    (output / 'evidence.json').write_text(json.dumps(evidence, indent=2), encoding='utf-8')
    print(json.dumps(evidence, indent=2))


if __name__ == '__main__':
    main()
