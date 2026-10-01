# 断点 Stacktrace 与寄存器采集计划审查报告 1

- **审查日期：** 2026-10-01
- **审查对象：** `Docs/superpowers/plans/2026-10-01-stacktrace-register-breakpoint.md`（SHA-256 `911ccfda…c309`，见第五节快照）。
- **需求依据：** `Docs/goal2.md`（SHA-256 `ea56ab21…c793`）。
- **审查重点（用户指定）：** 1）是否在所有失败条件下都不会对内存造成残留修改；2）方案整体是否合理、MCP 能力能否支持。
- **审查方式：** 静态对照计划与现有源码；实际启动 `CheatEngine.Mcp.Gateway.exe` 做只读探测（tools/list 全目录、六个目标工具的 inputSchema/outputSchema/annotations、错误语义、失败调用前后残留对照）；提取 Gateway 二进制中的错误类型词表；运行现有 unittest。全程未附加调试器、未设置或删除断点、未继续目标、未读写目标内存、未调用任何写类工具。
- **修改范围：** 本轮只新增本报告；未修改被审查计划、`Docs/goal2.md`、任何源码或测试。

本文行号以本次审查快照为准。

## 一、结论

**方案整体合理，MCP 能力逐项支持；核心安全目标（任何失败都不残留内存修改）在脚本设计层面成立，但计划还缺少把它变成可验证证据的两块拼图，另有若干合同细节与实现约定需要修订。**

对用户两个问题的直接回答：

1. **残留修改：不会。** 脚本没有任何可写 CE 的代码路径：白名单只有 6 个只读调用，收尾阶段不为了"清理"调用 continue/pause/detach，文件写入走原子替换且失败时清理临时文件。CE 侧"只读"由网关合同保证，本轮已取得三重证据：读工具 `readOnlyHint=true`/`idempotentHint=true`、写类工具独立存在且 `readOnlyHint=false`、多次失败调用前后 `resourceCount/jobCount`、附加状态与进程身份完全一致（详见第四节）。残留风险只剩"网关实现偏离合同"这一外部假设。
2. **MCP 能力：完全支持。** `instance_list`、`runtime_get_info`、`runtime_get_overview`、`debugger_get_status`、`debugger_get_context`、`debugger_get_stack_trace` 六个工具在实测 tools/list（共 191 项）中全部存在；`includeExtraRegisters`、`depth=128`、RIP/EIP、寄存器字符串映射、stacktrace 的 `stackAddress/returnAddress/callInstruction/isHeuristic/scannedSlots` 字段与报告设计逐条对上（详见第二节）。

需要修订的问题共 8 项，其中 4 项 P2（应在实施前修正）：

| 编号 | 问题 | 属性 | 主要影响 |
| --- | --- | --- | --- |
| R1 | ToolError 分类与退出码在计划内自相矛盾，且未覆盖实测错误类型词表 | P2 | 实现与测试无法确定"工具错误→2 还是 3" |
| R2 | 缺少"无副作用"证据链：未利用 `hostEffect`，也没有采集前后残留计数核对 | P2 | "失败不留残留"只能靠声明，无法被验收 |
| R3 | 字段校验清单与真实 outputSchema 不一致，可能把契约允许的可选字段当错误拒绝 | P2 | 合法响应被误判为结构错误，退出码 2 |
| R4 | 采集后无会话/进程指纹复核，报告元数据可能与上下文不同源 | P2 | 报告中进程信息与实际寄存器/栈帧错配 |
| R5 | 缺少运行时工具目录与 schema 校验（现有脚本有先例） | P3 | 网关版本漂移要到采集期才暴露 |
| R6 | 退出码约定未覆盖输出侧失败（目录不可建、写文件失败） | P3 | 失败路径存在未定义行为 |
| R7 | `streg_gateway.stderr.log` 固定文件名 + `"w"` 模式，并发运行互相覆盖 | P3 | 诊断日志被截断；报告覆盖语义未对称声明 |
| R8 | 渲染层转义不满足计划自身的"控制字符"要求；"断点地址"语义需说明 | P3 | 表格可能被控制字符破坏；用户可能误读文件名 |

