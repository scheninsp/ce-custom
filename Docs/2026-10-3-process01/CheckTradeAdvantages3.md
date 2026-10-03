# Trade Advantage 数学计算流程

## 1. 符号和定点常量

| 符号 | 含义 | 参考地址/来源 |
|---|---|---|
| `S = 100000` | 贸易优势层的中性定点值 | `+13C1A10`、`+11FBEF0`、`+13A3B10` |
| `B = 100` | Trade Center 基础绝对优势 | `00_defines.txt`：`TRADE_CENTER_ADVANTAGE_BASE` |
| `P = 0.25` | 相对优势对价格的影响系数 | `00_defines.txt`：`TRADE_CENTER_ADVANTAGE_PRICE_MULTIPLIER` |
| `TA_i` | 第 `i` 个贸易中心的单位绝对优势 | `+11FBDA0` / `c+0x40` |
| `Q_i` | 第 `i` 个贸易中心的贸易量 | `+11FBDA0` / `c+0x38` |

游戏代码使用定点数保存部分中间结果：

```text
Fixed(x) = x × S
Real(x)  = Fixed(x) / S
```

`+13C2350` 中还存在 `sar ..., 0xE` 的通用定点乘除缩放；它是底层算术实现细节，不改变下面的业务公式。

## 2. 单位绝对优势

### 2.1 基础公式

对某个贸易中心、商品和贸易方向：

```text
TA_raw = B + Σ AdvantageContribution_k
```

其中：

```text
B = 100
```

已知贡献项及定义常量：

```text
市场区域生产贡献
    = 200 × 对应市场生产/全球生产比例

公司特许贡献
    = 50 × 对应公司生产比例

市场声望商品贡献
    = 100 × 对应声望商品比例

贸易协议贡献
    = 100 × 对应贸易协议贸易比例

条约港贡献
    = 200 × 对应条约港贸易比例

禁运贡献
    = -100 × 对应禁运贸易比例

战争贡献
    = -75 × 对应战争贸易比例
```

常量来源：

```text
TRADE_CENTER_ADVANTAGE_BASE = 100
TRADE_CENTER_ADVANTAGE_MARKET_AREA_PRODUCTION_FACTOR = 200
TRADE_ADVANTAGE_COMPANY_CHARTER_FACTOR = 50
TRADE_CENTER_ADVANTAGE_MARKET_PRESTIGE_GOOD_FACTOR = 100
TRADE_CENTER_ADVANTAGE_TRADE_AGREEMENT_FACTOR = 100
TRADE_CENTER_ADVANTAGE_TREATY_PORT_FACTOR = 200
TRADE_CENTER_ADVANTAGE_EMBARGO_FACTOR = -100
TRADE_CENTER_ADVANTAGE_AT_WAR_FACTOR = -75
```

来源函数和伪代码对应关系：

| 数学步骤 | 函数入口 | 伪代码对应关系 |
|---|---:|---|
| 读取州/市场/商品/方向输入 | `+1226160` | `BuildDirectionalAdvantageContext` |
| 加入市场贸易比例 | `+1228B90` | `AddMarketTradeFractionToAdvantageContext` |
| 组合各优势贡献 | `+1226160`、`+1228B90` | `ComputeDirectionalAdvantage` 内部上下文构造 |
| 定点乘除、插值、上下界 | `+13C2350` | `NormalizeDirectionalAdvantage` |

当前静态证据可以确认上述贡献项存在，但还不能确认每个贡献项的精确计算顺序和上下文槽位。

### 2.2 定点归一化

绝对优势上下文完成后，进入定点归一化：

```text
TA_fixed = Normalize(TA_raw)
```

`Normalize` 包含：

```text
定点乘法
    → 右移 14 位
    → 定点除法
    → 多个贡献相加
    → 上下界裁剪
```

参考地址：

```text
+13C2350
```

在 `+11FBDA0` 中还执行最低值处理：

```text
TA_fixed_final = max(TA_fixed, S)
```

参考地址：

```text
+11FBEF0 / +11FBF6E
```

### 2.3 绝对优势缓存

最终值写入方向商品缓存：

```text
DirectionTable[direction].Advantage[goodsId] = TA_fixed_final
```

参考地址：

```text
+1027760
```

然后写入候选对象：

```text
candidate->advantage = TA_fixed_final
```

参考地址：

```text
+11FBE60
+11FC008
```

伪代码对应：

```text
ReadOrComputeAbsoluteAdvantage
    = +11FBDA0 内联路径
ComputeDirectionalAdvantage
    = +11FBDA0 内联计算链
```

## 3. 绝对优势到相对优势

### 3.1 加权绝对优势

对同一商品、同一贸易方向的所有贸易中心：

```text
W_i = TA_i × Q_i
```

其中：

```text
TA_i = 第 i 个贸易中心的单位绝对优势
Q_i  = 第 i 个贸易中心的贸易量
```

全体贸易中心的加权优势：

```text
W_total = Σ(W_i)
       = Σ(TA_i × Q_i)
```

总贸易量：

```text
Q_total = Σ(Q_i)
```

静态代码中的 `imul`、`idiv` 和 `imul 0x186A0` 结构，表明该阶段使用定点乘除。

核心入口：

```text
+13A3B10
```

伪代码对应：

```text
ComputeRelativeTradeAdvantage
```

### 3.2 平均绝对优势

按贸易量加权的平均绝对优势：

```text
TA_average = W_total / Q_total
```

即：

```text
TA_average = Σ(TA_i × Q_i) / Σ(Q_i)
```

### 3.3 相对优势比值

某贸易中心的相对优势比值：

```text
RelativeValue_i = TA_i / TA_average
```

展开为：

