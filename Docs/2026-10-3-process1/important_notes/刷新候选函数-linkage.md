

# 核心整理文档

# UpdateStateTrades
每周末尾触发一次
末尾的证据是断点时UI还停在周进度条的末尾，而非下一周的开头。
但是这不能严格证明游戏的上一周末尾和下一周开头是有去别的

```text
UpdateStateTrades(+131C2B0)
    ├─ 准备本轮共享数据（+13260F0）
    ├─ 遍历州，建立贸易调整条目（+11FD230）
    ├─ 按剩余预算排序
    ├─ 循环直到不发生任何 adjust
        ├─ 遍历所有条目，对每个条目，准备候选 PrepareCandidatesForEntries。
        ├─ 然后再遍历所有条目，对每个每个条目 TryAdjustStateTrade(+11FD470)
        └─ 若发生了调整则 adjust = true

    └─ 结束后执行收尾批处理（+1326430）
```

## 遍历全球所有州，建立贸易调整条目

ReadCountryModifier(state, selector0334)
读取州所在国的 selector0334 modifier，推测是`country_disallow_trade_bool`  ，国家级“禁止贸易”布尔修正，对应孤立主义（`law_isolationism`）。

if ReadTradePotential(state) <= 0:
    continue
州的贸易潜力要>0

entry = BuildTradeAdjustmentEntry(state)
这里会在 entry 中初始化本轮的贸易调整预算。

entries.append(entry)

| 偏移 | 含义 |
|---|---|
| `entry+00` | 本次初始操作预算 `B` |
| `entry+04` | 剩余操作预算，排序和后续扣减使用 |
| `entry+08` | 州对象引用/句柄 |
| `entry+0C` | 分组键，可能对应市场或相关贸易对象 |
| `entry+10`、`entry+60` | 临时贸易数值表 |
| `entry+B0` | 增加候选，后续保存商品、方向、评分、数量等 |
| `entry+F8` | 减少候选，结构与增加候选类似 |

SortByRemainingBudgetDescending(entries)
本轮优先处理剩余贸易调整预算较多的州。
这个函数有点蠢，为了性能直接牺牲逻辑了。

接下来是一个 while 循环
while(anyAdjusted)
{
移除所有已经没有剩余预算的州

对剩余的所有 entries
// 为每个条目重新选择一个减少候选商品和一个增加候选商品。
PrepareCandidatesForEntries(entries, groupedTables, aggregateTables, seed)

设置 anyAdjusted = false
for entry in entries:
    adjusted = TryAdjustStateTrade(entry,tables，aggregateTables)

    //任意一个entry如果调整过，说明整体商品贸易分布发生了改变，PrepareCandidatesForEntries 对每个州的结果可能会发生变化。因此需要继续迭代。
    
    //迭代直到所有项目都不需要调整，或者 entries 前面已经清空
    anyAdjusted = anyAdjusted or adjusted
}

每个 entry(州) 都有一个州贸易调整预算
在执行 TryAdjustStateTrade 过程中会扣减预算
如果成功则 -1(100%)，失败则 - 0.2*initialBudget(-20%)
因此一定会在有限次数内耗尽预算，结束while


# BuildTradeAdjustmentEntry
功能：为一个州创建本轮贸易调整条目，计算初始操作预算，并初始化后续候选选择、临时表和候选槽位。
就是一个变量初始化，提供一个空的 Entry 初始状态容器。

预算 ≈ 本州每周可进行的贸易调整次数

`game/common/defines/00_ai.txt` 还明确说明：贸易中心成功执行一次贸易消耗 1 次 weekly trade，失败执行则消耗总 weekly trades 的 `0.2`。

WeeklyTradeTotal =  1
            + Σ(贸易中心等级 × staffing 百分比 × Weekly Trades/级)
            + 其他 Weekly Trades 修正
这一部分是基于贸易中心等级，满员率，和事件等其他修正，得到WeeklyTrade总值

预算 = max(1, trunc_toward_zero(WeeklyTradeTotal))
保证从 WeeklyTrade 机制计算出的预算绝不会<1 （大概对应每周调整一次贸易）

Build entry 之后 entry 中就会有州的 Budget 了。

# PrepareCandidatesForEntries
功能：对本轮仍有预算的所有条目重新选择一个减少候选和一个增加候选。
这个减少候选，和增加候选，被分别写入entry+F8，entry+B0

选择减少候选的函数 SelectReductionCandidate
选择增加候选的函数 SelectIncreaseCandidate

## SelectReductionCandidate

signedUnits = ReadGoodsValue(state.table1D88, goods) / 100000
读取当前该州所有已经在贸易中的商品的占用的贸易容量
前分析对应正值出口、负值进口

如果最近刚增加过贸易量的商品，8周内不会减少。

遍历州已存在贸易商品列表，挑选 best（评分最低商品）
best = null
for goods in 州已存在贸易商品列表

    //输入 state 州状态对象，和 goods（遍历中的一种商品） 
    candidate = MakeCandidate(
        state,
        goods,
        direction = (signedUnits > 0 ? 1 : 0),
        mode = REDUCTION
    )

    //刷新 candidate 商品的评分
    Refresh(candidate, context)

    if candidate.score < best.score
        best = candidate
    elseif candidate.score = best.score
        随机挑选二者一个作为 best

return best    


best = SelectReductionCandidate()  //best 就是返回值


## SelectIncreaseCandidate

