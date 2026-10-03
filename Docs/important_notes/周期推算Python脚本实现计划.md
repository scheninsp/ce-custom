# 周期推算 Python 原子操作实施方案

> **面向自动化执行人员：必须配套子能力：使用 superpowers:executing-plans 逐任务执行本方案。步骤使用复选框（`- [ ]`）用于进度跟踪。**

我将使用 writing-plans 能力生成完整实施方案。

**目标：** 提供可从 CMD 单独运行的 Lua 执行和原生条件执行断点添加命令；用户人工检查、Run 和推进游戏。

**架构方案：** 复用现有 MCP 客户端及固定 Lua 状态兼容查询，两个 CLI 共用一个小型执行/报告模块。原生条件通过 CE 已有断点条件界面事件设置并重新打开读回，不虚构 Lua 条件 API，不用回调筛选替代。界面后端先通过源码合同和人工现场验收，失败时保留实际结果，不自动重试、继续或删除断点。

**技术栈：** Windows、项目现有 Python 环境及标准库 argparse/unittest、CE 7.7、当前 MCP 网关、CE Lua 5.3、UTF-8 JSON、CE 原生窗体组件。

更新日期：2026-10-03（北京时间）。本次仅编写详细方案，未实现脚本、未调用 MCP、未操作 CE 或游戏。以下代码块是实施时写入文件的设计内容，不是已经安装可用的命令。

## 全局约束

- 使用中文进行对话输出。
- 使用中文进行代码注释，但是不要使用中文日志。
- python,powershell等脚本代码文件，需要在文件头部使用中文注释说明文件功能。
- 每个函数头部都要加上函数功能，以及入参与返回值的中文注释说明。
- 终端命令使用 PowerShell 语法；不要向 PowerShell 传递 Bash heredoc（例如 `<<'PATCH'`）。
- 文件修改通过专用 `apply_patch` 工具完成，不要把 `apply_patch` 补丁包装成 Bash 命令。
- 如果专用补丁工具不可用或调用失败，可以改用 PowerShell 原生命令或脚本编辑文件；采用 UTF-8 编码。
- `debugger_get_status` 的 `stateValid=false` 问题已经在 `get_stacktrace_register_at_breakpoint.py`采集流程中通过固定只读 Lua 查询解决，可以参考。
- 所有 Python 执行目录以项目目录 `D:\cebuild\ce-custom` 为基准；外部源码只读，不修改 CE 安装、MCP DLL 或游戏。
- 不执行 Run、Step、进程暂停/恢复、游戏暂停/速度控制；不自动计数或推进一周，不提交 Git、不建分支。
- 只添加执行断点；本阶段不新增 access/write 捕获、Lua 回调后端或插件接口。
- 通用 Lua 不是沙箱：助手提交的 Lua 必须人工审阅，不能通过关键词过滤宣称任意 Lua 已无副作用。

---

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

本次源码检查确认原生入口位于 `frmBreakpointlistunit.pas` 的 `miSetConditionClick`：打开 `TfrmBreakpointCondition`，读取 Simple/Complex 控件，确认后调用 Pascal 的 `setbreakpointcondition`。它不是已注册的 Lua API。详细方案使用 Lua 调用已有菜单事件，并由临时定时器在模态循环内填写/关闭条件窗口；再次打开同一窗口读回。这条路径有源码依据，但尚未在当前安装实例执行验证，不能提前宣称现场可用。不得虚构 `debug_setBreakpointCondition`。

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

## 七、文件结构与职责边界

先固化以下文件结构，再按任务执行；不拆出额外公共框架。

| 文件 | 动作 | 唯一职责 |
| --- | --- | --- |
| `Scripts/ce_lua_common.py` | 新建 | 输入文本、Lua 字符串编码、MCP 合同检查、一次执行生命周期和 JSON 报告 |
| `Scripts/ce_execute_lua.py` | 新建 | Lua CLI 参数和一次用户源码执行 |
| `Scripts/ce_native_condition.lua` | 新建 | 创建执行断点、原生界面条件设置/读回和局部 UI 资源清理 |
| `Scripts/ce_set_conditional_breakpoint.py` | 新建 | 条件 CLI、固定后端源码组装和回执检查 |
| `Scripts/tests/test_ce_execute_lua.py` | 新建 | 公共执行生命周期和 Lua CLI 离线测试 |
| `Scripts/tests/test_ce_conditional_breakpoint.py` | 新建 | 条件输入、编码、后端回执及禁止隐式动作测试 |
| `Docs/ce_lua_conditional_breakpoint.md` | 新建 | 两个 CMD 命令、故障处理和人工现场验收记录模板 |

复用但不修改：`Scripts/ce_mcp_client.py`、`Scripts/opcode_report.py`、`Scripts/get_stacktrace_register_at_breakpoint.py`。不调用 `ce_utils.run_capture`，因为该函数执行单步；其 CLI 外观只是参考。公共模块导入采集模块的函数，不执行其 `main`，也不调用要求完整堆栈工具目录的 `validate_catalog`。

实施前阅读：

