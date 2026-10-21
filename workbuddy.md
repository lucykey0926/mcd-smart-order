# WorkBuddy 开发记录

## 项目信息
- 项目名称：麦麦遛娃点餐师（MaiMai-Kids-Order）
- 参赛赛事：2026 麦当劳程序员创意开发大赛
- 开发工具：腾讯 WorkBuddy

## WorkBuddy 参与内容

本项目全程由 WorkBuddy 辅助开发，具体包括：

1. Skill 设计：系统提示词、触发词、多轮对话流程
2. 计算逻辑：family_optimize.py 家庭点餐组合枚举与最优方案计算
3. 文档生成：README、MCP_INTEGRATION.md、本文件等全部参赛文档
4. 架构规划：目录结构、文件组织、参赛合规检查

## MCP 接入

- 真实接入麦当劳中国 MCP（https://mcp.mcd.cn）
- 使用 store.list / menu.query / coupon.list / promo.current / order.preview / order.confirm
- 配置通过环境变量 MCD_MCP_TOKEN 传入

## 开发过程

需求澄清 → Skill prompt 设计 → 计算脚本编写 → MCP 接入方案 → 文档生成 → 合规自检

## 声明

本项目为参赛作品，非麦当劳官方产品。所有餐品信息、价格以麦当劳官方实时数据为准。
