# Refresh 在 Ghidra 中的地址、调用链与导出

`FakeCode/2026-10-3-process1/trade_advantage_functions.md` 中的 `Refresh` 是真实入口
`victoria3.exe+11FBDA0` 的分析名称。当前 Ghidra 项目对应的地址为 **`0x1411FBDA0`**。
已经把此入口的全部直接调用、尾跳目标和已解析静态调用边的递归闭包导出到
[FakeCode/ghidra_refresh_20261003](../FakeCode/ghidra_refresh_20261003/README.md)，项目 AI 可直接读取文本文件。

## 地址怎样换算和定位

CE 的 `victoria3.exe+11FBDA0` 中，`11FBDA0` 是 RVA，而不是文件偏移或完整虚拟地址。

| 地址类型 | 本次值 | 用途 |
| --- | --- | --- |
| 模块 RVA | `0x11FBDA0` | 跨 ASLR 地址换算、索引和函数命名 |
| PE / Ghidra Image Base | `0x140000000` | 静态程序的映像基址，已读取 Ghidra 和磁盘 PE 双重核对 |
| Ghidra 地址 | `0x140000000 + 0x11FBDA0 = 0x1411FBDA0` | 在 Ghidra 的 Go To 中输入 |
| 第一次进程模块基址 | `0x7FF776AF0000` | 来自历史 `module_get.json` |
| 第一次进程入口 | `0x7FF777CEBDA0` | 基址加同一个 RVA；不能直接拿来搜索未重定位的 Ghidra 项目 |

GUI 操作：打开 `D:\cebuild\vic3-rev\vic3-rev.gpr`，进入 `victoria3.exe` 的 CodeBrowser，
按 **G**，输入 **`1411FBDA0`**。在 Decompiler 窗口查看该入口的伪代码。
如果以后对程序做了 Rebase，需要用新的 `currentProgram.getImageBase()` 加 RVA 重新换算。

这次读取的已保存项目中，该地址存在 `FUN_1411fbda0`，但函数体只有入口一个字节，指令尚未保存。
有函数标签并不代表反汇编和反编译已完成。导出脚本在一次性项目副本中读取 `.pdata` 的 x64
`RUNTIME_FUNCTION` 表，按边界恢复指令和函数体，再调用 Ghidra 的 `DecompInterface`。
对没有异常表条目的叶函数，使用受限反汇编和 Ghidra 的函数体识别，并排除其他函数占据的地址。
原 GUI 项目没有被此次脚本改写。

## Refresh 的真实范围和业务过程

PE 异常表确认入口范围是 **`+11FBDA0 .. +11FC07C`**，右端不包含。
`+11FC077` 的最后一条指令是 `jmp +11FC320`，不是普通 `call`。
递归图将评分函数记录为单独的尾跳目标；Ghidra 原始反编译显示却可能沿尾跳展开评分代码，
所以 [Refresh 的原始文本](../FakeCode/ghidra_refresh_20261003/function_11FBDA0.md) 比本入口范围对应的逻辑更长。
判断实际边界应看 PE、[根反汇编](../Output/ghidra_refresh_20261003/function_11FBDA0.asm)及调用图。

入口 `RCX` 是候选对象，`RDX` 是共享评估上下文。直接证据对应的过程如下：

1. 以候选 `+0x28` 的引用字段地址调用 `+7C96A0`，取得州相关对象。
2. 调用 `+122AB50`，把返回输出槽里的单位数量写入候选 `+0x38`。
3. 检查商品 ID 和存在位图，按方向读取州对象中的商品优势表，写入候选 `+0x40`。
4. **只有缓存值大于零才命中**。值为零或负数时，解析州对象 `+0x20` 的关联引用并进入计算链。
5. 对方向 `0/1` 构造临时上下文、加入商品方向和市场比例，归一化后取 `max(value, 100000)`。
6. 清理临时成员，调用 `+1027760` 写表，随后重新检查商品和存在位并读取缓存。
7. 结果仍不大于零时调用 `+7A1610` 的断言报告路径。调用者没有提前 `return`；如果报告调用返回，继续刷新。
8. 调用 `+11FBA60` 更新短缺、`+11FC080` 更新收益，最后尾跳 `+11FC320` 计算意愿评分。

