# 断点 Stacktrace 与寄存器采集 实施方案
> 面向自动化执行人员：必须配套使用 superpowers:executing-plans 逐任务执行本方案。步骤使用复选框（- [ ]）用于进度跟踪。
**目标：** 在用户已手动让 Cheat Engine 停在断点的前提下，通过现有 MCP Gateway 读取当前断点地址、完整寄存器集合和当前停顿上下文的 stacktrace，并生成 Output/streg_<断点地址>.md。
**架构方案：** 新脚本复用 Scripts/ce_mcp_client.py 的 stdio MCP 传输，只调用实例发现、运行时健康检查和调试器只读工具；不附加进程、不创建或删除断点、不继续运行目标、不修改目标内存。采集结果先在内存中完成结构校验，再通过原子文本替换写入单个 Markdown 文件。
**技术栈：** Python 3 标准库、现有 McpClient、CheatEngine.Mcp 2.0.0-beta.2 Gateway、debugger_get_status、debugger_get_context、debugger_get_stack_trace。

## 全局约束

- 脚本从项目根目录执行时默认使用 McpExternals/CheatEngine.Mcp-2.0.0-beta.2-win-x64/CheatEngine.Mcp.Gateway.exe，默认输出目录为项目根目录 Output。
- 用户必须在运行脚本前手动附加目标进程并使 CE 停在断点；脚本发现未附加、未停止或上下文不可读时失败，不改变 CE 状态。
- 除 instance_list 外的 MCP 调用都必须带本次发现的 instanceId；实例不唯一时要求 --instance-id，不得猜选。
- 允许调用的业务工具固定为 instance_list、runtime_get_info、runtime_get_overview、debugger_get_status、debugger_get_context、debugger_get_stack_trace；启动期允许额外调用一次 tools/list 做目录/schema 校验，测试必须断言业务调用集合不超出该集合。
- debugger_get_context 必须传 includeExtraRegisters=true，以尽可能包含 FP0-FP7 与 XMM0-XMM15；报告保留 MCP 返回的寄存器键和值，不自行推导缺失寄存器。
- debugger_get_stack_trace 的 depth 传 128（接口允许的最大值）；报告明确说明 frame 是启发式候选，不能把它表述为经过符号器确认的调用栈。
- 断点地址从当前上下文的 RIP（64 位）或 EIP（32 位）读取，并规范化为无 0x、大写十六进制文本；该值实际表示当前停止上下文的指令地址，不保证是断点列表登记地址；文件名只允许该规范化地址，禁止把任意响应文本拼接到路径。
- 报告使用 UTF-8、LF 换行，Markdown 单元格中的 |、换行和控制字符必须转义或替换；写文件使用现有 opcode_report.atomic_text，避免生成半截报告。stderr 固定日志仅支持同一输出目录单实例运行。
- Python 文件头部和每个函数头部都使用中文注释说明功能、入参与返回值；日志和错误输出使用英文，避免中文日志影响现有命令行约定。
- 退出码约定：成功为 0；参数、实例、未停止状态、响应结构错误以及 invalid_argument、capability_disabled、unsupported、not_found 类 ToolError 为 2；not_attached、invalid_state、target_changed、stopping、instance_unavailable、cancelled 类会话失效 ToolError，以及 MCP 传输失败或采集期间会话失效为 3；采集只读工具出现 memory_*_failed、partial_effect、limit_exceeded 或未知 kind 时按状态未确认处理，退出 3 并输出英文告警；host_refused 按发生阶段归类：前置 stopped 检查为 2，采集中为 3；用户中断为 130。无论退出原因都关闭脚本自己启动的 Gateway。

## 文件结构与职责

| 文件 | 操作 | 职责边界 |
| --- | --- | --- |
| Scripts/get_stacktrace_register_at_breakpoint.py | 新建 | CLI、实例选择、停止状态校验、只读采集、响应校验、Markdown 渲染、退出码和 Gateway 生命周期；不承载通用 MCP 传输实现 |
| Scripts/tests/test_stacktrace_register.py | 新建 | 使用假 MCP 客户端覆盖成功、边界和失败路径；不连接真实 CE，不依赖真实地址 |
| Docs/stacktrace_register.md | 新建 | 部署前提、手动断点操作、命令、输出字段、启发式 stacktrace 限制和故障排查 |
| Scripts/ce_mcp_client.py | 不修改 | 复用既有 JSON-RPC/MCP 客户端及 BaseException 清理行为 |
| Scripts/opcode_report.py | 不修改 | 复用既有 atomic_text 和 Markdown 安全转义所需的小工具；不扩展其 opcode 领域职责 |