- `Scripts/ce_mcp_client.py`：`McpClient(argv, timeout, log_path)`、`start/tools/call/close`、`ToolError` 和 `TransportError`。
- `Scripts/get_stacktrace_register_at_breakpoint.py`：`select_instance`、`validate_runtime`、`read_status`、`require_stopped`、`check_status_context`、`fingerprint`。
- `Scripts/opcode_report.py`：`atomic_text`。JSON 用此函数原子写入，不沿用单步 Markdown 标题。
- `Docs/mcp_debugger_status_diagnosis.md`、`Docs/stacktrace_register.md`：已完成的兼容查询和历史验收。
- `C:\Program Files\Cheat Engine\celua.txt`：debugger、Form、Component、Timer、ListView 和 MenuItem 接口。
- `D:\cebuild\cheat-engine\Cheat Engine\LuaHandler.pas`：`debug_setBreakpointForThread`、`debug_getBreakpointList`；设置函数可能没有可信成功返回，必须查列表。
- 同目录 `frmBreakpointlistunit.pas/.lfm`、`frmBreakpointConditionUnit.pas/.lfm`、`MemoryBrowserFormUnit.pas`、`debughelper.pas`：控件名、模态窗口、条件保存和读取。
- `D:\cebuild\CheatEngine.Mcp\srcs\CheatEngine.Mcp.Tools\Lua\LuaRecords.cs`：`ok/phase/error/hostEffect/returnValues/droppedOpaqueCount` 合同。部署版本以本次 `tools/list` 和响应为准。

## 八、接口、报告与失败合同

### 8.1 固定 CLI

公共参数：`--instance-id` 可选；`--gateway` 默认沿用项目网关路径；`--timeout` 正有限数、默认 30 秒；`--output` 为报告目录、默认 `Output/cycle_count`。不增加 `--no-output`，有副作用的请求必须保存证据。

Lua 命令要求 `--source` 或 `--file` 恰好一个。条件命令要求 `--address`、`--condition-type simple|complex`，以及 `--condition` 或 `--condition-file` 恰好一个；后端固定 `native-ui`，不提供 callback 切换。条件命令的内部界面等待预算为 3000 毫秒，`--timeout` 必须至少 10 秒，给模态返回、读回和报告留出余量。

输入 UTF-8/UTF-8 BOM 均接受，CRLF/CR 统一为 LF；不静默 `.strip()` 改写内容。拒绝空白文本、NUL、编码错误、超过 65536 UTF-8 字节的文本。Simple 必须为单行表达式；Lua `load('return (' .. expression .. ')', ..., 't')` 检查语法，但不执行表达式。Complex 编译原文；未返回布尔值的实际命中行为由用户检查，不伪造命中结果。

### 8.2 报告字段

报告文件名为 `lua_<UTC时间>_<随机标识>.json` 或 `condition_<UTC时间>_<随机标识>.json`；同次网关日志同前缀，避免覆盖上次实验。时间存 UTC ISO，用户展示日期使用北京时间。

```json
{
  "schemaVersion": 1,
  "operation": "condition",
  "instanceId": "ce-test",
  "request": {"address": "victoria3.exe+11FD93B", "conditionType": "complex", "source": "return true"},
  "actionAttempted": false,
  "hostEffect": "not_started",
  "baseline": {},
  "status": {},
  "luaResponse": null,
  "result": null,
  "finalOverview": null,
  "manualVerificationRequired": true,
  "error": null,
  "exitCode": 2
}
```

额外记录源码 SHA-256、开始/结束时间、最终状态和关闭网关结果。条件 `result` 的固定字段为 `ok/phase/address/conditionType/condition/created/conditionReadbackMatched/backend/error`。UI 创建的断点标记 `resourceOwner=ce-lua-untracked`，不能填成 MCP 资源 ID；临时窗体/定时器另列 UI 副作用。

退出码：0 请求完成且自动检查通过；2 未修改请求目标，前置或编译检查失败；3 已修改、运行失败、通信/现场/回执效果不确定；130 用户中断。只读兼容查询失败仍保留其原有错误证据。MCP 的 `hostEffect` 与业务 `created` 分开：Lua 已返回 `completed` 不代表业务配置成功。报告写入失败在已尝试动作后返回 3；任何路径均不自动补发请求。

## 九、逐任务实施

### 任务 1：可单独运行的 Lua 执行命令

**涉及文件：** 新建 `Scripts/ce_lua_common.py`、`Scripts/ce_execute_lua.py`、`Scripts/tests/test_ce_execute_lua.py`。

**接口依赖：**

- 输入：`McpClient(argv: list[str], timeout: float, log_path: Path | None)`；`select_instance(client, wanted)`；`validate_runtime(client, instance_id)`；`read_status(client, instance_id, *, collecting=False, compat_available=False)`。
- 输出：`read_text(source: str | None, file: Path | None) -> str`；`lua_quote(text: str) -> str`；`execute_once(client, instance_id: str, source: str, chunk_name: str, report: dict) -> dict`；`run_cli(args, operation: str, request: dict, source: str, client_factory=McpClient, result_validator=None) -> int`；`ce_execute_lua.main(argv=None, client_factory=McpClient) -> int`。`result_validator` 是只检查响应的 `(response: dict, request: dict) -> dict` 函数，不控制目标执行。

