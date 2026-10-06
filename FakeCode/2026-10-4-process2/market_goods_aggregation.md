# 市场商品表重建的分析伪代码

来源：`Output/market_tables/ghidra/function_CFD550.c`、`function_CFDD40.c` 及同名 TSV。
保留已导出 Ghidra 名称；这里仅提取与目标表相关的路径，不代表完整函数。
市场对象 M 的统计子对象 B 位于 M+0x18；所有下标为十六进制偏移。

```cpp
// 功能：提取市场统计重建中的目标表更新；入参为统计子对象 B；无返回值。
// 地址：victoria3.exe+CFD550；以下为相关路径的分析摘录。
void FUN_140cfd550(B) { // victoria3.exe+CFD550
    ClearGoodsTables(B);
    M = ResolveMarketReference(B + 8);
    for (stateRef : M[7B0 .. 7BC]) {
        state = Resolve(stateRef); // victoria3.exe+7C96A0
        FUN_140cfdd40(&B, state); // victoria3.exe+CFDD40
    }
    // 此处处理经筛选的国家关系条款；细节存在反编译跳转表警告。
    // FUN_140cfe5a0 将正数量累加到 B[3B0] 或 B[400]。
    ProcessFilteredRelations(B); // 内部调用 victoria3.exe+CFE5A0
    AddTable(B[1C0], B[400]); // victoria3.exe+1027CE0
    AddTable(B[210], B[3B0]); // victoria3.exe+1027CE0
    // B[450]、B[4A0] 为另外的组合表，不是本次 M[228]/M[2D8]。
}

// 功能：提取单州对市场目标表的累加；入参为统计子对象指针和州；无返回值。
// 地址：victoria3.exe+CFDD40；省略其他统计表和缓存的更新。
void FUN_140cfdd40(Bptr, state) { // victoria3.exe+CFDD40
    B = *Bptr;
    if (HasPresentGoods(state[498])) {
        AddTable(B[2C0], state[498]); // victoria3.exe+1027CE0
    }
    access = state[58];
    if (access > 0) {
        sell = CopyTable(state[C8]); // victoria3.exe+C104C0
        buy  = CopyTable(state[78]); // victoria3.exe+C104C0
        ScaleTable(sell, access); // victoria3.exe+10283B0
        ScaleTable(buy, access);  // victoria3.exe+10283B0
        AddTable(B[1C0], buy);   // victoria3.exe+1027CE0
        AddTable(B[210], sell); // victoria3.exe+1027CE0
    }
}
```

`AddTable` 为上文语义占位，实际沿用 `FUN_141027ce0`（victoria3.exe+1027CE0）；
`ScaleTable` 实际沿用 `FUN_1410283b0`（victoria3.exe+10283B0）。
其余语义占位不是新命名的可执行函数，不能据此设置执行断点。

对应关系：B[210]=M[228]、B[2C0]=M[2D8]、B[3B0]=M[3C8]、B[400]=M[418]。
`state[58]` 与 `state[68]` 是不同字段，不应混用；前者业务名称未独立确认。
