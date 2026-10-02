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


# Refresh ->UpdateCandidateRevenue (UpdateCandidatePartB,+11FC080)



# Refresh ->CalculateDesirability (+11FC320)