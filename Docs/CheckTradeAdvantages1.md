# Trade Advantage 静态反编译检查

## 1. 范围与采集方式

本次只使用 Cheat Engine MCP 的只读 opcode 采集、函数边界和本地 `victoria3.exe` 磁盘字节校验，没有执行单步、继续运行、读写游戏内存或动态分析。

- 游戏模块基址：`7FF776AF0000`
- 用户断点：`victoria3.exe+11FBDA0 = 7FF777CEBDA0`
- 版本文件：`D:\Games\Victoria3\Victoria 3\binaries\victoria3.exe`
- 采集目录：`Output\check_trade_advantages1_20261003`
- 采集结果与磁盘文件逐条 opcode 一致；函数边界优先使用 PE `.pdata`，并合并连续 chained unwind 函数块。

本报告的地址均使用模块相对地址，例如 `+11FBDA0`。新增语义名称只在本报告中使用，并在名称后保留对应地址；这些名称不是游戏官方符号。

## 2. 结论摘要

目前可以把 `Refresh` 中的候选优势字段还原为以下三层：

```text
缓存读取
    -> 方向商品表中的单位绝对优势 TA
缓存未命中
    -> 构造州/市场/商品/方向上下文
    -> 读取优势来源并进行定点合成
    -> 以 100000 为定点基准做归一化/边界处理
    -> 写回方向商品表
后续价格链
    -> 计算相对优势或价格修正量
    -> 乘以价格倍率，并按进口/出口方向取正负或倒数
```

最可靠的静态结论如下：

1. `+11FBDA0` 的 `c+0x40` 是方向商品表中的单位绝对优势缓存值，不是 UI 的相对优势百分比。
2. 绝对优势的核心计算链位于 `+11FBDA0` 内联代码及其调用的 `+1226160`、`+1228B90`、`+13C2350`。
3. `+1226160` 明确引用了优势来源字符串：`ADVANTAGE_FROM_TRADE_AGREEMENTS_ENTRY`、`ADVANTAGE_FROM_TREATY_PORT_ENTRY`、`ADVANTAGE_FROM_POWER_BLOC_ENTRY`、`ADVANTAGE_FROM_RELIGION_ENTRY`、`ADVANTAGE_FROM_EMBARGO_ENTRY`、`ADVANTAGE_FROM_AT_WAR_ENTRY`、`ADVANTAGE_FROM_INTEREST_TIER_ENTRY`，因此绝对优势不是单一字段读取。
4. `+13C2350` 是一个已能逐指令还原的定点组合/归一化函数：使用 `0x186A0 = 100000`、`0xE = 14` 位移和有符号乘除，处理加法、乘法、上下限及插值，不是简单的 `abs()`。
5. 游戏定义文件确认价格修正常数为 `TRADE_CENTER_ADVANTAGE_PRICE_MULTIPLIER = 0.25`，并且价格公式作用于“相对优势减 1”。这与 `+13A5280` 的定点代码结构吻合，但仅凭当前调用者不能把所有价格层输入字段全部命名。

## 3. `+11FBDA0`：绝对优势缓存读取与未命中分支

### 3.1 方向表读取

`+11FBDA0` 先完成数量写入：

```asm
+11FBDD7  call +122AB50
+11FBDDC  mov r8,[rax]
+11FBDDF  mov [r14+38],r8       ; c->quantity
```

随后从商品对象读取 ID，并按方向选择两套缓存：

```asm
方向 0：
+11FBE0D  mov rcx,[rbp+rax*8+7E8] ; 商品存在位图
+11FBE1B  mov rax,[rbp+7D0]       ; 商品优势数组

方向 1：
+11FBE42  mov rcx,[rbp+rax*8+798] ; 商品存在位图
+11FBE50  mov rax,[rbp+780]       ; 商品优势数组
```

商品 ID 的存在性通过 `bt` 检查，存在时按 `goodsId * 8` 读取：

```asm
+11FBE15  bt rcx,rdx
+11FBE22  mov rax,[rax+rbx*8]
+11FBE60  mov [r14+40],rax       ; c->advantage
+11FBE64  test rax,rax
+11FBE67  jg +11FC041            ; 正值直接进入后续 Refresh
```

