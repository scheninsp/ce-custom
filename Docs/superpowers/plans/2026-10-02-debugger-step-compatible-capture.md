# 调试器兼容单步采集实施方案
> **面向自动化执行人员：必须配套子能力：使用 superpowers:executing-plans 逐任务执行本方案。步骤使用复选框（`- [ ]`）用于进度跟踪。**
**目标：** 通过 Python 封装 MCP 的 `debugger_step`，使用已验证的固定 Lua 状态兼容查询确认单步前后停止现场，并在指定的 Victoria 3 指令边界采集寄存器、栈和字段信息。
**架构方案：** 复用 `Scripts/get_stacktrace_register_at_breakpoint.py` 中的固定 Lua 兼容查询、会话指纹和现场校验，不再把原生 `debugger_get_status` 的失败结果直接当作未停止。新增独立的单步采集脚本，仅允许固定的单步模式和只读采集接口；每次单步后轮询兼容状态，确认 RIP 到达预期地址或明确记录分支路径，然后采集寄存器和目标内存。脚本不设置、删除或移动用户断点，不修改寄存器，不执行目标 Lua。
**技术栈：** Python 3.11+ 标准库、现有 `McpClient`、Cheat Engine MCP `debugger_step`、固定 `lua_execute` 状态查询、MCP 调试器只读工具、JSON/UTF-8 Markdown。

## 全局约束
- 使用中文进行对话输出。
- 使用中文进行代码注释，但是不要使用中文日志。
- python,powershell等脚本代码文件，需要在文件头部使用中文注释说明文件功能。
- 每个函数头部都要加上函数功能，以及入参与返回值的中文注释说明。
- 不修改 `D:\cebuild\CheatEngine.Mcp` 源码或部署 DLL。
- 不设置、删除、启用、禁用或移动用户断点；不写入目标内存；不调用 `debugger_continue`；不调用 `debugger_set_register`。
- 单步工具是有副作用的：只在用户明确要求执行单步时调用 `debugger_step`，默认使用 `mode="into"`，并支持 `mode="over"` 作为显式选项。
- `debugger_step` 的调用后，必须使用固定 Lua 查询确认 `debug_isDebugging()` 和 `debug_getCurrentContextTable(false)` 仍证明线程已停止；不能只依赖 `debugger_get_status`。
- 只使用目标进程当前模块基址解析的绝对地址；任何地址命中都必须同时校验 PID、runtime epoch、selection epoch、线程 ID、RSP 和候选指针。
- 单步失败、状态无法确认、目标进程变化、线程变化、RIP 非预期或断点列表变化时，立即停止后续单步并保留报告；不得自动恢复运行。
- Gateway 必须在 `finally` 中关闭；报告使用原子写入，失败不能覆盖已有报告。

---

## 文件结构和职责

| 文件 | 职责 |
|---|---|
| `Scripts/step_capture_at_breakpoint.py` | 新增单步采集 CLI；固定路线、兼容状态轮询、现场快照、内存读取和 Markdown 报告 |
| `Scripts/tests/test_step_capture.py` | 使用假 MCP 客户端测试工具目录、兼容状态、单步返回、预期 RIP、分支失败、现场漂移和资源清理 |
| `Docs/step_capture.md` | 说明运行前提、单步路线、失败处理和报告字段 |
| `Docs/superpowers/plans/2026-10-02-debugger-step-compatible-capture.md` | 本实施方案 |

不修改现有 `Scripts/get_stacktrace_register_at_breakpoint.py`；通过导入其固定常量和校验函数，避免复制兼容查询代码。

## 接口合同

### `step_capture_at_breakpoint.py`

```python
def parse_hex_address(value: str) -> int:
    """解析无前缀或带 0x 的十六进制地址；参数为地址文本，返回非零地址整数。"""

def read_fixed_status(client, instance_id: str, *, compat_available: bool) -> dict:
    """读取原生或固定 Lua 兼容停止状态；参数为客户端、实例 ID 和能力标记，返回已校验状态。"""

def require_step_stopped(status: dict, expected_pid: int, expected_epoch: int) -> None:
    """校验单步后目标仍停止且会话未变化；参数为状态、PID 和 runtime epoch，失败时抛出 CaptureError。"""

def call_step(client, instance_id: str, mode: str) -> dict:
    """执行一次明确模式的单步；参数为 MCP 客户端、实例 ID 和 into/over，返回单步受理结果。"""

def wait_for_stopped(client, instance_id: str, *, timeout: float, interval: float) -> dict:
    """轮询固定状态直到停止或超时；参数为客户端、实例、超时和轮询间隔，返回停止状态。"""

def read_context_and_memory(client, instance_id: str, context: dict, memory_items: list[dict]) -> dict:
    """读取寄存器与固定内存字段；参数为实例、当前上下文和读取项，返回组合快照。"""

def run_capture(argv: list[str]) -> int:
    """执行单步采集路线并生成报告；参数为命令行参数，返回进程退出码。"""
```

