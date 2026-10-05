# 贸易候选与州调整伪代码

本文件集中保存 Docs 中已出现的贸易候选相关伪代码。地址均为 `victoria3.exe+相对地址`；函数名为分析命名，不代表游戏符号。

## MakeCandidate：内联候选初始化

沿用 Docs 已有的 MakeCandidate 命名，无独立 ABI 入口；对应减少选择函数 victoria3.exe+122AC50 内的 +122AE7A..+122AEB5，以及增加选择函数 victoria3.exe+122B320 内的 +122B501..+122B534。
此处仅初始化候选，Refresh(+11FBDA0) 是之后的独立调用。字段名结合 Refresh 和收益/短缺计算的读写恢复。

```cpp
// 功能：抽象两个选择函数内联的候选初始化，不包含 Refresh。
// 入参：state 为州对象；goods 为商品对象；direction 为方向字节（0/1）；
//       mode 为评估模式（0=减少，1=增加）。
// 返回值：约 0x48 字节的候选布局视图；数值计算字段初始均为零。
// 地址：减少路径 victoria3.exe+122AE7A..+122AEB5；
//       增加路径 victoria3.exe+122B501..+122B534；无独立函数入口。
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

减少侧从已截断为整数的带符号容量取得方向（正值 1，负值 0），mode=0；增加侧枚举方向 0/1，mode=1。stateRef 来自州对象 +08；两侧寄存器分别为 R14/R13，均由入口 RCX 保存。Refresh(+11FBDA0) 在 +11FBDBD/+11FBDC1 将候选 +28 传入 Resolve(+7C96A0)。0=进口、1=出口是现有业务分析的高可信映射，不作为独立运行时验证结果。

指令来源：[减少](../../Output/2026-10-3-process1/goal3_static_20261002/function_7FF777D1AC50.md)、[增加](../../Output/2026-10-3-process1/goal3_static_20261002/function_7FF777D1B320.md)、[Refresh](../../Output/2026-10-3-process1/goal3_static_20261002/function_7FF777CEBDA0.md)。

## PassCountryAndMarketFilters：内联过滤

此名称沿用候选准备文档。国家对象在商品循环前解析；列表过滤位于循环内。字段名仅表达偏移，不认定列表为禁运或已有贸易列表。

```cpp
// 功能：概括增加候选中的国家商品资格过滤；不是独立 ABI 函数。
// 入参：goods 为商品对象；state 为州对象。
// 返回值：通过过滤为 true；否则为 false。
// 地址：victoria3.exe+122B37E..+122B3D7、+122B440..+122B495。
function PassCountryAndMarketFilters(goods, state):
    // Resolve(+7B0AB0) 解析国家，+7C0380 解析市场。
    if state.field_11B8 != 0 and state.ref_B48 != 0xFFFFFFFF:
        associated = call_address(+7C33B0, address_of(state.ref_B48))
        marketRef = associated.field_10
    else:
        owner = call_address(+7B0AB0, address_of(state.ref_E48))
        marketRef = owner.field_9D4
    market = call_address(+7C0380, address_of(marketRef))
    country = call_address(+7B0AB0, address_of(market.ref_848))

    // 数组属于国家对象；列表业务名称尚未由写入点确认。
    if state.field_11B8 == 0:
        for index in [0, country.count_2414):
            if country.goodsPointers_2408[index] == goods:
                return false

    // +C34A80 是真实调用；限制条目的具体业务类型仍需确认。
    return call_address(+C34A80, country, goods)
```

来源：[增加候选反汇编](../../Output/2026-10-3-process1/goal3_static_20261002/function_7FF777D1B320.md)。`call_address` 为原始 RVA 调用记法，不代表独立函数命名。

## `CalculateQuantityPerCapacity`（`victoria3.exe+122AB50`）

```cpp
// 功能：计算刷新候选时，指定州对指定商品产生的单位交易数量。
// 入参：state 为州对象，goods 为商品对象；返回：应用下限后的单位交易数量。
// 地址：victoria3.exe+122AB50
int64 CalculateQuantityPerCapacity(byte* state, byte* goods)
{
    const int64 SCALE = 100000;
    int64 base = ReadGoodsBaseQuantity(goods);
    int64 modifier = ReadStateGoodsModifier(state, goods, 0x97);
    int64 adjusted = FixedMultiply(base, modifier + SCALE);
    int64 minimum = ReadGlobalMinimumGoodsTradedQuantity();
    return adjusted < minimum ? minimum : adjusted;
}
```

## `RefreshQuantityFragment`（`victoria3.exe+11FBDC9` 调用点）

```cpp
// 功能：说明刷新候选时数量字段的实际写回过程，仅展示相关片段。
// 入参：candidate 为候选对象，resolvedState 为已解析的州指针；返回：无。
// 地址：调用点位于 victoria3.exe+11FBDC9..+11FBDDF。
void RefreshQuantityFragment(byte* candidate, byte* resolvedState)
{
    int64 temporaryQuantity;
    byte* goods = ReadPointer(candidate + 0x00);
    int64* result = CalculateQuantityPerCapacity(resolvedState, goods);
    WriteInt64(candidate + 0x38, *result);
}
```

## `ExecuteTickTask`（`victoria3.exe+7B81E0`）

```cpp
// 功能：准备并执行一个 Tick 任务的多阶段回调。
// 入参：gameState 为游戏状态，task 为 Tick 任务；返回：未识别业务返回值。
// 地址：victoria3.exe+7B81E0。
function ExecuteTickTask(gameState, task):
    context = EmptyContext(gameState)
    WithHiddenLogicAccess(task.Prepare(context))
    while context.rangeCallback or context.singleCallback:
        ExecuteCallbacks(context)
    return context.result
```

## `CallbackAdapter_7C49D0`（`victoria3.exe+7C49D0`）

```cpp
// 功能：将通用回调转交给其持有对象。
// 入参：callback 为回调对象，context 为执行上下文；返回：被调函数的结果。
// 地址：victoria3.exe+7C49D0。
function CallbackAdapter_7C49D0(callback, context):
    owner = callback.field08
    return owner.vfunc38(context)
```

