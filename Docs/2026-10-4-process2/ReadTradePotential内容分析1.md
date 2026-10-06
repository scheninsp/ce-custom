# `ReadTradePotential` 内容分析（1）

## 结论

`UpdateStateTrades(+131C2B0)` 中标记为 `ReadTradePotential(state)` 的调用，实际目标是 `victoria3.exe+1210600`（Ghidra 地址 `0x141210600`）。该函数不是按商品计算贸易潜力，也没有发现读取 `AUTONOMOUS_TRADE_POTENTIAL_REVENUE_BASE_COST_FACTOR` 的证据。

它实际返回的是州的**世界市场接入度**（World Market Access）相关数值：

1. 游戏正在初始化时，直接返回 `state+0x58`。
2. 正常情况下解析州的市场/世界市场关联。
3. 无有效关联时返回 0，并可写入 `WORLD_MARKET_ACCESS_NO_HUB` 或 `WORLD_MARKET_ACCESS_BLOCKED` 诊断信息。
4. 有效关联时读取 `state+0x58`，再根据封锁程度计算修正后的接入度。
5. 使用定点比例 `100000`（100%），并将封锁影响按 `DAT_1458893E8` 计算；运行时该全局值对应 `75000`，与 `BLOCKADE_WORLD_MARKET_ACCESS_IMPACT_SCALING = 0.75` 一致。
6. 最终把结果写入第二个参数指向的输出槽并返回。

因此，`ReadTradePotential` 是此前静态伪代码中的误命名。`UpdateStateTrades` 的筛选条件实际近似为：州必须有正的世界市场接入度，而不是“贸易潜力大于零”。

## 调用证据

`Output/2026-10-3-process1/goal3_static_20261002/function_7FF777E0C2B0.md` 的 `+131C4C2`：

```text
mov r8d, 0
lea rdx, [rsp+58]
mov rcx, rbx
call 7FF777D00600
cmp qword ptr [rax], 0
jng ...
```

`7FF777D00600 - 7FF776AF0000 = +1210600`。因此该调用的真实目标为 `+1210600`，不是一个已确认的“Trade Potential”函数。

## 反编译结构

导出文件：`Output/2026-10-4-process2/read_trade_potential/function_1210600.c`。

反编译函数签名为：

```cpp
longlong* FUN_141210600(longlong state, longlong* output, longlong diagnostic);
```

完整分析伪代码来源：[FakeCode 世界市场接入度读取链](../../FakeCode/2026-10-4-process2/read_world_market_access.md)。下列为该来源的流程摘要：

```text
if game.initializing:
    *output = state+0x58
    return output

market = Resolve(state+0xB48)
hub = Resolve(market+0x48 的引用)
if hub 无效:
    可选写诊断文本
    *output = 0
    return output

if 世界市场路径查询结果为空:
    *output = 0
    return output
rawAccess = state+0x58
blockade = 读取关联对象的封锁值
blockadePenalty = fixed_mul(-blockade, 0.75)
access = rawAccess * max(1 + blockadePenalty, 0)
可选写 VALUE / BLOCKADE_LEVEL 诊断
*output = access
return output
```

实际机器码中的乘法使用定点整数，分母是 `100000`。`0x14447E050` 等字符串已通过运行时只读查询确认：

```text
WORLD_MARKET_ACCESS_NO_HUB
WORLD_MARKET_ACCESS_BLOCKED
WORLD_MARKET_ACCESS_FROM_MARKET_ACCESS
WORLD_MARKET_ACCESS_IS_HUB
WORLD_MARKET_ACCESS_HAS_HUB
```

这些字符串直接证明该函数属于世界市场接入度显示/计算链，而不是商品收益归一化链。

## 连通性与封锁路径的细节