## 任务 1：建立脚本边界与 MCP 合同

**涉及文件：**
- 新建：Scripts/get_stacktrace_register_at_breakpoint.py

**接口依赖：**
- 输入：命令行可选 --gateway PATH、--output PATH、--instance-id ID、--timeout SECONDS；不传参数时支持用户给出的 python ./Scripts/get_stacktrace_register_at_breakpoint.py 命令。
- MCP 输入：instance_list {}；其余调用均使用 {"instanceId": instance_id}。debugger_get_context 额外传 includeExtraRegisters=true；debugger_get_stack_trace 额外传 depth=128。
- 输出：内部快照字典至少包含 instanceId、进程身份、采集时间、状态响应、上下文响应、stacktrace 响应和规范化断点地址。

**执行步骤：**

1. 按现有脚本模式计算 ROOT = Path(__file__).resolve().parents[1]，定义 Gateway 默认路径、Output 默认路径和只读工具白名单；不创建新传输层。
2. 实现 positive_timeout(text) -> int，拒绝非正整数，保证无效参数在启动 Gateway 前失败。
3. 实现 select_instance(client, wanted: str | None) -> str：调用 instance_list，拒绝 discoveryIncomplete、空列表和多实例未指定 ID；指定 ID 必须精确匹配唯一条目。
4. 实现 validate_runtime(client, instance_id) -> dict：启动后先调用 tools/list 校验六个允许工具均存在，并校验 debugger_get_context 的 inputSchema 含 includeExtraRegisters、debugger_get_stack_trace 的 inputSchema 含 depth；目录或 schema 漂移归类为退出码 2。随后读取 runtime_get_info 与 runtime_get_overview，记录进程 ID、进程名、指针宽度、会话标识及 resourceCount/jobCount 基线；若未附加目标或会话身份不可用则抛出可归类为退出码 2 的错误。该函数不调用 attach、pause 或 debugger attach。
5. 实现 require_stopped(status: dict) -> None：要求 stateValid、attached、broken 都为真；将未附加、未命中断点、状态无效和 host error 转成可读的前置条件错误。
6. 实现 normalize_address(value: object) -> str：只接受 0x 可选前缀的 1 至 16 位十六进制文本或整数，校验 0 < address < 2**64，返回大写无前缀文本；不得接受路径分隔符、空值或科学计数法。
7. 实现 capture_snapshot(client, instance_id, runtime) -> dict：按“状态 -> 上下文 -> stacktrace -> 状态 -> overview”顺序调用，第二次状态检查仍须为 stopped；从 registers["RIP"] 或 registers["EIP"] 取当前停止指令地址，并验证 is64Bit 与寄存器宽度一致。context 必填 `[is64Bit, registers, includesExtraRegisters]`，`activeInterface` 可为 null；寄存器映射值必须为字符串，FP/XMM 可缺省；stacktrace 必填 `[stackPointer, pointerSize, frames, scannedSlots]`，frame 必填 `[stackAddress, returnAddress]`，`callInstruction`、`isHeuristic` 为可选且仅在存在时校验类型。仅缺少必填字段、出现字段类型错误或 scannedSlots 越界才拒绝写文件。收尾 overview 同时复核 runtime.epoch、processId、selectionEpoch、pointerSize 和 resourceCount/jobCount；指纹变化或计数变化退出 3 且不写报告，计数结果写入 residueCheck: unchanged/changed/unavailable。
8. 对每个响应保留原始结构化字段，以便报告可重现；错误诊断同时记录 ToolError 的 kind 与 hostEffect，并对只读白名单工具断言 hostEffect 仅为 not_started 或 started，出现其他值时按状态未确认处理。寄存器按名称稳定排序，stacktrace 保持 CE 返回的栈顺序。不要通过额外内存读取“修正”启发式 frame，也不要为了确认地址而反汇编或继续执行。
9. 在 main(argv=None) -> int 中创建输出目录、启动 McpClient、执行上述流程、调用 render_report(snapshot) -> str，最后通过 atomic_text(output / f"streg_{address}.md", text) 写入；输出目录创建或写入 OSError 归类为退出码 2，并输出英文原因；使用 try/finally 确保启动未完成或采集中断时都关闭客户端。
10. 将 Gateway stderr 写到输出目录下固定的 streg_gateway.stderr.log，并在文档说明该文件仅用于诊断且同一输出目录同一时刻只允许一个采集实例；报告文件只保留用户要求的 streg_<地址>.md 内容。