### MCP 调用限制

允许调用：

- `instance_list`
- `tools/list`
- `runtime_get_info`
- `runtime_get_overview`
- `debugger_get_status`（仅作为原始错误证据）
- `debugger_get_context`
- `debugger_list_breakpoints`
- `memory_read_batch`
- `code_disassemble`
- `lua_execute`（只能发送导入的固定 `STATUS_COMPAT_SOURCE`，不接收用户源码）
- `debugger_step`

禁止调用：

- `debugger_continue`
- `debugger_set_register`
- `debugger_set_breakpoint`
- `debugger_delete_breakpoint`
- `debugger_run_to`
- `lua_execute` 的任意用户源码
- 任何内存写入、Auto Assembler、注入或目标代码执行接口

## 采集路线

默认路线使用当前用户现场和最近的指令边界：

```text
victoria3.exe+11FD5C9  mov eax,[r14+1D58]  当前断点
        │ debugger_step(mode="into")
        ▼
victoria3.exe+11FD5D0  mov [rsp+50],eax
        │ 采集寄存器和 [RSP+0x50]、[RSP+0x330]
        │ debugger_step(mode="into")
        ▼
victoria3.exe+11FD5D4  mov rcx,[rdi+F8]
        │ 可选单步；只执行普通寄存器读取
        │ debugger_step(mode="into")
        ▼
victoria3.exe+11FD5DB  mov rax,[rcx]
        │ debugger_step(mode="into")
        ▼
victoria3.exe+11FD5DE  call qword ptr [rax]
        │ 默认不跨 call；使用 mode="over" 只作为用户显式指定的下一路线
```

默认 CLI 只执行第一步并在 `+11FD5D0` 停止。使用 `--steps 2` 停止在 `+11FD5D4`。使用 `--steps 4 --mode over` 时，前四步全部使用 `over`，并在每步后确认 RIP；如果实际目标不是预期地址，脚本立即退出并记录现场。

这里的“步骤数”表示从当前停止指令开始调用多少次 `debugger_step`，不是字节数。脚本不尝试跨越 `call`，除非用户明确传入 `--mode over` 且路线预期包含该 call。

## 报告字段

报告必须包含：

- `captureStartedAt`、`captureFinishedAt`；
- instance ID、PID、进程名、模块基址、runtime epoch、selection epoch；
- 起始断点列表及每一步之后的断点列表；
- 每一步的 `mode`、MCP 单步返回、兼容状态原始错误和 Lua 状态；
- 每一步的 RIP、RSP、RBP、R14、RDI、RSI、THREADID、EFLAGS；
- 预期 RIP、实际 RIP、是否匹配；
- 当前指令窗口 `code_disassemble`；
- `[RSP+0x50]`、`[RSP+0x330]`、`[R14+0x1D58]`、`[R14+0x1D5C]` 的读取结果；
- 前后断点列表是否完全一致；
- 失败原因和退出码。

现场判定规则：

1. 起始 `RIP` 必须是 `victoria3.exe+11FD5C9`，否则拒绝执行单步。
2. 每次单步后，兼容状态必须是 `stateValid=true`、`attached=true`、`broken=true`，且 `instructionPointer` 与 `debugger_get_context` 的 RIP 一致。
3. 每次单步后必须保持同一 PID、runtime epoch、selection epoch、pointer size 和 THREADID；THREADID 变化时停止并报告，不自动猜测线程迁移。
4. 预期路线为 `+11FD5D0`、`+11FD5D4`、`+11FD5DB`、`+11FD5DE`；任一偏离都停止后续采集。
5. `[RSP+0x50]` 只能在执行 `+11FD5D0` 后验证；在更早位置读取该槽位不能当作本次字段复制结果。
6. `R14+0x1D58` 和 `R14+0x1D5C` 的地址按每一步现场 R14 动态计算，不能硬编码当前对象地址。
7. 数据断点地址属于用户断点，脚本只读列表，不删除或重新设置；断点列表变化立即停止。

## 采集流程

### 任务 1：新增单步脚本

**涉及文件：** 新建 `Scripts/step_capture_at_breakpoint.py`。

**接口依赖：** `McpClient`、`STATUS_COMPAT_SOURCE`、`STATUS_COMPAT_CHUNK`、`field`、`normalize_address`、`CaptureError`、`atomic_text`；输出本方案规定的 JSON/Markdown 报告。

**执行步骤：**