前提：
PassCountryAndMarketFilters 
//如果商品在该国或者该州禁止贸易的列表中则不进入后续处理
//例如事件禁酒，禁鸦片，或者条约禁止贸易某种商品
GoodsCanBeTraded //是可贸易的货物，排除本地商品如运力
ExistingTradeHasOppositeDirection  //如果已存在反方向贸易则不在此方向贸易中增加此类货物

//对两个方向，分别遍历所有可用商品类型
//注意是对两个方向最终只挑选出一个评分最高的，也就是进出口两个方向只能一次更新调整一个商品
for direction in [0, 1]:
    for goods in GoodsDatabase:
        //流程和 SelectReductionCandidate 内循环基本一致
        //先把当前商品作为 candidate，然后更新它的评分
        candidate = MakeCandidate(
            state,
            goods,
            direction,
            mode = INCREASE
        )

        Refresh(candidate, context) 

        //若评分未达到可增加的阈限，则继续遍历其他商品
        if not MeetsIncreaseThreshold(candidate):
            continue

        //挑选评分最高的
        if candidate.score > best.score:
            best = candidate
        elseif candidate.score = best.score
            随机挑选二者一个作为 best
        
return best

best = SelectIncreaseCandidate()  


-----------------

# MakeCandidate
初始化 candidate 对象，包含下面字段
```cpp
function MakeCandidate(state, goods, direction, mode):
    candidate = stack_storage(0x48)
    candidate.goods       = goods                    // +00，8 字节商品指针
    candidate.direction   = direction                // +08，1 字节方向
    candidate.baseRevenue = 0                        // +10，8 字节基础收益
    candidate.unitRevenue = 0                        // +18，8 字节单位净收益
    candidate.score       = 0                        // +20，8 字节最终意愿评分
    candidate.stateRef    = load_u32(state + 0x08)    // +28，4 字节州引用
    candidate.mode        = mode                     // +2C，4 字节评估模式
    candidate.shortage    = 0                        // +30，8 字节短缺评分项
    candidate.quantity    = 0                        // +38，8 字节本次单位容量交易量
    candidate.advantage   = 0                        // +40，8 字节方向性贸易优势
    // +09..+0F 未见初始化，不把结构填充字节假定为已清零。
    return candidate
```

candidate 的信息会被用在 Refresh 中，作为读写的容器。
初始化的时候基本都是空的，Refresh 过程中会逐渐填充它。

------------------

# Refresh
根据最新的商品数量，刷新候选商品的评分

# Refresh ->CalculateQuantityPerCapacity (+122AB50)

## CalculateQuantityPerCapacity
功能：计算刷新候选时，指定州每单位贸易容量能够产生的货品数量


# Refresh ->ReadOrComputeDirectionalTradeAdvantage（+11FBDA0）

## ReadOrComputeDirectionalTradeAdvantage 
读取或计算指定州、商品和贸易方向的绝对贸易优势

绝对贸易优势会被用来计算相对贸易优势，然后决定商品进口价格。
来源于开发日志和wiki猜测（Docs\vic3_doc_copy\trade_center_model1.md）

（1）计算X州贸易中心的单位绝对贸易优势 TA_raw
TA_raw = B + Σ AdvantageContribution_k
B = 100 基础值
AdvantageContribution_k 各种加成

（2）计算贸易中心的相对贸易优势 r
单个 X 贸易中心的加权优势为：
W_tc = TA_tc × Q_tc
Q_tc：某个贸易中心，对某一种商品、在某一个贸易方向（进口或出口）上的交易量

同一商品、同一贸易方向下，全球加权优势为：
W_total = Σ(TA_j × Q_j)

优势份额和交易量份额分别为：
R_share = (TA_tc × Q_tc) / Σ(TA_j × Q_j)
V_share = Q_tc / ΣQ_j

最终计算得当前 X 贸易中心的相对贸易优势为：
RelativeAdvantage = R_share / V_share - 1


# Refresh ->UpdateCandidateShortage (UpdateCandidatePartA，+11FBA60)
// 功能：计算候选商品的短缺指标，仅对进口商品返回非0值
有效供给低于需求的一半时，返回短缺评分>0。短缺评分在0~0.5之间，越大的值代表短缺程度越强。
shortage_unclamped = 1 - (supply/demand) / 0.5
shortage = clamp(shortage_unclamped, 0, 0.5)


# Refresh ->UpdateCandidateRevenue (UpdateCandidatePartB,+11FC080)





# Refresh 中调整量的计算已得到数据验证
验证数据在 `Docs\important_notes\刷新候选函数进出口数量输出分析.md` L161。
算法：
每 1 单位贸易容量承载的商品量 = traded_quantity
贸易中心生产方式带来的修正 = modifier_raw（需转换定点数）
q_raw = FixedMultiply(base_raw, 100000 + modifier_raw)
q_raw = max(q_raw, MINIMUM_GOODS_TRADED_QUANTITY)
MINIMUM_GOODS_TRADED_QUANTITY = 0.5 * 100000 = 50000 （定点数）

累计商品变化 = Σ每次成功增加的 q_i - Σ每次成功减少的 q_i


---------------------------


# TryAdjustStateTrade

输入一个 entry (对应一个州的贸易情况)
对 entry 中的两个候选商品分别刷新一次评分，然后评估贸易容量
尝试移除候选商品中的候选移除项
尝试增加候选商品中的候选增加项
如果成功，那么就修改全局 table ，更新贸易情况。


