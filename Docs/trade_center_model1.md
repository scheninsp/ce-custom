# 贸易中心模型：商船价格、优势和利润

> **数据校正说明**：原始观测曾将日本山东（青岛）的数据标为“条约港”。现已确认这些数据来自**青岛普通地区**，并非条约港。因此下文不再把山东/青岛观测作为条约港样本，也不据此推导条约港专属机制。凡涉及条约港的结论，仅保留为游戏规则背景或待验证事项。

数据来源：`Docs/treaty_port1.md`（标注日期 1870-01-01）及本地游戏文件。下文的“精确复现”仅指按 UI 显示精度一致；不将不同提示框的数值强行视为同一计算时点或同一内部精度。

## 1. 观测数据和数据一致性

| 指标 | 日本山东（青岛普通地区） | 荷兰（阿姆斯特丹贸易中心） |
|---|---:|---:|
| 商船进口量 | 12 | 30 |
| 世界市场价 | £50.9 | £50.9 |
| 进口价 | £53.9 | £44.8 |
| 本地价 | £67.4 | £58.0 |
| 所属市场价 | 日本 £62.4 | 法兰西 £56.8 |
| 商船基准价 | £50 | £50 |
| 市场/本地定价权重 | 80% / 20% | 95% / 5% |
| 本地生产 / 消费 | 19.2 / 70.8 | 84.0 / 150 |
| 相对优势（进口面板） | -21% | +54% |
| 进口价修正（面板） | +5% | -11% |
| 商品贸易利润 | £0.16K | £0.39K |
| 每容量商品数量 | 4 | 6 |
| 每容量商品利润 | £54.1 | £79.1 |
| 关税 / 补助 | 0 / 0 | 0 / 0 |

**警告：荷兰各 UI 记录不一致。**“全球贸易优势”列表给荷兰 `7.48K、+47%`；荷兰进口优势子提示则给 `7.84K、+54%`，并且同组资料中既有“249 基础优势”，又有“261 / 单位进口”。这些数值**恰好形成两组**，不能不加说明地混用：

| 可能的一组 | 单位优势 | 进口量 30 对应的优势 | 全球优势占比（全球 37.5K） | 与全球贸易量占比 30/222 对比 |
|---|---:|---:|---:|---:|
| 列表/249 | 249 | 7.47K，约 7.48K | 约 19.95% | 约 +47.6%（UI +47%） |
| 子提示/261 | 261 | 7.83K，约 7.84K | 约 20.91% | 约 +54.7%（UI +54%） |

两组之间优势约差 4.8%。可能是更新时点、口径、UI 显示缓存或其他未记录修正；**不能据此确定原因**。以下分别计算，不把 +47% 偷换成 +54%。日本山东（青岛普通地区）的 `132 × 12 = 1,584`，与 `1.58K` 对应。该样本不属于条约港，故只能用于普通地区贸易中心的计算核对。

## 2. 贸易优势和相对优势

### 2.1 单位贸易优势

日本山东的 UI 可以直接核对：

```text
基础 100 × (1 + 日本帝国 25% + 贸易容量约 7%) ≈ 132
132 × 12 = 1,584 ≈ 1.58K
```

荷兰的静态项合计：

```text
基础 100 + 贸易特权 76.5 + 利益 1.03 - 禁运 1.21 = 176.32
176.32 × (1 + 尼德兰 25% + 贸易容量约 16%)
= 176.32 × 1.41 ≈ 248.61 ≈ 249
```

这支持“百分比加成**相加后**乘以静态优势”的候选规则，而不是 `(176.32 × 1.25 × 1.16) ≈ 255.66`。但荷兰另一处 `261/单位` 无法由已列出的 +25%、+16% 得到；若其余基础项不变，则需要合计约 `261/176.32 - 1 = 48.03%`（即在 +25% 外另有约 +23%），而非 41%。**261 对应的未显示/变动项待核查**。容量 141 → +7%、329 → +16% 与每 20 容量约 +1% 的量级一致，但“上限”分别显示 25%、30%，不能凭两点断言通用容量公式。

