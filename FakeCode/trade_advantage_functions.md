# 贸易优势伪代码

## `Refresh`（`victoria3.exe+11FBDA0`）

```cpp
// 功能：刷新候选的单位数量、贸易优势和最终意愿评分。
// 入参：候选 c、共享计算上下文；返回：主要通过 c 原位写回，业务返回值待确认。
// 地址：victoria3.exe+11FBDA0。
void Refresh(Candidate* c, TradeContext* context)
{
    State* state = Resolve(c->stateRef);
    c->quantity = CalculateQuantityPerCapacity(state, c->goods);
    c->advantage = ReadOrComputeDirectionalTradeAdvantage(
        state, c->goods, c->direction);
    if (c->advantage <= 0)
        return;
    UpdateCandidateShortage(c, context);       // +11FBA60
    UpdateCandidateRevenue(c, context);        // +11FC080
    CalculateDesirability(c, context);          // +11FC320
}
```

## `ReadOrComputeDirectionalTradeAdvantage`（`victoria3.exe+11FBDA0` 内联路径）

```cpp
// 功能：读取指定州、商品和贸易方向的绝对贸易优势；缓存不存在时计算并返回。
// 入参：state 为州对象，goods 为商品对象，direction 为进口/出口方向；
// 返回：正的绝对贸易优势，使用游戏内部定点整数单位。
// 地址：victoria3.exe+11FBDA0 内联计算链，非独立已确认符号函数。
int64 ReadOrComputeDirectionalTradeAdvantage(State* state, Goods* goods,
                                             uint8 direction)
{
    DirectionTable* table = SelectDirectionTable(state, direction);
    int32 goodId = ReadGoodsId(goods);
    int64 cached = table->values[goodId];
    if (cached != 0)
        return cached;
    return ComputeAbsoluteTradeAdvantage(state, goods, direction);
}
```

## `ComputeAbsoluteTradeAdvantage`（`victoria3.exe+11FBDA0` 内联路径）

```cpp
// 功能：构造州/市场/商品/方向上下文，并把定点优势中间值写入方向商品缓存。
// 入参：state/market、goods、direction；返回：缓存中的绝对优势定点值。
// 地址：victoria3.exe+11FBDA0 内联路径；辅助调用地址见行内注释。
int64 ComputeAbsoluteTradeAdvantage(State* state, Goods* goods, uint8 direction)
{
    TempContext t;
    InitTempContext(&t, 0);                         // +EB1A10
    WrapNumericContext(&t);                         // +D16080
    FillGoodsDirectionContext(state, &t, goods, direction); // +D16160
    BuildMarketTradeFraction(state, &t);            // +D18B90
    int64 normalized = NormalizeAdvantage(&t);      // +EB2350
    int64 fixedInput = normalized < 100000 ? 100000 : normalized;
    DirectionTable* table = SelectDirectionTable(state, direction);
    int64 result = UpdateAdvantageCache(table, goods, fixedInput); // +B17760
    table->values[ReadGoodsId(goods)] = result;
    return result;
}
```

## `UpdateCandidateShortage`（`victoria3.exe+11FBA60`）

```cpp
// 功能：计算候选商品的短缺指标并写入候选对象的 c+30。
// 入参：候选 c、共享计算上下文 context；返回：无，结果原位写回。
// 地址：victoria3.exe+11FBA60。
void UpdateCandidateShortage(Candidate* c, TradeContext* context)
{
    if (c->direction != 0 || !HasEligibleMarketGoods(c->stateRef, c->goods)) {
        c->shortage = 0;
        return;
    }
    c->shortage = ComputeShortage(c, context);
}
```

## `UpdateCandidateRevenue`（`victoria3.exe+11FC080`）