"手动停在断点后再采集""不自动 attach/continue""stacktrace 是启发式候选"三个设计选择与 goal2 和网关合同一致，作为有意设计接受，不列为缺陷。

## 二、已确认可被 MCP 支持的部分（逐条实测证据）

1. **六个工具存在且注解符合只读定位。** 实测 tools/list：`debugger_get_status`、`debugger_get_context`、`debugger_get_stack_trace` 的 annotations 均为 `readOnlyHint=true, idempotentHint=true, destructiveHint=false`；`debugger_attach/continue/step/set_register/set_breakpoint/delete_breakpoint/run_to/...` 等写类工具独立存在且 `readOnlyHint=false`。计划只调用前一类，合同成立。
2. **`includeExtraRegisters=true` 可传。** schema：`boolean, default false`；描述确认 CE 提供时返回 FP0-FP7（10 字节）与 XMM0-XMM15（32 位目标为 XMM0-XMM7），以空格分隔十六进制字节、内存序（低字节在前）返回——与计划 L13、L57 的 little-endian 说明和"缺失不猜测"处理一致。
3. **`depth=128` 合法。** schema：`1 through 128, default 32`；实测 `depth=0/129` 被服务端以 `invalid_argument`（`hostEffect=not_started`，`details.parameter=depth`）拒绝，不会触达 CE。
4. **status 的 `broken` 语义与计划的 `require_stopped` 判断一致。** outputSchema 必填 `stateValid/attached/canBreak/broken/reportedBroken/stepping`，附加 `activeInterface`（enum default/windows/veh/kernel）与 `error`；工具描述明确"broken 通过获取上下文证明，比 reportedBroken 更可靠"。计划要求 `stateValid && attached && broken` 为真、拒绝 host error，与合同完全一致。实测未附加时返回**软错误**：`isError=false`，载荷 `{stateValid:false, attached:false, ..., error:"..."}`——计划按字段判断而不是只按调用是否抛异常，处理方式正确。
5. **context 字段与计划校验一致。** 必填 `is64Bit/registers/includesExtraRegisters`；`registers` 为大写寄存器名到字符串的映射（整型寄存器为无 0x 大写十六进制）。计划"从 RIP 或 EIP 取地址、校验 is64Bit 与寄存器宽度一致、寄存器必须是字符串映射"可实现。
6. **stacktrace 字段与报告设计一致。** 必填 `stackPointer/pointerSize/frames/scannedSlots`；frame 必填 `stackAddress/returnAddress`，`callInstruction` 仅在 CE 能反汇编时出现，`isHeuristic` 默认 true。计划"序号、stack slot 地址、return address、call instruction、isHeuristic"五列与"空 frame 也要写 scannedSlots 数量"逐项对上；"启发式候选、不等于符号化调用栈"的表述与该工具标题（Get heuristic stack trace）和描述一致。
7. **错误语义已实测，hostEffect 可区分"未开始/已开始"。** 未停止时 `debugger_get_context/get_stack_trace` 返回硬错误 `ToolError{kind:"host_refused", operation:"Lua.Execute", hostEffect:"started", message:"Debugger has no stopped context"}`；参数越界则是 `invalid_argument + hostEffect:"not_started"`。即失败时能证明"主机操作未开始或只是只读执行被拒"。
8. **会话指纹字段齐备。** 实测 overview 含 `runtime.epoch`、`process.{isOpen, processId, processName, pointerSize, selectionEpoch}`、`resourceCount/jobCount`（当前 0/0），与现有 `run_opcode_export.check_session`（run_opcode_export.py:122-127）用法一致，可直接复用到 R4 的建议中。
9. **退出码 0/130 与资源回收路径成立。** `McpClient.start` 对 `BaseException`（含 KeyboardInterrupt）先回收本次子进程再抛出（ce_mcp_client.py:57-63）；计划 main 的 try/finally 关闭客户端；任务 2 步骤 6 明确"不为清理调用继续、暂停或 detach"，与"失败不留状态修改"目标一致。
10. **文件写入安全。** `atomic_text` 临时文件在 finally 中 `unlink(missing_ok=True)`（opcode_report.py:120-135），中断/失败不会留下半截报告；重复运行同地址覆盖的语义与既有导出流程的原子替换一致。
11. **测试命令与仓库惯例一致。** 实测 `python -m unittest Scripts/tests/test_ce_mcp_client.py Scripts/tests/test_opcode_report.py -v` 与 `python -m unittest discover -s Scripts/tests -p "test_*.py"` 在当前工作树 28 项全部通过，计划任务 4 的命令形式可用；任务 2 的假客户端模式与 test_opcode_export.py 的 FakeMcp 模式一致。
12. **需求对齐。** goal2 的三项要求（断点 stacktrace、所有寄存器、`Output/streg_<断点地址>.md`）在计划中有逐项落点；"用户手动停在断点"的前置条件与 README"插件不会自动附加"一致。

