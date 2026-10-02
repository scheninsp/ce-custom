# goal3：当前断点及上层调用链的静态反汇编分析

分析日期：2026-10-02（北京时间）。本次保持当前断点暂停，仅采集寄存器、栈、内存和指令；没有单步、继续游戏、修改内存或运行游戏对照实验。下文伪代码是根据机器码人工整理的语义表达，不是恢复出的原始源码。

## 1. 目前最有价值的结论

1. **当前函数 `victoria3.exe+11FD470` 很像“对一个州尝试执行一次贸易调整”**：刷新增加/减少两个候选，比较评分及容量，按一个容量单位增减商品贸易，消耗本轮操作次数，并更新容量缓存。
2. **直接上层 `+131C2B0` 可以较高可信度命名为 `UpdateStateTrades`**。机器码直接引用了该字符串和 `source/logic/statemanager.cpp`；它建立州条目数组、排序、反复计算候选并尝试调整，直到一轮没有成功操作。
3. 更上层是单个 Tick 任务执行器、Tick 任务列表调度器、推进一次 Tick 的函数和外围 Tick 包装函数。当前调用链明显属于模拟更新；没有看到 UI 数字格式化链的特征。但这一次暂停本身不能证明贸易任务的每周调度频率。
4. 当前被考虑增加的商品是 **`wood`（软木，ID 10）**，被考虑减少的商品是 **`fine_art`（艺术品，ID 52）**。只限制九州对象的断点会命中不同商品，本次现场不是硬木候选。
5. 数量换算已找到一个很具体的函数：`+122AB50` 读取商品基础交易量、州修正值和最小交易量，计算**一次容量调整对应的商品数量**。硬木最终分配多少容量，仍取决于候选选择和多轮调整，不能仅由该函数解释。

可信度约定：**已证实**表示可以直接读到的指令、字符串或本次内存值；**高可信推断**表示多个调用和数据流共同支持；**待确认**表示结构名称、业务方向或完整数学语义尚未闭合。

## 2. 采集范围与调用链依据

### 2.1 暂停现场

| 项目 | 本次值 |
| --- | --- |
| 进程 | `victoria3`，PID `43884` |
| 模块基址 | `7FF776AF0000` |
| 断点 RIP | `7FF777CED5C9`，即 `+11FD5C9` |
| RSP / 线程 | `8C5DE8D870` / `60D0` |
| R14 | `3A484D9DB60`，任务原文识别的九州对象 |
| RDI | `3A5FF822A80`，当前大小为 `0x140` 的处理条目 |
| 模块构建标识 | PE 时间戳字段 `6A3BF239`，只作构建身份记录 |

原始采集时间保留 UTC，例如开始快照 `2026-10-01T16:24:56.823716+00:00` 对应北京时间 2026-10-02。证据目录：[Output/goal3_static_20261002](../Output/goal3_static_20261002)。

### 2.2 不是把所有栈内代码指针都当成调用者

原始工具只扫描 128 个栈槽，返回了一层候选。本次另读了从 RSP 开始的 8192 字节，利用程序 `.pdata` 中的函数范围和展开记录计算返回槽，再核对函数序言、现场返回地址和调用点。

六层的展开记录均与目标进程内存中的字节相同，采集到的六个主函数所有已解码指令也与对应程序文件字节一致。各层在调用点已完成序言，使用的展开记录无链式展开标志；下表中的栈增量包括局部栈和压栈保存寄存器，不包括返回地址本身。

| 层级 | 所在函数入口 | 当前栈指针 | 到返回槽增量 | 返回槽 | 返回地址 |
| --- | --- | --- | --- | --- | --- |
| 0 当前 | `7FF777CED470` / `+11FD470` | `8C5DE8D870` | `0x328` | `8C5DE8DB98` | `7FF777E0D21E` |
| 1 | `7FF777E0C2B0` / `+131C2B0` | `8C5DE8DBA0` | `0x1348` | `8C5DE8EEE8` | `7FF7772A8563` |
| 2 | `7FF7772A81E0` / `+7B81E0` | `8C5DE8EEF0` | `0x458` | `8C5DE8F348` | `7FF7772AE76D` |
| 3 | `7FF7772AE1B0` / `+7BE1B0` | `8C5DE8F350` | `0x318` | `8C5DE8F668` | `7FF7772C65A8` |
| 4 | `7FF7772C6400` / `+7D6400` | `8C5DE8F670` | `0xA8` | `8C5DE8F718` | `7FF777E6C9E7` |
| 5 | `7FF777E6C990` / `+137C990` | `8C5DE8F720` | `0x128` | `8C5DE8F848` | `7FF7777B0D4D` |

