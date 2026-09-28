# 📖 漫剧制作教程站 · 文件导航

> v1.5 全完成 · 114 节 + 6 专题 / 13 大类 · 玉哥整理
> 更新时间:2026-09-24

## 🎯 一、入口直达(打开看效果)

| 类型 | 路径 | 用途 |
|---|---|---|
| 🏠 **首页**(RUNOOB 风格) | [`site/index.html`](site/index.html) | 简洁 hero + 9 大类速通卡片 |
| 📚 **教程列表页**(RUNOOB 风格) | [`site/tutorial/all-courses.html`](site/tutorial/all-courses.html) | 13 大类 114 节全卡片,176px sticky 左侧 |
| 📅 **更新日志** | [`site/changelog.html`](site/changelog.html) | v1.0 里程碑 + 阶段史 |
| 🗂 **玉哥原版课件 20 份** | [`site/legacy/`](site/legacy/) | junction 接入到 `legacy/`,玉哥独立修改 |
| 🎯 **学习路径** | [`site/learning-path.html`](site/learning-path.html) | 5 个教程内部页底部导航引用 |

## 🎬 二、教程节 114 节(8 大类,B 已并入首页锚点)

> 都在 [`site/tutorial/<大类目录>/<节次>.html`](site/tutorial/) 下

| 类 | 目录 | 节数 | 入口页 |
|---|---|---|---|
| **A · 漫剧基础** | [`A-manju-basic/`](site/tutorial/A-manju-basic/) | 8 | [A-1.html](site/tutorial/A-manju-basic/A-1.html) |
| **B · 小说改剧本** | 已并入 [`index.html`](site/index.html) 锚点 + [`剧本.html`](site/剧本.html) SPA | 8 子页 | [剧本.html](site/剧本.html) |
| **C · 角色制作** | [`C-character/`](site/tutorial/C-character/) | 17 | [C-1.html](site/tutorial/C-character/C-1.html) |
| **D · 分镜** | [`D-storyboard/`](site/tutorial/D-storyboard/) | 15 | [D-1.html](site/tutorial/D-storyboard/D-1.html) |
| **E · AI 出图** | [`E-ai-image/`](site/tutorial/E-ai-image/) | 19 | [E-1.html](site/tutorial/E-ai-image/E-1.html) |
| **F · AI 视频** | [`F-ai-video/`](site/tutorial/F-ai-video/) | 18 | [F-1.html](site/tutorial/F-ai-video/F-1.html) |
| **G · 配音剪辑** | [`G-audio-edit/`](site/tutorial/G-audio-edit/) | 18 | [G-1.html](site/tutorial/G-audio-edit/G-1.html) |
| **H · 发布运营** | [`H-publish/`](site/tutorial/H-publish/) | 10 | [H-1.html](site/tutorial/H-publish/H-1.html) |
| **I · 附录速查** | [`I-appendix/`](site/tutorial/I-appendix/) | 9 | [I-1.html](site/tutorial/I-appendix/I-1.html) |

## 📦 三、资源库入口(7 个内页)

| 入口 | 路径 | 说明 |
|---|---|---|
| 🖼 图片作品 | [`site/prompts/image-prompts.html`](site/prompts/image-prompts.html) | AI 出图作品展示 |
| 🎬 视频作品 | [`site/video-prompts/video-prompts.html`](site/video-prompts/video-prompts.html) | AI 视频作品展示 |
| 📋 模板库 | [`site/templates/library.html`](site/templates/library.html) | 模板下载 |
| 🛠 工具箱 | [`site/tools/toolkit.html`](site/tools/toolkit.html) | 工具推荐 |
| ❓ 问题库 | [`site/qa/troubleshooting.html`](site/qa/troubleshooting.html) | 玉哥答疑 |
| 🎞 制作实例 | [`site/instances/showcase.html`](site/instances/showcase.html) | 完整作品实例 |
| 💰 商业化 | [`site/commercial/monetize.html`](site/commercial/monetize.html) | 变现指南 |
| 📰 行业新闻 | [`site/news/industry.html`](site/news/industry.html) | 行业动态 |

