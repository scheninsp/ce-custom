# Trade Advantage 完整静态计算流程

## 1. 结论

基于目前采集到的 CE MCP opcode、PE 函数边界、本地机器码调用关系以及 Victoria 3 的定义文件，目前可以写出一条完整的静态计算链：

```text
候选刷新
  +11FBDA0
    ↓
读取方向商品表中的单位绝对优势
    ↓ 缓存不存在或值不大于 0
构造绝对优势上下文
  +13C1A10
  +1226080
  +1226160
  +1228B90
    ↓
定点合成、插值和边界处理
  +13C2350
    ↓
最低值限制：max(result, 100000)
  +11FBEF0 / +11FBF6E
    ↓
写入方向商品缓存
  +1027760
    ↓
得到单位绝对优势 TA

相对优势阶段
  +13A3460 或 +140A6B0
    ↓
按贸易量和市场总量进行定点归一化
  +13A3B10
    ↓
得到以 100000 为中性的相对优势值
    ↓
上层根据方向转换为 relative - 100000 或 100000 - relative

价格阶段
  +13A5280
    ↓
将相对优势差值转换为价格倍率/价格修正
    ↓
进口、出口方向进入不同的定点写回路径

候选收益阶段
  +11FC080
    ↓
通过 +140A6B0 使用相对优势与价格修正结果
```

其中：

- `+11FBDA0` 到 `+1027760` 是**单位绝对优势**计算和缓存链。
- `+13A3B10` 是**相对优势比值**计算链的核心入口。
- `+13A5280` 是**相对优势影响价格**的核心入口。
- `+13A3460`、`+140A6B0`、`+1943600` 等是连接相对优势和价格函数的上层调用者。

## 2. 定点数约定

目前代码中反复出现以下常数：

```text
0x186A0 = 100000
```

因此本分析使用：

```text
FixedValue(x) = x / 100000
```

表示定点实数。

需要注意，某些底层通用定点函数还使用 `sar ..., 0xE`，也就是 14 位小数的中间格式。不能把所有出现的 `0x186A0` 和 `sar 0xE` 混为同一种存储格式；前者是贸易优势层明显使用的中性基准，后者是通用定点乘除的中间缩放。

## 3. 第一阶段：读取或计算单位绝对优势

### 3.1 入口：`+11FBDA0`

当前断点所在函数是：

```text
victoria3.exe+11FBDA0
```

实际运行地址曾采集为：

```text
7FF777CEBDA0
```

该函数首先写入候选数量：

```asm
+11FBDD7  call +122AB50
+11FBDDC  mov r8,[rax]
+11FBDD7  mov [r14+38],r8       ; c+38 = quantity
```

之后读取商品 ID，根据候选的方向字段 `c+0x08` 选择方向商品表：

```asm
方向 0：
+11FBE0D  mov rcx,[rbp+rax*8+7E8] ; 存在位图
+11FBE1B  mov rax,[rbp+7D0]       ; 优势数组

方向 1：
+11FBE42  mov rcx,[rbp+rax*8+798] ; 存在位图
+11FBE50  mov rax,[rbp+780]       ; 优势数组
```

商品 ID 通过位图检查后，按 `goodsId * 8` 读取：

```asm
+11FBE15  bt rcx,rdx
+11FBE22  mov rax,[rax+rbx*8]
+11FBE60  mov [r14+40],rax       ; c+40 = absolute advantage
+11FBE64  test rax,rax
+11FBE67  jg +11FC041
```

所以：

```text
c+0x40 = 某州/贸易中心、某商品、某方向的单位绝对优势缓存值
```

这里不是 UI 显示的相对优势百分比。

### 3.2 缓存命中路径

当方向表中已有正值时，`+11FBDA0` 直接把该值写入 `c+0x40`，然后跳到 `+11FC041` 继续候选刷新。

```cpp
// 功能：从指定方向的商品优势数组读取缓存值。
// 入参：directionTable 为方向商品表；goodsId 为商品 ID。
// 返回：缓存中的单位绝对优势定点值。
// 地址：victoria3.exe+11FBDA0 内联读取路径。
int64 ReadAbsoluteAdvantageCache(DirectionTable* directionTable,
                                 int32 goodsId);
```

