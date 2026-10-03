# 周期推算Python脚本实现计划

更新日期：2026-10-03（北京时间）。这是简单文字版计划，不使用 writing-plans skill。本次只修改计划，不实现脚本，不操作 CE 或游戏。以下新脚本名称和参数是拟定接口，尚不可运行。

操作背景见：[周期推算操作步骤指南](周期推算操作步骤指南.md)。该指南包含计数实验；本计划当前阶段改为“添加条件断点，人工运行至命中”，不要求实现指南中的全套自动计数流程。

## 一、本阶段分工

脚本/助手只负责两件事：

1. 执行用户明确指定的 Lua，返回执行结果或错误。
2. 在用户指定地址添加条件断点，输出地址、条件内容、使用的后端和设置回执，供用户人工检查。

用户负责：

1. 确认 CE 已附加正确的游戏进程，提供本次有效的州/商品筛选参数。
2. 在 CE 界面检查断点是否添加成功、地址是否正确、条件类型与条件内容是否正确。
3. 在目前已经断点住的情况下，人工执行 CE 的 Run。
4. 在游戏内检查游戏已经解除暂停并推进；必要时人工解除游戏自身暂停，直到触发目标断点。
5. 检查新断点现场、记录游戏日期和命中信息；需要继续观察时再次人工 Run。

脚本不得自动 Run、单步、挂起/恢复进程、解除游戏暂停、修改速度、等待/推进一周或自动反复继续。也不自动删除或覆盖用户已有断点。Lua 执行入口不得隐式附加上述动作；本阶段提交执行的 Lua 本身也须遵守这些限制。

## 二、仅实现两个原子命令

| 拟建脚本 | 要完成的事情 | 验证方式 |
| --- | --- | --- |
| `ce_execute_lua.py` | 从 `--source` 或 UTF-8 `--file` 执行 Lua，保存返回值、错误及请求信息 | 先执行 `return 2 + 3`，返回值应为 5；有副作用的 Lua 另由用户检查，不把接口成功当作副作用已验证 |
| `ce_set_conditional_breakpoint.py` | 在指定地址添加带指定条件的执行断点；提供条件文本或 UTF-8 条件文件，明确 Simple/Complex 类型及实际后端 | 输出设置回执和实际发送的条件；如接口支持则读回配置，最终由用户在 CE 中检查，再人工 Run 验证命中 |

复用 `Scripts/ce_mcp_client.py` 的网关调用和实例选择，参考 `Scripts/ce_utils.py`、`Scripts/ce_run_step_over.py` 的独立 CLI 风格。不为本阶段新增状态、内存、Run、暂停、捕获、计数器、游戏日期或编排脚本；必要的实例/目标校验在这两个命令内部完成。

## 三、条件断点的实现前提

此前核对的 MCP `debugger_set_breakpoint` 接口没有 condition/callback 参数，因此不能仅创建普通断点后宣称已添加条件断点。安装版 celua.txt 支持 `debug_setBreakpoint(..., functiontocall)`，但回调筛选不等于 CE 界面中的原生 Simple/Complex 条件。

先确认当前 CE 版本是否存在可用的原生条件设置入口，能否通过 Lua 或现有插件接口完成“创建执行断点 + 设置条件”。不得虚构 `debug_setBreakpointCondition` 等尚未确认的 API。接口未确认时，只完成 Lua 执行命令，并明确报告条件断点添加能力仍未实现。

本阶段目标是用户能在 CE 中检查的原生条件断点，不默认改用 Lua 回调，也不覆盖全局 `debugger_onBreakpoint`。如果只能通过回调筛选，先说明其与原生条件的差别并由用户确认是否接受，不能静默替换实现。

条件满足时应停在断点上，供用户观察；不是上一版计数实验中 `return false` 后不停下的条件。Complex 条件应返回筛选结果，不能无条件返回 false，也不能调用自动继续。

示例筛选对象为一个州商品表和一个商品：在两个候选调用点核实 `RCX` 是目标州的 `state+0x1D88` 表，`RDX` 指向的商品对象 `+0x10` 处的 4 字节商品 ID 符合目标。读取失败或参数无效时明确报错，不伪造匹配结果。具体条件由用户确认；本阶段不额外加入计数或方向筛选。

## 四、独立 CMD 接口和输出

所有命令从项目根目录执行。拟定公共参数为 `--instance-id`、`--gateway`、`--timeout`、`--output`。Lua 的 `--source` 与 `--file` 二选一；条件断点的 `--condition` 与 `--condition-file` 二选一，并显式指定 `--condition-type simple|complex`。

报告采用 UTF-8 JSON，记录实例/目标身份、请求参数、Lua/条件原文、接口回执、可读回的结果，以及“待用户人工确认”的项目。终端日志使用英文；脚本文件头和函数功能/入参/返回值说明使用中文。

返回成功只代表请求已执行且可做的检查通过，不代表用户已验收条件或真实命中。建议退出码为：0 请求完成，2 前置失败且未执行动作，3 动作已尝试但失败或效果不确定，130 中断。超时不得盲重试；可能部分完成的断点设置要报告已知状态，交给用户检查，不自动 Run 或删除。