```cpp
// 功能：准备收益计算上下文，计算单位净收益和基础收益。
// 入参：候选 c、共享计算上下文 context；返回：无，结果写入 c+18 与 c+10。
// 地址：victoria3.exe+11FC080；两个语义子过程的展开见本文件后续章节。
void UpdateCandidateRevenue(Candidate* c, TradeContext* context)
{
    State* state = Resolve(c->stateRef); // victoria3.exe+7C96A0，调用点 +11FC09F
    TradeContext simulatedStorage;
    TradeContext* evaluation = ApplyCandidateToSimulation(
        &simulatedStorage, context, c);

    c->unitRevenue = ComputeUnitRevenue(state, evaluation, c); // c+0x18
    if (c->mode == 1)
        CallAt<void>(0xE337B0, &simulatedStorage); // victoria3.exe+E337B0，调用点 +11FC1F6

    c->baseRevenue = FixedMultiply(c->quantity, c->unitRevenue); // c+0x10
}
```

## `CalculateDesirability`（`victoria3.exe+11FC320`）

```cpp
// 功能：检查候选数量限制并合成最终意愿评分。
// 入参：候选 c、共享计算上下文 context；返回：无，最终评分写入 c+20。
// 地址：victoria3.exe+11FC320。
void CalculateDesirability(Candidate* c, TradeContext* context)
{
    int64 worldOpposite = ReadWorldOppositeTrade(c, context);
    int64 marketOpposite = ReadMarketOppositeTrade(c, context);
    int64 localDirection = ReadMarketDirectionTrade(c, context);
    if (!WithinQuantityLimits(c, worldOpposite, marketOpposite, localDirection)) {
        c->desirability = INT64_MIN;
        return;
    }
    c->desirability = c->baseRevenue + c->shortage + localDirection;
}
```

## 候选收益计算展开：记法、布局与证据边界

以下展开只使用仓库已有的 opcode。`ApplyCandidateToSimulation` 和 `ComputeUnitRevenue` 是为了阅读而拆出的 **`+11FC080` 内联语义子过程**，不是新发现的两个独立 ABI 函数。

- `CallAt<Result>(RVA, args...)` 表示调用 `victoria3.exe+RVA` 处的引擎函数；它是伪代码记法，不是一个新增的游戏函数。没有展开的被调函数明确保留地址，不用猜测公式替换。
- `FixedMultiply(left, right)` 沿用本文件已有的算术记法，表示五位小数定点乘法；普通路径为 `trunc(left × right / 100000)`，数值较大时使用 opcode 中的拆分乘法。`trunc` 表示向零截断。
- `ReadGlobal<T>(RVA)`、`Load<T>(address)` 和 `LoadSignedWord(address)` 是读取记法，不代表独立 ABI 函数；`moduleBase` 来自导出的 `module_get.json`。本文所有地址都使用 RVA，不用绝对地址尾部代替模块偏移。
- `TradeContext::tables[index]` 是布局视图：八张表分别位于 `0x00/0x50/0xA0/0xF0/0x140/0x190/0x1E0/0x230`，每张表跨度 `0x50`，总跨度 `0x280`。不将这些临时表强行命名为已确认的 UI 字段。
- `GoodsTable::values` 对应表 `+0x08` 的数组指针；`presenceWords` 对应表 `+0x20` 起的存在位图；`flags48` 对应表 `+0x48` 的 32 位字段。
- 所有金额、数量、倍率和率值都用 `100000` 定点整数；方向保留 `0/1`。`0≈进口、1≈出口` 仍是高可信经济解释，不是已恢复的有符号枚举。

