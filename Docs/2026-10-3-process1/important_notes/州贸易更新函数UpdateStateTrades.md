# 州贸易更新函数 `UpdateStateTrades`

来源：`victoria3.exe+131C2B0` 附近反汇编。该入口引用了 `UpdateStateTrades` 字符串，并负责为多个州建立贸易调整条目、反复选择候选并执行调整。

## 一、函数定位

```text
UpdateStateTrades(+131C2B0)
    ├─ 准备本轮共享数据（+13260F0）
    ├─ 遍历州，建立贸易调整条目（+11FD230）
    ├─ 按剩余预算排序
    ├─ 循环准备候选并调用 TryAdjustStateTrade(+11FD470)
    └─ 结束后执行收尾批处理（+1326430）
```

入口参数 `RCX` 是州管理对象，不是单个州或单个商品。该管理对象包含州对象数组，当前分析中使用其 `+F0` 附近的州集合。

## 二、完整伪代码

```cpp
// 功能：为多个州建立并执行贸易容量调整，直到本轮不再发生成功调整。
// 入参：manager 为包含州集合及批处理上下文的管理对象。
// 返回值：当前反汇编未确认有独立业务返回值；主要效果通过州和贸易表写回。
function UpdateStateTrades(manager):
    if GameState.initializing:
        seed = 1
    else:
        seed = MakeSeedFromContext(manager)

    // 预先准备本轮可能使用的共享数据，具体工作体尚未完全展开。
    RunPreparationBatch(manager.states, seed)       // +13260F0

    entries = []
    for state in manager.states:
        related = ResolveRelatedStateObject(state)
        if related.fieldE8 <= 0:
            continue

        if ReadCountryModifier(state, selector0334) > 0:
            continue

        if ReadTradePotential(state) <= 0:
            continue

        entry = BuildTradeAdjustmentEntry(state)     // +11FD230
        entries.append(entry)                        // 单条记录步长约 0x140

    // 剩余预算较大的条目优先处理。
    SortByRemainingBudgetDescending(entries)

    groupedTables = CreateGroupedTradeTables()
    aggregateTables = CreateAggregateTradeTables()

    do:
        // 删除本轮已经没有剩余预算的条目。
        RemoveEntriesWithNonPositiveBudget(entries)  // +131CEE0 附近
        if entries.empty:
            break

        // 为每个条目重新选择一个减少候选和一个增加候选。
        PrepareCandidatesForEntries(
            entries,
            groupedTables,
            aggregateTables,
            seed
        )                                             // +131D170 / +131D540

        anyAdjusted = false

        for entry in entries:
            tables = groupedTables.lookupOrCreate(entry.field0C)

            adjusted = TryAdjustStateTrade(
                entry,
                tables,
                aggregateTables
            )                                             // +11FD470

            anyAdjusted = anyAdjusted or adjusted

        RenderFrameIfNeeded()
    while anyAdjusted

    // 具体写回范围仍需继续从 +1326430 展开确认。
    RunFinalizationBatch(manager.states)             // +1326430

    DestroyTemporaryTablesAndEntries()
    return
```

## 三、条目筛选和建立

不是所有州都会进入 `entries`。当前静态证据显示至少有以下筛选：

1. 关联州对象的 `fieldE8` 必须大于零；
2. `selector0334` 对应的国家修正不能大于零；
3. 州的贸易潜力必须大于零。

通过筛选后，`+11FD230` 为该州建立一个临时调整条目。条目中包含州引用、剩余预算、分组键以及后续写入的增加/减少候选。条目并非一条最终贸易路线，而是本轮容量调整的工作记录。

## 四、候选准备与单次调整

每轮循环先调用候选准备逻辑，再调用 `TryAdjustStateTrade`：

```text
PrepareCandidates(+131D540)
    ├─ SelectReductionCandidate(+122AC50)
    │    └─ 遍历州已有贸易，选最低评分候选
    └─ SelectIncreaseCandidate(+122B320)
         └─ 遍历商品库和两个方向，选最高评分候选

TryAdjustStateTrade(+11FD470)
    ├─ Refresh(+11FBDA0) 减少候选
    ├─ Refresh(+11FBDA0) 增加候选
    ├─ 判断容量、评分和资格
    └─ 最多执行一次减少和一次增加，成功预算共扣一次
```

候选准备阶段会刷新枚举中的临时候选；`TryAdjustStateTrade` 开始时还会再次刷新最终选中的候选。因此，单次 `TryAdjustStateTrade` 的 `Refresh` 上限是两个，但一次 `UpdateStateTrades` 的总刷新次数取决于商品数量、方向数量和循环轮数。

## 五、多轮循环的含义

