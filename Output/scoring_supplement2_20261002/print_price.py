import json
from pathlib import Path
root=Path('Output/goal3_scoring_20261002')
d=json.loads((root/'function_7FF777EFA6B0.json').read_text(encoding='utf-8'))
rows=sorted((r for b in d['blocks'] for r in b.get('instructions',[])),key=lambda x:int(x['address'],16))
for r in rows:
 if r['opcode'].startswith('call') or 'imul' in r['opcode'] or 'idiv' in r['opcode'] or 'sar' in r['opcode'] or 'shr' in r['opcode'] or 'cmp' in r['opcode'] or 'cmov' in r['opcode']:
  print(f"{int(r['address'],16)-0x7FF776AF0000:X} {r['opcode']} {r.get('extra','')}")