因此当前伪代码应写成：

```cpp
// 功能：读取指定方向和商品的单位绝对贸易优势；缓存为非正值时进入计算链。
// 入参：candidate 为 Refresh 候选对象；返回：无，结果写入 candidate->advantage。
// 地址：victoria3.exe+11FBDA0。
void ReadOrComputeDirectionalTradeAdvantage(Candidate* candidate)
{
    int32 goodsId = candidate->goods->id;
    DirectionTable* table = SelectDirectionTable(candidate->state, candidate->direction);

    int64 cached = table->contains(goodsId)
        ? table->values[goodsId]
        : 0;
    candidate->advantage = cached;

    if (cached <= 0)
        candidate->advantage = ComputeDirectionalAdvantage(candidate);
}
```

这里的 `candidate->advantage` 对应 `c+0x40`，不是相对优势百分比。

### 3.2 未命中后的调用链

方向 1 和方向 0 的调用序列相同，只是传给核心函数的 `direction` 分别为 `1` 和 `0`：

```text
+13C1A10  InitDirectionalValueContext
+1226080  WrapDirectionalValueContext
+1226160  BuildDirectionalAdvantageContext
+1228B90  AddMarketTradeFractionContext
+13C2350  NormalizeDirectionalAdvantage
+C48D10   临时资源/句柄生命周期辅助
+1027760  WriteOrCreateDirectionalAdvantageCache
```

在 `+11FBDA0` 中的参数关系：

```asm
+11FBEA9  movzx r9d,bl       ; direction = 1
+11FBEAD  mov r8,r12         ; goods
+11FBEB0  lea rdx,[rsp+40]    ; 临时上下文
+11FBEB5  mov rcx,r13        ; state/market 相关对象
+11FBEB8  call +1226160
```

方向 0 分支的 `+11FBF28 xor r9d,r9d` 将方向明确置零。

## 4. 绝对优势计算：`+1226160` 及其上下文

### 4.1 `+1226080`：上下文包装

`+1226080` 建立一个短期的数值计算/表达式上下文，调用 `+6DE750` 初始化内部对象，尾部负责字符串/小对象清理。它没有直接读取商品优势数值，因此不应命名为绝对优势公式本体。

```cpp
// 功能：把临时方向数值上下文包装为表达式计算对象。
// 入参：valueContext 为调用者提供的上下文；返回：无，生命周期在调用期间维护。
// 地址：victoria3.exe+1226080。
void WrapDirectionalValueContext(TempValueContext* valueContext);
```

### 4.2 `+1226160`：核心优势来源构造

入口保存四个关键输入：

```asm
+1226160  mov [rsp+08],rcx    ; state/market
+122616B  mov [rsp+10],rdx    ; 临时上下文
+1226167  mov [rsp+18],r8     ; goods
+1226163  mov [rsp+20],r9b    ; direction
```

随后：

```asm
+12261A3  call +2C7550
+12261A8  mov r14,[rax+120]
+12261AF  add r14,508          ; 取方向/优势数据区域
+12261B6  mov r13,[r15+18B0]  ; state 关联对象
```

该函数内有大量以下形式的算术：

```asm
imul ..., ...
sar ...,0E
idiv ...
imul ...,000186A0
```

这证明优势值使用定点乘除和比例合成。它还通过表达式条目字符串构造多个输入。静态字符串证据包括：

```text
ADVANTAGE_FROM_TRADE_AGREEMENTS_ENTRY
ADVANTAGE_FROM_TREATY_PORT_ENTRY
ADVANTAGE_FROM_POWER_BLOC_ENTRY
ADVANTAGE_FROM_RELIGION_ENTRY
ADVANTAGE_FROM_EMBARGO_ENTRY
ADVANTAGE_FROM_AT_WAR_ENTRY
ADVANTAGE_FROM_INTEREST_TIER_ENTRY
CONCEPT_IMPORTS
CONCEPT_EXPORTS
```

所以，当前能安全还原的经济模型是：

```text
TA_raw = TRADE_CENTER_ADVANTAGE_BASE
       + Σ(方向、市场、贸易协议、条约港、阵营、宗教、禁运、战争、利益等级等贡献)
TA = 定点归一化并经过边界处理后的 TA_raw
```