## 三、逐项问题

### R1 — ToolError 分类与退出码在计划内自相矛盾，且未覆盖实测错误类型词表

**优先级：P2。属性：计划内部一致性。**

**定位：**

- 计划 L18：退出码约定"参数、实例、未停止状态、响应结构错误或**工具错误为 2**；MCP 传输失败或**会话在采集期间失效为 3**"。
- 计划 L79（任务 2 步骤 5）："覆盖 TransportError、**ToolError**、响应 JSON 解析错误和第二次状态检查发现已继续运行；断言退出码为 **3**"。

**问题：**

同一份计划对 ToolError 给出两种退出码（2 与 3），测试断言无法同时成立。根本原因是"工具错误"不是单一类别：实测网关错误 kind 至少 15 种（从 Gateway 二进制提取的词表：`invalid_argument / invalid_state / not_found / not_attached / cancelled / capability_disabled / unsupported / target_changed / host_refused / memory_read_failed / memory_write_failed / limit_exceeded / partial_effect / stopping / instance_unavailable`，另有 `busy/timeout` 字样）。其中：

- `host_refused` 同时覆盖"前置条件不满足"（require_stopped 应当先拦住）和"采集期间停止上下文丢失"（计划语义是 3）两种场景，仅凭 kind 无法区分，需要结合发生阶段判断；
- `invalid_argument` 是参数/合同错误（2）；
- `not_attached / invalid_state / target_changed / stopping / instance_unavailable` 是会话失效（3）；
- 现有先例 run_opcode_export.py 只把 `{target_changed, not_attached, stopping, invalid_state}` 视为会话错误，新脚本不扩展该表就无法覆盖调试器场景。

**实测证据：**

```text
debugger_get_context（未停止）→ ToolError kind=host_refused, hostEffect=started, "Debugger has no stopped context"
debugger_get_stack_trace（depth=129）→ ToolError kind=invalid_argument, hostEffect=not_started, details.parameter=depth
```

**建议修订：**

- 在全局约束中给出显式映射表，并修正 L79 的表述（例如"会话类 ToolError → 3，其余 ToolError → 2"）。建议：

| kind | 归类 | 退出码 |
| --- | --- | --- |
| invalid_argument / capability_disabled / unsupported / not_found | 参数或合同 | 2 |
| not_attached / invalid_state / target_changed / stopping / instance_unavailable / cancelled | 会话失效 | 3 |
| host_refused | 按发生阶段：require_stopped 前置检查 → 2；采集调用中（上下文/栈帧/二次状态）→ 3 | 2 或 3 |
| 白名单只读工具出现 memory_*_failed / partial_effect / limit_exceeded | 不应出现，视为状态未确认 | 3 + 英文告警 |
| 其他未列出的 kind | 保守默认 | 3 |

