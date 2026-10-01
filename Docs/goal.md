
# 项目目标
本项目试图使用 CE + Lua 实现一个很薄的让 AI 自动化操作 CE 进行条件断点，获取寄存器信息，代码反汇编等信息传递给 AI 的工具。

CE源码地址：`D:\cebuild\cheat-engine`
CE的可执行程序地址：`C:\Program Files\Cheat Engine`(和源码不是一个版本)

这样可以直接使用 CE 已经实现好的：
- 进程附加
- 模块基址解析
- 断点
- 条件断点
- 单步
- 寄存器读取
- 内存读取
- 反汇编
- 调用栈
你只需要自动化 CE，而不是重新实现调试器。


1. Cheat Engine Lua
最适合你的需求。
CE 本身支持 Lua 脚本，可以通过脚本完成：
解析 地址xxx
设置断点
设置条件
断点命中后记录寄存器
读取 RDI+4、RDI+D0 等地址
输出附近 opcode
写入 JSON 或文本文件
你可以把文档中的操作变成一个配置文件：
breakpoints = {
  {
    address = "xxx",
    condition = "R14 == yyy",
    reads = {
      "RDI",
      "[RDI]",
      "[RDI+0x4]",
      "[RDI+0xD0]",
      "[RSP+0x330]",
      "[RSP+0x50]"
    }
  }
}
AI 或外部脚本只需要修改配置并读取结果。
CE 源码中与你需求最相关的部分已经存在：
- CEDebugger.pas
- DebuggerInterface.pas
- breakpointtypedef.pas
- disassembler.pas
但你不需要编译或修改这些源码。

