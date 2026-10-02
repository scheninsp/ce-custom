# 调试器兼容单步采集计划审查报告 1

- **审查日期：** 2026-10-02
- **审查对象：** `Docs/superpowers/plans/2026-10-02-debugger-step-compatible-capture.md`（工作区当前版本，SHA-256 `e0184e2f…ac26`，见第六节快照；相对 HEAD 有未提交修改，本次按工作区版本审查）。
- **需求依据：** `Docs/goal3.md`（SHA-256 `f76e1820…99bd`）、`Docs/goal3_analysis_plan.md`（SHA-256 `16aa8068…d22bd`）。
- **审查重点（用户指定）：** 1）是否存在对 CE 监控内存产生无法修复破坏的情况；2）缺漏、前后不一致、MCP 调用错误。
- **审查方式：** 静态对照计划与现有源码；实际启动 `CheatEngine.Mcp.Gateway.exe` 做只读探测（191 项 tools/list 全目录、计划涉及全部工具的 inputSchema/annotations、当前停止现场、断点列表、模块信息、指令字节、四个目标内存字段、探测前后残留对照）；只读核对本地插件源码（`DebuggerTools.Step`、`DebuggerLuaScripts.Step`、`PluginLuaToolRuntime`）与 CE 源码的 `debug_continueFromBreakpoint` 绑定；运行离线测试基线。全程未调用 `debugger_step`、未 continue/pause、未附加或分离、未设置或删除断点、未写内存、未调用任何写类工具。
- **修改范围：** 本轮只新增本报告与 `Output/mcp_step_review1_20261002/` 探测产物；未修改被审查计划、`Docs/goal3*`、任何源码或测试。

本文行号以本次审查快照为准。

## 一、结论

**方案的安全边界模型成立；在“按计划实现且阶段守卫生效”的前提下，脚本允许的工具集合内不存在任何写内存、改寄存器、增删断点、恢复运行的路径，唯一不可逆动作是 CE 核心单步（与用户在 CE 界面按 F7/F8 完全相同的一条路径）。但计划缺一个实现必需且安全相关的接口（模块基址来源），并有一处核心边界语义自相矛盾（是否允许多步），应在实施前修正；另有若干合同与表述细节需要补齐。**

对用户两个问题的直接回答：

1. **不可修复破坏：不存在计划引入的路径。** 计划允许的接口中没有任何写类工具（见第四节的完整矩阵与实测证据）；`lua_execute` 固定源码经逐行核对只读；`debugger_step` 实测注解 `readOnlyHint=false`、`destructiveHint=false`，其实现是“断言已附加且已停止 → `debug_continueFromBreakpoint(co_stepinto/over)` → 立即返回 `{mode, continued=true}`”，插件不为单步注册 job 或资源，因此关闭 Gateway 不会取消 CE 核心的单步收尾（TF 单步与断点重装由 CE 主程序调试核心完成）。脚本失败路径不调用任何恢复工具，符合计划声明。残余不确定性只剩“CE 核心自身在步进中异常”这一外部风险，与人工单步同源。
2. **MCP 能力：完全支持。** 计划点名的 10 个工具在实测目录中全部存在；`debugger_step` 的 `instanceId`/`mode(into|over)` 合同与阶段 B 调用示例逐字一致；全部查询工具注解为只读；固定 Lua 兼容查询在当前现场可用（既有生产报告同场景验证）。

需要修订的问题共 10 项，其中 2 项 P2（应在实施前修正）：