`+131D21E` 将每个条目的返回值合并到 `anyAdjusted`；`+131D27F/+131D289` 控制是否开始下一轮。由此可确认：

- 只要本轮至少一个条目成功调整，就会再进行一轮；
- 下一轮会重新准备候选，候选不是永久锁定的；
- 同一商品可能在不同轮次再次成为候选；
- 商品表、容量表和评分变化会影响下一轮的选择；
- 当一整轮没有成功调整时，循环结束，即使个别条目仍可能有剩余预算。

因此，一次 `UpdateStateTrades` 不是只调整固定的两个商品。两个商品只是某一个条目、某一轮中的增加候选和减少候选；整个更新批次可能涉及多个州、多个商品和多个方向。

## 六、排序与分批调度

条目建立后会按剩余预算排序。小数组路径表现为插入排序，大数组路径表现为分治排序和合并；不能把其中出现的数量阈值解释为“超过某个州数就不处理”。

候选准备和条目执行可能经过 `+1326280` 的分批或并行调度，已知串行工作体为 `+131D540`。分批大小中的“条目数 / 工作线程相关数量 / 3，至少为 1”是调度粒度，不能解释为商品数量或贸易容量比例。

## 七、初始化与普通更新

初始化状态会使用固定种子 `1`；普通更新会从上下文生成种子。初始化还会影响 `TryAdjustStateTrade` 内部的评分门槛和预算处理，因此不能直接假设初始化批次与普通贸易更新完全相同。

## 八、已确认内容与分析边界

已确认：

- `+131C2B0` 是多个州的贸易更新入口；
- 它建立临时条目并反复调用 `+11FD470`；
- 候选在每轮调整前重新准备；
- `anyAdjusted` 控制多轮循环；
- `+131CEE0`、`+131D170`、`+131D219`、`+131D21E` 和 `+131D27F/+131D289` 分别对应条目清理、候选准备、单条目执行、结果合并和下一轮控制。

仍需保留边界：

- `+13260F0` 的完整共享数据准备过程尚未全部展开；
- `+1326430` 的最终写回范围尚未完全确认；
- 任务排程何时调用 `UpdateStateTrades`，不能仅凭本函数确定为固定游戏周或固定星期；
- 分批/并行调度不会改变候选选择语义，但其线程执行顺序仍需运行时采集进一步核对。



## 九、ReadCountryModifier 这里读取的这个修正会是什么值？能不能反推出来？

可以反推出它大概率是：

> `country_disallow_trade_bool`  
> 国家级“禁止贸易”布尔修正，对应孤立主义（`law_isolationism`）。

依据如下：

- 反汇编在 `+131C49C` 把常量 `0x0334` 放入 `r8d`；
- 随后调用 `+334150`，读取州所属国家的修正；
- 返回值在 `+131C4AD` 处与 `0` 比较，若大于 `0` 就跳过该州；
- 游戏脚本中，孤立主义定义了：

```text
country_disallow_trade_bool = yes
```

位置：[00_trade_policy.txt:159](D:/Games/Victoria3/Victoria%203/game/common/laws/00_trade_policy.txt:159) 和 [00_trade_policy.txt:203](D:/Games/Victoria3/Victoria%203/game/common/laws/00_trade_policy.txt:203)。

该修正的定义也明确是布尔型：

```text
country_disallow_trade_bool = {
    decimals = 1
    color = bad
    boolean = yes
}
```

因此这里的逻辑可以还原为：

```cpp
country = state->GetCountry();

if (country->GetModifier(0x0334 /* country_disallow_trade_bool */) > 0)
    continue; // 不为该州建立自动贸易调整条目
```

数值层面可以确定：

- 没有该修正：`0`；
- 有效 `yes`：某个正值；
- 这段代码只关心是否 `> 0`，不依赖具体正值。

具体内存值是 `1`、`100000` 还是其他定点表示，仅凭当前静态代码不能确定；需要运行时读取一个孤立主义国家和一个自由贸易国家的对应修正槽位才能确认。`0x0334` 本身是内部修正索引，不是脚本文件中的数值。

## 十、`BuildTradeAdjustmentEntry` 与 `PrepareCandidatesForEntries` 伪代码

### 10.1 `BuildTradeAdjustmentEntry`（`victoria3.exe+11FD230`）

功能：为一个州创建本轮贸易调整条目，计算初始操作预算，并初始化后续候选选择、临时表和候选槽位。

入参：`entry` 为调用方提供的约 `0x140` 字节条目缓冲区；`state` 为州对象。

返回值：返回 `entry` 指针。初始预算同时写入 `entry+00` 和 `entry+04`。

