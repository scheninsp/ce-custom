# 导出固化列表中的 opcode 窗口

运行前先在 CE 中手动附加 victoria3.exe；脚本不会自动附加、切换或分离目标。

在 D:\cebuild\ce-custom 中运行：

    python Scripts/run_opcode_export.py

也可以直接指定一个十六进制地址和前后指令条数，例如：

    python Scripts\\run_opcode_export.py 7FF777CED5C9 100

单地址模式会先由 CE 解码目标指令，以当前机器码作为锚点，再导出前后各指定条数；地址和条数必须同时提供。

CE 未附加 victoria3，或已附加其他程序时，脚本以退出码 2 停止。
目标地址与原始机器码固化在 Scripts/run_opcode_export.py 的 TARGETS 列表（9 对，来源为 Docs/testdata-2026-10-1-10-58.md）。
游戏重启后地址失效：重新采集报告并手动更新 TARGETS；脚本不读取也不解析报告文件。

自定义输出根目录：

    python Scripts/run_opcode_export.py --output Output/opcodes

多个 CE 实例时，用本次 instance_list 结果提供 --instance-id。
该参数不保存为跨重启默认值。
--timeout 控制单次 MCP 请求的超时秒数，默认 30。
--gateway 可指定另一个同版本 Gateway 可执行文件的完整路径。

脚本最后打印本次输出目录。每次都建立独立子目录，包含：
- opcode_<大写十六进制地址>.md：每个唯一指令地址一个文件。
- index.md：本次所有目标的状态与相对链接。
- manifest.json：实例、目标 PID、选择代次、条数、CE 资源计数基线、收尾核对结果（residueCheck）和错误。
- gateway.stderr.log：本次 Gateway 的诊断输出。

批量模式文件包含前 100 条、目标指令、后 100 条，共 201 条；单地址模式的条数由命令行参数决定。
目标标记为 TARGET，Offset 从 -100 到 +100。
CE 前置边界属于估计；结果通过连续性和目标机器码检查，
并不证明实际执行路径，也不是暂停进程得到的原子快照。

退出码 0 表示全部目标完整成功，且收尾残留核对已取得结论（unchanged/changed）。
1 表示至少一个地址失败；2 表示固化列表、配置、实例选择、未附加或文件系统失败；
3 表示传输失效、CE 会话变化，或残留核对未能完成；130 表示用户中断。
manifest 的 status=starting/running 表示未完整结束，不能用于宣告成功。
失败文件只记录错误，不携带冒充完整窗口的指令表。
脚本全程只调用只读工具，不写内存、不设断点、不注入、不附加/分离；
任何失败都不会留下对 CE/游戏内存或状态的修改。
manifest 中的 residueCheck 记录收尾核对状态：changed 表示运行前后 CE 的 resourceCount/jobCount
发生变化，需人工核查；unavailable/skipped 表示无法确认，按 reason 字段排查。

常见处理：
- 无 CE 实例：确认插件仍为 Enabled，并确认 Gateway/CE 为同一用户。
- CE 未附加：先在 CE 中手动附加 victoria3.exe，再重新运行；脚本不会代为附加。
- 多实例：提供当次的 --instance-id。
- 源机器码不一致或地址不可读：重新采集当前游戏的报告，手动更新 TARGETS 列表。
- 第 101 行不是目标或连续性失败：在 CE 内存查看器核对边界；
  本次保持失败，不通过缩短窗口、修改机器码基线或切换解码器掩盖问题。
- 请求超时：检查 CE 是否正在显示模态窗口/忙于操作；确认状态后重新运行。
  脚本不会自动重发请求，也不会结束用户的 CE/游戏。
- manifest 的 residueCheck.state 非 unchanged：changed 时核对 CE 的 resourceCount/jobCount
  变化来源（只读工具本身不会产生 CE 资源）；unavailable/skipped 时按 reason 字段排查。
- 输出不可写：换用可写的 --output 目录，不修改 MCP 文件权限设置。

文件写入由本地 Python 完成，无需启用 MCP 的 Files:AllowedRoots，
也无需启用 unsafe Lua、AA、代码注入或内核能力。