**报告格式：**

- 一级标题 # Stacktrace and Registers at Breakpoint <ADDRESS>。
- 元数据区：采集时间、CE instance、进程名和 PID、指针宽度、active debugger interface、状态为 stopped、includeExtraRegisters=true、stack depth 128。
- Registers 表格：寄存器名、值；包含所有 MCP 返回项，注明 FP/XMM 以字节序列返回时的 little-endian 表示，不把缺失项填成猜测值。
- Stacktrace 表格：序号、stack slot 地址、return address、call instruction、isHeuristic；空 frame 列表也要明确写出 scanned slot 数量。
- Capture Contract：声明报告来自一次停顿上下文，stacktrace 为启发式扫描结果，脚本只读，不代表符号化调用链。
- Raw MCP Snapshot：以稳定、缩进的 JSON 保存 status/context/stacktrace，便于后续诊断；所有值通过 JSON 序列化，不直接拼接未经转义的文本。

**完成标准：** 新脚本只依赖现有客户端和标准库，支持目标命令；成功时恰好写入一个按 RIP/EIP 命名的 Markdown 文件，失败时不写成功报告、不调用任何状态改变工具。

## 任务 2：实现离线测试和失败语义

**涉及文件：**
- 新建：Scripts/tests/test_stacktrace_register.py

**接口依赖：**
- 使用假客户端实现 tools()、call()、broken 和 close()，其响应严格模拟 MCP 的结构化结果；使用 unittest.mock 替换 McpClient、临时目录和时间。
- 测试只检查脚本对工具合同的处理，不测试真实 CE 的寄存器值或启发式算法。

**执行步骤：**

1. 构造 64 位成功响应：status 为 broken、context 含 RIP、通用寄存器、EFLAGS、FP 和 XMM，stacktrace 含多个 frame；断言退出码为 0、文件名为 streg_<RIP>.md、表格和 Raw JSON 同时包含这些值。
2. 断言调用顺序为 tools/list、instance_list、runtime 健康检查（含 overview 基线）、状态、context、stacktrace、最终状态、overview 收尾；断言所有调用参数都带正确 instanceId，并断言调用集合是只读白名单加 tools/list 的子集。
3. 覆盖 32 位 EIP 路径、RIP 缺失、RIP 非法、is64Bit 与寄存器不一致、必填字段缺失、已出现字段类型错误、stack frame 必填字段缺失、depth/scannedSlots 越界；另覆盖 FP/XMM 缺省、可选 frame 字段缺省和 activeInterface=null 的合法响应。非法场景为退出码 2 且不生成报告，合法可选字段缺省场景成功生成报告。
4. 覆盖未附加、stateValid=false、broken=false、调试器未附加、多个实例未指定 ID、显式实例不存在；断言不会调用 debugger_get_context 或 stacktrace 工具。
5. 覆盖 TransportError、各类 ToolError、响应 JSON 解析错误和第二次状态检查发现已继续运行；按 kind/发生阶段断言退出码 2 或 3，stderr 含英文 kind 诊断，报告不存在，并且客户端关闭。
6. 覆盖 KeyboardInterrupt 发生在初始化、状态读取、context 读取和写文件前后；断言退出码为 130、Gateway 被关闭，且不会为了清理调用继续、暂停或 detach。
7. 覆盖原子写失败，确认临时文件被清理且不会留下伪成功文件，输出目录不可创建或 OSError 归类为退出码 2；同时检查 Markdown 清洗会处理 `\x00`、`\x1b`、`|`、换行，阻止寄存器值或指令文本破坏表格。
8. 覆盖重复运行：第二次同一停止地址通过原子替换产生完整文件，文件不包含上一次快照的残留行；该行为在操作文档中明确为覆盖当前快照。补充并发启动两个实例的约束测试，确认固定 stderr 日志要求同一输出目录单实例运行。

**完成标准：** python -m unittest Scripts/tests/test_stacktrace_register.py -v 全部通过；测试不启动真实 CE、不读取项目现有 Output 报告、不改变用户文件。

## 任务 3：补充操作说明

