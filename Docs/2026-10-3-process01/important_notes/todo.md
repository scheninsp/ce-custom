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