第 5 层以上本轮不展开。原始计算见 [unwind_frames.json](../Output/goal3_static_20261002/unwind_frames.json)。栈扫描产生的其他候选保存在独立文件中，不作为本报告调用链。

实际逻辑链中还有不新增栈帧的尾跳转：

```text
+137C990  Tick 外围包装
  call +7D6400   推进一次 Tick
    call +7BE1B0   执行 Tick 任务列表
      call +7B81E0   执行一个任务的多个上下文阶段
        call [callback.vtable+0x10]
          +7C49D0   回调适配：取 callback+8，再跳 [owner.vtable+0x38]
            +1319B40   取上下文中的州管理器，然后尾跳
              +131C2B0   UpdateStateTrades
                call +11FD470   尝试一次州贸易调整
```

虚调用也作了现场核对：`[8C5DE8EF88]=8C5DE8EF50`，回调虚表 `7FF77AEC54B8` 的 `+0x10` 指向 `+7C49D0`；回调内对象 `3A53587E4F0` 的虚表 `+0x38` 指向 `+1319B40`，后者机器码明确尾跳 `+131C2B0`。因此不能把这两个跳板遗漏后，误称 `+7B8560` 是直接调用贸易函数。

## 3. 当前函数：`+11FD470`，尝试一次州贸易调整

[完整反汇编](../Output/goal3_static_20261002/function_7FF777CED470.md)，415 条可达指令。

### 3.1 条目与候选结构的初步解释

以下对象先称为“州/贸易状态对象”，暂不把它认定为独立的贸易中心建筑对象。

| 条目偏移 | 推测用途 | 当前值或证据 |
| --- | --- | --- |
| `+00`，32 位 | 本轮初始操作预算 | `11`；构造时由 `+12295A0` 返回 |
| `+04`，32 位 | 本轮剩余操作预算 | `11`；构造时复制 `+00`，成功时减 1 |
| `+08` | 州引用/句柄 | 解析后得到 R14；当前低 32 位 `894` |
| `+0C`，32 位 | 分组键，疑似市场或相关对象 ID | `6`；上层用这四个字节做哈希，确切类型待确认 |
| `+10` / `+60` | 两个方向的临时商品数值表 | 按候选方向选择其中之一 |
| `+B0` | 增加候选，大小 `0x48` | 商品 `wood` |
| `+F8` | 减少候选，大小 `0x48` | 商品 `fine_art` |

两个候选内部结构相同：`+00` 商品指针，`+08` 单字节方向，`+10/+18` 评分相关中间值，`+20` 贸易意愿评分，`+28` 州引用，`+2C` 增加/减少计算模式，`+38` 单次交易量，`+40` 贸易优势相关系数。

方向字段必须按**一个字节**读取，不能把紧随其后的未初始化/填充字节解释成指针。例如条目 `+B8` 的八字节看起来像地址，但相关指令只读取最低字节 `0`。

`state+1D58` 推测是容量上限，`state+1D5C` 推测是已用容量：当后者大于等于前者且不能移除旧贸易时，当前函数终止该条目。本次直接内存读取确认二者都为 `126`。`state+1D88` 已确认是按商品 ID 索引的带符号数值表，业务上高度符合商品容量分配表。

### 3.2 伪代码

`fp` 表示缩放为 `100000` 的定点数。`MulFixed` 表示原汇编的定点乘法；常用数值范围可理解为乘积除以 `100000` 后向零截断，大值路径还包含分解运算，精确复算须保留该路径的舍入行为。