`state+0xB48` 经 `+7C33B0` 解析后，从关联对象 `+0x48` 读取州引用，再经 `+7C96A0` 得到枢纽州。枢纽对象通过虚函数有效性检查后，构建两个索引集合，调用 `+13FC470`；返回容器的数量字段为零时，接入度返回零并可生成 `WORLD_MARKET_ACCESS_BLOCKED` 文本。该路径查询本身处理图节点/连接集合，尚未完整确认各索引类型和海峡规则，不应将其概括为简单的市场对象有效性检查。

封锁取值对象由 `hubRef == state+8` 决定：本州就是枢纽时取本州，否则取关联枢纽州。先调用 `+1230350`；仅该检查通过时读取对象 `+0x1D60` 的封锁值。该辅助函数在一个模式下返回关联对象 `+0x1CA` 的字节，在另一模式下遍历州的省份范围并调用省份有效性虚函数；其正式业务名称尚未独立确认。

令 `A` 为 `state+0x58` 的原始定点值，`B` 为通过上述检查取得的封锁定点值，`K` 为全局 `+58893E8`。仅当 `B>0` 才应用：

```text
delta = MulFixed(-B, K)
multiplier = max(100000 + delta, 0)
result = MulFixed(A, multiplier)
```

未封锁或资格检查失败时返回 `A`。初始化路径直接返回 `A`，跳过枢纽、连通性和封锁检查。源码并未把最终接入度钳制到 100%；钳制的是封锁乘数的下界。定点乘法按整数截断，并含较大数值分解路径，不能保证用浮点公式重算能逐位一致。

## 采集与证据边界

2026-10-06 使用现有 `ExportBreakpointFunction.java` 以 Ghidra `-readOnly -noanalysis` 导出，原项目修改已丢弃。PE 异常表范围为 `[+1210600,+1211175)`，653 条指令，2932 个已解码字节，函数范围长度为 2933 字节（差额为末尾填充字节），反编译成功且无错误消息。项目记录的可执行文件 SHA-256 为 `5fe215db840e311541950e2b57689a1c67c3fa4c85daf51949c433430a125e21`。

辅助导出包括 `+1230350`、`+13FC470`、`+12295A0`，保存在同一 Output 目录。Ghidra 输出是原始机器码的反编译，不代表所有类型和间接调用已恢复。

只读 CE 字符串与全局值采集回执：`Output/cycle_count/lua_20261006T102717840803Z_e0638ad9ea71.json`，确认六个接入度本地化键及 `+58893E8=75000`。本地 `00_defines.txt:860` 的封锁系数为 0.75；目前是读取地址、运行时数值和语义吻合的证据，尚未另行恢复该全局的 defines 注册过程。未调用目标函数、未单步或继续游戏，也未改变断点。

`+1210600` 可确认不存在商品收益归一化运算。尚未逐个恢复所有通用路径/文本辅助函数的整个递归闭包，因此本结论不声称全局范围内没有任何间接函数读取贸易潜力配置，也没有定位实际 Trade Potential 的计算函数。

## 与 0.25 参数的关系

在 `function_1210600.c` 和对应 TSV 中：

- 没有 `0.25` 浮点常量或等价的 `25000/100000` 定点乘法；
- 没有商品基础价格、商品 ID 遍历、单位收益或贸易潜力评分计算；
- 唯一明确的比例参数是封锁对世界市场接入度的 `0.75` 修正。

所以目前证据支持：

```text
AUTONOMOUS_TRADE_POTENTIAL_REVENUE_BASE_COST_FACTOR = 0.25
```

**不在 `+1210600` 中使用**。`00_ai.txt` 中该参数真正的消费者仍需通过其他调用链定位；不能用 `ReadTradePotential` 这次调用来证明它参与了 `UpdateStateTrades` 的州筛选。

## 对现有文档的修正建议

现有 `goal3_static_disassembly.md` 和 `州贸易更新函数UpdateStateTrades.md` 中的：

```text
if ReadTradePotential(state) <= 0: continue
```

应改名为更保守的：

```text
if ReadWorldMarketAccess(state) <= 0: continue
```

并保留真实地址注释：`victoria3.exe+1210600`。这是命名修正，不代表已经恢复了商品 Trade Potential 的完整算法。