- 测试对每个归类至少一个用例，并断言 stderr 里的英文诊断包含 kind。

### R2 — 缺少"无副作用"证据链：未利用 hostEffect，也没有采集前后残留计数核对

**优先级：P2。属性：本次新增（用户核心关切未被自动验证覆盖）。**

**定位：**

- 计划 L48（capture_snapshot 校验响应结构）、L51（只写诊断日志）、L53-60（报告格式）、L112（任务 4 步骤 6 靠人工确认"未产生内存写入"）。

**问题：**

计划反复声明只读（L4、L10、L62），但全部依赖网关合同，没有把"无残留"做成自动证据：

1. 错误载荷里的 `hostEffect`（词表：`not_started / not_applied / started / completed / cleanup_unconfirmed / unknown`）直接描述主机侧效果，本可用于断言"只读调用失败时未生效"，计划完全未使用。
2. `runtime_get_overview` 提供 `resourceCount/jobCount`，`run_opcode_export.check_residue`（run_opcode_export.py:129-165）已有"采集前后计数一致"的先例；新脚本一次 overview 调用即可做同样对比，且不需要扩展工具白名单。目前计划连这个零成本证据也没有。

**建议修订：**

- 错误诊断（stderr 的英文消息 + 任务 4 的人工核对项）记录 `error.kind` 与 `error.hostEffect`；对白名单只读工具的失败断言 `hostEffect ∈ {not_started, started}`，出现 `not_applied / completed / cleanup_unconfirmed / unknown` 时按"CE 状态未确认"处理（建议退出码 3 + 明确告警），不得静默按普通失败处理。
- 在 validate_runtime 记录 `resourceCount/jobCount` 基线，采集结束后（与 R4 的指纹复核合并为同一次 overview 调用）对比计数；结果写入报告元数据（如 `residueCheck: unchanged/changed/unavailable`）。这是本项目"只读"承诺目前唯一可自动化的直接证据。
- 注意任务 2 步骤 2 的调用顺序断言需同步更新（末尾增加一次 overview）。

### R3 — 字段校验清单与真实 outputSchema 不一致，可能拒绝契约允许的合法响应

**优先级：P2。属性：合同理解歧义。**

**定位：**

- 计划 L48："上下文和 stacktrace 任一响应缺少必需字段、寄存器不是字符串映射、frame 字段类型错误或 scannedSlots 越界，都拒绝写文件。"
- 计划 L77："覆盖 32 位 EIP 路径、RIP 缺失、RIP 非法、is64Bit 与寄存器不一致、**额外寄存器字段为空或类型错误**、**stack frame 缺字段**、depth/scannedSlots 越界；每个场景均为退出码 2 且不生成报告。"
- 计划 L57-58（报告字段）。

**问题：**

真实 outputSchema 中，下列情况是**合法**的，按 L77 字面实现会误报退出码 2：

- context：FP0-FP7/XMM 只在 Cheat Engine 提供时出现（契约原文 "they appear in registers only where Cheat Engine supplied them"）——"额外寄存器为空"不能视为错误；应校验的是 echo 字段 `includesExtraRegisters=true`（因为请求了 true）以及所有已出现值均为字符串。
- stacktrace：frame 的必填字段只有 `stackAddress/returnAddress`；`callInstruction` 仅在"CE 能反汇编"时出现，`isHeuristic` 有默认 true——"stack frame 缺字段"需要按可选字段排除后再判定。
- `activeInterface` 在停止上下文下按合同应存在，但 schema 允许其为 null；报告渲染应对 null 容错（打印 unavailable），而不是崩溃或拒绝。

另外两处建议明确的细节：64 位与 32 位下 RIP/EIP 的取用优先级（64 位应取 RIP、忽略 EIP；32 位取 EIP；两者都缺才拒绝）；`status.stepping` 是否纳入报告元数据（合同字段存在，单步停下的现场值得记录）。

