# `ComputeDirectionalAdvantage` 函数重新分析

## 1. 分析范围与命名说明

本文结合 `Docs/vic3_doc_copy/trade_center_model1.md` 的贸易中心模型，重新解释 `victoria3.exe+11FBDA0` 中被语义命名为 `ReadOrComputeDirectionalTradeAdvantage` / `ComputeDirectionalAdvantage` 的路径。

需要区分三个层次：

1. **单位绝对贸易优势**：某贸易中心、某商品、某方向的 `TA`，基础值为 100，并叠加静态优势项和百分比乘数。
2. **加权优势**：单位绝对优势乘以该贸易中心该商品该方向的交易量，即 `TA × Q`。
3. **相对贸易优势**：本贸易中心的加权优势份额除以交易量份额，再减 1，用于成交价格修正。

`+11FBDA0` 中写入候选对象 `c+0x40` 的值，应解释为**供贸易候选计算使用的方向绝对优势值或其缓存值**，不能直接称为 UI 显示的相对优势百分比。`ComputeDirectionalAdvantage` 是分析命名，不是已确认的游戏符号，也不是独立可调用函数边界。

## 2. 已确认的贸易中心模型

### 2.1 单位绝对贸易优势

根据 `Docs/vic3_doc_copy/trade_center_model1.md`，单个贸易中心、某商品、某方向的基础优势为：

```text
TA_base = 100
```

静态优势项按贡献相加，已整理出的项目包括：

```text
+2    × 市场区域占全球产量的百分比
+0.5  × 市场内由拥有贸易权公司控制的产量百分比
+1    × 奢侈品产量百分比（仅出口方向）
+1    × 流向贸易中心所有者拥有利益国家的贸易百分比
+2    × 流向条约港贸易中心的贸易百分比
-0.5  × 流向贸易中心所有者没有利益国家的贸易百分比
-0.75 × 与贸易中心所有者交战国家的贸易百分比
-1    × 流向禁运贸易中心所有者国家的贸易百分比
```

将静态项合计为 `TA_static` 后，当前模型支持“百分比乘数先相加、再统一乘以静态优势”的形式：

```text
TA = TA_static × (1 + m_power_bloc + m_market_capital
                    + m_trade_law + m_trade_capacity + ...)
```

已整理出的乘数来源包括：

```text
+25% External Trade I 阵营原则
+5%  市场首都贸易中心
+25% 自由贸易法
+最多 +0.5% / 每 100 贸易容量的贸易容量修正
```

贸易容量修正的通用上限、实际取整和适用条件仍需运行时样本确认。`trade_center_model1.md` 中日本山东约 `132`、荷兰约 `249` 的观测支持上述结构，但荷兰另一处 `261` 的显示值尚未解释。

### 2.2 加权优势与相对优势

单个贸易中心的加权优势为：

```texts
W_tc = TA_tc × Q_tc
```
TA_tc : 上面计算得到的单位绝对贸易优势
Q_tc：某个贸易中心，对某一种商品、在某一个贸易方向（进口或出口）上的交易量

同一商品、同一贸易方向下，全球加权优势为：

```text
W_total = Σ(TA_j × Q_j)
```

优势份额和交易量份额分别为：

```text
R_share = (TA_tc × Q_tc) / Σ(TA_j × Q_j)
V_share = Q_tc / ΣQ_j
```

相对贸易优势为：

```text
RelativeAdvantage = R_share / V_share - 1
```

代数约消后：

```text
RelativeAdvantage = TA_tc / TA_weighted_average - 1
TA_weighted_average = Σ(TA_j × Q_j) / ΣQ_j
```

这解释了为什么 UI 的相对优势可以为负：它比较的是本贸易中心的单位绝对优势与全球按交易量加权的单位优势，而不是把单位绝对优势简单转换成正百分比。

### 2.3 相对优势的后续用途