| 编号 | 问题 | 属性 | 主要影响 |
| --- | --- | --- | --- |
| S1 | 模块基址无来源：计划要求 `RIP == 模块基址+0x11FD5C9/0x11FD5D0`，但允许接口表与合同校验都没有任何模块查询工具 | P2 | 该前置安全校验无法按设计执行，或被迫绕过 |
| S2 | 单步次数语义自相矛盾：“只允许一次”与“明确指定额外步骤时可再次单步”并存 | P2 | 唯一不可逆边界的语义未定，实现与测试冲突 |
| S3 | `stepIssued` 置位点与“发送前异常→false”无法同时实现，措辞与测试断言冲突 | P3 | 边界记录可能被误报为“未发生单步” |
| S4 | 报告字段与退出码未定义（旧版“报告字段”章节被删；仅一处退出码 2） | P3 | 自动化执行与验收缺少统一契约 |
| S5 | “断点列表完整内容”超出工具实际能力（仅地址集合 + owned + total/truncated） | P3 | 实现者期待不存在的字段 |
| S6 | 单步后 “stepping” 判断在本环境不可用；轮询未绑定到兼容查询路径 | P3 | 轮询可能落空或误用原始 status |
| S7 | `R14、RDI、RSI 可读` 检查与该路线无关联且无用途说明 | P3 | 实现者误解出额外的校验义务 |
| S8 | 禁用清单含不存在的 `debugger_pause`；实际“暂停线程”工具是 `debugger_break_thread` | P3 | deny 断言可能形同虚设 |
| S9 | `unsafe_lua` 能力门未纳入前置合同校验 | P3 | 能力关闭时只能靠调用失败兜底 |
| S10 | 预检批量读取的失败判定与单步后内存读取语义未定义 | P3 | 读取失败可能不被识别；报告可能被误读 |

“单步前零副作用”“单步后不恢复”“不触碰用户断点”“只有 `debugger_step` 改变执行位置”四个设计选择与插件合同和现有工程约定一致，作为有意设计接受，不列为缺陷。

## 二、已确认可被 MCP/CE 支持且与计划一致的部分（逐条实测证据）

1. **工具存在性。** 实测 tools/list 共 191 项，计划用到的 `instance_list`、`runtime_get_info`、`runtime_get_overview`、`debugger_get_status`、`debugger_get_context`、`debugger_list_breakpoints`、`memory_read_batch`、`code_disassemble`、`lua_execute`、`debugger_step` 全部存在（缺失集合为空）。`module_get`/`module_list` 也存在（见 S1）。
2. **只读注解合同成立。** 实测 `readOnlyHint=true` 且 `destructiveHint=false`：`instance_list`、`runtime_get_info`、`runtime_get_overview`、`debugger_get_status`、`debugger_get_context`、`debugger_list_breakpoints`、`memory_read_batch`、`code_disassemble`、`memory_read`、`code_decode`、`module_get`、`module_list`。因此任务 1“所有查询工具 readOnlyHint=true、destructiveHint=false，否则退出码 2”的检查是可满足的。
3. **`debugger_step` 合同与调用示例一致。** inputSchema：`instanceId` 必填，`mode` 枚举 `["into","over"]` 默认 `into`；annotations：`readOnlyHint=false, destructiveHint=false, idempotentHint=false`，与 L165“非只读但非 destructive”一致；阶段 B 的 `client.call("debugger_step", {"instanceId":…, "mode":…})` 参数名和取值完全正确。
4. **单步实现语义（源码 + 实测行为）。** 插件 `DebuggerTools.Step` 只调用一条 Lua：`assert(debug_isDebugging())`、`assert(debug_getContext(false))`、`debug_continueFromBreakpoint(co_stepinto/co_stepover)`，随后立即返回 `{mode, continued=true}`；它不使用本环境有缺陷的 `debug_isBroken`，也不注册 job/资源（dispatchClass=`short`）。因此：响应只代表“CE 已受理继续”，不代表单步完成——计划“不以返回值判断副作用”的处理正确；关闭 Gateway 不会波及 CE 核心的单步收尾。
5. **状态兼容路径可用且已验证。** 当前现场 `debugger_get_status` 返回已知软错误（`stateValid=false` + `debug_isBroken did not return a boolean debugger state`，即使已附加且已停止也一样）；固定 `lua_execute` 兼容查询是实际可用路径。既有生产报告 `Output/streg_7FF777CED5C9.md` 在同现场以 `statusSource=lua_execute_fixed_query`、`residueCheck=unchanged` 成功产出，证明该路径在本环境成立。
6. **固定 Lua 常量可导入且只读。** `STATUS_COMPAT_SOURCE`/`STATUS_COMPAT_CHUNK` 在 `Scripts/get_stacktrace_register_at_breakpoint.py` 中存在；逐行核对仅调用 `debug_isDebugging`、`debug_getCurrentContextTable`、`targetIs64Bit`、`debug_getCurrentDebuggerInterface` 与 `string.format`，无任何写操作；导入该模块无副作用（有 `__main__` 守卫），满足“不修改现有脚本、只导入常量”的要求。
7. **路线与预期 RIP 正确。** 实测现场 RIP=`7FF777CED5C9`；`module_get` 返回 victoria3.exe base=`7FF776AF0000`，偏移恰为 `0x11FD5C9`；`code_decode` 返回字节 `41 8B 86 58 1D 00 00`（`mov eax,[r14+00001D58]`，长 7），`code_disassemble` 显示下一条 `+D0: mov [rsp+50],eax`。计划的 `+11FD5D0` 预期停点与指令长度自洽。
8. **字段读取前提成立。** `memory_read_batch` 实测：`R14+0x1D58=126`、`R14+0x1D5C=126`（与 goal3 及静态分析一致）；`[RSP+0x330]=126`、`[RSP+0x50]=130`（尚未被下一条指令覆盖的旧值）。
9. **断点现场已记录。** `debugger_list_breakpoints` 返回 3 条：`3A484D9F8B8`、`3A484D9F8BC`、`7FF777CED5C9`，全部 `owned=false`、`truncated=false`、`total=3`。前两条恰好是 `R14+0x1D58/0x1D5C` 字段地址（用户的数据断点）。单步执行 `mov eax,[r14+1D58]` 时若其为访问型硬件断点可能触发数据断点，但数据断点在指令执行后上报，停止地址仍应为 D0，属正常调试事件而非破坏（见第四节）。
10. **非调试器读取工具无 job 副作用。** `memory_read_batch`、`code_disassemble`、`module_get` 等 dispatchClass 均为 `short`，不创建 CE job，支持计划“单步前不启动 job/临时断点”的声明。
11. **只读探测零残留。** 本轮全部探测调用前后：`resourceCount 0→0`、`jobCount 0→0`、`runtime.epoch 1→1`、`process` 对象完全一致。
12. **测试与命令形式可用。** 实测 `python -m unittest Scripts.tests.test_stacktrace_register -v` 32 项通过、`python -m unittest discover -s Scripts/tests -v` 60 项全部通过（日志 `Output/mcp_step_review1_20261002/discover.log`），计划“验证流程”的命令形式可用。

