# AGENTS.md

This workspace is a static HTML knowledge site for a Chinese AI short-drama tutorial project. The goal is to publish a tutorial site with many one-page lessons under `site/tutorial/`, while keeping the project lightweight and easy to browse locally.

## Project shape

- `README.md`: main project overview, site structure, style guide, and authoring workflow.
- `PLAN.md`: full task list for all tutorial sections (`A`–`I`) and their priority/status.
- `site/`: main tutorial website.
  - `site/index.html`: homepage.
  - `site/tutorial-template.html`: reusable template for each lesson page.
  - `site/tutorial/<category>/`: per-category lesson pages such as `A-manju-basic/`, `B-novel-to-script/`, etc.
  - `site/assets/site.css`: shared styling.
- `legacy/`: read-only historical HTML course material, used as content source.
- `_brainmap/`: planning artifacts from the design process.

## Working conventions

- This project is primarily static HTML/CSS. There is no build step, package manager, or automated test suite.
- Prefer editing existing HTML pages directly. When creating a new tutorial page, match the structure and tone of `site/tutorial-template.html`.
- Keep the site fully local and dependency-free. Do not add external JS/CSS unless explicitly requested.
- Use Chinese content and keep the existing “玉哥” style unless the task says otherwise.
- Keep navigation and page layout consistent with the existing site. Major structure includes:
  - top navigation bar
  - left-side section directory
  - main article content
  - bottom “上一节 / 下一节” navigation

## Important workflows

1. Start from the existing project docs before editing:
   - [README.md](README.md)
   - [PLAN.md](PLAN.md)
   - [site/tutorial-template.html](site/tutorial-template.html)
2. For a new lesson page, create or update the relevant file under `site/tutorial/<category>/` and use the same HTML structure as the template.
3. If a page is part of the content plan, update the corresponding task status in [PLAN.md](PLAN.md) only when the page is actually completed.
4. For content sourcing, prefer existing material in [legacy/](legacy/) and the planning notes in `_brainmap/` rather than inventing new structure from scratch.

## Quality bar for AI agents

- Preserve consistent filenames, section IDs, and breadcrumbs.
- Do not break links between pages or the homepage.
- Keep content concise, practical, and tutorial-oriented.
- When adding new pages, follow the pattern of one lesson per HTML file with a clear intro, examples, exercises, and next/previous navigation.
- If you need to add new folders or pages, keep them aligned with the category naming in the project plan.

## Useful references

- [README.md](README.md)
- [PLAN.md](PLAN.md)
- [site/index.html](site/index.html)
- [site/tutorial-template.html](site/tutorial-template.html)
- [site/assets/site.css](site/assets/site.css)
- [legacy/](legacy/)

## Suggested next customizations

If more customization is needed later, a focused follow-up could add:
- a `skills/` file for tutorial authoring conventions
- a specialized `AGENTS.md` for `site/tutorial/` content creation
- a reusable prompt for generating new lesson pages from the template

## Current design decisions (玉哥定稿 2026-09-18)

### Visual system v3 (玉哥暖色调)
- 配色:`#FFFCF6 / #FFF7E8 / #F7EFDC / #E8DFC8 / #1F1A14 / #6F6657`
- Hero 渐变:`#FFE9D6 → #FFF7E8 → #ECE7FF`
- 玉哥亲自署名(非"老师"/"阿白"),元数据已清理

### Topbar (锁定)
- 高度:56px 固定(`height/min-height/max-height: 56px; overflow: hidden`)
- 背景:`var(--bg2)` = `#F7EFDC`
- nav 项:`flex-wrap: nowrap; overflow-x: auto`(横向滚动)
- active 高亮(玉哥最后定稿):
  ```css
  color: #635BFF !important;      /* hard-code 紫蓝,不用 var() */
  font-weight: 500 !important;
  background: transparent !important;
  position: relative !important;
  ```
  + `::after` 伪元素绝对定位底部 2px 蓝条,`background: #635BFF !important`
- 已知陷阱:玉哥"看不到 active 颜色"是 CSS 变量 `var(--blue-deep)` 解析丢失,改 hard-code + `!important` 彻底解决。

### Footer 方案 D (单列居中纵向堆叠,Apple/Netflix 风)
- 结构:`品牌 → 副标题 → QR 占位 → 链接(inline · 分隔)→ 版权`
- 全站 140+ 页面已批量推送

### Server
- `scripts/serve-nocache.py` 用 **ThreadingHTTPServer**(多线程),不再用单线程 http.server
- 端口固定 **18080**(服务器根目录 = 项目根目录,访问路径须加 `/site/` 前缀)
- 响应头:`Cache-Control: no-store, no-cache, must-revalidate, max-age=0`
- 启动:`scripts/start-server.cmd`(后台,无窗口)