来源：11FD470 附近 opcode
```text
// 功能：尝试对一个州执行一次贸易增减。
// 入参：条目 e，以及六个市场/汇总数值表参数；返回：本次是否发生调整。
function TryAdjustStateTrade(e, table1, table2, table3, table4, table5, table6):
    state = Resolve(e.stateRef)
    if not state.isValid() or e.remaining <= 0:
        return false
    initializing = GameState.flag148
    if not valid(e.remove.goods) and not valid(e.add.goods):
        if not initializing: e.remaining = 0
        return false

    context = BuildContext(e, table1..table6)       // +11FD370
    if valid(e.remove.goods): Refresh(e.remove, context) // +11FBDA0
    if valid(e.add.goods): Refresh(e.add, context)
    used = state.field1D5C
    limit = state.field1D58
    removed = false

    if valid(e.remove.goods):
        maintain = 25fp
        if initializing: maintain = MulFixed(maintain, 0.75fp)
        betterReplacement = (
            used >= limit and e.remove.goods != e.add.goods
            and MulFixed(e.remove.score, 2fp) < e.add.score
        )
        if betterReplacement or e.remove.score < maintain:
            RemoveOneTradeUnit(e.remove, context)  // +11FAF20，参数细节见后文
            removed = true

    if not removed and used >= limit:
        e.remaining = 0
        return false

    added = MeetsIncreaseThreshold(e.add)          // +11FBC80，通常要求 score >= 50fp
    if added:
        if valid(e.add.goods) and (goods.flags40 & 2) and not (goods.flags40 & 1):
            sign = +1 if e.add.direction == 1 else -1
            AddByGoods(state.table1D88, e.add.goods, sign * 1fp)
            AddByGoods(selectedDirectionTable, e.add.goods, e.add.quantity)
            AddByGoods(selectedMarketTable, e.add.goods, e.add.quantity)
            AddByGoods(selectedGlobalTable, e.add.goods, e.add.quantity)
            AddByGoods(selectedValueTable, e.add.goods,
                       MulFixed(e.add.quantity, e.add.advantage))
        if not initializing:
            RecordTradeIncreaseDate(state, e.add.goods) // +122BED0

    if added or removed:
        e.remaining -= 1
        RefreshCapacityCaches(state)              // +122BF50
        NotifyStateChange(state, 3)                // +C46410，事件 3 的正式含义待确认
        return true

    if initializing:
        e.remaining -= 1
    else:
        e.remaining -= max(1, round(e.initialBudget * 0.2))
    return false
```

关键证据：`+11FD6FD` 的容量比较；`+11FD7BF/+11FD7C8` 的替换/维持评分比较；`+11FD869` 清空预算；`+11FD93B` 的商品容量增量；`+11FDA35` 成功减 1；`+11FDB66` 失败按计算量扣减。失败舍入代码先按正负加减 `50000`，再除以 `100000`；对非负预算相当于通常的四舍五入。

这里的 `added` 按代码实际含义是“通过增加门槛”，不是某个下游函数返回的成交成功。真实数值写入还受商品有效性和 `flags40` 检查约束，不能把两者混成一个交易结果。

### 3.3 当前现场能预测什么

| 输入 | 原始值 | 按定点解释 |
| --- | --- | --- |
| 增加候选商品 | `3A4012E4A60`，`+10=10`，名称 `wood` | 软木 |
| 减少候选商品 | `3A4012E94C0`，`+10=52`，名称 `fine_art` | 艺术品 |
| 增加候选评分 `e+D0` | `9921745` | `99.21745` |
| 减少候选评分 `e+118` | `6128133` | `61.28133` |
| 增加候选数量 `e+E8` | `1500000` | `15` |
| 减少候选数量 `e+130` | `225000` | `2.25` |
| 两个候选方向字节 | 都为 `0` | 对应容量表负方向；进口/出口枚举名称仍不靠符号单独认定 |
| 初始化标志 | 当前 R12 为 `0` | 普通更新路径 |

本次读到的常量：维持门槛 `2500000`，增加门槛 `5000000`，替换倍率 `200000`，初始化倍率 `75000`，失败扣减比例 `20000`。这些值与本地配置的 `25/50/2/0.75/0.2` 对应。两个商品对象的有效性虚函数均指向 `+61A580`，该函数直接返回 true。