- [ ] 编写文件头中文功能注释，并从 `get_stacktrace_register_at_breakpoint` 导入兼容查询常量和安全校验函数；不得复制 Lua 字符串。
- [ ] 定义常量：目标进程名 `victoria3`、模块名 `victoria3.exe`、起始 RVA `0x11FD5C9`、预期 RVA 列表 `[0x11FD5D0, 0x11FD5D4, 0x11FD5DB, 0x11FD5DE]`、默认步骤数 `1`、默认超时 `10` 秒、轮询间隔 `0.05` 秒。
- [ ] 启动前调用 `tools()`，检查 `debugger_step` 的 schema 必须包含 `instanceId`、`mode`，且 mode enum 必须包含 `into`、`over`；检查固定 Lua 查询需要的 `instanceId`、`source`、`chunkName`；缺失能力退出 2，不调用单步。
- [ ] 调用 `instance_list`、`runtime_get_info`、`runtime_get_overview`，只允许选择唯一实例并校验 `victoria3`、64 位目标；记录 PID、epoch、selectionEpoch、pointerSize 和资源计数。
- [ ] 调用 `debugger_list_breakpoints` 与兼容状态查询；要求起始 RIP 为当前模块基址加 `0x11FD5C9`，并保存初始断点数组，断点数组不可排序或改写。
- [ ] 起始状态不满足 `stateValid/attached/broken` 时，只有固定 Lua 查询明确证明停止才继续；固定查询错误、上下文缺少 RIP/RSP、原生状态与上下文冲突时退出 2 或 3，绝不调用 `debugger_step`。
- [ ] 每次单步前重新获取兼容状态和上下文；确认 PID、epoch、selectionEpoch、pointer size、THREADID 未变化；确认当前 RIP 等于路线中的前一地址。
- [ ] 调用：

```python
result = client.call("debugger_step", {
    "instanceId": instance_id,
    "mode": args.mode,
})
```

  将返回结果原样记录；工具错误按 `hostEffect` 分类，状态不明时退出 3。
- [ ] 单步返回后使用轮询循环调用固定兼容状态，最多等待 `--timeout` 秒；`stepping=true` 或兼容查询未证明 stopped 时继续等待；超时退出 3，不调用 continue。
- [ ] 停止后调用 `debugger_get_context`、`debugger_list_breakpoints`、`runtime_get_overview`；核对 RIP 为预期下一地址，断点列表与初始列表完全相同，PID/epoch/selectionEpoch/THREADID 保持一致。
- [ ] 仅当 RIP 为 `+11FD5D0` 或更后对应路线时，动态生成内存读取项：

```python
items = [
    {"address": f"{rsp + 0x50:X}", "valueType": "int32"},
    {"address": f"{rsp + 0x330:X}", "valueType": "int32"},
    {"address": f"{r14 + 0x1D58:X}", "valueType": "int32"},
    {"address": f"{r14 + 0x1D5C:X}", "valueType": "int32"},
]
```

  读取失败或目标会话变化退出 3；不读取固定旧地址。
- [ ] 调用 `code_disassemble` 读取当前 RIP 前后少量指令，仅作证据，不调用 `code_get_function` 或任何执行类工具。
- [ ] 使用 `atomic_text` 写入 `Output/step_capture_<address>_<timestamp>.md`，临时文件失败时清理；Gateway 统一在 `finally` 关闭。

### 任务 2：单元测试和假 MCP

**涉及文件：** 新建 `Scripts/tests/test_step_capture.py`。

**接口依赖：** 任务 1 的常量、`run_capture`、`read_fixed_status`、`wait_for_stopped`；假客户端提供完整工具目录、实例、运行概览、兼容 Lua 响应、上下文、断点列表、动态内存结果和 `debugger_step` 响应。

**执行步骤：**

- [ ] 编写中文函数注释和测试方法说明；测试日志/错误字符串使用英文，符合项目约束。
- [ ] 测试正常原生状态路径：单步工具存在，起始 RIP 正确，调用一次 `debugger_step(mode="into")`，最终 RIP 为 `+11FD5D0`，断点列表不变。
- [ ] 测试兼容状态路径：`debugger_get_status` 返回已知 `debug_isBroken` 类型错误，固定 Lua 查询证明 stopped，仍成功完成一次单步。
- [ ] 测试 `debugger_step` 缺失、schema 缺少 `mode`、mode enum 缺少 `into/over`、lua_execute 缺失；预期不调用单步，退出码 2。
- [ ] 测试起始 RIP 不是 `+11FD5C9`；预期不调用单步，报告指出需要用户重新停在起始断点。
- [ ] 测试单步工具返回 `hostEffect=unknown`、`started` 或传输断开；预期退出码 3，不再读取后续内存，不调用 continue。
- [ ] 测试单步后兼容状态保持 `stepping=true` 直到下一次轮询，然后 stopped；验证轮询次数和超时行为。
- [ ] 测试单步后 RIP 偏离预期、THREADID 变化、runtime epoch/PID/selectionEpoch 变化、断点列表变化；预期立即停止后续步骤并保留报告。
- [ ] 测试单步路线遇到 `+11FD5DE call` 时，`mode="into"` 的返回 RIP 不在预期列表则停止；`mode="over"` 只允许在显式路线参数下执行，并验证返回后的 RIP。
- [ ] 测试字段读取使用动态 `RSP/R14` 计算地址，不能读取旧的 `3A484D9F8B8` 或旧栈地址。
- [ ] 测试任何异常都关闭 Gateway；报告采用原子写入，不覆盖已有报告。

