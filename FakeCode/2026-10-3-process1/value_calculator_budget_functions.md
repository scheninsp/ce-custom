# CalculateTradeAdjustmentBudget 依赖的 ValueCalculator 伪代码

以下伪代码来自 2026-10-4 运行时反汇编。定点数的比例单位是 `SCALE=100000`。

```cpp
// 地址：victoria3.exe+AF8ECAC0
// 功能：把一个修正值应用到 ValueCalculator 上下文；mode=1 为加法，mode=2 为定点乘法。
// 入参：ctx 为上下文；value 为定点修正值；mode 为操作码。
// 返回值：无，结果写回 ctx。
void ApplyValueCalculatorOperation(Context* ctx, int64 value, int mode)
{
    switch (mode) {
    case 1:                         // +AF8ECB08 的跳转表分支
        ctx->additive += value;     // [ctx+08] 或 [ctx+10]，本调用路径使用 +10
        return;
    case 2:                         // +AF8ECB1A..+AF8ECB65
        ctx->factor = FixedMultiply(ctx->factor, value);
        return;
    case 3:                         // 其他路径使用的上下界/选择操作
    case 4:
    case 5:
        ApplyBoundOperation(ctx, value, mode);
        return;
    default:
        return;
    }
}

// 地址：victoria3.exe+B0072350
// 功能：求 ValueCalculator 节点链的定点结果。
// 入参：node 为节点链根；out 为结果写入地址。
// 返回值：返回 out。
ValueNode* EvaluateValueCalculator(ValueNode* node, int64* out)
{
    int64 additive = node->field10 + SCALE;
    int64 value = node->field00 + node->field08;
    int64 result = FixedMultiply(value, additive);
    // +B007246B..+B0072576 继续处理 child(+20)、op(+28) 和 endpoint(+18)，
    // 溢出时选择上下端点；最后把结果写入 out。
    result = EvaluateChildrenAndBounds(node, result);
    *out = result;
    return node;
}

// 地址：victoria3.exe+12295A0
// 功能：计算州贸易调整预算。
// 入参：state 为州对象。
// 返回值：每周可执行的贸易调整次数。
int CalculateTradeAdjustmentBudget(State* state)
{
    if (!TradeAdjustmentPrerequisite(state))
        return 0;

    Context ctx = MakeValueCalculatorContext(); // +B0071A10，ctx.factor=SCALE
    uint16 selector = *(uint16*)(exe + 0x2E86F9C); // 指令标记 [0099]
    if (selector != 0xFFFF) {
        int64 modifier = ReadStateModifierThroughValueCalculator(state, selector, SCALE);
        ApplyValueCalculatorOperation(&ctx, modifier, 1); // +AF8ECAC0：ADD

    int64 internationalMarketAccess = ReadStateInternationalMarketAccess(state); // state+0x68
        if (internationalMarketAccess < SCALE)
            ctx.factor = FixedMultiply(ctx.factor, internationalMarketAccess); // +AF89ECB0：FACTOR
    }

    int64 x;
    EvaluateValueCalculator(BuildRootNode(&ctx), &x); // +B0072350
    int q = trunc_toward_zero(x / SCALE);             // +1229BAD..+1229BC5
    return max(1, q);                                 // +1229BC8..+1229BCB
}
```

`FixedMultiply(a,b)` 是 `trunc_toward_zero(a*b/100000)`；乘积可能溢出时，机器码先取较大端点的商和余数，再计算余数乘较小端点，以保持同一结果。`+AF8ECAC0` 的跳转表证明预算上下文至少有“加法累计值”和“定点倍率”两个独立槽位；因此最终形状是 `(SCALE + ADD) × FACTOR`，而不是单纯读取一个 `state_weekly_trades_add` 整数。

这里的 `state+0x68` 已可按业务指标命名为“州的国际市场接入度（定点比例）”：同一州对象的 `+1228B90` 市场贸易比例构造函数也读取该字段，并只在其低于 `100000` 时把它作为比例输入；这与界面显示的国际市场接入度以及“接入度不足按比例削弱贸易活动”的语义一致。预算路径对它采用相同的 `min(1, access)` 逻辑，因此不是再次按 workforce 缩放。