游戏定义文件给出基础项：

```text
TRADE_CENTER_ADVANTAGE_BASE = 100
TRADE_CENTER_ADVANTAGE_MARKET_AREA_PRODUCTION_FACTOR = 200
TRADE_ADVANTAGE_COMPANY_CHARTER_FACTOR = 50
TRADE_CENTER_ADVANTAGE_MARKET_PRESTIGE_GOOD_FACTOR = 100
TRADE_CENTER_ADVANTAGE_TRADE_AGREEMENT_FACTOR = 100
TRADE_CENTER_ADVANTAGE_TREATY_PORT_FACTOR = 200
TRADE_CENTER_ADVANTAGE_EMBARGO_FACTOR = -100
TRADE_CENTER_ADVANTAGE_AT_WAR_FACTOR = -75
```

这些定义值与 `+1226160` 中的表达式条目相互印证，但当前没有足够证据把每个定义值逐一映射到某个具体栈槽及最终加法顺序。

### 4.3 `+1228B90`：市场贸易分数/比例输入

`+1228B90` 从 `state + 0x18B0` 取得关联对象，调用 `+6DDFB0` 和 `+D21B10` 查询市场数据，然后执行与 `+1226160` 相同的定点比例运算。该函数至少生成一个市场侧比例值，并把它加入后续表达式上下文。

因此旧文档中的 `BuildMarketTradeFraction` 可以保留为分析名，但应标注为：

```cpp
// 功能：把市场贸易比例及相关市场条件加入方向优势计算上下文。
// 入参：stateOrMarket 为州/市场对象；context 为临时表达式上下文；返回：无，结果写入 context。
// 地址：victoria3.exe+1228B90。
void AddMarketTradeFractionContext(StateOrMarket* stateOrMarket,
                                   TempValueContext* context);
```

### 4.4 `+13C2350`：定点归一化、插值和边界

该函数的入口字段：

```asm
+13C2357  mov r11,[rcx+10]
+13C2363  add r11,000186A0
+13C236A  cmp byte ptr [rcx+30],00
+13C2390  mov rcx,[rbx+08]
+13C239D  mov r12,000000016A09E666
+13C23B4  mov rsi,rcx
+13C23B4  mov rsi,rcx
```

典型安全算术路径为：

```text
product = signed_mul(valueA, valueB)
product = arithmetic_shift_right(product, 14)
product = signed_divide(product, 0x29F16B11C6D1E109 对应的定点比例)
result = result + contribution
```

当乘法可能溢出时，代码改用 `cmovl/cmovg` 选择边界后进行分段插值；最后使用 `+0x20`、`+0x28` 的上下界约束结果，并写回调用者提供的输出指针：

```asm
+13C2587  cmp rdx,r10
+13C258A  jnl +13C25A0
+13C258C  mov [rdi],rbp
+13C25A0  cmp rdx,rsi
+13C25A3  cmovg rdx,r14
+13C25A7  mov [rdi],rdx
```

当前最准确的命名是 `NormalizeDirectionalAdvantage`，而不是 `ComputeAbsoluteTradeAdvantage`：它负责定点组合和边界，输入来源由 `+1226160` 与 `+1228B90` 准备。

## 5. 缓存写回：`+1027760`

`+1027760` 的作用可以静态确认：

```asm
+102776F  movsxd rsi,dword ptr [rdx+10] ; goods id
+1027773  mov rdi,rcx                   ; direction table
+1027778  mov rbx,r8                    ; fixed value
+102777B  call +1026630                 ; 检查商品 ID
+10277B5  mov rax,[rdi+08]
+10277B9  mov [rax+rsi*8],rbx            ; 写商品优势值
+10277C2  and [rcx+20],r8                ; 清除/更新存在位图
```

缓存未命中时它会建立商品位图；后续 `+11FBF93` 再次从方向表读取写回的值：

```asm
+11FBF8D  mov r8,rbx
+11FBF90  mov rdx,r12
+11FBF93  call +1027760
+11FBF98  ...
+11FC008  mov [r14+40],rax
```

所以 `+1027760` 应命名为 `WriteOrCreateDirectionalAdvantageCache`，不能误称为相对优势计算函数。