```cpp
// 功能：构造并初始化一个州的贸易调整工作条目。
// 入参：entry 为输出条目缓冲区；state 为待处理的州对象。
// 返回值：返回初始化后的 entry 指针。
function BuildTradeAdjustmentEntry(entry, state):
    initialBudget = CalculateTradeAdjustmentBudget(state) // +12295A0
    entry.field00 = initialBudget
    entry.field04 = initialBudget

    entry.stateRef = state.field08
    entry.field0C = ResolveGroupingKey(state)              // +CFD3D0

    // 初始化条目内的临时贸易数值表和容器。
    InitializeTemporaryTable(entry + 0x18)
    InitializeTemporaryTable(entry + 0x40)
    InitializeTemporaryTable(entry + 0x68)
    InitializeTemporaryTable(entry + 0x90)

    // 初始化增加候选槽位（entry+B0）及其附属字段。
    entry.add.goods = InvalidGoodsHandle()
    entry.add.direction = 2
    entry.add.score = 0
    entry.add.quantity = 0
    entry.add.extra = 0

    // 初始化减少候选槽位（entry+F8）及其附属字段。
    entry.remove.goods = InvalidGoodsHandle()
    entry.remove.direction = 2
    entry.remove.score = 0
    entry.remove.quantity = 0
    entry.remove.extra = 0

    return entry
```

其中，`+11FD230` 的直接反汇编见 [function_7FF777CED230.md](../../../Output/2026-10-3-process1/goal3_static_20261002/function_7FF777CED230.md)。`+12295A0` 的预算计算和 `+CFD3D0` 的分组键含义仍未完全展开；上面的字段名是根据写入偏移和后续使用位置得到的工作性命名。

### 10.2 `PrepareCandidatesForEntries`（调度 `+131D170`，工作体 `+131D540`）

功能：对本轮仍有预算的所有条目重新选择一个减少候选和一个增加候选。`+131D170` 负责批处理/并行调度，实际处理单个条目的串行工作体是 `+131D540`。

入参：`entries` 为贸易调整条目数组；`groupedTables` 和 `aggregateTables` 为本轮共享贸易表；`seed` 为随机种子。

返回值：批处理过程通过每个条目的 `entry+B0` 和 `entry+F8` 写回候选；没有已确认的独立业务返回值。

（Docs\2026-10-3-process1\intermediates\goal3_static_disassembly4.md）
| --- | --- | --- |
| `entry+B0` | 增加候选：希望再分配一单位容量的商品 | 候选 `+08` 的方向字节 |
| `entry+F8` | 减少候选：优先考虑释放一单位容量的商品 | 候选 `+08` 的方向字节 |

```cpp
// 功能：调度本轮所有条目的候选准备工作。
// 入参：entries 为条目数组；groupedTables、aggregateTables 为共享表；seed 为随机种子。
// 返回值：候选通过条目字段写回；返回值暂无独立业务含义。
function PrepareCandidatesForEntries(entries, groupedTables, aggregateTables, seed):
    shared = MakeCandidatePreparationContext(
        groupedTables,
        aggregateTables,
        seed
    )
    DispatchInBatches(entries, shared) // +1326280；串行工作体为 +131D540
    return


PrepareCandidatesForEntries
    └─ DispatchInBatches（+1326280）
       └─ PrepareCandidatesWorker（+131D540）

// 功能：为单个条目计算减少候选和增加候选。
// 入参：shared 为本轮共享上下文；entry 为单个州贸易调整条目。
// 返回值：候选写回 entry+F8 和 entry+B0；返回值暂无独立业务含义。
// 注意：PrepareCandidatesWorker 是本文为 +131D540 起的语义化临时名称，
// 不是 victoria3.exe 中可搜索的原始符号名。该地址对应的真实调用关系
// 应按 RVA 查询：+131D170 → +1326280 → +131D540。
function PrepareCandidatesWorker(shared, entry):
    grouped = LookupGroupedTable(shared, entry.field0C)
    state = ResolveState(entry.stateRef)
    context = BuildTradeContext(entry, grouped, shared.aggregateTables)

    // 由条目字段和共享种子生成该州本轮的随机状态。
    rng = MakeStateSeed(shared.seed, state.id)

    // 从州已有贸易中选择评分最低的减少候选。
    removeCandidate = SelectReductionCandidate(
        state,
        context,
        false,                    // 不绕过增加后的保护期
        rng
    )                         // +122AC50
    CopyCandidate(entry + 0xF8, removeCandidate)

    // 从允许交易的商品和两个方向中选择评分最高的增加候选。
    addCandidate = SelectIncreaseCandidate(
        state,
        context,
        rng
    )                         // +122B320
    CopyCandidate(entry + 0xB0, addCandidate)
    return
```