**执行步骤：**

- [ ] 先创建测试，验证文本错误在启动客户端前退出，成功只发送一次用户源码；下列核心函数写入公共模块，所有其他函数按同样中文说明格式编写。

```python
def read_text(source, file):
    """读取请求文本；入参为互斥源码和路径，返回规范化的非空 UTF-8 文本。"""
    if (source is None) == (file is None):
        raise ValueError("exactly one text input is required")
    text = source if file is None else file.read_text(encoding="utf-8-sig")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    if not text.strip() or "\0" in text or len(text.encode("utf-8")) > 65536:
        raise ValueError("invalid or oversized source text")
    return text


def lua_quote(text):
    """编码安全 Lua 字符串；入参为文本，返回按 UTF-8 字节转义的带引号字面量。"""
    return '"' + "".join(f"\\{byte:03d}" for byte in text.encode("utf-8")) + '"'


def execute_once(client, instance_id, source, chunk_name, report):
    """执行一次请求且不重试；入参为客户端、实例、源码、块名及报告，返回原始响应。"""
    report["actionAttempted"] = True
    report["hostEffect"] = "unknown"
    response = client.call("lua_execute", {
        "instanceId": instance_id, "source": source, "chunkName": chunk_name,
    })
    report["luaResponse"] = response
    report["hostEffect"] = response.get("hostEffect", "unknown")
    if response.get("ok") is not True or response.get("hostEffect") != "completed":
        raise ValueError("Lua execution failed or host effect is unconfirmed")
    if type(response.get("droppedOpaqueCount")) is not int:
        raise ValueError("invalid Lua copy metadata")
    if response["droppedOpaqueCount"] != 0:
        raise ValueError("Lua returned opaque values; result is incomplete")
    if not isinstance(response.get("returnValues"), list):
        raise ValueError("invalid Lua return values")
    return response
```

- [ ] `run_cli` 按下面顺序实现；它只是一套会话执行生命周期，不接受附加动作列表：

```text
本地校验参数、输入、网关文件与输出目录，生成唯一报告路径
创建并 start 客户端；tools() 校验本次需要的每个工具和参数名
select_instance → validate_runtime → 校验 gates.unsafeLua 为 true
Lua CLI：附加目标必须存在，但不要求 broken=true
条件 CLI：额外 require_stopped(read_status(..., compat_available=True))
写入 request、baseline 和源码散列；execute_once 只调用一次
Lua CLI：result 保存全部 returnValues，不执行用户源码第二次以“读回”
条件 CLI：调用任务 3 的业务回执校验
成功后读取 runtime_get_overview，fingerprint 必须与 baseline 一致
条件 CLI：再读 status/context，IP/SP 必须与前置现场一致；线程由固定后端核对
finally：关闭本次客户端、原子写 JSON；不删除 CE 资源
遇到连接失效不再读回，保存 unknown；输出 ASCII 转义的英文 ERROR 日志
```

工具目录仅要求 `instance_list/runtime_get_info/runtime_get_overview/lua_execute`；条件 CLI 再要求 `debugger_get_status/debugger_get_context`，不要求栈工具。复用 `validate_runtime` 返回的基线和 `fingerprint`，避免复制状态兼容源码。`ToolError` 携带已证明 `not_started` 或 Lua `phase=compile, hostEffect=not_applied` 时可返回 2；runtime 错误、超时、缺字段或响应丢失返回 3。中断返回 130，记录动作是否已尝试。

- [ ] 公共模块新增 `make_parser(description: str) -> argparse.ArgumentParser`，两个入口均使用下列完整参数定义。不要包装用户源码，不声明可以阻止用户主动写入/调用 Run；仅助手提供的源码遵守本方案限制。

```python
import argparse
from pathlib import Path
from get_stacktrace_register_at_breakpoint import DEFAULT_GATEWAY


def make_parser(description):
    """创建公共参数解析器；入参为英文描述，返回解析器。"""
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--instance-id")
    parser.add_argument("--gateway", type=Path, default=DEFAULT_GATEWAY)
    parser.add_argument("--timeout", type=float, default=30)
    parser.add_argument("--output", type=Path, default=Path("Output/cycle_count"))
    return parser
```

Lua CLI 的入口代码如下，模块文件头先写中文功能说明；文件末尾采用 `if __name__ == "__main__": sys.exit(main())`。argparse 参数错误退出 2；读取失败在尚未启动客户端时以英文日志退出 2。

```python
import sys
from pathlib import Path
from ce_mcp_client import McpClient
from ce_lua_common import make_parser, read_text, run_cli


def main(argv=None, client_factory=McpClient):
    """执行一次用户 Lua；入参为命令参数和客户端工厂，返回退出码。"""
    parser = make_parser("Execute one Cheat Engine Lua request")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--source")
    group.add_argument("--file", type=Path)
    args = parser.parse_args(argv)
    try:
        source = read_text(args.source, args.file)
    except KeyboardInterrupt:
        return 130
    except (OSError, UnicodeError, ValueError) as error:
        print("ERROR: " + ascii(str(error)), file=sys.stderr)
        return 2
    request = {"source": source, "sourceFile": str(args.file) if args.file else None}
    return run_cli(args, "lua", request, source, client_factory=client_factory)
```
- [ ] 增加如下可直接运行的核心测试；测试文件头使用中文功能说明，导入方式沿用 `Scripts/tests` 的 `sys.path` 模式。

