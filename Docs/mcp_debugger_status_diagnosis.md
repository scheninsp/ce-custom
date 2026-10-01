# MCP 调试状态异常排查记录

排查日期：2026-10-01。

## 结论

当前目标确实存在可读的断点上下文。采集脚本失败的直接原因是 MCP 的 `debugger_get_status` 将 `debug_isBroken()` 的非布尔返回值视为整个状态查询失败，不是 CMD 命令或寄存器、栈接口无法运行。

当前 CE 进程中，`debug_isBroken()` 返回了该函数对象自身，而非布尔值；Lua 调试信息将其标识为原生 C 函数。已排除“返回一个普通 Lua 函数实现”的情况，但尚未定位该原生绑定为何异常，不能将问题泛化为所有 CE 7.7 安装都存在的缺陷。

初次排查只完成诊断和专用接口验证。随后根据用户要求，已在 Python 采集脚本实现固定 Lua 状态兼容查询并完成真实采集，无需重编译或重载 DLL；见本文末尾的处理结果。CE 全局函数未被替换，停止上下文和首尾会话仍受校验。

## 现场与直接证据

| 项目 | 实测结果 |
| --- | --- |
| CE 进程 | PID 72480，`C:\Program Files\Cheat Engine\cheatengine-x86_64-SSE4-AVX2.exe` |
| MCP 包 | `CheatEngine.Mcp-2.0.0-beta.2-win-x64` |
| 对照的本地 MCP 源码 | `D:\cebuild\CheatEngine.Mcp`，HEAD `c51a0ec` |
| 目标进程 | `victoria3`，PID 43884，64 位 |
| 当前 RIP | `7FF777CED5C9` |
| 当前 RSP | `8C5DE8D870` |
| 当前 RBP | `8C5DE8DD30` |
| 调试器接口 | `debug_getCurrentDebuggerInterface()` 返回整数 `1`，对应 Windows 调试器 |

`debugger_get_status` 原始错误：

```text
CheatEngine.Mcp/debugger_get_status:4: debug_isBroken did not return a boolean debugger state
```

该响应同时将 `stateValid`、`attached`、`broken`、`reportedBroken` 等字段置为 false。这些 false 是错误分支的默认值，不能据此认定用户未附加或未停止。

通过临时、只读的 `lua_execute` 诊断片段检查各函数的实际返回类型；片段仅使用局部变量、查询函数与 `debug.getinfo`，未替换全局函数：

| 查询 | 返回类型 | 返回内容 |
| --- | --- | --- |
| `debug_isDebugging()` | boolean | true |
| `debug_canBreak()` | boolean | true |
| `debug_isBroken()` | function | 与 `_G.debug_isBroken` 相等 |
| `debug_isStepping()` | boolean | false |
| `debug_getCurrentDebuggerInterface()` | number | 1 |
| `debug_getCurrentContextTable(false)` | table | 包含 RIP `7FF777CED5C9` |

`debug.getinfo(debug_isBroken, 'S')` 返回 `what='C'`、`source='=[C]'`。诊断使用通用 Lua 工具是为了区分原生返回类型和 MCP 校验错误；该工具未加入采集脚本的六项业务工具白名单。

## 寄存器和 Stacktrace 专用接口验证

为排查故障范围，诊断阶段直接调用了现有只读接口，并复用了采集脚本的结构校验函数；这不改变正式脚本要求先通过 stopped 校验的流程。

- `debugger_get_context(includeExtraRegisters=true)` 成功，`is64Bit=true`、`includesExtraRegisters=true`。
- 共返回 43 个寄存器，包括通用寄存器、EFLAGS、THREADID、FP0–FP7、XMM0–XMM15。
- `validate_context` 校验通过，规范化地址为 `7FF777CED5C9`。
- `debugger_get_stack_trace(depth=128)` 成功，`scannedSlots=128`，`pointerSize=8`，返回 1 个启发式 frame。
- `validate_stacktrace` 校验通过；候选 frame 不等于经过符号确认的调用链。
- 诊断前后 `process` 身份一致；`resourceCount` 为 0→0，`jobCount` 为 0→0。
- 所有本次启动的 Gateway 均在 finally 中关闭。没有调用 attach、continue、pause、detach、断点修改或目标内存写入工具。

## 源码定位