**建议修订：**

- 在计划中用一张"必填/可选字段清单"替换文字描述：context 必填 `[is64Bit, registers, includesExtraRegisters]`（echo 必须为 true、值全为字符串）；stacktrace 必填 `[stackPointer, pointerSize, frames, scannedSlots]`，frame 必填 `[stackAddress, returnAddress]`，`callInstruction/isHeuristic` 为可选项（存在时校验类型）；`activeInterface=null` 渲染为 unavailable。
- 任务 2 步骤 3 的用例改为"必填字段缺失 → 2；可选字段缺失 → 正常出报告"两类，避免把契约允许的响应练成失败路径。

### R4 — 采集后无会话/进程指纹复核，报告元数据可能与上下文不同源

**优先级：P2。属性：报告一致性。**

**定位：**

- 计划 L45（validate_runtime 记录进程身份与会话标识）、L48（调用顺序"状态 → 上下文 → stacktrace → 状态"）、L79（最后只核对"仍是 stopped"）。

**问题：**

现有 `run_opcode_export.check_session` 在导出前、每个目标前后复核 `runtimeEpoch/processId/selectionEpoch/pointerSize`（run_opcode_export.py:63-75、122-127）；新计划只在最后复核"仍在停止"。若用户在采集窗口内 detach 后对**另一个进程** attach 并断下，第二次状态检查仍满足 `broken=true`，脚本会把进程 A 的元数据与进程 B 的寄存器/RIP/栈帧拼进同一份报告——报告内部数据来自 B，元数据却声明 A，两者不同源且无法从报告本身察觉。

**实测证据：** overview 指纹字段齐备：`runtime.epoch`、`process.isOpen/processId/processName/pointerSize/selectionEpoch`（当前 `{"processId":43884,"processName":"victoria3","pointerSize":8,"selectionEpoch":0}`）。

**建议修订：**

- 把 R2 建议的收尾 overview 同时用于指纹复核：`runtime.epoch + processId + selectionEpoch + pointerSize` 与采集前基线不一致 → 退出码 3、不写报告。
- 测试增加"采集中进程选择变化（selectionEpoch/processId 改变）"用例，断言退出码 3 且无报告。

### R5 — 缺少运行时工具目录与 schema 校验（有现成先例）

**优先级：P3。属性：健壮性。**

**定位：** 计划 L37（MCP 输入约定）、任务 1 步骤 1（只定义白名单）。

**问题：** `run_opcode_export.main` 在使用前校验每个必需工具存在且 `inputSchema.properties` 覆盖所需参数（run_opcode_export.py:273-279）；新计划没有对应步骤。若网关升级后 `includeExtraRegisters` 改名或 `depth` 被移除，脚本会在采集期以"响应结构错误"（2）甚至被静默忽略参数的形式暴露，不如启动时失败清晰。

**建议修订：** 增加启动期 catalog 校验（`tools/list` 不属于工具调用白名单约束，不违反 L12）：六个工具必须存在，`debugger_get_context` 必须含 `includeExtraRegisters`、`debugger_get_stack_trace` 必须含 `depth`；失败 → 退出码 2。测试覆盖工具缺失与 schema 漂移两类用例。

### R6 — 退出码约定未覆盖输出侧失败

**优先级：P3。属性：约定完整性。**

**定位：** 计划 L18（退出码）、L81（任务 2 步骤 7 原子写失败）。

**问题：** 约定覆盖了参数/实例/未停止/结构/工具/传输/中断，但没有"输出目录不可创建、报告写入失败（OSError）"的归类；步骤 7 也只断言"临时文件被清理且不留伪成功文件"，未断言退出码。

**建议修订：** 明确 OSError → 2（与 run_opcode_export 现有行为一致），stderr 输出英文原因；步骤 7 补充退出码断言。

