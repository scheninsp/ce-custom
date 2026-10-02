# 调试器兼容单步采集实施方案
> **面向自动化执行人员：必须配套子能力：使用 superpowers:executing-plans 逐任务执行本方案。步骤使用复选框（`- [ ]`）用于进度跟踪。**
**目标：** 通过 Python 在严格的单步边界前完成全部可变状态检查，仅把一次 `debugger_step` 作为唯一目标执行操作；单步之后只读取新停点并报告结果，不尝试恢复、清理或重试目标状态。
**架构方案：** 复用既有固定 Lua 状态兼容查询，但把它放在“单步前检查”和“单步后观测”两个阶段。单步前动态取得模块基址、校验工具合同、能力门、目标身份、暂停状态、线程和断点快照；任一检查失败都在单步前退出。v1 固定只执行一次单步，单步调用开始后无论返回成功、超时、传输断开还是状态不明，都不调用恢复型工具，只做有限只读观测并输出报告。
**安全承诺边界：** 本方案只能保证脚本层面“单步请求发出前不主动调用改变目标执行、内存、寄存器、用户断点或 CE job 的操作；单步请求发出后不主动恢复、清理或重试”。它不能证明 MCP/CE 内部实现绝对无副作用，不能消除查询与单步之间的 TOCTOU 窗口，也不能在通信异常时证明单步是否完成或 CE 临时调试状态是否已经收尾。
**技术栈：** Python 3.11+ 标准库、现有 `McpClient`、Cheat Engine MCP `debugger_step`、固定 `lua_execute` 状态查询、MCP 调试器查询工具、JSON/UTF-8 Markdown。

## 全局约束
- 使用中文进行对话输出。
- 使用中文进行代码注释，但是不要使用中文日志。
- python,powershell等脚本代码文件，需要在文件头部使用中文注释说明文件功能。
- 每个函数头部都要加上函数功能，以及入参与返回值的中文注释说明。
- 不修改 `D:\cebuild\CheatEngine.Mcp` 源码或部署 DLL。
- v1 固定只调用一次 `debugger_step`；不提供 `--steps` 参数，不自动再次单步。
- 不调用 `debugger_continue`、`debugger_break_thread`、`debugger_run_to`、`debugger_start_trace`、`debugger_start_capture`、`runtime_stop_job`、`debugger_set_register`。
- 不设置、删除、启用、禁用或移动用户断点；不写入目标内存；不执行 Auto Assembler、注入或任意目标代码。
- `debugger_step` 是唯一允许改变目标执行位置的工具，也是本方案唯一接受的不可逆状态边界。
- 单步之前的任何异常、超时、合同不匹配、能力缺失、状态不确定或文件准备失败，都必须在调用 `debugger_step` 前结束；单步之前不得调用任何可能启动 CE job、安装临时断点或改变调试上下文的工具。
- 单步调用之后不执行恢复性调用。无论单步结果如何，脚本只进行有限状态观测；观测失败时不重试会改变状态的工具。
- `lua_execute` 只能发送从现有脚本导入的固定 `STATUS_COMPAT_SOURCE` 和固定 `STATUS_COMPAT_CHUNK`；不得接受命令行 Lua、文件 Lua 或字符串插值。它是**受限源码调用，不是严格只读能力**，其残余风险必须写入报告。
- 关闭 Gateway 只回收 Python 自己创建的 stdio 子进程，不等同于恢复或取消 CE 调试状态；如果请求仍在服务端处理，关闭 Gateway 也不保证服务端已完成或取消。
- 目标进程状态和 CE 调试器底层清理由 MCP/CE 负责；Python 不在失败路径中猜测或补偿。
- 所有单步前检查必须完成并写入内存中的 audit 对象；单步前本地报告使用临时文件，不接触目标进程。

## 未消除的运行时风险

以下风险不能由 Python 原子消除，必须作为正式报告状态：