## 6. 相对优势：静态可确认的数学结构

相对优势不是 `+11FBDA0` 直接写入的 `c+0x40`。根据现有函数和定义文件，最稳定的数学关系是：

```text
TA_i       = 某贸易中心、商品、方向的单位绝对优势
W_i        = TA_i × Q_i
TA_average = Σ(TA_i × Q_i) / ΣQ_i
RelativeAdvantage = TA_i / TA_average
```

若 UI 或文档把中性值写成 `0`，则显示值为：

```text
RelativeAdvantageDelta = TA_i / TA_average - 1
```

这两个写法只是是否把“中性 1”提前减掉的差别。静态代码中大量出现：

```asm
imul value,0x186A0
idiv denominator
```

说明相对量以 `100000` 为定点单位计算。相对优势可以为负（若使用减一后的显示形式），而绝对优势缓存必须满足 `c+0x40 > 0` 才能继续刷新候选。

### 6.1 相对优势候选函数：`+13A3B10`

`+13A3B10` 的入口立即按 `r9b` 分方向：

```asm
+13A3B40  movzx eax,r9b
+13A3B75  test r9b,r9b
+13A3B78  je  +13A3C14
+13A3B8C  mov qword ptr [rdx],000186A0
```

方向为特殊分支时直接返回定点基准 `100000`；其他方向读取多个市场/贸易数据，并执行：

```text
weightedPart = value × 100000 / denominator
remainderPart = remainder × 100000 / denominator
result = weightedPart + remainderPart
```

随后多次对结果再次做 `value × 100000 / denominator`。这种结构与“加权优势份额/数量份额”的定点除法相符。函数本体没有出现价格倍率常数 `0.25`，所以它更接近相对优势/加权比例计算，而不是最终价格函数。

当前伪代码：

```cpp
// 功能：按贸易方向将单位优势与贸易量/市场总量进行定点归一化，生成相对优势候选值。
// 入参：stateOrMarket、output、goodsContext、direction；返回：output 指针。
// 地址：victoria3.exe+13A3B10。
FixedPoint* ComputeRelativeTradeAdvantage(
    StateOrMarket* stateOrMarket,
    FixedPoint* output,
    GoodsContext* goodsContext,
    uint8 direction)
{
    if (direction == 2)
        *output = 100000;
    else
        *output = WeightedAdvantageDividedByTradeQuantity(
            stateOrMarket, goodsContext, direction);
    return output;
}
```

`WeightedAdvantageDividedByTradeQuantity` 是语义名，当前尚不能把它作为独立游戏函数名使用。

## 7. 相对优势影响价格：`+13A5280`

`+13A5280` 明确是定点倍率/差值处理函数。其关键路径：

```asm
+13A5289  mov r9d,000186A0       ; 100000
+13A52A7  cmp rdx,r9
+13A52B0  sub r9,[7FF77C379E10]  ; 全局定点基准/价格输入
+13A52B7  lea rcx,[rdx-000186A0]
...
+13A5354  sub r10,rdx
+13A5408  jne +13A541F
+13A541F  mov rax,00000002540BE400
+13A542B  idiv r10
+13A542E  mov [r11],rax
+13A5439  mov [r11],r10
```

它先计算相对输入与中性值 `100000` 的差，再按方向选择正向、反向或倒数形式。结合游戏定义：

```text
TRADE_CENTER_ADVANTAGE_PRICE_MULTIPLIER = 0.25
```

价格层的语义公式应写成：

```text
priceMultiplier = 1 + (RelativeAdvantage - 1) × 0.25
```

进口/出口方向随后使用不同的方向分支；其中一个方向会对倍率执行倒数或等价的反向定点除法。因此可以确认“相对优势影响价格”，但不能仅凭 `+13A5280` 确认它是否就是最终的进口/出口成交价函数：它还接收调用者提供的定点输入，实际价格对象在其上层构造。

当前伪代码：

