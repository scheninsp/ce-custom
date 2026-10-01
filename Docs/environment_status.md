# 当前环境状态与准备结论

## 已验证可行

- Cheat Engine 已安装并可正常使用。
- Cheat Engine 源码目录：`D:\cebuild\cheat-engine`。
- Cheat Engine 可执行程序目录：`C:\Program Files\Cheat Engine`。
- Victoria 3 已安装，目标进程为 `victoria3.exe`。
- 已成功获取过 Victoria 3 的进程、模块和调试信息，说明 CE 与目标程序的基本连接可用。
- 正常启动 CE 不需要管理员权限；后续脚本也应按普通权限运行，除非目标进程权限发生变化。
- 项目所需的空脚本/配置文件已经创建。
- 输出格式确定为 JSON 文本，供 AI 或外部监控程序读取。

## 启动和操作方式

项目不以人工 GUI 操作为主，而是由脚本自动控制 CE：

1. 启动 Cheat Engine 进程。
2. 通过 CE Lua 脚本附加或打开 `victoria3.exe`。
3. 根据配置解析地址并设置断点/条件断点。
4. 断点命中后读取寄存器、内存、栈和附近 opcode。
5. 将每次事件追加写入 JSON 文本文件（建议使用 JSON Lines，每行一个完整 JSON 对象）。
6. AI 侧持续监控该文件并处理新事件。

## Lua 环境要求

CE 自带 Lua 运行环境，原则上不需要另外安装 Lua。需要在实际 CE 版本中验证：

- 能否从命令行或脚本入口自动执行 Lua 文件；
- `openProcess` 或等效接口能否附加 `victoria3.exe`；
- `getAddress` 能否解析 `victoria3.exe+11FD5C9`；
- 断点创建、条件判断和断点回调接口；
- 断点回调中读取寄存器、内存和栈地址的接口；
- 反汇编接口；
- Lua 文件写入权限和 JSON 序列化方案。

## JSON 输出约定

建议输出文件使用 JSON Lines（`.jsonl`）：

```json
{"timestamp":"...","event":"breakpoint","address":"victoria3.exe+11FD5C9","registers":{},"memory":{},"opcode":"..."}
```

每次断点命中追加一行，避免覆盖已有事件，也便于 AI 侧按行增量读取。写文件时使用 UTF-8 编码，并定期 flush/关闭文件以便外部进程及时看到内容。

## 重要限制

- `victoria3.exe+11FD5C9`、条件表达式、寄存器偏移和栈偏移均可能随游戏版本变化；脚本应把这些内容放在配置文件中，不要硬编码在逻辑里。
- 当前不需要重新编译或修改 CE 源码，也不需要安装 Free Pascal/Lazarus、Visual Studio、Python 或 Node.js。
- 如果日后改为由外部程序解析 JSON 或连接 AI，再单独安装对应运行时即可。

## 编码问题说明

`Docs\goal.md` 文件实际为 UTF-8 编码，文件开头字节和 UTF-8 解码结果均正常。此前出现的乱码是读取工具或终端使用了错误字符集（例如将 UTF-8 按 GBK/ANSI 解码）造成的，不代表 agent 环境或项目文件损坏。读取该文件时应明确指定 UTF-8。