### 3.3 缓存未命中路径

如果读取结果不大于零，代码进入：

```asm
+11FBE6D  movzx ebx,byte ptr [r14+08] ; 方向
+11FBE72  mov r12,[r14]              ; 商品对象
+11FBE79  call +7C96A0                ; 获取州/市场相关对象
+11FBE81  test bl,bl
+11FBE83  je +11FBF11
+11FBE89  cmp ebx,01
+11FBE8C  jne +11FBF98
```

方向 1 的调用链：

```asm
+11FBE99  call +13C1A10
+11FBEA4  call +1226080
+11FBEB8  call +1226160
+11FBEC5  call +1228B90
+11FBED7  call +13C2350
+11FBEF0  cmp [rax],100000
+11FBEF7  cmovg rbx,rax
+11FBEF3  mov rbx,[rbx]
+11FBEF03 call +C48D10
+11FBF93  call +1027760
```

方向 0 使用相同的函数，只是传入方向值为 0：

```asm
+11FBF18  call +13C1A10
+11FBF23  call +1226080
+11FBF36  call +1226160
+11FBF43  call +1228B90
+11FBF55  call +13C2350
+11FBF6E  cmp [rax],100000
+11FBF75  cmovg rbx,rax
+11FBF81  call +C48D10
+11FBF93  call +1027760
```

`+11FBEF0`/`+11FBF6E` 的语义是：

```text
fixedInput = max(normalizedValue, 100000)
```

这也是 `c+0x40` 最终满足正值约束的关键步骤之一。

## 4. 第二阶段：构造绝对优势计算上下文

### 4.1 `+13C1A10`：初始化临时定点上下文

入口实际为：

```text
victoria3.exe+13C1A10
```

关键字段初始化：

```asm
+13C1A10  mov [rcx+00],0
+13C1A14  mov [rcx+08],0
+13C1A18  mov [rcx+10],0
+13C1A1C  mov qword ptr [rcx+18],000186A0
+13C1A27  mov [rcx+20],8000000000000000
+13C1A32  mov [rcx+28],7FFFFFFFFFFFFFFF
+13C1A3D  mov [rcx+30],0
+13C1A44  mov [rcx+31],dl
```

可确认的语义：

```text
+0x00/+0x08/+0x10  中间累加或结果槽
+0x18              定点基准 100000
+0x20              下界 INT64_MIN
+0x28              上界 INT64_MAX
+0x30/+0x31         状态/模式字段
```

```cpp
// 功能：初始化方向优势计算所需的临时定点上下文。
// 入参：context 为输出上下文；mode 为初始化模式。
// 返回：无，原位初始化 context。
// 地址：victoria3.exe+13C1A10。
void InitializeDirectionalAdvantageContext(TempValueContext* context,
                                           uint8 mode);
```

### 4.2 `+1226080`：包装表达式上下文

`+1226080` 将前一步上下文包装成可供表达式/数值系统处理的对象：

```asm
+1226080  vpxor xmm0,xmm0,xmm0
+1226097  vmovdqu xmm1,[global]
+12260CF  call +6DE750
+12260E2  ... 清理临时对象
```

该函数的职责是上下文包装和生命周期管理，不是贸易优势公式本身。

```cpp
// 功能：将临时定点上下文包装成表达式计算对象。
// 入参：context 为临时上下文；返回：无，包装对象在调用链内有效。
// 地址：victoria3.exe+1226080。
void WrapDirectionalAdvantageContext(TempValueContext* context);
```

### 4.3 `+1226160`：绝对优势来源构造

入口参数：

```asm
+1226160  mov [rsp+08],rcx    ; state/market
+122616B  mov [rsp+10],rdx    ; 临时上下文
+1226167  mov [rsp+18],r8     ; goods
+1226163  mov [rsp+20],r9b    ; direction
```

函数随后：

