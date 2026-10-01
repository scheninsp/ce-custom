# 断点状态兼容查询 实施方案

我将使用 writing-plans 能力生成完整实施方案。

> 面向自动化执行人员：使用 executing-plans 逐任务执行本方案，按复选框记录进度。

**目标：** 不重编译或重载 MCP DLL，让现有 CMD 无参数采集命令在 debug_isBroken 返回异常类型时正常采集。
**架构方案：** 保留正常 debugger_get_status 路径，仅对已实测的特定错误执行固定 lua_execute 查询。使用 debug_isDebugging 和 debug_getCurrentContextTable(false) 判定停止，保留原始错误和 Lua 响应，继续使用专用寄存器、栈工具。
**技术栈：** Python 标准库、现有 McpClient、MCP lua_execute、CE Lua 5.3。

## 全局约束

- 不改 MCP 源码或部署包，不替换 CE 全局函数，不附加、继续、暂停、修改断点或写目标内存。
- lua_execute 仅由专用函数发送固定查询；不加入通用只读工具白名单，不接受用户 Lua 参数。
- 仅当原状态 stateValid=false 且 error 为 debug_isBroken 非布尔状态断言时回退；其他错误保持失败。
- Lua 正常结果要求 ok=true、hostEffect=completed、droppedOpaqueCount=0，returnValues 中恰好一个字典；未知效果及执行失败退出 3，工具能力未启用退出 2。
- 前后兼容状态的 IP/SP 必须与 context 及 stacktrace 对应值一致，发生变化退出 3。
- 中文注释，英文日志；关闭自行启动的 Gateway，报告仍使用 atomic_text。

## 任务 1：状态兼容适配

**涉及文件：** `Scripts/get_stacktrace_register_at_breakpoint.py`。
**接口依赖：** `read_status(client, instance_id, *, collecting=False, compat_available=False) -> dict` 返回原生状态或带来源、原始响应的兼容状态；`check_status_context(status, context, address) -> None` 校验采集一致性。

- [x] 启动目录检查返回 lua_execute 的 instanceId/source/chunkName 参数是否可用，缺少该可选工具不影响正常路径。
- [x] 使用以下固定逻辑构建 Lua 常量，所有变量均为 local，不调用异常函数：

```lua
local attached = debug_isDebugging()
assert(type(attached) == 'boolean', 'Invalid attached state')
local context = attached and debug_getCurrentContextTable(false) or nil
local broken = type(context) == 'table'
local is64Bit = targetIs64Bit()
assert(type(is64Bit) == 'boolean', 'Invalid target architecture')
local active = nil
if attached then
    local interfaces = {[1]='windows', [2]='veh', [3]='kernel'}
    active = interfaces[debug_getCurrentDebuggerInterface()]
    assert(active ~= nil, 'Unsupported debugger interface')
end
local result = {stateValid=true, attached=attached, broken=broken, activeInterface=active, is64Bit=is64Bit}
if broken then
    local ip = context[is64Bit and 'RIP' or 'EIP']
    local sp = context[is64Bit and 'RSP' or 'ESP']
    assert(math.type(ip) == 'integer' and ip ~= 0, 'Invalid stopped instruction pointer')
    assert(math.type(sp) == 'integer', 'Invalid stopped stack pointer')
    result.instructionPointer = string.format('%X',ip)
    result.stackPointer = string.format('%X',sp)
end
return result
```

- [x] 用兼容适配函数替换前后两次状态调用；保留其他调用顺序、会话指纹及资源计数校验。前后地址不一致抛 CaptureError(code=3)。
- [x] 报告记录 statusSource 及原始状态错误、Lua 响应；reportedBroken 不伪造为布尔值。

## 任务 2：验证与文档

**涉及文件：** `Scripts/tests/test_stacktrace_register.py`、`Docs/stacktrace_register.md`、`Docs/mcp_debugger_status_diagnosis.md`。
**接口依赖：** 假客户端复用现有 FakeMcp，仅兼容专用固定查询；所有数据位于临时目录。

- [x] 覆盖回退成功、非特定错误不回退、工具缺失、功能禁用、Lua 执行失败、非 completed 效果、返回字段错误、前后 IP/SP 变化、中断关闭客户端。断言 lua_execute 参数与固定常量完全一致。
- [x] 运行定向及全量 unittest、py_compile，检查本次文件空白问题。
- [x] 通过 cmd.exe 执行 `cd /d D:\cebuild\ce-custom && python Scripts\get_stacktrace_register_at_breakpoint.py`，校验生成报告的原始快照、停止地址、寄存器、栈候选及计数。
- [x] 更新操作说明与诊断记录，明确本次用户授权的兼容路径扩展了原六工具约束；现有 DLL 无需重编译，lua_execute 能力被禁用时需检查配置。
