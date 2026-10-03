void UpdateCandidateRevenue(Candidate* c, TradeContext* context)
{
    TradeContext simulated = *context;
    ApplyCandidateToSimulation(&simulated, c);
    c->unitRevenue = ComputeUnitRevenue(&simulated, c);
    c->baseRevenue = FixedMultiply(c->quantity, c->unitRevenue);
}
ApplyCandidateToSimulation
ComputeUnitRevenue
检查这两个函数的具体内容
分析如何使用 P_export/P_import -> 基础收益 R


对于刷新候选函数Refresh，是否每周每中心每商品只 Refresh 一次，同商品本周容量最多调整几次？
`Docs\2026-10-3-process01\plans\贸易周期自动编排2.md` 执行时进程崩溃了。