| 入口或调用点 | 本文件展开内容 | 原始证据 |
| --- | --- | --- |
| `+11FC0A7` 至 `+11FC198` | 模式判断、复制八张表、加入本次交易量 | `Output/check_trade_advantages1_20261003/function_11FC080.asm` |
| `+1027970` | 商品表增量、存在位和零值处理；沿用已有名称 `AddByGoods` | `Output/goal3_static_20261002/function_7FF777B17970.md` |
| `+11FC1BB/+11FC21B` | 调用方向价格差函数 | `Output/check_trade_advantages1_20261003/function_11FC080.asm` |
| `+140A6B0` | 两端价格、相对优势、倍率、限价及方向价差 | `Output/check_trade_advantages1_20261003/function_140A6B0.asm` |
| `+13A5280` | 相对优势比值到正向/倒数倍率 | `Output/check_trade_advantages1_20261003/function_13A5280.asm` 和同名 `.json` |
| `+11FC1E0/+11FC240` | 调用税补后的单位净收益函数 | `Output/check_trade_advantages1_20261003/function_11FC080.asm` |
| `+1207860` | 商品基价、政策查询、关税与补助折算 | `Output/check_trade_advantages1_20261003/function_1207860.asm` |
| `+1206D40/+1207370` | 净收益所用的有效关税率/补助率来源 | `Output/goal3_scoring_20261002/function_7FF777CF6D40.md`、`function_7FF777CF7370.md` |

本次新增了两个语义子过程及实际价格/净收益路径，没有修改前面 `CalculateDesirability` 的旧简化骨架；最终评分的完整展开应另查 `Docs/important_notes/刷新候选函数.md`，不能把该旧骨架当作本次逐指令恢复的评分公式。

## `ApplyCandidateToSimulation`（`victoria3.exe+11FC080` 内联子过程）

模式不等于 `1` 时直接使用原上下文。只有模式 `1` 才复制八张商品表，随后增加两张表中的商品量；不是无条件浅复制，也不在减少模式先减去 `q`。

```cpp
// 功能：选择收益评估上下文；增加模式复制商品表并模拟加入本次数量。
// 入参：storage 为未初始化临时上下文，original 为原上下文，candidate 为候选。
// 返回：模式 1 返回 storage；其他模式返回 original，且不初始化 storage。
// 地址：victoria3.exe+11FC080 内联子过程，主要指令为 +11FC0A7 至 +11FC198。
TradeContext* ApplyCandidateToSimulation(TradeContext* storage,
                                        TradeContext* original,
                                        Candidate* candidate)
{
    if (candidate->mode != 1)
        return original;

    // 八次复制构造对应 +11FC0B9/+11FC0CA/+11FC0DE/+11FC0F2、
    // +11FC106/+11FC11A/+11FC12E/+11FC142；未展开复制构造器内部的分配实现。
    for (int32 tableIndex = 0; tableIndex < 8; ++tableIndex)
        CallAt<void>(0xC104C0,
                     &storage->tables[tableIndex],
                     &original->tables[tableIndex]); // victoria3.exe+C104C0

    if (candidate->direction == 0) {
        AddByGoods(&storage->tables[0], candidate->goods, candidate->quantity); // +1027970，表 +0x00
        AddByGoods(&storage->tables[4], candidate->goods, candidate->quantity); // +1027970，表 +0x140
    } else if (candidate->direction == 1) {
        AddByGoods(&storage->tables[1], candidate->goods, candidate->quantity); // +1027970，表 +0x50
        AddByGoods(&storage->tables[5], candidate->goods, candidate->quantity); // +1027970，表 +0x190
    }
    return storage;
}
```

真实调用点是：方向 `0` 首次加量在 `+11FC17F`，方向 `1` 首次加量在 `+11FC164`；第二次加量共用 `+11FC193`。其他方向虽然仍复制上下文，但跳过这两次商品加量。

## `AddByGoods`（`victoria3.exe+1027970`）

沿用 `Docs/important_notes/州贸易调整函数.md` 中已使用的名称。该函数不只是裸数组加法，还维护商品有效位，并区分是否保留零值。