本地定义 `game/common/defines/00_defines.txt:452-462` 给出基础优势 100、条约港、贸易协定等因素；这里“来自日本帝国/尼德兰 +25%”的具体机制不能仅靠国名推定为条约港加成。尤其需要注意：本次山东数据来自**普通地区**，因此不能用它证明条约港因素已生效，也不能用它反推出条约港加成。

### 2.2 全球份额和相对优势

由两州数据共同支持的候选公式：

```text
优势份额 a = 本州该货物进口优势总和 / 全球该货物进口优势总和
贸易份额 t = 本州该货物进口量 / 全球进口量
相对优势 r = a/t - 1
```

日本山东（使用显示值）：

```text
a = 1,580 / 37,500 ≈ 4.2133%
t = 12 / 222 ≈ 5.4054%
r ≈ 4.2133% / 5.4054% - 1 ≈ -22.05%（UI -21%）
```

荷兰子提示的一组：

```text
a = 7,840 / 37,500 ≈ 20.9067%（提示框写 20.87%）
t = 30 / 222 ≈ 13.5135%
r ≈ 20.9067% / 13.5135% - 1 ≈ +54.71%（UI +54%）
```

若改用荷兰列表的 7.48K：

```text
a = 7,480 / 37,500 ≈ 19.9467%
r ≈ 19.9467% / 13.5135% - 1 ≈ +47.60%（列表 UI +47%）
```

**两组荷兰数据各自支持同一个比值公式**，是对候选式的有力佐证；但山东算出 -22.05% 而不是 -21%，荷兰的 `7.84K/37.5K` 算出 20.91% 而不是提示的 20.87%。这说明 UI 的“精确占比”与紧邻的 K 数值、总数也并非完全同一精度/口径。不能声称已经精确识别取整或内部更新顺序。

### 2.3 为什么相对优势不是单纯由进口量决定

设某州的单位进口优势为 `u_i`，该州进口量为 `q_i`；对全球各州分别使用下标 `j`。则该州的进口优势总值为：

```text
A_i = u_i × q_i
```

全球该商品的进口优势总和为：

```text
A_global = Σ(u_j × q_j)
```

因此，优势份额和贸易份额分别是：

```text
a_i = (u_i × q_i) / Σ(u_j × q_j)
t_i = q_i / Σq_j
```

将两者相除：

```text
a_i / t_i
= [(u_i × q_i) / Σ(u_j × q_j)] / [q_i / Σq_j]
= u_i × Σq_j / Σ(u_j × q_j)
```

令全球按进口量加权的平均单位优势为：

```text
ū = Σ(u_j × q_j) / Σq_j
```

则：

```text
a_i / t_i = u_i / ū
相对优势 r_i = u_i / ū - 1
```

这说明，`q_i` 在本州优势总值 `u_i × q_i` 与本州贸易份额 `q_i` 中会发生**显式约消**。所以相对优势的直接含义不是“进口量大就有优势”，而是：

> 本州单位进口优势相对于全球进口量加权平均单位优势高出或低于多少。

例如，本州单位优势为 `150`，全球加权平均单位优势为 `100`，则：

```text
r = 150 / 100 - 1 = +50%
```

不过，这不表示进口量在整个系统中完全没有作用。`q_i` 仍有以下间接作用：

1. **改变全球加权平均值。** `ū` 的分母和分子都包含 `q_i`。如果本州单位优势高于当前全球平均值，增加本州进口量会使全球平均值向 `u_i` 靠近，从而可能降低本州相对优势；如果 `u_i` 低于全球平均值，则方向相反。
2. **可能影响单位优势本身。** 贸易容量、贸易协定、国家修正、禁运等因素可能改变 `u_i`；如果进口量的变化同时来自这些机制，进口量便会通过单位优势间接影响 `r_i`。
3. **实际 UI 数值存在取整和不同步问题。** 上述代数推导使用同一时点、同一内部精度的数值；游戏界面显示的优势总值、进口量和百分比可能来自不同精度或更新时点，因此用显示值计算时不会严格相等。