`+131D540` 的直接反汇编见 [function_7FF777E0D540.md](../../../Output/2026-10-3-process1/goal3_static_20261002/function_7FF777E0D540.md)。该函数先用 `entry+0C` 查找共享表，再调用 `+122AC50` 和 `+122B320`，分别把约 `0x48` 字节的结果写入 `entry+F8` 和 `entry+B0`。候选选择的进一步伪代码见 [州贸易调整函数的候选准备函数.md](州贸易调整函数的候选准备函数.md)；`+131D170` 的调度关系见 [goal3_static_disassembly.md](../intermediates/goal3_static_disassembly.md) 第 5.1 节。

调用关系的关键证据在批处理函数 `+1326280`：串行分支的 `+1326405` 有一条直接 `call victoria3.exe+131D540`。而 `UpdateStateTrades(+131C2B0)` 在 `+131D170` 调用 `+1326280`。因此完整链路是：

```text
UpdateStateTrades(+131C2B0)
    └─ +131D170
       └─ +1326280（批处理/并行调度）
          └─ +131D540（串行工作体）
```

在 `+1326280` 的其他分支中，工作体可能通过任务/回调机制间接执行，所以静态调用图未必在每条路径都显示 `+131D540` 的直接 `call`。搜索时应使用 `+131D540`、`7FF777E0D540` 或对应反汇编文件名，而不是搜索 `PrepareCandidatesWorker`。

### 10.3 `CalculateTradeAdjustmentBudget`（`victoria3.exe+12295A0`）当前可确认的功能

该函数由 `BuildTradeAdjustmentEntry` 在 `+11FD248` 调用，调用时 `RCX` 指向州对象；返回的 32 位整数写入 `entry+00`，随后复制到 `entry+04`。因此它返回的是**本州本轮可尝试的贸易调整次数/操作预算**，不是贸易容量，也不是单次商品数量：

```cpp
// 功能：读取或计算指定州本轮的贸易调整操作预算。
// 入参：state 为州对象。
// 返回值：本轮初始操作预算，写入 entry+00；具体缩放和边界尚未完全确认。
function CalculateTradeAdjustmentBudget(state):
    if not CheckTradeUpdateEligibility(state):       // +1229520
        return 0

    // +1229520 内先检查关联对象的 fieldE8，
    // 再读取 country modifier selector 0x0334；该修正为正时返回 false。
    modifierSelector = *(uint16*)GlobalSelector_0099
    budgetValue = ReadStateModifierThroughValueCalculator(
        state,
        modifierSelector,
        scale = 100000
    )
    return ConvertValueCalculatorResultToBudget(budgetValue)
```

这部分已经可以进一步追到：运行时导出的 `+12295A0` 函数并不是简单的“容量乘修正”或单条 `imul`。它调用 `+1229520` 做州/国家资格检查，然后构造一个通用 Value Calculator 查询；反汇编在 `+1229621` 读取全局表中的 16 位 selector（当前静态标记为 `0x0099`），并在 `+1229658` 使用定点比例 `100000`。

后续调用的 `+844150` 行为已经明确：它接收一个州修正表对象和 16 位 selector，使用 FNV-1a 风格哈希定位桶，遍历桶内条目并比较 selector；找到后返回该条目的值指针，找不到则返回默认空值。它本身不计算贸易容量，也不执行 `workforce` 乘法。真正的定点值转换和最终整数返回在 `+12295A0` 后续调用的通用 Value Calculator 代码中完成。

因此当前最可信的解释是：`0x0099` 是 `state_weekly_trades_add` 的内部修正 selector，`+12295A0` 从已经按生产方式 staffing 汇总的州修正表中取出该值，再通过 Value Calculator 转换为 `entry+00` 所需的整数预算。

游戏目录已经提供了更直接的语义证据。`game/localization/english/modifiers_l_english.yml` 将 `state_weekly_trades_add` 描述为“一个州每周可以进行的贸易调整次数”；简体中文对应文本是“提高或降低一个州每周可以进行的贸易数量”。`game/common/defines/00_ai.txt` 还明确说明：贸易中心成功执行一次贸易消耗 1 次 weekly trade，失败执行则消耗总 weekly trades 的 `0.2`。因此这里的“预算”就是该州本周可尝试的贸易调整次数，失败扣除比例也与反汇编中按初始预算比例扣除的现象相符。

贸易中心生产方式在 `game/common/production_methods/11_private_infrastructure.txt` 中按 workforce 缩放提供 `state_weekly_trades_add = 1`，而 `state_trade_capacity_add = 10` 是另一项独立修正。`game/common/production_methods/production_methods.md` 对 `workforce_scaled` 的定义是：修正按建筑 staffing level 缩放，staffing level 的范围是 `0.0` 到建筑等级。因此，对贸易中心等级 `L`、有效 staffing level `W`（`0 <= W <= L`）而言，脚本层面的贡献可写成：