## 📁 四、项目根目录结构

```
12小说/
├── 📄 AGENTS.md               ← 项目说明(给 AI agent 看)
├── 📄 PLAN.md                 ← 任务清单 + 状态
├── 📄 README.md               ← 项目总体介绍
├── 📄 DEPLOY.md               ← 部署说明
├── 📄 netlify.toml            ← Netlify 部署配置
├── 📄 robots.txt              ← 搜索引擎规则
├── 📄 .nojekyll               ← Netlify 不走 Jekyll 处理
├── 📄 .gitignore              ← Git 忽略规则
├── 📄 OUTPUT_INDEX.md         ← 本文件(HTML 导航)
│
├── 📂 site/                   ← ⭐ 主交付物(全站 225 个 HTML)
│   ├── index.html             ← 简洁首页(RUNOOB 风格)
│   ├── tutorial/              ← 13 大类(含 M Seedance / N AI 写小说)
│   ├── assets/                ← CSS / JS / 图片
│   ├── prompts/ / video-prompts/ / templates/ / tools/ / qa/ / instances/ / commercial/ / news/
│   └── legacy/                ← 玉哥原版课件 11 份(唯一源,直接部署)
│
├── 📂 scripts/                ← 项目脚本(35 个 · 230 KB)
│   ├── serve-nocache.py       ← 多线程本地 server(端口 18080)
│   ├── bump-cache-v6.py       ← cache-bust 推新版本号
│   ├── fix-*.py               ← 路径修复工具
│   ├── clean-yuanban-*.py     ← 玉哥语气词清理(已执行)
│   └── ...
│
├── 📂 _trash-removed/         ← 玉哥回收站
│
├── 📂 logs/                   ← guard 守护进程日志
│
├── 📂 .github/                ← GitHub Actions 配置
│
└── 📂 飞书脑图_AI漫剧短剧制作全流程_avocado/   ← 飞书导出的脑图
```

## 🚀 五、本地预览

启动 python http server(已跑):

```powershell
cd E:\AIGC\课件\12小说\site
python -m http.server 8765 --bind 127.0.0.1
```

然后浏览器访问:
- 首页:http://127.0.0.1:8765/
- 教程列表:http://127.0.0.1:8765/tutorial/
- 任意一节:http://127.0.0.1:8765/tutorial/A-manju-basic/A-1.html

## 🔍 六、修改入口

| 想改什么 | 编辑这个文件 |
|---|---|
| 顶部 logo / 导航栏 / 搜索框 | [`site/assets/site.css`](site/assets/site.css) 末段 + 各页 `<header class="topbar">` |
| 教程列表页 9 大类卡片 | [`site/tutorial/all-courses.html`](site/tutorial/all-courses.html) 第 254 行起的 `.cat-block` |
| 左侧 sidebar 自动渲染 | [`site/assets/tutorial.js`](site/assets/tutorial.js) 的 `SIDEBAR` 数组 |
| footer 4 列样式 | [`site/assets/site.css`](site/assets/site.css) 的 `.dock-run` 块 |
| 全站 114 节列表状态 | [`site/assets/tutorial.js`](site/assets/tutorial.js) 的 `DONE_PAGES` 集合 |

## 📊 七、当前统计

- HTML 文件总数:**225 个**(114 节 + 13 大类入口页 + 资源内页 + 404)
- 教程节:**114 节**(A 8 / C 17 / D 15 / E 19 / F 18 / G 18 / H 11 / I 9)
- 大类:**13 个**(A/C/D/E/F/G/H/I/J/K/L/M/N · B 已并入 index)
- M 专题(Seedance 即梦):✅已集成
- N 专题(AI 写小说实战课):✅已集成
- 全站 broken link:**0**
- 全站 HTTP 200:**225 / 225 ✓**
- 项目根目录清理:**2026-09-24**(释放 312 MB)
- cache-bust 版本:`fix20260924-1500`
- v1.0 完工日期:**2026-09-16**
- v1.5 完成日期:**2026-09-24**(M/N 集成 + 全站体检 + 项目根清理)