因此，更准确的结论是：**本州进口量在 `a/t` 的本地分子和本地贸易份额中会显式约消；它不直接决定相对优势，但会通过全球加权平均单位优势、单位优势的形成以及游戏内部更新机制间接影响相对优势。**

## 3. 本地价格：两州交叉校验

### 3.1 游戏文件的边界和比例

`game/common/defines/00_defines.txt:415-417`：

```text
PRICE_RANGE = 0.75
BUY_SELL_DIFF_AT_MAX_FACTOR = 2
```

注释规定商品价格最低/最高为基准价的 `1 ± 0.75`，且说明买卖单的比例到达 `BUY_SELL_DIFF_AT_MAX_FACTOR` 时达到价格极限。`game/localization/english/concepts_l_english.yml:681-690` 说明州本地价格由本地生产、消费、所属市场价格及市场准入价格影响共同决定；提示框直接给出两州市场权重 80% 与 95%。

两州都可用以下**由注释和观测共同支持的候选供需价格函数**解释：

```text
商品基础价 B = £50
本地买单 D、本地卖单 S（暂按 UI 的消费/生产为对应订单）
本地孤立价格 L = B × [1 + 0.75 × clamp(D/S - 1, -1, +1)]
本地成交价格 P = w × 所属市场价 + (1-w) × L
```

`clamp(x, -1, +1)` 意味着变化幅度限制在 -75% 至 +75%。此式在 `D/S = 2` 时达到最高价 £87.5；对于本篇两个 **D > S** 的实例，下面的验证只用到上限，不能借此确认 `D < S` 区间以及零供应的实现细节，也不能排除额外垄断等价格修正。

### 3.2 日本山东普通地区：达到本地价格上限

```text
D/S = 70.8 / 19.2 ≈ 3.6875 > 2
L = £50 × (1 + 0.75) = £87.5
P = 0.80 × £62.4 + 0.20 × £87.5
  = £49.92 + £17.50 = £67.42 → UI £67.4
```

先前从 `£67.4 = 0.8 × £62.4 + 0.2 × L` 用一位小数显示值反解出的 `L=£87.4`，是**显示取整后的反解值**；定义所支持的上限是 **£87.5**，预测的最终本地价 £67.42 与 UI £67.4 匹配。`67.4/62.4 - 1 ≈ +8.01%` 也与“高于日本市场 +8%”一致。

### 3.3 荷兰：未达到本地价格上限

```text
D/S = 150 / 84 ≈ 1.785714 < 2
L = £50 × [1 + 0.75 × (150/84 - 1)]
  = £50 × (1 + 0.589286) ≈ £79.4643
P = 0.95 × £56.8 + 0.05 × £79.4643
  = £53.96 + £3.9732 ≈ £57.9332
```

按**所给显示值**四舍五入到一位小数应为 **£57.9**，而 UI 显示 £58.0。误差约 £0.067：远小于基础价格上限跨度，但不应称为精确吻合。尤其荷兰的 `95%` 权重、`150` 消费值及 `£56.8` 市场价都可能是四舍五入后的结果；例如市场价若靠近 £56.85、权重约 94.5%，计算值可接近 £57.98。荷兰本地价格高于市场价约 `58.0/56.8 - 1 ≈ +2.11%`，**与 UI 写的“+1%”不一致**；即便按一位小数价格的普通取整，差异也难降至 +1%。需核对该提示的百分比计算口径或截图时点。

作为对比，直接由显示值反推的荷兰等效本地部分为 `(58.0 - 0.95×56.8)/0.05 = £80.0`；候选供需函数给出 £79.46，差 £0.54，但经仅 5% 权重后差约 £0.027。不能仅根据这个反推值推断内部孤立价恰为 £80。