```python
import unittest
from unittest.mock import Mock
from ce_mcp_client import TransportError
from ce_lua_common import execute_once, lua_quote


class LuaExecutionTests(unittest.TestCase):
    def test_execute_once(self):
        """验证请求只执行一次；无入参和返回值。"""
        client = Mock()
        client.call.return_value = {
            "ok": True, "hostEffect": "completed", "returnValues": [5], "droppedOpaqueCount": 0,
        }
        report = {}
        response = execute_once(client, "ce-test", "return 2 + 3", "cycle_user_lua", report)
        self.assertEqual(response["returnValues"], [5])
        self.assertTrue(report["actionAttempted"])
        client.call.assert_called_once_with("lua_execute", {
            "instanceId": "ce-test", "source": "return 2 + 3", "chunkName": "cycle_user_lua",
        })

    def test_timeout_does_not_retry(self):
        """验证超时不重发；无入参和返回值。"""
        client = Mock()
        client.call.side_effect = TransportError("MCP request timed out")
        report = {}
        with self.assertRaises(TransportError):
            execute_once(client, "ce-test", "return 5", "cycle_user_lua", report)
        self.assertEqual(client.call.call_count, 1)
        self.assertEqual(report["hostEffect"], "unknown")

    def test_utf8_quote(self):
        """验证特殊字符按字节编码；无入参和返回值。"""
        encoded = lua_quote('"\\\n木')
        self.assertEqual(encoded, '"\\034\\092\\010\\230\\156\\168"')
```

用 Fake 客户端补齐参数表驱动用例：空文件/NUL/乱码/65537 字节、零/负/NaN/inf 超时、不完整发现/多实例/目标关闭/unsafeLua=false/缺工具、编译失败/运行失败/丢弃值/非列表、目标指纹变化、日志或报告写入失败、客户端关闭失败和中断。每例断言退出码、报告字段、关闭次数和请求次数。Fake 的 `call` 对未列工具直接抛 AssertionError，使隐藏调试动作导致测试失败。

- [ ] 执行 `python -m unittest discover -s Scripts\tests -p "test_ce_execute_lua.py" -v`，先确认新用例失败于模块缺失，再实现至通过。
- [ ] Lua 命令交付评审：从 CMD 可执行 `return 2 + 3` 并保存返回 5 的报告；真实 CE 验收由用户确认后执行，不附带任何 Run。

### 任务 2：原生条件 UI 后端及失败边界

**涉及文件：** 新建 `Scripts/ce_native_condition.lua`；新建 `Scripts/tests/test_ce_conditional_breakpoint.py` 的后端合同部分。

**接口依赖：** 输入为 Python 前缀定义的局部 `request={address=<文本>, conditionType=<simple或complex>, condition=<文本>}`；输出为第 8.2 节规定的单个 Lua 对象。依赖 CE 文档中的原生组件接口，不依赖任务 1 的任何新 Lua 全局函数。

**执行步骤：**

- [ ] 写入下列完整核心后端。前缀与文件内容拼接为同一 chunk，使 `request` 保持局部变量。所有名称/控件均来自本次检查的 CE 源码；不得用数字坐标、中文标题、CE 内部地址偏移或调用 Pascal 私有方法代替。

