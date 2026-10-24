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
5. 合规自检：仓库体检、历史敏感信息扫描、参赛声明原文校验

---

## 跑通记录

### 安装方式

1. 申请麦当劳 MCP Token（https://open.mcd.cn/mcp，免费）
2. WorkBuddy【连接器】→【自定义连接器】→【配置 MCP】，按 `mcp-config.example.json` 填入（`${MCD_MCP_TOKEN}` 替换为本地真实 Token，不进仓库）
3. Skill 放入 `~/.workbuddy/skills/maimai-kids-order/`
4. 无 Token 也可离线验证：`python scripts/family_optimize.py`

### 触发话术

- `/遛娃点餐`、`/带娃吃麦`、`/家庭点餐`
- 自然语言示例：「周末中午，带孩子，两大一小，预算70，别太甜，要有开心乐园餐玩具」

### 调用链（严格顺序，对齐官方工具名）

```
now-time-info（服务器日期与时段）
→ query-nearby-stores（city+地标关键词，beType=1，用户确认门店）
→ query-meals（storeCode 拉实时菜单）
→ query-meal-detail（rounds 确认玩具、默认饮料/小食和替换项）
→ query-store-coupons + query-my-coupons（门店适用券+券包参考）
→ campaign-calendar（仅补充综合活动，不据此判断玩具）
→ calculate-price（三套方案逐一真实核价，金额由分转元）
→ 渲染三套方案与少甜提示
→ 【停住】等用户字面“确认下单”
→ create-order（仅此时可执行）
```

写操作仅两个：`create-order`（字面“确认下单”后）、`auto-bind-coupons`（领券需用户同意，默认不调用）。`query-promotions` 仅限企业团餐 `beType=6`，不在家庭到店自取调用链上。

### 验证结论

| 验证项 | 方式 | 结果 |
|---|---|---|
| 必交文件齐全性 | 逐文件核对（含官方必交 4 件 + workbuddy.md） | ✅ 10 个文件全部就位 |
| CONTEST_DECLARATION.md 官方原文 | 与 M-China 官方仓库 sha256 比对 | ✅ 逐字节一致（并加 .gitattributes 防换行污染） |
| 敏感信息 | 工作树 grep + 10 个提交全历史扫描 + fsck 孤儿对象 | ✅ 0 命中（无 Token/手机号/券号） |
| skill.yaml 可识别性 | 对照官方校验规范（name hyphen-case + description 必填 + entry 存在） | ✅ 修复缺失 description 后全部通过 |
| family_optimize.py 纯函数性 | AST 级 import 检查 | ✅ 无网络/子进程/文件系统依赖，无硬编码 Token |
| 三套方案正确性 | 14 项离线断言（模拟输入：两大一小/预算70/少甜/要乐园餐） | ✅ 14/14 PASS（全家稳 62→54 / 孩子开心 60→52 / 家长友好 67→59，均 ≤ 预算） |
| 少甜输入消费 | 断言方案 note 含换饮提示 | ✅ 已修复"low_sweet 被静默忽略"缺陷 |
| 下单红线 | AST 检查 + 模拟对话验证（用户说"那就第一套吧"） | ✅ 脚本内不存在任何下单调用；非字面"确认下单"流程停住 |
| MCP 工具名真实性 | 与官方 mcd-mcp v1.0.0 实测资料（35 tools）交叉比对 | ✅ 6 个虚构工具名全部修正为真实名，全仓 grep 零残留 |
| 本地模拟跑通 | examples/run-demo.md 完整记录 | ✅ 场景识别→模拟 MCP 链→三套方案→换饮提示→下单前停住 |
| 真实 MCP 联调 | 大连青云街门店，只读调用至 calculate-price | ✅ 门店/菜单/详情/券/活动/三组核价全部成功；未下单、未领券 |
| 真实接口规则修正 | 对照工具 Schema 与真实返回 | ✅ query-promotions 限团餐；玩具以 meal-detail 为准；价格单位由分转元 |

完整模拟运行对话见 [examples/run-demo.md](examples/run-demo.md)。

### 2026-10-24 真实联调记录

- 配置：本地 `mcp.json` 校验通过，Token 仅保存在本地，未写入仓库。
- 场景：大连市中山区，到店自取；用户确认“麦当劳大连青云街地铁站餐厅”（`storeCode=3230317`）。
- 时间：`now-time-info` 返回 2026-10-24 周六，GMT+8。
- 菜单：`query-meals` 返回真实在售菜单，开心乐园分类含 3 款乐园餐。
- 乐园餐：`query-meal-detail` 返回汉堡包、迷你薯条、苹果片、纯牛奶及海绵宝宝×航海王系列玩具；牛奶和苹果片为当次默认项。
- 优惠券：券包和门店券均为 2 张咖啡类券，与本次组合无关，未使用，记录中不保存券码。
- 活动：`campaign-calendar` 调用成功，但仅作综合活动参考，不作为玩具依据。
- 真实核价：全家稳 ¥56.50；孩子开心 ¥68.50；家长友好 ¥69.50，均不超过 ¥70。
- 安全边界：全程未调用 `create-order` 或 `auto-bind-coupons`，未产生订单或领券操作。

以上结果只代表该门店和该次查询；后续运行仍须实时查询，不缓存价格、玩具或供应状态。

### 安全边界

- **不自动下单**：未收到用户字面"确认下单"四个字，绝不调用 create-order
- **核价前置**：下单前必须 calculate-price 核价并展示实付明细
- **不静默领券**：auto-bind-coupons 必须用户同意后才调用
- **Token 零入库**：仓库仅含 `${MCD_MCP_TOKEN}` 占位符，真实 Token 只存本地环境变量
- **不编造价格**：一切以 MCP 实时返回为准，不缓存；模拟数据必须标注"示例"
- **营养仅参考**：营养数据只标"参考值"，不作医疗/膳食建议
- **不猜测门店**：必须用户确认门店后才进入下单流程
- **参赛声明不可改**：CONTEST_DECLARATION.md 保持官方原文（.gitattributes 已设 `-text` 防换行差异）

---

## 开发过程

需求澄清 → Skill prompt 设计 → 计算脚本编写 → MCP 接入方案 → 文档生成 → 合规自检（仓库体检/历史扫描/工具名对齐）→ 离线模拟跑通 → 真实 MCP 只读联调 → 接口规则与跑通记录修正

## 声明

本项目为参赛作品，非麦当劳官方产品。所有餐品信息、价格以麦当劳官方实时数据为准。