## 三、逐项问题

### S1 — 模块基址无来源，直接阻塞 RIP 偏移校验

**优先级：P2。属性：缺漏（安全相关）。**

**定位：**

- 计划 L160-161、L172：“当前 RIP 等于模块基址加 `0x11FD5C9`”“RIP 等于模块基址加 `0x11FD5D0`”。
- 计划 L33-43 接口表是穷尽式声明（“实际允许调用的接口及目的如下”），其中没有任何模块查询工具；L182 接口依赖也未列；CLI 只支持 `--mode`，无基址/预期 RIP 参数。

**问题：** 没有取得模块基址的合法途径，两个关键的现场校验（起始 RIP、预期停点 RIP）按计划无法实现。实现者面临两难：要么使用表外工具（违反阶段守卫与合同校验），要么放弃该校验（可能在并非 `+11FD5C9` 的现场下发单步）。这是安全相关缺漏，不只是功能缺失。

**实测证据：**

```text
module_get {instanceId, module:"victoria3.exe"} → readOnlyHint=true, destructiveHint=false,
  base=7FF776AF0000, pe.timeDateStamp=6A3BF239, name=victoria3.exe
RIP=7FF777CED5C9；7FF777CED5C9 - 7FF776AF0000 = 0x11FD5C9（吻合）
```

**建议修订：**

- 在 L33-43 接口表加入 `module_get`（单步前，模块信息查询；失败退出、不单步），并在 `validate_tool_contract` 中校验其 `inputSchema` 含 `instanceId/module`、注解为只读；用返回的 `base` 计算两个预期 RIP，把 `name`、`pe.timeDateStamp`（本现场 `6A3BF239`）写入基线审计。
- 测试增加“`module_get` 缺失或 schema 漂移 → 单步 0 次”“base 与预期偏移不一致 → 单步 0 次”。
- 可选加固（两项都并入本项）：用 `code_disassemble`/`code_decode` 核对 RIP 处首字节 `41 8B 86 58 1D 00 00`，防止“同偏移、不同构建”的现场被当成目标现场；把构建指纹不一致也列为单步前退出条件。