```asm
+12261A3  call +2C7550
+12261A8  mov r14,[rax+120]
+12261AF  add r14,508
+12261B6  mov r13,[r15+18B0]
```

其中：

- `r15` 是传入的州/市场相关对象；
- `r13 = [r15+0x18B0]` 是州侧关联市场/修正对象；
- `r14` 指向与优势相关的方向数据区域；
- `r8` 保存商品对象；
- `r9b` 保存方向。

函数中还出现以下优势条目字符串：

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

因此可以确认它不是只读取一个“优势数值”，而是根据州、市场、商品和方向构造多个优势来源。

结合游戏定义文件，业务层可以写成：

```text
TA_raw = TRADE_CENTER_ADVANTAGE_BASE
       + 市场区域生产贡献
       + 公司特许贡献
       + 市场声望商品贡献
       + 贸易协议贡献
       + 条约港贡献
       + 阵营/宗教/利益等级贡献
       + 禁运贡献
       + 战争贡献
       + 其他方向条件贡献
```

已知定义值包括：

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

这些定义项和 opcode 中的 `ADVANTAGE_FROM_*_ENTRY` 字符串相互印证，但当前仍不能把每一个定义值唯一映射到某个栈槽和具体加法顺序。

### 4.4 `+1228B90`：加入市场贸易比例

`+1228B90` 读取州对象的市场关联字段：

```asm
+1228BC8  mov rbx,[rcx+18B0]
+1228BD8  lock inc [rbx+08]
+1228C17  call +6DDFB0
+1228C60  call +D21B10
```

之后同样执行 `imul`、`sar 0xE`、`idiv` 和 `imul 0x186A0` 形式的定点运算，并把市场贸易比例加入表达式上下文。

```cpp
// 功能：将市场贸易比例和市场条件加入绝对优势计算上下文。
// 入参：stateOrMarket 为州/市场对象；context 为定点表达式上下文。
// 返回：无，结果写入 context。
// 地址：victoria3.exe+1228B90。
void AddMarketTradeFractionToAdvantageContext(
    StateOrMarket* stateOrMarket,
    TempValueContext* context);
```

当前可以确认它参与市场侧比例计算，但不能仅凭静态 opcode 判定该比例是生产份额、消费份额、相反方向贸易份额，还是多个比例的组合。

## 5. 第三阶段：绝对优势定点合成和写回

### 5.1 `+13C2350`：通用定点组合和边界处理

`+13C2350` 的关键行为：

```asm
+13C2363  add r11,000186A0
+13C23DF  imul rdx,r11
+13C23EC  sar rdx,0E
+13C23F7  add rdx,rax
+13C2402  cmovl r9,rcx
+13C240C  cmovg r10,rcx
+13C2424  imul rax,r8,000186A0
+13C2435  imul r9,r10
+13C244D  test rdx,rdx
```

函数末端对结果进行上下限选择：

```asm
+13C2587  cmp rdx,r10
+13C258A  jnl +13C25A0
+13C258C  mov [rdi],rbp
+13C25A0  cmp rdx,rsi
+13C25A3  cmovg rdx,r14
+13C25A7  mov [rdi],rdx
```

它的安全语义是：

```text
定点乘法
  -> 14 位缩放
  -> 定点除法
  -> 多个贡献相加
  -> 根据上下界做裁剪
  -> 写入输出槽
```

```cpp
// 功能：对绝对优势上下文中的定点贡献进行组合、插值和上下限处理。
// 入参：context 为优势计算上下文；output 为定点输出对象。
// 返回：指向 output 的结果指针。
// 地址：victoria3.exe+13C2350。
FixedPoint* NormalizeDirectionalAdvantage(
    TempValueContext* context,
    FixedPoint* output);
```

该函数不能简单等价为 `abs(value)` 或 `max(value, 0)`；它包含有符号乘除、分段插值和上下限处理。

### 5.2 `+1027760`：写回方向商品缓存

`+1027760` 接收：

```text
rcx = 方向商品表
rdx = 商品对象
r8  = 至少为 100000 的定点值
```

关键 opcode：