```cpp
// 功能：在商品数值表中累加定点增量，并维护零值与存在位。
// 入参：table 为商品表，goods 为商品对象，delta 为有符号定点增量。
// 返回：无；修改 table，非法商品或 delta 为零时不修改。
// 地址：victoria3.exe+1027970。
void AddByGoods(GoodsTable* table, Goods* goods, int64 delta)
{
    if (delta == 0)
        return;

    int32 goodsId = goods->id; // goods+0x10
    if (!CallAt<bool>(0x1026630, goodsId)) // victoria3.exe+1026630，商品索引检查
        return;

    int32 wordIndex = goodsId >> 6;
    uint64 goodsMask = uint64(1) << (goodsId & 63);
    bool present = (table->presenceWords[wordIndex] & goodsMask) != 0;
    int64 previousValue = present ? table->values[goodsId] : 0;
    int64 nextValue = previousValue + delta;

    if (table->flags48 == 0 && nextValue == 0) {
        if (present) {
            table->values[goodsId] = 0;
            table->presenceWords[wordIndex] &= ~goodsMask;
            CallAt<void>(0x1026970, table, goodsId); // victoria3.exe+1026970，原始删除/整理调用
        }
        return;
    }

    CallAt<void>(0x1026700, table); // victoria3.exe+1026700，写入前的存储准备调用
    table->values[goodsId] = nextValue;
    table->presenceWords[wordIndex] |= goodsMask;
}
```

## `ComputeUnitRevenue`（`victoria3.exe+11FC080` 内联子过程）

本子过程将修正价格折算成价差，再把价差传入税补函数。它返回的是单位净收益，而不是成交价或最终意愿评分。

```cpp
// 功能：在选定上下文中计算方向价差，并折算为单位净收益。
// 入参：state 为 +11FC09F 已解析的州对象，evaluation 为评估表，candidate 为候选。
// 返回：单位净收益定点整数，由调用者写入 candidate+0x18。
// 地址：victoria3.exe+11FC080 内联子过程，对应 +11FC198 至 +11FC1ED，
//       或未复制上下文的 +11FC1FD 至 +11FC24D；不是独立 ABI 函数。
int64 ComputeUnitRevenue(State* state, TradeContext* evaluation,
                         Candidate* candidate)
{
    int64 priceDifference;
    PriceOrAdvantageDeltaCandidate(&priceDifference, state, candidate->goods,
                                  candidate->direction, evaluation); // victoria3.exe+140A6B0

    int64 unitRevenue;
    byte* rateContext = reinterpret_cast<byte*>(state) + 0x18;
    CalculateNetUnitProfit(rateContext, &unitRevenue, candidate->goods,
                           candidate->direction, priceDifference); // victoria3.exe+1207860
    return unitRevenue;
}
```

`PriceOrAdvantageDeltaCandidate` 沿用 `Docs/CheckTradeAdvantages1.md` 的地址命名；`Docs/important_notes/刷新候选函数.md` 中的 `CalculateDirectionalPriceDifference` 指的是同一个 `+140A6B0` 语义位置，不为同一地址另建函数名。

## `ReadDirectionGoodsValue`（`victoria3.exe+140A6B0` 内联读取）

沿用既有优势分析中的商品表读取名称；这里只抽取已重复出现的有效性检查与位图读取，不声明新的独立函数入口。

```cpp
// 功能：读取指定商品的表值；非法索引或不存在的表项按零处理。
// 入参：table 为商品表，goods 为商品对象；返回：有符号定点表值或零。
// 地址：victoria3.exe+140A6B0 内联读取，见 +140A738 至 +140A893 的重复片段。
int64 ReadDirectionGoodsValue(GoodsTable* table, Goods* goods)
{
    int32 goodsId = goods->id; // goods+0x10
    if (!CallAt<bool>(0x1026630, goodsId)) // victoria3.exe+1026630
        return 0;

    uint64 goodsMask = uint64(1) << (goodsId & 63);
    if ((table->presenceWords[goodsId >> 6] & goodsMask) == 0)
        return 0;
    return table->values[goodsId];
}
```

