# 功能：从已保存的静态控制流导出中提取评分与价格函数证据。
import json
from pathlib import Path
root=Path('.'); out=root/'Output/scoring_supplement2_20261002'
base=int(json.loads((out/'module.json').read_text())['modules'][0]['base'],16)
entries={
 'refresh':'Output/goal3_static_20261002/function_7FF777CEBDA0.json',
 'execute':'Output/goal3_static_20261002/function_7FF777CED470.json',
 'context':'Output/goal3_static_20261002/function_7FF777E0D540.json',
 'price':'Output/goal3_scoring_20261002/function_7FF777EFA6B0.json',
}
terms=['11FD370','11FDBDA0','11FC320','1408330','13A3280','13A3B10','13A5280','1726A10','1726AF0','11FC080']
for name,path in entries.items():
 data=json.loads((root/path).read_text())
 rows=sorted((row for block in data['blocks'] for row in block.get('instructions',[])),key=lambda x:int(x['address'],16))
 selected=[]
 for row in rows:
  text=(row.get('opcode','')+' '+row.get('extra','')).upper()
  if any(term in text for term in terms): selected.append(row)
  if name=='refresh' and int(row['address'],16)-base in range(0x1fd5b0,0x1fd750): selected.append(row)
 out.joinpath(name+'_selected.json').write_text(json.dumps(selected,ensure_ascii=False,indent=2),encoding='utf-8')
 out.joinpath(name+'_selected.md').write_text('\n'.join(f"+{int(r['address'],16)-base:X} {r['opcode']} {r.get('extra','')}" for r in selected)+'\n',encoding='utf-8')
 print(name,len(rows),len(selected))


