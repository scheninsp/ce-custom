# 贸易候选与州调整伪代码

本文件集中保存 Docs 中已出现的贸易候选相关伪代码。地址均为 `victoria3.exe+相对地址`；函数名为分析命名，不代表游戏符号。

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