1. **TOCTOU：** 最终 RIP/线程/断点检查与 `debugger_step` 请求不是一个原子操作；其他 CE 操作、其他客户端或目标线程可能在两次调用之间改变现场。
2. **单步响应不确定：** 请求发出后传输超时、Gateway 崩溃或 CE 异常时，不能证明单步是否执行、是否只执行一条指令或线程是否仍停止。
3. **数据断点交互：** 当前用户断点可能包含 `R14+0x1D58`、`R14+0x1D5C` 对应的数据地址。单步执行读取指令时，可能因访问断点先停下；此时 `stopReason` 必须为 `unknown` 或 `data_breakpoint`，不能只依据 RIP 期望值宣称单步成功。
4. **CE 临时调试状态：** `debugger_step` 的临时单步机制、线程调试标志、异常队列和硬件槽位由 CE 核心维护；`resourceCount/jobCount` 只能作为辅助残留证据，不能覆盖所有内部状态。
5. **查询非原子性：** 模块、状态、寄存器、断点和内存读取来自不同 MCP 调用，报告必须保留采集顺序和时间，不得声称它们构成一个原子现场。
6. **固定 Lua 残余风险：** 固定查询源码已人工审查为不写目标，但 `lua_execute` 使用高权限能力；脚本只限制源码，不把 MCP 工具本身标为严格只读。

## 阶段安全模型

### 阶段 A：单步前纯检查

阶段 A 只允许以下查询工具：

- `tools/list`
- `instance_list`
- `runtime_get_info`
- `runtime_get_overview`
- `module_get` 或 `module_list`
- `debugger_get_status`
- 固定 `lua_execute`
- `debugger_get_context`
- `debugger_list_breakpoints`
- `memory_read_batch`
- `code_disassemble`

任何工具目录缺失、合同不符或未列出的工具调用都立即退出，不调用单步。

### 阶段 B：唯一单步边界

调用前最后一次检查必须包括：

```text
目标 PID、runtime epoch、selection epoch、pointer size
victoria3.exe 模块基址和模块构建身份
当前 RIP、RSP、THREADID
当前工具合同快照
当前断点快照
固定 Lua 源码和 chunkName 校验结果
unsafe_lua 能力门
R14 和动态内存预检结果
```

将审计对象中的 `stepCallStarted` 保持为 `false`。进入 Python `client.call("debugger_step", ...)` 调用边界前，不写入目标进程、不调用任何写类工具。

### 阶段 C：单步后只读观测

单步调用一旦开始，立即将 `stepCallStarted=true`，然后只允许：

- 固定兼容状态查询；
- `debugger_get_context`；
- `runtime_get_overview`；
- `debugger_list_breakpoints`；
- `memory_read_batch`；
- `code_disassemble`；
- 本地报告写入。

单步后禁止：

- `debugger_continue`；
- `debugger_break_thread`；
- `debugger_run_to`；
- `debugger_start_trace`；
- `debugger_start_capture`；
- `runtime_stop_job`；
- 设置、删除或修改断点；
- 修改寄存器；
- 写内存；
- 第二次 `debugger_step`。

如果单步后状态不明，报告 `postStepState=unknown` 并结束。脚本不尝试恢复目标状态，用户需要在 CE 中人工确认。

## MCP 工具合同和安全能力

### 工具目录校验

单步前读取 `tools/list`，并验证：

- 查询工具的 `annotations.readOnlyHint is true`；
- 查询工具的 `annotations.destructiveHint is false`；
- `debugger_step` 的 `readOnlyHint is false`、`destructiveHint is false`、`idempotentHint is false`；
- `debugger_step.inputSchema` 必须要求 `instanceId`，且 `mode.enum` 精确包含 `into`、`over`；
- `module_get` 或 `module_list` 的 schema 能取得 `victoria3.exe` 的基址和路径；
- `memory_read_batch` 的 schema 支持 `items`；
- `lua_execute` 的 schema 包含 `instanceId`、`source`、`chunkName`。

工具注解是合同证据，不是运行时隔离证明。若查询工具注解缺失或不符合预期，在单步前退出。

