# CE 原生 StackTrace 采集实施方案
> **面向自动化执行人员：必须配套子能力：使用 superpowers:executing-plans 逐任务执行本方案。步骤使用复选框（`- [x]`）用于进度跟踪。

我将使用 writing-plans 能力生成完整实施方案。

**目标：** 默认通过 MCP 获取 CE Memory Viewer → View → StackTrace 的全部行，替换仅扫描 128 个槽的默认输出。
**架构方案：** 保持现有实例发现、寄存器采集、状态兼容、会话指纹及原子文件写入。使用固定 Lua 在 CE 主线程刷新原生 StackTrace 窗口并复制全部行；窗口不存在时通过原生菜单创建，完成或异常后关闭本次创建的窗口，已有窗口保持打开。原启发式路径通过 `--stack-mode heuristic` 显式选择，原生路径失败不自动降级。
**技术栈：** Python 标准库、现有 MCP stdio 客户端、CE 7.7 Lua 5.3、CE 原生 StackWalk64。

## 全局约束
使用中文进行对话输出。
使用中文进行代码注释，但是不要使用中文日志。
python,powershell等脚本代码文件，需要在文件头部使用中文注释说明文件功能。
每个函数头部都要加上函数功能，以及入参与返回值的中文注释说明。
保留 evidence、capabilities、hostVersion、platform 的递归输出过滤。
不继续、单步、附加目标，不更改断点、目标内存、寄存器或 CE 全局函数。
---

## 调研依据与文件职责

- `D:/cebuild/CheatEngine.Mcp/srcs/CheatEngine.Mcp.Tools/Debugger/DebuggerTools.cs`：接口 depth 合同为 1–128 槽。
- 同目录 `DebuggerLuaScripts.cs`：逐槽取值并查找前一条 call，非栈展开。
- `D:/cebuild/cheat-engine/Cheat Engine/frmstacktraceunit.pas`：Refresh1 → refreshtrace → StackWalk64，五列来源为原生帧及符号器。
- `D:/cebuild/cheat-engine/Cheat Engine/MemoryBrowserFormUnit.pas`：Stacktrace1 菜单创建/显示原生窗口。
- `C:/Program Files/Cheat Engine/celua.txt`：getFormCount/getForm、findComponentByName、doClick、Items/SubItems、close。
- 2026-10-02 现场探测确认 lua_execute 运行于 CE 主线程，可读取全部 17 行；仅复制数值/字符串，不返回 CE 对象。
- 修改 `Scripts/get_stacktrace_register_at_breakpoint.py`：固定查询、模式选择、原生响应校验及报告渲染。
- 修改 `Scripts/tests/test_stacktrace_register.py`：扩展假客户端和原生模式回归测试。
- 修改 `Docs/stacktrace_register.md`：模式、UI 刷新影响、适用边界与现场结果。
- 更新 `Output/streg_7FF777CED5C9.md`：实际运行生成，不手工补造帧。

### 任务 1：实现原生采集、校验及测试
**接口依赖：** 现有 `McpClient.call(name, arguments)`、`field(mapping, key, expected)`、`CaptureError`、`tool_failure`。
**对外输出：** `read_native_stacktrace(client, instance_id, context) -> dict`，返回 source、pointerSize、instructionPointer、stackPointer、framePointer、threadId、frameCount、frames、termination。帧包含 pc、pcAddress、stackAddress、frameAddress、returnSymbol、returnAddress、parameters。

- [x] 定义固定 `NATIVE_STACK_SOURCE` 与 `NATIVE_STACK_CHUNK`；使用 `debug_getCurrentContextTable(false)` 记录 IP/SP/BP/THREADID，读取前后保持完全相同。地址统一为大写十六进制字符串，避免 64 位整数精度丢失。
- [x] 枚举 ClassName 为 TfrmStacktrace 的唯一窗口；若有多个则拒绝。不存在时调用 getMemoryViewForm().findComponentByName('Stacktrace1').doClick() 后再定位。通过 pcall 包住刷新和复制，以确保异常也执行自建窗口 close()；不销毁用户已有窗口。
- [x] 调用 Refresh1.doClick()，读取 ListView1.Items；列数须为 5、每行 SubItems.Count 须为 4，返回帧数须在 1–2048。超限拒绝而非截断。pc/returnSymbol 用 getAddressSafe 解析为数值地址。
- [x] 固定查询执行响应必须 ok=true、hostEffect=completed、droppedOpaqueCount=0 且唯一返回对象。检查全部帧字段、地址位宽、首帧 IP/SP、查询上下文 IP/SP/BP/THREADID 与寄存器一致。末返回地址为零标记 zero_return，否则 unwind_stopped，报告明确 CE 展开停止不保证到栈底。
- [x] CLI 新增 --stack-mode native/heuristic，默认 native。原生模式要求 lua_execute 的 instanceId/source/chunkName schema，不要求旧启发式工具；旧模式保留现有工具和深度校验。通用只读白名单不增加 lua_execute。
- [x] 默认表格列为 Index/PC/Stack/Frame/Return/Parameters，元数据记录来源、帧数、终止原因。仅旧模式显示 scannedSlots 和 heuristic 说明；Parameters 为 CE 显示摘要，不能当作完整 x64 调用实参。
- [x] 增加离线覆盖：默认原生调用、17 帧及末零返回、超过 128 帧无截断、非零终止、32 位、缺少 Lua、错误响应/丢弃对象/空帧/计数不符/缺失列/非法地址/上下文漂移、调用失败与网关关闭、过滤与 Markdown 清洗。旧测试显式使用 heuristic，继续覆盖原合同。

核心选择逻辑：
```python
if runtime.get("stackMode", "native") == "native":
    stacktrace = read_native_stacktrace(client, instance_id, context)
else:
    stacktrace = read_tool(client, "debugger_get_stack_trace", instance_id,
                          collecting=True, depth=STACK_DEPTH)
    validate_stacktrace(stacktrace, pointer_size)
```

帧结构校验实现规则：
```python
frames = field(stacktrace, "frames", list)
count = field(stacktrace, "frameCount", int)
if not 1 <= count <= 2048 or count != len(frames):
    raise CaptureError("invalid native stack frame count")
for frame in frames:
    for key in ("pc", "pcAddress", "stackAddress", "frameAddress",
                "returnSymbol", "returnAddress", "parameters"):
        field(frame, key, str)
```

### 任务 2：文档及现场验收
**接口依赖：** 任务 1 的 CLI 及报告结构。
**对外输出：** 说明文档、实际 Markdown 报告、验证摘要。

- [x] 更新说明文档，写明仅刷新/短暂打开关闭原生窗口的 UI 效果、原生展开边界和旧模式限制。
- [x] 执行 `python -m unittest discover -s Scripts/tests -p "test_*.py"`；运行 py_compile 和 git diff --check。
- [x] 执行 `python Scripts/get_stacktrace_register_at_breakpoint.py`；若现场不再停止则保留旧报告并报告原因。
- [x] 从报告 JSON 核对来源、17 帧 PC/Stack/Frame/Return 对应用户样本，末返回值零，前后状态/会话指纹和资源计数一致，四个过滤字段均不存在。实参以实时读取为准，不能复制用户旧值。
- [x] 汇报源码原因、实现路径、测试数量、实际报告地址与帧数、必要的 CE 展开限制。
