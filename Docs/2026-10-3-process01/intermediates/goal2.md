写一个采集当前断点 stacktrace 和所有寄存器内容的脚本 'get_stacktrace_register_at_breakpoint.py'。
我会手动运行 CE 到断点。然后通过 cmd 在项目根目录 `D:\cebuild\ce-custom` 运行 `python ./Scripts/get_stacktrace_register_at_breakpoint.py`
运行此脚本后，将寄存器和断点信息生成一个 streg_<断点地址>.md 纯文本文件，保存到 Output 文件夹下。


