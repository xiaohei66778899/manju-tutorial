/**
 * 持久化层 · 单一职责
 * - 读/写 site/news/data.json(向后兼容 v1.0 schema)
 * - 保留旧字段(id/title/category/tag/summary/source/url/date)
 * - 新增可选字段(置信度、标签数组、AI 摘要、原文链接、规范化 URL)
 * - 保留 90 天,重要新闻可永久标记
 */
import fs from 'node:fs';
import path from 'node:path';

const SITE_ROOT = path.join(process.cwd(), '..', '..', 'site');
const DATA_FILE = path.join(SITE_ROOT, 'news', 'data.json');

export function readDataJson() {
  if (!fs.existsSync(DATA_FILE)) {
    return {
      version: '2.0',
      lastUpdated: new Date().toISOString(),
      total: 0,
      sources: [],
      categories: {
        policy: '政策监管',
        tech: '技术前沿',
        tool: '产品工具',
        platform: '平台动态',
        business: '市场商业',
        creation: '创作运营',
        case: '案例教程',
        copyright: '版权合规',
        overseas: '海外资讯',
        data: '行业数据',
        course: '教程动态',
        open_source: '开源项目',
        model: 'AI 模型'
      },
      news: []
    };
  }
  return JSON.parse(fs.readFileSync(DATA_FILE, 'utf-8'));
}

export function writeDataJson(data) {
  if (!fs.existsSync(path.dirname(DATA_FILE))) {
    fs.mkdirSync(path.dirname(DATA_FILE), { recursive: true });
  }
  data.lastUpdated = new Date().toISOString();
  data.total = data.news.length;
  data.sources = [...new Set(data.news.map(n => n.source).filter(Boolean))];
  fs.writeFileSync(DATA_FILE, JSON.stringify(data, null, 2), 'utf-8');
}

/**
 * 合并新条目到现有数据
 * - 按 canonical URL 去重
 * - 保留现有 id 序列
 * - 重要新闻不参与清理(permanent = true)
 */
export function mergeArticles(existingData, newItems) {
  const seen = new Set(existingData.news.map(n => n.url || n.normalizedUrl));
  const maxId = existingData.news.reduce((m, n) => Math.max(m, n.id || 0), 0);
  let nextId = maxId + 1;

  let added = 0;
  for (const it of newItems) {
    const url = it.normalizedUrl || it.url;
    if (!url || seen.has(url)) continue;
    if (!it.title || !it.date) continue;
    seen.add(url);
    existingData.news.push({
      id: nextId++,
      title: it.title,
      title_zh: it.title_zh || it.title,
      category: it.category || 'tech',
      category_label: it.category_label,
      tag: (Array.isArray(it.tags) ? it.tags : [it.tag || '速报']).slice(0, 5).join(' / '),
      tags: Array.isArray(it.tags) ? it.tags : [it.tag || '速报'],
      summary: (it.summary || '').slice(0, 500),
      llm_summary: it.llm_summary,
      llm_key_points: it.llm_key_points,
      llm_impact: it.llm_impact,
      llm_audience: it.llm_audience,
      llm_processed_at: it.llm_processed_at,
      source: it.source || '',
      url: it.url || '',
      canonical_url: it.normalizedUrl || it.url,
      date: it.date,
      fetched_at: new Date().toISOString(),
      confidence: it.confidence,
      sensitive: it.sensitive || false,
      permanent: it.permanent || false,
      status: it.confidence !== undefined && it.confidence < 0.7 ? 'pending_review' : 'published'
    });
    added++;
  }

  existingData.news.sort((a, b) => (b.date || '').localeCompare(a.date || ''));
  return added;
}

/**
 * 清理过期新闻
 * - 默认保留 90 天
 * - permanent = true 永久保留
 * - 政策类(policy)默认 365 天
 */
export function cleanup(data, opts = {}) {
  const { defaultDays = 90, policyDays = 365, sensitiveDays = 60 } = opts;
  const cutoff = Date.now() - defaultDays * 86400000;
  const policyCutoff = Date.now() - policyDays * 86400000;
  const sensitiveCutoff = Date.now() - sensitiveDays * 86400000;

  const before = data.news.length;
  data.news = data.news.filter(n => {
    if (n.permanent) return true;
    const ts = new Date(n.date || n.fetched_at || 0).getTime();
    if (n.category === 'policy') return ts >= policyCutoff;
    if (n.sensitive) return ts >= sensitiveCutoff;
    return ts >= cutoff;
  });
  return before - data.news.length;
}