```lua
-- 添加原生条件执行断点并读回；不继续目标，不覆盖或删除已有断点。
local result = {
    ok=false, phase='preflight', created=false, conditionReadbackMatched=false,
    backend='native-ui', conditionType=request.conditionType, condition=request.condition,
}
local timer = nil
local ownedDialog = nil

-- 查找唯一指定类窗体；入参为类名，返回窗体或 nil。
local function findForm(className)
    local found = nil
    for index = 0, getFormCount() - 1 do
        local form = getForm(index)
        if form.ClassName == className then
            assert(found == nil, 'Multiple matching forms')
            found = form
        end
    end
    return found
end

-- 读取必需组件；入参为窗体和组件名，返回组件，缺失时失败。
local function component(form, name)
    local control = form.findComponentByName(name)
    assert(control ~= nil, 'Missing native component: ' .. name)
    return control
end

-- 在模态循环中设置或只读条件；入参为菜单和是否写入，返回读回对象。
local function visitCondition(menu, write)
    assert(findForm('TfrmBreakpointCondition') == nil, 'Condition dialog already open')
    local observed = nil
    local failure = nil
    local began = getTickCount()
    timer = createTimer(nil, false)
    timer.Interval = 50
    -- 驱动本次条件窗口；入参为定时器，无返回值。
    timer.OnTimer = function(sender)
        local handled, message = pcall(function()
            local dialog = findForm('TfrmBreakpointCondition')
            if dialog == nil then
                assert(getTickCount() - began < 3000, 'Native dialog deadline exceeded')
                return
            end
            ownedDialog = dialog
            sender.Enabled = false
            local easy = component(dialog, 'rbEasy')
            local complex = component(dialog, 'rbComplex')
            local expression = component(dialog, 'edtEasy')
            local script = component(dialog, 'mComplex')
            if write then
                easy.Checked = request.conditionType == 'simple'
                complex.Checked = not easy.Checked
                if easy.Checked then expression.Text = request.condition
                else script.Text = request.condition end
            end
            observed = {
                conditionType=easy.Checked and 'simple' or 'complex',
                condition=easy.Checked and expression.Text or script.Text,
            }
            dialog.ModalResult = write and 1 or 2
        end)
        if not handled then
            failure = tostring(message)
            sender.Enabled = false
            if ownedDialog ~= nil then ownedDialog.ModalResult = 2 end
        end
    end
    timer.Enabled = true
    local clicked, clickError = pcall(function() menu.doClick() end)
    timer.Enabled = false
    timer.destroy()
    timer = nil
    ownedDialog = nil
    assert(clicked, tostring(clickError))
    assert(failure == nil, failure)
    assert(observed ~= nil, 'Native dialog did not return condition')
    return observed
end

local completed, errorText = pcall(function()
    assert(debug_isDebugging() == true, 'Debugger is not attached')
    local before = debug_getCurrentContextTable(false)
    assert(type(before) == 'table', 'No stopped context')
    assert(targetIs64Bit() == true, '64-bit target required')
    assert(request.conditionType == 'simple' or request.conditionType == 'complex', 'Invalid condition type')
    local address = getAddressSafe(request.address)
    assert(math.type(address) == 'integer' and address > 0, 'Cannot resolve address')
    result.address = string.format('%X', address)
    local compiled = request.conditionType == 'simple'
        and ('return (' .. request.condition .. ')') or request.condition
    local chunk, compileError = load(compiled, 'cycle_condition_compile', 't', _G)
    assert(chunk ~= nil, tostring(compileError))
    assert(findForm('TfrmBreakpointCondition') == nil, 'Condition dialog already open')
    for _, existing in ipairs(debug_getBreakpointList() or {}) do
        assert(existing ~= address, 'Breakpoint address already exists')
    end
    local list = findForm('TfrmBreakpointlist')
    if list == nil then
        component(getMemoryViewForm(), 'Breakpointlist1').doClick()
        list = findForm('TfrmBreakpointlist')
    end
    assert(list ~= nil, 'Breakpoint list unavailable')
    local view = component(list, 'ListView1')
    local refresh = component(list, 'Timer1').OnTimer
    local menu = component(list, 'miSetCondition')
    assert(type(refresh) == 'function', 'Breakpoint refresh unavailable')
    assert(type(createTimer) == 'function', 'Timer API unavailable')
    result.phase = 'create-attempted'
    debug_setBreakpoint(address)
    local matches = 0
    for _, existing in ipairs(debug_getBreakpointList() or {}) do
        if existing == address then matches = matches + 1 end
    end
    assert(matches == 1, 'New breakpoint was not uniquely registered')
    result.created = true
    refresh(component(list, 'Timer1'))
    local selected = nil
    for index = 0, view.Items.Count - 1 do
        local item = view.Items[index]
        if getAddressSafe(item.Caption) == address then
            assert(selected == nil, 'Ambiguous native breakpoint row')
            selected = item
        end
    end
    assert(selected ~= nil, 'Native breakpoint row unavailable')
    for index = 0, view.Items.Count - 1 do view.Items[index].Selected = false end
    selected.Selected = true
    result.phase = 'condition-write-attempted'
    visitCondition(menu, true)
    result.phase = 'condition-readback'
    local readback = visitCondition(menu, false)
    local normalized = readback.condition:gsub('\r\n', '\n'):gsub('\r', '\n')
    assert(readback.conditionType == request.conditionType, 'Condition type mismatch')
    assert(normalized == request.condition, 'Condition text mismatch')
    result.conditionReadbackMatched = true
    local after = debug_getCurrentContextTable(false)
    assert(type(after) == 'table', 'Stopped context lost')
    for _, name in ipairs({'RIP', 'RSP', 'THREADID'}) do
        assert(before[name] ~= nil and before[name] == after[name], 'Stopped context changed')
    end
    result.threadIdBefore = string.format('%X', before.THREADID)
    result.threadIdAfter = string.format('%X', after.THREADID)
    result.phase = 'completed'
    result.ok = true
end)
if timer ~= nil then timer.Enabled = false; timer.destroy(); timer = nil end
if not completed then result.error = tostring(errorText) end
return result
```

- [ ] 源码静态检查与当前安装 UI 只读探查：控件名、类名、`Timer1.OnTimer` 返回函数、`getTickCount`、`createTimer` 和菜单 `doClick` 均须存在；此步骤不创建断点。探查源码以 `return` 普通对象返回各项能力，不返回 userdata，执行通过 Lua CLI，不另建探查命令。

探查时用户先打开 CE 断点列表，再通过 `--file` 执行下列文本；只读取现有组件，不点击菜单或创建窗体。结果缺失任一能力即停止后端验收。

