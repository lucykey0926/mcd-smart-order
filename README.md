# 麦麦遛娃点餐师（MaiMai-Kids-Order）

> 两大一小家庭场景的麦当劳 WorkBuddy Skill，一句话算出带娃最省家庭餐。

## 痛点

家长周末带娃吃麦当劳常遇三难：
- 开心乐园餐玩具不知道有没有
- 甜饮想换牛奶/苹果片不会操作
- 成人餐+儿童餐+满减券组合算不过来

## 功能

- 识别两大一小家庭上下文
- 真实调用麦当劳 MCP 拉门店/菜单/券/活动
- 固定输出三套方案：全家稳 / 孩子开心 / 家长友好
- 乐园餐甜饮→牛奶/苹果片自动提示
- 下单双保险（calculate-price 核价展示 + 字面"确认下单"才执行）

## 对话示例

> 👤 用户：周末中午，带孩子，两大一小，预算70，别太甜，要有玩具/开心乐园餐。

> 🤖 麦麦遛娃点餐师：已识别开心乐园餐档期🎈（当前小汽车玩具款）

| 方案 | 内容 | 原价 | 家庭实付 | 备注 |
|---|---|---:|---:|---|
| 👨👩👦全家稳 | 2板烧鸡腿堡+1乐园餐(甜饮换牛奶) | 62 | 54 | 满60减8命中 |
| 🍟孩子开心 | 1板烧+1麦辣+1乐园餐 | 60 | 52 | 有玩具，甜饮可免费换 |
| 🥗家长友好 | 2堡+乐园餐+玉米杯 | 67 | 59 | 整体更低卡 |

提示：乐园餐苹果片为默认配置，已按"别太甜"勾换牛奶，下单前可改。完整模拟运行记录见 [examples/run-demo.md](examples/run-demo.md)。

## 快速开始

```bash
git clone https://github.com/lucykey0926/mcd-smart-order.git

cd mcd-smart-order

cp mcp-config.example.json mcp-config.json
```

## 安装方式（WorkBuddy）

1. **申请麦当劳 MCP Token**（免费）：https://open.mcd.cn/mcp → 手机号登录 → 控制台 → 激活 → 复制 Token
2. **配置 MCP 连接器**：WorkBuddy 左侧边栏【专家·技能·连接器】→【连接器】→【自定义连接器】→【配置 MCP】，填入 `mcp-config.example.json` 内容，把 `${MCD_MCP_TOKEN}` 替换为你的真实 Token（**只填在本地，不要提交到任何仓库**），保存并启用
3. **安装 Skill**：将本仓库放入 `~/.workbuddy/skills/maimai-kids-order/`（skill.yaml、prompts/、scripts/、examples/ 一并复制）
4. **开聊**：触发词 `/遛娃点餐` / `/带娃吃麦` / `/家庭点餐`

其他客户端（Claude Code 等）配置方式相同，见 [MCP_INTEGRATION.md](MCP_INTEGRATION.md)。

## 离线验证（无需 Token）

```bash
python scripts/family_optimize.py
```

输出两大一小 / 预算70 / 少甜 / 要乐园餐场景下的三套方案 JSON。完整模拟运行记录见 [examples/run-demo.md](examples/run-demo.md)。

## 目标用户

周末带娃去麦当劳的家长（典型：两大一小、预算敏感、要开心乐园餐玩具、想控制孩子糖分摄入）。

## 文件结构

| 文件 | 说明 |
|---|---|
| skill.yaml | Skill 清单（名称/描述/触发词/入口） |
| prompts/main.md | 系统提示词（处理流程与红线） |
| scripts/family_optimize.py | 家庭点餐组合计算引擎（纯函数，无网络） |
| MCP_INTEGRATION.md | MCP 工具、调用流程与业务价值 |
| mcp-config.example.json | 脱敏配置示例（仅环境变量占位符） |
| examples/run-demo.md | 本地模拟运行记录（含红线验证） |
| workbuddy.md | WorkBuddy 开发与跑通记录 |
| CONTEST_DECLARATION.md | 参赛声明（官方原文，一字不差） |
