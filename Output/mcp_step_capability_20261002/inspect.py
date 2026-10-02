# 功能：检查 MCP 单步工具目录和当前调试状态；仅执行只读查询。
import sys,json
from pathlib import Path
sys.path.insert(0,str(Path('Scripts').resolve()))
from ce_mcp_client import McpClient
out=Path('Output/mcp_step_capability_20261002')
c=McpClient([str(Path('McpExternals/CheatEngine.Mcp-2.0.0-beta.2-win-x64/CheatEngine.Mcp.Gateway.exe').resolve())],30,out/'gateway.log')
try:
 c.start(); tools=c.tools();
 selected={n:tools[n] for n in tools if n in {'debugger_step','debugger_continue','debugger_get_context','debugger_get_status','debugger_get_stack_trace'}}
 (out/'tools.json').write_text(json.dumps(selected,ensure_ascii=False,indent=2),encoding='utf-8')
 listing=c.call('instance_list',{});(out/'instances.json').write_text(json.dumps(listing,ensure_ascii=False,indent=2),encoding='utf-8')
 print('TOOLS',json.dumps({n:t['inputSchema'] for n,t in selected.items()},ensure_ascii=False))
 print('INSTANCES',json.dumps(listing,ensure_ascii=False))
 if listing.get('instances'):
  iid=listing['instances'][0]['instanceId']
  for name,args in [('runtime_get_overview',{}),('debugger_get_status',{}),('debugger_get_context',{})]:
   if name in tools:
    result=c.call(name,{'instanceId':iid,**args});(out/(name+'.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(name,json.dumps(result,ensure_ascii=False))
finally:c.close()
