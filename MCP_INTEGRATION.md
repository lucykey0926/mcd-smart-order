# MCP 接入说明

## MCP Server

- 地址：`https://mcp.mcd.cn`
- 传输：Streamable HTTP / JSON-RPC 2.0
- 认证：Bearer Token，通过本地环境变量 `MCD_MCP_TOKEN` 配置，不写入仓库

## 家庭点餐使用的工具

| 工具名 | 类型 | 用途与约束 |
|---|---|---|
| `now-time-info` | 只读 | 获取服务器时间，判断当前日期与菜单时段 |
| `query-nearby-stores` | 只读 | 按城市和中文地标查询门店；到店自取 `beType=1`，无需 `beCode` |
| `query-meals` | 只读 | 获取指定门店在售菜单、商品编码和当前价格；必须传 `storeCode` |
| `query-meal-detail` | 只读 | 获取套餐 `rounds`、默认搭配、可选替换项和玩具信息；是判断乐园餐构成的主要依据 |
| `query-store-coupons` | 只读 | 查询指定门店与订单类型下可使用的券 |
| `query-my-coupons` | 只读 | 查询用户券包；不代表券一定适用于当前门店和订单 |
| `campaign-calendar` | 只读 | 查询综合营销活动日历；不能单独作为开心乐园餐玩具档期依据 |
| `list-nutrition-foods` | 只读 | 查询营养参考数据，只标“参考值”，不作医疗或膳食建议 |
| `calculate-price` | 只读 | 对具体商品、套餐搭配和可选券进行真实核价，不产生订单 |
| `create-order` | 写 | 真实下单；只有收到用户字面“确认下单”后才允许调用 |
| `auto-bind-coupons` | 写 | 领券；必须经用户明确同意，默认不调用 |

`query-promotions` **仅适用于企业团餐 `beType=6`**，需要团餐门店的 `beCode`，不属于本项目“两大一小到店自取”的调用链。

明确不使用：`draw-lottery`、`mall-*`、`cancel-order`、`delivery-*`。本项目不处理抽奖、积分商城、取消订单或外送。

## 家庭点餐调用流程

1. `now-time-info`：确认服务器日期和时段。
2. `query-nearby-stores`：以 `searchType=2`、城市、地标和 `beType=1` 查询到店自取门店；由用户确认具体门店。
3. `query-meals`：以 `storeCode`、`orderType=1`、`beType=1` 拉取实时菜单。
4. `query-meal-detail`：读取开心乐园餐 `rounds`，确认主食、小食、饮料和玩具的默认选项及可替换项。
5. `query-store-coupons`：查询当前门店和订单类型可用券；必要时结合 `query-my-coupons`，但只采用确实适用的券。
6. `campaign-calendar`：补充综合活动信息；不得据此臆测门店玩具库存。
7. `calculate-price`：对三套候选方案分别核价，以返回价格为准。
8. 输出“全家稳 / 孩子开心 / 家长友好”三套方案，并说明少甜搭配和预算余额。
9. 流程停住。未收到用户字面“确认下单”，不得调用 `create-order`。

## 真实联调规则

### 门店与菜单

- `query-nearby-stores` 使用城市和中文地标，不依赖经纬度。
- 到店自取：`beType=1`、`orderType=1`，不传 `beCode`。
- 得来速：`beType=5`，后续调用必须带门店返回的 `beCode`。
- 菜单、价格和供应状态以 `query-meals` 实时返回为准，不缓存、不编造。

### 乐园餐与少甜处理

- 玩具名称、默认小食和饮料以 `query-meal-detail` 的 `rounds` 为准。
- 某门店在某次联调中默认提供牛奶和苹果片，不代表所有门店、所有时期均相同；每次都要重新查询。
- 套餐核价时按 `roundList` 传入所选子项。
- 对包含 `unselectedKey` 的特调组，选中项使用 `selectedKey`，未选中项也必须携带并使用 `unselectedKey`。

### 优惠券与价格

- `query-my-coupons` 只做资产查询；当前订单是否可用以 `query-store-coupons` 和 `calculate-price` 为准。
- 与组合无关的券不使用，不为凑优惠增加不需要的商品。
- `calculate-price` 返回金额单位为**分**，展示为元时必须除以 100。
- 核价返回的 `productList`、`discount`、`price` 是方案展示依据；不得继续沿用离线示例中的满减金额。

## 2026-10-24 真实只读联调

- 门店：麦当劳大连青云街地铁站餐厅，`storeCode=3230317`，到店自取。
- 已成功调用：时间、门店、菜单、乐园餐详情、门店券、券包、活动日历和三组价格试算。
- 当次乐园餐详情：汉堡包、迷你薯条、苹果片、纯牛奶，以及海绵宝宝×航海王系列玩具。
- 三套核价结果：麦香鸡×2＋乐园餐 ¥56.50；麦辣鸡腿汉堡×2＋乐园餐 ¥68.50；麦香鱼×2＋乐园餐 ¥69.50。
- 两张咖啡类券与家庭餐组合无关，未使用；未领券、未创建订单。

## 安全边界

- 未收到用户字面“确认下单”，绝不调用 `create-order`。
- 下单前必须先用 `calculate-price` 核价并展示明细。
- `auto-bind-coupons` 只有用户明确同意后才可调用。
- Token、券码、手机号等敏感信息不得写入仓库或联调记录。
- 玩具、库存和价格以实时返回及门店实际供应为准。
- 营养数据仅作参考，不作医疗或膳食建议。
