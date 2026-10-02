# 功能：只读读取当前 R14 对象的相邻字段并核对断点现场，不修改目标状态。
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path('Scripts').resolve()))
from ce_mcp_client import McpClient
out=Path('Output/scoring_supplement2_20261002')
instance=json.loads((out/'instances.json').read_text(encoding='utf-8'))['instances'][0]['instanceId']
before=json.loads((out/'context_before.json').read_text(encoding='utf-8'))
breaks=json.loads((out/'breakpoints_before.json').read_text(encoding='utf-8'))
client=McpClient([str(Path('McpExternals/CheatEngine.Mcp-2.0.0-beta.2-win-x64/CheatEngine.Mcp.Gateway.exe').resolve())],30,out/'field_gateway.log')
result={}
try:
 client.start()
 result['before_context']=client.call('debugger_get_context',{'instanceId':instance})
 result['before_breakpoints']=client.call('debugger_list_breakpoints',{'instanceId':instance,'limit':1024})
 result['fields']=client.call('memory_read_batch',{'instanceId':instance,'items':[{'address':'3A484D9F8B8','valueType':'int32'},{'address':'3A484D9F8BC','valueType':'int32'},{'address':'3A484D9F8B8','valueType':'bytes','size':16}]})
 result['after_context']=client.call('debugger_get_context',{'instanceId':instance})
 result['after_breakpoints']=client.call('debugger_list_breakpoints',{'instanceId':instance,'limit':1024})
 result['unchanged']=result['before_context']==result['after_context'] and result['before_breakpoints']==result['after_breakpoints']
 print(json.dumps(result,ensure_ascii=False))
finally:
 (out/'field_read.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
 client.close()
