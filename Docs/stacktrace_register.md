# 手动断点的 Stacktrace 与寄存器采集

此脚本读取用户已经手动停住的 Cheat Engine 调试现场，默认生成寄存器表、CE 原生 StackTrace 表及精简后的 MCP 快照。脚本不附加目标、不设置或删除断点、不暂停或继续目标、不写目标内存。原生模式通过固定 Lua 查询刷新 CE 堆栈窗口；若窗口不存在，会临时打开并在读取完成或异常后关闭，仅结束自己启动的 Gateway。

## 环境与手动准备

- Windows x64、Cheat Engine 7.7 x64，安装目录为 `C:\Program Files\Cheat Engine`。
- 已按 [MCP 部署说明](mcp_setup.md) 启用 `CheatEngine.Mcp.dll`。本项目使用 `CheatEngine.Mcp-2.0.0-beta.2-win-x64` 包。
- 已安装包所需的 .NET 10 运行时：`Microsoft.NETCore.App`、`Microsoft.AspNetCore.App`、`Microsoft.WindowsDesktop.App`；CE 的 runtimeconfig 需与部署要求一致。
- Gateway 与 CE 使用同一个 Windows 用户运行，具备访问目标的权限。
- Python 3.10 或更新版本；仅使用标准库及项目内的 `ce_mcp_client.py`、`opcode_report.py`。

先在 CE 中选择目标进程，手动设置并命中断点，确认调试器处于 stopped/broken 状态，再运行采集。采集期间保持现场不动，不单步、不继续、不切换线程或目标进程。脚本的首尾状态和会话指纹校验无法识别两次调用之间发生的继续后再次停止，也不能替代用户保持现场稳定。

## 执行命令

在 CMD 中直接运行，无需额外参数：

```cmd
cd /d D:\cebuild\ce-custom
python Scripts\get_stacktrace_register_at_breakpoint.py
```

`cd /d` 同时切换盘符和目录。PowerShell 中也可从项目根目录运行：

```powershell
Set-Location D:\cebuild\ce-custom
python ./Scripts/get_stacktrace_register_at_breakpoint.py
```

默认 Gateway：`McpExternals/CheatEngine.Mcp-2.0.0-beta.2-win-x64/CheatEngine.Mcp.Gateway.exe`。
默认输出目录：项目根目录 `Output`。这两个默认值以脚本所在项目为基准，不受启动目录影响。

可选参数：

```powershell
python ./Scripts/get_stacktrace_register_at_breakpoint.py --instance-id "<instance_list 返回的精确 ID>" --timeout 30 --output "D:\cebuild\ce-custom\Output"
python ./Scripts/get_stacktrace_register_at_breakpoint.py --gateway "D:\path\CheatEngine.Mcp.Gateway.exe"
python ./Scripts/get_stacktrace_register_at_breakpoint.py --stack-mode heuristic
```

`--timeout` 为每次 MCP 请求的正整数超时秒数，默认 30。实例不唯一时必须指定 `--instance-id`，脚本不会猜选。`discoveryIncomplete=true` 时也不会采集。

`--stack-mode native` 为默认值，无参数运行即可获取原生堆栈。`--stack-mode heuristic` 显式启用旧的 128 槽候选扫描，仅供兼容诊断；原生模式失败不会自动降级。

同一输出目录同一时刻只允许一个采集实例。脚本不提供并发锁；同时运行的两个实例会使用同一个 `streg_gateway.stderr.log`，可能截断彼此日志并覆盖同地址报告。需要并行运行时使用不同的 `--output` 目录。

## 输出与字段解释

成功写入 `Output/streg_<RIP-or-EIP>.md`。地址为当前停止上下文的 RIP（64 位）或 EIP（32 位），规范化为大写十六进制、无 `0x`、无前导零。**该地址不保证等于断点列表登记地址**，例如单步或异常停顿也可能产生停止上下文。

