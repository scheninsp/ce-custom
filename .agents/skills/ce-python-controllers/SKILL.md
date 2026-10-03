---
name: ce-python-controllers
description: control cheat engine by python
---

所有python执行目录以项目目录为基准。

# 1.采集 opcode
python Scripts\run_opcode_export.py 7FF777CED5C9 100
返回 7FF777CED5C9 前后 +-100 行的 opcode 输出到 Output 文件夹。

# 2.采集当前断点的 stacktrace 和 registers
python Scripts\get_stacktrace_register_at_breakpoint.py
只读采集 CE 手动断点现场的寄存器与启发式栈候选，并原子生成 Markdown 报告。

# 3.执行单步 Step Over
python Scripts\ce_run_step_over.py
结果默认保存到项目根目录下的 `Output/step_capture.md`。
如果不需要采集文件，则使用：`python Scripts/ce_run_step_over.py --no-output`。

# 3.执行单步 Step Into
python Scripts\ce_run_step_into.py

# 4.执行一次 CE Lua
python Scripts\ce_execute_lua.py --source "print('hello')"
python Scripts\ce_execute_lua.py --file path\to\request.lua
向 Cheat Engine 执行一段 Lua 并保存原始回执。`--source` 与 `--file` 必须二选一；脚本不会隐式控制目标进程。

# 5.添加原生条件执行断点
python Scripts\ce_set_conditional_breakpoint.py --address victoria3.exe+11FBDA0 --condition-type simple --condition "RAX == 0"
`--condition-type` 支持 `simple` 和 `complex`，条件文本也可通过 `--condition-file` 从 UTF-8 文件读取。该命令不会继续目标或清理已有断点。

