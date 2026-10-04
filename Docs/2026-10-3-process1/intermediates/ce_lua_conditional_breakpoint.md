# Lua 执行与原生条件断点命令

2026-10-03（北京时间）：两个独立 CLI 已实现。状态兼容复用既有 `read_status` 的固定只读查询，没有修改采集脚本、插件、CE 安装或游戏。原生 UI 后端已完成本地源码合同核对和离线测试；**尚未通过当前安装实例的只读 UI 探查、真实设置/读回及人工命中验收**。

实施进度：

- [x] 任务 1：公共生命周期、Lua CLI、离线输入及失败测试。
- [x] 任务 2：固定原生 Lua 后端、源码核对、失败边界和静态合同测试。
- [ ] 任务 2 现场门：用户打开断点列表后只读探查当前 UI，提供一个已停止且无冲突的地址进行添加验收。
- [x] 任务 3：条件 CLI、回执校验及 Fake 客户端测试。
- [x] 任务 4：CMD 指南与离线回归。
- [ ] 任务 4 现场门：算术返回 5、真实条件保存/读回、用户人工 Run 并观察命中。

所有命令从 `D:\cebuild\ce-custom` 根目录运行；Python 3.10+，标准库，无新增依赖。CE 必须预先附加目标，MCP 必须启用 `unsafeLua`；脚本不会自动附加或修改配置。条件命令另要求目标为 64 位 `victoria3.exe`，调试器已经停止。MCP 返回的进程名允许 `victoria3` 或 `victoria3.exe`，忽略大小写，但不接受路径、前后空白或其他名称；报告保留原始名称，前后目标身份校验不变。

## 独立 CMD 命令

```cmd
cd /d D:\cebuild\ce-custom
python Scripts\ce_execute_lua.py --source "return 2 + 3" --output Output\cycle_count
python Scripts\ce_execute_lua.py --file Output\cycle_count\setup.lua --output Output\cycle_count
```

第一条应返回 `[5]` 并退出 0；本次尚未在真实 CE 执行。第二条文件由用户准备并审阅。通用 Lua 不是沙箱，可以执行副作用；CLI 原样发送源码，不做关键词安全承诺，也不再次运行源码来“验证”。助手提供的源码必须遵守本阶段不 Run、Step、暂停/恢复、写内存或推进游戏的约束。

条件命令模板（先将尖括号内容替换为本次已确认参数）：

```cmd
python Scripts\ce_set_conditional_breakpoint.py --address "<当前无冲突地址>" --condition-type complex --condition-file "<UTF-8 条件文件>" --output Output\cycle_count
```

可以使用 `--condition "return true"` 或 Simple 单行表达式 `--condition-type simple --condition "RCX == 0x1234"`；这些只是语法示例，不是本次游戏筛选配置。两种条件输入必须恰好选择一种。地址允许 1–16 位十六进制绝对地址（可带 `0x`），或 `victoria3.exe+` 加 1–16 位十六进制 RVA。绝对地址零、其他模块和任意 CE 表达式均被拒绝。历史候选 `victoria3.exe+11FD93B`、`victoria3.exe+11FAF69` 须核对当前版本，不能直接作为本次执行授权。

公共选项：

| 参数 | 作用与默认值 |
| --- | --- |
| `--instance-id` | 精确选择发现的 CE 实例；多实例时必填，不模糊匹配 |
| `--gateway` | 默认项目内 `McpExternals/CheatEngine.Mcp-2.0.0-beta.2-win-x64/CheatEngine.Mcp.Gateway.exe` |
| `--timeout` | 每次 MCP 请求正有限秒数，默认 30；条件命令至少 10 秒 |
| `--output` | 报告目录，默认根目录下 `Output/cycle_count` |

文本接受 UTF-8/UTF-8 BOM，换行规范为 LF，保留前后空白；拒绝纯空白、NUL、无效编码及超过 65536 UTF-8 字节的输入。条件以 UTF-8 字节转义到 Lua 字符串，组装后仍须不超过 65536 字节，因此可接受的条件长度小于原文上限。Simple 只允许一行并以 `return (<表达式>)` 编译检查；Complex 编译原文，都不会为检查语法而执行条件。条件实际返回类型和异常表现需要用户观察。

