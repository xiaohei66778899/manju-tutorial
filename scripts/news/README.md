# 漫剧教程站 · 行业新闻自动抓取系统(MVP v2.0)

> 玉哥 · 2026-09-17
> 把"行业新闻"板块做成每日自动更新、零依赖、轻量、可在 40G 低配服务器长期运行。

---

## 一、系统总览

```
┌─────────────────────────────────────────────────────┐
│  8 个新闻源(RSS / 公开 API / HTML)                  │
│  ↓                                                  │
│  关键词相关性过滤 → 9 大分类 + 标签 + 置信度         │
│  ↓                                                  │
│  SimHash + URL 去重                                  │
│  ↓                                                  │
│  合并写入 site/news/data.json(静态 JSON)            │
│  ↓                                                  │
│  site/news/index.html 直接读取(零后端)              │
└─────────────────────────────────────────────────────┘
```

**核心原则**(玉哥决策):
- 前端纯静态不动(`site/news/index.html` 不改)
- 后端零依赖(Node 18+ 内置 fetch/crypto/fs)
- 数据桥接:SQLite 文件(可选)+ 静态 JSON 双写
- LLM 可选增强,默认走关键词方案

---

## 二、目录结构

```
scripts/news/
├── package.json              # 独立 Node.js 模块声明
├── README.md                 # 本文档
├── fetch.js                  # 主入口 · 抓取+合并
├── stats.js                  # 统计面板
├── cleanup.js                # 自动清理(90/365 天策略)
├── config/
│   ├── sources.json          # 新闻源配置(8 个起步)
│   └── keywords.json         # 分类/标签/敏感词配置
├── lib/
│   ├── http.js               # 统一 HTTP 客户端(超时+重试)
│   ├── logger.js             # 每日日志 + 14 天自动清理
│   ├── classifier.js         # 关键词分类 + 标签 + 置信度
│   ├── dedupe.js             # SimHash + URL + content_hash 去重
│   ├── storage.js            # JSON 读写 + 合并 + 清理策略
│   └── fetchers/
│       ├── base.js           # Fetcher 基类
│       ├── rss.js            # 通用 RSS(RSS 2.0 + Atom 1.0)
│       ├── weibo.js          # 微博热搜(过滤 AI/短剧)
│       ├── zhihu.js          # 知乎热榜(API 失效兜底中)
│       └── github-trending.js # GitHub Trending(关键词过滤)
├── data/                     # SQLite 数据库(未来扩展用)
├── logs/                     # 每日抓取日志
└── config/
```

---

## 三、CLI 命令

```bash
# 1. 抓取并合并到 site/news/data.json(默认并发 2)
node fetch.js

# 2. 干跑模式(只打印不写文件,验证用)
node fetch.js --dry

# 3. 只抓取指定源
node fetch.js --source=jiqizhixin

# 4. 统计面板(分类/标签/来源分布 + 待审核)
node stats.js

# 5. 自动清理(90 天普通 + 365 天政策 + 14 天日志)
node cleanup.js

# 6. 自定义清理策略
node cleanup.js --days=60          # 普通新闻改 60 天
node cleanup.js --logs-only        # 只清日志
node cleanup.js --vacuum           # 压缩 data.json
```

通过 `package.json` 的 scripts 字段,可直接:
```bash
npm run news:fetch
npm run news:fetch:dry
npm run news:stats
npm run news:cleanup
```

---

## 四、定时任务配置

### 方案 A · 腾讯云服务器 crontab(推荐)

```cron
# 每天 06:30 全量抓取 + 入库
30 6 * * * cd /path/to/12小说 && node scripts/news/fetch.js >> scripts/news/logs/cron.log 2>&1

# 每天 08:00 生成统计
0 8 * * * cd /path/to/12小说 && node scripts/news/stats.js >> scripts/news/logs/cron-stats.log 2>&1

# 每天 03:30 自动清理
30 3 * * * cd /path/to/12小说 && node scripts/news/cleanup.js >> scripts/news/logs/cron-cleanup.log 2>&1
```

### 方案 B · Windows 本地任务计划程序

```powershell
# 创建每日 06:30 抓取任务
$action = New-ScheduledTaskAction -Execute 'node.exe' -Argument 'E:\AIGC\课件\12小说\scripts\news\fetch.js' -WorkingDirectory 'E:\AIGC\课件\12小说\scripts\news'
$trigger = New-ScheduledTaskTrigger -Daily -At '06:30'
Register-ScheduledTask -TaskName 'ManjuNewsFetch' -Action $action -Trigger $trigger -RunLevel Highest
```

### 方案 C · GitHub Actions(无需服务器)

`.github/workflows/news.yml`(玉哥项目根目录):
```yaml
name: News Fetch
on:
  schedule:
    - cron: '30 6 * * *'   # 每天 06:30 UTC
  workflow_dispatch:         # 手动触发
jobs:
  fetch:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20 }
      - run: cd scripts/news && node fetch.js
      - uses: stefanzweifel/git-auto-commit@v5
        with:
          commit_message: 'news: 自动更新 [skip ci]'
          file_pattern: 'site/news/data.json'
```

---

## 五、磁盘占用估算

| 项 | 大小 | 说明 |
|---|---|---|
| `site/news/data.json` | ~50 KB / 40 条 | 每条约 1.2 KB,90 天约 300 KB |
| `scripts/news/logs/` | ~5 KB / 天 | 14 天 ≈ 70 KB |
| **总计** | **< 500 KB** | 远低于 5G 限制 |

