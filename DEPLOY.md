# 漫剧教程站 · 部署文档(5 步上线)

> 玉哥 · 2026-09-14(初版)· 2026-09-24(同步 Netlify 配置 + cache-bust)
> 阿白你按这个文档走,5 分钟把网站部署到公网。

> **2026-09-27 体检更新**:加 `manju.tuanpiao.work` 域名部署指引 · sitemap.xml · favicon · 404.html 重写 · .gitignore + netlify.toml 双层 ignore 排除 N 专题 1.2 GB 仓库 + M 专题 2.6 GB 视频。

---

## 准备工作 · 2 件事

| 准备 | 用途 | 成本 | 时间 |
|---|---|---|---|
| **GitHub 账号** | 存代码 + 触发 Actions | 免费 | 已有就用 |
| **Netlify 账号** | 部署 + 域名 | 免费层够用 | 5 分钟注册 |
| **域名**(可选) | 绑定 `yourname.com` | ¥30-80/年 | 10 分钟买 |

**本地预览**(可选)· 端口 **18080**:
```powershell
cd E:\AIGC\课件\12小说
python scripts\serve-nocache.py
# 浏览器开 http://127.0.0.1:18080/site/
```

---

## 项目部署文件(已就绪 · 无需手写)

| 文件 | 作用 |
|---|---|
| `netlify.toml` | publish = `site/` · 缓存策略 · 安全头 · 404 → `404.html` · **ignore 规则** 排除 N 专题 1.2 GB 仓库 + M 专题 2.6 GB 视频 |
| `.nojekyll` | 告诉 Netlify 不走 Jekyll 处理(避免下划线文件被忽略) |
| `robots.txt` | 搜索引擎规则(禁爬 `N-aixiexiaoshuo/repos/`,避免 661MB 仓库被索引) |
| `.gitignore` | 拦截 `*.log` / `*.pyc` / `tmp-*` / `__pycache__` / N-repos / M-mp4 / 玉哥私人资料 等 |
| `site/sitemap.xml` | 157 个页面 URL 索引,提交 Google Search Console / 百度站长平台 |
| `site/favicon.svg` | 玉哥"漫"字 favicon(紫蓝渐变),已注入 153 个 HTML 页面 |
| `site/404.html` | 玉哥暖色 404 兜底卡片(5 个核心入口) |

---

## 第 1 步 · 推代码到 GitHub(2 分钟)