同一地址再次成功采集会原子覆盖当前快照，旧的寄存器行不会残留。写入失败保留此前完整报告，因此目录中已有报告不表示本次采集成功；应同时检查退出码和报告采集时间。文件使用 UTF-8、LF。每次成功只写入一个 Markdown 报告，不生成额外 manifest。

`streg_gateway.stderr.log` 是 Gateway 的诊断日志，每次启动覆盖，不能作为寄存器或栈数据使用。

| 区域 | 含义 |
| --- | --- |
| 标题及元数据 | 停止指令地址、UTC 采集时间、CE 实例、目标 PID/名称、指针宽度、调试接口及 stopped 状态 |
| Registers | MCP 返回的所有寄存器键和值，按名称稳定排序；始终请求 `includeExtraRegisters=true` |
| FP/XMM | 后端提供时保留 FP0–FP7、XMM0–XMM15（32 位通常为 XMM0–XMM7）；字节序列为内存顺序，little-endian，低有效字节在前，不重新解释成浮点数 |
| Stacktrace（默认 native） | CE View → StackTrace 的所有行：序号、PC、Stack、Frame、Return、Parameters；保留 CE 显示的符号和顺序 |
| frameCount / termination | CE 返回帧数；末返回地址为零记为 `zero_return`，否则为 `unwind_stopped` 并明确告警可能未展开到底 |
| Stacktrace（heuristic） | 旧模式的序号、栈槽地址、候选返回地址、可选 callInstruction、可选 isHeuristic |
| scannedSlots（仅 heuristic） | 实际扫描栈槽数，范围 0–128；空候选列表仍记录扫描数量 |
| Capture Contract | 目标只读范围、原生窗口刷新影响、停止地址语义及所选堆栈模式的限制 |
| Raw MCP Snapshot | 状态、context、stacktrace、前后 overview、runtime 信息、会话指纹及资源计数；递归排除 `evidence`、`capabilities`、`hostVersion`、`platform`，使用稳定缩进 JSON 保存 |
| residueCheck | 成功报告为 `unchanged`，并包含前后 resourceCount/jobCount；变化时日志显示 `changed`，末次核对不可用时显示 `unavailable` 或传输错误，拒绝写入新报告 |

FP/XMM 是否出现取决于调试器后端，缺失不等于零，不补猜测值。`activeInterface=null` 和未返回的可选 frame 字段在表格显示 `unavailable`，Raw JSON 保留原始结构。Markdown 中的控制字符、换行和分隔符会清洗，原始内容可从 JSON 还原。

## Stacktrace 的适用边界

### 默认原生模式

现有 MCP 没有直接提供 CE 窗口使用的原生展开接口。脚本通过 `lua_execute` 执行固定查询，在 CE 主线程定位唯一 `TfrmStacktrace`，调用 `Refresh1.doClick()`，然后复制 `ListView1` 的全部行。窗口不存在时通过 Memory Viewer 的 `Stacktrace1` 菜单创建；只关闭本次创建的窗口，保留用户已有窗口。此路径可能短暂显示窗口，并刷新已有窗口的行与选择状态；它不属于完全无界面副作用的查询。

CE 本地源码 `frmstacktraceunit.pas` 的该路径调用 Windows `StackWalk64`，并通过模块异常/展开数据及符号器生成 PC、Frame 和 Return。这与逐栈槽猜测返回地址不同，不受 128 槽、1 KB 栈空间限制。脚本导出 CE 返回的全部行，上限为 2048 帧以控制 MCP 响应大小；超限会拒绝报告而非静默截断。该上限只约束结果复制，不控制 CE 内部展开耗时；Gateway 超时不表示 CE 的主线程展开已经中止。

