/**
 * 关键词分类器 + 标签 + 置信度
 * 策略:每个分类按命中关键词加权,得分最高者胜出。
 * 置信度 = 最高分 / 总分(0-1),< 0.7 进入待审核(本地标记,不入主库)。
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const KW_FILE = path.join(__dirname, '..', 'config', 'keywords.json');

let CACHE = null;
function loadConfig() {
  if (!CACHE) CACHE = JSON.parse(fs.readFileSync(KW_FILE, 'utf-8'));
  return CACHE;
}

export function classify(text, defaultCategory = 'tech') {
  if (!text) return { category: defaultCategory, confidence: 0, tags: [], sensitive: false, score: {} };

  const cfg = loadConfig();
  const lower = text.toLowerCase();
  const score = {};

  for (const [cat, info] of Object.entries(cfg.categories)) {
    let hits = 0;
    for (const kw of info.keywords) {
      if (lower.includes(kw.toLowerCase())) hits++;
    }
    score[cat] = hits * info.weight;
  }

  const entries = Object.entries(score).sort((a, b) => b[1] - a[1]);
  const top = entries[0];
  const total = entries.reduce((s, [, v]) => s + v, 0) || 1;
  const confidence = total > 0 ? +(top[1] / total).toFixed(2) : 0;

  const tags = [];
  for (const [tag, kws] of Object.entries(cfg.tags)) {
    if (kws.some(k => lower.includes(k.toLowerCase()))) tags.push(tag);
    if (tags.length >= 5) break;
  }

  const sensitive = cfg.sensitiveKeywords.some(k => lower.includes(k.toLowerCase()));

  return {
    category: top[1] > 0 ? top[0] : defaultCategory,
    confidence,
    tags: tags.length > 0 ? tags : ['速报'],
    sensitive,
    score
  };
}

export function isRelatedToAI(text) {
  if (!text) return false;
  const lower = text.toLowerCase();
  const triggers = [
    'ai', 'aigc', '人工智能', '大模型', 'llm', 'gpt',
    '短剧', '漫剧', '微短剧',
    '文生视频', '图生视频', '视频生成',
    'sora', '可灵', '海螺', 'hailuo', 'kling', 'wan',
    'comfyui', 'midjourney', '即梦', 'flux', 'runway',
    '千川', '投流', 'roi',
    '番茄', '红果', 'reelshort',
    '广电', '网信', '管理办法', '微短剧发展管理办法'
  ];
  return triggers.some(t => lower.includes(t));
}
