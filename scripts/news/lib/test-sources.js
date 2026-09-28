/**
 * 测试所有源连通性 + 抓取条数
 *   node lib/test-sources.js
 *   node lib/test-sources.js --source=xxx
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { RSSFetcher } from './fetchers/rss.js';
import { WeiboHotFetcher } from './fetchers/weibo.js';
import { GitHubTrendingFetcher } from './fetchers/github-trending.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const SOURCES_FILE = path.join(__dirname, '..', 'config', 'sources.json');
const ONLY = process.argv.find(a => a.startsWith('--source='))?.split('=')[1];

const FETCHER_MAP = {
  'weibo-hot': WeiboHotFetcher,
  'github-trending': GitHubTrendingFetcher
};

const cfg = JSON.parse(fs.readFileSync(SOURCES_FILE, 'utf-8'));
const sources = cfg.sources.filter(s => s.enabled !== false);
const filtered = ONLY ? sources.filter(s => s.id === ONLY) : sources;

console.log('\n========== 新闻源连通性测试 ==========\n');

for (const src of filtered) {
  const FetcherClass = FETCHER_MAP[src.id] || RSSFetcher;
  const fetcher = new FetcherClass(src);
  const start = Date.now();
  try {
    const result = await fetcher.safeFetch();
    const ms = Date.now() - start;
    if (result.ok) {
      const marker = result.items.length > 0 ? '✅' : '⚠️';
      console.log(`  ${marker} ${src.id.padEnd(20)} ${src.name.padEnd(20)} ${result.items.length.toString().padStart(4)} 条 (${ms}ms)`);
    } else {
      console.log(`  ❌ ${src.id.padEnd(20)} ${src.name.padEnd(20)} 失败: ${result.error} (${ms}ms)`);
    }
  } catch (e) {
    console.log(`  💥 ${src.id.padEnd(20)} ${src.name.padEnd(20)} 异常: ${e.message}`);
  }
}

console.log('\n========== 结束 ==========\n');