## 原生后端与源码证据

后端固定为 `native-ui`，不提供 callback 替代，不覆盖全局 `debugger_onBreakpoint`。

本地 CE 源码目录为 `D:\cebuild\cheat-engine\Cheat Engine`：

- `frmBreakpointlistunit.pas:312` 的 `miSetConditionClick` 打开 `TfrmBreakpointCondition`，读取原有条件，确认时调用 `setbreakpointcondition`。
- `frmBreakpointConditionUnit.pas/.lfm` 包含 `rbEasy/rbComplex/edtEasy/mComplex`；`frmBreakpointlistunit.lfm` 包含 `ListView1/Timer1/miSetCondition`。
- `frmBreakpointlistunit.pas:404` 的 `Timer1Timer` 更新列表；`MemoryBrowserFormUnit.pas:4382` 的 `Breakpointlist1Click` 打开或激活列表。
- `debughelper.pas:2610` 保存原生条件；`LuaHandler.pas:3373` 返回断点地址表，`:3541` 默认执行断点及既有默认方法，注册项包含 `debug_setBreakpoint/debug_getBreakpointList/getTickCount`。
- 安装版 `C:\Program Files\Cheat Engine\celua.txt` 列出 `findComponentByName`、`doClick`、`ModalResult`、`OnTimer` 及执行断点接口。
- MCP `LuaRecords.cs` 定义 `ok/phase/error/hostEffect/returnValues/droppedOpaqueCount`。实际工具合同以本次发现和响应为准。

源码与安装版可能有差别，静态合同不能证明当前安装 UI 可用。添加前编译、检查同地址冲突；只创建一次断点，以列表唯一存在确认创建。通过临时定时器填入条件并确认，随后再次打开窗口读回并取消。前后核对 RIP/RSP/THREADID，Python 另核对目标指纹和停止现场。只读状态兼容查询仅在既有已知错误严格匹配时调用，原始失败和查询回执进入报告，不伪造 `reportedBroken`。

## 当前 UI 只读探查

用户先打开 CE 断点列表，并将下列内容存为自己指定的 UTF-8 Lua 文件，再用 Lua CLI 的 `--file` 执行。探查不点击菜单或创建窗体；返回的能力有任何 false 时，停止现场添加验收。

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

## 报告与故障处理

### 当前安装版文本绑定修复

2026-10-03：首次现场添加创建了断点，但 Complex 条件没有保存，读回阶段因文本为 `nil` 失败。临时隐藏 Memo 上复现了 `memo.Text` 读取为 `nil`、赋值不改变实际内容；Pascal 的 `mComplex.Text` 不能直接当作 Lua 可用属性。后端改用安装版已验证的 `setCaption/getCaption`，它们访问实际控件文本。窗口确认前先校验类型和完整文本，保存后重新打开核对；报告额外保留 `conditionWriteVerified/readbackConditionType/readbackCondition`。文本不可读或写入不符时取消本次条件窗口，不将空条件视为成功，不自动删除已创建断点。该修复不授权 Run 或自动继续。

每次会话生成唯一的 `lua_<UTC时间>_<随机标识>.json` 或 `condition_<UTC时间>_<随机标识>.json`，同前缀 `.gateway.log`。UTF-8 JSON 保存请求原文、实际执行源码 SHA-256、实例和目标基线、原始回执、后置概览/停止状态、关闭结果、UTC 开始结束时间、退出码及最终状态。终端诊断为英文，任意用户文本均 ASCII 转义。参数或文本在创建会话前无效时只输出错误；报告路径可建立后，各失败路径均尝试保存报告。