按当前暂停输入推演：`2 × 61.28133 = 122.56266 > 99.21745`，不足以替换；艺术品评分又不低于 25，不满足低评分移除条件；容量已满。因此**预测将走 `+11FD869`，把该条目的剩余预算由 11 清为 0，并返回 false**。这是尚未执行的静态分支预测，不是已经观察到的游戏运行结果，也不能据此认定九州其他商品或整轮更新都不再变化。

## 4. 直接上层：`+131C2B0`，UpdateStateTrades

[完整反汇编](../Output/goal3_static_20261002/function_7FF777E0C2B0.md)，1013 条可达指令。

`+131C2E3/+131C2EA` 引用源文件路径和 `UpdateStateTrades` 字符串。入口参数 `RCX` 指向一个包含 `+F0` 州对象数组的管理对象，而不是当前单个商品。

```text
// 功能：为多个州建立贸易调整条目，并进行多轮调整。
// 入参：州管理对象 manager；返回：未识别为有意义业务返回值，按过程描述。
function UpdateStateTrades(manager):
    seed = initializing ? 1 : MakeSeedFromContext()
    RunPreparationBatch(manager.states, seed)      // +13260F0，具体工作体未展开

    entries = []
    for state in manager.states:
        if ResolveRelated(state).fieldE8 <= 0: continue
        if ReadCountryModifier(state, selector0334) > 0: continue
        if ReadTradePotential(state) <= 0: continue
        entries.append(BuildEntry(state))          // +11FD230，条目步长 0x140

    SortByRemainingDescending(entries)
    // 小数组内联插入排序；大数组分治排序。不是“超过 32 个条目就不处理”。
    groupedTables = CreateTables()
    aggregateTables = CreateTables()
    do:
        RemoveEntriesWithNonPositiveBudget(entries)
        PrepareCandidatesForEntries(entries, groupedTables, aggregateTables, seed)
        // +1326280：可以分批/并行调度；串行工作体为 +131D540。
        anyAdjusted = false
        for e in entries:
            tables = groupedTables.lookupOrCreate(e.field0C)
            anyAdjusted |= TryAdjustStateTrade(e, tables, aggregateTables)
        RenderFrameIfNeeded()
    while anyAdjusted

    RunFinalizationBatch(manager.states)           // +1326430，具体写回范围待继续分析
    DestroyTemporaryTablesAndEntries()
```

证据与边界：

- `+131C6D0` 比较条目 `+04`，小数组排序把较大的剩余预算放在前面；大数组分支呈现排序分治和合并结构，其子函数没有全部展开。后面的淘汰会用末尾条目覆盖耗尽条目，不能保证每轮都仍严格有序。
- `+131CEE0` 剔除剩余预算非正的条目；`+131D170` 准备候选；`+131D219` 调用当前函数。
- `+131D21E` 将本次返回值并入 `anyAdjusted`；`+131D27F/+131D289` 控制下一轮。这是逐次调整机制的直接代码证据。
- `+131D1A0` 的哈希输入实际是 `entry+0x0C..0x0F`，不是条目前四字节，也不是硬木 ID。
- 分批大小使用“条目数 / 工作线程相关数量 / 3，至少为 1”。这个除以 3 是调度颗粒度线索，不能当成商品份额公式。
- `RenderFrameIfNeeded` 是长任务中的渲染/调度配合，不能仅凭这个字符串把整个函数归为 UI 数量计算。

## 5. 商品选择、评分和数量更新的辅助函数

这些不是新增的上层栈帧，而是为了理解上述两个核心函数补采的下游函数。

### 5.1 `+131D540`：准备一个州的增减候选

[反汇编](../Output/goal3_static_20261002/function_7FF777E0D540.md)。它根据 `entry+0C` 找共享表，建立上下文，再把两个选择函数返回的 `0x48` 字节结果分别放到 `entry+F8` 和 `entry+B0`。

```text
// 功能：计算一个条目的增加、减少候选。
// 入参：共享上下文 shared 和条目 e；返回：通过 e 写回两个候选，返回值不作业务解释。
function PrepareCandidates(shared, e):
    grouped = shared.lookup(e.field0C)
    context = BuildContext(e, grouped, shared.tables)
    state = Resolve(e.stateRef)
    randomState = MakeStateSeed(shared.seed, state.id)
    e.remove = SelectReductionCandidate(state, context, false, randomState) // +122AC50
    e.add = SelectIncreaseCandidate(state, context, randomState)           // +122B320
```

