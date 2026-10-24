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

## 真实联调示例

> 👤 用户：周末中午，带孩子，两大一小，预算70，别太甜，要有开心乐园餐玩具。大连市中山区，到店自取。

2026-10-24 在大连青云街地铁站餐厅完成真实只读联调。当次乐园餐详情为：汉堡包、迷你薯条、苹果片、纯牛奶，以及海绵宝宝×航海王系列玩具；牛奶和苹果片均为默认选项。

| 方案 | 内容 | calculate-price 实付 | 预算余额 |
|---|---|---:|---:|
| 👨👩👦全家稳 | 麦香鸡×2 + 汉堡开心乐园餐 | ¥56.50 | ¥13.50 |
| 🍟孩子开心 | 麦辣鸡腿汉堡×2 + 汉堡开心乐园餐 | ¥68.50 | ¥1.50 |
| 🥗家长友好 | 麦香鱼×2 + 汉堡开心乐园餐 | ¥69.50 | ¥0.50 |

三套方案均未使用优惠券，未创建订单。价格、玩具和供应状态以实时查询及门店实际为准；完整真实联调结论见 [workbuddy.md](workbuddy.md)，离线流程示例见 [examples/run-demo.md](examples/run-demo.md)。

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