```asm
+102776F  movsxd rsi,dword ptr [rdx+10] ; goodsId
+1027773  mov rdi,rcx                  ; direction table
+1027778  mov rbx,r8                   ; fixed value
+102777B  call +1026630                ; 商品 ID 合法性检查
+10277B5  mov rax,[rdi+08]
+10277B9  mov [rax+rsi*8],rbx           ; 写优势数组
+10277C2  and [rcx+20],r8               ; 更新存在位图
```

该函数是缓存写回函数，不是相对优势函数：

```cpp
// 功能：把单位绝对优势写入方向商品表，并更新商品存在位图。
// 入参：directionTable 为方向商品表；goods 为商品对象；fixedValue 为定点优势值。
// 返回：无或内部缓存句柄，业务结果通过表写回。
// 地址：victoria3.exe+1027760。
void WriteDirectionalAbsoluteAdvantage(
    DirectionTable* directionTable,
    Goods* goods,
    int64 fixedValue);
```

写回后，`+11FBF93` 再次调用 `+1027760` 周边的表处理逻辑，最终把结果写入候选：

```asm
+11FC008  mov [r14+40],rax
```

## 6. 第四阶段：单位绝对优势到相对优势

### 6.1 上层入口：`+13A3460`

`+13A3460` 是目前最清晰的“相对优势 → 价格”组合入口之一。

关键调用：

```asm
+13A3527  movzx r9d,r15b
+13A352B  mov r8,r13
+13A352E  lea rdx,[rbp+230]
+13A3535  mov rcx,rdi
+13A3538  call +13A3B10

+13A353D  movzx r8d,r15b
+13A3541  mov rdx,[rbp+230]
+13A3548  lea rcx,[rbp+238]
+13A354F  call +13A5280
```

这证明：

```text
+13A3B10 的输出会成为 +13A5280 的输入或其关联上下文的一部分
```

因此，相对优势和价格修正不是两个无关的数学函数。

### 6.2 核心入口：`+13A3B10`

`+13A3B10` 的方向分支：

```asm
+13A3B40  movzx eax,r9b
+13A3B75  test r9b,r9b
+13A3B78  je  +13A3C14
+13A3B8C  mov qword ptr [rdx],000186A0
```

在特定方向/模式分支中，函数直接产生中性基准：

```text
result = 100000
```

其他分支会读取多个市场/贸易量相关数值，执行：

```text
part = value × 100000 / denominator
remainder = remainder × 100000 / denominator
result = part + remainder
```

并进行溢出安全的分段除法。可确认的业务模型为：

```text
W_i = TA_i × Q_i
W_total = Σ(TA_j × Q_j)
Q_total = ΣQ_j
TA_average = W_total / Q_total
RelativeValue = TA_i / TA_average
```

其中 `RelativeValue` 的中性值是 `1.0`，定点表示为 `100000`。

若转换为以零为中性的显示/修正值：

```text
RelativeDelta = RelativeValue - 1
```

定点形式：

```text
RelativeDeltaFixed = RelativeValueFixed - 100000
```

```cpp
// 功能：按贸易量和市场总量将单位绝对优势归一化为相对优势比值。
// 入参：stateOrMarket 为州/市场对象；output 为输出槽；goodsContext 为商品上下文；direction 为方向。
// 返回：output 指针；*output 为以 100000 为中性的相对优势值。
// 地址：victoria3.exe+13A3B10。
FixedPoint* ComputeRelativeTradeAdvantage(
    StateOrMarket* stateOrMarket,
    FixedPoint* output,
    GoodsContext* goodsContext,
    uint8 direction);
```

### 6.3 `+1943600` 对中性值的直接处理证据

`+1943600` 调用 `+13A3B10` 后立即执行：

```asm
+19438AC  call +13A3B10
+19438B1  mov eax,000186A0
+19438B6  sub rax,[rbp-80]
+19438BA  mov [r15],rax
```

也就是：

```text
output = 100000 - relativeValue
```

同一函数的另一条路径出现：

```asm
+19439C9  lea rax,[r9-000186A0]
+19439D0  mov [rbp-80],rax
```

