# 📋 部署前全面体检 Code Review Prompt

> **项目**: 玉哥漫剧制作教程站  
> **目标域名**: `<你的域名>` (`.work` TLD 或其他)  
> **部署平台**: Netlify (自动读 `netlify.toml`)  
> **项目根目录**: `E:\AIGC\课件\12小说\`
> **部署子目录**: `site/` (Netlify publish=site)
> **本机预览服务器**: `http://127.0.0.1:18080/site/`

---

## 🎯 你的任务

对**玉哥漫剧制作教程站**做一次**全面、独立的部署前体检**。这是一个**纯静态 HTML 网站**,包含 ~225 个教程页面,准备部署到 `<你的域名>`。

请以**独立审计员视角**审查,不要相信任何"已修复"的声明 —— **自己动手验证**。重点检查项已列在下方,但请自由扩展你认为必要的检查维度。

---

## 📂 项目背景(必读,避免重复劳动)

项目已在 2026-09-27 完成一轮 M3 模型修复,以下项目**已修复/已存在**,你**不需要重复做**,但**请独立验证**这些修复是否真的正确:

### 已修复/已配置(请验证)
| 项 | 状态 | 验证方式 |
|---|---|---|
| `site/404.html` 重写 | 已完成 | 打开看是否干净中文 + UTF-8 BOM |
| `site/sitemap.xml` 生成 | 157 URL · 24 KB | 检查 URL 完整性 |
| `site/favicon.svg` 紫蓝渐变"漫"字 | 已生成 + 注入 153 页 | 检查是否所有页面路径正确 |
| `.gitignore` 加 N-repos/M-mp4/私人资料 | 已加 | 检查是否覆盖到位 |
| `netlify.toml` 加 `[[build.ignore]]` 6 条 | 已加 | 验证 ignore 模式正确性 |
| 3 个乱码 ref(C-4 / C-13 / C-16) | 已修 | 验证指向真实文件 |
| `.github/workflows/news.yml` 乱码 | 已删 | 验证目录干净 |
| 根目录临时脚本(check_*.py 等 9 个) | 已删 | 验证根目录干净 |
| cache 版本号 `?v=fix20260927-2215` | 已统一 | 验证全站一致 |

### 已验证(请复核)
- ✅ 全站 225 个 HTML `200 OK`(本地服务器 `http://127.0.0.1:18080/site/`)
- ✅ 部署范围(去掉 N-repos 后 157 个 HTML)内部链接 2562 个,**0 个真死链**
- ✅ `node --check site/assets/site-enhance.js` 无语法错误
- ✅ 最终部署体积 268.8 MB(原始 4.4 GB,忽略后节省 93.9%)
- ✅ 最大单文件 11.27 MB(M-seedance 音频),在 Netlify 50 MB 限制内

### 已知保留项(玉哥私人资料,不需要动)
- `视频直链清单.txt` (玉哥私人清单,根目录)
- `飞书脑图_AI漫剧短剧制作全流程_avocado/` (玉哥飞书导出的资料)
- `site/tutorial/N-aixiexiaoshuo/repos/` (1.2 GB GitHub 仓库合集,**netlify.toml 已 ignore,不部署**)
- `site/tutorial/M-seedance/{tutorials,workflows,official-demos}/*.mp4` (海外教程视频,**netlify.toml 已 ignore**)

### 玉哥的设计定稿(不要改主色)
- **玉哥暖色 v3 主色**:`#635BFF` 紫蓝,`--bg #FFFCF6` 暖白
- **Hero 渐变**:`#FFE9D6 → #FFF7E8 → #ECE7FF`
- **Topbar**:56px 固定,active 用 `#635BFF !important`
- **M 专题 Seedance**:**保留冷蓝** `#3B72F0`(玉哥指定)
- **N 专题 AI 写小说**:**保留浅蓝** `#EEF3FB → #FAFBFC`(玉哥指定)

---

## 🔍 必查清单(请独立验证)

### 1️⃣ 部署配置审查(高优先级)
- [ ] `netlify.toml` 配置是否正确(`publish=site` · 缓存头 · 安全头 · ignore 规则 · 404 兜底)
- [ ] 部署体积是否真的在平台限制内
  - Netlify:50 MB/单文件 · 无限总量
  - Cloudflare Pages:25 MB/单文件(备选)
- [ ] `.gitignore` 是否覆盖 `site/tutorial/N-aixiexiaoshuo/repos/` 整个目录
- [ ] `netlify.toml` 的 `[[build.ignore]]` 规则是否与 `.gitignore` 一致
- [ ] `.nojekyll` 是否存在(Netlify 必须,避免 _headers 等被 Jekyll 误处理)
- [ ] `robots.txt` 是否禁爬 N-repos(虽然部署已排除,SEO 仍需)

### 2️⃣ HTML 质量审查
- [ ] 抽样 5-10 个 HTML,验证:
  - `<title>` 是否合理(每页独立标题,不要全站一个)
  - `<meta name="description">` 是否每页有
  - OG tags(`og:title` `og:description` `og:image` `og:url`)是否关键页都有
  - `<link rel="canonical">` 是否设置(避免重复内容)
  - `lang="zh-CN"` 是否设置
  - viewport meta 是否移动端友好
- [ ] 玉哥暖色 / M 冷蓝 / N 浅蓝 三套样式是否互不污染

### 3️⃣ 资源 / 加载审查
- [ ] favicon 是否全站 200(子目录 HTML 的相对路径)
- [ ] `assets/site.css?v=fix20260927-2215` 是否全站引用一致
- [ ] `assets/site-enhance.js?v=fix20260927-2215` 是否全站引用一致
- [ ] 是否有 404 的图片/视频/音频资源