```text
RelativeValue_i
    = TA_i × Σ(Q_j)
      / Σ(TA_j × Q_j)
```

定点形式：

```text
RelativeValueFixed_i = FixedDivide(TA_i, TA_average)
```

其中中性值为：

```text
RelativeValue = 1
RelativeValueFixed = S = 100000
```

`+13A3B10` 的方向特殊分支会直接产生：

```text
RelativeValueFixed = 100000
```

参考地址：

```text
+13A3B78
+13A3B8C
```

### 3.4 相对优势差值

价格层或显示层可以把中性的相对优势转换为差值：

```text
RelativeDelta_i = RelativeValue_i - 1
```

定点形式：

```text
RelativeDeltaFixed_i = RelativeValueFixed_i - 100000
```

或者根据方向使用相反符号：

```text
RelativeDeltaFixed_i = 100000 - RelativeValueFixed_i
```

直接证据：

```asm
+19438B1  mov eax,000186A0
+19438B6  sub rax,[rbp-80]
```

以及：

```asm
+19439C9  lea rax,[r9-000186A0]
```

因此，正负号由上层方向语义选择，不能只由 `+13A3B10` 单独确定。

## 4. 相对优势到价格

### 4.1 业务层价格公式

定义文件给出：

```text
TRADE_CENTER_ADVANTAGE_PRICE_MULTIPLIER = 0.25
```

价格倍率的业务公式：

```text
PriceMultiplier_i
    = 1 + (RelativeValue_i - 1) × P
```

代入 `P = 0.25`：

```text
PriceMultiplier_i
    = 1 + (RelativeValue_i - 1) × 0.25
```

定点形式：

```text
PriceMultiplierFixed_i
    = S + (RelativeValueFixed_i - S) × 25000 / S
```

这里：

```text
S = 100000
P × S = 25000
```

### 4.2 方向价格修正

`+13A5280` 消费 `+13A3B10` 生成的相对优势值，并根据方向执行不同定点处理：

```text
PriceResult_i
    = ApplyDirectionPriceRule(
        PriceMultiplier_i,
        direction)
```

伪代码对应：

```text
ApplyRelativeAdvantageToPrice
```

函数入口：

```text
+13A5280
```

调用关系已确认：

```text
+13A3460
    → +13A3B10
    → +13A5280

+140A6B0
    → +13A3B10
    → +13A5280

+1943600
    → +13A3B10
    → +13A5280
```

当前只能确认 `direction == 0` 与非零方向进入不同分支，不能仅凭现有静态 opcode 确认哪个数值对应进口、哪个数值对应出口。

### 4.3 进口/出口的业务含义

根据定义文件和既有贸易模型：

```text
出口：相对优势提高时，成交卖价倾向于高于基准价格
进口：相对优势提高时，成交买价倾向于低于基准价格
```

但这是贸易系统的业务语义；`+13A5280` 的完整上下文还包含运行时价格输入和方向对象，因此不能只凭该函数本体写出完整的最终成交价格：

```text
FinalTradePrice
    = WorldOrDomesticBasePrice
      × PriceMultiplier
      + 其他价格、税费或贸易上下文修正
```

其中 `WorldOrDomesticBasePrice` 及后续税费函数不属于目前已经闭合的 `+13A3B10` / `+13A5280` 静态链。

## 5. 函数级完整关系

```text
+11FBDA0
    读取 DirectionTable[direction].Advantage[goodsId]
    │
    ├─ 缓存 > 0
    │    └─ TA_fixed
    │
    └─ 缓存 <= 0
         ├─ +13C1A10：初始化定点上下文
         ├─ +1226080：包装表达式上下文
         ├─ +1226160：构造绝对优势来源
         ├─ +1228B90：加入市场贸易比例
         ├─ +13C2350：归一化/边界处理
         ├─ +11FBEF0：max(value, 100000)
         └─ +1027760：写回绝对优势缓存
              │
              └─ TA_fixed

+13A3460 或 +140A6B0
    └─ +13A3B10
         TA_i、Q_i
         → W_i = TA_i × Q_i
         → W_total = Σ(TA_j × Q_j)
         → Q_total = ΣQ_j
         → TA_average = W_total / Q_total
         → RelativeValue_i = TA_i / TA_average
         │
         └─ +13A5280
              → RelativeDelta = RelativeValue_i - 1
              → PriceMultiplier = 1 + RelativeDelta × 0.25
              → 按方向生成价格修正
```

## 6. 当前结论边界

目前可以完整标注到入口地址的数学链为：

```text
绝对优势：
+11FBDA0
  → +1226160 / +1228B90
  → +13C2350
  → +1027760

相对优势：
+13A3B10

价格修正：
+13A5280
```

可以确认的公式：

```text
TA_raw = 100 + Σ优势贡献
TA_average = Σ(TA_i × Q_i) / ΣQ_i
RelativeValue_i = TA_i / TA_average
RelativeDelta_i = RelativeValue_i - 1
PriceMultiplier_i = 1 + RelativeDelta_i × 0.25
```

仍未完全确认的内容：

1. `+1226160` 内各优势贡献项的精确求和顺序。
2. `+1228B90` 中市场比例的每个具体统计来源。
3. `+13A3B10` 中各寄存器对应的完整对象类型。
4. `+13A5280` 中价格倍率常数 `0.25` 的具体运行时读取位置。
5. 进口/出口方向枚举的具体数值。
6. 价格倍率之后的最终基准价格、税费和成交价函数。

因此，本文件是当前静态证据支持的“纯数学流程版”；相比 `CheckTradeAdvantages2.md`，省略了大部分 opcode 和伪代码，只保留公式、常量、入口地址及其函数对应关系。