查询对 IP、SP、BP、THREADID 做前后核对，Python 还会比较查询身份与首次寄存器结果，并在末次重新读取寄存器复核身份。首帧 PC/SP 必须与停止现场一致，以拒绝不匹配的窗口内容。多窗口歧义、控件结构不符、空帧、非法字段、Lua 返回丢弃对象或查询失败均拒绝覆盖旧报告，不会以候选扫描替代原生结果。

“全部行”指当前 CE 原生展开得到的全部结果，不保证缺失展开元数据、损坏栈或不可读内存场景仍能恢复完整调用链。末返回地址不为零时，终端和报告都警告可能不完整；返回零本身也不构成对目标调用链正确性的独立证明。

Parameters 按 CE 当前显示文本保留。CE 的此窗口取四个参数槽并显示摘要，不能将其当成完整的 x64 函数参数或自动推断寄存器实参。JSON 同时记录符号文本和解析后的 PC/Return 十六进制地址。

### 显式启发式模式

`--stack-mode heuristic` 使用 `debugger_get_stack_trace(depth=128)`，最多扫描 **128 个栈槽**，不是保证返回 128 个调用帧；64 位目标实际覆盖 1024 字节。frame 是启发式候选，可能包含陈旧栈数据或误判的代码指针，并非原生展开调用链。`callInstruction` 可缺省，分析时须结合现场与反汇编复核。

两种模式都使用 `instance_list`、`runtime_get_info`、`runtime_get_overview`、`debugger_get_status`、`debugger_get_context`。原生模式新增固定 `lua_execute` 查询，不依赖 `debugger_get_stack_trace`；启发式模式使用该旧工具。启动期调用 `tools/list` 校验当前模式所需工具及参数。除实例发现外，每个业务调用均带本次发现的 `instanceId`。

## 无需重编译 DLL 的状态兼容路径

部分现场的 `debug_isBroken()` 返回函数对象，使 MCP 状态查询报告 `stateValid=false`。脚本仅识别这一项已确认的非布尔返回错误，并自动通过 `lua_execute` 发送固定只读查询，以 `debug_isDebugging()` 和 `debug_getCurrentContextTable(false)` 确认停止状态，不调用异常的 `debug_isBroken()`。其他状态错误仍按原规则失败。

状态兼容功能与原生堆栈查询均通过专用调用点发送写死的 Lua，不接受外部 Lua 源码，不修改 CE 全局函数、目标内存、断点或运行状态。`lua_execute` 是通用执行工具，本身不声明只读，也不会加入通用只读工具白名单；原生堆栈查询的界面刷新影响见上节。

原生堆栈和状态兼容查询都要求已启用 `Mcp:EnableUnsafeLua`；当前现场已经启用，无需重载插件。禁用时会以 `capability_disabled` 退出 2，不会替用户更改配置。成功响应必须为 `ok=true`、`hostEffect=completed` 且无丢弃数据；Lua 运行失败或效果无法确认退出 3。

采集前后兼容查询的指令地址和栈指针必须与寄存器响应一致，栈接口的 stackPointer 也要匹配；会话指纹和资源计数照常核对。报告标记 `statusSource=lua_execute_fixed_query`，并保留 `originalStatus`、`luaResponse` 原始证据，不伪造 `reportedBroken`。

## 故障处理

