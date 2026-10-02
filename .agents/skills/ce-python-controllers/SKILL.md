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
