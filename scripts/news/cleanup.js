/**
 * 自动清理 · 90 天普通 + 365 天政策 + 永久保留
 *   node cleanup.js
 *   node cleanup.js --days=60       # 自定义普通保留期
 *   node cleanup.js --logs-only     # 只清理日志
 *   node cleanup.js --vacuum        # 执行后清理 SQLite/JSON 压缩(本 MVP 无 SQLite,仅打印)
 */
import { readDataJson, writeDataJson, cleanup } from './lib/storage.js';
import { getLogs, info, success } from './lib/logger.js';
import fs from 'node:fs';
import path from 'node:path';

const args = process.argv.slice(2);
const customDays = parseInt(args.find(a => a.startsWith('--days='))?.split('=')[1] || '90');
const logsOnly = args.includes('--logs-only');
const vacuum = args.includes('--vacuum');

console.log('\n========== 漫剧教程站 · 新闻清理 ==========\n');
console.log(`普通新闻保留期: ${customDays} 天`);
console.log(`政策新闻保留期: 365 天`);
console.log(`敏感新闻保留期: 60 天`);
console.log(`日志保留期: 14 天\n`);

if (!logsOnly) {
  const data = readDataJson();
  const before = data.news.length;
  const removed = cleanup(data, { defaultDays: customDays, policyDays: 365, sensitiveDays: 60 });
  writeDataJson(data);
  console.log(`📰 新闻清理: ${before} → ${data.news.length} 条(移除 ${removed} 条过期)`);
}

console.log('📋 清理过期日志:');
const logs = getLogs(14);
let logRemoved = 0;
for (const l of logs) {
  if (l.expired) {
    const full = path.join(process.cwd(), 'logs', l.file);
    if (fs.existsSync(full)) {
      fs.unlinkSync(full);
      logRemoved++;
      console.log(`  ✓ 删除 ${l.file}`);
    }
  }
}
console.log(`📋 日志清理: 移除 ${logRemoved} 个过期日志`);

if (vacuum) {
  const dataFile = path.join(process.cwd(), '..', '..', 'site', 'news', 'data.json');
  if (fs.existsSync(dataFile)) {
    const raw = fs.readFileSync(dataFile, 'utf-8');
    const minified = JSON.stringify(JSON.parse(raw));
    fs.writeFileSync(dataFile, minified, 'utf-8');
    console.log(`🗜  data.json 已压缩: ${(raw.length / 1024).toFixed(1)} KB → ${(minified.length / 1024).toFixed(1)} KB`);
  }
}

success('清理完成');