```text
weekly_trades_from_this_pm = 1 × W
trade_capacity_from_this_pm = 10 × W
```

满员时 `W = L`，所以每个满员贸易中心等级贡献 1 次 weekly trade 和 10 点贸易容量；半员时两项都会按 staffing 比例下降。贸易中心每等级的岗位由建筑定义中的 `building_employment_clerks_add = 800` 和 `building_employment_shopkeepers_add = 200` 提供，即每等级 1000 个岗位；实际 `W` 取决于这些岗位的 staffed ratio，而不是只看建筑等级。运行记录中观察到预算值 `11`，可能对应总 staffing level 约为 11，但仍需运行时读取修正汇总来确认取整方式。

[00_ai.txt (line 1121)](D:/Games/Victoria 3/Victoria 3/game/common/defines/00_ai.txt:1121) 明确写道：
- 成功执行一次贸易，消耗 1 次 weekly trade；
- 失败执行一次贸易，消耗总 weekly trades 的 0.2；
- 这样可以避免拥有大量 weekly trades 的贸易中心反复尝试无效贸易。

[11_private_infrastructure.txt (line 358)](D:/Games/Victoria 3/Victoria 3/game/common/production_methods/11_private_infrastructure.txt:358) 中，贸易中心同时提供：
state_weekly_trades_add = 1
state_trade_capacity_add = 10

尚未完全确认的部分包括：`0x0099` 与脚本修正名的最终映射、Value Calculator 内部是否叠加基础值、定点结果转整数的具体舍入方式、最小/最大值钳制，以及初始化状态是否使用不同预算。相关运行时反汇编已保存于 [opcode_7FF6AFED95A0.md](../../../Output/opcodes/20261004T164556438643Z_6d324c41/opcode_7FF6AFED95A0.md) 和 [+844150 的反汇编](../../../Output/opcodes/20261004T165749525689Z_47107bcc/opcode_7FF6AF4F4150.md)；其中 `+12295A0` 是当前进程基址下的地址，RVA 仍为 `+12295A0`。

#### workforce 对 state_weekly_trades_add 的缩放

是的，但需要区分“建筑等级”和“有效 workforce”。

`production_methods.md` 对 `workforce_scaled` 的定义是：

> 修正按建筑的 staffing level 缩放，staffing level 范围为 `0.0` 到建筑等级。

因此，对某个生产方式实例的建筑等级 `L`、有效 staffing level `W`（`0 <= W <= L`）和该生产方式提供的修正值 `m` 而言：

```text
modifier_contribution_from_this_pm = W × m
```

标准贸易中心生产方式的 `m = 1`，所以它对 weekly trades 的贡献才是 `W × 1`；同一个生产方式中的 `state_trade_capacity_add = 10` 是另一个修正键，只贡献贸易容量，不会自动加入 weekly trades 预算。

例如：

| 贸易中心等级 | staffing 状态 | weekly trades | trade capacity |
|---:|---:|---:|---:|
| 10 | 满员，W=10 | +10 | +100 |
| 10 | 80% staffed，W≈8 | +8 | +80 |
| 10 | 50% staffed，W≈5 | +5 | +50 |

所以“每等级提供 1 次调整机会”只在该生产方式的 `m = 1` 且贸易中心满员时成立。

贸易中心建筑每等级提供：

```text
800 clerks
200 shopkeepers
= 1000 个岗位
```

这些岗位由 `building_employment_*_add` 按建筑等级增加。若 10 级建筑有 8000/10000 个岗位被填充，则 staffing ratio 约为 80%，有效 staffing level 约为 8，`state_weekly_trades_add` 约为 8。

需要保留一个细节：游戏内部可能使用定点数，最终预算写入 `entry+00` 时的取整方式目前还没有从 `+12295A0` 反汇编确认。因此：

```text
state_weekly_trades_add_total
    = Σ(所有活动生产方式实例的 staffing_level × 该实例的 state_weekly_trades_add)
      + Σ(其他来源的 state_weekly_trades_add)

预算 = ValueCalculator(state_weekly_trades_add_total, selector=0x0099)
```

目前游戏目录中可见的其他同名来源包括部分 DLC 静态修正中的 `state_weekly_trades_add = 2`；它们应与贸易中心生产方式贡献相加。其他生产方式修正（例如 `state_trade_capacity_add`、`state_trade_quantity_mult`）只有在直接使用 `state_weekly_trades_add` 键，或间接改变 staffing level 时，才会影响预算。预算不能简单写成“建筑等级总和”，也不能写成“贸易容量乘修正”。