## `PriceOrAdvantageDeltaCandidate`（`victoria3.exe+140A6B0`）

这里展开算术和参数数据流。世界价格曲线 `+13A3280 → +13FAC30`、完整相对优势生成函数 `+13A3B10` 以及价格边界读取函数没有在本段伪造实现，保持原始调用。省略一次性初始化及界面说明文本路径。

```cpp
// 功能：计算两端有效价格，在贸易侧应用方向倍率和上下界后返回方向价差。
// 入参：output 为价差输出，state 为州对象，goods 为商品，direction 为方向，evaluation 为评估表。
// 返回：原 output 指针，价差通过 *output 写回；方向不是 0/1 时写零。
// 地址：victoria3.exe+140A6B0；沿用既有名称，不代表已确认的游戏符号。
int64* PriceOrAdvantageDeltaCandidate(int64* output, State* state,
                                     Goods* goods, uint8 direction,
                                     TradeContext* evaluation)
{
    byte* singleton = ReadGlobal<byte*>(0x58B8A50); // victoria3.exe+58B8A50 数据槽
    byte* manager = Load<byte*>(singleton + 0x608);
    byte* worldContext = Load<byte*>(manager + 0x120) + 0x508;

    int64 localPrice;
    CallAt<int64*>(0x1408330, &localPrice, goods, state, evaluation); // victoria3.exe+1408330

    int64 localDirectionQuantity;
    int64 directionExtraQuantity;
    if (direction == 0) {
        localDirectionQuantity = ReadDirectionGoodsValue(&evaluation->tables[0], goods);
        directionExtraQuantity = ReadDirectionGoodsValue(&evaluation->tables[7], goods);
    } else {
        localDirectionQuantity = ReadDirectionGoodsValue(&evaluation->tables[1], goods);
        directionExtraQuantity = ReadDirectionGoodsValue(&evaluation->tables[6], goods);
    }
    int64 table5Quantity = ReadDirectionGoodsValue(&evaluation->tables[5], goods);
    int64 table4Quantity = ReadDirectionGoodsValue(&evaluation->tables[4], goods);

    // +140A8B1：基准价格接收两张全局侧数量表的值，不直接读取 UI 世界价格。
    int64 baseTradePrice;
    CallAt<int64*>(0x13A3280, worldContext, &baseTradePrice, goods,
                  table4Quantity, table5Quantity); // victoria3.exe+13A3280

    // +140A8F7：沿用 ComputeRelativeTradeAdvantage 的名称，但保留此调用点实际的额外参数。
    // 第三个寄存器参数是 state，goods 是第五个参数；旧四参数概括不是完整 ABI。
    int64 relativeRatioFixed;
    CallAt<int64*>(0x13A3B10, worldContext, &relativeRatioFixed, state, direction,
                  goods, localDirectionQuantity, table4Quantity, table5Quantity,
                  directionExtraQuantity, nullptr); // victoria3.exe+13A3B10，ComputeRelativeTradeAdvantage

    // +140A910 至 +140A9C0：相对比值转倍率，再与基准价做定点乘法。
    int64 directionalMultiplier;
    ApplyRelativeAdvantageToPrice(&directionalMultiplier, relativeRatioFixed,
                                 direction); // victoria3.exe+13A5280
    int64 correctedPrice = FixedMultiply(baseTradePrice, directionalMultiplier);

    // +140A9CB/+140A9DE：从商品对象取得上下界；不假设它们恒为某个固定百分比。
    int64 upperPrice;
    int64 lowerPrice;
    CallAt<int64*>(0x1726A10, goods, &upperPrice); // victoria3.exe+1726A10
    CallAt<int64*>(0x1726AF0, goods, &lowerPrice); // victoria3.exe+1726AF0
    if (correctedPrice < lowerPrice)
        correctedPrice = lowerPrice;
    else if (correctedPrice > upperPrice)
        correctedPrice = upperPrice;

    if (direction == 0)
        *output = localPrice - correctedPrice; // +140AA16/+140AA1E
    else if (direction == 1)
        *output = correctedPrice - localPrice; // +140AA09
    else
        *output = 0;
    return output;
}
```