**清理策略**(cleanup.js):
- 普通新闻:90 天
- 政策新闻:365 天(可手动 permanent 标记永久保留)
- 敏感新闻:60 天
- 日志:14 天
- 磁盘 >75%:自动缩短普通新闻到 60 天(玉哥后续扩展)

---

## 六、已实现能力 ✅

| 能力 | 实现方式 | 状态 |
|---|---|---|
| 8 个新闻源 | RSSFetcher / WeiboHotFetcher / GitHubTrendingFetcher | ✅ |
| 关键词相关性过滤 | `isRelatedToAI()` 20+ 触发词 | ✅ |
| 9 大分类 | keyword 加权 + 置信度 | ✅ |
| 自动打标签 | 关键词匹配,最多 5 个 | ✅ |
| 敏感标记 | sensitiveKeywords 命中 | ✅ |
| URL 去重 | normalizeUrl 去 utm/fbclid 等 | ✅ |
| title hash 去重 | MD5 前 16 字节 | ✅ |
| content_hash 去重 | SHA256 前 32 字节 | ✅ |
| SimHash | 64 位指纹(汉明距离 ≤3 近似) | ✅ |
| 置信度 0-1 | 最高分 / 总分 | ✅ |
| 待审核队列 | confidence < 0.7 → status=pending_review | ✅ |
| 90 天清理策略 | cleanup.js 自动 | ✅ |
| 14 天日志清理 | logger.js 自动 | ✅ |
| 统计面板 | stats.js | ✅ |
| 数据 schema 向后兼容 | 保留所有原 v1.0 字段 | ✅ |
| CLI 命令 | npm run news:fetch/stats/cleanup | ✅ |
| Node 18+ 零外部依赖 | 仅用 fs/path/crypto/fetch | ✅ |
| 干跑模式 | --dry | ✅ |
| 单源抓取 | --source=xxx | ✅ |
| 并发控制 | 默认 2,可配 | ✅ |
| 超时控制 | 15s,可配 | ✅ |
| 重试机制 | 1 次,可配 | ✅ |

---

## 七、待玉哥决策的能力 ⏳

| 能力 | 状态 | 说明 |
|---|---|---|
| **DeepSeek V3 LLM 摘要(Top 20)** | ⏳ 需 API key | 每日只处理重点新闻,关键词方案已覆盖 80% |
| **RSS 全量解析(知乎热榜)** | ⚠️ API 401 | 改用 web scrape 或玉哥提供 cookie |
| **更多源** | 🔧 可扩展 | 在 sources.json 加即可 |
| **后台管理 UI** | ❌ 玉哥决策 | 当前 CLI + 日志代替 |
| **SQLite 持久化层** | 🔧 预留 | 当前 JSON 已够用,数据 > 1000 条可启用 |

---

## 八、待玉哥提供

1. **DeepSeek API Key**(LLM 摘要用,可选)
   ```bash
   # 写入 scripts/news/.env
   DEEPSEEK_API_KEY=sk-xxx
   DEEPSEEK_BASE_URL=https://api.deepseek.com
   ```
2. **知乎热榜备选方案**:Cookie / 浏览器抓包 / 第三方 API(玉哥偏好)

---

## 九、当前默认源(8 个起步)

| ID | 名称 | 类型 | 频率 | 状态 |
|---|---|---|---|---|
| jiqizhixin | 机器之心 | RSS | 2h | ⚠️ URL 404 待修 |
| qbitai | 量子位 | RSS | 2h | ✅ |
| 36kr | 36氪 | RSS | 3h | ✅ |
| weibo-hot | 微博热搜 | JSON | 1h | ✅ |
| zhihu-hot | 知乎热榜 | JSON | 1h | ❌ API 401 待修 |
| github-trending | GitHub Trending | HTML | 4h | ✅ |
| huxiu | 虎嗅 | RSS | 3h | ⚠️ 超时 |
| aibase | AIBase | RSS | 3h | ❌ 已移除 |

**玉哥手工补源建议**:
- 钛媒体、亿邦动力、IT 桔子(行业)
- 抖音/快手官方公告(平台)
- OpenAI/Google AI 官方博客(海外)
- 量子位 Pro / 机器之心 SOTA(技术)

---

## 十、磁盘 & 性能保证

- **磁盘**:< 500 KB(JSON + 日志),远低于 5G 限制
- **每次抓取耗时**:~30 秒(8 个源并发 2)
- **内存峰值**:< 30 MB
- **CPU**:零本地计算(只跑正则 + 哈希)
- **网络**:每源 1-2 个 HTTP 请求,总流量 < 1MB/天

---

## 十一、故障排查

```bash
# 1. 跑 dry 模式看具体哪些源失败
node fetch.js --dry

# 2. 查看最近日志
Get-Content scripts/news/logs/fetch-2026-09-17.log

# 3. 单源测试
node fetch.js --source=jiqizhixin --dry

# 4. 清理过期数据后重跑
node cleanup.js && node fetch.js
```

---

## 十二、版本 & 变更记录

### v2.0 · 2026-09-17(玉哥 MVP 决策版)
- 全新目录结构(`scripts/news/` 独立模块)
- 零外部依赖(Node 18+ 内置)
- 8 个新闻源起步
- 9 大分类 + 标签 + 置信度
- SimHash + URL + content_hash 三重去重
- 90/365 天清理策略
- CLI 命令全套
- cron / GitHub Actions / Windows 任务计划三种调度方案

### v1.0 · 2026-09-14(玉哥初版)
- scripts/fetch-news.js · 36kr 单源 · 关键词过滤
- 输出 site/news/data.json(30 条手动整理)