### 5.2 `+122AC50` / `+122B320`：选最低/最高评分的候选

[减少候选反汇编](../Output/goal3_static_20261002/function_7FF777D1AC50.md)，[增加候选反汇编](../Output/goal3_static_20261002/function_7FF777D1B320.md)。

```text
// 功能：从已有贸易中挑选适合减少的商品。
// 入参：州、上下文、是否绕过保护期、随机状态；返回：最低调整后评分候选或无效候选。
function SelectReductionCandidate(state, context, bypassProtection, rng):
    best = invalid
    for goods in state.list1DD8:
        signedUnits = ReadGoodsValue(state.table1D88, goods) / 100000
        if integer(signedUnits) == 0: continue
        if not bypassProtection and now < lastIncrease(goods) + 8 * 168:
            continue
        candidate = MakeCandidate(goods, direction = signedUnits > 0, mode = 0)
        Refresh(candidate, context)
        ApplySelectionRandomness(candidate, rng)
        best = LowerScoreWithRandomTieBreak(best, candidate)
    return best

// 功能：从允许交易的商品和两个方向中挑选适合增加的贸易。
// 入参：州、上下文、随机状态；返回：最高调整后评分候选或无效候选。
function SelectIncreaseCandidate(state, context, rng):
    best = invalid
    for direction in [0, 1]:
        for goods in GoodsDatabase:
            if not PassCountryAndMarketFilters(goods): continue
            if ExistingTradeHasOppositeDirection(state, goods, direction): continue
            candidate = MakeCandidate(goods, direction, mode = 1)
            Refresh(candidate, context)
            if not MeetsIncreaseThreshold(candidate): continue
            ApplySelectionRandomness(candidate, rng)
            best = HigherScoreWithRandomTieBreak(best, candidate)
    return best
```

减少侧 `+122AE1B` 将运行时值 8 乘以 `0xA8=168`，并与商品上次增加日期、当前游戏日期比较；结合配置，符合 8 周保护期。随机扰动常量在两侧均为 `50000`（0.5 定点），且存在明确的伪随机状态更新和同分选择。**扰动的精确分布和全部数值边界尚未还原，不能直接写成“加一个均匀随机数”。**

当前函数 `+11FD470` 随后再次 Refresh 候选，说明“选择时的扰动评分”和“执行调整时重新计算的评分”不是同一个阶段。

### 5.3 `+11FBDA0`：刷新候选数据；尾跳 `+11FC320` 计算评分

[反汇编及尾跳目标](../Output/goal3_static_20261002/function_7FF777CEBDA0.md)。该图沿直接尾跳继续收录了 `+11FC320`，所以文件中的 1015 条指令不全属于 `+11FBDA0` 自身。

```text
// 功能：刷新候选的单位数量、贸易优势和最终意愿评分。
// 入参：候选 c、共享计算上下文；返回：主要通过 c 原位写回，业务返回值待确认。
function Refresh(c, context):
    state = Resolve(c.stateRef)
    c.quantity = CalculateQuantityPerCapacity(state, c.goods) // +122AB50
    c.advantage = ReadOrComputeDirectionalTradeAdvantage(state, c.goods, c.direction)
    assert c.advantage > 0
    UpdateCandidatePartA(c, context)              // +11FBA60
    UpdateCandidatePartB(c, context)              // +11FC080
    tailcall CalculateDesirability(c, context)   // +11FC320，最终写 c+20
```

优势字段 `+40` 附近有明确断言字符串：`It should never be possible for calculated trade advantage to return zero or below`。评分尾函数读取关税、补助、反向贸易份额和短缺相关常量的线索明显；但目前没有把每个中间量与价格口径逐项绑定，**不在这里虚构完整利润公式**。`+11FBC80` 已确认只是比较候选 `+20` 与增加门槛，并在初始化模式下乘 0.75。

### 5.4 `+122AB50`：一次容量单位对应多少商品

[反汇编](../Output/goal3_static_20261002/function_7FF777D1AB50.md)，60 条指令。