以下仅为未来 CMD 命令示例，不是已经创建的文件：

```text
cd /d D:\cebuild\ce-custom
python Scripts\ce_execute_lua.py --source "return 2 + 3" --output Output\cycle_count
python Scripts\ce_execute_lua.py --file Output\cycle_count\setup.lua --output Output\cycle_count
python Scripts\ce_set_conditional_breakpoint.py --address "victoria3.exe+11FD93B" --condition-type complex --condition-file Output\cycle_count\trade_condition.lua --output Output\cycle_count
python Scripts\ce_set_conditional_breakpoint.py --address "victoria3.exe+11FAF69" --condition-type complex --condition-file Output\cycle_count\trade_condition.lua --output Output\cycle_count
```

示例 Lua/条件文件尚未生成。`+11FD93B` 和 `+11FAF69` 分别是已分析的增加/减少调整提交调用点，后续仍需核对当前游戏版本。命中只能证明到达提交调用点，不能直接证明内部已经成功写入。

## 五、实现与人工验收顺序

1. 实现 Lua 执行命令，用 `return 2 + 3` 验证执行和返回值；不改变当前游戏运行状态。
2. 确认原生条件设置入口，实现条件断点添加命令；检查同地址已有断点，冲突时停止，不覆盖。
3. 用户提供当前有效参数，先添加一个条件断点；用户在 CE 中核对地址和条件，再决定是否添加第二个。
4. 用户人工 Run，并检查游戏解除暂停、时间推进，直到目标断点命中；脚本不参与继续或推进。
5. 用户检查命中现场及条件筛选是否正确。需要一周计数、Write 验证或计数导出时另行确定需求，不作为这两个命令的隐式动作。

## 六、已解决的调试状态兼容问题：直接复用，不重新排障

此前 `debugger_get_status` 的 `stateValid=false` 问题已经在 Python 采集流程中通过固定只读 Lua 查询解决，不再作为本计划的待解决问题。这里是客户端兼容处理，不是插件/DLL 根因修复；原始错误分支里的 false 仍不能当作可靠状态，应使用兼容查询的验证结果。

现有实现位于 `Scripts/get_stacktrace_register_at_breakpoint.py`：复用 `STATUS_COMPAT_SOURCE`、`STATUS_COMPAT_CHUNK` 和 `read_status(...)` 的处理逻辑。需要停止现场校验时，参考 `require_stopped(...)`、`check_status_context(...)`，不为本阶段新增状态诊断脚本，也不执行采集脚本的完整入口。

- 正常情况下沿用 `debugger_get_status`。仅当 `stateValid=false` 且错误严格匹配 `CheatEngine.Mcp/debugger_get_status:<行号>: debug_isBroken did not return a boolean debugger state` 时，使用固定兼容查询；其他状态错误不能被此路径掩盖。
- 查询通过 `debug_isDebugging()` 确认调试器附加，通过 `debug_getCurrentContextTable(false)` 是否返回上下文表判断停止状态；校验目标架构及停止时 IP/SP 的有效性，不调用异常的 `debug_isBroken()`，也不将函数对象按 Lua 真值转换为 true。
- 兼容调用需要可用的 `lua_execute` 和启用的 unsafeLua 能力。检查返回 `ok=true`、`hostEffect=completed`、无不透明数据丢弃，以及返回对象字段类型；能力不可用或响应异常时明确失败，不自动修改配置。
- 报告标注 `statusSource=lua_execute_fixed_query`，保留 `originalStatus`、`luaResponse`；不伪造 `reportedBroken`。若需要确认当前停止现场，再将兼容查询的 IP/SP 与寄存器上下文核对。
- 内部状态查询只发送已有固定源码，不接收用户 Lua、条件文件或参数插值；与本计划的通用 Lua 执行入口分开。它不修改 CE 全局函数、游戏内存、断点或运行状态。

既有验收记录见：[MCP 调试状态诊断与已完成兼容处理](../mcp_debugger_status_diagnosis.md#已完成的兼容处理)。该记录确认 CMD 采集退出 0，生成 `Output/streg_7FF777CED5C9.md`，首尾 RIP/RSP 一致，资源及作业计数为 0→0，并记录当时 51 项离线测试和 py_compile 通过。这是已有验收记录，不是本次重新运行测试或查询当前现场。

相关测试在 `Scripts/tests/test_stacktrace_register.py`，覆盖兼容成功、仅允许已知错误、能力缺失、异常响应和现场变化；[调试器兼容单步采集实施方案](../superpowers/plans/2026-10-02-debugger-step-compatible-capture.md) 也已明确复用固定查询。本计划沿用这套边界，不把已解决问题重新列为实现前置阻塞。

状态检查只用于确认实例/目标及报告可证明的现场，不授权脚本执行 Run。Run、游戏暂停解除和时间推进仍完全由用户人工完成。

完成标准：两个命令可以分别从 CMD 运行；Lua 返回值或错误明确；条件断点设置内容透明且可由用户人工核对；筛选匹配时能够停下；整个过程中脚本不擅自继续执行或推进游戏。