即：

```text
output = relativeValue - 100000
```

因此最终正负号不是由 `+13A3B10` 单独决定，而是由上层根据贸易方向和价格语义选择：

```text
relativeValue - 100000
或
100000 - relativeValue
```

这也是相对优势可以在 UI 或价格层表现为正、负的静态证据。

## 7. 第五阶段：相对优势影响价格

### 7.1 价格修正入口：`+13A5280`

`+13A5280` 被以下路径直接调用：

```text
+13A3460 -> +13A3B10 -> +13A5280
+140A6B0 -> +13A3B10 -> +13A5280
+1943600 -> +13A3B10 -> +13A5280
+1944A00 -> +13A3B10 -> +13A5280
```

入口关键字段：

```asm
+13A5289  mov r9d,000186A0
+13A52A7  cmp rdx,r9
+13A52B0  sub r9,[7FF77C379E10]
+13A52B7  lea rcx,[rdx-000186A0]
```

它明确以 `100000` 作为中性基准，计算相对优势相对于中性的差值，并按方向执行不同写回路径：

```asm
+13A5401  test dil,dil
+13A5408  jne  +13A541F
+13A541F  idiv r10
+13A542E  mov [r11],rax
+13A5439  mov [r11],r10
```

### 7.2 游戏定义层的价格公式

游戏定义文件：

```text
TRADE_CENTER_ADVANTAGE_PRICE_MULTIPLIER = 0.25
```

定义旁的注释说明价格倍率作用于“相对优势减 1”：

```text
priceMultiplier = 1 + (relativeAdvantage - 1) × 0.25
```

因此业务语义可以写成：

```text
relativeRatio = RelativeValueFixed / 100000
priceMultiplier = 1 + (relativeRatio - 1) × 0.25
```

若换成定点形式：

```text
priceMultiplierFixed
    = 100000 + (RelativeValueFixed - 100000) × 25000 / 100000
```

但需要严格区分：

- 上式是游戏定义层和已有文档支持的**业务公式**；
- `+13A5280` 的 opcode 已确认使用中性值、定点差值、乘除和方向分支；
- 当前尚未从 `+13A5280` 本体逐条定位 `25000` 立即数，因此不能把上式声称为完整的机器码等价式。

### 7.3 进口/出口方向

`+140A6B0` 保存并传递方向参数：

```asm
+140A6D3  movzx r13d,r9b
+140A743  test r13b,r13b
+140A746  jne  +140A7B2
+140A8F7  call +13A3B10
+140A910  call +13A5280
```

目前确认：

```text
r13b = 来自 r9b 的方向/模式字节
0 和非 0 进入不同的方向表路径
```

目前不能仅通过静态采集确定：

```text
direction == 0 是否必然等于进口
direction == 1 是否必然等于出口
```

因此文档中只能写“进口/出口方向分支”，不能给出未经验证的数值枚举。

## 8. 第六阶段：进入候选收益计算

`+11FC080` 是候选收益计算函数。它通过 `+140A6B0` 进入相对优势/价格修正路径：

```asm
+11FC1BB  call +140A6B0
+11FC21B  call +140A6B0
```

这说明完整业务链不是在 `+11FBDA0` 内全部结束，而是分成：

```text
+11FBDA0
  -> 生成并缓存单位绝对优势

+11FC080
  -> 在候选收益/价格上下文中调用 +140A6B0
     -> +13A3B10 计算相对优势
     -> +13A5280 生成价格修正
```

因此 `c+0x40` 的绝对优势值会先作为候选有效性和后续收益计算的输入，但不能把 `c+0x40` 直接等同于价格层的相对优势。

## 9. 完整伪代码

下面是目前可以由静态证据支持的语义级伪代码。它不是未经验证的原始 C++ 反编译，而是按照已确认的函数入口组织出的完整流程。

