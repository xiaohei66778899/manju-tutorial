/**
 * 回填脚本 · 给旧条目补 LLM 摘要
 *
 * 用途:玉哥手写的 30 条原数据没有 LLM 字段,跑一次这个脚本批量补上
 *
 * 用法:
 *   node reprocess.js              # 默认处理所有缺 llm_summary 的条目
 *   node reprocess.js --max=50     # 限制本次最多处理 50 条
 *   node reprocess.js --id=5,10,15 # 指定 ID 列表
 *
 * 配额控制:每日 DAILY_LLM_LIMIT 默认 200,够补 ~150 条
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { readDataJson, writeDataJson } from './lib/storage.js';
import { isEnabled, summarizeBatch, loadCost } from './lib/summarizer.js';
import { info, success, warn } from './lib/logger.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
const maxArg = parseInt(args.find(a => a.startsWith('--max='))?.split('=')[1] || '200');
const idArg = args.find(a => a.startsWith('--id='))?.split('=')[1];

if (!isEnabled()) {
  warn('LLM 未启用(缺少 DEEPSEEK_API_KEY),无法回填');
  process.exit(1);
}

const data = readDataJson();
const targets = idArg
  ? data.news.filter(n => idArg.split(',').map(Number).includes(n.id))
  : data.news.filter(n => !n.llm_summary);

const limited = targets.slice(0, maxArg);
info(`待回填: ${targets.length} 条,本次处理: ${limited.length} 条`);

const cost = loadCost();
const remaining = Math.max(0, 200 - cost.calls);
if (remaining < limited.length) {
  warn(`⚠️ 今日 LLM 配额仅剩 ${remaining} 次,本次只能跑 ${Math.min(remaining, limited.length)} 条`);
}
const final = limited.slice(0, remaining);

if (final.length === 0) {
  warn('无可处理条目,退出');
  process.exit(0);
}

// 构造 items 数组(用 summarizeBatch)
const items = final.map(n => ({
  title: n.title,
  summary: n.summary,
  date: n.date,
  tags: n.tags || [n.tag || '速报'],
  category: n.category,
  source: n.source,
  url: n.url,
  confidence: n.confidence,
  sensitive: n.sensitive
}));

info('开始批量回填 LLM...');
await summarizeBatch(items, { maxItems: final.length });

// 把结果写回 data.json
let ok = 0;
for (let i = 0; i < final.length; i++) {
  const orig = data.news.find(n => n.id === final[i].id);
  const updated = items[i];
  if (updated.title_zh || updated.llm_summary) {
    if (updated.title_zh) orig.title_zh = updated.title_zh;
    if (updated.llm_summary) orig.llm_summary = updated.llm_summary;
    if (updated.llm_key_points) orig.llm_key_points = updated.llm_key_points;
    if (updated.llm_impact) orig.llm_impact = updated.llm_impact;
    if (updated.llm_audience) orig.llm_audience = updated.llm_audience;
    if (updated.tags && Array.isArray(updated.tags)) orig.tags = updated.tags;
    if (updated.confidence) orig.confidence = updated.confidence;
    if (updated.llm_processed_at) orig.llm_processed_at = updated.llm_processed_at;
    ok++;
  } else if (updated.llm_skipped) {
    orig.llm_skipped = true;
    orig.llm_reason = updated.llm_reason;
  } else if (updated.llm_error) {
    orig.llm_error = updated.llm_error;
  }
}

writeDataJson(data);
success(`回填完成: 处理 ${final.length} 条,成功 ${ok} 条`);