### 3.4 当前本地模型的适用范围

两州的“本地生产/消费值”是否已包含贸易中心进出口订单，提示文字仅说国际市场贸易参与定价；目前没有订单明细可以独立验证 `S=生产值、D=消费值` 的完整口径。但上述计算在山东精确复现 UI 一位小数、在荷兰接近一位小数，因此是比只反解等效价格更有解释力、且可继续用第三州检验的模型。切勿把本地价格当作进口价格的直接输入：进口影响本地供应订单和随后结算的本地价格，是间接反馈。

## 4. 相对优势 → 进口价：新增荷兰数据尚未闭合

`game/localization/english/concepts_l_english.yml:692-696` 指明进口价取决于世界市场价和相对优势。`game/common/defines/00_defines.txt:447-450` 将相对优势偏离 1 对价格的影响系数设为 `0.25`。结合山东和荷兰两组观测，目前最接近的进口方向公式是：

```text
进口价 P_i = 世界价 P_w / (1 + 0.25 × r)
```

其中 `r` 是带符号的相对优势小数：`+54% = 0.54`，`-21% = -0.21`。该式的方向符合贸易竞争关系：相对优势为正时，进口价格低于世界市场价；相对优势为负时，进口价格高于世界市场价。

### 4.1 荷兰数据

荷兰显示相对优势为 +54%，国际市场价为 £50.9：

```text
P_i = 50.9 / (1 + 0.25 × 0.54)
    = 50.9 / 1.135
    ≈ £44.85
```

UI 显示 £44.8，误差约 £0.05。这是目前对该公式最强的单组验证。

### 4.2 日本山东数据

山东显示相对优势为 -21%，国际市场价为 £50.9：

```text
P_i = 50.9 / (1 + 0.25 × -0.21)
    = 50.9 / 0.9475
    ≈ £53.72
```

UI 显示 £53.9，差异约 £0.18。这个差异仍可能来自内部未显示精度、价格与优势数据不同步、或尚有未显示的修正项；但若用优势份额和贸易量份额反推山东相对优势，约为 -22.05%，与 UI 的 -21% 本身已经存在约一个百分点的差别。按观测进口价反推所需优势为：

```text
r = (P_w / P_i - 1) / 0.25
  = (50.9 / 53.9 - 1) / 0.25
  ≈ -22.26%
```

这反而接近由全球份额计算出的约 -22.05%。因此山东的差异不能简单视为公式失效。

### 4.3 与直接乘法模型比较

若使用另一个候选式：

```text
P_i = P_w × (1 - 0.25 × r)
```

则得到：

| 数据组 | 直接乘法模型 | 倒数模型 | UI 进口价 |
|---|---:|---:|---:|
| 山东，-21% | £53.57 | £53.72 | £53.9 |
| 荷兰，+54% | £44.03 | £44.85 | £44.8 |

倒数模型在荷兰数据上明显更接近，在山东数据上也更接近。因此当前应把倒数模型作为**最佳工作模型**，而不是继续把它列为与直接乘法等价的普通候选。

### 4.4 公式的证据等级和限制

目前可以采用：

\[
\boxed{
P_{\text{进口}}
=\frac{P_{\text{国际市场}}}
{1+0.25r}
}
\]

作为贸易中心进口价格的最接近模型。它同时解释：

- 荷兰 `+54%` → 进口价格低于 £50.9，预测约 £44.85；
- 山东 `-21%` → 进口价格高于 £50.9，预测约 £53.72；
- 贸易优势越高，进口路线越有竞争力，采购价格越低；
- 贸易优势越低，采购价格越高。

但这还不是源码级确认。山东仍有 £0.18 的显示差异，且荷兰数据存在 `249/7.48K/+47%` 与 `261/7.84K/+54%` 两组不同提示。荷兰进口价 £44.8 与倒数模型吻合的是 +54% 这一组；若使用另一组 +47%，预测为：

```text
50.9 / (1 + 0.25 × 0.47) ≈ £44.92
```

