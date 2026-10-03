# `+11FBDA0` 中 Trade Advantage 读取/计算路径

## 结论

该函数目前**没有在仓库中被单独解析出来**。已有资料只解析了它的调用者 `victoria3.exe+11FBDA0`：

- [刷新候选函数](刷新候选函数.md)：给出 `c.advantage = ...` 的骨架和断言。
- [goal3_static_disassembly.md](../goal3_static_disassembly.md)：说明 `+11FBDA0` 的字段写入、调用关系和断言。
- [function_7FF777CEBDA0.md](../../Output/goal3_static_20261002/function_7FF777CEBDA0.md)：是 `+11FBDA0` 连同尾跳评分函数的反汇编，不是一个名为 `ReadOrComputeDirectionalTradeAdvantage` 的已识别函数。

## 当前可确定的伪代码

规范来源：[`FakeCode/trade_advantage_functions.md`](../../FakeCode/trade_advantage_functions.md#readorcomputedirectionaltradeadvantage)。

```cpp
// 功能：读取指定州、商品和贸易方向的绝对贸易优势；缓存不存在时计算并返回。
// 入参：state 为州对象，goods 为商品对象，direction 为进口/出口方向；
// 返回：正的绝对贸易优势，使用游戏内部定点整数单位。
int64 ReadOrComputeDirectionalTradeAdvantage(State* state,
                                             Goods* goods,
                                             uint8 direction)
{
    // direction == 0/1 分别选择两套方向数据；具体枚举名称仍需运行时验证。
    TradeAdvantageTable* table = ResolveTradeAdvantageTable(state, direction);
    int32 goodId = goods->id;

    // 位图先判断该商品在对应表中是否存在，再按商品 ID 读取指针/数值。
    if (!table->contains(goodId))
        return 0;

    int64 advantage = table->values[goodId];
    if (advantage > 0)
        return advantage;

    // +11FBDA0 随后进入方向分支，构造上下文并调用若干贸易/市场辅助函数。
    // 这些调用位于调用者内联路径中，当前证据不足以把它们拆成一个独立 ABI 函数，
    // 因而以下是语义级伪代码，而不是已验证的源码还原。
    TradeContext ctx = BuildDirectionalTradeContext(state, goods, direction);
    int64 computed = ComputeAbsoluteTradeAdvantage(ctx);
    table->values[goodId] = computed;
    return computed;
}
```

在 `+11FBDA0` 的机器码中，前半段可直接确认：

1. `c.quantity` 写入候选 `c+0x38`。
2. 根据 `c+0x08` 的方向选择两套表：方向 0 使用基址附近 `+0x7D0/+0x7E8`，方向 1 使用 `+0x780/+0x798`。
3. 用商品 ID 的位图检查商品是否有效，然后从对应数组读取值并写入 `c+0x40`。
4. 若结果 `<= 0`，才进入后续方向相关计算路径；最终再次写 `c+0x40`，并在 `+11FC00C` 检查其必须大于零。

## 为什么 UI 可以显示负百分比，而这里断言 `advantage > 0`

这里的 `c+0x40` 不是 UI 直接显示的“相对贸易优势百分比”，而是候选计算所需的**绝对贸易优势**。游戏资料明确区分两种量：

- absolute trade advantage：内部用于按商品、方向和贸易量进行竞争计算的正值；
- relative trade advantage：本文统一工作模型为 `r = R_share / V_share - 1`；其中 `R_share` 是同商品、同方向的绝对优势乘交易量所得的全球份额，`V_share` 是交易量份额。它不是单纯的优势份额，低于平均单位优势时可为负；UI 精确映射仍需验证。

因此，`assert c.advantage > 0` 不是把 UI 的负百分比简单取绝对值，也没有证据表明这里做了 `abs()` 或 `max(x, 0)`。它约束的是内部绝对量：基础贸易优势在定义中为 100，随后叠加/乘以方向修正；正常候选必须仍为正。负的 `state_*_advantage_mult` 是对该绝对基数的修正，不等同于最终 UI 的相对百分比。

成交价格暂与 [贸易中心模型第 4 节](../vic3_doc_copy/trade_center_model1.md#4-相对优势--成交价统一工作模型尚未源码级确认) 统一：

```text
r = R_share / V_share - 1
M = 1 + 0.25 × r
出口成交价 P_export = P_world × M
进口成交价 P_import = P_world / M
```

这是尚未源码级确认的工作模型，要求 `M > 0`；出口式暂作候选，进口式有主模型中的观测支持。`r = +100% = 1` 时，出口价格提高 `25%`，进口价格降低 `20%`；`0.25` 是本地配置的倍率系数，不是已证实的价格改善上限。官方日志未给出这组精确公式，其价格零和描述与进口倒数模型也尚未闭合，来源和限制见主模型第 4.0 节。

因此 UI 相对百分比和内部绝对表值不是同一标度。当前反汇编尚未追到 UI 格式化函数，不能将以上工作模型当作已还原的 UI 实现；可以确定的是，断言发生在候选内部绝对值写入后、评分计算前。

## 证据边界

`+11FBDA0` 文件覆盖了 1015 条指令，并通过尾跳包含 `+11FC320` 评分函数。若要把上面的语义伪代码提升为逐指令函数，需要继续解析 `+2B96A0`、`+B16630`、`+D16080`、`+D16160`、`+D18B90`、`+EB2350`、`+B17760` 等辅助调用，以及 UI 读取相对优势的调用点；现有仓库没有完成这一步。

## 对 `BuildDirectionalTradeContext` / `ComputeAbsoluteTradeAdvantage` 的追踪

前文两个名称是语义化伪代码名，并不是已经由符号或函数边界确认的两个真实函数。继续按 opcode 追踪后，当前能确认的是：这段逻辑被编译器直接展开在 `+11FBDA0` 内，至少包含下面的调用链。

### 方向 1（`c+0x08 == 1`）

```asm
+11FBE92  xor edx,edx
+11FBE94  lea rcx,[rsp+40]
+11FBE99  call 7FF777EB1A10
+11FBE9F  lea rdx,[rsp+40]
+11FBEA4  call 7FF777D16080
+11FBEA9  movzx r9d,bl          ; 方向
+11FBEAD  mov r8,r12            ; 商品对象
+11FBEB0  lea rdx,[rsp+40]      ; 临时上下文
+11FBEB5  mov rcx,r13           ; 市场/州相关对象
+11FBEB8  call 7FF777D16160
+11FBEBD  lea rdx,[rsp+40]
+11FBEC2  mov rcx,r13
+11FBEC5  call 7FF777D18B90
+11FBECA  lea rdx,[rsp+0xD0]
+11FBED2  lea rcx,[rsp+40]
+11FBED7  call 7FF777EB2350
+11FBEDC  mov qword ptr [rsp+0xC0],0x186A0
+11FBEF0  cmp qword ptr [rax],0x186A0
+11FBEF7  cmovg rbx,rax
+11FBEFB  mov rbx,[rbx]
+11FBEFE  lea rcx,[rsp+78]
+11FBF03  call 7FF777738D10
+11FBF08  lea rcx,[rbp+0x778]
+11FBF0F  jmp 7FF777CEBF8D
+11FBF8D  mov r8,rbx
+11FBF90  mov rdx,r12
+11FBF93  call 7FF777B17760
```

### 方向 0（`c+0x08 == 0`）

方向 0 使用完全对应的一组调用，差异是 `+11FBF28 xor r9d,r9d`，即把方向参数置为 0；随后同样经过 `+EB2350`、`+738D10`，最后调用 `+B17760`：

```asm
+11FBF11  xor edx,edx
+11FBF13  lea rcx,[rsp+40]
+11FBF18  call 7FF777EB1A10
+11FBF1E  lea rdx,[rsp+40]
+11FBF23  call 7FF777D16080
+11FBF28  xor r9d,r9d
+11FBF2B  mov r8,r12
+11FBF2E  lea rdx,[rsp+40]
+11FBF33  mov rcx,r13
+11FBF36  call 7FF777D16160
+11FBF3B  lea rdx,[rsp+40]
+11FBF40  mov rcx,r13
+11FBF43  call 7FF777D18B90
+11FBF48  lea rdx,[rsp+0xD0]
+11FBF50  lea rcx,[rsp+40]
+11FBF55  call 7FF777EB2350
+11FBF5A  mov qword ptr [rsp+0xC0],0x186A0
+11FBF6E  cmp qword ptr [rax],0x186A0
+11FBF75  cmovg rbx,rax
+11FBF79  mov rbx,[rbx]
+11FBF7C  lea rcx,[rsp+78]
+11FBF81  call 7FF777738D10
+11FBF86  lea rcx,[rbp+0x7C8]
+11FBF8D  mov r8,rbx
+11FBF90  mov rdx,r12
+11FBF93  call 7FF777B17760
```

### 各调用的已知作用边界

| 地址 | 当前能从调用点确认的作用 | 对两个伪代码名的归属 |
|---|---|---|
| `+EB1A10` | 以 `rcx=&stack+0x40`、`edx=0` 初始化一个临时对象 | `BuildDirectionalTradeContext` 的初始化步骤 |
| `+D16080` | 接收同一临时对象地址，继续解析/填充上下文 | 上下文构造步骤 |
| `+D16160` | 参数为上下文、商品对象和方向值；是方向/商品相关的核心填充调用 | 上下文构造步骤 |
| `+D18B90` | 再次以市场对象和临时上下文为参数补充数据 | 上下文构造步骤 |
| `+EB2350` | 输入临时上下文，输出到 `[rsp+0xD0]`，返回 `rax` 指向定点数候选 | 计算前的聚合/规范化步骤 |
| `+738D10` | 接收 `&rsp+0x78`，其结果随后只用于选择 `[rbp+0x778]` 或 `[rbp+0x7C8]` | 方向数据/修正读取步骤 |
| `+B17760` | `rcx` 为方向相关表项，`rdx=goods`，`r8=rbx` 为前面选出的定点值；调用后回到缓存读取路径 | 最接近 `ComputeAbsoluteTradeAdvantage` 的实际计算调用 |

这里的 `0x186A0` 是 `100000` 定点比例。`+EB2350` 返回的值会与 `100000` 比较并取较大者，再传给 `+B17760`。因此可以把语义伪代码更新为：

```cpp
// 功能：按方向和商品构造贸易优势计算上下文，并调用内部优势计算器。
// 入参：market/state、goods、direction；返回：定点绝对贸易优势或写回缓存。
int64 ComputeDirectionalAdvantage(state, goods, direction)
{
    TempContext t{};
    InitContext(&t, 0);                         // +EB1A10
    ResolveContext(&t);                         // +D16080
    FillGoodsDirectionContext(market, &t, goods, direction); // +D16160
    ExtendMarketContext(market, &t);            // +D18B90
    int64 normalized = max(100000, ExtractValue(&t)); // +EB2350
    normalized = SelectFixedPoint(&normalized);  // +738D10
    return ComputeOrStoreAdvantage(directionTable, goods, normalized); // +B17760
}
```

BuildDirectionalTradeContext
ComputeAbsoluteTradeAdvantage
两个被伪代码解释二合一
->
ComputeDirectionalAdvantage


### 目前不能确认的部分

- 这些目标函数的独立函数入口、完整 opcode 和返回结构尚未采集，因此不能把它们分别命名为已完成反汇编的 `BuildDirectionalTradeContext` 与 `ComputeAbsoluteTradeAdvantage`。
- `+B17760` 的调用点明确表明它使用方向表、商品对象和一个至少为 `100000` 的定点值，但其是否直接返回最终 `c+0x40`，或只是更新表缓存，仍需单独导出该地址的函数图才能确定。
- 所以更准确的结论是：前文两个伪代码函数对应的是 `+11FBDA0` 内的一段**内联计算链**；目前已追到调用边界和定点下限，尚未取得两个独立函数的完整实现。

## 本轮继续追踪结果：不能把调用目标当作已解析函数

对当前仓库的全部 `Output`、opcode 报告和脚本再次检索后，没有发现以下目标地址的独立函数导出：

```text
7FF777EB1A10  (+11? 相对模块基址的目标调用)
7FF777D16080
7FF777D16160
7FF777D18B90
7FF777EB2350
7FF777738D10
7FF777B17760
```

现有唯一的机器码证据仍然是 `function_7FF777CEBDA0.md` 中的调用点。也就是说，当前可以继续确认调用约定和数据流，但不能凭调用者一侧的 opcode 推出目标函数内部的逐条 opcode。尤其不能把 `+B17760` 直接写成“返回最终优势”的实现；调用点只证明它收到：

```text
rcx = [rbp+0x778]（方向 1）或 [rbp+0x7C8]（方向 0）
rdx = r12 = 商品对象
r8  = max(100000, *返回自 +EB2350 的指针)
```

随后程序回到 `+11FBF98` 的第二次商品表读取路径，并最终把表值写入 `c+0x40`。因此当前最严谨的作用描述是：

```cpp
// +B17760：以方向表、商品对象和定点输入执行/更新贸易优势相关缓存。
// 返回值和是否直接写缓存尚未由目标函数本体确认。
AdvantageIntermediate B17760(DirectionTable* table,
                              Goods* goods,
                              int64 fixedInput);
```

同理，`+EB1A10` 至 `+EB2350` 只能称为临时上下文的初始化、填充和归一化调用链。若要获得这两个伪代码函数的“实际 opcode”，下一步必须在同一版本、同一模块基址下通过 `code_disassemble` 或 `code_get_function` 单独导出上述七个入口；现有静态文件没有这些目标的函数体，不能继续从 `+11FBDA0` 文件中推导。

## 已采集目标函数 opcode（2026-10-02）

本轮通过 CE 只读 `code_disassemble` 采集了 7 个目标入口，原始窗口保存在 [trade_advantage_opcode_20261002](../../Output/trade_advantage_opcode_20261002) 下：

| 地址 | 采集结果 | 当前识别 |
|---|---|---|
| `+EB1A10` | 成功，入口 `7FF777EB1A10` | 初始化贸易优势计算临时上下文 |
| `+D16080` | 成功，入口 `7FF777D16080` | 构造/清理数值上下文对象 |
| `+D16160` | 成功，入口 `7FF777D16160` | 读取州/商品/方向数据并做定点合成 |
| `+D18B90` | 成功，入口 `7FF777D18B90` | 构造市场/州修正查询上下文，含 `TRADE_FRACTION` |
| `+EB2350` | 成功，入口 `7FF777EB2350` | 对上下文数值做定点乘法、插值和边界处理 |
| `+738D10` | 成功，入口 `7FF777738D10` | 管理缓存/资源句柄；不是优势公式本体 |
| `+B17760` | 成功，入口 `7FF777B17760` | 商品 ID 对应缓存的读取、失效和写回 |

### `+EB1A10`：临时上下文的真实字段

入口 opcode 直接初始化 `rcx` 指向的对象：

```asm
mov [rcx+00],0
mov [rcx+08],0
mov [rcx+10],0
mov qword ptr [rcx+18],000186A0       ; 100000
mov [rcx+20],8000000000000000         ; INT64_MIN
mov [rcx+28],7FFFFFFFFFFFFFFF         ; INT64_MAX
mov [rcx+30],0
mov [rcx+31],dl                       ; 调用者传入的模式/方向标志
```

这证明临时对象至少包含：三个 64 位累加/结果槽（`+00/+08/+10`）、定点比例 `+18`、最小/最大边界 `+20/+28`、状态字节 `+30` 和调用模式字节 `+31`。当 `dl==1` 时，函数还从全局对象取得资源；调用者在 `+11FBE99/+11FBF18` 传入 `edx=0`，所以这两个路径都使用“非 1 模式”。

### `+D16080`：把上下文包装为数值计算对象

入口先把 `rdx` 保存的临时上下文复制/包装到栈对象，并写入虚表/类型指针 `[rsp+0x30]`、`[rsp+0x40]`；随后调用 `+6DE750`。函数尾部检查内部字符串/小对象长度（`<=0xF` 的短对象路径，否则释放堆对象），然后返回。它本身没有商品或州字段的直接读取，也没有最终优势乘法；作用是建立可供后续值计算器使用的多态上下文。

### `+D16160`：州对象、商品对象和方向参数的核心合成

入口首先保存参数：

```asm
mov [rsp+08],rcx       ; market/state 相关对象
mov [rsp+10],rdx       ; 临时上下文
mov [rsp+18],r8        ; goods 对象
mov [rsp+20],r9b        ; direction
```

随后关键路径读取：

```asm
call +2C7550
mov r14,[rax+120]
add r14,508             ; 取全局/市场数据表
mov r13,[r15+18B0]      ; 从 state 取得关联修正/市场对象
...
call +D16080            ; 包装上下文
...
mov [rsp+0xB0],0x186A0  ; 默认定点 100000
cmp qword ptr [rcx],0x186A0
cmovg rax,rcx
mov [r14],rax           ; 输出至少为 100000 的定点值
call +738D10            ; 资源/缓存句柄处理
```

函数中大量出现 `imul ...; sar ...,0xE; idiv rbx` 以及 `imul ...,0x186A0`，说明它把多个有符号定点量按比例插值后相加，而不是直接读取一个百分数。`r15+0x18B0` 是明确的州侧关联对象来源；`r8` 是商品对象；`r9b` 是方向。因此上下文确实同时包含州/市场、商品和方向信息。

### `+D18B90`：贸易市场修正上下文

该函数入口保存 `rcx` 为市场/州对象，`rdx` 为临时上下文，并从 `[rcx+0x18B0]` 取得共享市场对象。早期构造字段中出现 `TRADE_FRACTION` 字符串，并在后续数值路径将结果写入 `[rbp+0x58]`。`+D18B90` 后半段使用 64 位乘法、高位取整和 `0x186A0` 缩放，产生供上层使用的市场贸易份额/修正值。它不是单纯的州名称读取函数，而是将州关联市场状态转换成贸易优势计算的定点输入。

### `+EB2350`：定点插值公式已可确认

该函数不是简单 getter。入口读取上下文中的 `+0x10` 槽并加上 `0x186A0`，随后有两套对称的溢出安全计算。核心数学形态是对两个端点 `a`、`b` 和比例 `p` 做定点线性插值：

```text
result = a + ((b - a) * p) / 100000
```

汇编通过 `imul`、`sar 0x0E`、符号修正和 `idiv` 拆分计算，以避免 64 位乘法溢出；`0x186A0` 就是比例分母。调用者随后再次执行 `max(result, 100000)`。因此这里的 `computed` 不是“百分比字符串”，而是经过定点插值和下限保护的绝对数值。

### `+B17760`：实际是商品缓存写回器，不是优势公式

此函数的入口 opcode 已完整采集。关键路径是：

```asm
movsxd rsi,dword ptr [rdx+10]    ; goods->id
mov rdi,rcx                       ; 方向表/缓存对象
mov rbx,r8                        ; 输入定点值
call +B16630                      ; ID 有效性检查
...
test [rdi + (id>>6)*8 + 0x20], bit
mov [rdi+8][id], rbx              ; 写入 values[id]
and bitmap, ~bit                   ; 清除旧失效标记
...
call +B16700                      ; 另一种缓存/失效路径
mov [rdi+8][id],rbx
bts bitmap,bit                     ; 标记已计算
```

函数末尾还根据 `[rdi+0x30]`、`[rdi+0x3C]` 管理块状缓存，并可能调用 `+AC6D4C0`。所以 `+B17760` 的真实作用是“按商品 ID 缓存/失效/写回一个已经计算好的值”；它不包含 Trade Advantage 的完整经济公式。

## 当前能写出的更准确公式与边界

把上述真实调用合并后，`+11FBDA0` 的优势路径应改写为：

```cpp
// 功能：构造州/市场/商品/方向上下文，并把定点优势中间值写入方向商品缓存。
// 入参：state/market、goods、direction；返回：缓存中的绝对优势定点值。
int64 ComputeAbsoluteTradeAdvantage(State* state, Goods* goods, uint8 direction)
{
    TempContext t;
    InitTempContext(&t, /*mode=*/0);                 // +EB1A10
    WrapNumericContext(&t);                          // +D16080
    int64 stateGoodsDirection =
        BuildStateGoodsDirectionValue(state, goods, direction, &t); // +D16160
    int64 marketTradeFraction =
        BuildMarketTradeFraction(state, &t);         // +D18B90
    int64 interpolated = InterpolateFixedPoint(
        stateGoodsDirection, marketTradeFraction, t.scale = 100000); // +EB2350
    int64 normalized = max(interpolated, 100000);
    UpdateDirectionalGoodsCache(direction, goods, normalized); // +B17760
    return normalized;
}
```

可以确定的数学事实：

1. 中间值使用 `100000` 定点比例。
2. 至少有线性插值 `a + (b-a)*p/100000`，并使用溢出安全的拆分乘除。
3. 调用者在缓存写回前强制 `max(value, 100000)`，因此最终绝对优势基线为 `1.0`，不会因为 UI 的负相对百分比而变成负数。
4. `+D18B90` 引入 `TRADE_FRACTION` 等贸易市场份额数据；`+D16160` 明确读取州关联对象 `[state+0x18B0]`、商品对象和方向字节。

尚不能从本轮单独入口 opcode 唯一确定的内容：各个 `+2A.../+6D.../+AC...` 辅助函数所代表的具体游戏字段名称、每个修正项的加法/乘法顺序，以及 UI 相对优势百分比的最终归一化公式。文档中的 `BuildStateGoodsDirectionValue` 和 `BuildMarketTradeFraction` 是基于寄存器与字符串证据的分析命名，不是官方符号。

## `stateGoodsDirection` 与 `marketTradeFraction` 的业务含义推测

### `stateGoodsDirection`

这个中间量最合理的业务解释是：**某州/市场对指定商品、指定方向的绝对贸易优势输入**。它不是最终 UI 百分比，也不是单独的州属性。依据如下：

1. `+D16160` 的真实入口把 `rcx`、`rdx`、`r8`、`r9b` 保存为四个参数；在 `+11FBDA0` 调用点分别对应市场/州对象、临时上下文、商品对象和方向。
2. 函数从 `[state+0x18B0]` 读取州关联市场/修正对象，并通过商品对象参与后续计算。
3. 方向参数直接进入上下文；方向 0/1 会导致后续选择不同的贸易数据表。
4. 计算过程中大量使用 `100000` 定点比例和有符号乘除，结果随后经过 `max(value,100000)`，这符合“绝对优势至少为基础值 1.0”的语义。

因此，`stateGoodsDirection` 可以理解为基础优势与州、商品、方向修正合成后的定点量，例如：

```text
stateGoodsDirection ~= BaseAdvantage
                    + State/Market factors(goods, direction)
                    + Direction-specific modifiers
```

这里的 `~=` 是语义近似；当前 opcode 还不能把每一个加数准确映射到脚本中的 `state_trade_advantage_mult`、`state_import_advantage_mult` 或 `state_export_advantage_mult`。

### `marketTradeFraction`

这个中间量最合理的解释是：**州所属市场在该商品/方向上的贸易份额或贸易比例修正**。这是比 `stateGoodsDirection` 更接近“份额”的量，依据是：

1. `+D18B90` 的机器码引用了明确字符串 `ADVANTAGE_ENTRY_IMPORT_SUFFIX`、`ADVANTAGE_ENTRY_EXPORT_SUFFIX` 和 `TRADE_FRACTION`。
2. 函数从 `[state+0x18B0]` 取得共享市场对象，之后把一个结果写入 `[rbp+0x58]`。
3. 后续使用 64 位乘法、高位取整、`0x186A0` 缩放，符合“把贸易份额/比例转成定点值”的实现方式。
4. 该值随后由 `+EB2350` 与另一个端点/上下文槽做定点插值，而不是直接作为最终优势写入候选。

但必须区分“贸易份额”与“全球相对优势”：`TRADE_FRACTION` 字符串证明它是一个贸易比例字段或值计算器属性，不能单凭字符串证明它就是 UI 中显示的 relative trade advantage。

## 两个获取函数的实际算法边界

### `+D16160` 的可还原算法

从现有 opcode 可以还原出以下结构，而不是完整的经济公式：

```cpp
// 功能：从州/市场、商品和方向构造绝对优势候选值。
// 入参：stateOrMarket、temp、goods、direction；返回：写入临时/输出对象的定点值。
int64 BuildStateGoodsDirectionValue(StateOrMarket* stateOrMarket,
                                    TempContext* temp,
                                    Goods* goods,
                                    uint8 direction)
{
    MarketData* global = ResolveGlobalMarketData(); // +2C7550，后续取 [global+0x120]+0x508
    StateMarketRef* ref = stateOrMarket->field_18B0;

    WrapNumericContext(temp);                       // +D16080
    int64 x = ReadGoodsDirectionFactors(ref, goods, direction); // 内部多个辅助调用
    int64 y = ReadMarketOrStateFactors(ref, temp);
    int64 combined = FixedPointCombine(x, y, 100000);

    // 调用路径中明确存在下限保护。
    return max(combined, 100000);
}
```

`+D16160` 中可确认的数学形态包括：

```text
q = (a * b) / scale
r = (remainder * scale) / divisor
result = q + r + other_terms
```

这些分支用 `imul`、`cqo`、`idiv`、符号修正和溢出阈值常量实现 128 位中间精度。它们证明这是定点经济数值合成，不足以证明某一项就是“州生产占比”或“关税”。

### `+D18B90` 的可还原算法

该函数更像贸易份额值计算器的构造/评估过程：

```cpp
// 功能：从州关联市场对象读取贸易份额相关输入，并生成定点修正值。
// 入参：stateOrMarket、temp；返回：写入临时结果对象的贸易份额/修正值。
int64 BuildMarketTradeFraction(StateOrMarket* stateOrMarket,
                               TempContext* temp)
{
    SharedMarket* market = stateOrMarket->field_18B0;
    ValueEntry entry = ResolveValueEntry(market,
        direction == 0 ? "ADVANTAGE_ENTRY_IMPORT_SUFFIX"
                       : "ADVANTAGE_ENTRY_EXPORT_SUFFIX");
    ValueEntry fraction = ResolveValueEntry(entry, "TRADE_FRACTION");

    int64 numerator = ReadMarketTradeNumerator(fraction);
    int64 denominator = ReadMarketTradeDenominator(fraction);
    int64 scaled = SafeFixedDivide(numerator * 100000, denominator);
    temp->marketFraction = scaled;
    return scaled;
}
```

其中 `direction` 在 `+D18B90` 内不一定以裸字节直接出现，而可能已经编码在调用者构造的 value entry 中；所以导出的伪代码把方向选择标作语义层行为，不能视为逐指令等价代码。当前能确认的是 import/export 两个入口后缀和 `TRADE_FRACTION` 属性名，而不是 numerator/denominator 的具体字段偏移。

## 两者的关系

更稳妥的组合模型是：

```text
stateGoodsDirection = 州/市场 + 商品 + 方向的绝对优势候选
marketTradeFraction = 相关市场贸易份额/比例修正
computed = FixedPointInterpolate(stateGoodsDirection,
                                 marketTradeFraction,
                                 scale=100000)
computed = max(computed, 100000)
```

这能解释为什么同一商品在进口与出口方向有不同值，也能解释为什么州所属市场的信息会同时进入上下文。它还解释了 `assert c.advantage > 0`：候选中保存的是经过基线保护的绝对定点量，而 UI 显示的负百分比属于之后的相对化/价格显示层。

当前不能确认的内容包括：

- `stateGoodsDirection` 是否直接包含 Trade Center 等级、市场面积生产/消费比例、兴趣、贸易协定、关税或补助中的哪几项；
- `marketTradeFraction` 的精确分子、分母和方向选择字段；
- `+D16160` 中各个隐藏辅助调用返回值的脚本属性名称；
- UI relative advantage 的归一化和正负显示公式。

因此，这两个业务名称和上面的公式已经比原始占位名更接近真实含义，但仍应标记为“高可信语义推测”，不能当作完整源代码还原。

## 进一步校正：两者不是两个并列的最终数值

结合已采集的真实调用顺序，需要对前面的命名作一个重要修正：`stateGoodsDirection` 和 `marketTradeFraction` 更可能不是两个已经分别返回的、可直接相加的业务字段，而是同一个数值表达式上下文中的**不同阶段结果**。

`+D16160` 的调用约定是：

```text
rcx = 市场/州相关对象
rdx = 调用者提供的临时对象
r8  = 商品对象
r9b = 方向
```

入口先把这些参数保存到栈上，随后执行 `+2C7550`、`+D16080`、`+D18B90` 等调用，并在返回前把定点结果写入由 `rdx` 指向的对象。也就是说，调用者中的：

```cpp
int64 stateGoodsDirection = BuildStateGoodsDirectionValue(...); // +D16160
int64 marketTradeFraction = BuildMarketTradeFraction(...);      // +D18B90
```

是为了说明数据流而写的分析变量；真实机器码并没有显示两个独立的 C++ 返回值。`+D18B90` 是 `+D16160` 内部使用的辅助构造/评估步骤之一，不能证明它向 `+11FBDA0` 单独返回一个名为 `marketTradeFraction` 的值。

### 更可信的业务解释

#### `stateGoodsDirection`

仍可保留“州/市场、商品、方向相关的绝对优势候选”这一解释，但应理解为 `+D16160` 写入临时上下文后的**综合定点中间状态**，可能包含：

- 州对象通过 `[state+0x18B0]` 关联到的市场/修正容器；
- 商品对象中的商品 ID 和商品相关数值；
- 方向 0/1 对应的进口/出口入口；
- 从上下文取出的定点边界、比例和市场值。

当前没有足够证据把它收窄成“州生产量”或“州贸易中心等级”。

#### `marketTradeFraction`

`TRADE_FRACTION`、`ADVANTAGE_ENTRY_IMPORT_SUFFIX` 和 `ADVANTAGE_ENTRY_EXPORT_SUFFIX` 说明 `+D18B90` 会构造一个与贸易方向和贸易比例有关的 value entry。更稳妥的说法是：它提供**优势计算表达式所需的市场贸易比例输入**，而不是已经确定的“该州占全球贸易的最终份额”。

尤其要注意：`+D18B90` 末尾把结果写入其自身栈帧中的 `[rbp+0x58]`，随后构造数值对象并返回；没有证据显示这个槽位直接就是 UI 的 relative trade advantage。

### 更准确的算法模型

根据 `+D16160`、`+D18B90` 和 `+EB2350` 的数据流，当前最保守的模型是：

```cpp
// 功能：构造方向贸易优势表达式并输出定点绝对优势候选。
// 入参：stateOrMarket、goods、direction；返回：写入输出/缓存的定点结果。
int64 BuildDirectionalAdvantage(StateOrMarket* stateOrMarket,
                                Goods* goods,
                                uint8 direction)
{
    TempContext t;
    InitTempContext(&t, 0);                         // +EB1A10
    WrapNumericContext(&t);                         // +D16080

    // +D16160：把州/市场、商品、方向放入一个值计算上下文。
    // +D18B90：在该上下文内解析 import/export advantage entry 和 TRADE_FRACTION。
    PopulateStateGoodsDirectionContext(stateOrMarket, goods, direction, &t);
    PopulateMarketTradeFractionContext(stateOrMarket, &t);

    // +EB2350：对上下文中的两个端点/槽位进行定点插值或组合。
    int64 value = EvaluateFixedPointExpression(&t);
    return max(value, 100000);
}
```

对应的数学形态仍可以写成：

```text
value = Evaluate(
    state/market inputs,
    goods input,
    direction-specific advantage entry,
    TRADE_FRACTION,
    fixed-point scale = 100000
)
value = max(value, 100000)
```

目前不能把它严格化成：

```text
stateGoodsDirection + marketTradeFraction
```

也不能确认是：

```text
stateGoodsDirection * marketTradeFraction / 100000
```

因为 `+EB2350` 的两个输入端点来自临时对象和 value entry 的内部槽位，单靠调用者侧寄存器无法唯一确定它们分别对应哪个业务字段。已确认的是定点比例、方向入口、贸易比例属性和最终正值下限；未确认的是每个槽位的业务字段映射以及所有修正项的加法/乘法顺序。