### S2 — 单步次数语义自相矛盾（唯一不可逆边界的定义未定）

**优先级：P2。属性：计划内部一致性。**

**定位：**

- L13：“脚本只允许执行一次**或用户明确指定次数**的 `debugger_step`”。
- L96（阶段 C 禁止项）：“**再次调用 `debugger_step`，除非命令行明确指定了额外步骤且前一步的后置状态已完全确认**”。
- L147：“命令行不提供任意地址和任意步骤循环”；L153：“第一版固定 `--steps=1`，**不允许通过参数扩大步骤数**”；L222 测试：“验证正常单步只调用一次 `debugger_step(mode="into")`”。

**问题：** 同一份计划对“本脚本能下发几次单步”给出两种语义。单步是本方案唯一接受的不可逆边界，这个数字必须唯一确定；否则实现者可能构建被 L96 暗示多步路径（扩大了不可逆边界，也突破“第一版”安全审查范围），或者写出与文字冲突的测试。另 L29“此阶段禁止调用 `debugger_step` 之外的任何写类工具”可被读成“阶段 A 允许 `debugger_step`”，与“仅边界”的表述相互干扰。

**建议修订：**

- v1 语义写死为：**恰好一次 `debugger_step`，无 `--steps` 参数；任何第二次单步都必须作为新路线单独审查**（L153 已是此意）；删除 L13“或用户明确指定次数”、L96“除非命令行明确指定了额外步骤……”的措辞，或明确标注为“未来版本、本方案不实现”。
- 改写 L29 为“此阶段不得调用任何写类工具（包括 `debugger_step`；它只在阶段 B 出现一次）”。
- 测试补一条“阶段守卫拒绝任何第二次 `debugger_step`（不可达或抛错）”。

### S3 — `stepIssued` 置位点与“发送前异常→false”无法同时实现

**优先级：P3。属性：语义精确性。**

**定位：** L68-74（“标记必须在**发送请求前**写入……不得依赖返回值判断”）与 L197（“在调用 MCP 前设置 `audit["stepIssued"]=true`……**若 Python 在发送前异常，按 `stepIssued=false` 报告**”）；测试 L217-218 分别断言 false/true。

**问题：** 一旦按 L197 在调用前置位 true，就再无法区分“发送前异常”（如本地序列化失败）与“发送后异常”（`McpClient` 写管道失败、超时、连接断开）；现有 `McpClient.rpc/_send` 也不提供“请求是否已写出”的可靠信号。两句要求不可同时满足。

**建议修订：** 明确保守规则并同步测试：“进入 `issue_single_step` 完成本地准备后立即置 `stepIssued=true`；其后任何异常/超时/无结构结果一律按 `stepIssued=true` 记录（宁多勿少）；仅当在置位之前失败才报告 false。”L217 的“发送前异常”改为“置位前异常”，与实现可对齐。

### S4 — 报告字段与退出码未定义

**优先级：P3。属性：缺漏（契约完整性）。**

**定位：** L104 文件职责与 L182 接口依赖都只写“输出 JSON/Markdown 报告”；任务 1（L196-201）、现场验证规则（L168-176）、任务 3（L242）分散引用 `stepIssued`、`postStepState`、`unexpectedRip`、断点比较、残留/指纹、网关关闭说明等字段，但全文没有统一的报告字段表；退出码仅 L189 定义了合同失败的 2。

**问题：** 本计划面向“自动化执行人员”逐任务执行，且任务 2 需要断言报告内容与退出码；缺少契约会导致报告与文档/测试不一致（旧版计划曾有“报告字段”章节，现版本被删除但引用仍在）。

**建议修订：** 恢复一节“报告字段与退出码”，建议：

| 退出码 | 场景 |
| --- | --- |
| 0 | 单步完成，post-step 观测完成且 RIP 校验通过 |
| 2 | 单步前失败（CLI/合同/实例/runtime/状态/上下文/断点/内存读取/本地文件），保证未单步 |
| 3 | 单步前传输/会话失败；或 `stepIssued=true` 后观测失败、超时、状态无法确认 |
| 4（建议新增，或明确并入 3） | `stepIssued=true` 且 `postStepState=unknown`；报告已生成，需人工确认 |
| 130 | 用户中断 |