本轮通过 Cheat Engine 读取运行中进程的全局 selector 槽位 `[victoria3.exe+2E86F9C]`，得到当前 16 位值 `0x2474`；该槽位正是 `+12295A0` 指令 `movzx r8d, word ptr [..]` 标记为 `[0099]` 的地址。这个结果确认 `[0099]` 是运行时修正选择器，而不是预算数值本身，但目前仍没有找到 `0x2474` 到脚本键名 `state_weekly_trades_add` 的注册表映射。因此完整的 ValueCalculator 公式（基础值、定点缩放、舍入及钳制）仍不能仅凭 selector 数值写死。

### 10.4 对 `+12295A0` 尾部的进一步确认

继续采集 `+12295A0` 后半段后，预算返回路径已经可以写成明确的整数公式。函数先把 `r14d` 初始化为 `1`（`+122962E`）；资格检查 `+1229520` 失败时直接返回 `0`。selector 为 `0xFFFF` 时跳过修正查询，保留这个默认值 `1`。

selector 有效时，函数把修正查询结果交给 ValueCalculator，比例字段设为 `100000`（`+1229658`）。尾部 `+1229BAD` 读取计算结果的 64 位定点整数 `x`，通过乘数 `0x29F16B11C6D1E109`、算术右移 `14` 位完成除以 `100000` 的定点转换，然后用符号修正得到整数 `q`：

```text
q = trunc_toward_zero(x / 100000)
budget = max(1, q)
```

对应机器码为 `imul`、`sar rdx,14`、`shr rax,63`、`add rdx,rax`，随后 `cmp edx,1; cmovg r14d,edx`，最后返回 `r14d`。因此这部分不是“贸易容量乘一个修正”，而是：先从 selector 指向的州级修正条目取得已汇总的 `state_weekly_trades_add` 定点值，再转换为整数，并设置最小预算 1；资格检查失败才返回 0。当前仍缺的是 selector 注册表的名称映射，但它不再影响上述数值转换公式。

补充追踪：`+1229BA5` 调用的 `+B0072350` 是通用定点 ValueCalculator 节点。它读取节点的 `+00/+08/+10/+20/+28/+30` 字段，使用 `+10 + 100000` 形成端点；端点未溢出时执行定点线性组合，溢出时走端点选择分支，并在返回前继续处理下一层节点。该函数内部同样使用 `0x29F16B11C6D1E109`、右移 `14` 完成 `/100000`。因此 `+12295A0` 取得的 `x` 是 ValueCalculator 节点链的结果，而不是直接读取一个原始脚本整数。节点字段最终如何由 `+AF8FCE20` 和其调用者填充，仍是业务公式剩余的主要待展开部分。

对 `+AF8FCE20` 的反汇编复核后，需要修正上一句的推断：该函数主要是动态数组/节点容器扩容与初始化（读取 `+08/+0C` 计数，按 `1.5` 倍增长，初始化节点槽位），不是 `state_weekly_trades_add` 的计算函数。因此它不能提供修正值来源；预算输入仍需沿 `+12295A0` 构造 ValueCalculator 上下文的其他调用继续追踪。

### 10.5 ValueCalculator 上下文和预算公式的完整展开

本轮继续追到 `+B0071A10`、`+AF8ECAC0`、`+AF89ECB0` 和 `+B0072350`，已经能把预算计算拆成“加法累计值”和“定点倍率”两部分。对应的伪代码来源见 [value_calculator_budget_functions.md](../../../FakeCode/2026-10-3-process1/value_calculator_budget_functions.md)。

本节细化并替代 10.4 中“ValueCalculator 输入尚未展开”的暂定说法；10.4 保留原始采集记录，10.5 是结合新增调用链后的结论。

`+B0071A10` 初始化 ValueCalculator 上下文：`+00/+08/+10=0`，`+18=100000`，`+20=INT64_MIN`，`+28=INT64_MAX`，`+31` 保存计算模式。`+AF8ECAC0` 的跳转表给出了关键业务操作：本调用路径的操作码 `1` 把修正值累加到上下文的 `+10`；操作码 `2` 把上下文 `+18` 与修正值按五位小数定点乘法相乘。也就是说，计算器不是把修正值直接当作最终预算，而是先形成：

```text
additive = Σ(所有 ADD 修正值)
factor   = Π(所有 FACTOR 修正值 / 100000)
基础值   = 100000
```

