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
// 地址：victoria3.exe+11FC080。
void UpdateCandidateRevenue(Candidate* c, TradeContext* context)
{
    TradeContext simulated = *context;
    ApplyCandidateToSimulation(&simulated, c);
    c->unitRevenue = ComputeUnitRevenue(&simulated, c);
    c->baseRevenue = FixedMultiply(c->quantity, c->unitRevenue);
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