```text
// 功能：计算某州某商品的单次交易数量。
// 入参：州 state、输出位置 out、商品 goods；返回：out，且写入定点数量。
function CalculateQuantityPerCapacity(state, out, goods):
    baseQuantity = goods.field50
    modifier = ReadModifier(state.field18B0 + 0x10, selector = 0x97)
    out.value = max(MINIMUM_GOODS_TRADED_QUANTITY,
                    MulFixed(baseQuantity, 1fp + modifier))
    return out
```

`+122AB64` 读取商品 `+50`，`+122AB88` 对修正值加 `100000`，`+122AC24..+122AC37` 执行最小值限制。本地配置的 `MINIMUM_GOODS_TRADED_QUANTITY=0.5` 与当前指令注释中的 `50000` 对应。

对当前软木：商品对象 `+50=1000000`，即基础量 10；候选单次量为 15。若使用该函数的正常路径，则相应数量修正为 +50%，这与指令公式一致。属性编号 `0x97` 的正式修正名称尚未确认。

对硬木：本地配置基础量为 5；**如果**它采用同一州修正 +50%，则单次量为 7.5，旧 UI 的 330 可由 44 个容量单位解释。这只是与历史数据相容的推算，尚未读取硬木当前对象和容量表项，不能认定本次现场已证明“硬木分配 44”。

### 5.5 商品账本、移除与容量缓存

| 函数 | 已看到的行为 | 解释 |
| --- | --- | --- |
| `+1027970` | 取 `goods+10` 为索引，`oldValue + delta` 后写回，维护有效位图 | 商品数值表加法，高可信 |
| `+1027A40` | 同样取商品索引，但执行 `oldValue - delta` | 商品数值表减法，高可信 |
| `+11FAF20` | 对容量表、方向表、市场/全局表调用减法 | 移除一次既有贸易，高可信 |
| `+122BED0` | 按商品键在 `state+1DF0` 查表并写入当前游戏日期 | 记录增加时间，与减少保护期相呼应 |
| `+122BF50` | 调用 `+1229C50` 写 `+1D58`，调用 `+122A470` 写 `+1D5C` | 重算两个容量缓存，已证实 |

```text
// 功能：增减指定商品的表项。
// 入参：商品表 table、商品 goods、定点增量 delta；返回：无业务返回值。
function AddByGoods(table, goods, delta):
    if delta == 0 or not ValidGoodsIndex(goods.id): return
    table[goods.id] = ReadOrZero(table, goods.id) + delta
    UpdatePresenceBitsAndStorage(table, goods.id)

// 功能：删除一个贸易容量单位及对应的数量贡献。
// 入参：商品、方向、单位数量、系数和五个数值表；返回：无业务返回值。
function RemoveOneTradeUnit(goods, direction, quantity, coefficient, tables):
    if not valid(goods): return
    SubtractByGoods(tables.capacity, goods, direction == 1 ? 1fp : -1fp)
    SubtractByGoods(tables.direction, goods, quantity)
    SubtractByGoods(tables.market, goods, quantity)
    SubtractByGoods(tables.global, goods, quantity)
    SubtractByGoods(tables.value, goods, MulFixed(quantity, coefficient))
```

一个值得保留的参数细节：`+11FD849` 调用移除函数时，数量来自减少候选 `e+130`，但 R9 系数按当前指令来自 `[RSI+40]`，即增加候选 `e+F0`。这里如实记录数据流，暂不擅自改写成减少候选自己的系数；究竟是共享上下文设计还是另有语义，需要继续分析。

## 6. 上方其余四级函数的伪代码和含义

### 6.1 `+7B81E0`：执行一个任务的上下文阶段

[反汇编](../Output/goal3_static_20261002/function_7FF7772A81E0.md)，279 条指令。引用 `gamestatetick.cpp:1246`、`:1278`、`Prepare`、`Context %d`。主要是回调、区间和上下文管理，未见商品评分公式。