报告字段至少包含：`stepIssued`、原始 `debugger_step` 响应（可用时）、`postStepState(stopped/unknown)`、起始/结束 RIP+RSP+THREADID、`unexpectedRip`、PID/runtime epoch/selectionEpoch/pointerSize、断点与计数快照对照、`residueCheck`、Gateway 关闭声明、失败原因（英文诊断）。无论退出码如何，`stepIssued=true` 的路径都必须在 `finally` 落盘报告。

### S5 — “断点列表完整内容”超出工具实际能力

**优先级：P3。属性：合同理解。**

**定位：** L54（“当前断点列表完整内容”）、L163（“断点列表和单步前快照完整保存”）、L174（“比较……断点列表”）、L263（“只读用户断点列表，任何变化都报告”）。

**问题：** `debugger_list_breakpoints` 实际只返回地址集合：`{breakpoints:[{address, owned}], total, truncated}`（上限 1024、默认 256），不含条件、类型（软件/硬件/访问方式）、启用状态。按“完整内容”实现会落空或误报。

**实测证据：**

```text
debugger_list_breakpoints → total=3, truncated=false,
  [{address:3A484D9F8B8, owned:false}, {address:3A484D9F8BC, owned:false}, {address:7FF777CED5C9, owned:false}]
```

**建议修订：** 把比较对象定义为“`{breakpoints, total, truncated}` 快照全等”；报告中注明“仅地址与 owned/计数，不含条件与类型”；并说明当前两条数据断点位于 `R14+0x1D58/0x1D5C`（供解释单步时的数据断点触发可能）。

### S6 — 单步后 “stepping” 判断在本环境不可用；轮询未绑定兼容查询

**优先级：P3。属性：合同/环境适配。**

**定位：** L173（“若状态仍在 stepping 或无法确认，写 `postStepState=unknown`”）、L199（“短轮询”但未给对象、间隔与时限）。

**问题：** 本现场（CE 进程 72480）`debugger_get_status` 实测无论是否可读停止上下文都返回 `stateValid=false` + `debug_isBroken` 已知错误（已停止时亦然），其 `stepping` 字段不可用；固定 `STATUS_COMPAT_SOURCE` 也没有 `stepping` 字段（只有 `attached/broken/is64Bit` 等）。因此“仍在 stepping”只能表达为“未确认停止”：`attached=true 且 broken=false`。若实现者按字面依赖原始 status 的 `stepping`，轮询会立即失败。

**建议修订：** 明确轮询对象 = 固定兼容状态查询（必要时以 `debugger_get_context` 成功作为停止旁证），判定：`broken=true` → stopped；`attached=true 且 broken=false` → 仍在运行/单步中；给出间隔与总时限（建议总时长小于 MCP timeout，且在宣布 `unknown` 前完成全部轮询、之后才关闭 Gateway）；`stepping` 仅作为原始 status 可用时的补充记录字段。

### S7 — `R14、RDI、RSI 可读` 检查与该路线无关联

**优先级：P3。属性：缺漏/表述。**

**定位：** L164：“`R14`、`RDI`、`RSI` 可读”。

**问题：** 单步路线（`+11FD5C9` → `+11FD5D0`）只涉及 R14 与 RSP；RDI/RSI 不参与任何预检读取或 post-step 读取（本现场 `RDI=3A5FF822A80`、`RSI=3A5FF822B30` 均为对象指针）。实现者可能误解为需要额外读取 `[rdi+…]`/`[rsi+…]` 或额外校验。

**建议修订：** 删除 RDI/RSI，或补一句用途说明（例如“仅记录供上层分析，不参与校验”）；如需校验“可读”，明确其含义是“上下文寄存器值为可解析的十六进制字符串”。

### S8 — 禁用清单含不存在的工具名 `debugger_pause`

**优先级：P3。属性：准确性。**

**定位：** L13、L90、L254 均出现 `debugger_pause`。

