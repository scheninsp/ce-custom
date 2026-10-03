# Refresh 四层伪代码实施方案

我将使用 writing-plans 能力生成完整实施方案。

> **面向自动化执行人员：必须配套子能力：使用 executing-plans 逐任务执行本方案。步骤使用复选框用于进度跟踪。**

**目标：** 在 `FakeCode/ghidra_disassembly` 输出 Refresh 到最短静态调用深度 4 的全部可用函数体，以及不能恢复的路径清单。
**架构方案：** 读取已验证的 Ghidra 调用图，以 BFS 独立计算最短深度，按 RVA 去重。完整保留反编译控制流，对已有证据支持的参数添加语义名称；Refresh 单独恢复真实尾跳边界，调用点索引作为参数推断和间接调用的证据补充。
**技术栈：** Python 标准库、现有 Ghidra Markdown 导出、JSON 调用图及历史 opcode。

## 全局约束

使用中文进行对话输出。
使用中文进行代码注释，但是不要使用中文日志。
python,powershell等脚本代码文件，需要在文件头部使用中文注释说明文件功能。
每个函数头部都要加上函数功能，以及入参与返回值的中文注释说明。
对于每个伪代码函数，如果产生新的函数命名，那么一定要在后续注释上它对应的地址（victoria3.exe+XXX 的这个 XXX 相对地址）。
如果要生成新的伪代码函数名时，先查找他的相对地址是否在生成过的伪代码函数中已经存在了，如果已经存在，那么就沿用之前的函数名。
生成伪代码函数要在 FakeCode 文件夹，放置到与函数最相关的文件，单个文件不得容纳超过2000行，若超过行数则新建文件容纳。

### 任务1：生成全部函数体和调用范围

**涉及文件：** 新建 `Scripts/ghidra/build_refresh_depth4.py`；生成 `FakeCode/ghidra_disassembly/function_<RVA>.md`、函数分片、`index_*.md`、`manifest.json`、`verification.json`。
**接口依赖：** 输入 `Output/ghidra_refresh_20261003/callgraph.json`、`manifest.json`、`decompiler_warnings.json` 和 `FakeCode/ghidra_refresh_20261003/function_*.md`；输出按最短深度排序的函数清单、完整函数体和证据清单。

- [x] 用 `collections.deque` 从 `11FBDA0` 开始沿所有已解析边计算最短深度，选择 `depth <= 4`；与现有 manifest 深度逐项核对。
- [x] 按源文件代码围栏拼接各函数片段，保留每行源代码的顺序；只用单词边界替换明确参数名，不推断新业务函数名称。
- [x] 根函数在 `uStack_70 = 0x1411fc33d;` 前结束，追加 `CalculateDesirability(candidate, context)` 尾调用记法；用 opcode 核对 `WrapNumericContext` 的 RDX 入参及调用前准备。
- [x] 每个函数页面记录入口 RVA、原始来源、参数映射、所有出边和深度 4 边界；未解析边保留指令和调用点，外部导入不生成空函数体。
- [x] 每份 Markdown 不超过 2000 行，代码分片控制在 1400 行并重复注明入口与续片属性。

### 任务2：证据说明与验证

**涉及文件：** 生成 `FakeCode/ghidra_disassembly/README.md`、`semantic_notes.md`、`unresolved_edges.json`、`boundary_edges.json`、`external_symbols.json`、`decompiler_warnings.json`。
**接口依赖：** 输入任务1的范围和生成结果；输出语义证据说明及可复核的验证结果。

- [x] 对照 `FakeCode/2026-10-3-process1/trade_advantage_functions.md` 和 `Docs/2026-10-3-process01/important_notes/刷新候选函数.md`，说明候选布局、缓存正值门槛、收益模拟和真实评分公式的来源与旧骨架缺陷。
- [x] 逐函数反向还原参数名称，验证除根函数的两项显式修正外，全部正文与原始导出一致；不以可编译性代替反编译正确性。
- [x] 校验 BFS 深度、333 个内部函数覆盖、19 个外部符号、全量链接存在、分片行数、调用边无遗漏、警告与未解析边归属。
- [x] 执行 `python Scripts/ghidra/build_refresh_depth4.py`，检查生成 `verification.json` 中所有验证错误为空，最后向用户报告已知静态覆盖与未恢复范围。

验证结果：333 个函数正文重新拼接一致；3228 个已有文件链接通过，验证报告链接写入后独立检查；Markdown 最大 1148 行；根函数 24 条调用/尾跳边；全部 314 条范围边界出边来自深度 4。所有验证错误为空。