### `unsafe_lua` 硬门槛

`runtime_get_info` 或 `runtime_get_overview` 返回的能力门必须满足：

```python
if type(gates.get("unsafeLua")) is not bool or gates["unsafeLua"] is not True:
    raise CaptureError("unsafe_lua capability is unavailable", code=2)
```

能力门缺失、类型错误或为 `false` 时，必须在单步前退出。调用时若仍返回 `capability_disabled`，不得重试，不得单步，不得恢复。

### 模块基址和构建身份

使用 `module_get` 或 `module_list` 动态取得 `victoria3.exe` 的 `base`、`path`、`size`、`is64Bit`。单步前要求：

- 进程名为 `victoria3`；
- 模块名为 `victoria3.exe`；
- `is64Bit=true`；
- 路径为 `D:\Games\Victoria3\Victoria 3\binaries\victoria3.exe` 或与用户现场一致的已确认路径；
- `base`、`size` 为合法非零值；
- 当前 RIP 等于 `base + 0x11FD5C9`；
- 单步后预期 RIP 为 `base + 0x11FD5D0`。

禁止使用旧报告中的硬编码绝对地址验证当前执行位置；对象指针和栈地址也必须每次按当前寄存器动态计算。

## 单步路线和版本策略

v1 只支持一次单步：

```text
victoria3.exe+11FD5C9  mov eax,[r14+1D58]
        │ 唯一状态改变边界：debugger_step(mode="into")
        ▼
victoria3.exe+11FD5D0  mov [rsp+50],eax
```

不提供 `--steps` 参数，不允许脚本循环单步，不允许脚本自动从 `+11FD5D0` 继续到 `+11FD5D4`。后续若需要第二步，必须由用户重新确认停点并重新启动一次脚本。

## 现场和响应验证规则

### 单步前

必须满足：

- 目标进程名、PID、runtime epoch、selection epoch、pointer size 与基线一致；
- 模块基址、路径、大小和位数通过模块工具确认；
- 固定 Lua 查询源码/chunkName 与导入常量逐字相等；
- 原始状态正常，或已知 `debug_isBroken` 错误由固定 Lua 查询证明 `stateValid=true`、`attached=true`、`broken=true`；
- 固定 Lua 状态与 `debugger_get_context` 的 RIP、RSP 和架构一致；
- `THREADID` 为非零合法十六进制值；
- 断点快照返回 `breakpoints`、`total`、`truncated`，且 `truncated=false`；
- 记录 `R14`、`RSP`，并按它们生成内存地址；`RDI`、`RSI` 只能记录，不参与安全校验，也不解引用；
- `memory_read_batch` 预检满足严格成功规则。

### 单步后

- `stepCallStarted=true` 后，无论 MCP 返回成功、错误、超时或断连，都不把它改回 `false`；
- 原始 `debugger_get_status.stepping` 仅作为附加诊断字段，不能作为停止判据；
- 轮询使用固定兼容查询：只有兼容查询的 `broken=true` 且后续 `debugger_get_context` 的 RIP/RSP/架构一致，才能报告 `postStepState=stopped`；不能证明停止时只能报告 `unknown`；
- 轮询参数固定为间隔 50ms、总时限 10s；轮询只调用查询工具；
- `postStepState=stopped` 时要求 RIP 为 `base+0x11FD5D0`；偏离则写 `unexpectedRip=true`，不再继续；
- 记录 `stopReason`：`step`、`data_breakpoint`、`unknown`；MCP 当前合同没有可靠的停止原因时不猜测，使用 `unknown`；如果断点列表/工具或 CE 诊断明确表明数据断点命中，记录 `data_breakpoint`；
- 线程 ID、PID、runtime epoch、selection epoch 或断点快照变化时，记录漂移并停止；
- 单步后内存读取使用动态 RSP/R14；不读取旧现场绝对地址。

## 断点快照范围

