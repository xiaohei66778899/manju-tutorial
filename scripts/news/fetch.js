/**
 * 漫剧教程站 · 行业新闻自动抓取主入口
 *
 * 工作流:
 *   1. 加载 sources.json 配置
 *   2. 实例化对应 fetcher(并发上限 2)
 *   3. 抓取 → 关键词过滤(isRelatedToAI)→ 分类(classify)→ 去重(dedupe)
 *   4. 合并到 site/news/data.json
 *   5. 写入日志
 *
 * 用法:
 *   node fetch.js            # 抓取并合并
 *   node fetch.js --dry      # 只打印不写入
 *   node fetch.js --source=jiqizhixin  # 只抓取指定源
 *
 * 调度建议(腾讯云 crontab):
 *   30 6 * * *  cd /path/to/12小说 && node scripts/news/fetch.js >> logs/cron.log 2>&1
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { info, warn, error, success } from './lib/logger.js';
import { classify, isRelatedToAI } from './lib/classifier.js';
import { dedupe } from './lib/dedupe.js';
import { readDataJson, writeDataJson, mergeArticles } from './lib/storage.js';
import { RSSFetcher } from './lib/fetchers/rss.js';
import { WeiboHotFetcher } from './lib/fetchers/weibo.js';
import { GitHubTrendingFetcher } from './lib/fetchers/github-trending.js';
import { isEnabled as llmEnabled, summarizeBatch } from './lib/summarizer.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const SOURCES_FILE = path.join(__dirname, 'config', 'sources.json');
const DRY_RUN = process.argv.includes('--dry');
const ONLY_SOURCE = process.argv.find(a => a.startsWith('--source='))?.split('=')[1];
const WITH_LLM = process.argv.includes('--with-llm');

const FETCHER_MAP = {
  rss: RSSFetcher,
  json: RSSFetcher,
  html: GitHubTrendingFetcher,
  'weibo-hot': WeiboHotFetcher,
  'github-trending': GitHubTrendingFetcher
};

async function main() {
  info('====== 漫剧教程站 · 行业新闻抓取开始 ======');

  if (!fs.existsSync(SOURCES_FILE)) {
    error('sources.json 不存在', { path: SOURCES_FILE });
    process.exit(1);
  }

  const cfg = JSON.parse(fs.readFileSync(SOURCES_FILE, 'utf-8'));
  const sources = cfg.sources.filter(s => s.enabled !== false);
  const filtered = ONLY_SOURCE ? sources.filter(s => s.id === ONLY_SOURCE) : sources;

  if (filtered.length === 0) {
    warn('没有启用的源,退出');
    process.exit(0);
  }

  info(`启用源 ${sources.length} 个,本次抓取 ${filtered.length} 个`);

  // 并发抓取(上限 2)
  const allItems = [];
  const queue = [...filtered];
  const concurrency = cfg.global.maxConcurrent || 2;

  async function worker() {
    while (queue.length > 0) {
      const src = queue.shift();
      if (!src) break;
      const FetcherClass = FETCHER_MAP[src.id] || FETCHER_MAP[src.type] || RSSFetcher;
      const fetcher = new FetcherClass(src);
      info(`→ 抓取 [${src.id}] ${src.name}`);
      const result = await fetcher.safeFetch();
      if (result.ok) {
        info(`  ✓ 解析到 ${result.items.length} 条 (耗时 ${result.duration}ms)`);
        for (const it of result.items) {
          if (!it.source) it.source = src.name;
        }
        allItems.push(...result.items);
      } else {
        warn(`  ✗ 抓取失败: ${result.error}`);
      }
    }
  }
  await Promise.all(Array.from({ length: concurrency }, () => worker()));

  info(`总计抓取 ${allItems.length} 条`);

  // 1. 关键词相关性过滤(去掉完全不沾边的)
  const related = allItems.filter(it => isRelatedToAI(`${it.title} ${it.summary || ''}`));
  info(`相关性过滤: ${allItems.length} → ${related.length}`);

  // 2. 分类 + 标签
  for (const it of related) {
    const text = `${it.title} ${it.summary || ''}`;
    const cls = classify(text, it._source_default_category || 'tech');
    it.category = cls.category;
    it.category_label = catLabel(cls.category);
    it.confidence = cls.confidence;
    it.tags = cls.tags;
    it.sensitive = cls.sensitive;
    it.source = it.source || (filtered.find(s => s.id === it._source_id)?.name) || '未知';
  }

  // 2.5. LLM 增强(默认关,需 --with-llm 且 DEEPSEEK_API_KEY)
  if (WITH_LLM && llmEnabled()) {
    info('LLM 增强模式:启用 DeepSeek V3 摘要');
    await summarizeBatch(related);
  } else if (WITH_LLM) {
    warn('--with-llm 已指定,但 DEEPSEEK_API_KEY 未配置,降级到关键词方案');
  }

  // 3. 去重(URL + title hash + content hash)
  const { unique, duplicates } = dedupe(related);
  info(`去重: ${related.length} → ${unique.length} (重复 ${duplicates.length})`);

  if (DRY_RUN) {
    info('-- DRY RUN -- 不写入文件');
    unique.slice(0, 5).forEach(it => {
      console.log(`  - [${it.date}] [${it.category}|conf=${it.confidence}] ${it.title}`);
      console.log(`    标签: ${it.tags.join(' / ')}`);
      console.log(`    URL: ${it.url}`);
      console.log('');
    });
    return;
  }

  // 4. 合并到 data.json
  const data = readDataJson();
  const added = mergeArticles(data, unique);
  writeDataJson(data);

  success('====== 抓取完成 ======', {
    total: data.news.length,
    added,
    duplicates: duplicates.length,
    sources: filtered.length
  });
}

function catLabel(cat) {
  const map = {
    policy: '政策监管', tech: '技术前沿', tool: '产品工具',
    platform: '平台动态', business: '市场商业', creation: '创作运营',
    case: '案例教程', copyright: '版权合规', overseas: '海外资讯'
  };
  return map[cat] || cat;
}

main().catch(e => {
  error('抓取主流程失败', { error: e.message, stack: e.stack });
  process.exit(1);
});
