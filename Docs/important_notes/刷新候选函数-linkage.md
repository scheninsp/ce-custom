# Refresh ->CalculateQuantityPerCapacity (+122AB50)

## CalculateQuantityPerCapacity
功能：计算刷新候选时，指定州每单位贸易容量能够产生的货品数量


# Refresh ->ReadOrComputeDirectionalTradeAdvantage（+11FBDA0）

## ReadOrComputeDirectionalTradeAdvantage 
读取指定州、商品和贸易方向的绝对贸易优势
->
BuildDirectionalTradeContext
功能：按方向和商品构造贸易优势计算上下文
+
ComputeAbsoluteTradeAdvantage
功能：把定点优势中间值写入方向商品缓存。
->
BuildStateGoodsDirectionValue
功能：从州/市场、商品和方向构造绝对优势候选值。
BuildMarketTradeFraction
功能：从州关联市场对象读取贸易份额相关输入，并生成定点修正值。

绝对贸易优势会被用来计算相对贸易优势，然后决定商品进口价格。
来源于开发日志和wiki猜测（Docs\trade_center_model1.md）

# Refresh ->UpdateCandidateShortage (UpdateCandidatePartA，+11FBA60)
// 功能：计算候选商品的短缺指标，仅对进口商品返回非0值
有效供给低于需求的一半时，返回短缺评分>0。短缺评分在0~0.5之间，越大的值代表短缺程度越强。
shortage_unclamped = 1 - (supply/demand) / 0.5
shortage = clamp(shortage_unclamped, 0, 0.5)

# Refresh ->UpdateCandidateRevenue (UpdateCandidatePartB,+11FC080)
// 功能：按增加或减少模式准备收益计算上下文，计算单位净收益和基础收益。
计算单位净收益 `p`
还会返回本次调整量的基础收益 `R = q × p`
这份伪代码没有展开价差和单位净收益的内部公式。

# Refresh ->CalculateDesirability (+11FC320)
// 功能：检查候选数量限制，并合成最终意愿评分。
参考（`Docs\important_notes\刷新候选函数评分影响因子分析.md`）

本市场方向量超过外部反方向可承接量的两倍时，候选直接无效
D ≈ R
   - 25 × max(有效关税率, 0)
   + 补助差额评分
   - 1000 × 反方向市场份额
   + 300 × 短缺评分 H

补助差额评分 = 本方向补助率 × 100 - 反方向补助率 × 100
若差额为正，且方向为 0（需要进口）、则认为候选是供给不足，则补助差额评分再乘 20

反方向市场份额 = 当前本地市场的反方向数量/世界市场的反方向数量

短缺评分在上面函数 UpdateCandidateShortage



# Refresh 中调整量的计算已得到数据验证
验证数据在 `Docs\important_notes\刷新候选函数进出口数量输出分析.md` L161。
算法：
每 1 单位贸易容量承载的商品量 = traded_quantity
贸易中心生产方式带来的修正 = modifier_raw（需转换定点数）
q_raw = FixedMultiply(base_raw, 100000 + modifier_raw)
q_raw = max(q_raw, MINIMUM_GOODS_TRADED_QUANTITY)
MINIMUM_GOODS_TRADED_QUANTITY = 0.5 * 100000 = 50000 （定点数）

累计商品变化 = Σ每次成功增加的 q_i - Σ每次成功减少的 q_i