`debugger_list_breakpoints` 只保证返回工具合同允许的字段：`breakpoints`、`total`、`truncated`，以及每项实际存在的 `address`、`owned`、可选 `resourceId`。它不保证条件、类型、大小、访问方式、线程过滤、启用状态等 CE 内部属性。报告只能比较工具返回的原样快照；若 `truncated=true`，写入 `breakpointsUnchanged=unknown`，不得声称列表完整。

## 内存批量读取响应规则

`memory_read_batch` 返回批量结果时：

- 单步前：响应必须是对象，`failed == 0`，`items` 数量等于请求数量；每项地址顺序与请求一致；每项必须有 `value`，不得有 `error`。
- 单步后：RPC 失败属于观测失败；`failed > 0` 或单项错误属于部分观测失败，记录原始 `failed/items`，不重试、不恢复；关键字段缺失时 `postObservation=partial` 或 `unknown`。
- 任何响应结构错误都不得被当作成功；单步前退出码 2，单步后退出码 3。

## 报告字段和退出码

报告至少包含：

- `stepCallStarted`：进入 `debugger_step` 调用边界后为 `true`；发送前异常为 `false`；不表示 CE 已确认完成单步；
- `stepResponse`：收到的结构化响应或错误摘要；
- `preflight`：工具合同、能力门、模块、进程、状态、上下文、断点快照和内存预检；
- `postStepState`：`stopped` 或 `unknown`；
- `postObservation`：`complete`、`partial` 或 `unknown`；
- `stopReason`：`step`、`data_breakpoint` 或 `unknown`；
- `initialRip`、`actualRip`、`expectedRip`、`unexpectedRip`；
- `initialRsp`、`actualRsp`、`initialThreadId`、`actualThreadId`；
- PID、runtime epoch、selection epoch、pointer size；
- `breakpointsBefore`、`breakpointsAfter`、`breakpointsUnchanged`；只表示 MCP 返回范围内的快照；
- `residueCheck`：`unchanged`、`changed` 或 `unavailable`；只表示已检查的资源/作业/快照项，不覆盖 CE 全部临时调试状态；
- `queryTimeline`：每个工具调用的顺序、阶段、开始/结束时间和结果类别；
- `error`、`gatewayClosed`、`manualRecoveryRequired`。

退出码固定为：

- `0`：单步调用开始且收到响应，后置状态确认停止，预期 RIP 匹配，后置观测完整，未发现可报告漂移；
- `2`：单步前失败，`stepCallStarted=false`；
- `3`：单步调用开始后发生错误、通信失败、状态未知、RIP 偏离、线程/会话/断点漂移或后置观测不完整；
- `130`：用户中断；中断后同样不调用恢复工具。

## Python 接口

```python
def validate_tool_contract(catalog: dict) -> dict:
    """校验单步与查询工具合同；参数为 tools/list 目录，返回已确认的工具能力字典。"""

def read_fixed_status(client, instance_id: str, *, compat_available: bool, phase: str) -> dict:
    """读取原生或固定 Lua 兼容状态；参数为客户端、实例、能力和阶段，返回状态或阶段错误。"""

def capture_preflight(client, instance_id: str, catalog: dict) -> dict:
    """执行全部单步前纯查询；参数为客户端、实例和工具目录，返回不可变基线快照。"""

def issue_single_step(client, instance_id: str, mode: str, audit: dict) -> dict:
    """标记调用边界并发出一次单步；参数为客户端、实例、模式和审计对象，返回响应或错误。"""

def capture_post_step(client, instance_id: str, baseline: dict, expected_rip: int) -> dict:
    """只读采集单步后状态；参数为客户端、实例、基线和预期 RIP，返回观测快照。"""

def write_report(path: Path, report: dict) -> None:
    """原子写入单步报告；参数为目标路径和报告对象，无返回值。"""

def run_capture(argv: list[str]) -> int:
    """执行单步前检查、一次单步和单步后观测；参数为命令行参数，返回退出码。"""
```

## 任务 1：新增单步脚本

**涉及文件：** 新建 `Scripts/step_capture_at_breakpoint.py`。

