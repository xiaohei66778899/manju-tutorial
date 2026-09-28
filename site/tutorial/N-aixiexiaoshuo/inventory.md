# AI 写小说垂直教学站 · 资源总索引（inventory）

> **定位**：AI 写小说领域最全、最专业的垂直教学站前期资源库——别人有的我要有，别人没有的我也要有。
> **收集日期**：2026-09-21
> **原则**：宁缺毋滥，只收真正高质量的一手资料；所有 URL 均来自实际检索/抓取，未编造；拿不准的数据一律标「待核实」。
> **目录结构**：
>
> ```
> E:\AI写小说\
> ├─ inventory.md          ← 本文件，总索引
> ├─ video-links.md        ← 视频链接清单（仅链接，未下载视频）
> ├─ tools.md              ← 主流写小说工具对比
> ├─ repos\                ← 实际 clone 下来的 GitHub 仓库 + 同名 .txt 说明 + README.md
> └─ articles\             ← 文章资料（每篇一个 .md，附 _index.md）
> ```

---

## 一、视频资源 → [`video-links.md`](video-links.md)

**共 20 条**：YouTube 12 条（必看 5 / 选看 7）+ B站 8 条（必看 3 / 选看 5）。
只存链接与元信息（标题/时长/UP主/核心内容/推荐级别），**未下载任何视频文件**。时长、发布日期经 YouTube 观看页与 B站官方接口逐条核实。

**必看精选**：
- YouTube：Sudowrite 官方速览与快速上手、NovelCrafter 官方新手指南、The Nerdy Novelist《How to Write a GOOD Book with AI in 2025》、Sean Dollwet《Write a Book with ChatGPT 全教程》。
- B站：非凡写作官方《45 分钟 AI 写小说拆解流程》、0爱喝汽水的猫0《硬核辅助工具大更新》、普普通通的程序员呀《九分钟零基础写长篇》。
- 另收一条责编 Alyssa Matesic《AI Novels Make Me Furious》做反面参照，平衡视角。

---

## 二、GitHub 仓库 → [`repos\README.md`](repos/README.md)

**10 个仓库全部 `git clone --depth 1` 成功落盘**，目录均非空；每个仓库旁有同名 `.txt` 说明（URL / star 数 / 最近更新 / 主要内容 / 收录理由）。star 数经 GitHub 接口或仓库页实时核实。

| 仓库 | Stars | 类别 |
|---|---|---|
| [AI_NovelGenerator](repos/AI_NovelGenerator.txt) | 6104 | 提示词模板 / 工作流 / 世界观 |
| [chinese-novelist-skill](repos/chinese-novelist-skill.txt) | 3138 | 中文写小说工作流 |
| [ai-novel-writing-assistant](repos/ai-novel-writing-assistant.txt) | 2966 | AI 小说工作流（全栈样本） |
| [NovelForge](repos/NovelForge.txt) | 1206 | AI 小说工作流（卡片式） |
| [AI-automatically-generates-novels](repos/AI-automatically-generates-novels.txt) | 951 | 中文写网文流水线 |
| [awesome-novel-skill](repos/awesome-novel-skill.txt) | 751 | awesome / Skill 汇总 |
| [writing-agent](repos/writing-agent.txt) | 422 | 中文写作工作流（DeepSeek/通义/GLM/Kimi） |
| [WenShape](repos/WenShape.txt) | 417 | 角色卡 / 世界观一致性 |
| [NovelClaw](repos/NovelClaw.txt) | 372 | AI 小说工作流（章节起草） |
| [NovelGenerator](repos/NovelGenerator.txt) | 146 | 本地 Ollama/Gemini 长篇生成 |

**五个收集类别全部覆盖**：awesome 汇总、提示词模板、自动化工作流、角色卡/世界观、中文写网文。
**未收录但如实记录**：`ReNovel-AI`（404 不存在）、`Novel-Claude`（仅 12 star）、`AIStoryWriter`（超一年未维护）、通用提示词库 awesome-chatgpt-prompts（不垂直）——原因见 repos/README.md。

---

## 三、文章资料 → [`articles\_index.md`](articles/_index.md)