| 现象 | 退出码 | 人工处理 |
| --- | ---: | --- |
| 没有附加进程、调试器未附加、没有 stopped context 或状态无效 | 2 | 在 CE 手动选择目标并命中断点，保持停止后重试 |
| 多个 CE 实例、指定实例不存在或发现不完整 | 2 | 确认实例列表，使用精确 `--instance-id`；待发现完整后重试 |
| 工具目录/schema 漂移、响应字段或地址非法 | 2 | 核对已部署 MCP 包与接口合同，查看英文错误，不使用旧报告冒充新结果 |
| Gateway 超时、通信失败或 JSON 无法解析 | 3 | 查看 stderr 日志，确认 CE 响应、同一 Windows 用户及 Gateway 进程环境；必要时增大 `--timeout` |
| Gateway 路径错误、输出目录权限错误 | 2 | 修正路径或目录权限后重试 |
| 输出文件被占用或原子替换失败 | 2 | 解除文件占用并检查目录权限；旧报告如已存在会保留 |
| 采集中目标继续运行、会话身份或资源/作业计数变化 | 3 | 在 CE 人工检查目标、停止状态及资源；稳定现场后重试 |
| `invalid_argument`、`capability_disabled`、`unsupported`、`not_found` | 2 | 根据 kind 检查参数、部署配置和能力 |
| `not_attached`、`invalid_state`、`target_changed`、`stopping`、`instance_unavailable`、`cancelled` ToolError | 3 | 会话已失效，人工恢复目标及断点现场后重新运行 |
| `host_refused` | 前置检查 2；采集中 3 | 手动确认停止现场；采集中拒绝时不信任本次快照 |
| `memory_*_failed`、`partial_effect`、`limit_exceeded`、未知 kind 或非只读 hostEffect | 3 | 状态未确认，保留英文告警及日志进行人工排查 |
| Ctrl+C | 130 | 本次 Gateway 会关闭，目标不自动继续；若中断发生在原子提交后，完整报告可能已存在 |

成功退出码为 0。ToolError 诊断同时打印 `kind` 和 `hostEffect`；只接受 `not_started` 或 `started`，其他效果按状态未确认处理。

## 验证命令与人工验收

```powershell
python -m unittest Scripts/tests/test_ce_mcp_client.py Scripts/tests/test_stacktrace_register.py -v
python -m unittest discover -s Scripts/tests -p "test_*.py" -v
python -m py_compile Scripts/get_stacktrace_register_at_breakpoint.py Scripts/tests/test_stacktrace_register.py
git diff --check
```

离线测试使用假客户端和临时目录，不连接 CE，也不读取项目现有 Output 报告。

真实验收须由用户手动准备断点：运行默认命令后，核对标题地址与 Raw JSON 的 RIP/EIP 一致，位宽对应的 SP/BP/IP 和 THREADID 寄存器存在、`includesExtraRegisters=true`、`stacktrace.source=ce_stacktrace_window`、`frameCount` 与窗口行数一致；逐列比较 PC/Stack/Frame/Return，检查 termination、前后指纹与 `residueCheck.state=unchanged`。仅旧模式检查 `scannedSlots<=128`。随后人工确认 CE 仍停在原指令、断点未增删、目标内存未被修改。离线测试通过不代表已完成所有人工验收。

2026-10-01 实测：现有 `2.0.0-beta.2` DLL 未重编译或重载，上述 CMD 无参数命令退出 0，生成 `Output/streg_7FF777CED5C9.md`。目标为 victoria3（PID 43884），返回 43 项寄存器、扫描 128 个栈槽、1 个启发式候选。首尾停止地址和栈指针一致，resourceCount/jobCount 均为 0→0，residueCheck 为 unchanged。全量 51 项离线测试及 py_compile 通过；自动核对不等于对目标全部内存做差分验证。

2026-10-02 00:29:38（北京时间）原生模式实测：同一部署包无需重编译，执行 `python Scripts/get_stacktrace_register_at_breakpoint.py` 退出 0，更新 `Output/streg_7FF777CED5C9.md`。取得 17 帧，PC/Stack/Frame/Return 与用户粘贴的 17 行对应，末帧为 `ntdll.RtlUserThreadStart+2C`，返回地址零。Parameters 使用本次实读值，其中 `victoria3.exe+3ACD8CE` 一行与用户旧样本不同。43 项寄存器、前后身份与资源计数校验通过，四类冗余字段继续被过滤；本次复用已有隐藏窗口，读取后保持隐藏。前置现场探测也覆盖了临时打开并关闭窗口的路径。全量 60 项离线测试（含 32 项断点采集测试）、py_compile 及本次修改文件的 diff 空白校验通过。
