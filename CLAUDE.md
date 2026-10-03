
## 语言相关
使用中文进行对话输出。
使用中文进行代码注释，但是不要使用中文日志。

## 外部环境相关
### CheatEngine
CheatEngine 7.7 安装路径在 `C:\Program Files\Cheat Engine`

### CheatEngine MCP
CheatEngine MCP 以编译好的 dll 插件形式嵌入到 CheatEngine 软件中。其源码在 `D:\cebuild\CheatEngine.Mcp`，但版本可能有小的差别。
`debugger_get_status` 的 `stateValid=false` 问题已经在 `get_stacktrace_register_at_breakpoint.py`采集流程中通过固定只读 Lua 查询解决，可以参考。

### Victoria3 游戏
victoria3 游戏路径在 `D:\Games\Victoria3\Victoria 3`。其中的 `D:\Games\Victoria3\Victoria 3\Docs` 包含了一些游戏功能文档。
`D:\Games\Victoria3\Victoria 3\game\common`是游戏的文件目录，包含了很多功能的文本化描述。

### ghidra反编译结果
ghidra反编译 victoria3.exe 的项目位于`D:\cebuild\vic3-rev`。

## 代码规范
python,powershell等脚本代码文件，需要在文件头部使用中文注释说明文件功能。
每个函数头部都要加上函数功能，以及入参与返回值的中文注释说明。

## 反编译生成伪代码的规范
对于每个伪代码函数，如果产生新的函数命名，那么一定要在后续注释上它对应的地址（victoria3.exe+XXX 的这个 XXX 相对地址）
如果要生成新的伪代码函数名时，先查找他的相对地址是否在生成过的伪代码函数中已经存在了，如果已经存在，那么就沿用之前的函数名。
生成伪代码函数要在 FakeCode 文件夹，放置到与函数最相关的文件，单个文件不得容纳超过2000行，若超过行数则新建文件容纳。
Docs文件夹允许在文档中复制伪代码函数的内容，但是必须在 FakeCode 文件夹中有来源。

## 执行前检查
无特殊说明

## 工具使用
无特殊说明

## 调试进程启动记录
2026.10.3 18:32 第一次 victoria3.exe 进程结束
所有第一次进程执行期间产生的文档和记录都被放入各个文件夹下的"2026-10-3-process1"子文件夹。

## Ghidra 反编译资料入口
`Refresh`（`victoria3.exe+11FBDA0`）的定位与分析见 [Docs/ghidra_refresh_20261003.md](Docs/ghidra_refresh_20261003.md)。
完整静态递归导出、按 RVA 的函数文件和调用索引见 [FakeCode/ghidra_refresh_20261003/README.md](FakeCode/ghidra_refresh_20261003/README.md)。
先读入口中的证据边界；间接调用和带警告代码不能视为已全部恢复。

