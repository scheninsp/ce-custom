# 供给评估上下文的分析摘录

原始来源：`Output/market_tables/context_ghidra` 中的 C、TSV 与元数据文件。
这是相关字段路径的语义摘录，省略无关表、候选筛选和容量处理，不是完整函数。

```cpp
// 功能：初始化州贸易调整条目；入参为条目和州对象；返回初始化的条目。
// 地址：victoria3.exe+11FD230；这里只表示两个净调整表的初始状态。
FUN_1411fd230(entry, state) { // victoria3.exe+11FD230
    entry.table10 = empty; // 出口净调整表
    entry.table60 = empty; // 进口净调整表
    return entry;
}

// 功能：构造评估上下文；入参为州条目、输出 X、市场进口/出口调整表及全局表；返回 X。
// 地址：victoria3.exe+11FD370；省略全局数量和加权价值表。
FUN_1411fd370(entry, X, marketImportDelta, marketExportDelta, otherTables) { // victoria3.exe+11FD370
    X.table00 = copy(entry.table60); // 复制赋值：victoria3.exe+C10560
    X.table50 = copy(entry.table10); // 复制赋值：victoria3.exe+C10560
    X.tableA0 = copy(marketExportDelta);
    X.tableF0 = copy(marketImportDelta);
    subtractTable(X.tableA0, entry.table10); // victoria3.exe+1027E20
    subtractTable(X.tableF0, entry.table60); // victoria3.exe+1027E20
    return X;
}

// 功能：提取已执行进口增加时的调整量记录；入参为州条目与共享调整表；返回是否调整。
// 地址：victoria3.exe+11FD470；省略出口方向及其他处理。
FUN_1411fd470(entry, marketImportDelta, otherTables) { // victoria3.exe+11FD470
    if (increaseAccepted && direction == 0) {
        AddByGoods(entry.table60, goods, q); // victoria3.exe+1027970
        AddByGoods(marketImportDelta, goods, q); // victoria3.exe+1027970
    }
    // 撤销进口通过 +11FAF20 向这两张表减 q（+1027A40）。
}
```

`copy`、`subtractTable` 和 `empty` 为操作记法，不是新增的可执行函数命名。
两项相加在整数域还原市场分组进口净调整：`X[00]+X[F0]=marketImportDelta`。
基础读取沿用 `FUN_1411fd0d0`（victoria3.exe+11FD0D0）：`S=M[228]+X[00]+X[F0]`。