### 任务 3：文档和操作验收

**涉及文件：** 新建 `Docs/step_capture.md`。

**接口依赖：** 任务 1 的 CLI 参数和报告格式；任务 2 的测试结论。

**执行步骤：**

- [ ] 说明运行前提：CE 已附加 Victoria 3，用户手动停在 `victoria3.exe+11FD5C9`，游戏保持暂停，断点列表不得由脚本管理。
- [ ] 给出命令示例：

```powershell
cd D:\cebuild\ce-custom
python Scripts\step_capture_at_breakpoint.py --steps 1 --mode into
python Scripts\step_capture_at_breakpoint.py --steps 2 --mode into
```

- [ ] 说明脚本可能执行单步并改变当前 RIP，因此报告失败时用户应在 CE 中检查当前地址，不要直接重复运行。
- [ ] 说明 `debugger_get_status` 的原始错误仍可能存在，但固定 Lua 查询会验证真正的 stopped 状态。
- [ ] 说明脚本不会自动 `continue`，单步后如果目标停止状态不确定，脚本只退出并报告。
- [ ] 说明报告中必须先看 `actual RIP`、`thread ID`、`RSP/R14` 和 `breakpointUnchanged`，再解释字段值。

## 验证流程

- [ ] 运行语法检查：

```powershell
python -m py_compile Scripts\step_capture_at_breakpoint.py Scripts\tests\test_step_capture.py
```

- [ ] 运行定向单元测试：

```powershell
python -m unittest Scripts.tests.test_step_capture -v
```

- [ ] 运行既有兼容测试，确保没有回归：

```powershell
python -m unittest Scripts.tests.test_stacktrace_register -v
```

- [ ] 运行全量 Python 测试：

```powershell
python -m unittest discover -s Scripts/tests -v
```

- [ ] 真实 CE 验收前，先运行 `tools/list` 和实例查询；确认唯一实例为目标 Victoria 3，确认固定 Lua 查询能力存在。
- [ ] 真实验收步骤一：用户手动把 RIP 停在 `victoria3.exe+11FD5C9`，运行 `python Scripts\step_capture_at_breakpoint.py --steps 1 --mode into`；预期报告显示实际 RIP 为 `victoria3.exe+11FD5D0`，断点列表未变化。
- [ ] 真实验收步骤二：如果步骤一报告成功且用户希望继续，重新确认 CE 仍停在报告地址，再运行 `--steps 1` 或 `--steps 2`；禁止脚本自动推断并重复单步。
- [ ] 真实验收步骤三：比较多份报告的 PID、线程、R14、RDI、RSP、方向和候选字段；只把身份一致的样本合并分析。
- [ ] 真实验收不得使用 `debugger_continue`、`debugger_run_to`、`debugger_set_register`、断点管理或目标写入工具。

## 自检

- [ ] 需求覆盖：已说明 Python 单步、兼容状态绕过、寄存器采集、路线验证、失败停止和文档。
- [ ] 安全约束：未授权时不单步；脚本不修改断点、不继续运行、不写寄存器/内存。
- [ ] 根因处理：复用固定 Lua 查询，而不是把 `debugger_get_status` 的错误字段伪造为正常状态。
- [ ] 地址防漂移：会话指纹、线程 ID、RIP 路线、RSP/R14 动态读取、断点列表均有校验。
- [ ] 测试覆盖：成功、兼容路径、能力缺失、工具错误、超时、分支偏离、线程/会话/断点漂移和清理均有具体测试项。
- [ ] 文件范围：实现、测试、文档三类职责分离；不修改 MCP 源码、DLL、用户断点或已有兼容脚本。

## 交付边界

本方案只生成实施计划，不创建脚本、不调用 `debugger_step`、不改变当前 CE 调试现场。执行本方案需要随后使用 `superpowers:executing-plans`，并在真实 CE 验收前再次获得用户明确授权。