**接口依赖：** `McpClient`、`STATUS_COMPAT_SOURCE`、`STATUS_COMPAT_CHUNK`、`field`、`normalize_address`、`CaptureError`、`atomic_text`；输出 JSON/Markdown 报告。

**执行步骤：**

- [ ] 文件头加入中文功能注释；函数头全部写中文功能、入参与返回值说明。
- [ ] 导入固定兼容查询常量，不复制或拼接 Lua 源码。
- [ ] 实现阶段守卫：preflight 只允许上文查询工具；step 阶段只允许一次 `debugger_step`；postflight 只允许上文查询工具。
- [ ] 实现 `validate_tool_contract`，严格校验 tools/list 的 annotations、schema、`module_get/module_list`、`memory_read_batch`、固定 Lua 字段和 `unsafe_lua` 能力门；注意 `lua_execute` 只作受限源码调用，不标记为严格只读。
- [ ] 取得模块基址前不使用旧绝对地址；从模块工具返回结果中解析 `victoria3.exe` 的基址、路径、大小和位数。
- [ ] 选择唯一实例，读取 runtime info/overview，建立进程与 runtime 基线；unsafe_lua 不可用时退出码 2。
- [ ] 读取原始状态；已知错误只通过固定兼容查询确认停止，其他错误退出；读取上下文、断点快照、模块和代码窗口，校验当前 RIP 为 `base+0x11FD5C9`。
- [ ] 按当前 R14/RSP 动态生成预检内存请求；严格检查 `failed==0`、请求/响应数量、每项 value/error；预检任何失败都不调用单步。
- [ ] 单步前将完整基线写入内存审计对象；记录查询时间线和每个接口的结果类别。
- [ ] 在进入 `client.call("debugger_step", ...)` 的 Python 调用边界前保持 `stepCallStarted=false`；进入该调用包装函数后立即设置为 `true`。设置后无论异常类型如何不恢复为 false；不把 true 解读为 CE 已完成单步。
- [ ] 单步后只用固定兼容查询轮询，50ms 间隔、10s 超时；原始 `stepping` 只记录，不作为判据。
- [ ] 停止确认后读取 context、overview、breakpoints、动态内存和代码窗口；任何失败只记录，返回退出码 3，不重试写类工具。
- [ ] 根据兼容状态、上下文和可用诊断记录 `stopReason`；无法证明是 step 或 data_breakpoint 时写 `unknown`。
- [ ] finally 只关闭 Gateway 和写本地报告；不得调用任何 CE 恢复接口；Gateway 关闭不得被报告为 CE 状态恢复。

## 任务 2：单元测试

**涉及文件：** 新建 `Scripts/tests/test_step_capture.py`。

**接口依赖：** 任务 1 的阶段守卫、合同校验、预检、单步边界、后置观测和报告函数。

**执行步骤：**

- [ ] 假客户端记录工具名、参数、阶段、时间线、调用次数和每次响应；任何未列工具直接失败。
- [ ] 测试模块工具缺失、错误模块、RIP 不匹配、PID/epoch/selection/thread/RSP/R14/断点不匹配：单步调用次数为 0。
- [ ] 测试查询工具 annotations 不符合、schema 漂移、固定 Lua 常量不匹配、unsafe_lua 缺失/false：单步调用次数为 0。
- [ ] 测试内存预检 `failed>0`、items 数量不符、单项 error、缺 value 或结构错误：单步调用次数为 0。
- [ ] 测试单步调用前抛错：`stepCallStarted=false`；进入调用后抛错、超时、断连或未收到响应：`stepCallStarted=true`，不调用任何恢复工具。
- [ ] 测试单步后兼容查询 pending/unknown、RIP 偏离、线程/会话/断点漂移、数据断点命中标记、内存部分失败：只记录并退出 3，不再次单步、不恢复。
- [ ] 测试查询调用之间的快照不一致，报告 TOCTOU/非原子现场，不把结果标记为原子快照。
- [ ] 测试正常路径只调用一次 `debugger_step(mode="into")`，到达 `base+0x11FD5D0`，后置观测完整并退出 0。
- [ ] 测试 `debugger_break_thread`、`debugger_continue`、`debugger_run_to`、trace、job、寄存器写入、断点工具、内存写入均不会被调用。
- [ ] 测试 Gateway 关闭和本地报告失败不会触发 CE 工具调用。