**问题：** 实测 191 项目录中不存在 `debugger_pause`；“请求线程暂停”的实际工具是 `debugger_break_thread`（且它是异步请求，需轮询 status）。若测试按 L213“没有 continue、pause、run_to、register、breakpoint 或 job 工具调用”写 deny 断言，`debugger_pause` 永远匹配不到任何真实调用，断言形同虚设。

**建议修订：** 禁用/deny 清单改列实际存在的写类与状态类工具：`debugger_break_thread`、`debugger_attach`、`debugger_detach`、`debugger_continue`、`debugger_run_to`、`debugger_start_trace`、`debugger_start_capture`、`runtime_stop_job`、`debugger_set_breakpoint`/`debugger_delete_breakpoint`、`debugger_set_register`、`debugger_set_thread_ignored`、`memory_write`/`memory_write_batch`、`memory_set_protection`、`memory_allocate`/`memory_free`、`asm_apply_code_patch`、`process_set_paused` 等；测试断言以阶段白名单（正向）为准，deny 断言覆盖上述名字。

### S9 — `unsafe_lua` 能力门未纳入前置合同校验

**优先级：P3。属性：加固。**

**定位：** L188-189（合同校验与退出码）、L193（原始 status 失败后调用固定 Lua）。

**问题：** `lua_execute` 带 `cheatengine/requires:["unsafe_lua"]`；`runtime_get_info` 实测提供 `gates.unsafeLua=true`。当前现场可用，但计划没有在单步前把“Lua 能力可用”变成显式检查；一旦能力被关闭，只能到调用时以 `capability_disabled` 兜底（仍然安全，但诊断更晚）。

**建议修订：** 在 `validate_tool_contract` 之前的 runtime 校验里断言 `gates.unsafeLua === true`（失败按合同失败处理、退出不单步），或将此检查写入计划说明并保留 `capability_disabled` 兜底路径。

### S10 — 预检批量读取失败判定与单步后读取语义未定义

**优先级：P3。属性：缺漏（实现细节与报告语义）。**

**定位：** L195（“读取失败则退出且不单步”）、L201（“动态读取 `[RSP+0x50]`、`[RSP+0x330]`、`[R14+0x1D58]`、`[R14+0x1D5C]`”）。

**问题 1（失败判定）：** `memory_read_batch` 的合同是“逐个地址带内报错、其余照常读取”，顶层成功不代表全部成功；计划未说明如何判定失败，实现者可能只看顶层结果而漏掉单条错误。
**问题 2（读取语义）：** 单步后停在下一条指令 `+11FD5D0: mov [rsp+50],eax`（尚未执行）。实测：`[RSP+0x50]=130` 是旧值（本次单步**不会**改变它）、`[RSP+0x330]=126` 是此前 `+11FD5C2` 已写入的值、`[R14+0x1D58]=[R14+0x1D5C]=126`。若报告不注释语义，读者可能把 `[RSP+0x50]` 误解为“已被写入 126”。

**建议修订：** 预检读取必须检查 `failed==0` 且每个 item 无错误载荷，任一失败 → 退出不单步（补测试）；报告中为每条读取标注含义与预期关系（例如“单步后 RAX 与单步后重读的 `[R14+0x1D58]` 对照；本现场两字段同为 126，数值本身不具区分力，按 goal3 说明记录”），并明确 `[RSP+0x50]` 在本次单步后仍应保持旧值。

## 四、不可修复破坏风险专章（用户问题 1 的完整矩阵）

判定依据 = 计划允许调用集合（L33-43）× 该调用是否可能写内存/改 CE 状态 × 失败时的行为。