### Cache-busting
- 当前版本:`?v=fix20260924-1900`
- 升级方式:`python scripts/bump-cache-v6.py`(每次改完资源后必跑,推新版本号)
- HTML 内 `<link rel="stylesheet" href="(相对路径)assets/site.css?v=fix20260924-1900">`
- JS:`<script src="...site-enhance.js?v=fix20260924-1900">`

### Scripts 目录(35 个 · 2026-09-24 清理后)
- **Server 核心**:`serve-nocache.py`
- **Cache-bust**:`bump-cache-v5.py` `bump-cache-v6.py`(只留最新版) · `bump-site-css-v2.py` · `bump-tutorial-cache.py` · `check-cache.py`
- **Cleanup 系列**(玉哥语气词清理 · 已执行过):`clean-yuanban-phase2/3/suffix.py` + `clean-sidebar-titles.py` `clean-index-words.py` `clean-double-script-close.py`
- **Fix 系列**:`fix-jubens-redirect-paths.py` `fix-tutorial-index-jubens.py` `fix-yuge-qr-path.py` / `-2.py` `remove-comfyui-sections.py`
- **Footer 系列**:`rewrite-footer.py` / `push-compact-footer.py` / `sync-compact-footer.py`
- **Scan 系列**:`scan-yuge-residue.py` `scan-yuge-shuo-residue.py` `classify-yuge-residue.py`
- **Misc**:`append-responsive-css.py` `add-view-bottom-nav.py` `restore-yuge-zhuanlan.py` `deploy-yuge-qr.py` `guard-server.py`
- **Test/Verify**:`test-sidebar-router.py` `test-get-tutorial-href.py` `url-join-test.py` `e2e-sidebar-test.py` `verify-sidebar-href.py` `verify-group-entry.py` `_test-remove.py`

### M 专题(Seedance 即梦实操课) — 2026-09-24 集成
- 路径:`site/tutorial/M-seedance/Seedance即梦实操课.html`
- **风格保留**:不覆盖玉哥暖色,保持原版冷蓝 `#3B72F0` 浅蓝渐变 hero
- **inline `<style>` 覆盖**:`body.seedance-page .hero` / `.chapter` / `.stats-card`(特异性 `.seedance-page .xxx`)
- ⚠️ **AI agent 修改警告**:改玉哥主样式前先看此专题是否被 inline 样式压倒。优先级:`inline <style>` > site.css

### N 专题(AI 写小说实战课) — 2026-09-24 集成
- 路径:`site/tutorial/N-aixiexiaoshuo/AI写小说实战课.html`
- 资源:`articles/`(12 篇) + `tutorials/`(15 章) + `repos/`(16 个 GitHub 仓库 661 MB · `robots.txt` 已禁爬) + `_shots/`(60 张) + 4 个 .md
- **风格保留**:不覆盖玉哥暖色,浅蓝渐变 hero `#EEF3FB → #FAFBFC`
- **inline `<style>` 覆盖**:`body.ainovel-page .xxx`(特异性 `.ainovel-page .xxx`)
- **sidebar 让出 topbar**:`.sidebar top: 0 → 56px`(让出玉哥 56px topbar)
- **mobile menu-toggle**:translateX 切换
- ⚠️ **AI agent 修改警告**:此专题内含极少量腾讯字体外链,主站其他页面不动

### Legacy — 单一源 `site/legacy/`
- **位置**:`site/legacy/`(11 份 HTML v4~v17,353 KB)← **唯一源,直接在 Netlify 部署内**
- 改这里就生效,无需同步(因为 junction 双源已合并,2026-09-24)
- 历史备份位置:`D:\share\9月21号\教学网站\legacy\`(玉哥共享目录,9月24日数据恢复来源)

### 已删除(历史记录)
- `B-novel-to-script/` 整个目录(18 文件,335 KB)· 改并入 `index.html` 锚点
- 临时调试页 `debug-nav.html` 已删
- 项目根 21 个冗余文件:9 个 `剧本-XX-xxx.html` + `剧本.html` + `NOL` + `tmp-*.html` + `start-server.bat/ps1` + 5 个 `.log` + `网站结构规划.md`
- `site/server.err.log` `site/server.log` `scripts/server-err.log` `scripts/server-out.log`
- `_debug-archives/`(305 MB · 56 个浏览器快照)
- `_brainmap/`(21 MB · 279 项规划草稿)
- `scripts/bump-cache-v2/v3/v4.py`(老版本)
- `scripts/clean-yuge-*.py` × 7(一次性 cleanup,玉哥语气词清理已执行完毕)
- **根目录 `legacy/`**(junction 双源合并,统一保留 `site/legacy/`)
- **`site/legacy/README.md`**(双源说明,合并后无需"部署副本"说明,已删)
- **根目录 `legacy/README.md`**(双源说明,合并后无需,已删)
