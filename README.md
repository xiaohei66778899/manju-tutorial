# 漫剧制作教程站

> 一节一节学会做漫剧 · 从小说、剧本、角色、分镜,到画面、视频、配音、剪辑和发布
> 玉哥 · 2026 · v3 架构
> 最近维护:**2026-09-24**(M/N 专题集成 + 全站体检 + 项目清理)

---

## 这是什么

一个**玉哥风格的漫剧制作教学站**。学员从打开网站到做出 1 部能赚钱的 AI 漫剧,每一步都有教程、工具、实例、练习。

## 核心数据(2026-09-24 现状)

- **13 大类教程** · **114 节** · 每节 1 个独立 HTML 页面
- **总 HTML 数:225 个**(114 节 + 入口页 + 资源页 + 404)
- **顶栏 8 入口**(首页 / 教程 / 学习路径 / 实例 / 模板 / 工具 / 问题 / 商业化)
- **四库并列**:教程库 / 实例库 / 工具与模板库 / 参考手册
- **玉哥口吻**:📢 玉哥说 / 玉哥口吻 / 玉哥整理
- **玉哥骨架**:左侧目录 + 中间内容 + 底部 1 篇/下 1 篇
- **本地预览端口:18080**(多线程 no-cache server)
- **缓存策略**:`?v=fix20260924-1900`(每次更新全站 cache-bust)
- **部署**:Netlify(publish = site/,含 `netlify.toml` `.nojekyll` `robots.txt`)

## 13 大类清单

| 类 | 目录 | 节数 | 入口页 |
|---|---|---|---|
| A | `A-manju-basic/` | 8 节 | A-1 |
| C | `C-character/` | 17 节 | C-1 |
| D | `D-storyboard/` | 15 节 | D-1 |
| E | `E-ai-image/` | 19 节 | E-1 |
| F | `F-ai-video/` | 18 节 | F-1 |
| G | `G-audio-edit/` | 18 节 | G-1 |
| H | `H-publish/` | 11 节 | H-1 |
| I | `I-appendix/` | 9 节 | I-1 |
| J | `J-comfyui/` | 1 入口 | J-ComfyUI 实操课 |
| K | `K-投流/` | 1 入口 | K-投流 |
| L | `L-airepo/` | 1 入口 | L-AI 漫画仓库 |
| **M** | `M-seedance/` | 1 入口 | **Seedance 即梦实操课** ✅ |
| **N** | `N-aixiexiaoshuo/` | 1 入口 | **AI 写小说实战课** ✅ |

> **B · 小说改剧本**:已并入 `index.html` 的 `#view-1-1` ~ `#view-2-4` 锚点,不再单独成目录
> **M/N 专题**:从外部源(`M-seedance/Seedance即梦实操课.html` + `E:\AI写小说\`)集成,**保持原版浅蓝渐变风格**(不覆盖玉哥暖色)

## 目录结构(2026-09-24 清理后)

```
12小说/
├─ README.md                  ← 你正在看
├─ PLAN.md                    ← 13 大类任务清单 + 优先级 + 状态
├─ AGENTS.md                  ← 项目规范 + AI agent 协作约定
├─ DEPLOY.md                  ← 部署步骤(Netlify)
├─ OUTPUT_INDEX.md            ← 全站 HTML 导航
├─ netlify.toml               ← Netlify 部署配置
├─ robots.txt                 ← 搜索引擎规则
├─ .nojekyll                  ← Netlify 不走 Jekyll
├─ .gitignore                 ← Git 忽略规则
│
├─ site/                      ← ⭐ 主交付物(225 HTML · Netlify publish 目录)
│  ├─ index.html              ← 首页(玉哥暖色风)
│  ├─ 404.html                ← 404 fallback(玉哥暖色卡)
│  ├─ changelog.html / learning-path.html / tutorial-template.html
│  ├─ assets/                 ← site.css / site-enhance.js / tutorial.js / 图片
│  ├─ tutorial/               ← 13 大类 114 节 + M/N 专题
│  ├─ prompts/ / video-prompts/ / templates/ / tools/ / qa/ / instances/ / commercial/ / news/
│  ├─ legacy/                 ← 玉哥原版课件 11 份(部署副本,源在根目录 legacy/)
│  └─ 剧本.html / 剧本-*.html ← 剧本 SPA 入口 + 8 个跳转页
│
├─ site/legacy/               ← 玉哥原版课件 11 份(v4~v17 · 唯一副本,根目录 legacy/ 已并入清理)
├─ scripts/                   ← 项目脚本(35 个 · serve-nocache / cache-bust / 路径修复 / 测试)
│
├─ _trash-removed/            ← 玉哥回收站(zhihu.js.removed-20260917-113227)
├─ logs/                      ← guard 守护进程日志
├─ .github/                   ← GitHub Actions 配置
│
└─ 飞书脑图_AI漫剧短剧制作全流程_avocado/   ← 飞书导出的全流程脑图源
```

## 风格

- **玉哥暖色 v3 主色**:`#635BFF`(顶栏 / 按钮 / 高亮)
- **M 专题风格**:`#3B72F0` 冷蓝 hero · 章节节奏 · stats 卡片(inline `<style>` 覆盖)
- **N 专题风格**:`#EEF3FB → #FAFBFC` 浅蓝渐变 hero · sidebar 让出 topbar(inline `<style>` 覆盖)
- **字体**:系统字体栈
- **不引外部资源**(JS/CSS 全本地,除 N 专题内的极少量腾讯字体)
- **单页 HTML**(无构建,直接 `file://` 或 HTTP server)

## 开发方式

1. **Cursor 打开本目录** `E:\AIGC\课件\12小说\`
2. **认领任务**:在 PLAN.md 找一行,把 🔴 改成 🟡 写中
3. **复制模板**:`site/tutorial-template.html` → 改名 `<类>-<节>.html` 放到对应目录
4. **写内容**:按"1 段话讲清 + 实例 + 节点位置 + 练习 + 1 篇/下 1 篇"结构
5. **改状态**:写完把 🟡 改成 🟢
6. **本地预览**:`python scripts/serve-nocache.py` → 浏览器开 `http://127.0.0.1:18080/site/`

## 进度

- v0.1:**18 节 P0** = 最小可用 ✅
- v0.5:**50 节 P0+P1** = 学员能看完跑通 ✅
- v1.0:**114 节** + M/N 专题 ✅
- v1.5:**M/N 专题集成 + 全站体检 + 项目清理** ✅ (2026-09-24)

## 参考

- **鱼皮 Vibe Coding 教程**(开发方法):https://ai.codefather.cn/vibe
- **legacy/ 11 份老 HTML**(v4 ~ v17,内容源)
- **AGENTS.md**(项目规范 · 设计决策)

---

## 📮 联系玉哥

| 渠道 | 入口 |
|---|---|
| 🌐 官方网站 | **manju.tuanpiao.work** |
| 📺 B 站 / 抖音 / 小红书 | 搜索「**玉哥漫剧**」 |
| 💬 学员交流群 | 扫码加入(见网站 footer 二维码) |
| 📧 商务合作 | `yuge@manju.local`(占位,请替换) |

> 📌 想看完整联系方式,打开网站 footer 区域(`site/assets/qr-yuge.png`)

---

🤖 项目由玉哥 + Mavis 协作 · 2026-09
