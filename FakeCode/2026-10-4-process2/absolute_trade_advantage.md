# 绝对贸易优势计算伪代码

2026-10-06。来源：`FakeCode/ghidra_refresh_20261003/function_1226160.md`、
`function_1228B90.md`、`function_13C2350.md` 及
`Output/2026-10-4-process2/absolute_trade_advantage` 的带字节反汇编。
沿用既有名称；`FUN_...` 仍沿用 Ghidra 名称。以下省略引用计数、说明文本与异常清理。
`mul`、`div` 是定点算术记号，不是新命名的游戏函数；比例一单位为 100000。
大数路径见原始反编译，不能用浮点运算替代后声称逐位一致。

## FillGoodsDirectionContext

```text
// 功能：向优势上下文加入商品、外交加项及商品/方向倍率。
// 入参：s 为 Refresh 解析 s+20 后取得的州相关对象；t 为数值上下文；g 为商品；d 为方向。
// 返回：无，写入 t；d=0 进口，d=1 出口。
function FillGoodsDirectionContext(s, t, g, d): // victoria3.exe+1226160
    attributes = read_ptr(s + 0x18B0)
    market = resolve_effective_market(s) // 内联辅助链：+120D3D0、+7C0380
    marketOwner = resolve_country(market.ownerRef) // +7B0AB0
    area = market + 0x18
    globalProduction = read_goods(world + 0x5F8, g) // +10276F0

    if d == 1 and globalProduction > 0:
        areaMarket = resolve_market(s + 0xB48) // +7C33B0
        areaGoods = FUN_140cfcbf0(area, areaMarket) // victoria3.exe+CFCBF0
        production = read_goods(areaGoods, g)
        productionShare = div(production, globalProduction)
        productionContribution = mul(200*S, mul(read_i64(s+0x58), productionShare))
        t.add += productionContribution
        charterProduction = FUN_140cfccd0(area, areaMarket, g) // victoria3.exe+CFCCD0
        if production > 0 and charterProduction > 0:
            t.add += mul(50*S, div(charterProduction, production))
        prestigeShare = FUN_141027410(areaGoods, g) // victoria3.exe+1027410
        if prestigeShare > 0:
            t.add += mul(100*S, prestigeShare)

    opposite = 1-d
    globalOpposite = FUN_1411f9790(world+0x508, g, opposite) // victoria3.exe+11F9790
    ownOpposite = FUN_141254850(area, g, opposite) // victoria3.exe+1254850
    if globalOpposite > 0:
        markets = world.goodsMarkets[g][opposite] // +13A5590/+13A5630
        for other in markets:
            if other.id == market.id:
                continue
            linkedProduction = read_directional_production(area, other, g, d) // +CFCDE0/+CFCE60
            if ownOpposite > 0 and linkedProduction > 0:
                w = div(linkedProduction, ownOpposite)
            else:
                w = div(FUN_141254850(other+0x18, g, opposite), globalOpposite)
            w = clamp(w, 0, S)
            if w <= 0:
                continue
            otherOwner = resolve_country(other.ownerRef)
            if FUN_140c35550(marketOwner, otherOwner): // victoria3.exe+C35550，贸易特权判定
                t.add += mul(100*S, w)
            treatyPortAmount = read_treaty_port_directional_goods(other, s.owner, g, d) // +CFCB90/+CFCB30
            if treatyPortAmount > 0:
                t.add += mul(200*S, div(treatyPortAmount, globalOpposite))
            if FUN_1413cfcc0(s.owner, otherOwner): // victoria3.exe+13CFCC0，集团关系判定
                blocBonus = modifier(s.owner.powerBloc, power_bloc_trade_advantage_add)
                if blocBonus > 0:
                    t.add += mul(blocBonus, w)
            if s.owner.religion == otherOwner.religion:
                religionBonus = modifier(attributes, state_trade_advantage_same_religion_add)
                if religionBonus > 0:
                    t.add += mul(religionBonus, w)
            if FUN_140eb1c60(diplomacy, otherOwner, marketOwner): // victoria3.exe+EB1C60，禁运
                t.add += mul(-100*S, w)
            else if FUN_140c35d50(s.owner, otherOwner): // victoria3.exe+C35D50，战争
                t.add += mul(-75*S, w)
            else:
                tier = FUN_140f69380(interestManager, s.owner, other) // victoria3.exe+F69380
                if tier.rank > 0 or not rule(s.owner, country_no_advantage_loss_from_lack_of_interest_bool):
                    tierBonus = read_i64(tier + (0x1D8 if d==1 else 0x1E0))
                    t.add += mul(tierBonus, w)

    t.percent += modifier(attributes, goods_modifier_table[g.id*28 + 10])
    t.percent += modifier(attributes, state_import_advantage_mult if d==0 else state_export_advantage_mult)
```

上面 `read_directional_production`、`read_treaty_port_directional_goods` 等是内联表达式记法，
不是新增独立游戏函数。须使用文档中给出的真实 ABI：辅助函数有输出指针，原反编译可能漏显参数。

## BuildMarketTradeFraction

```text
// 功能：加入通用倍率、威望商船倍率、容量倍率和最终接入度乘数。
// 入参：s 为州相关对象；t 为上下文；返回：无，原位写回。
function BuildMarketTradeFraction(s, t): // victoria3.exe+1228B90
    a = read_ptr(s+0x18B0)
    t.percent += modifier(a, state_trade_advantage_mult)
    tradeCenter = FUN_141231b10(s) // victoria3.exe+1231B10
    if tradeCenter.virtual_valid() and tradeCenter.level > 0:
        merchantInputs = FUN_140e3fc40(tradeCenter) // victoria3.exe+E3FC40
        prestigeMerchantShare = FUN_141027410(merchantInputs, merchant_marine) // victoria3.exe+1027410
        if prestigeMerchantShare > 0:
            t.percent += mul(0.25*S, prestigeMerchantShare)
    capacity = read_i32(s+0x1D58)
    capacityBonus = mul(capacity*S, modifier(a, state_trade_advantage_from_capacity_add))
    t.percent += min(capacityBonus, modifier(a, state_max_trade_advantage_from_capacity_add))
    accessFactor = read_i64(s+0x68)
    if accessFactor < S:
        t.product = mul(t.product, accessFactor)
```

## NormalizeAdvantage

```text
// 功能：先合计加项，乘百分比合计，再乘独立乘数，并按上下界裁剪。
// 入参：t 为数值上下文；output 为结果地址；返回：output。
function NormalizeAdvantage(t, output): // victoria3.exe+13C2350
    x = t.base + t.add
    m = S + t.percent
    if not t.allowNegativeMultiplier and m < 0:
        m = 0
    first = mul(x, m)
    if x != 0 and m != 0 and first == 0:
        first = 1 if x > 0 else -1
    result = mul(first, t.product)
    *output = clamp(result, t.lower, t.upper)
    return output
```

`Refresh`（victoria3.exe+11FBDA0）初始化上述上下文，`WrapNumericContext`
（victoria3.exe+1226080）加入基础 100 点，结算后取 `max(result,100000)`，
即至少 **1 点**，再通过 `UpdateAdvantageCache`（victoria3.exe+1027760）保存。