```text
// 功能：准备并执行一个 Tick 任务的多阶段回调。
// 入参：游戏状态 gameState、任务 task；返回：未识别业务返回值。
function ExecuteTickTask(gameState, task):
    context = EmptyContext(gameState)
    WithHiddenLogicAccess(task.Prepare(context))  // 虚表 +30
    while context.rangeCallback or context.singleCallback:
        nextContext = EmptyContext(gameState)
        WithHiddenLogicAccess:
            if context.rangeCallback:
                ExecuteByFlags(context.range, context.flags, nextContext)
                // 分段或整段调用虚表 +10，必要时让出时间片。
            if context.singleCallback:
                context.singleCallback.Invoke(nextContext) // 本次命中 +7B8560
        context = MoveAndCleanup(nextContext)
```

中间两个尾跳转的伪代码：

```text
// 功能：将通用回调转交给其持有对象。
// 入参：回调 callback、上下文 context；返回：尾跳到被调函数。
function CallbackAdapter_7C49D0(callback, context):
    owner = callback.field08
    tailcall owner.vfunc38(context)

// 功能：从任务上下文取得州管理器。
// 入参：任务对象、上下文 context；返回：尾跳到州贸易更新函数。
function StateTradeTaskAdapter_1319B40(task, context):
    root = context.field08
    manager = root.field120 + 0x1C00
    tailcall UpdateStateTrades(manager)
```

### 6.2 `+7BE1B0`：执行一个 Tick 的任务列表

[反汇编](../Output/goal3_static_20261002/function_7FF7772AE1B0.md)，730 条指令。包含 `Tick Tasks for {}`、任务耗时统计及 `gamestatetick.cpp` 字符串。

```text
// 功能：构造并依次执行本次 Tick 的任务列表。
// 入参：游戏状态、游戏时间；返回：业务返回值未确认。
function ExecuteTickTaskList(gameState, date):
    CheckLogicAccess()
    UpdateDateDependentState(gameState, date)
    tasks = BuildTaskList(gameState, date)          // +7B6ED0 等
    PrepareTimingAndDiagnostics()
    for task in tasks:
        StartTaskTimer()
        ExecuteTickTask(gameState, task)           // +7BE768
        CollectTaskTimingAndOptionalDiagnostics()
    RenderFrameIfNeeded()
    FinalizeTickTasksAndCleanup()
```

它说明贸易更新是某个任务，但任务如何按天/周排期仍在列表构造和任务注册侧，本轮没有证明。

### 6.3 `+7D6400`：推进游戏时间并处理一次 Tick

[反汇编](../Output/goal3_static_20261002/function_7FF7772C6400.md)，140 条指令。包含 `Processing Tick:`，并在 `+7D64A0` 将 `gameState+08` 的 32 位时间值增加 6。

```text
// 功能：推进并处理一个模拟 Tick。
// 入参：游戏状态，另有一个本轮主路径未见实质使用的整型参数；返回：未确认。
function ProcessOneTick(gameState, extra):
    IncrementGlobalTickCounter()
    oldFlag = gameState.flag14E
    gameState.flag14E = true
    RunCalendarBoundaryHooksIfNeeded(gameState.date)
    gameState.date.raw += 6
    NormalizeAndDescribeDate(gameState.date)
    ExecuteTickTaskList(gameState, gameState.date)  // +7D65A3
    RunOptionalPostTickObservers()
    gameState.flag14E = oldFlag
```

数字 6 是明确事实；结合上层按 24 求余、保护期按 168 计算，时间单位很像小时，但这里不把日期类型的完整编码当作已知。

### 6.4 `+137C990`：外围 Tick 与后续事件包装

[反汇编](../Output/goal3_static_20261002/function_7FF777E6C990.md)，251 条指令。

```text
// 功能：从全局状态取得模拟对象，处理 Tick 并执行后续事件调度。
// 入参：未见主路径依赖入口实参；返回：未确认业务返回值。
function TickAndPostProcess():
    CheckLogicAccess()
    gameState = GlobalState.field608
    ProcessOneTick(gameState)                      // +137C9E2
    SaveAndTemporarilyResetThreadLocalCounter()
    if RelevantGlobalFlagsAllow():
        if NormalizedTimeModulo24(gameState.date) == 0:
            QueueOrExecuteEventFamilyA()
        ProcessClockAndOtherPostTickConditions()
        if AdditionalCondition(gameState):
            QueueOrExecuteEventFamilyB()
    RestoreThreadLocalCounter()
    NotifyOptionalObserver()
```