方向读取中，`0` 使用州对象 `+0x7C8` 的表，其他值使用 `+0x778` 的表；
缓存未命中后的计算分支只处理 `0` 或 `1`。两张表的数组指针位于表 `+0x08`，存在位图位于表 `+0x20`。
这里的 `100000` 是定点整数单位。候选 `+0x40` 不能直接命名为 UI 相对优势百分比。

## 根函数中的全部调用位置

根入口含 **23 条 call 和 1 条尾跳，共 14 个不同目标**。所有位置已从磁盘机器码重新解码位移并核对。
对应的逐函数原始伪代码链接集中在 [导出入口的直接调用表](../FakeCode/ghidra_refresh_20261003/README.md)。

| 目标 RVA | 名称 / 用途 | 调用位置 RVA |
| --- | --- | --- |
| `+7C96A0` | `Resolve`，解析两个引用 | `+11FBDC1`、`+11FBE79` |
| `+122AB50` | `CalculateQuantityPerCapacity`，数量 | `+11FBDD7` |
| `+1026630` | `FUN_141026630`，商品 ID 检查 | `+11FBDF3`、`+11FBE28`、`+11FBFA8`、`+11FBFD7` |
| `+13C1A10` | `InitTempContext`，初始化 | `+11FBE99`、`+11FBF18` |
| `+1226080` | `WrapNumericContext`，上下文包装 | `+11FBEA4`、`+11FBF23` |
| `+1226160` | `FillGoodsDirectionContext`，方向优势来源 | `+11FBEB8`、`+11FBF36` |
| `+1228B90` | `BuildMarketTradeFraction`，市场比例输入 | `+11FBEC5`、`+11FBF43` |
| `+13C2350` | `NormalizeAdvantage`，输出定点结果 | `+11FBED7`、`+11FBF55` |
| `+C48D10` | `FUN_140c48d10`，临时成员清理 | `+11FBF03`、`+11FBF81` |
| `+1027760` | `UpdateAdvantageCache`，原位写表 | `+11FBF93` |
| `+7A1610` | `FUN_1407a1610`，断言报告 | `+11FC03C` |
| `+11FBA60` | `UpdateCandidateShortage` | `+11FC047` |
| `+11FC080` | `UpdateCandidateRevenue` | `+11FC052` |
| `+11FC320` | `CalculateDesirability` | `+11FC077`，尾跳 |

`WrapNumericContext` 的实际函数体使用 **RDX** 传入的上下文，不能照旧骨架理解为普通单参数 RCX 调用。
`NormalizeAdvantage` 使用输出指针。`UpdateAdvantageCache` 是原位写表，根函数没有消费它的返回值，
而是重新读取商品缓存。`+C48D10` 的清理步骤也不能遗漏。

## 旧骨架需要修正的地方

原文件的部分注释把运行时绝对地址的尾部当成 RVA，导致下面几组值少了 `0x510000`。
本次沿用原分析函数名，修正前三个骨架，不为同一地址另造业务名称。

| 原注释 | 正确 RVA | 沿用名称 |
| --- | --- | --- |
| `+EB1A10` | `+13C1A10` | `InitTempContext` |
| `+D16080` | `+1226080` | `WrapNumericContext` |
| `+D16160` | `+1226160` | `FillGoodsDirectionContext` |
| `+D18B90` | `+1228B90` | `BuildMarketTradeFraction` |
| `+EB2350` | `+13C2350` | `NormalizeAdvantage` |
| `+B17760` | `+1027760` | `UpdateAdvantageCache` |

`ReadOrComputeDirectionalTradeAdvantage` 和 `ComputeAbsoluteTradeAdvantage` 仍是 `Refresh` 内联逻辑的分析拆分，
不存在这两个独立 ABI 入口。旧 `CalculateDesirability` 骨架不是完整评分公式，应阅读
[真实评分反编译](../FakeCode/ghidra_refresh_20261003/function_11FC320.md)。

