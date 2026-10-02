# 从游戏内观测数据可知：进口1单位织物占0.1贸易容量，进口1单位茶叶占 0.2贸易容量。1单位帆船占0.3贸易容量。能否搜索到这些占贸易容量的常数，在目前本地文件夹中，是否有记录配置？

可以，当前本地文件中有明确配置记录。核心字段不是 `convoy_cost_multiplier`，而是商品定义中的 `traded_quantity`。

**商品配置**
基于Victoria3游戏目录文件解析得到。
- `game/common/goods/00_goods.txt:113`：`fabric` 的 `traded_quantity = 10`
  - 1 单位织物占 `1 / 10 = 0.1` 贸易容量。
- `game/common/goods/00_goods.txt:468`：`tea` 的 `traded_quantity = 5`
  - 1 单位茶叶占 `1 / 5 = 0.2` 贸易容量。
- `game/common/goods/00_goods.txt:234`：`clippers`（帆船）的 `traded_quantity = 3.5`
  - 1 单位帆船占 `1 / 3.5 ≈ 0.2857`，界面按一位小数显示为 `0.3`。

在 [00_goods.txt](/D:/Games/Victoria3/Victoria%203/game/common/goods/00_goods.txt) 中：

- `wood`：第 **133** 行，`traded_quantity = 10`
- `fine_art`（艺术品）：第 **596** 行，`traded_quantity = 1.5`

计算关系可概括为：

```text
每单位商品占用贸易容量 = 1 / traded_quantity
```

此外：

- `game/common/defines/00_defines.txt:620` 的 `GOODS_DEFAULT_TRADE_QUANTITY = 10` 是没有单独设置商品值时的默认贸易量。
- `game/common/production_methods/11_private_infrastructure.txt:393-451` 中的 `state_trade_quantity_mult` 会调整每点贸易容量对应的实际贸易量，例如贸易中心生产方式可使贸易量变为 `-50%`、`+50%` 或 `+100%`。
- 同一商品定义中的 `convoy_cost_multiplier` 是运输航线的船队/运输成本，不是贸易容量占用。例如织物为 `0.15`、茶叶为 `0.5`、帆船为 `0.15`，不要与 `traded_quantity` 混淆。


## 贸易中心的四种基础生产方式
生产方式	商船队消耗 / 每级	可交易量倍率	
Small-Scale Trading 小规模贸易	+3.0	−50%	
Regular Trading 常规贸易	+4.0	
Bulk Trading 大宗贸易	+5.0	+50%	
Mass-Scale Trading 大规模贸易	+6.0	+100%	