同样接近 £44.8，但不能用两组数据证明其中哪一组是进口价格结算时采用的内部值。后续若获得暂停在同一时点的完整优势值和价格值，应优先检验倒数模型，而不是直接乘法模型。

## 5. 单位、每容量和总商品利润

进口贸易中心提示框的商品利润模型可以直接复算：

```text
单位商品利润 = 本地价 - 进口价 + 单位补助 - 单位关税
每容量商品利润 = 单位商品利润 × 每容量商品量
总商品贸易利润 = 单位商品利润 × 实际进口量
```

这里核对的是**商品路线利润**，不等于扣除建筑工资和其他投入后的贸易中心净收入。

| 货物 | 单位价差 | 每容量数量 | 按显示值计算的每容量利润 | UI | 按显示值计算的商品总利润 | UI |
|---|---:|---:|---:|---:|---:|---:|
| 山东商船 | 67.4 - 53.9 = £13.5 | 4 | £54.0 | £54.1 | 12 × 13.5 = £162 | £0.16K |
| 荷兰商船 | 58.0 - 44.8 = £13.2 | 6 | £79.2 | £79.1（提示写价差 £13.1） | 30 × 13.2 = £396 | £0.39K |
| 山东硬木 | 28.3 - 47.4 + 20.0 = £0.9 | 5 | £4.50 | £4.43 | 40 × 0.9 = £36 | £0.03K |

荷兰的 `£58.0 - £44.8 = £13.2` 与子提示所写 `£13.1` 相差 £0.1；不同字段可能分别取整或跨结算时点，**不能把显示值的精度当作内部计算精度**。荷兰使用贸易容量 `30 / 6 = 5`，山东商船 `12 / 4 = 3`，山东硬木 `40 / 5 = 8`。按荷兰显示的每容量 £79.1 × 5 = £395.5，与 £0.39K 的显示精度/舍入规则需另核；不宜仅据此推断额外税费。

硬木“50% 补助”与 UI“£20.0 每单位补助”不能按 `50% × £47.4` 换算：那会得到 £23.7。商船两州补助都为零，不能用它们检验补助计价基准或**条约港补助是否实际支付**。由于山东不是条约港，本组数据也不能支持任何“条约港补助”结论。

## 6. 目前最可靠的计算流程及待验证项

1. **单位优势**：山东普通地区约 132；荷兰已列项目可得约 249，但另一子提示为 261。
2. **相对优势**：按 `(本州优势份额 / 本州贸易量份额) - 1`；荷兰的两组数据各自支持此式，日本显示值约差 1 个百分点。
3. **进口价格**：当前最佳工作模型为 `P_i = P_w / (1 + 0.25r)`。荷兰 +54% 的预测值约 £44.85，接近 UI £44.8；山东 -21% 的预测值约 £53.72，低于 UI £53.9，但按进口价反推的 -22.26% 接近由全球份额得到的约 -22.05%。该公式已得到两组观测的方向和量级支持，但仍需同一时点的内部精度数据进行源码级确认。
4. **本地价格**：用 £50 基准价、±75% 上限、2 倍供需阈值所构造的孤立价格，再按 UI 的 80%/20% 或 95%/5% 与市场价混合；山东结果 £67.42→£67.4，荷兰约 £57.93 与 £58.0 接近。
5. **商品利润**：本地价减进口价加补助减关税，按商品量或贸易容量计；两州商船和硬木均在 UI 精度内基本匹配。
6. **条约港结论限制**：山东/青岛观测是普通地区，不能用于验证条约港专属优势、贸易或补助机制。需要另行采集明确标识为条约港的样本。

进一步确定进口价格内部公式，应在**同一暂停时点**收集两州的世界价、进口价、整数百分比的完整子提示、单位优势、优势总和及贸易量；尤其要查清荷兰 `249/7.48K/+47%` 与 `261/7.84K/+54%` 的来源。进一步验证本地价格函数，应记录第三个 `D/S` 在 1 与 2 之间且本地权重较高的州，以便更清楚地检验未到上限时的价格斜率。