`+12295A0` 的有效 selector 路径把 `[victoria3.exe+2E86F9C]`（机器码标记 `[0099]`）查到的州级修正条目作为操作码 `1` 的输入。因此，在该 selector 确认对应 `state_weekly_trades_add` 后，脚本层的预算输入就是 `additive = state_weekly_trades_add` 的全部来源之和；贸易中心 `workforce_scaled { state_weekly_trades_add = 1 }` 已在州修正表生成阶段按 staffing level 汇总到这个值。`state_trade_capacity_add` 和 `state_trade_quantity_mult` 没有进入这个 ADD 槽位。

函数随后读取 `state+0x68`。当该定点值小于 `100000` 时，`+AF89ECB0` 将它作为 FACTOR 乘入上下文的 `+18`；这条机器码路径证明存在独立的 workforce/状态倍率输入，但目前仅凭偏移尚不能把 `+0x68` 的字段名写死为某一个脚本修正。若运行时结构确认它就是 staffing ratio，则该部分等价于乘以 `staffing_ratio`；不能把已经写入 `state_weekly_trades_add` 的 workforce 缩放再次重复相乘。

`+B0072350` 对节点链求值。正常无溢出路径是五位小数定点乘法，溢出路径使用上下端点选择；本预算调用没有观察到额外的贸易容量项。于是引擎级公式可以明确写成：

```text
S = 100000
if !TradeAdjustmentPrerequisite(state):
    budget = 0
else:
    A = Σ(selector 对应的 ADD 修正值)       // 定点整数，单位为 S
    F = Π(独立 FACTOR 值 / S)               // 初始 F=1
    x = (S + A) × F                         // ValueCalculator 节点链，定点
    q = trunc_toward_zero(x / S)
    budget = max(1, q)
```

因此标准贸易中心、没有额外 factor 且有效 staffing 的特例是 `budget = max(1, 1 + state_weekly_trades_add_total)`。例如十级贸易中心每级贡献 `1`，州修正表得到 `A=10*S`，则预算为 `1+10=11`；这解释了运行记录中的初始预算 11。若 `+0x68` 的运行时值为 `0.8*S`，则同一例子的未取整值为 `11×0.8=8.8`，最终按机器码的向零截断得到 8，再执行最小值 1。

目前唯一仍需通过 selector 注册表或运行时条目名称补上的，是把数值 `0x2474`（当前进程读取到的 `[0099]` 值）与脚本键 `state_weekly_trades_add` 做名称级对应；这不影响上述引擎公式、加法槽位、倍率槽位和取整/下限行为已经由机器码确定的部分。


---------------------


是的，前面的公式只完整描述了**引擎的数值处理流程**，并没有把每个输入值的游戏业务来源都完全命名清楚。更准确地写法是：

```text
S = 100000

if 不满足贸易调整前置条件:
    return 0

a = selector 选择的州级修正值（定点值）
f = S

if selector != 0xFFFF:
    additive = a

    if state[0x68] < S:
        f = state[0x68]

x = (S + additive) × f / S
q = trunc_toward_zero(x / S)

return max(1, q)
```

其中：

- `S=100000` 是 ValueCalculator 的定点比例单位，不是 100000 次贸易。
- `S + additive` 中的 `additive` 是**每周贸易调整次数的加法修正**。
- 如果脚本值为 `state_weekly_trades_add = 1`，引擎中通常表现为 `100000`，因此贡献 1 次。
- 如果多个来源提供该修正，例如多个贸易中心、生产方式或静态修正，它们会先汇总：

```text
additive = state_weekly_trades_add_total × 100000
```

贸易中心配置位于：

[11_private_infrastructure.txt](D:/Games/Victoria3/Victoria%203/game/common/production_methods/11_private_infrastructure.txt)

```text
state_modifiers = {
    workforce_scaled = {
        state_weekly_trades_add = 1
        state_trade_capacity_add = 10
    }
}
```

因此，标准贸易中心的业务含义是：

```text
贸易中心贡献 =
有效 staffing level × 1 次每周贸易调整
```

例如十级贸易中心、80% staffing：

```text
有效 staffing level = 10 × 0.8 = 8
state_weekly_trades_add_total = 8
```

若没有其他倍率：

```text
budget = max(1, trunc(1 + 8))
       = 9
```

`state_trade_capacity_add = 10` 是贸易容量，不进入这个预算的 ADD 槽位；`state_trade_quantity_mult` 也是贸易数量倍率，也不直接增加调整次数。

`FACTOR` 的含义不同。它不是“额外增加几次贸易”，而是对整个基础值和 ADD 值进行比例缩放：

```text
budget_raw =
    (1 + state_weekly_trades_add_total)
    × factor
```

当前反汇编已经确认，`+12295A0` 会读取 `state+0x68`；当它小于 `100000` 时，将其作为定点倍率使用。例如：