**共 12 篇**：国外 6 篇 + 国内 6 篇。每篇一个 `.md`，含来源 URL、作者/站点、日期、150–300 字中文摘要（均基于实际抓取正文）、一句话推荐理由。

**国外（6）**：
1. [用 Claude 写 34 本小说的经验](articles/用Claude写34本小说的经验.md) — 工程化多文件设定集 + loop 循环
2. [ChatGPT 写小说六步法](articles/ChatGPT写小说六步法.md) — 自出版作者六步流程 + 模型选型
3. [用 ChatGPT 写长篇小说专业工作流](articles/用ChatGPT写长篇小说专业工作流.md) — 把专业编辑流程映射到 AI
4. [用 AI 构思情节（NovelCrafter 官方）](articles/用AI构思情节-NovelCrafter官方.md) — 设定集驱动 + 三层细化
5. [用 GPT-4 从零写一整本小说（译文）](articles/用GPT-4从零写一整本小说.md) — 首尾边界控制法 + 连续性笔记
6. [Claude 长篇小说写作助手手册](articles/Claude长篇小说写作助手手册.md) — 故事圣经 + 三段式写作清单

**国内（6）**：
1. [知乎盐选实操手册与 AI 提示词](articles/知乎盐选实操手册与AI提示词.md) — 爽点密度 + 付费卡点 + 可复制提示词
2. [AI 写小说四步实战法](articles/AI写小说四步实战法.md) — 专家设定→大纲→子场景→上下文回顾
3. [DeepSeek 打造爆款知乎盐选](articles/DeepSeek打造爆款知乎盐选.md) — 前 300 字定生死 + 金句植入
4. [多 Agent 架构写连载小说](articles/多Agent架构写连载小说.md) — 治长篇失忆与 AI 味
5. [做故事架构师而非码字工](articles/做故事架构师而非码字工.md) — 反向提问 + 人格锚点 + 信息差钩子
6. [DeepSeek-V4 提示词终极指南](articles/DeepSeek-V4提示词终极指南.md) — CRISPE 框架 + 长篇续写任务书

**因反爬/质量未收录**：知乎多篇（正文反爬抓不到）、Medium 站内（检索限流）、Sudowrite/NovelAI 官方长指南（无足够正文）、短视频口播与营销测评文——清单见 articles/_index.md。

---

## 四、工具盘点 → [`tools.md`](tools.md)

**覆盖 11 个工具**，每个含：一句话定位 / 价格（注明核实时间 2026-09）/ 擅长类型 / 独特功能 / 适合人群 / 官网。文末附「按人群/场景选型建议」。

- **国外（6）**：Sudowrite、NovelCrafter、NovelAI、Claude、ChatGPT、Gemini
- **国内（5）**：文心一言（ERNIE）、通义千问、豆包、Kimi、DeepSeek

**价格已官网核实**：Sudowrite（$10/$22/$44）、NovelCrafter（$4/$8/$14/$20）、Claude（$20 起 / $100）、Gemini（$4.99/$19.99 起）、Kimi（¥49/¥99/¥199/¥699）、DeepSeek（网页免费 + API 按量）、豆包（¥68/¥200/¥500）、通义（¥19/¥49/¥128）。
**待核实（已如实标注）**：NovelAI（官网订阅页无法抓取，采信第三方报道）、文心一言 C 端付费档位、ChatGPT Pro 细分档。

---

## 五、维护与后续扩充方向

1. **待核实项**：NovelAI / 文心一言 / ChatGPT Pro 价格；后续可人工访问官网补齐。
2. **可继续扩充的缺口**：
   - 知乎、公众号深度长文（当前受反爬限制，建议后续用浏览器登录态采集）；
   - Sudowrite / NovelAI / NovelCrafter 官方完整用户手册与模板库；
   - YouTube 更多非英语区（日语、西语）AI 写作教程；
   - 角色卡 / 世界观工具（如 NovelCrafter Lorebooks、Sudowrite Story Bible）的横向实测。
3. **更新机制**：本索引为快照，视频播放量、star 数、价格均随时间变化，引用时以原文/官网为准。