后续事件对象的正式类型没有恢复，不能把它们猜成某一种经济结算。就本任务而言，继续向这些外围层深挖的收益低于分析贸易候选评分和容量数量表。

## 7. 对最终目标的解释与尚未闭合部分

现有证据支持的模型是：

```text
州获得本轮操作预算
→ 选择可减少的低评分贸易、可增加的高评分贸易
→ 容量满时检查替换倍率；容量未满时检查增加门槛
→ 按商品增减一个带方向的容量单位和相应商品数量
→ 更新容量缓存、保护期记录和汇总表
→ 多州多轮重复，直到本轮没有成功调整
```

这能解释为什么不是简单按利润比例一次性分摊全部容量，也能解释为什么硬木数值的 UI 临时地址不是最好的入口。持久的商品容量表已经有具体结构线索：`state+1D88` 的值数组位于 `state+1D90`，按商品 ID 索引，并由 `state+1DA8` 附近位图标记存在性。

尚未完成的部分明确保留：

- `+11FC320` 最终意愿评分的逐项数学公式，特别是补助、价格、短缺及优势如何组合。
- 两个方向枚举的正式进口/出口名称，以及不同汇总表的精确市场归属。
- 随机扰动的完整表达式、所有溢出和舍入边界。
- 当前硬木商品对象、容量表项和数量修正的实际值；软木样本不能代替硬木证据。
- 每周任务注册条件、准备/收尾批处理工作体、初始预算 `+12295A0` 的完整算法。
- 旧 UI 中硬木 330 的完整形成过程。单个暂停现场无法恢复之前多轮选择的历史。

若下一轮仍只做静态分析，优先顺序建议为：**细化 `+11FC320` → 读取硬木当前容量表项和 `+122AB50` 输入 → 展开 `+12295A0` 与贸易任务注册处**。不需要先恢复游戏运行。

## 8. 原始证据与复核方式

- [开始断点快照](../Output/goal3_static_20261002/before/streg_7FF777CED5C9.md)。
- [结束现场核对](../Output/goal3_static_20261002/final_verification.json)：仍为 stopped，全部返回寄存器、目标进程信息及 CE 资源计数与开始快照一致。这是首尾一致性检查，不是对两次查询之间所有外部操作的监控。
- [模块信息](../Output/goal3_static_20261002/module.json)、[栈原始字节](../Output/goal3_static_20261002/stack.json)、[展开链](../Output/goal3_static_20261002/unwind_frames.json)。
- [条目原始字节](../Output/goal3_static_20261002/entry.json)、[州容量附近原始字节](../Output/goal3_static_20261002/center.json)、[商品与常量](../Output/goal3_static_20261002/fields.json)、[回调目标核对](../Output/goal3_static_20261002/callback.json)。
- [opcode 导出目录](../Output/goal3_static_20261002/opcodes)：使用现有脚本采集各层入口/返回点窗口。
- 每个 `function_ADDRESS.md` 有对应 JSON，保存基本块、调用点和指令。控制流图未因指令数量上限截断，但不自动进入普通被调函数，也不能证明间接跳转的所有目标；会跟随窗口内直接尾跳，所以部分文件包含后续函数。
- [只读控制流采集辅助脚本](../Output/goal3_static_20261002/collect_graphs.py)仅放在本次证据目录，调用实际插件的只读接口；没有修改项目已有采集脚本。

本次一个 16384 字节栈读取越过可读范围而失败，随后改为 8192 字节；一个前后各 1000 条的 opcode 请求因总数超过插件 1024 条上限被拒绝，随后以各 500 条窗口及控制流图补齐。失败输出保留，不当作有效指令证据。

opcode 采集示例（地址仅适用于本次进程）：

```powershell
# 功能：只读导出当前函数和直接上层的指令窗口；无函数入参与返回值。
python Scripts\run_opcode_export.py 7FF777CED5C9 500 --output Output\goal3_static_20261002\opcodes
python Scripts\run_opcode_export.py 7FF777E0C2B0 500 --output Output\goal3_static_20261002\opcodes
python Scripts\run_opcode_export.py 7FF777E0D21E 500 --output Output\goal3_static_20261002\opcodes
```
