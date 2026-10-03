# 功能：从当前 CE 只读采集指定 PE 函数的 opcode，按模块相对地址归档，不执行游戏代码。
import argparse
import bisect
import json
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'Scripts'))
from ce_mcp_client import McpClient
from run_opcode_export import DEFAULT_GATEWAY

OUT = Path(__file__).resolve().parent
EXE = Path(r'D:\Games\Victoria3\Victoria 3\binaries\victoria3.exe')

class Image:
    # 功能：解析本地 PE 节区与异常表；入参为可执行文件路径；返回初始化后的对象。
    def __init__(self, path=EXE):
        self.data = path.read_bytes()
        pe = struct.unpack_from('<I', self.data, 0x3c)[0]
        section_count = struct.unpack_from('<H', self.data, pe + 6)[0]
        optional_size = struct.unpack_from('<H', self.data, pe + 20)[0]
        self.preferred_base = struct.unpack_from('<Q', self.data, pe + 48)[0]
        self.sections = []
        for index in range(section_count):
            offset = pe + 24 + optional_size + 40 * index
            name = self.data[offset:offset+8].rstrip(b'\0').decode()
            virtual_size, rva, raw_size, raw = struct.unpack_from('<IIII', self.data, offset + 8)
            self.sections.append((name, rva, virtual_size, raw, raw_size))
        pdata_rva, pdata_size = struct.unpack_from('<II', self.data, pe + 24 + 112 + 24)
        pdata = self.offset(pdata_rva)
        self.functions = [struct.unpack_from('<III', self.data, offset) for offset in range(pdata, pdata+pdata_size, 12)]
        self.starts = [row[0] for row in self.functions]

    # 功能：将模块偏移转换为文件偏移；入参为 RVA；返回文件偏移，找不到则报错。
    def offset(self, rva):
        for name, start, size, raw, raw_size in self.sections:
            if start <= rva < start + raw_size:
                return raw + rva - start
        raise ValueError(f'Unmapped RVA {rva:X}')

    # 功能：查询异常表中的函数边界；入参为 RVA；返回起点、终点和展开信息偏移。
    def bounds(self, rva):
        index = bisect.bisect_right(self.starts, rva) - 1
        if index >= 0 and self.functions[index][0] <= rva < self.functions[index][1]:
            start, end, unwind = self.functions[index]
            root = start
            for next_start, next_end, next_unwind in self.functions[index+1:]:
                if next_start != end:
                    break
                offset = self.offset(next_unwind)
                flags = self.data[offset] >> 3
                count = self.data[offset+2]
                if not flags & 4:
                    break
                chain = offset + 4 + ((count+1)//2)*4
                parent = struct.unpack_from('<I', self.data, chain)[0]
                if not root <= parent < end:
                    break
                end = next_end
            return start, end, unwind
        raise ValueError(f'No pdata function for RVA {rva:X}')

# 功能：采集若干静态函数并验证磁盘代码一致性；入参来自命令行 RVA；返回无。
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('rvas', nargs='+')
    args = parser.parse_args()
    image = Image()
    client = McpClient([str(DEFAULT_GATEWAY)], 90, OUT / 'gateway_capture.stderr.log').start()
    try:
        listing = client.call('instance_list', {})
        if len(listing['instances']) != 1:
            raise ValueError('Expected one CE instance')
        instance = listing['instances'][0]['instanceId']
        module = client.call('module_get', {'instanceId': instance, 'module': 'victoria3.exe'})
        base = int(module['base'], 16)
        (OUT / 'module_get.json').write_text(json.dumps(module, indent=2), encoding='utf-8')
        for value in args.rvas:
            requested = int(value, 16)
            start, end, unwind = image.bounds(requested)
            destination = OUT / f'function_{start:X}.json'
            if destination.exists() and json.loads(destination.read_text(encoding='utf-8'))['end'] == f'{end:X}':
                print(f'EXISTS +{start:X}')
                continue
            cursor = start
            instructions = []
            while cursor < end:
                response = client.call('code_disassemble', {'instanceId': instance, 'address': f'{base+cursor:X}', 'before': 0, 'count': min(512, end-cursor)})
                rows = response['instructions']
                if not rows or int(rows[0]['address'],16) != base+cursor:
                    raise ValueError('Noncontiguous instruction window')
                for row in rows:
                    rva = int(row['address'], 16) - base
                    if rva >= end:
                        break
                    raw = bytes.fromhex(row['bytes'])
                    offset = image.offset(rva)
                    if image.data[offset:offset+len(raw)] != raw:
                        raise ValueError(f'Live/disk opcode mismatch at {rva:X}')
                    row['rva'] = f'{rva:X}'
                    instructions.append(row)
                cursor = int(instructions[-1]['rva'],16) + instructions[-1]['size']
            result = {'base': f'{base:X}', 'start': f'{start:X}', 'end': f'{end:X}', 'unwind': f'{unwind:X}', 'liveDiskMatch': True, 'instructions': instructions}
            destination.write_text(json.dumps(result, indent=2), encoding='utf-8')
            lines = [f"+{row['rva']} {row['bytes']:30} {row['opcode']}" for row in instructions]
            (OUT / f'function_{start:X}.asm').write_text('\n'.join(lines)+'\n', encoding='utf-8')
            calls = []
            for row in instructions:
                raw = bytes.fromhex(row['bytes'])
                if raw[0] in (0xe8, 0xe9) and len(raw) == 5:
                    target = int(row['rva'],16) + 5 + int.from_bytes(raw[1:], 'little', signed=True)
                    calls.append(f"+{row['rva']}->{target:X}")
            print(f'CAPTURE +{start:X}..+{end:X} {len(instructions)} instructions; calls: '+', '.join(calls))
        overview = client.call('runtime_get_overview', {'instanceId': instance})
        (OUT/'final_overview.json').write_text(json.dumps(overview,indent=2),encoding='utf-8')
    finally:
        client.close()

if __name__ == '__main__':
    main()

