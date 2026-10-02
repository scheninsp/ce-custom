# Refresh ->CalculateQuantityPerCapacity (+122AB50)

## CalculateQuantityPerCapacity
功能：计算刷新候选时，指定州每单位贸易容量能够产生的货品数量


# Refresh ->ReadOrComputeDirectionalTradeAdvantage（+11FBDA0）

## ReadOrComputeDirectionalTradeAdvantage 
读取指定州、商品和贸易方向的绝对贸易优势
->
BuildDirectionalTradeContext
ComputeAbsoluteTradeAdvantage

BuildDirectionalTradeContext
ComputeAbsoluteTradeAdvantage
两个被伪代码解释二合一
->
ComputeDirectionalAdvantage
功能：按方向和商品构造贸易优势计算上下文，并调用内部优势计算器。


ComputeAbsoluteTradeAdvantage
功能：构造州/市场/商品/方向上下文，并把定点优势中间值写入方向商品缓存。
->
BuildStateGoodsDirectionValue
功能：从州/市场、商品和方向构造绝对优势候选值。
BuildMarketTradeFraction
功能：从州关联市场对象读取贸易份额相关输入，并生成定点修正值。


# Refresh ->UpdateCandidateShortage (UpdateCandidatePartA，+11FBA60)
// 功能：计算候选商品的短缺指标，并写入候选对象的 c+30。该指标只用于方向 0。

# Refresh ->UpdateCandidateRevenue (UpdateCandidatePartB,+11FC080)
// 功能：按增加或减少模式准备收益计算上下文，计算单位净收益和基础收益。


# Refresh ->CalculateDesirability (+11FC320)
// 功能：检查候选数量限制，并合成最终意愿评分。


# Refresh 中调整量的计算已得到数据验证
验证数据在 `Docs\important_notes\刷新候选函数进出口数量输出分析.md` L161。
算法：
每 1 单位贸易容量承载的商品量 = traded_quantity
贸易中心生产方式带来的修正 = modifier_raw（需转换定点数）
q_raw = FixedMultiply(base_raw, 100000 + modifier_raw)
q_raw = max(q_raw, MINIMUM_GOODS_TRADED_QUANTITY)
MINIMUM_GOODS_TRADED_QUANTITY = 0.5 * 100000 = 50000 （定点数）

累计商品变化 = Σ每次成功增加的 q_i - Σ每次成功减少的 q_i
