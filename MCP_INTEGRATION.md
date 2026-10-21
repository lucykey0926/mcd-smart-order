# MCP 接入说明

## MCP Server
- 地址：https://mcp.mcd.cn
- 认证方式：Bearer Token（环境变量 `MCD_MCP_TOKEN`）

## 使用的工具

| 工具名 | 用途 |
|---|---|
| store.list | 查询附近门店 |
| menu.query | 获取菜单与商品信息 |
| coupon.list | 获取当前可用优惠券 |
| promo.current | 获取门店活动 |
| order.preview | 下单预览（不扣款） |
| order.confirm | 确认下单（需用户明确指令） |

> 以上工具名以麦当劳 MCP 官方实际接口为准，如有差异以官方文档为准。

## 调用流程
用户输入（两大一小/预算/忌口）

↓

门店澄清 → store.list

↓

拉菜单 → menu.query

↓

拉券/活动 → coupon.list + promo.current

↓

计算方案 → family_optimize.py

↓

渲染三套方案展示给用户

↓

用户说"确认下单"

↓

order.preview（预览，不执行）

↓

用户再次确认

↓

order.confirm（正式下单）

## 业务价值

家长带娃吃麦当劳时面临三个痛点：
1. 开心乐园餐玩具档期不确定
2. 甜饮想换牛奶/苹果片不会操作
3. 成人餐+儿童餐+满减券组合算不过来

本 Skill 通过真实调用麦当劳 MCP，把「门店选择 → 菜单拉取 → 券匹配 → 方案计算 → 确认下单」全流程自动化，让家长一句话得到最优家庭点餐方案。

## 注意事项

- 所有价格、库存、供应状态以 MCP 实时返回为准，不缓存、不编造
- 写操作（下单/用券/扣积分）必须用户明确说"确认下单"才执行
- Token 不硬编码，仅通过环境变量传入