上述 `localPrice` 与 `baseTradePrice` 是计算上下文中的两端价格。将它们分别解释为本地价和世界价是经济层解释，不能认定它们就是同一时点 UI 显示的两个裸价格；增加模式还会受到模拟表加量的影响。

## `ApplyRelativeAdvantageToPrice`（`victoria3.exe+13A5280`）

沿用已生成的函数名。此处按实际三个寄存器参数展开：`RCX=output`、`RDX=relativeRatioFixed`、`R8B=direction`；没有一个额外的商品指针参数。

```cpp
// 功能：把以 100000 为中性的相对优势比值转换为方向价格倍率。
// 入参：output 为倍率输出，relativeRatioFixed 为未减中性值的定点比值，direction 为方向。
// 返回：原 output 指针；方向 0 写倒数倍率，非零方向写正向倍率。
// 地址：victoria3.exe+13A5280。
int64* ApplyRelativeAdvantageToPrice(int64* output, int64 relativeRatioFixed,
                                    uint8 direction)
{
    const int64 SCALE = 100000;
    int64 priceCoefficient = ReadGlobal<int64>(0x5889E10); // victoria3.exe+5889E10
    int64 remainingCoefficient = SCALE - priceCoefficient;
    int64 multiplier = relativeRatioFixed;

    if (relativeRatioFixed > SCALE) {
        int64 positiveDifference = relativeRatioFixed - SCALE;
        multiplier -= FixedMultiply(positiveDifference, remainingCoefficient);
    } else {
        int64 negativeDifference = SCALE - relativeRatioFixed;
        multiplier += FixedMultiply(negativeDifference, remainingCoefficient);
    }

    if (direction == 0) {
        if (multiplier == 0)
            *output = int64(0x00000000FFFFFFFF); // +13A540F：EAX 写入后零扩展，不是 int64(-1)
        else
            *output = trunc(int64(10000000000) / multiplier); // +13A541F/+13A542B
    } else {
        *output = multiplier; // +13A5439
    }
    return output;
}
```

`function_13A5280.json` 中 `+13A52B0/+13A5364` 的操作数注释为 `[000061A8]`，即 `25000`。`function_9C21A0.json` 同时将该数据槽与 `TRADE_CENTER_ADVANTAGE_PRICE_MULTIPLIER` 关联。因此采集时 `priceCoefficient/100000 = 0.25` 有直接证据，而不是寻找不存在的 `25000` 立即数。

忽略定点截断时，令 `r = relativeRatioFixed/100000 - 1`，正向倍率为 `M=1+0.25r`，方向 `0` 的倍率为 `1/M`。真正机器码先分支定点乘法，再执行定点倒数，不能用一个浮点公式宣称逐位等价；此函数也没有将倍率改善钳到 `25%`，价格边界在上层处理。

## `CalculateNetUnitProfit`（`victoria3.exe+1207860`）

沿用 `Docs/important_notes/刷新候选函数.md` 中净收益调用的名称，补充该调用的地址和真实数据流。税补所乘的是商品基价，不是修正后的成交价格。