| 退出码 | 含义 |
| --- | --- |
| 0 | 请求完成且自动检查通过；仍需人工验收 |
| 2 | 本地/前置失败，或编译失败且明确未应用；业务 `preflight` 明确未创建断点 |
| 3 | 已尝试修改、运行失败、通信超时、回执/现场不确定，或动作后证据保存失败 |
| 130 | 用户中断；报告记录动作是否已尝试 |

MCP `hostEffect=completed` 只说明 Lua 返回，不说明业务成功。条件业务必须包含 `ok=true/created=true/conditionReadbackMatched=true/backend=native-ui/phase=completed`、正确条件文本、有效解析地址和一致线程。失败回执中的 `phase/created/error` 始终保留；从 `create-attempted` 起即使 `created=false` 也不能推断无残留。原生断点标记 `resourceOwner=ce-lua-untracked`，没有虚构 MCP 资源 ID。

UI 的 3000 毫秒预算不是强制取消保证。原生菜单的 `ShowModal` 是嵌套消息循环；CE 不调度定时器、其他模态窗口或主线程冻结时，Python 超时/关闭 Gateway 不能取消已经进入 CE 的 Lua。失败后先人工检查窗口和可能残留的普通断点，再决定下一步。不自动重试、不自动删除或覆盖断点、不 Run，也不改用回调。该 UI 操作不能视作严格原子事务。

## 离线回归与人工验收记录

离线命令不连接 CE：

```cmd
python -m unittest discover -s Scripts\tests -p "test_ce_execute_lua.py" -v
python -m unittest discover -s Scripts\tests -p "test_ce_conditional_breakpoint.py" -v
python -m unittest discover -s Scripts\tests -p "test_stacktrace_register.py" -v
python -m unittest discover -s Scripts\tests -v
python -m py_compile Scripts\ce_lua_common.py Scripts\ce_execute_lua.py Scripts\ce_set_conditional_breakpoint.py Scripts\tests\test_ce_execute_lua.py Scripts\tests\test_ce_conditional_breakpoint.py
```

测试使用 Fake 客户端，区别固定兼容查询和业务 Lua，拒绝目录外隐藏动作，覆盖冲突/部分配置失败/超时而无需故意冻结游戏。静态后端测试不等于 Lua 或真实 UI 功能测试。

本次离线结果（2026-10-03，北京时间）：Lua CLI 13 项、条件 CLI 9 项、既有状态采集 32 项通过；全量 89 项通过，`py_compile`、函数中文说明检查和 `git diff --check` 通过。两个独立 CLI 的 `--help` 可运行。另在独立 Python 进程加载安装目录的 `lua53-64.dll`，对 Simple/Complex 两种组装源码执行 `luaL_loadbufferx` 编译检查并通过；未执行编译后的 chunk，未连接 CE。这只证明 Lua 5.3 语法可编译，不能证明原生 UI 功能可用。

现场逐项记录（当前均待用户验收）：

| 项目 | 本次记录 |
| --- | --- |
| 实例 ID、PID、游戏版本 | 待填写 |
| 当前州商品表地址、商品 ID | 待用户确认；历史 ID 10 是木材，不是硬木 |
| 算术请求报告及返回 `[5]` | 待执行 |
| 只读 UI 能力探查报告 | 待执行 |
| 一个无冲突断点地址、默认方法/槽位 | 待用户确认 |
| 条件类型、完整原文及设置报告路径 | 待填写 |
| 添加后 RIP/RSP 和线程一致 | 待验证 |
| 用户在 CE 界面核对地址和条件 | 待验证 |
| 用户人工 Run、游戏解除暂停及日期推进 | 用户操作，脚本不参与 |
| 命中 RCX、RDX+0x10 的商品 ID、游戏日期 | 待记录 |
| 未命中时的观察时段、窗口或残留断点 | 待记录，不能视为“本周零次调整” |

第一个断点通过检查后，用户再决定是否添加第二个。脚本不禁用其他断点。到达提交调用点不证明内部已经成功写入；不输出自动一周计数结论。只有本次原生设置/读回及用户命中验收均通过，才能记录“条件断点功能验收完成”。