```lua
-- 只读核对原生断点界面合同；不设置断点或触发窗口事件。
local list = nil
for index = 0, getFormCount() - 1 do
    local form = getForm(index)
    if form.ClassName == 'TfrmBreakpointlist' then
        assert(list == nil, 'Multiple breakpoint lists')
        list = form
    end
end
assert(list ~= nil, 'Open the breakpoint list before probing')
local view = list.findComponentByName('ListView1')
local refresh = list.findComponentByName('Timer1')
local menu = list.findComponentByName('miSetCondition')
local memory = getMemoryViewForm()
return {
    breakpointList=true,
    listView=view ~= nil,
    refreshEvent=refresh ~= nil and type(refresh.OnTimer) == 'function',
    conditionMenu=menu ~= nil,
    openListMenu=memory.findComponentByName('Breakpointlist1') ~= nil,
    timerApi=type(createTimer) == 'function',
    tickApi=type(getTickCount) == 'function',
}
```
- [ ] 检查源码注册和源码版本差异。上述 `debug_setBreakpoint(address)` 使用用户现有调试器默认断点方法，不传不存在的参数、不启动新调试器。停止现场已由前置查询证明；实际函数可能吞异常，列表唯一存在才允许 `created=true`。
- [ ] 离线测试读取后端文件，断言包含创建/查重/保存/读回步骤，且不含 `debug_continueFromBreakpoint`、`debugger_onBreakpoint`、`debug_removeBreakpoint`、`writeInteger`。这是源码合同测试，不是 Lua 或真实 UI 功能通过的证明。
- [ ] 现场验收门：用户在安全的已停止现场提供一个没有已有断点的地址，确认运行添加命令。成功应保存原生条件且保持原停止现场；用户再打开条件窗口核对。失败不得改用 callback，不自动删除残留断点；Lua CLI 仍可独立交付。

**重要失败边界：** 原生菜单内部 `ShowModal` 是嵌套消息循环。定时器仅在 CE 正常调度且出现预期窗体时能取消本次窗口；3000 毫秒不是强制取消保证。如果当前安装不调度定时器、出现其他模态窗口或主线程冻结，MCP 超时只能报告 unknown，不能从 Python 保证解除窗口。关闭网关也不能取消已进入 CE 的 Lua。报告必须提醒用户检查窗口和残留普通断点；用户先处理模态窗口再重试。不得把这条 UI 路径描述成无风险、严格原子或已现场验证。

### 任务 3：条件断点 CLI、回执验证和离线测试

**涉及文件：** 新建 `Scripts/ce_set_conditional_breakpoint.py`；扩充 `Scripts/tests/test_ce_conditional_breakpoint.py`；只在确有接口需要时扩充 `Scripts/ce_lua_common.py` 的条件分支。

**接口依赖：** 输入为任务 1 的 `read_text/lua_quote/run_cli`；固定文件 `Scripts/ce_native_condition.lua`。输出为 `build_condition_source(address: str, condition_type: str, condition: str) -> str`、`validate_condition_result(response: dict, request: dict) -> dict`、`main(argv=None, client_factory=McpClient) -> int`。

**执行步骤：**

- [ ] 先添加源码生成与回执测试，再实现下列函数。地址仅允许 1–16 位十六进制绝对地址，或 `victoria3.exe+` 加 1–16 位十六进制 RVA；拒绝绝对地址 0、空白、分号、其他模块和任意 CE 表达式。数值绝对地址可去除 `0x` 后标准化；RVA 保留表达式由 CE 解析，不能硬编码历史模块基址。

```python
def build_condition_source(address, condition_type, condition):
    """构造固定后端请求；入参为地址、条件类型和文本，返回安全编码的 Lua 源码。"""
    absolute = re.fullmatch(r"(?:0[xX])?([0-9a-fA-F]{1,16})", address)
    relative = re.fullmatch(r"victoria3\.exe\+([0-9a-fA-F]{1,16})", address)
    if not (absolute or relative) or (absolute and int(absolute[1], 16) == 0):
        raise ValueError("invalid breakpoint address")
    if condition_type not in {"simple", "complex"}:
        raise ValueError("invalid condition type")
    if condition_type == "simple" and "\n" in condition:
        raise ValueError("simple condition must be a single expression")
    normalized = f"{int(absolute[1], 16):X}" if absolute else address
    prefix = (
        "local request = {address=" + lua_quote(normalized)
        + ",conditionType=" + lua_quote(condition_type)
        + ",condition=" + lua_quote(condition) + "}\n"
    )
    backend = Path(__file__).with_name("ce_native_condition.lua").read_text(encoding="utf-8")
    source = prefix + backend
    if len(source.encode("utf-8")) > 65536:
        raise ValueError("assembled Lua source exceeds the local limit")
    return source


def validate_condition_result(response, request):
    """验证条件业务回执；入参为 Lua 响应和请求，返回成功业务对象，否则抛出异常。"""
    values = response["returnValues"]
    if len(values) != 1 or not isinstance(values[0], dict):
        raise ValueError("expected one native condition result")
    result = values[0]
    if any(result.get(key) is not True for key in ("ok", "created", "conditionReadbackMatched")):
        raise ValueError("native condition setup is incomplete")
    if result.get("backend") != "native-ui" or result.get("phase") != "completed":
        raise ValueError("unexpected condition backend or phase")
    if result.get("conditionType") != request["conditionType"] or result.get("condition") != request["source"]:
        raise ValueError("condition receipt differs from request")
    if not isinstance(result.get("address"), str) or not re.fullmatch(r"[0-9A-F]{1,16}", result["address"]):
        raise ValueError("invalid resolved breakpoint address")
    thread_before = result.get("threadIdBefore")
    if not isinstance(thread_before, str) or not re.fullmatch(r"[0-9A-F]{1,16}", thread_before):
        raise ValueError("invalid stopped thread receipt")
    if result.get("threadIdAfter") != thread_before:
        raise ValueError("stopped thread changed")
    return result
```