## 递归导出的范围和证据缺口

脚本以函数入口去重，使用广度优先遍历，不限制深度；在每个函数体内收集调用和跳出函数体的跳转，
解析 IAT 外部符号，将可确定目标加入队列。循环和共享子函数各导出一次。

本次有 **1,526 个可执行文件内函数、62 个外部导入符号、8,382 条边**，最短静态路径最大深度为 **22**。
全部 1,526 个内部函数获得 Ghidra 反编译文本，包含通用容器、内存操作、异常和报告路径。
外部导入符号没有本项目内的 DLL 函数体，仅记录符号和调用关系。

仍有 **1,178 个未解析间接调用位置和 47 个未解析计算跳转位置**；另有 62 个外部导入符号没有本项目内函数体。
虚函数目标取决于实际对象，跳转表也可能尚未恢复；不能凭一个函数指针表达式补造函数地址。
因此这里完整导出了**已解析静态边的递归闭包**，没有声称枚举全部运行时可达函数。

30 个函数有跳转表恢复或坏指令警告，保留在
[警告清单](../Output/ghidra_refresh_20261003/decompiler_warnings.json)。
其中 `+C3CAC0` 的 `+C3CE5C` 路径存在坏指令/截断警告；其局部伪代码不完整。
`ok` 仅指 Ghidra 返回文本，不代表控制流、参数类型和业务语义全部确认。
后续分析应同时查看原始反汇编和未解析边清单。

## 校验与复现

[verification.json](../Output/ghidra_refresh_20261003/verification.json) 保存了本次独立核对：

- 可执行文件：`D:\Games\Victoria3\Victoria 3\binaries\victoria3.exe`。
- SHA-256：`5fe215db840e311541950e2b57689a1c67c3fa4c85daf51949c433430a125e21`，与 Ghidra 导入记录一致。
- PE 时间戳字段：`0x6A3BF239`；映像基址与 Ghidra 一致。
- 历史根入口 182 条指令的字节全部与磁盘相同；24 个根调用位置和目标全部与 Ghidra 图相同。
- 所有内部函数都有伪代码文件；分片和索引少于 2,000 行，引用文件无缺失。

导出脚本是 [ExportRefreshTree.java](../Scripts/ghidra/ExportRefreshTree.java)，
名称登记和索引脚本是 [index_refresh_tree.py](../Scripts/ghidra/index_refresh_tree.py)。
复现时先把项目的 `.gpr` 和 `.rep` 复制到一个临时目录，避开原项目锁；
可使用本次副本 `C:\Users\infin\AppData\Local\Temp\vic3-ghidra-refresh-20261003`。
如果源项目正在保存，等保存完成后再复制，确保快照一致。

在项目根目录执行下面的 PowerShell 命令；`-readOnly` 保证脚本对副本的标签、指令和函数体修改不持久保存。

```powershell
python Scripts/ghidra/index_refresh_tree.py --prepare-names
$env:GHIDRA_HEADLESS_MAXMEM = '4G'
& 'D:/cebuild/ghidra/ghidra_12.1.4_PUBLIC/support/analyzeHeadless.bat' `
    'C:/Users/infin/AppData/Local/Temp/vic3-ghidra-refresh-20261003' vic3-rev `
    -process victoria3.exe -readOnly -noanalysis `
    -scriptPath 'D:/cebuild/ce-custom/Scripts/ghidra' `
    -postScript ExportRefreshTree.java `
    'D:/cebuild/ce-custom/Output/ghidra_refresh_20261003' `
    'D:/cebuild/ce-custom/FakeCode/ghidra_refresh_20261003' `
    'D:/cebuild/ce-custom/Scripts/ghidra/refresh_names.tsv'
python Scripts/ghidra/index_refresh_tree.py
```

脚本会复用已有 `status_*.json` 中成功的导出。程序版本、Image Base、名称表或恢复策略改变时，
应选择全新的输出目录，避免把不同版本的结果混在一起。
