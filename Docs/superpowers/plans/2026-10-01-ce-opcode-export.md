我将使用 writing-plans 能力生成完整实施方案`r`n`r`n# CE 输出文件自动化实施方案
> **面向自动化执行人员：必须配套子能力：使用 superpowers:executing-plans 逐任务执行本方案。步骤使用复选框（`- [ ]`）用于进度跟踪。**
**目标：** 从 `Docs/testdata-*.md` 提取 CE 报告中的地址，并自动生成每个地址前后 100 条反汇编指令的独立 Markdown 文件。
**架构方案：** 由 CE 内运行的 Lua 脚本负责解析输入文档、调用 CE 的反汇编接口、定位目标指令并写出结果；外部 Python 仅负责发现输入、启动或加载 CE Lua、轮询结果和返回退出码，不实现调试器。脚本将地址、模块、字节码和指令文本统一写成稳定的 Markdown 格式，并生成汇总索引，便于 AI 后续读取。
**技术栈：** Cheat Engine Lua、CE Lua `disassemble`/`getInstructionSize`、系统 Python 3（外部编排）、UTF-8 Markdown。
## 全局约束
- 使用中文对话和代码注释；脚本日志使用英文。
- 不修改 Cheat Engine 源码，不重新实现进程附加、断点或反汇编。
- 绝对地址只对产生该报告的当前 `victoria3.exe` 进程有效；输入地址必须先确认 CE 已附加同一进程。
- 输出文件名使用小写前缀 `opcode_` 加不带 `0x` 的十六进制地址，例如 `opcode_7FF71C8D9218.md`。
---

### 任务1：定义配置和输出目录
**涉及文件：**
- 新建：`Config/opcode_export.json`
- 新建：`Output/opcodes/.gitkeep`

**接口依赖：**
- 依赖输入：无。
- 对外输出：配置字段 `input_glob`、`output_dir`、`before_count`、`after_count`、`scan_back_bytes`、`process_name`。

**执行步骤：**
- [ ] 创建以下固定配置，默认从最新测试数据读取，并输出 100/100 指令：
```json
{
  "input_glob": "Docs/testdata-*.md",
  "output_dir": "Output/opcodes",
  "before_count": 100,
  "after_count": 100,
  "scan_back_bytes": 4096,
  "process_name": "victoria3.exe"
}
```
- [ ] 将 `before_count`、`after_count` 限制为正整数，将 `scan_back_bytes` 限制在 256 到 65536 之间；配置错误时 Lua 立即终止并写英文错误日志。

### 任务2：实现 CE Lua 导出器
**涉及文件：**
- 新建：`Scripts/opcode_export.lua`
- 修改：`Scripts/main.lua`（增加菜单/快捷调用入口，不在入口中复制导出逻辑）

**接口依赖：**
- 依赖输入：任务1的 JSON 配置和一个已附加 `victoria3.exe` 的 CE 会话。
- 对外输出：`exportOpcodes(configPath) -> {ok:boolean, files:table, errors:table}`；每个输出文件为 UTF-8 Markdown。

**执行步骤：**
- [ ] 用 CE Lua 文件 API 读取配置和输入 Markdown；输入文件按文件名中的时间排序，选择最新文件。若找不到文件，返回 `ok=false` 并写明搜索路径。
- [ ] 使用模式 `The following opcodes accessed%s+([0-9A-Fa-f]+)` 提取每个段落的目标地址；同时用 `([0-9A-Fa-f]+)%s*%-%s*` 提取同段指令地址。对重复地址去重并按数值升序处理。
- [ ] 将目标地址转换为整数，调用 `readInteger`/`getAddress` 验证 CE 能访问该地址；不可访问的地址只记录错误，不阻塞其他地址。
- [ ] 编写 `decodeForward(address, count)`：循环调用 `disassemble(current)` 获取文本，调用 `getInstructionSize(current)` 获取长度；长度小于 1 或反汇编失败时停止并返回错误。
- [ ] 编写 `findWindowStart(target, beforeCount, scanBackBytes)`：从 `target-1` 向前逐字节尝试候选起点；对每个候选点顺序调用 `getInstructionSize`，只有当某次解码恰好落在 `target` 时才接受该候选点。选择距离目标最近且能解码出 `beforeCount` 条指令的候选点；找不到时输出“无法可靠定位前置指令”，并仍导出目标之后的指令。
- [ ] 从窗口起点解码 `beforeCount + 1 + afterCount` 条，记录地址、机器码（用 `readBytes(address, size, true)` 转成两位十六进制）和 CE 返回的汇编文本。目标行增加 `> TARGET` 标记。
- [ ] 每个地址写入 `Output/opcodes/opcode_<UPPER_HEX>.md`，格式固定为：来源文件、目标地址、生成时间、前后条数、三列表格（地址/bytes/instruction）。写文件采用临时文件后 rename，避免半文件。
- [ ] 生成 `Output/opcodes/index.md`，列出来源文件、目标地址、输出文件、成功/失败和错误原因；脚本结束时返回结构化结果供入口显示。
- [ ] 所有日志使用英文，例如 `INFO: exported ...`、`ERROR: decode failed ...`；代码注释使用中文。