公共执行层在业务校验前保存原始返回对象；失败也必须保留 `phase/created/error`。若后端返回 `ok=false, phase=preflight, created=false`，明确无断点创建且只有 UI 前置影响时返回 2；从 `create-attempted` 起任何失败均返回 3，即使 `created=false` 也不能推断没有残留。其余缺字段或错误结构一律返回 3。成功报告仍标明 `manualVerificationRequired=true`。

- [ ] 条件前置：使用 `read_status(..., compat_available=True)` 和 `require_stopped`，从 `debugger_get_context(includeExtraRegisters=False)` 保存 RIP/RSP，核对兼容查询 IP/SP；要求 processName 为 `victoria3.exe`、pointerSize 为 8。后置比较同一 fingerprint 和停止现场。不要复用要求 `includesExtraRegisters=True` 的 `validate_context`；只验证本次请求的必要字段。线程由固定 Lua 后端前后读取 `debug_getCurrentContextTable(false).THREADID` 并在回执中比较，不假定 MCP 状态/寄存器响应有独立 threadId 字段；不需要读取整份栈，不执行单步。
- [ ] 添加以下核心回执测试，测试采用 `unittest` 和 `copy.deepcopy`，在测试文件导入新增函数；不连接真实 CE。

```python
import copy
import unittest
from ce_set_conditional_breakpoint import build_condition_source, validate_condition_result


class ConditionReceiptTests(unittest.TestCase):
    def test_receipt_requires_real_condition_readback(self):
        """验证普通断点不被当作条件成功；无入参和返回值。"""
        request = {"conditionType": "complex", "source": "return true"}
        result = {
            "ok": True, "created": True, "conditionReadbackMatched": True,
            "backend": "native-ui", "phase": "completed", "address": "7FF777CED93B",
            "conditionType": "complex", "condition": "return true",
            "threadIdBefore": "1234", "threadIdAfter": "1234",
        }
        self.assertEqual(validate_condition_result({"returnValues": [result]}, request), result)
        for key in ("ok", "created", "conditionReadbackMatched"):
            invalid = copy.deepcopy(result)
            invalid[key] = False
            with self.subTest(key=key), self.assertRaises(ValueError):
                validate_condition_result({"returnValues": [invalid]}, request)

    def test_injected_address_is_rejected(self):
        """验证地址不能注入 Lua；无入参和返回值。"""
        with self.assertRaises(ValueError):
            build_condition_source('victoria3.exe+11FD93B;return true', 'complex', 'return true')
```

- [ ] 用 Fake 客户端完整驱动 `main`：正常状态与已知兼容错误两条路径均能成功；非已知错误不发送业务 Lua；同地址冲突/语法错误返回 2；创建后无列表条目/多条/条件读回不同/控件缺失返回 3；通信超时只请求一次；用户中断/进程切换/线程或 RIP 变化不能返回 0。Fake 按 chunkName 区分固定状态查询和条件配置请求，不能把状态查询算作重复业务动作。

条件 CLI 的入口完整定义如下；模块内同时包含前述 `build_condition_source` 和 `validate_condition_result`，导入 `re`、`lua_quote`；文件末尾同样调用 `sys.exit(main())`。

```python
import sys
from pathlib import Path
from ce_mcp_client import McpClient
from ce_lua_common import make_parser, read_text, run_cli


def main(argv=None, client_factory=McpClient):
    """添加一个原生条件断点；入参为命令参数和客户端工厂，返回退出码。"""
    parser = make_parser("Add one native conditional execute breakpoint")
    parser.add_argument("--address", required=True)
    parser.add_argument("--condition-type", choices=("simple", "complex"), required=True)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--condition")
    group.add_argument("--condition-file", type=Path)
    args = parser.parse_args(argv)
    try:
        condition = read_text(args.condition, args.condition_file)
        source = build_condition_source(args.address, args.condition_type, condition)
    except KeyboardInterrupt:
        return 130
    except (OSError, UnicodeError, ValueError) as error:
        print("ERROR: " + ascii(str(error)), file=sys.stderr)
        return 2
    request = {"address": args.address, "conditionType": args.condition_type, "source": condition}
    return run_cli(args, "condition", request, source, client_factory=client_factory,
                   result_validator=validate_condition_result)
```
- [ ] 对每个 Fake 测试统一断言：无 `debugger_continue/debugger_step/process_set_paused/debugger_start_capture` 工具调用；无自动删除；实例 ID 精确匹配；状态查询源码等于已导入常量。日志通过捕获 stderr 断言英文消息，用户条件原文只保存在 UTF-8 报告或以 ASCII 转义日志展示。
- [ ] 执行 `python -m unittest discover -s Scripts\tests -p "test_ce_conditional_breakpoint.py" -v`。本任务完成不意味着真实 UI 或命中已验收，必须区分 offline 与 live。