### R7 — `streg_gateway.stderr.log` 固定文件名 + `"w"` 模式，并发运行互相覆盖

**优先级：P3。属性：运行约定。**

**定位：** 计划 L51、L9（默认输出目录）。

**问题：** `McpClient` 以 `"w"` 打开日志（ce_mcp_client.py:40）；同一输出目录两次并发采集会截断彼此的诊断日志。报告同地址覆盖是有意设计（L82 已声明），日志覆盖没有对称声明。

**建议修订：** 文档写明"同一输出目录同一时间只运行一个采集实例"，或在日志名加入进程号/时间戳；保留"日志仅用于诊断"的说明。

### R8 — 渲染层转义不满足计划自身要求；"断点地址"语义需说明

**优先级：P3。属性：渲染与文档。**

**定位：** 计划 L16（"Markdown 单元格中的 |、换行和**控制字符**必须转义或替换"，并复用 opcode_report 小工具）、L15/L55（`streg_<断点地址>`）。

**问题：**

1. `md()` 只替换 `\r`、`\n` 并转义 `|`（opcode_report.py:85-87），不覆盖其他控制字符；直接复用 `md()` 不能满足 L16 对"控制字符"的要求，需要在渲染层加一个窄清洗（例如过滤 C0/C1 控制符）并补测试用例。
2. RIP/EIP 是"当前停止地址"，并不等于 CE 断点列表中登记的地址（单步、异常停下的场景也会产生停止上下文）；文件名与标题使用"断点地址"可能被误读。建议在文档与报告 Capture Contract 中一句话说明该定义（脚本有意不调用 `debugger_list_breakpoints`，属可接受设计）。

**建议修订：** 渲染层增加清洗函数（新增在 `get_stacktrace_register_at_breakpoint.py` 内，不改 `opcode_report.py` 的职责边界），测试注入含 `\x00/\x1b/|` 的值；文档补充地址语义说明。

## 四、残留修改风险专章（用户问题 1 的完整矩阵）

判定依据 = 脚本调用集合（L12 白名单）× 该调用是否可能写内存/改 CE 状态 × 失败时的清理行为。

| 失败场景 | 触达 CE 的调用 | 是否可能残留修改 | 依据 |
| --- | --- | --- | --- |
| CLI 参数非法 / 网关文件不存在 | 无 | 否 | 启动前校验，未创建进程 |
| 网关启动、握手失败或被 Ctrl+C | 无工具调用 | 否 | McpClient.start 对 BaseException 自清理（ce_mcp_client.py:57-63） |
| 实例发现失败 / 多实例未指定 ID | instance_list | 否 | 本地发现接口 |
| runtime 读取失败 | runtime_get_info / runtime_get_overview | 否 | 两者 readOnlyHint=true；实测调用后进程身份不变 |
| 未附加 / 未停止 / 状态无效 | debugger_get_status | 否 | readOnlyHint=true；实测软错误、`attached` 保持 false |
| 上下文 / stacktrace 调用失败 | debugger_get_context / debugger_get_stack_trace | 否 | readOnlyHint=true；实测失败调用前后 `resourceCount/jobCount` 0→0、`process` 完全一致 |
| 采集中传输超时 / 网关崩溃 | 至多一个在途只读请求 | 否（合同） | 白名单无写工具；客户端 broken 后不再发请求并回收进程 |
| 第二次状态检查发现目标已继续 | debugger_get_status | 否 | 只读；脚本不负责也不需要重新暂停 |
| 用户中断（任意阶段） | 无清理型 CE 调用 | 否 | try/finally 只 close 自己的网关；任务 2 步骤 6 断言不调用 continue/pause/detach |
| 响应结构校验失败 / 重复运行 / 写文件失败 | 无新增调用 | 否 | 校验发生在写文件前；atomic_text 失败清理临时文件 |

**结论：** 全部失败路径都不包含写内存、改寄存器、增删断点、附加/分离调试器、继续目标这五类操作；唯一的文件系统副产物是 `Output/streg_gateway.stderr.log`（计划已声明仅诊断用途）和成功时的报告文件本身。