### 4️⃣ 性能审查
- [ ] 大文件清单(>500 KB 的 HTML/图片/视频)
  - M-seedance 即梦实操课.html 2.1 MB(已知)
  - N-aixiexiaoshuo AI 写小说实战课.html 737 KB(已知)
  - prompts/image-prompts.html 451 KB(已知)
- [ ] 是否需要拆分/压缩/懒加载
- [ ] 图片格式:是否有用 WebP / AVIF(替代 jpg/png)

### 5️⃣ 可访问性(a11y)
- [ ] 图片 `alt` 属性是否齐全
- [ ] 链接文字是否清晰(不要"点击这里")
- [ ] 标题层级是否合理(h1 → h2 → h3)
- [ ] 颜色对比度(玉哥暖色 + 紫蓝 active 是否通过 WCAG AA)

### 6️⃣ SEO 审查
- [ ] `sitemap.xml` 是否完整(157 URL 是否覆盖所有重要页面)
- [ ] 每页 OG tags 是否齐全(社交分享卡片)
- [ ] 是否需要 JSON-LD 结构化数据(`@type: Course` / `@type: Article`)

### 7️⃣ 安全审查
- [ ] `netlify.toml` 安全头是否合理
  - `X-Frame-Options: DENY`(防 clickjacking)✅
  - `X-Content-Type-Options: nosniff` ✅
  - `Referrer-Policy: strict-origin-when-cross-origin` ✅
  - `Permissions-Policy: geolocation=(), microphone=(), camera=()` ✅
- [ ] 是否有暴露的私人文件(配置错误导致)
- [ ] `404.html` 是否泄露服务端信息

### 8️⃣ 跨浏览器 / 设备
- [ ] mobile responsive(媒体查询是否到位)
- [ ] 暗色模式(`data-theme="dark"`)是否所有页面支持
- [ ] iPhone 安全区 `env(safe-area-inset-*)` 是否生效
- [ ] 微信 web-view / 小程序 web-view 兼容性

### 9️⃣ 代码风格审查
- [ ] HTML 是否规范(每个 meta 标签闭合、属性引号一致)
- [ ] 是否有遗留的调试代码(`console.log` / `alert` / TODO 注释)
- [ ] 内联 `<style>` 是否过多(应该统一在 site.css)

### 🔟 我可能漏掉的关键问题
- [ ] 部署流程:玉哥如何操作?git push 后 Netlify 自动部署?
- [ ] DNS:`<你的域名>` 是新域名,NS 在哪家管(国内服务商 / Cloudflare)?
- [ ] SSL:Netlify 自动 Let's Encrypt(`.work` 支持)还是需要手动配?
- [ ] CDN:Netlify 全球 CDN,国内访问速度(玉哥目标用户是国内吗?)
- [ ] 备份:站点数据是否需要定期备份到 GitHub 之外?

---

## 📋 输出格式要求

请按以下结构输出报告:

```markdown
# 🔍 Code 独立体检报告

## 总评
- 评级:[A/B/C/D]
- 一句话总结:[是否可以部署?还需要修什么?]

## ✅ 验证通过
[列出你独立验证通过的项目,每项一行]

## ⚠️ 发现的问题
### P0 - 阻塞部署(必须修)
[具体文件 + 具体行号 + 具体修改建议]

### P1 - 重要改进(部署后修)
[同上]

### P2 - 锦上添花(可选)
[同上]

## 💡 我(M3)可能漏掉的盲区
[你认为 M3 一轮修复可能漏掉的问题,任何维度都行]

## 🚀 部署建议
[Netlify 操作步骤 + DNS 配置 + 验证清单]

## ❓ 需要玉哥决定的事
[玉哥还没确认的关键决策]

## 详细发现(逐项)
[每项发现的:文件名:行号 + 问题描述 + 推荐修复方案]
```

---

## 🛠️ 工具提示

你可以使用以下工具验证:

```powershell
# 本地预览(玉哥电脑已运行,端口 18080)
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:18080/site/

# 检查 HTML
Get-Content site\index.html -Encoding UTF8 | Select-Object -First 50

# 扫描所有 HTML
Get-ChildItem site -Filter *.html -Recurse | Measure-Object

# grep 检查
grep -r "console.log" site/
grep -r "TODO" site/
grep -r "FIXME" site/

# Python 检查
python -c "import urllib.request; ..."

# 检查大文件
Get-ChildItem site -Recurse | Where-Object {$_.Length -gt 1MB} | Sort-Object Length -Descending
```

---

## ⚠️ 重要约束

1. **不要修改玉哥暖色 v3 主色**(除非有明确 WCAG 对比度问题)
2. **不要覆盖 M 专题冷蓝 / N 专题浅蓝**
3. **不要重写 site-enhance.js**(已通过 node --check 语法验证)
4. **不要重新生成 sitemap.xml**(已 157 URL)
5. **不要清理根目录**(已经清理过)
6. **不要动 `视频直链清单.txt` / `飞书脑图_*/`**(玉哥私人资料)
7. **不要 git 操作**(除非玉哥明确要求)
8. **给可执行建议,不要空话** —— 玉哥要的是 5 分钟能部署上线

---

## 📊 参考指标

| 指标 | 当前值 | Netlify 限制 |
|---|---|---|
| 部署体积 | 268.8 MB | 无限 |
| 单文件最大 | 11.27 MB | < 50 MB |
| HTML 总数 | 225 个 | - |
| 部署范围 HTML | 157 个(去 N-repos) | - |
| 内部链接 | 2562 个 | - |
| 真死链 | 0 个 | - |
| cache 版本 | `fix20260927-2215` | - |

---

> 准备好后,请开始独立审查。**重点是发现 M3 一轮修复可能漏掉的盲区**。  
> 输出报告后,**不要自动修改任何文件** —— 等玉哥确认。