## 任务 3：文档和真实验收

**涉及文件：** 新建 `Docs/step_capture.md`。

**接口依赖：** 任务 1 CLI、任务 2 测试结果和报告字段。

**执行步骤：**

- [ ] 说明用户必须手动停在 `victoria3.exe+11FD5C9`；脚本不会定位、暂停、继续、恢复或清理目标。
- [ ] 说明单步前失败不调用 `debugger_step`；单步调用开始后失败只做有限观测并人工恢复。
- [ ] 说明 `stepCallStarted=true` 只表示客户端进入单步调用边界，不表示 CE 已确认完成。
- [ ] 说明 `postStepState=unknown` 时不得直接重复运行脚本，必须先在 CE 中人工确认 RIP、线程、断点和异常/数据断点提示。
- [ ] 提供命令：

```powershell
cd D:\cebuild\ce-custom
python Scripts\step_capture_at_breakpoint.py --mode into
```

- [ ] 说明 v1 不提供 `--steps`，第二次单步必须重新人工确认并重新启动脚本。
- [ ] 说明报告退出码、时间线、TOCTOU 限制、`stopReason` 和断点快照的合同范围。
- [ ] 说明 resource/job 计数只是辅助证据，Gateway 关闭不是 CE 恢复动作。

## 验证流程

- [ ] `python -m py_compile Scripts\step_capture_at_breakpoint.py Scripts\tests\test_step_capture.py`
- [ ] `python -m unittest Scripts.tests.test_step_capture -v`
- [ ] `python -m unittest Scripts.tests.test_stacktrace_register -v`
- [ ] `python -m unittest discover -s Scripts/tests -v`
- [ ] 真实验收前只做 tools/list、instance_list、runtime、module、状态和读取类预检；合同不通过时不单步。
- [ ] 真实验收第一次只执行一次 `debugger_step(mode="into")`；单步后即使查询失败，也不自动继续、暂停、恢复或清理。
- [ ] 真实验收不得调用 `debugger_break_thread`、`debugger_continue`、`debugger_run_to`、trace/job、寄存器/断点/内存写入工具。
- [ ] 真实验收由用户人工确认 CE 的最终 RIP、停止状态、断点显示、数据断点命中情况和异常提示；脚本报告不能替代 CE UI 的底层状态确认。

## 自检

- [ ] S1：模块基址由 `module_get/module_list` 动态取得，不使用旧硬编码绝对地址。
- [ ] S2：v1 只允许一次单步，无 `--steps` 和自动再次单步语义。
- [ ] S3：用 `stepCallStarted` 区分“进入调用边界”和“收到 CE 响应”，不误报单步已完成。
- [ ] S4：报告字段和退出码已统一定义。
- [ ] S5：断点快照只声明 MCP 返回范围内的字段，不声称拥有 CE 内部完整断点属性。
- [ ] S6：单步后轮询固定兼容查询，原始 `stepping` 只做诊断。
- [ ] S7：R14/RSP 用于动态读取，RDI/RSI 只记录不解引用。
- [ ] S8：禁用真实的 `debugger_break_thread`，阶段白名单为主防线。
- [ ] S9：unsafe_lua 是单步前硬门槛。
- [ ] S10：批量内存读取按 `failed/items/value/error` 严格解析，前置失败不单步，后置只记录。
- [ ] TOCTOU、数据断点、Gateway 关闭时序、CE 临时状态和固定 Lua 残余风险均已明确记录。
- [ ] 交付边界：本计划只修订方案，不创建脚本、不调用 `debugger_step`、不改变 CE 现场。
