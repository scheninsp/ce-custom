# 世界市场接入度读取链

来源：`Output/2026-10-4-process2/read_trade_potential/function_1210600.c` 和 `.tsv`。
旧文档分析名称 `ReadTradePotential` 对应 `victoria3.exe+1210600`，本文件沿用旧名定位，并注明已确认的实际语义。

```text
// 功能：读取世界市场接入度，检查世界市场枢纽和路径，并应用封锁影响。
// 入参：state 为州对象；output 为定点整数输出地址；diagnostic 为可空的说明文本对象。
// 返回：output 地址；*output 是以 100000 为一单位的接入度。
function ReadTradePotential(state, output, diagnostic): // victoria3.exe+1210600；旧名，实际语义为世界市场接入度
    if game.initializing:
        *output = read_i64(state + 0x58)
        return output

    market = FUN_1407c33b0(state + 0xB48) // victoria3.exe+7C33B0
    hubRef = read_u32(market + 0x48)
    hub = FUN_1407c96a0(&hubRef) // victoria3.exe+7C96A0
    if not hub.virtual_validity_check():
        if diagnostic != null:
            append(diagnostic, "WORLD_MARKET_ACCESS_NO_HUB")
        *output = 0
        return output

    manager = game.field120.field4500
    destination = [read_u16(game.field120 + 0x8C8)]
    sourceIndex = 0xFFFF
    related = FUN_14154aa50(read_ptr(hub + 0xE78)) // victoria3.exe+154AA50
    if related.virtual_check() and read_u8(related + 0x1C8) == 0 and read_i32(related + 0x6C) != 0:
        sourceIndex = read_u16(read_ptr(related + 0x60))
    source = [sourceIndex]
    // 此调用另有国家引用、标志 0 和空排除集合参数；不是商品收益计算。
    path = FUN_1413fc470(manager, source, destination, read_u32(state + 0xE48), flags=0, excluded=[]) // victoria3.exe+13FC470
    if path.count == 0:
        if diagnostic != null:
            append(diagnostic, "WORLD_MARKET_ACCESS_BLOCKED")
        *output = 0
        destroy(path)
        return output

    access = read_i64(state + 0x58)
    if diagnostic != null:
        append_value(diagnostic, "WORLD_MARKET_ACCESS_FROM_MARKET_ACCESS", access)

    if hubRef == read_u32(state + 8):
        blockadeState = state
    else:
        blockadeState = hub
    blockade = 0
    if FUN_141230350(blockadeState): // victoria3.exe+1230350；资格检查，完整语义尚未独立确认
        blockade = read_i64(blockadeState + 0x1D60)
    if blockade > 0:
        delta = fixed_mul(-blockade, read_i64(victoria3.exe + 0x58893E8))
        multiplier = max(100000 + delta, 0)
        access = fixed_mul(access, multiplier)
        if diagnostic != null:
            append_values(diagnostic, "BLOCKADE_IMPACT_DESC", VALUE=delta, BLOCKADE_LEVEL=blockade)

    if diagnostic != null:
        append_hub_description(diagnostic, hub,
            hubRef == read_u32(state + 8) ? "WORLD_MARKET_ACCESS_IS_HUB" : "WORLD_MARKET_ACCESS_HAS_HUB")
    *output = access
    destroy(path)
    return output
```

`fixed_mul(a,b)` 表示带截断的 `a*b/100000`；原码另含较大数值的分解乘法路径。上述容器和诊断操作为概括表达，不是新恢复的原生函数名称。路径函数的图规则与 `+1230350` 的正式业务名称仍有证据边界。
