/**
 * 统计面板 · 展示 data.json 当前状态
 *   node stats.js
 */
import { readDataJson } from './lib/storage.js';
import { getLogs } from './lib/logger.js';

const data = readDataJson();
const news = data.news || [];

console.log('\n========== 漫剧教程站 · 新闻统计 ==========\n');
console.log(`📅 最后更新: ${data.lastUpdated}`);
console.log(`📰 总条数: ${news.length}`);
console.log(`📡 来源数: ${data.sources?.length || 0}`);

const byCat = {};
const byTag = {};
const bySource = {};
for (const n of news) {
  byCat[n.category] = (byCat[n.category] || 0) + 1;
  if (Array.isArray(n.tags)) for (const t of n.tags) byTag[t] = (byTag[t] || 0) + 1;
  if (n.source) bySource[n.source] = (bySource[n.source] || 0) + 1;
}

console.log('\n📊 分类分布:');
Object.entries(byCat).sort((a, b) => b[1] - a[1]).forEach(([k, v]) => {
  console.log(`  ${k.padEnd(12)} ${String(v).padStart(4)} 条`);
});

console.log('\n🏷  Top 10 标签:');
Object.entries(byTag).sort((a, b) => b[1] - a[1]).slice(0, 10).forEach(([k, v]) => {
  console.log(`  ${k.padEnd(14)} ${String(v).padStart(4)} 次`);
});

console.log('\n📡 来源分布:');
Object.entries(bySource).sort((a, b) => b[1] - a[1]).forEach(([k, v]) => {
  console.log(`  ${k.padEnd(16)} ${String(v).padStart(4)} 条`);
});

const now = Date.now();
const last7d = news.filter(n => {
  const t = new Date(n.date || 0).getTime();
  return now - t < 7 * 86400000;
}).length;
const last30d = news.filter(n => {
  const t = new Date(n.date || 0).getTime();
  return now - t < 30 * 86400000;
}).length;
console.log(`\n⏰ 7 天内: ${last7d} 条 | 30 天内: ${last30d} 条`);

console.log('\n📋 日志文件:');
const logs = getLogs(14);
logs.slice(-5).forEach(l => {
  console.log(`  ${l.file} (${(l.size / 1024).toFixed(1)} KB, ${l.expired ? '⚠️ 过期' : '✓'})`);
});

const pendingReview = news.filter(n => n.status === 'pending_review').length;
console.log(`\n🔍 待审核: ${pendingReview} 条(置信度 < 0.7)`);
const permanent = news.filter(n => n.permanent).length;
console.log(`📌 永久保留: ${permanent} 条`);

console.log('\n========== 结束 ==========\n');