```cpp
// 功能：把相对优势定点值转换为贸易价格倍率，并按方向处理正向或反向倍率。
// 入参：priceContext 为价格计算上下文；relativeAdvantage 为 100000 定点相对优势；direction 为贸易方向。
// 返回：写回 priceContext 的 100000 定点价格倍率。
// 地址：victoria3.exe+13A5280。
int64 ApplyRelativeAdvantageToPrice(
    PriceContext* priceContext,
    int64 relativeAdvantage,
    GoodsContext* goodsContext,
    uint8 direction)
{
    int64 neutral = 100000;
    int64 delta = relativeAdvantage - neutral;
    int64 multiplier = neutral + FixedMultiply(delta, 25000); // 0.25

    if (direction == IMPORT_DIRECTION)
        return FixedDivide(neutral * neutral, multiplier);
    return multiplier;
}
```

`IMPORT_DIRECTION` 的具体数值不能只根据当前静态调用点命名；已有 `+11FBDA0` 代码只确认方向值 `0` 与 `1` 的两套缓存选择。

## 8. `+140A6B0`：价格/优势差值的另一个候选路径

另外采集到的 `+140A6B0` 末段：

```asm
+140A9E3  mov rax,[rax]
+140A9E6  cmp rbx,rax
+140A9E9  jl  +140A9F5
+140A9EB  cmp rbx,rdi
+140A9F1  cmovg rax,rdi
+140A9F5  test r13b,r13b
+140A9F8  je   +140AA16
+140A9FE  je   +140AA09
+140AA09  sub rax,[rsp+B0]
+140AA11  mov [r14],rax
+140AA16  sub rcx,rax
+140AA21  mov [r14],rcx
```

该函数对上下界裁剪后的值与基准值做差，并按方向写入差值。它很可能属于价格或贸易优势差异层，但当前采集到的调用者不是 `+11FBDA0` 的直接路径，且尚未获得完整上层语义，因此不能把它确定为最终成交价格函数。它应作为下一轮静态交叉引用的候选，而不是本轮结论中的确定函数。

## 9. 与旧伪代码的修正

`FakeCode\trade_advantage_functions.md` 中旧的以下命名需要按本报告理解：

```text
ComputeAbsoluteTradeAdvantage
BuildMarketTradeFraction
NormalizeAdvantage
UpdateAdvantageCache
```

更准确的地址映射为：

| 语义名称 | 地址 | 结论 |
|---|---:|---|
| `ReadOrComputeDirectionalTradeAdvantage` | `+11FBDA0` | 已确认是内联缓存读取/未命中分支 |
| `BuildDirectionalAdvantageContext` | `+1226160` | 已确认构造优势来源和定点上下文 |
| `AddMarketTradeFractionContext` | `+1228B90` | 已确认加入市场比例相关输入 |
| `NormalizeDirectionalAdvantage` | `+13C2350` | 已确认定点乘除、插值和边界处理 |
| `WriteOrCreateDirectionalAdvantageCache` | `+1027760` | 已确认商品 ID 表写回/建立位图 |
| `ComputeRelativeTradeAdvantage` | `+13A3B10` | 高可信候选，定点加权除法结构已确认 |
| `ApplyRelativeAdvantageToPrice` | `+13A5280` | 高可信候选，按中性值和方向处理价格倍率 |
| `PriceOrAdvantageDeltaCandidate` | `+140A6B0` | 仅候选，确认了裁剪后差值写回 |

## 10. 当前不能静态确认的内容

以下内容本轮不做过度推断：

1. `+1226160` 中每一个表达式条目与具体 `00_defines.txt` 常数的逐项映射。
2. `+1228B90` 生成的市场比例究竟对应生产份额、消费份额、贸易份额还是多个比例的组合。
3. `+13A3B10` 的四个参数中每个寄存器对应的完整 C++ 类型。
4. `+13A5280` 的两个方向值具体哪一个是进口、哪一个是出口。
5. `+140A6B0` 是否是最终成交价函数，还是被更上层价格函数复用的差值辅助函数。
6. `+11FBDA0` 的 `c+0x40` 是否在 `+11FC080` 或 `+11FC320` 中直接参与最终评分；当前报告只确认它是进入后续流程的正值门槛和候选字段。

## 11. 下一步建议（仍可保持纯静态）

若继续不做动态分析，优先顺序应为：