**证据边界（必须明确）：** 本次实测覆盖"调试器未附加"状态下的失败路径与残留对照；"**已附加且已停止**"状态下的真实只读性无法在不占用用户现场的情况下离线证明，它依赖上述注解合同，并应由任务 4 步骤 6 的人工核对最终确认——计划已含该步骤，建议按 R2 再补一条自动的计数/`hostEffect` 证据，使人工核对只需确认目标仍停在原断点、断点列表无增删。

## 五、验证记录与证据

### 5.1 本轮实际执行的探测

| 检查 | 结果 |
| --- | --- |
| tools/list 全目录 | 191 个工具；六个目标工具全部存在 |
| debugger 读工具 annotations | `get_status/get_context/get_stack_trace` 均 `readOnlyHint=true, idempotentHint=true` |
| 三工具 outputSchema | 字段与必填项已逐条记录（第二节） |
| `includeExtraRegisters` / `depth=128` | schema 接受；`depth=0/129 → invalid_argument, hostEffect=not_started` |
| `debugger_get_status`（未附加） | 软错误 `isError=false`，`stateValid=false` 且含 `error` 文本 |
| `debugger_get_context/get_stack_trace`（未停止） | 硬错误 `host_refused, operation=Lua.Execute, hostEffect=started` |
| 失败调用残留对照 | 前后 `resourceCount/jobCount` 0→0；`attached` 保持 false；`process` 对象完全相同 |
| Gateway 二进制错误词表 | kind 15 种 + hostEffect 6 种（R1/R2 引用） |
| 插件日志（`%APPDATA%\CheatEngine.Mcp\CheatEngine.Mcp.72480.log`） | 各次探测的 IsError 标记与客户端观察一致 |
| 现有测试 | `discover` 28 项全部通过；计划任务 4 的命令形式可用 |
| 真实断点采集 | **未执行**（需用户手动现场；不作为本轮前提） |

所有探测均为只读；未附加调试器、未设置/删除断点、未继续目标、未读写目标内存数据、未调用任何写类或状态改变工具。

### 5.2 审查快照（SHA-256）

```text
Docs/superpowers/plans/2026-10-01-stacktrace-register-breakpoint.md
911ccfda8e4371f18c60cd2b41d0d261d7cba6802be3181cc1dacd28c412c309

Docs/goal2.md
ea56ab21cb7dafdae951f75c04935104f17f775120616b15cfe06f2f97f9c793

Scripts/ce_mcp_client.py
34879b4bc4bde4b15b8ef88f94358946b7b3e7717883a4c4a8adf87ce7a9aa29

Scripts/opcode_report.py
ec986ff5e1fcc1759baacd7cb0f5c8474a954cd72f2c9296c39a11254dde08e0
```

## 六、建议修订顺序

1. **先修 R1**：统一 L18 与 L79 的退出码语义，写出 kind 映射表；这是实现与测试的前置。
2. **再修 R3**：用必填/可选字段清单替换文字描述，防止把合法响应练成失败路径。
3. **合并实施 R4 + R2**：在采集收尾增加一次 `runtime_get_overview`（指纹复核 + 残留计数）、在错误诊断中记录 `kind/hostEffect` 并断言白名单只读工具的 `hostEffect` 集合；同步更新任务 1 步骤 7、任务 2 的顺序断言与验收项。
4. **小修 R5/R6/R7/R8**：catalog 校验、OSError→2、日志命名约定、渲染清洗与地址语义说明。
5. 全部修订完成后，再按任务 4 执行一次真实手动断点验收；验收时额外核对"停止前后 `resourceCount/jobCount` 一致"与"目标仍停在原断点"。

以上修订均不涉及新工具、不扩大脚本权限，也不需要修改 `ce_mcp_client.py` / `opcode_report.py` 的现有职责。