```cpp
// 功能：刷新候选的数量和单位绝对优势，并在优势有效时继续进入收益阶段。
// 入参：candidate 为贸易候选；sharedContext 为共享收益上下文。
// 返回：无，结果写入 candidate。
// 地址：victoria3.exe+11FBDA0。
void RefreshTradeCandidate(Candidate* candidate,
                           SharedTradeContext* sharedContext)
{
    candidate->quantity = CalculateQuantityPerCapacity(
        ResolveState(candidate->stateRef), candidate->goods); // +122AB50

    candidate->absoluteAdvantage =
        ReadOrComputeAbsoluteAdvantage(candidate);             // +11FBDA0 内联

    if (candidate->absoluteAdvantage <= 0)
        return;

    UpdateCandidateShortage(candidate, sharedContext);         // +11FBA60
    UpdateCandidateRevenue(candidate, sharedContext);          // +11FC080
    CalculateCandidateDesirability(candidate, sharedContext);  // +11FC320
}

// 功能：读取或计算方向商品的单位绝对优势。
// 入参：candidate 为候选对象；返回：100000 定点单位的正向绝对优势。
// 地址：victoria3.exe+11FBDA0 内联路径。
int64 ReadOrComputeAbsoluteAdvantage(Candidate* candidate)
{
    DirectionTable* table = SelectDirectionTable(
        candidate->state, candidate->direction);
    int32 goodsId = candidate->goods->id;
    int64 cached = ReadDirectionGoodsValue(table, goodsId);

    if (cached > 0)
        return cached;

    TempValueContext context;
    InitializeDirectionalAdvantageContext(&context, 0);         // +13C1A10
    WrapDirectionalAdvantageContext(&context);                 // +1226080
    BuildDirectionalAdvantageContext(                           // +1226160
        candidate->state, &context, candidate->goods,
        candidate->direction);
    AddMarketTradeFractionToAdvantageContext(                   // +1228B90
        candidate->state, &context);

    FixedPoint normalized;
    NormalizeDirectionalAdvantage(&context, &normalized);       // +13C2350
    int64 fixedValue = max(normalized.value, 100000);

    WriteDirectionalAbsoluteAdvantage(                           // +1027760
        table, candidate->goods, fixedValue);
    return ReadDirectionGoodsValue(table, goodsId);
}

// 功能：计算单位绝对优势对应的相对优势比值。
// 入参：stateOrMarket、output、goodsContext、direction；返回：100000 为中性的定点比值。
// 地址：victoria3.exe+13A3B10。
FixedPoint* ComputeRelativeTradeAdvantage(
    StateOrMarket* stateOrMarket,
    FixedPoint* output,
    GoodsContext* goodsContext,
    uint8 direction)
{
    if (direction == SPECIAL_NEUTRAL_MODE) {
        *output = 100000;
        return output;
    }

    // 业务等价形式；底层使用拆分余数和溢出安全定点除法。
    int64 weightedAdvantage = SumAdvantageTimesQuantity(stateOrMarket,
                                                        goodsContext,
                                                        direction);
    int64 totalQuantity = SumTradeQuantity(stateOrMarket,
                                            goodsContext,
                                            direction);
    int64 averageAdvantage = weightedAdvantage / totalQuantity;
    *output = FixedDivide(goodsContext->absoluteAdvantage,
                          averageAdvantage);
    return output;
}

// 功能：把相对优势比值转换为价格倍率或价格修正。
// 入参：priceContext 为价格输出上下文；relativeValue 为 100000 中性定点值；
//       goodsContext 为商品上下文；direction 为方向/模式。
// 返回：价格输出上下文或其定点结果。
// 地址：victoria3.exe+13A5280。
PriceContext* ApplyRelativeAdvantageToPrice(
    PriceContext* priceContext,
    int64 relativeValue,
    GoodsContext* goodsContext,
    uint8 direction)
{
    int64 delta = relativeValue - 100000;
    int64 priceMultiplier =
        100000 + FixedMultiply(delta, 25000); // 业务公式：0.25

    if (direction == REVERSE_PRICE_MODE)
        priceMultiplier = FixedDivide(10000000000, priceMultiplier);

    priceContext->value = priceMultiplier;
    return priceContext;
}
```