| 失败/路径 | 触达 CE 的调用 | 是否可能残留或破坏 | 依据 |
| --- | --- | --- | --- |
| CLI 参数、网关文件、输出目录等在启动前失败 | 无 | 否 | 启动前校验，未创建子进程 |
| 网关启动失败或被中断 | 无工具调用 | 否 | `McpClient.start` 对 `BaseException` 先回收子进程（ce_mcp_client.py:57-63） |
| 合同校验、实例、runtime、状态、上下文、断点、内存读取任一失败 | 仅查询工具（含固定 Lua） | 否 | 全部查询工具 `readOnlyHint=true`；固定 Lua 逐行只读；本轮实测此类调用前后 `resourceCount/jobCount 0→0`、`process` 一致 |
| 起始 RIP/THREADID/位宽不符合 | 无新增调用 | 否 | 单步前退出路径 |
| `debugger_step` 下发 | CE 核心 `debug_continueFromBreakpoint(co_stepinto/over)` | 与用户按 F7/F8 完全同路径；MCP 插件不注册 job/资源、不承担 TF/断点清理 | 插件源码 `DebuggerTools.Step` + `DebuggerLuaScripts.Step`；CE 源码 `debug_continueFromBreakpoint` 绑定 |
| 单步已下发后传输断开 / Gateway 被终止 | 无新增调用 | 否（脚本层面） | 单步是同步 Lua 下发；关闭 Gateway 只回收 Python 子进程，不参与 CE 核心的单步收尾；插件不为单步注册 job，没有可被取消的清理对象 |
| 单步后观测失败 / 超时 / 状态未知 | 仅查询工具 | 否 | 计划 L17-18、L198；本次未实测该场景（不单步），属源码+合同证据 |
| 用户断点相关 | 仅 `debugger_list_breakpoints` 读取 | 否 | 只读注解；不调用 set/delete；变化只报告 |
| 用户中断（任意阶段） | 无恢复型调用 | 否 | `finally` 只关网关与落盘报告 |
| 理论外部风险 | CE 核心在步进中处理断点/TF 自身异常 | 与本方案无关、与人工单步同源 | 无法由本脚本排除；计划 L242 已声明人工确认 |

**两个需要留意的现场特征（非破坏，但应在报告中解释）：**

1. 当前断点列表中 `3A484D9F8B8`、`3A484D9F8BC` 恰为 `R14+0x1D58/0x1D5C` 的数据断点。单步执行 `mov eax,[r14+1D58]` 会读取被监视字段；若为访问型硬件断点，CPU 在指令执行后上报数据断点，CE 就此停止（RIP 仍应为 D0）。这不构成破坏，但停止“原因”与单纯单步不同，报告应保留断点快照以解释来源。
2. 计划 L242 的“不保证底层 MCP/CE 必然完成临时单步断点清理”可以按源码事实更新为更强的结论：**插件对单步没有任何清理责任**（无 job、无资源注册），步进收尾完全由 CE 核心负责；Gateway 关闭与此无关。这能减少用户对“关掉 Gateway 会不会留下残留单步断点”的担忧，也让“单步后不恢复”的取舍更有据可依。

**证据边界（必须明确）：** 单步本身属边界动作，本审查**没有**、也不应该实际执行；以上“单步路径”结论来自 tools/list 合同、插件/CE 源码核对与同现场生产报告证据，最终应由任务 3 的真实验收确认。验收时建议人工核对：目标仍停止、RIP 到达 `+11FD5D0`、3 条断点仍在（无增删）、`resourceCount/jobCount` 前后一致。

## 五、验证记录与证据

### 5.1 本轮实际执行的探测（全部只读；产物在 `Output/mcp_step_review1_20261002/`）

| 检查 | 结果 |
| --- | --- |
| tools/list 全目录 | 191 项；计划涉及工具全部存在（缺失集合为空） |
| 目标工具 annotations | 查询工具全部 `readOnlyHint=true/destructiveHint=false`；`debugger_step`、`debugger_continue` 为 `readOnly=false/destructive=false`；`lua_execute` 为 `destructive=true`、`may_prompt`、`requires=["unsafe_lua"]` |
| `debugger_step` schema | `instanceId` 必填；`mode` 枚举 `into/over`、默认 `into`；输出 `{mode, continued}` |
| 当前现场 | `instance_list` 1 个实例（CE 72480）；overview：victoria3 PID 43884、pointerSize 8、epoch 1、selectionEpoch 0 |
| `debugger_get_status` | 已知软错误：`stateValid=false` + `debug_isBroken did not return a boolean debugger state`（已停止现场亦同） |
| `debugger_get_context` | 成功；RIP=`7FF777CED5C9`、RSP=`8C5DE8D870`、R14=`3A484D9DB60`、THREADID=`60D0` |
| `debugger_list_breakpoints` | 3 条，均 `owned=false`；`truncated=false` |
| `module_get` | base=`7FF776AF0000`、`pe.timeDateStamp=6A3BF239`；偏移核对 `11FD5C9` 吻合 |
| `code_decode`/`code_disassemble` | C9=`mov eax,[r14+1D58]`（`418B86581D0000`，len 7）；D0=`mov [rsp+50],eax` |
| `memory_read_batch` | `R14+1D58=126`、`R14+1D5C=126`、`[RSP+50]=130`、`[RSP+330]=126`；`failed=0` |
| 残留对照 | `resourceCount 0→0`、`jobCount 0→0`、`epoch 1→1`、`process` 一致 |
| 插件源码核对 | `DebuggerTools.Step`→`DebuggerLuaScripts.Step`：`debug_continueFromBreakpoint` + 立即返回；无 job/资源注册 |
| 离线测试 | `test_stacktrace_register` 32 项通过；`discover` 60 项全部通过 |
| `debugger_step`/`continue`/写类调用 | **未执行**（审查不触碰边界动作） |

