from pathlib import Path
import json
root=Path('.')
out=root/'Output/scoring_supplement2_20261002'
terms=['7FF777CED370','7FF777CEBDA0','7FF777CEC320','7FF777EFA6B0','7FF777EF3280','7FF777EF3B10','7FF777EF5280','7FF77826A10','7FF77826AF0']
entries={'refresh':'Output/goal3_static_20261002/function_7FF777CEBDA0.json','execute':'Output/goal3_static_20261002/function_7FF777CED470.json','context':'Output/goal3_static_20261002/function_7FF777E0D540.json','price':'Output/goal3_scoring_20261002/function_7FF777EFA6B0.json'}
base=int(json.loads((root/'Output/goal3_static_20261002/module.json').read_text(encoding='utf-8'))['base'],16)
for name,path in entries.items():
 data=json.loads((root/path).read_text(encoding='utf-8')); rows=sorted((r for b in data['blocks'] for r in b.get('instructions',[])),key=lambda x:int(x['address'],16)); selected=[]
 for r in rows:
  text=(r.get('opcode','')+' '+r.get('extra','')).upper()
  if any(t in text or t in r.get('text','').upper() for t in terms) or (name=='refresh' and 0x1fd5b0 <= int(r['address'],16)-base <= 0x1fd750): selected.append(r)
 out.joinpath(name+'_selected.json').write_text(json.dumps(selected,ensure_ascii=False,indent=2),encoding='utf-8')
 out.joinpath(name+'_selected.md').write_text('\n'.join(f"+{int(r['address'],16)-base:X} {r['opcode']} {r.get('extra','')}" for r in selected)+'\n',encoding='utf-8')
 print(name,len(rows),len(selected))