1. 对 `+13A3B10` 的所有静态交叉引用做 `code_find_references`，确认它是否被价格计算路径调用。
2. 对 `+13A5280` 的所有调用者导出完整函数，寻找传入 `relativeAdvantage` 和价格定义常数的位置。
3. 对 `+140A6B0` 的调用者导出函数图，确认 `[rsp+B0]` 的对象字段和 `r13b` 的方向枚举。
4. 继续沿 `+1226160` 中的 `ADVANTAGE_FROM_*_ENTRY` 条目，分别导出对应表达式读取函数，建立定义常数到上下文槽位的映射。

## 12. 后续静态追踪结果（2026-10-02）

### 12.1 交叉引用方法和限制

先调用了 CE MCP 的 `code_find_references`：当前 CE 会话没有建立代码 dissect 索引，因此对 `+13A3B10`、`+13A5280`、`+140A6B0`、`+1226160`、`+1228B90` 均返回 `total = 0`。这不是“没有调用者”的证据。

随后对本地 `victoria3.exe` 的 `.text` 节逐字节扫描直接相对 `E8` 调用，并使用同一 PE 的 `.pdata` 确定调用者函数边界。扫描结果保存在：

```text
Output/check_trade_advantages1_20261003/followup_disk_callrefs.json
```

该方法在本版本中找到了以下关键调用关系：

| 目标 | 调用点 | 调用者 | 结论 |
|---|---:|---:|---|
| `+13A3B10` | `+13A3538` | `+13A3460` | 与价格倍率函数在同一上层流程中连续调用 |
| `+13A5280` | `+13A354F` | `+13A3460` | 相对优势结果随后进入价格倍率路径 |
| `+13A3B10` | `+140A8F7` | `+140A6B0` | `+140A6B0` 直接使用相对优势计算 |
| `+13A5280` | `+140A910` | `+140A6B0` | `+140A6B0` 直接使用价格倍率计算 |
| `+140A6B0` | `+11FC1BB`、`+11FC21B` | `+11FC080` | 候选收益计算路径调用价格/优势差值函数 |
| `+1226160`、`+1228B90` | `+11FBEB8`、`+11FBEC5` 等 | `+11FBDA0` | 原有绝对优势计算链确认 |

另外，绝对优势上下文链还被以下函数复用：`+1201220`、`+1225F70`、`+1943300`、`+1943FF0`、`+1944400`、`+1944A00`、`+194E320`、`+24AB6D0` 和 `+24AB7C0`。这说明 `+1226160`/`+1228B90` 不是只供候选刷新使用的局部代码，而是通用的贸易优势表达式计算链。

### 12.2 `+13A3460`：相对优势到价格的直接上层调用者

已完整采集函数：

```text
Output/check_trade_advantages1_20261003/function_13A3460.asm
```

函数入口保存：

```asm
+13A3487  movzx r15d,r9b  ; 保存方向/模式字节
+13A348B  mov r13,r8      ; 第三个对象参数
+13A348E  mov r12,rdx     ; 第二个对象参数
+13A3491  mov rdi,rcx     ; 第一个对象参数
```

它先从方向表中读取商品 ID 对应的缓存值，然后把同一组对象和方向参数传给两个目标：

```asm
+13A3527  movzx r9d,r15b
+13A352B  mov r8,r13
+13A352E  lea rdx,[rbp+230]
+13A3535  mov rcx,rdi
+13A3538  call +13A3B10       ; 计算相对优势/归一化优势

+13A353D  movzx r8d,r15b
+13A3541  mov rdx,[rbp+230]
+13A3548  lea rcx,[rbp+238]
+13A354F  call +13A5280       ; 使用相对结果计算价格倍率/价格修正
```

这解决了第 11 节中的主要疑问：`+13A3B10` 确实被价格计算路径调用，并且 `+13A5280` 紧随其后使用由前者准备的定点值。两者不是互不相关的通用数学函数。

当前可更新为：

```cpp
// 功能：先计算贸易相对优势，再把该结果交给价格修正函数。
// 入参：ownerOrMarket、context、goods、direction；返回：价格计算上下文或其结果。
// 地址：victoria3.exe+13A3460。
PriceContext* ComputeRelativeAdvantageAndPrice(
    OwnerOrMarket* ownerOrMarket,
    AdvantageContext* context,
    Goods* goods,
    uint8 direction)
{
    FixedPoint relative = ComputeRelativeTradeAdvantage(
        ownerOrMarket, &context->relative, goods, direction); // +13A3B10
    return ApplyRelativeAdvantageToPrice(
        &context->price, relative, goods, direction);          // +13A5280
}
```