1. 注册/登录 [github.com](https://github.com)
2. 点 `+` → `New repository` → 仓库名:**`manju-tutorial`**(或任意名)
3. 选 `Public` → 不要勾 Add README → 创建
4. **在你电脑上**,打开 PowerShell 跑:

```powershell
cd E:\AIGC\课件\12小说
git init
git add .
git commit -m "v1.5 教程站(M/N 集成 + 全站清理)"
git branch -M main
git remote add origin https://github.com/<你的用户名>/manju-tutorial.git
git push -u origin main
```

> 如果提示登录,按提示输入 GitHub 用户名 + Personal Access Token(在 GitHub → Settings → Developer settings → Personal access tokens 生成)

**完成后**:GitHub 仓库里有所有代码(含 netlify.toml / .nojekyll / robots.txt)。

---

## 第 2 步 · Netlify 部署(1 分钟)

1. 打开 [app.netlify.com](https://app.netlify.com/) → 用 GitHub 登录
2. 点 **`Add new site`** → **`Import an existing project`**
3. 选 **`GitHub`** → 选你刚建的 `manju-tutorial` 仓库
4. Netlify 会**自动读取**根目录 `netlify.toml`,无需手动配 Build / Publish:
   - **Branch to deploy**:`main`
   - **Build command**:留空(纯静态)
   - **Publish directory**:`site`(从 netlify.toml 读取)
5. 点 **`Deploy site`**

**完成后**:Netlify 给你一个随机域名,例如:
```
https://manju-tutorial-abc123.netlify.app
```

这个域名立刻能访问!🎉

---

## 第 3 步 · 绑定自己的域名(2 分钟,可选)

如果你买了自己的域名(`manju.tuanpiao.work` 之类):

1. 在 Netlify 控制台 → 你的 site → **`Domain settings`**
2. 点 **`Add custom domain`** → 输入 `manju.tuanpiao.work` → `Verify`
3. Netlify 给你 4 个 NS 记录(类似 `dns1.p01.nsone.net`)
4. 去你买域名的服务商(阿里云/腾讯云/Cloudflare)→ DNS 设置 → 改 NS 记录为 Netlify 提供的
5. 等 5-30 分钟(全球 DNS 生效)
6. Netlify 自动签发 HTTPS 证书(Let's Encrypt 免费)

**完成后**:`https://manju.tuanpiao.work` 全网可访问,带 https 锁标。

### 3.1 绑子域名(如 `manju.tuanpiao.work` 主域 / `www.tuanpiao.work` 别名)

`.work` 是国际 TLD,Let's Encrypt 全支持,Netlify 自动签发证书不用额外操作。

**DNS 在阿里云/腾讯云设置**(以 `tuanpiao.work` 域名为例):
- 类型 `CNAME` · 主机记录 `manju` · 记录值 `<你的站点>.netlify.app` · TTL 600
- 类型 `CNAME` · 主机记录 `www` · 记录值 `<你的站点>.netlify.app` · TTL 600

**DNS 在 Cloudflare 设置**(推荐,免备案 + CDN 加速):
- 类型 `CNAME` · 名称 `manju` · 目标 `<你的站点>.netlify.app` · 代理开启(橙色云朵)

> Cloudflare 走代理后,玉哥站走 Cloudflare CDN 国内访问速度更快,无需备案。

---

## 第 4 步 · 缓存策略与资源更新

**缓存配置**(已在 `netlify.toml`):
- HTML:`Cache-Control: no-cache`(每次访问 Netlify 都重新发)
- CSS/JS:`Cache-Control: public, max-age=31536000, immutable`(1 年强缓存)
- 图片:`Cache-Control: public, max-age=31536000, immutable`

**Cache-bust 机制**(玉哥专用):
- 当前版本:`?v=fix20260924-1900`(152 个 HTML/CSS/JS 都带这个版本号)
- 改完资源后跑:`python scripts\bump-cache-v6.py` → 自动推新版本号 → 强制所有 CDN 边缘失效旧版
- 不跑 cache-bust:用户可能 1 年看不到新样式

---

## 第 5 步 · 验证(1 分钟)

打开浏览器访问:
- `https://<你的域名>` 或 `https://<netlify随机域名>.netlify.app`
- 看首页 5 屏正常显示(RUNOOB 风 · 玉哥暖色)
- 点 **顶栏导航** → 各分类正常切换
- 进 **M 专题**(`Seedance即梦实操课`)→ 看冷蓝 hero · 章节节奏
- 进 **N 专题**(`AI写小说实战课`)→ 看浅蓝渐变 · sidebar 让出 topbar
- 任意 URL 输错 → 跳到 `404.html`(玉哥暖色卡片)
- 改完 push → Netlify 30 秒自动部署

---

## 常见问题

### Q0. 部署时被 Netlify 拒绝"文件超过 50 MB"?
**A**:本项目原 4.4 GB,核心页面 ~150 MB 可直接部署。已通过 `netlify.toml` 的 `[[build.ignore]]` 规则自动排除:
- `site/tutorial/N-aixiexiaoshuo/repos/**`(1.2 GB 仓库合集 · 含 `.git`)
- `site/tutorial/M-seedance/tutorials/*.mp4` 等(2.6 GB 海外教程视频)
排除后页面仍可访问,只是 `*.mp4` 请求会 404(已有 fallback 提示)。

### Q1. 国内访问慢?
**A**:绑 Cloudflare CDN 即可免费加速。Cloudflare → 添加站点 → 改 NS → 自动 CDN + HTTPS。

### Q2. 国内要备案吗?
**A**:海外服务器(Netlify 默认美国)不需备案。国内服务器(阿里云/腾讯云)要 ICP 备案(7-20 天)。
- 玉哥建议:先用 Netlify 海外 → 访问够用,等流量大了再迁国内备案。

### Q3. 域名要多少钱?
**A**:
- `.com` · 国内 ¥65-80/年 · 海外(Cloudflare Registrar)$10/年 ≈ ¥70
- `.cn` · 国内 ¥30/年
- `.top` / `.xyz` · 几块钱

### Q4. 怎么加内容?
**A**:
- 加 1 节教程:`site/tutorial/<类目>/<节名>.html` → 复制 `tutorial-template.html` 改
- 加 1 条新闻:直接编辑 `site/news/data.json`(在 GitHub 网页就能改)
- 改完 git push → Netlify 30 秒自动部署

### Q5. 改了 CSS / JS 但线上没生效?
**A**:跑 `python scripts\bump-cache-v6.py` 推新版本号 → push → Netlify 重新部署
- Netlify 默认 CSS/JS 1 年强缓存(性能优化),不 bump 用户看不到
- HTML 没缓存,改完直接生效

### Q6. 怎么加自定义功能(评论/搜索/会员)?
**A**:
- 评论:加 Disqus 或 Giscus(GitHub 登录)
- 搜索:Netlify 自带 Algolia 集成
- 会员:Netlify Identity(免费 1000 用户)

---

## 升级路径(等你流量大了)

| 阶段 | 触发 | 升级 |
|---|---|---|
| 0-1000 UV/天 | 起步 | Netlify 免费层(够) |
| 1000-10000 UV/天 | 流量起来 | Cloudflare CDN + 缓存 |
| 10000+ UV/天 | 商业化 | 国内备案 + 阿里云 CDN |

---

## 玉哥建议

**今晚**:Netlify 部署 + 绑个便宜域名(`.top` 几块钱一年练手)
**这周**:用 GitHub Actions 抓 3-5 天真实新闻
**下周**:开始写 M/N 专题扩展内容,边写边补 GitHub

有任何问题,直接问"部署卡住了"或"News 不更新",我帮你看。

🤖 玉哥 · 2026-09-14(初版)· 2026-09-24(同步)