相对优势用于修正实际成交价格，而不是直接等于 `+11FBDA0` 中候选的 `c+0x40`：

```text
出口：RelativeAdvantage > 0 时，成交卖价高于世界市场价
进口：RelativeAdvantage > 0 时，成交买价低于世界市场价
```

与 [贸易中心模型第 4 节](../vic3_doc_copy/trade_center_model1.md#4-相对优势--成交价统一工作模型尚未源码级确认) 统一的两方向工作公式为：

```text
r = RelativeAdvantage = R_share / V_share - 1
M = 1 + 0.25 × r
出口成交价 P_export = P_world × M
进口成交价 P_import = P_world / M
```

这组公式要求 `M > 0`，尚未源码级确认；出口式暂作候选，进口式有主模型中的观测支持。相对优势 `+100%` 即 `r = 1`，此时出口价提高 `25%`，进口价降低 `20%`，不能将二者统称为价格改善 `25%`。本地系数 `0.25` 也不能证明存在 `25%` 的价格改善上限。

官方开发日志没有给出这组精确公式，其价格零和描述与未归一化的进口倒数模型尚未闭合；外部来源、Wiki 访问限制及配置证据见主模型第 4.0 节。是否还有钳位或归一化需继续确认。价格层、利润层和贸易候选评分层使用不同上下文，不能仅凭 UI 百分比反推 `c+0x40` 的存储值。


### 2.4 已从 opcode 证实公式 P_export = P_world × M 和 P_import = P_world / M

**有，而且比此前文档描述的证据更强：现有 opcode 已能支持“一个方向乘倍率，另一个方向乘其倒数”。** 但把它完整命名为最终 `P_export`、`P_import`，还差价格基准和边界函数的确认。

**1. 系数 0.25 已有直接采集证据**
此前分析主要看 `.asm`，遗漏了 `.json` 保存的操作数信息：

- `Output/check_trade_advantages1_20261003/function_9C21A0.json:202` 标出了配置名 `TRADE_CENTER_ADVANTAGE_PRICE_MULTIPLIER`。
- 同文件 `:1551` 将对应存储位置指向 `victoria3.exe+5889E10`，采集注释显示值为 `0x61A8 = 25000`。
- `Output/check_trade_advantages1_20261003/function_13A5280.json:111` 确认价格修正函数读取该位置，并保留相同读数。

定点单位为 `100000`，所以这里确实对应 **0.25**，并非仅从配置文本推测。

**2. `+13A5280` 的倍率计算可以还原**
设入口相对优势比值为定点整数 \(X\)，中性值 \(S=100000\)，配置值 \(C=25000\)。其普通数值路径为：

\[
T=
\begin{cases}
X-\operatorname{trunc}\!\left((X-S)(S-C)/S\right), & X>S\\
X+\operatorname{trunc}\!\left((S-X)(S-C)/S\right), & X\le S
\end{cases}
\]

依据：`Output/check_trade_advantages1_20261003/function_13A5280.asm:9` 和同文件 `:54`。

**忽略定点截断**，两条路径都化简为：

\[
\frac TS=1+0.25\left(\frac XS-1\right)
\]

因此，若文档中的带符号相对优势 \(r=X/S-1\)，就得到：

\[
M=1+0.25r
\]

随后方向分支非常明确：

- **方向 0**：计算 `10000000000 / T`，即定点形式的 **\(1/M\)**。
- **非零方向**：直接写回 `T`，即 **\(M\)**。

依据：`Output/check_trade_advantages1_20261003/function_13A5280.asm:97`。这里的实际跳转目标是 `+13A5439`，旧分析中写成 `+13A541F` 的注释不准确。

**3. 上层确实将倍率乘到价格基准上**
`+140A6B0` 连续调用 `+13A3B10`、`+13A5280`，随后把返回倍率与 `+13A3280` 准备的基准值做定点乘法。依据：`Output/check_trade_advantages1_20261003/function_140A6B0.asm:139`。

所以，在尚未触发后续限价时，现有证据支持：

\[
P_{\text{方向1}}\approx P_{\text{基准}}M,\qquad
P_{\text{方向0}}\approx P_{\text{基准}}/M
\]

**仍需保留的边界**
- `0≈进口、1≈出口` 有收益差值正负和短缺逻辑支持，但还不是有符号枚举的直接证明。
- `P_基准` 是否精确等于 UI 当前显示的 `P_world`，还需展开 `+13A3280` 及其调用的 `+13FAC30`。
- **已经发现上下界裁剪**：上层调用 `+1726A10`、`+1726AF0` 获取两个边界，再裁剪修正后的值；见 `Output/check_trade_advantages1_20261003/function_140A6B0.asm:199`。因此最终价格不能无条件只写成乘法或除法。

**结论：这组公式已不只是观测拟合，倍率层有机器码支持；最终成交价的完整公式，还需补齐价格基准、限价边界及整数截断。** 本次仅检查现有导出，没有修改文档或读取游戏运行时。



## 3. `+11FBDA0` 中的实际数据流

### 3.1 候选字段和缓存读取

候选对象中目前可以使用以下字段解释：

```text
c+0x00  商品对象指针
c+0x08  贸易方向
c+0x28  州引用或相关状态引用
c+0x38  每单位贸易容量对应的商品数量
c+0x40  方向绝对优势或其缓存结果
```

`+11FBDA0` 先计算并写入 `c+0x38`，然后读取商品 ID，根据 `c+0x08` 的方向选择两套方向数据表：

```text
方向 0：基址附近 +0x7D0 / +0x7E8
方向 1：基址附近 +0x780 / +0x798
```

商品 ID 先通过位图检查，随后按 `goods_id × 8` 读取优势值，并写入：

```asm
+11FBE60  mov [r14+40], rax
```

其中 `r14` 是候选对象，`rax` 是方向表读取到的值。

### 3.2 缓存未命中时的计算路径

如果读取结果不大于零，代码进入方向分支，构造临时计算上下文。

方向 1 的主要调用顺序：

```text
+11FBE99  call +EB1A10
+11FBEA4  call +D16080
+11FBEB8  call +D16160
+11FBEC5  call +D18B90
+11FBED7  call +EB2350
+11FBEF0  与 100000 比较并执行下限处理
+11FBF03  call +738D10
+11FBF93  call +B17760
```

方向 0 使用对应的另一组调用点：

```text
+11FBF18  call +EB1A10
+11FBF23  call +D16080
+11FBF36  call +D16160
+11FBF43  call +D18B90
+11FBF55  call +EB2350
+11FBF6E  与 100000 比较并执行下限处理
+11FBF81  call +738D10
+11FBF93  call +B17760
```

当前能确认的参数关系是：

```text
rcx = +D16160 的州/市场相关对象
rdx = 临时上下文地址 rsp+0x40
r8  = 商品对象
r9b = 贸易方向
```

`+D16160` 把州/市场、商品和方向相关输入写入临时数值上下文；`+D18B90` 处理方向对应的优势入口和 `TRADE_FRACTION` 相关输入；`+EB2350` 对上下文中的数值表达式进行定点求值或组合。

### 3.3 当前最合理的 `ComputeDirectionalAdvantage` 伪代码

下面是结合贸易中心模型后的语义伪代码，不是逐指令 C++ 还原。

```cpp
// 功能：读取或计算指定州/市场、商品和方向的绝对贸易优势。
// 入参：stateOrMarket 为州或其关联市场对象；goods 为商品对象；direction 为贸易方向。
// 返回：用于候选计算的正向定点优势值；具体缓存写入位置仍需运行时确认。
// 地址：victoria3.exe+11FBDA0 内联路径。
int64 ComputeDirectionalAdvantage(StateOrMarket* stateOrMarket,
                                  Goods* goods,
                                  uint8 direction)
{
    DirectionTable* table = SelectDirectionTable(stateOrMarket, direction);
    int32 goodsId = ReadGoodsId(goods);

    if (DirectionTableContains(table, goodsId)) {
        int64 cached = ReadDirectionGoodsValue(table, goodsId);
        if (cached > 0)
            return cached;
    }

    TempContext context;
    InitTempContext(&context, 0);                  // +EB1A10
    WrapNumericContext(&context);                  // +D16080
    BuildStateMarketGoodsDirectionContext(
        stateOrMarket, &context, goods, direction); // +D16160
    AddDirectionalAdvantageTradeFractionInputs(
        stateOrMarket, &context, direction);       // +D18B90

    int64 evaluated = EvaluateDirectionalFixedPointExpression(
        &context);                                  // +EB2350
    int64 fixedInput = evaluated < 100000 ? 100000 : evaluated;

    int64 result = UpdateDirectionalAdvantageCache(
        table, goods, fixedInput);                  // +738D10 / +B17760
    return result;
}
```

结合已确认模型，经济意义可以写成：

```text
TA_static = 100 + 各项静态优势贡献
TA_unit = TA_static × (1 + 各项百分比乘数)
```

但目前还不能把 `+D16160`、`+D18B90` 和 `+EB2350` 直接写成以下任一种未经验证的形式：

```text
TA = TA_static + market_fraction
TA = TA_static × market_fraction
TA = TA_static × (1 + market_fraction)
```

当前静态反汇编只确认了临时上下文、方向入口、`TRADE_FRACTION` 和定点下限，尚未确认每个上下文槽位对应的业务字段，以及 `+EB2350` 内部的加法、乘法或插值顺序。

## 4. 与相对优势公式的关系

当前最合理的完整业务链是：

```text
ComputeDirectionalAdvantage
    ↓
得到单个贸易中心、商品、方向的单位绝对优势 TA
    ↓
TA × 交易量 Q
    ↓
得到全球同方向的加权优势份额
    ↓
除以交易量份额，再减 1
    ↓
RelativeAdvantage
    ↓
修正进口/出口成交价格
    ↓
影响贸易中心利润和后续贸易流量
```

`+11FBDA0` 的候选对象刷新流程是：

```text
c+0x38 = 每容量商品数量
c+0x40 = 方向绝对优势
c+0x30 = 短缺指标
c+0x18 = 单位收益
c+0x10 = 基础收益
c+0x20 = 最终意愿评分
```

`c+0x40` 可能参与候选有效性、贸易调整或其他外围计算，但现有 `+11FBDA0` 反汇编没有直接证明它在 `+11FC080` 或 `+11FC320` 中以哪一种算术形式进入评分，必须通过运行时 Access 追踪确认实际读取点。

## 5. 仍需要断点确认的地址和采集内容

### 5.1 首先确认候选优势的写入值

对以下两个指令地址设置执行断点：

```text
victoria3.exe+11FBE60
victoria3.exe+11FC008
```

采集内容：

```text
r14                         候选对象地址 c
r14+0x00                    商品对象指针
[r14+0x08]                  方向值
[r14+0x28]                  州/状态引用
[r14+0x38]                  quantity
rax（+11FBE60 时）          缓存读取值
rsi（+11FC008 时）          最终写入值
rbx                         商品 ID
写入前后的 [r14+0x40]       候选优势值
调用栈                       刷新来源和后续调用者
```

同时记录：

```asm
+11FBE64  test rax,rax
+11FBE67  jg  +11FC041
```

以区分缓存命中和重新计算路径。

### 5.2 追踪候选优势后续是否被读取

命中 `+11FBE60` 或 `+11FC008` 后，计算：

```text
advantage_address = r14 + 0x40
```

对这个动态地址设置 Cheat Engine 的硬件 `Read/Write` 访问断点，继续运行并记录：

```text
触发指令地址
访问类型：读或写
触发时的候选对象地址
触发时的商品 ID 和方向
访问前后寄存器值
调用栈
```

重点查找：

```asm
mov  reg,[candidate+40]
cmp  reg,[candidate+40]
imul reg,[candidate+40]
```

如果只捕获到 `+11FBE60` 和 `+11FC008` 的写入，说明当前测试场景尚未发现后续直接读取，应扩大到候选对象的下一次刷新或贸易调整过程。

### 5.3 追踪单位绝对优势的计算输入

对以下地址设置断点：

```text
victoria3.exe+D16160
victoria3.exe+D18B90
victoria3.exe+EB2350
victoria3.exe+738D10
victoria3.exe+B17760
```

每次至少采集：

```text
进入函数时 rcx、rdx、r8、r9
返回前后的 rax
rdx 指向的临时对象内容
rsp+0x40 临时上下文内容
rsp+0xD0 表达式输出/端点对象内容
rsp+0xC0 的 100000 基线
商品对象中的商品 ID
州/市场对象指针及 [state+0x18B0] 关联对象
方向值
```

重点目标：

| 地址 | 重点 | 必须确认的内容 |
|---|---|---|
| `+D16160` | 州/市场、商品、方向输入构造 | 哪些临时槽位对应基础 100、静态贡献、商品/市场比例 |
| `+D18B90` | 方向优势入口与贸易比例输入 | `ADVANTAGE_ENTRY_IMPORT_SUFFIX`、`ADVANTAGE_ENTRY_EXPORT_SUFFIX`、`TRADE_FRACTION` 的实际值及方向选择 |
| `+EB2350` | 定点表达式求值 | 输入端点、输出值、是否执行插值/乘法/加法以及缩放因子 |
| `+738D10` | 结果对象或缓存条目处理 | 传入值如何封装、是否发生额外缩放或舍入 |
| `+B17760` | 方向商品缓存更新 | 缓存基址、商品索引、最终写入值和返回值 |

### 5.4 追踪方向表缓存地址

在 `+11FBDA0` 中记录：

```asm
方向 0：mov rax,[rbp+7D0]，随后 mov rax,[rax+rbx*8]
方向 1：mov rax,[rbp+780]，随后 mov rax,[rax+rbx*8]
```

采集：

```text
rbp                         方向表或状态对象相关基址
rbx                         商品 ID
[rbp+0x780] / [rbp+0x7D0]   方向商品数组指针
[rbp+0x798] / [rbp+0x7E8]   商品有效位图
[array+goods_id*8]          原始缓存优势值
```

如果使用 `Find out what accesses this address`，追踪目标应是运行时解析出的：

```text
direction_array + goods_id × 8
```

而不是固定写死 `victoria3.exe+0x780` 或 `victoria3.exe+0x7D0`，因为这些是对象内部偏移，不是模块绝对地址。

### 5.5 采样设计

为了把模型公式和机器码输入一一对应，至少采集以下成对样本：

```text
同一商品、同一方向、不同贸易中心
同一贸易中心、同一商品、进口与出口方向
同一贸易中心、同一方向、贸易容量变化前后
同一贸易中心、同一方向、拥有利益/禁运/战争状态变化前后
```

每个样本必须在同一个暂停时点记录：

```text
单位绝对优势 TA
交易量 Q
TA × Q
全球同方向优势总和
全球同方向交易量总和
UI 相对优势
世界市场价和实际成交价
+D16160、+D18B90、+EB2350 的输入输出
```

最终要验证：

```text
机器码上下文输入 → TA_static 各项 → 百分比乘数 → 单位 TA
单位 TA 与 Q → 加权优势
加权优势与 Q → RelativeAdvantage
RelativeAdvantage → 成交价格修正
```

在完成上述采集前，应将 `ComputeDirectionalAdvantage` 视为“已知经济模型约束下的语义伪代码”，而不是已经逐字段、逐指令确认的完整函数公式。