`+13A3460` 的具体业务对象类型仍不能从入口寄存器单独确定，但调用顺序已经确认。

### 12.3 `+140A6B0`：相对优势与价格修正的另一个组合调用者

`+140A6B0` 的入口参数保存如下：

```asm
+140A6D0  mov rbp,r8
+140A6D3  movzx r13d,r9b
+140A6D7  mov rbx,rdx
+140A6DA  mov r14,rcx
```

所以 `r13b` 确实来自调用者的第四个参数 `r9b`，是该函数的方向/模式输入。它同时影响方向表选择：

```asm
+140A743  test r13b,r13b
+140A746  jne  +140A7B2
```

零值和非零值进入两套不同的方向数据表读取路径。函数末尾再次把这个方向字节传给两个核心函数：

```asm
+140A8DB  movzx r9d,r13b
+140A8E8  ...
+140A8F7  call +13A3B10

+140A8DE  movzx r9d,r13b
+140A910  call +13A5280
```

因此可以确认：

1. `r13b` 是方向相关枚举/模式字节；
2. 当前静态证据只确认 `0` 与“非 0”分支，不能确认 `0 = import` 或 `0 = export`；
3. `+140A6B0` 是相对优势和价格修正的组合上层函数，不应只命名为“差值函数”。

### 12.4 `[rsp+B0]` 的含义修正

`+140A6B0` 中：

```asm
+140A6FE  lea rcx,[rsp+B0]
+140A706  mov rsi,[rsp+B0]
+140A733  call +EF8330
```

随后：

```asm
+140A71B  mov rax,[r9+120]
+140A725  add rax,508
+140A72B  mov [rsp+90],rax
```

这里 `[rsp+B0]` 是本函数的局部临时上下文/资源句柄槽，先由 `+EF8330` 准备，再以 `rsi` 形式参与后续表读取和对象构造。当前没有证据表明它是某个固定游戏对象字段，因此旧文档中“确认 `[rsp+B0]` 对象字段”的说法应修正为：

```text
[rsp+B0] = +140A6B0 的局部上下文/资源句柄槽；其最终对象类型仍未确认。
```

### 12.5 `+1943600`：明确出现“中性值减相对优势”

已采集的 `+1943600` 在调用 `+13A3B10` 后立即执行：

```asm
+19438AC  call +13A3B10
+19438B1  mov eax,000186A0
+19438B6  sub rax,[rbp-80]
+19438BA  mov [r15],rax
```

这给出了比前一轮更直接的数学证据：该上层路径把 `+13A3B10` 输出的定点相对值转换为：

```text
output = 100000 - relativeValue
```

在后续分支中，`+19439C9` 又把另一份定点结果减去 `100000`：

```asm
+19439C9  lea rax,[r9-000186A0]
+19439D0  mov [rbp-80],rax
```

因此 `+13A3B10` 的返回值更接近“以 100000 为中性的相对比值”，而不是已经减一的最终 UI 百分比。不同上层调用者根据业务方向选择：

```text
relativeValue - 100000
100000 - relativeValue
```

这也解释了相对优势正负号随进口/出口上下文变化的现象。

### 12.6 `+1943600` 中的价格路径

`+1943600` 在相对值计算后，若价格上下文存在，会把 `r9` 形式的定点结果传给 `+13A5280`：

```asm
+19439E2  movzx r8d,byte ptr [rbp+6F0]
+19439EA  mov rdx,r9
+19439ED  lea rcx,[rsp+70]
+19439F2  call +13A5280
```

因此该函数给出了完整静态链：

```text
+13A3B10
    -> 得到以 100000 为中性的相对优势值
    -> 上层按方向做 relative - 100000 或 100000 - relative
+13A5280
    -> 使用相对结果及方向生成价格层定点结果
```

### 12.7 对 `+13A5280` 价格公式的修正边界

调用者证据确认 `+13A5280` 处于价格路径，但还不能从机器码中把游戏定义文件中的 `0.25` 直接定位为该函数的某一条立即数。当前更严谨的表达是：

