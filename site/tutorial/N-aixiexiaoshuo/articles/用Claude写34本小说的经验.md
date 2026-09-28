# What I Learned Making 34 Novels with Claude Sonnet

- **来源 URL**: https://triptych.writeas.com/what-i-learned-making-34-novels-with-claude-sonnet
- **作者/站点**: triptych（个人博客 writeas）
- **发布日期**: 2026-01-27

## 核心观点摘要（中文）

作者把"用 AI 写小说"当成一个软件开发项目来做，一年用 Claude Sonnet（配合 Nano Banana、Cline、Claude Code）产出了 34 本科幻/奇幻小说。核心流程是一套基于 Markdown 文件的工程化管线：先定类型，让 AI 把类型特征研究存成 `research.md`；协作定高层剧情存 `plot.md`；再派生出 `emotional-arc.md`、`sensory-details.md`、`magic-system.md`、人物档案、`world-history.md`、`writing-style.md` 等支撑文档；然后生成至少 30 章的 `chapter-by-chapter.md`（带复选框、字数、情节节拍，刻意写长以对抗 AI"偷懒写短"的倾向）；最关键的是写一个 `loop.md` 工作流，让 AI 每次读全部文档、定位下一章、写完再回写进度。每章必须在"干净上下文"里单独跑，禁止一次写多章，否则上下文越长质量越糊。全书写完后另起上下文让 AI 当无情编辑输出 `evaluation.md`（矛盾、剧情漏洞、时间线问题），再开新上下文按最小改动原则修复。最后用 Pandoc 把 Markdown 转成 ePub/PDF/HTML，并生成封面、人物图和配套书站。作者还总结了 AI 的怪癖：女爱用 Lyra/Elara、男爱用 Kyle、反派爱叫 Mal- 开头、执着"低语森林"和"开学校"套路，且总爱搞"第三选项"折中结局——需在提示词里主动排除。

## 一句话推荐理由

实战产出 34 本小说的完整工程化工作流（多文件设定集 + loop 循环 + 干净上下文逐章 + 事后一致性审查），是目前最"可复刻"的 AI 长篇方法论之一。