**涉及文件：**
- 新建：Docs/stacktrace_register.md

**执行步骤：**

1. 写明 Cheat Engine 7.7 x64、MCP DLL/Gateway、.NET 运行时和同一 Windows 用户的前置条件，并链接现有 Docs/mcp_setup.md。
2. 写明手动操作顺序：在 CE 选择目标进程、设置并命中断点、确认调试器窗口显示 stopped/broken，再从项目根目录运行用户给出的 Python 命令；脚本不会替用户附加、继续或恢复进程。
3. 说明默认输出 Output/streg_<RIP-or-EIP>.md、stderr 日志、寄存器表、原始快照和 stacktrace 表的字段含义，以及 FP/XMM 可能因调试器后端不提供而缺失；明确 RIP/EIP 是当前停止上下文的指令地址，不保证是断点列表登记地址，固定 stderr 日志仅支持同一输出目录单实例运行。
4. 明确 stacktrace 接口是最多 128 个栈槽的启发式扫描，callInstruction 只是 CE 能反汇编时提供的候选信息；分析时必须结合断点现场和反汇编复核。
5. 添加故障处理表：没有 stopped context、多个 CE 实例、Gateway 超时、权限/路径错误、输出文件被占用；每项给出退出码和下一步人工操作。

**完成标准：** 文档命令、输出文件名和脚本实际默认值一致，不承诺未实现的符号化 stacktrace、自动断点或自动恢复。

## 任务 4：验证与人工 CE 验收

**涉及文件：** 已完成任务 1 至 3 的全部文件。

**执行步骤：**

1. 运行 python -m unittest Scripts/tests/test_ce_mcp_client.py Scripts/tests/test_stacktrace_register.py -v，确认传输层和新脚本离线测试均通过，并覆盖工具目录/schema 漂移、ToolError kind 映射、收尾指纹及 resourceCount/jobCount 核对。
2. 运行 python -m unittest discover -s Scripts/tests -p "test_*.py" -v，确认新增测试没有破坏 opcode 相关流程。
3. 运行 python -m py_compile Scripts/get_stacktrace_register_at_breakpoint.py Scripts/tests/test_stacktrace_register.py，并运行 git diff --check；检查没有临时文件进入仓库。
4. 在 CE 中由用户手动将目标进程运行到断点，确认 CE 窗口保持 stopped；从 D:\cebuild\ce-custom 执行 python ./Scripts/get_stacktrace_register_at_breakpoint.py，不使用自动 attach 或 continue。
5. 检查 Output 中存在唯一的 streg_<断点地址>.md；核对标题地址等于报告 Raw JSON 中 RIP/EIP，寄存器包含 RSP/RBP/RIP（64 位）或对应 32 位寄存器，且 includesExtraRegisters 为真；核对 stacktrace 的 scannedSlots 不超过 128。
6. 人工确认脚本结束后目标仍停在原停止指令，CE 未新增/删除断点，未产生内存写入；核对报告中的收尾指纹与 residueCheck，必要时查看 streg_gateway.stderr.log，不把日志内容当作报告数据。
7. 记录真实 CE 验收的 Gateway 版本、目标进程 PID、输出文件名和测试命令；不在方案中伪造现场寄存器、stacktrace 或“符号化调用链已正确”的结论。

**完成标准：** 离线测试、静态检查和一次真实手动断点采集均通过；所有失败路径都有确定退出码和清理行为，且没有修改 CE/目标进程状态。

## 方案自检

- [ ] 每个新增文件的职责、接口、输入输出和边界已明确。
- [ ] 每个任务均能产生独立可测试的交付物，没有“待补充”“后续实现”或仅描述需求的占位步骤。
- [ ] 方案没有引用未定义的函数、字段或工具；所有调试器工具名称与当前 Gateway tools/list 合同一致。
- [ ] “所有寄存器”通过 includeExtraRegisters=true 和原样保存 MCP 返回键值实现，未承诺后端不存在的寄存器。
- [ ] “stacktrace”已明确为 MCP 的启发式候选 frame，而非未经验证的符号化调用栈。
- [ ] 没有加入自动附加、断点创建/删除、暂停/继续、内存读取或写入等超出需求的功能。
- [ ] 测试覆盖成功、输入错误、未停止、传输错误、中断、原子写失败和重复运行，不依赖真实 CE。
- [ ] 方案只新增计划文档；执行本方案前不得修改现有源码。