以上探测未附加/分离调试器、未设置/删除/移动断点、未继续目标、未写目标内存、未调用任何写类工具；期间目标现场保持停止在 `RIP=7FF777CED5C9`。

### 5.2 产物清单

```text
Output/mcp_step_review1_20261002/inspect.py            只读探测脚本
Output/mcp_step_review1_20261002/tools_subset.json     工具合同快照（与计划有关子集）
Output/mcp_step_review1_20261002/*.json                各次探测响应与 calls/residue 记录
Output/mcp_step_review1_20261002/discover.log          60 项离线测试输出
```

## 六、审查快照（SHA-256）

```text
Docs/superpowers/plans/2026-10-02-debugger-step-compatible-capture.md
e0184e2f826f0a42e9ed373b747c25cb812db4361feb2fcf6d7b73bab410ac26

Docs/goal3.md
f76e1820f1a0b8bbc79b12894f323163eae40b3d3fa8246863ee160a966099bd

Docs/goal3_analysis_plan.md
16aa8068b74880b0b8889e13e9b047240298a7e846c2882618644e35950d22bd

Docs/goal3_static_disassembly4.md
4c70171d90affb9a364ebac2ced9dba2b199275b7f8fe26c6049474d73249247

Scripts/get_stacktrace_register_at_breakpoint.py
03725ef284f675b5c6e1d83dca03259d8cd35fb3164d43a3774b9b8f45ce1362

Scripts/ce_mcp_client.py
34879b4bc4bde4b15b8ef88f94358946b7b3e7717883a4c4a8adf87ce7a9aa29

Scripts/opcode_report.py
16abe8a55cb8b2d57794f101dc6f262eef60714db58c9bbfbcfae512b607f62e

Output/mcp_step_review1_20261002/tools_subset.json
826f17d10a34efa41f2c93075151b4cc0321bf56cc660f3aaeb0de88e7ec161e
```

## 七、建议修订顺序

1. **先修 S1 + S2（P2，实施前必须）**：把 `module_get` 加入允许接口与合同校验、用 `base` 计算两个预期 RIP 并记录构建指纹；把 v1 语义写死为“恰好一次单步”，清除多步措辞与 L29 的歧义句。
2. **再修 S3 + S4**：确定 `stepIssued` 的保守置位规则；补“报告字段与退出码表”（含 `postStepState=unknown` 的退出码），并同步任务 2 的断言。
3. **补 S5 + S6 + S9**：断点列表比较字段与说明；轮询绑定固定兼容状态查询并给出间隔/时限；把 `gates.unsafeLua` 纳入前置检查。
4. **小修 S7 + S8 + S10**：删除或说明 RDI/RSI；更正禁用工具名并让 deny 断言覆盖实际存在的写类工具；补批量读取失败判定与单步后读取语义注释。
5. 全部修订完成后，按任务 3 执行真实验收：验收前先做一次只读预检（工具目录 + 现场 + 模块指纹），单步后由用户人工确认 CE 状态，再归档报告。

以上修订均不涉及新增写类工具、不扩大脚本权限；S1 新增的 `module_get` 为只读且不创建 job，不需要修改 `ce_mcp_client.py` / `get_stacktrace_register_at_breakpoint.py` 的现有职责。