```text
游戏定义层：TRADE_CENTER_ADVANTAGE_PRICE_MULTIPLIER = 0.25
调用层：+13A3B10 生成 relativeValue，+13A5280 消费该值并按方向修正价格
实现层：+13A5280 使用 100000 定点基准、全局定点输入和定点乘除；具体 0.25 的取值可能来自运行时定义/表达式上下文
```

所以原文中的：

```text
multiplier = 100000 + (relativeAdvantage - 100000) * 0.25
```

应视为业务语义公式，而不是已经逐指令证明的 `+13A5280` C++ 等价实现。逐指令已经确认的是：它消费相对优势结果、以 `100000` 为中性值、执行定点差值/倍率处理，并按方向走不同的写回路径。

### 12.8 `+1226160` / `+1228B90` 的复用情况

静态调用扫描显示，绝对优势上下文链存在多组重复调用：

```text
+1201220  -> +13C1A10 -> +1226080 -> +1226160 -> +1228B90 -> +13C2350
+1225F70  -> +13C1A10 -> +1226080 -> +1226160 -> +1228B90 -> +13C2350
+1943300  -> +13C1A10 -> +1226080 -> +1226160 -> +1228B90 -> +13C2350
+1943FF0  -> +13C1A10 -> +1226080 -> +1226160 -> +1228B90 -> +13C2350
+1944A00  -> +13C1A10 -> +1226080 -> +1226160 -> +1228B90 -> +13C2350
+24AB6D0  -> +13C1A10 -> +1226080 -> +1226160 -> +1228B90 -> +13C2350
+24AB7C0  -> +13C1A10 -> +1226080 -> +1226160 -> +1228B90 -> +13C2350
```

这进一步支持以下分层：

```text
+1226160  = 读取州/市场/商品/方向并构造优势来源上下文
+1228B90  = 加入市场贸易比例和市场条件
+13C2350  = 对上下文结果做统一定点归一化、插值和上下限处理
+13A3B10  = 在另一层按贸易量/总量归一化为相对优势
+13A5280  = 把相对优势消费为价格层定点修正
```

## 13. 本轮结论更新

第 11 节的四项后续任务完成情况：

| 任务 | 状态 | 更新结论 |
|---|---|---|
| `+13A3B10` 交叉引用 | 已完成 | 被 `+13A3460`、`+140A6B0`、`+1943600`、`+1943FF0`、`+1944540`、`+1944A00`、`+24AB550`、`+24AB610` 调用；其中多个调用者明确进入价格/贸易计算路径 |
| `+13A5280` 调用者 | 已完成 | 被 `+13A3460`、`+140A6B0`、`+1943600`、`+1944A00` 调用；确认其消费相对优势定点结果 |
| `+140A6B0` 调用者与方向 | 已完成 | `+11FC080` 调用它；`r13b = r9b` 是方向/模式输入，确认零/非零分支，未确认 import/export 数值枚举 |
| `+1226160` 优势条目映射 | 部分完成 | 已确认 `ADVANTAGE_FROM_*_ENTRY` 条目存在并参与表达式上下文；具体条目到栈槽、定义常数和最终加法顺序仍未完全展开 |

## 14. 修正后的函数关系图

```text
Refresh
  +11FBDA0
    ├─ 读取方向商品表
    └─ 缓存未命中
       ├─ +13C1A10：初始化临时定点上下文
       ├─ +1226080：包装表达式上下文
       ├─ +1226160：构造绝对优势来源
       ├─ +1228B90：加入市场贸易比例
       ├─ +13C2350：定点归一化和边界处理
       └─ +1027760：写回单位绝对优势缓存

相对优势/价格层
  +13A3460 或 +140A6B0
    ├─ +13A3B10：生成以 100000 为中性的相对优势值
    └─ +13A5280：按方向消费相对优势并修正价格

候选收益层
  +11FC080
    └─ +140A6B0
       ├─ +13A3B10
       └─ +13A5280
```

本轮仍然没有执行动态分析；所有新增结论来自 CE 只读 opcode、PE `.pdata` 函数边界、磁盘机器码交叉引用和游戏定义文本。

