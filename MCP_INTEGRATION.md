# MCP 接入说明

## MCP Server
- 地址：https://mcp.mcd.cn（服务端 `mcd-mcp v1.0.0`，Streamable HTTP / JSON-RPC 2.0，`tools/list` 共 35 个工具）
- 认证方式：Bearer Token（环境变量 `MCD_MCP_TOKEN`，不写入仓库）

## 使用的工具

| 工具名 | 类型 | 用途 |
|---|---|---|
| now-time-info | 只读 | 服务器时间锚点：判断午市/早餐档期、"仅今日"活动 |
| query-nearby-stores | 只读 | 查询附近门店。参数 beType/city/keyword/searchType；不支持经纬度，用「城市 + 中文地标关键词」查询 |
| query-meals | 只读 | 门店在售菜单与分类（必须传 storeCode，先定门店再拉菜单） |
| query-meal-detail | 只读 | 餐品详情与套餐构成（rounds 轮次：主食/小食/饮料），识别乐园餐可换项（牛奶/苹果片） |
| query-store-coupons | 只读 | 指定门店当前可用优惠券 |
| query-my-coupons | 只读 | 我的券包（已持有券），算价时优先代入 |
| available-coupons | 只读 | 当前可领取的券，仅用于提示用户，不自动领取 |
| campaign-calendar | 只读 | 活动日历：开心乐园餐玩具档期、限时活动窗口 |
| query-promotions | 只读 | 门店促销活动（如晚8后半价类信息） |
| list-nutrition-foods | 只读 | 全量营养参考值（"家长友好"方案的参考值标注来源） |
| calculate-price | 只读 | 组合实付价试算（含券、含活动价），不产生订单 |
| auto-bind-coupons | 写 | 领券。**必须用户同意后才调用**，默认不在调用链上 |
| create-order | 写 | 真实下单。**仅当用户字面说"确认下单"且经 calculate-price 核价展示后才调用** |

明确不使用：`draw-lottery`（扣积分）、`mall-*`（积分商城）、`cancel-order`、`delivery-*`（本项目不做外送/抽奖/积分场景）。

## 调用流程（严格按顺序）

用户输入（两大一小/预算/忌口/要乐园餐）

↓

时间锚点 → now-time-info（判断当前时段属于哪个菜单档期）

↓

门店澄清 → query-nearby-stores（city + 地标关键词；门店不明最多问 1 次，不瞎猜）

↓

拉菜单 → query-meals（storeCode）

乐园餐构成 → query-meal-detail（rounds 识别饮料轮次，确认可换牛奶/苹果片）

↓

拉券 → query-store-coupons + query-my-coupons（available-coupons 仅提示不代领）

活动/档期 → campaign-calendar + query-promotions（乐园餐玩具档期）

↓

算价 → calculate-price（三套方案逐一试算实付价）

营养参考 → list-nutrition-foods（只标"参考值"）

↓

family_optimize.py 渲染三套方案（全家稳 / 孩子开心 / 家长友好）+ 甜饮换饮提示

↓

用户字面说"确认下单"（**未收到这四个字，流程到此为止，绝不继续**）

↓

create-order（正式下单）

↓

回报订单结果

## 官方接口特性（联调要点）

- `query-nearby-stores` 不接受 latitude/longitude（字段会被静默忽略），必须用「城市 + 中文地标关键词」定位
- 工具返回非纯 JSON：`content[].text` 为「字段说明 + JSON payload」拼接，解析前需先定位 JSON 边界
- `list-nutrition-foods` 返回 CSV 字符串而非 JSON 数组，需单独解析
- 菜单按时段切换（早餐/正餐档），一切以 `query-meals` 实时返回为准，不缓存、不编造
- 门店当日可能无可用券：算价必须保留「无券按菜单价精算」的降级路径

## 业务价值

家长带娃吃麦当劳时面临三个痛点：
1. 开心乐园餐玩具档期不确定
2. 甜饮想换牛奶/苹果片不会操作
3. 成人餐+儿童餐+满减券组合算不过来

本 Skill 通过真实调用麦当劳 MCP，把「门店选择 → 菜单拉取 → 券匹配 → 档期确认 → calculate-price 核价 → 确认下单」全流程自动化，让家长一句话得到最优家庭点餐方案。

## 注意事项（安全边界）

- 所有价格、库存、玩具档期、供应状态以 MCP 实时返回为准，不缓存、不编造
- 未收到用户字面说"确认下单"四个字，绝不调用 create-order
- 下单前必须先用 calculate-price 核价并展示明细，等用户确认后才执行
- auto-bind-coupons 属写操作，领券前必须征得用户明确同意
- Token 不硬编码，仅通过环境变量 MCD_MCP_TOKEN 传入
- 营养数据只标"参考值"，不作医疗/膳食建议

> 以上工具名与调用顺序已对照 mcp.mcd.cn 官方服务（mcd-mcp v1.0.0）工具清单对齐；如有更新以官方文档为准。