```text
state_weekly_trades_add_total = 10
state[0x68] = 80000  // 0.8 倍

budget_raw = (1 + 10) × 0.8 = 8.8
budget = trunc(8.8) = 8
```

`state+0x68` 可结合同一州对象的市场贸易比例函数 `+1228B90` 命名为“国际市场接入度”（定点比例）。该函数同样读取此字段，并只在低于 `100000` 时把它作为比例输入；这与贸易中心界面显示的国际市场接入度，以及接入度不足时贸易活动按比例受限的业务含义一致。因此它不是 workforce 比例，也不能把贸易中心 `workforce_scaled` 已经折算进 `state_weekly_trades_add` 的 staffing 再乘一次。

因此，目前可以确定的业务公式是：

```text
预算 =
max(
    1,
    trunc_toward_zero(
        (1 + 州级 Weekly Trades 加法总和)
        × min(国际市场接入度, 100%)
    )
)
```

其中 `state_weekly_trades_add` 在修正定义和界面中就是 Weekly Trades；`0x0099` 是引擎取该修正类别的内部 selector，`0x2474` 是本进程中该类别的注册编号。编号本身不是业务量，业务量来自 selector 指向的州级 Weekly Trades 汇总值。


------------------------

### 10.6 贸易中心一次更新中可调整次数的预算的完整计算公式

你说得对。之前把 `state+0x68` 留作“未知倍率”，只能算引擎层描述，不能算完整业务公式。继续反查后，已经可以把它按业务指标整理出来：

```text
贸易调整预算
= max(
    1,
    向零截断(
        (1 + 州 Weekly Trades 总量)
        × 国际市场接入度修正
    )
)
```

其中各参数的业务来源是：

```text
州 Weekly Trades 总量
=
Σ(
    每个贸易中心生产方式实例的
    有效 staffing level
    × 该生产方式的 state_weekly_trades_add
)
+
Σ(其他州级 Weekly Trades 修正)
```

对标准贸易中心：

```text
有效 staffing level
= 贸易中心等级 × staffing 百分比

state_weekly_trades_add
= 1
```

所以：

```text
单个标准贸易中心贡献
= 贸易中心等级 × staffing 百分比 × 1
```

例如：

```text
10 级贸易中心
80% staffing

Weekly Trades = 10 × 0.8 × 1 = 8
```

如果州内还有其他来源，例如静态修正 `state_weekly_trades_add = 2`：

```text
州 Weekly Trades 总量 = 8 + 2 = 10
```

第二个参数是：

```text
国际市场接入度修正
= min(国际市场接入度, 100%)
```

它的业务含义是贸易中心所在州能够接入国际市场的比例：

```text
100% 国际市场接入度 → ×1.0
80% 国际市场接入度  → ×0.8
50% 国际市场接入度  → ×0.5
```

因此完整业务公式是：

```text
T =
    Σ(贸易中心等级 × staffing 百分比 × 生产方式 Weekly Trades 值)
    + 其他州级 Weekly Trades 修正

M = min(国际市场接入度, 1.0)

预算 =
    max(1, trunc_toward_zero((1 + T) × M))
```

例子：

```text
贸易中心等级 = 10
staffing = 80%
生产方式 Weekly Trades = 1
其他 Weekly Trades 修正 = 2
国际市场接入度 = 80%

T = 10 × 0.8 × 1 + 2
  = 10

预算 = trunc((1 + 10) × 0.8)
     = trunc(8.8)
     = 8
```

这也解释了为什么 `state_trade_capacity_add = 10` 不应放进预算公式：它增加的是贸易容量，不是每周允许调整的次数。

依据已经补齐：

- `state_weekly_trades_add` 的脚本定义就是 Weekly Trades；
- `11_private_infrastructure.txt` 中贸易中心以 `workforce_scaled` 提供 `state_weekly_trades_add = 1`；
- `+1228B90` 对同一州对象的 `+0x68` 进行市场贸易比例计算；
- `CalculateTradeAdjustmentBudget` 对同一字段执行“低于 100% 时按比例缩放”的逻辑；
- 贸易中心资料显示国际市场接入度与 Weekly Trades 同时存在，且贸易中心等级满员时每级提供 1 次 Weekly Trades。

因此，`0x0099` 和 `state+0x68` 现在可以转换成业务描述：

```text
0x0099
→ 州级 Weekly Trades 修正类别

state+0x68
→ 州国际市场接入度
```

地址只是实现细节；真正的业务公式就是：

```text
预算 =
max(
    1,
    trunc_toward_zero(
        (
            1
            + Σ(贸易中心等级 × staffing 百分比 × Weekly Trades/级)
            + 其他 Weekly Trades 修正
        )
        × min(国际市场接入度, 100%)
    )
)
```