## 7.贸易中心的绝对优势与相对优势

### 贸易中心（TC）的绝对贸易优势

Wiki 页面：[https://vic3.paradoxwikis.com/Trade#Trade_advantage](https://vic3.paradoxwikis.com/Trade#Trade_advantage)

> 
> 原文逐条：
> 
> 
> - Base trade advantage: 100
> - +2 for every percentage of the global production that is within the market area
> - +0.5 for every percentage of the production in a market area that is controlled by a company with trade rights
> - +1 for every percentage of production that is prestige goods, for export advantage only
> - +1 for each percentage of trade going to a country that the trade center's owner has trade privileges with
> - +2 for each percentage of trade that is to a trade center in a treaty port
> - −0.5 for each percentage of trade that is going to a country that the trade center owner lacks an interest with. Not applicable with External Trade III
> - −0.75 for each percentage of trade with a country that is at war with the trade center owner
> - −1 for each percentage of trade going to a country that is embargoing the trade center owner
> 
> 
> 百分比乘数修正：
> 
> 
> - +25% External Trade I power bloc principle
> - +5% market capital trade center
> - +25% trade law (Free Trade)
> - Up to +0.5% per 100 trade capacity (capped)

### 相对贸易优势
source: Dev Diary #143（Trade Rework: The World Market）

贸易优势按**每个贸易中心、每种商品、每个贸易方向（出口 / 进口）**独立计算。
绝对贸易优势 × 交易量得到权重；将该贸易中心的**全局优势占比**，和它的**全局交易量占比**对比，得到相对优势，用来修正成交价格。
贸易优势是零和博弈：所有交易者加权平均成交价永远等于世界市场价，你的溢价来自对手折价。


### 完整算法
#### 1. 先算：绝对贸易优势（Absolute Trade Advantage，简称 TA）

单个贸易中心，某商品，某方向的基础 TA：

```
TA_base = 100
```

叠加各项修正（按百分比贡献累加）：

- +2 / 每 1% 全球产量在你的市场内
- +0.5 / 每 1% 市场内产量由拥有贸易权的公司控制
- +1 / 每 1% 属于奢侈品产量（**仅出口**生效）
- +1 / 每 1% 贸易流向你拥有利益的国家
- +2 / 每 1% 流向条约港内贸易中心
- −0.5 / 每 1% 流向你没有利益的国家（外贸 III 法律可抵消）
- −0.75 / 每 1% 流向交战国家
- −1 / 每 1% 流向对你禁运的国家

再乘百分比乘数修正：

- 市场首都内贸易中心：+5%
- 自由贸易法：+25%
- 外贸 I 阵营原则：+25%
- 贸易容量随规模提供加成：每 100 贸易容量最多 + 0.5%（上限）

> 
> 得到：**单个 TC (Trade Center) 的绝对 TA（Trade Advantage） 值**

#### 2. 计算加权总优势：TA × 交易量

游戏把【绝对 TA × 该贸易中心此商品的交易量】作为权重：

\(W_{tc}=TA_{tc} \times Q_{tc}\)

- \(W_{tc}\)：该贸易中心的加权优势
- \(Q_{tc}\)：该 TC 此商品的交易数量（出口量 / 进口量）

全球同方向总和：

\(W_{total}=\sum W_{tc}\)

相对优势份额（Relative Advantage Share）

\(R_{share,tc} = \frac{W_{tc}}{W_{total}}\)

交易份额（Volume Share）

\(V_{share,tc} = \frac{Q_{tc}}{\sum Q_{tc}}\)

相对优势差值（决定价格修正）

\(RelAdvantage = \frac{R_{share,tc}}{V_{share,tc}} - 1\)

> 
> 例子：优势占比 88.68%，交易量占比 71.2% → RelAdvantage = 88.68/71.2 −1 = **+24%**Paradox Pl...

#### 3. 相对优势用来干什么：修正实际成交价格

> 
> 世界市场价 \(P_{world}\) 是同方向所有交易者的加权平均价格。

价格修正公式：

\(P_{actual}=P_{world} \times (1 + k \times RelAdvantage)\)

- k：缩放系数，游戏内上限：**相对优势 100% 时，获得最大 25% 价格加成**（tooltip 说明）
- 出口：RelAdvantage>0 → 卖价高于世界市场价，赚更多利润
- 进口：RelAdvantage>0 → **买价更低**（对你有利）

> 
> 零和性质：有人 + 24% 溢价，就必然有人负的折价，加权平均最终回归世界市场价。

#### 4. 价格修正之后：决定贸易中心利润 & 后续贸易流量

贸易中心利润 =（成交价格差 − 运费、维护、商船消耗）× 交易量
利润越高，贸易中心会**自动扩大贸易容量、提升交易量**，进一步放大你的加权优势 \(W_{tc}\)，形成正向滚雪球。



## 8.绝对优势相关常量配置在 Victoria3 游戏目录中的存储位置

本地当前安装版本是 `Victoria 3 1.13.9 (Matcha)`，这些数值并不全部存放在同一个文件中。核心 Trade Advantage 常量集中在：

`game/common/defines/00_defines.txt:447`

对应关系如下：

| Wiki 项目 | 本地常量 | 文件位置 |
|---|---:|---|
| Base trade advantage | `TRADE_CENTER_ADVANTAGE_BASE = 100` | `game/common/defines/00_defines.txt:452` |
| 市场区域全球产量：每 1% +2 | `TRADE_CENTER_ADVANTAGE_MARKET_AREA_PRODUCTION_FACTOR = 200` | `game/common/defines/00_defines.txt:453` |
| Trade Charter 公司产量：每 1% +0.5 | `TRADE_ADVANTAGE_COMPANY_CHARTER_FACTOR = 50` | `game/common/defines/00_defines.txt:454` |
| Prestige goods：每 1% +1 | `TRADE_CENTER_ADVANTAGE_MARKET_PRESTIGE_GOOD_FACTOR = 100` | `game/common/defines/00_defines.txt:455` |
| Trade privileges：每 1% +1 | `TRADE_CENTER_ADVANTAGE_TRADE_AGREEMENT_FACTOR = 100` | `game/common/defines/00_defines.txt:456` |
| Treaty port：每 1% +2 | `TRADE_CENTER_ADVANTAGE_TREATY_PORT_FACTOR = 200` | `game/common/defines/00_defines.txt:457` |
| Embargo：每 1% −1 | `TRADE_CENTER_ADVANTAGE_EMBARGO_FACTOR = -100` | `game/common/defines/00_defines.txt:460` |
| War：每 1% −0.75 | `TRADE_CENTER_ADVANTAGE_AT_WAR_FACTOR = -75` | `game/common/defines/00_defines.txt:461` |

这里的 `100` 表示每 1% 对应 `+1.0 TA`，`50` 表示 `+0.5 TA`，因此 Wiki 的显示值是这些内部整数因子除以 100 后的结果。

**缺乏 Interest 的 −0.5**

这一项不是普通 `defines` 常量，而是 Interest Tier 定义：

`game/common/interest_tier_types/interest_tier_types.txt`

其中最低级别：

```text
interest_tier_none = {
    trade_advantage_exports = -50
    trade_advantage_imports = 0
}
```

位置是：

- `game/common/interest_tier_types/interest_tier_types.txt:1`
- `game/common/interest_tier_types/interest_tier_types.txt:6`

所以本地脚本明确表示：没有 Interest 时，出口 Trade Advantage 为 `-50`，即 `−0.5`；进口方向为 `0`。External Trade III 通过下面的布尔修正取消该惩罚：

`game/common/power_bloc_principles/00_power_bloc_principles.txt:630`

```text
country_no_advantage_loss_from_lack_of_interest_bool = yes
```

**百分比乘数**

1. External Trade

位于：

`game/common/power_bloc_principles/00_power_bloc_principles.txt:566`

```text
principle_external_trade_1 = {
    member_modifier = {
        state_trade_advantage_mult = 0.25
    }
}
```

External Trade II 和 III 也各自有相同的 `0.25`：

- `game/common/power_bloc_principles/00_power_bloc_principles.txt:602`
- `game/common/power_bloc_principles/00_power_bloc_principles.txt:619`

因此脚本层面是每一级 `+25%`；后续等级的注释写明包含前级修正，实际等级可能累计为 `+25% / +50% / +75%`。

2. Market capital

位于：

`game/common/static_modifiers/00_code_static_modifiers.txt:287`

```text
market_capital_state = {
    state_trade_advantage_mult = 0.05
}
```

即 `+5%`。

3. Free Trade

位于：

`game/common/laws/00_trade_policy.txt:96` 附近的 `law_free_trade` 定义，修正位于：

`game/common/laws/00_trade_policy.txt:134`

```text
modifier = {
    state_trade_advantage_mult = 0.25
}
```

即 `+25%`。

4. Trade Capacity

位于：

`game/common/static_modifiers/00_code_static_modifiers.txt:70`

```text
state_trade_advantage_from_capacity_add = 0.0005
state_max_trade_advantage_from_capacity_add = 0.2
```

这里本地文件的字面值是：

- 每单位 Trade Capacity：`0.0005`
- 最大值：`0.2`

需要注意，这与您列出的 Wiki 表述“每 100 Trade Capacity +0.5%”存在数值疑点。若这些值按普通小数乘数解释，`0.0005 × 100 = 0.05`，即 `+5%`，而不是 `+0.5%`。本地脚本本身明确写的是 `0.0005` 和 `0.2`，建议以游戏内 tooltip 或当前版本实际显示为准，Wiki 可能对应其他版本或存在小数位换算/排版差异。

**Tooltip 文本位置**

游戏界面使用的 Trade Advantage 分解文本在：

`game/localization/english/interfaces_l_english.yml:6502`

相关条目包括：

- `ADVANTAGE_FROM_CAPACITY`
- `ADVANTAGE_FROM_TRADE_AGREEMENTS`
- `ADVANTAGE_FROM_TREATY_PORTS`
- `ADVANTAGE_FROM_INTEREST_TIER`
- `ADVANTAGE_FROM_AT_WAR`
- `ADVANTAGE_FROM_EMBARGO`
- `ADVANTAGE_MARKET_AREA_GOODS_PRODUCTION`
- `ADVANTAGE_MARKET_GOODS_TRADE_CHARTER`
- `ADVANTAGE_MARKET_PRESTIGE_GOODS`

修正名称和说明则在：

`game/localization/english/modifiers_l_english.yml:639`

例如：

```text
state_trade_advantage_mult
state_trade_advantage_from_capacity_add
state_max_trade_advantage_from_capacity_add
country_no_advantage_loss_from_lack_of_interest_bool
```

总结来说：

- **固定 TA 加减项**：`game/common/defines/00_defines.txt`
- **缺乏 Interest 的惩罚及 Interest 等级数值**：`game/common/interest_tier_types/interest_tier_types.txt`
- **Free Trade**：`game/common/laws/00_trade_policy.txt`
- **External Trade**：`game/common/power_bloc_principles/00_power_bloc_principles.txt`
- **Market capital 与 Capacity**：`game/common/static_modifiers/00_code_static_modifiers.txt`
- **Tooltip 显示文本**：`game/localization/english/interfaces_l_english.yml`
- **修正名称**：`game/localization/english/modifiers_l_english.yml`

真正把这些因子组合成最终 Trade Advantage 的逐项计算函数没有以脚本形式暴露在 `game/common` 中，主要位于游戏二进制引擎代码中；本地脚本提供的是常量、修正和 tooltip 接口。