```cpp
// 功能：将方向价差加上商品基价折算的补助，再减去商品基价折算的关税。
// 入参：rateContext 为州对象 +0x18 的上下文，output 为净收益输出，goods 为商品，
//       direction 为方向，priceDifference 为已计算的税补前价差。
// 返回：原 output 指针，单位净收益通过 *output 写回。
// 地址：victoria3.exe+1207860。
int64* CalculateNetUnitProfit(byte* rateContext, int64* output, Goods* goods,
                              uint8 direction, int64 priceDifference)
{
    const int64 SCALE = 100000;
    int16 rawBaseCost = LoadSignedWord(reinterpret_cast<byte*>(goods) + 0x44);
    int64 baseCostFixed = SCALE;
    if (rawBaseCost > 0)
        baseCostFixed = int64(rawBaseCost) * SCALE;

    // +12078A5/+12078B9/+12078C8：解析政策拥有者并查询该商品、方向的政策级别。
    byte* tariffObject = CallAt<byte*>(0x7C96A0, rateContext + 0x08); // victoria3.exe+7C96A0
    uint32 tariffOwnerId = Load<uint32>(tariffObject + 0xE48);
    byte* tariffOwner = CallAt<byte*>(0x7B0AB0, &tariffOwnerId); // victoria3.exe+7B0AB0
    int16 tariffPolicy = CallAt<int16>(0xC19460, tariffOwner, goods, direction); // victoria3.exe+C19460
    int64 tariffRate;
    CallAt<int64*>(0x1206D40, rateContext, &tariffRate, goods, direction,
                  tariffPolicy, nullptr); // victoria3.exe+1206D40，ReadEffectiveTariff
    int64 tariffPerUnit = FixedMultiply(baseCostFixed, tariffRate);

    // +120799D/+12079B1/+12079C0：opcode 再次查询政策，不合并成未经证明的共享缓存。
    byte* subventionObject = CallAt<byte*>(0x7C96A0, rateContext + 0x08); // victoria3.exe+7C96A0
    uint32 subventionOwnerId = Load<uint32>(subventionObject + 0xE48);
    byte* subventionOwner = CallAt<byte*>(0x7B0AB0, &subventionOwnerId); // victoria3.exe+7B0AB0
    int16 subventionPolicy = CallAt<int16>(0xC19460, subventionOwner, goods, direction); // victoria3.exe+C19460
    int64 subventionRate;
    CallAt<int64*>(0x1207370, rateContext, &subventionRate, goods, direction,
                  subventionPolicy, nullptr); // victoria3.exe+1207370，ReadSubsidy
    int64 subventionPerUnit = FixedMultiply(baseCostFixed, subventionRate);

    *output = subventionPerUnit - tariffPerUnit + priceDifference; // +1207A81/+1207A84/+1207A8F
    return output;
}
```

有效税率/补助率函数的导出已存在，本段将其作为有地址的外部调用，而非默认零值或直接使用 UI 政策百分比。其普通路径包含政策级别倍率、方向修正，关税还包含商品专用修正；特殊州标志可使税补归零，提示文本引用 `TREATY_PORT_NO_TARIFFS_OR_SUBVENTIONS`。相关具体 opcode 保留在证据表列出的两个文件中。

## 展开后的收益数据流

```text
mode == 1：复制八张表，按方向把 q 加入两张表
mode != 1：原上下文，不先减 q
    ↓
+140A6B0：两端价格 → 相对优势倍率/倒数 → 修正贸易侧价格 → 限价 → ΔP
    ↓
+1207860：baseCost = max(1, signed_word(goods+0x44))
          p = ΔP + FixedMultiply(baseCostFixed, subventionRate)
                 - FixedMultiply(baseCostFixed, tariffRate)
    ↓
+11FC080：c+0x18 = p
          c+0x10 = FixedMultiply(c+0x38, p)
    ↓
+11FC320：读取 c+0x10，在基础收益上合成最终意愿评分 c+0x20
```

仍未在这里恢复的实现边界包括：复制构造器的内部存储管理、`+1408330` 的本地价格曲线、`+13A3280/+13FAC30` 的另一端价格曲线、完整的 `+13A3B10` 相对比值生成、两个商品价格边界的读取实现以及税补率函数的逐条函数体。这些边界不妨碍确认上述调用顺序、表加量、倍率方向、税补符号和候选字段写回，也不表示已完整还原游戏交易执行逻辑。