### 任务3：增加 CE 内调用入口
**涉及文件：**
- 修改：`Scripts/main.lua`

**接口依赖：**
- 依赖输入：任务2导出的 `exportOpcodes`。
- 对外输出：CE 菜单项 `CE Auto -> Export opcode windows`，点击后调用 `exportOpcodes("Config/opcode_export.json")`。

**执行步骤：**
- [ ] 在脚本加载时注册一次菜单项，保存菜单对象避免重复注册。
- [ ] 点击时检查当前进程名；不是 `victoria3.exe` 时弹出中文提示并停止。
- [ ] 执行导出后弹窗显示成功数、失败数和 `Output/opcodes/index.md` 路径；详细信息只写英文日志。
- [ ] 菜单回调使用 `pcall`，将 Lua 异常转为可读错误，不让 CE 主界面崩溃。

### 任务4：提供 Python 外部编排器
**涉及文件：**
- 新建：`Scripts/run_opcode_export.py`

**接口依赖：**
- 依赖输入：正在运行且已附加 `victoria3.exe` 的 Cheat Engine。
- 对外输出：启动/加载 CE Lua 脚本；退出码 0 表示请求已发送，非 0 表示参数或路径错误。

**执行步骤：**
- [ ] 使用 `argparse` 接收 `--cheat-engine-path`、`--config-path`、`--wait-seconds` 参数，默认从 `C:\Program Files\Cheat Engine` 查找 CE。
- [ ] 使用 `pathlib.Path` 检查配置和 Lua 文件存在；不存在时输出英文错误并返回 2。
- [ ] 用 `subprocess.Popen` 启动指定 CE 可执行文件；启动前记录 `Output/opcodes/index.md` 的修改时间，避免误判旧结果。
- [ ] 通过 CE 支持的命令行脚本加载方式触发 Lua；若当前 CE 版本不支持命令行注入，输出明确提示，要求在 CE Lua Engine 手工执行 `Scripts/opcode_export.lua`，不模拟鼠标点击。
- [ ] 使用 `time.monotonic()` 轮询 `Output/opcodes/index.md`，检测文件更新时间和内容中的完成标记；超时返回 3，并保留 CE 生成的部分结果。
- [ ] 用 `subprocess.run` 或进程句柄清理本次由脚本启动的 CE 进程；用户已存在的 CE 实例不得被强制终止。

### 任务5：验证与回归
**涉及文件：**
- 新建：`Scripts/tests/opcode_export_fixture.md`
- 新建：`Scripts/tests/test_opcode_export.py`

**接口依赖：**
- 依赖输入：固定 fixture，包含两个 `The following opcodes accessed ...` 段落、重复地址和无效地址。
- 对外输出：可重复运行的解析与输出格式验证。

**执行步骤：**
- [ ] 在不启动 CE 的情况下测试纯文本解析：两个段落得到两个唯一目标地址，重复指令地址只保留一次。
- [ ] 在真实 CE 会话中选取 `Docs/testdata-2026-10-1-10-58.md` 的地址运行导出，确认每个成功文件含目标行、最多 100 条前置和 100 条后置记录，且 `index.md` 与文件数量一致。
- [ ] 验证无效地址、反汇编失败、输出目录不可写时：脚本继续处理其他地址，索引记录失败原因，Python 进程退出码符合任务4约定。
- [ ] 连续运行两次，确认同名文件被原子替换且不会产生重复临时文件。

## 自检
- 需求覆盖：已覆盖从 `Docs/testdata-*.md` 提取访问地址、调用 CE 获取附近 opcode、每个地址独立输出文件和自动化入口；未要求修改 CE 源码，因此方案不包含源码改动。
- 无占位符：全文未使用“待定”“后续补充”“后续实现”等未落地表述。
- 接口一致性：任务2定义 `exportOpcodes(configPath)`，任务3按同一签名调用；任务1字段名与任务2读取字段一致。