### 任务 4：独立 CMD 验收指南与回归

**涉及文件：** 新建 `Docs/ce_lua_conditional_breakpoint.md`。不修改计数指南以免把本阶段误写成自动统计。

**接口依赖：** 两个 `main`、固定 native-ui 后端、JSON 报告合同。输出为用户可以逐条执行的命令和验收记录，不新增可执行脚本。

**执行步骤：**

- [ ] 文档写明“新增命令现在是否已实现”“状态兼容已复用”“UI 后端是否通过当前实例验证”，不得以历史采集成功替代本次添加条件验收。
- [ ] 先执行离线验证，不连接 CE、不推进游戏：

```text
python -m unittest discover -s Scripts\tests -p "test_ce_execute_lua.py" -v
python -m unittest discover -s Scripts\tests -p "test_ce_conditional_breakpoint.py" -v
python -m unittest discover -s Scripts\tests -p "test_stacktrace_register.py" -v
python -m unittest discover -s Scripts\tests -v
python -m py_compile Scripts\ce_lua_common.py Scripts\ce_execute_lua.py Scripts\ce_set_conditional_breakpoint.py Scripts\tests\test_ce_execute_lua.py Scripts\tests\test_ce_conditional_breakpoint.py
```

只修本任务造成的回归；无关测试失败列入报告，不扩大范围。

- [ ] CMD 验收阶段由用户确认操作地址和已停止现场；先做最小算术，再添加一个断点，不默认一次创建两个：

```text
cd /d D:\cebuild\ce-custom
python Scripts\ce_execute_lua.py --source "return 2 + 3" --output Output\cycle_count
python Scripts\ce_set_conditional_breakpoint.py --address "victoria3.exe+11FD93B" --condition-type complex --condition "return RCX == 0x3A484D9F8E8 and readInteger(RDX + 0x10) == 10" --output Output\cycle_count
```

上面的州表地址是历史示例，只有用户本次确认有效才允许执行；10 为木材 ID，不是硬木。更稳妥的 Complex 条件文件内容如下，存放到用户指定 UTF-8 文件，以 `--condition-file` 输入；该文件不是本计划自动创建的实验配置。

```lua
-- 筛选用户已确认的州商品表和商品；不计数，不自动继续。
if RCX ~= 0x3A484D9F8E8 then return false end
assert(math.type(RDX) == 'integer' and RDX ~= 0, 'Invalid goods pointer')
local goodsId = readInteger(RDX + 0x10)
assert(goodsId ~= nil, 'Cannot read goods ID')
return goodsId == 10
```

读取失败时应显示条件执行错误，不能声称这是正常未匹配；用户负责检查 CE 对条件异常的呈现。只有成功读取且目标相符时返回 true。仅演示寄存器条件筛选，不新增反编译伪代码函数。

- [ ] 人工验收逐项记录：实例/PID、游戏版本、当前州表/商品 ID、请求报告路径、断点地址、条件类型/原文、添加后 RIP/RSP 未变化、CE 界面读回正确。随后**用户**点击 Run，确认游戏已解除暂停、日期推进并在匹配断点停下。记录命中时 RCX、RDX+0x10、游戏日期；若未命中也记录观察时段，不把它算作“本周零次调整”。
- [ ] 第一个断点通过人工检查后，用户决定是否以相同方式在 `victoria3.exe+11FAF69` 添加第二个。用户检查槽位、默认断点方法和其他已有断点对命中的影响；脚本不禁用已有断点。
- [ ] 使用假客户端验收同地址冲突、部分配置失败和超时，无需故意让真实游戏冻结。现场残留断点由用户人工清理；没有脚本自动清理或恢复步骤。

## 十、评审检查点和完成判据

1. 任务 1 评审：Lua CLI 能独立运行，输入/返回/失败报告可信；不必等待原生后端即可交付。
2. 任务 2 评审：原生 UI 入口有源码证据，风险和部分完成状态透明；当前实例不支持则明确拒绝，不提供冒充原生条件的替代。
3. 任务 3 评审：条件请求只执行一次，条件保存并读回，兼容状态复用，所有异常保留证据。
4. 任务 4 评审：离线回归与人工现场验收分开；用户负责检查、Run、游戏推进和命中观察。

最终交付只有两个 CLI、一份专用公共模块、一份原生 Lua 后端、两份测试及命令说明。不包含自动一周计数结论。只有当前实例真实设置/读回及用户命中验收均通过，才能写“条件断点功能验收完成”；仅离线通过时应明确标注这一限制。

方案自检结果：已覆盖两个原子操作、用户分工、原生条件限制、已解决状态兼容复用、文件职责、精确接口、CMD 验证、失败不重试和人工验收。未将插件根因修复、自动 Run/时钟/计数纳入任务；所有示例地址须用户重新确认；未声称本次操作了 CE。