伪代码中以下名称仍是分析命名，不是已确认的游戏符号：

```text
CalculateQuantityPerCapacity
SelectDirectionTable
BuildDirectionalAdvantageContext
SumAdvantageTimesQuantity
SumTradeQuantity
FixedMultiply
FixedDivide
```

## 10. 地址总表

| 阶段 | 入口地址 | 当前确认作用 | 证据等级 |
|---|---:|---|---|
| 候选刷新/缓存读取 | `+11FBDA0` | 读取方向商品绝对优势；未命中时进入计算链 | 已确认 |
| 数量计算调用 | `+122AB50` | 产生候选数量 | 已确认调用点 |
| 临时上下文初始化 | `+13C1A10` | 初始化 100000、上下界和状态字段 | 已确认 |
| 上下文包装 | `+1226080` | 建立表达式/数值上下文对象 | 已确认 |
| 优势来源构造 | `+1226160` | 读取 state/market/goods/direction，组织 `ADVANTAGE_FROM_*` 输入 | 高可信/部分逐项确认 |
| 市场比例输入 | `+1228B90` | 加入市场贸易比例及市场条件 | 高可信 |
| 定点归一化 | `+13C2350` | 定点乘除、插值、上下界处理 | 已确认 |
| 缓存写回 | `+1027760` | 写方向商品优势数组和位图 | 已确认 |
| 相对优势核心 | `+13A3B10` | 生成以 100000 为中性的相对优势值 | 高可信，调用关系已确认 |
| 相对优势上层 | `+13A3460` | 连续调用相对优势和价格修正 | 已确认调用关系 |
| 相对优势/价格组合 | `+140A6B0` | 读取方向相关数据，调用相对优势和价格函数 | 已确认调用关系 |
| 价格修正核心 | `+13A5280` | 消费相对优势，执行方向相关定点价格修正 | 高可信，调用关系已确认 |
| 候选收益 | `+11FC080` | 通过 `+140A6B0` 进入价格/优势层 | 已确认调用点 |
| 中性值方向转换 | `+1943600` | 明确执行 `100000-relative` 或 `relative-100000` | 已确认 |

## 11. 当前能够确认的“完整流程”边界

可以确认的完整流程是：

```text
绝对优势 TA
  = +11FBDA0 读取或触发计算
  = +13C1A10 初始化上下文
  = +1226080 包装上下文
  = +1226160 构造优势来源
  = +1228B90 加入市场比例
  = +13C2350 定点合成和边界处理
  = +1027760 写回方向商品缓存

相对优势 RelativeValue
  = +13A3B10 以贸易量/市场总量定点归一化
  = 100000 为中性值
  = 上层可能转换为 RelativeValue-100000
    或 100000-RelativeValue

价格修正
  = +13A5280 消费 RelativeValue
  = 使用相对优势相对 1 的差值
  = 业务定义倍率系数为 0.25
  = 按方向执行正向或反向定点写回
```

仍不能声称已经完全还原的部分是：

1. `+1226160` 中所有优势来源的精确加法顺序和每个上下文槽位。
2. `+1228B90` 的市场比例输入分别对应哪些市场统计量。
3. `+13A3B10` 的每一个寄存器对应的完整 C++ 对象类型。
4. `+13A5280` 中 `0.25` 的具体运行时取值位置，以及进口/出口枚举的数值。
5. 价格修正之后与世界价格、国内价格、税费和最终成交价之间的全部后续函数。

因此，本文件可以作为目前静态分析的完整“函数入口级流程图”，但其中绝对优势各项来源、价格函数内部的最终字段含义仍应标记为静态高可信推断，而不是官方源码级还原。

## 12. 分析约束

本报告没有执行动态分析，没有使用断点单步、寄存器现场、内存写入或运行时样本推断。所有地址和调用关系来自：

- Cheat Engine MCP 的只读 `code_disassemble` / `code_decode`；
- 本地 PE `.pdata` 函数边界；
- 本地 `.text` 中直接 `E8` 调用扫描；
- Victoria 3 `00_defines.txt` 的公开定义文本。