`D:\cebuild\CheatEngine.Mcp\srcs\CheatEngine.Mcp.Tools\Debugger\DebuggerLuaScripts.cs` 的 `Status`：

```lua
local function read(name, ...)
   local value = _G[name](...)
   assert(type(value) == 'boolean', name .. ' did not return a boolean debugger state')
   return value
end
```

它对主停止证据和辅助停止标志都使用同样的严格读取：

```lua
broken = attached and read('debug_getContext', false) or false,
reportedBroken = attached and read('debug_isBroken') or false,
```

只要辅助字段断言失败，外层 `pcall` 的错误分支就会把整个状态置为无效，掩盖已经成功读取的停止上下文。

`DebuggerRecords.cs` 将 `Broken` 描述为 `debug_getContext` 证明的停止状态，而 `ReportedBroken` 描述为 `debug_isBroken` 的独立报告。当前两者都使用非 nullable 的 bool，修复时需明确缺失辅助值如何表达。

本地 `NativeLuaAsmDebuggerV2Tests.cs` 已有“未附加时不调用异常 debug_isBroken”的测试，但未覆盖“已附加且上下文可读、debug_isBroken 返回函数对象”的本次现场。

本地 CE 源码 `D:\cebuild\cheat-engine\Cheat Engine\LuaHandler.pas` 中的 `debug_isBroken` 则会调用 `lua_pushboolean(L, r)`，与当前运行实例的实测行为不一致。因此，不能仅凭该源码断定已安装二进制内部的具体错误；仍需区分安装构建、原生绑定或运行期替换等原因。

## 建议修复边界

优先在 MCP 插件的状态查询实现中兼容异常的辅助查询：

1. 继续严格验证 `debug_isDebugging()`，并以布尔型 `debug_getContext(false)` 证明是否有停止上下文。
2. 对 `debug_isBroken()` 独立读取并保留返回值有效性。非布尔值不应推翻已验证的 `broken`，也不能使用 Lua 普通真值转换：函数对象会被错误解释为 true。
3. 让辅助字段能够诚实表达不可用，例如 nullable 的 `reportedBroken` 加诊断字段；同步调整记录类型、JSON schema、工具合同和相关测试。不要把推导值冒充 `debug_isBroken` 的实际报告。
4. 增加已附加/未附加、停止/运行、辅助函数返回 boolean/function/nil 或抛错的回归测试；主停止证据无效仍须失败。
5. Python 入口可单独改进错误展示：优先显示 MCP 返回的 `error`，避免仅输出 `stateValid=false` 让人误判现场。此项只改善诊断，不能代替插件修复。

修复后先完成 NativeLua 和合同测试、构建独立部署包，再安排插件更新和真实采集验收。正在使用的 CE 断点现场未被重启或重载插件。

## CMD 命令

当前脚本支持以下入口，已通过固定 Lua 查询绕过这项已知接口错误：

```cmd
cd /d D:\cebuild\ce-custom
python Scripts\get_stacktrace_register_at_breakpoint.py
```

初次诊断未生成正式报告；后续兼容处理结果如下。

## 已完成的兼容处理

- `debugger_get_status` 正常时沿用原路径；只有已知的 `debug_isBroken` 非布尔断言失败才进入固定 Lua 查询。
- 以 `debug_isDebugging` 和 `debug_getCurrentContextTable(false)` 确认停止，不使用异常函数，不替换 CE 全局变量或函数。
- 寄存器与栈继续使用 MCP 专用工具；首尾兼容查询的 IP/SP 与快照比对，会话指纹和资源计数继续复核。
- `lua_execute` 只允许专用固定源码调用；不纳入通用只读工具白名单。报告保留原始失败和兼容响应，不伪造 reportedBroken。
- 实际 CMD 执行退出 0，输出 `Output/streg_7FF777CED5C9.md`，目标 PID 43884，43 个寄存器，128 个栈槽，1 个启发式候选，资源及作业计数均为 0→0。
- 报告中的首尾 RIP 均为 `7FF777CED5C9`，RSP 均为 `8C5DE8D870`；原始 JSON 校验通过。
- 全量 51 项离线测试与 py_compile 通过。未修改 `D:\cebuild\CheatEngine.Mcp` 源码或安装中的 DLL。

插件内部异常仍然存在，但当前采集流程已可工作。未来如需彻底修复插件，前述源码修复建议仍适用。
