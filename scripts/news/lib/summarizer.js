/**
 * DeepSeek V3 摘要器 · 可选增强
 *
 * 设计原则:
 * - 仅 Top 20 重点新闻走 LLM(默认按"评论数 + 7 天内"排序)
 * - 默认 DISABLED(无 API key 时自动跳过,降级到关键词方案)
 * - 失败重试 2 次,仍失败则标记 status=pending_review
 * - Token 计数 + 调用日志,避免超额
 *
 * 配置(从 .env 读):
 *   DEEPSEEK_API_KEY=sk-xxx
 *   DEEPSEEK_BASE_URL=https://api.deepseek.com
 *   DEEPSEEK_MODEL=deepseek-chat
 *   DAILY_LLM_LIMIT=200
 *
 * 启用方式:
 *   export DEEPSEEK_API_KEY=sk-xxx
 *   node fetch.js --with-llm
 *
 * 输出 JSON 格式:
 * {
 *   "is_related": true,
 *   "title_zh": "中文标题",
 *   "category": "tech",
 *   "tags": ["AI短剧", "文生视频"],
 *   "summary": "100-200字中文摘要",
 *   "key_points": ["要点1", "要点2"],
 *   "impact": "对行业的影响",
 *   "audience": ["短剧创作者"],
 *   "confidence": 0.92,
 *   "sensitive": false,
 *   "reason": "分类理由"
 * }
 */
import fs from 'node:fs';
import path from 'node:path';
import { info, warn, error, success } from './logger.js';

const LOG_FILE = path.join(process.cwd(), 'logs', 'ai-process.log');
const COST_FILE = path.join(process.cwd(), 'logs', 'ai-cost.json');

const SYSTEM_PROMPT = `你是 AI/AIGC 内容创作行业新闻分析助手。给定一条新闻的标题和摘要,生成严格 JSON 输出。
你的服务对象是 AI 漫剧/短剧创作者,所以关注面应该包括:
- AI 视频 / AIGC 内容创作(短剧、漫剧、广告、电影)
- AI 模型/工具(文生视频、图生视频、角色一致性、口型同步、配音、剪辑)
- 短剧/漫剧/微短剧平台动态(抖音、快手、红果、番茄、B站、小红书、TikTok、ReelShort 等)
- 政策监管(广电总局、网信办、微短剧发展管理办法、AI 标识、内容合规)
- 市场商业(投流/千川/ROI/分账/出海/变现)
- 创作运营(剧本/分镜/提示词/账号运营/爆款拆解)
- AI 行业大事件(OpenAI/Google/DeepSeek/字节/阿里/腾讯/快手/百度 等重要发布)
- Agent/Workflow 等能影响创作流程的技术
- 仅当新闻完全无关(如纯娱乐八卦、社会新闻、不涉及任何 AI/AIGC/视频/数字人/创作工具)时才标记 is_related=false

输出要求(严格 JSON):
1. is_related: bool(true 表示与上述 AI/AIGC 创作行业相关)
2. title_zh: 翻译为更地道的中文标题(若原文已是中文可润色)
3. category: 一级分类(政策监管/技术前沿/产品工具/平台动态/市场商业/创作运营/案例教程/版权合规/海外资讯)
4. tags: 3-5 个关键词标签
5. summary: 100-200 字中文摘要,客观事实
6. key_points: 3-5 个关键要点
7. impact: 对短剧创作者/漫剧团队/AI 工具方/投资人/平台的影响(2-3 句话)
8. audience: 适合人群(短剧创作者/漫剧团队/AI 工具开发者/运营/投资人 等)
9. confidence: 0-1 的置信度
10. sensitive: 是否涉及违规/政策/版权敏感
11. reason: 一句话分类理由

不相关时只输出 {is_related: false, reason: "..."}。
不要捏造新闻事实,只总结给定文本。`;

/**
 * 从 .env 加载(简单解析)
 */
export function loadEnv() {
  const envPath = path.join(process.cwd(), '.env');
  if (!fs.existsSync(envPath)) return {};
  const env = {};
  for (const line of fs.readFileSync(envPath, 'utf-8').split('\n')) {
    const m = line.match(/^\s*([A-Z_][A-Z0-9_]*)\s*=\s*(.*?)\s*$/);
    if (m && !line.startsWith('#')) env[m[1]] = m[2];
  }
  return env;
}

export function isEnabled() {
  const env = loadEnv();
  return !!(env.DEEPSEEK_API_KEY && env.DEEPSEEK_API_KEY.length > 10);
}

export function loadCost() {
  if (!fs.existsSync(COST_FILE)) return { date: today(), calls: 0, tokens: 0 };
  try {
    const c = JSON.parse(fs.readFileSync(COST_FILE, 'utf-8'));
    if (c.date !== today()) return { date: today(), calls: 0, tokens: 0 };
    return c;
  } catch {
    return { date: today(), calls: 0, tokens: 0 };
  }
}

function saveCost(c) {
  fs.writeFileSync(COST_FILE, JSON.stringify(c, null, 2), 'utf-8');
}

function today() {
  return new Date().toISOString().split('T')[0];
}

function logLine(msg) {
  fs.appendFileSync(LOG_FILE, `[${new Date().toISOString()}] ${msg}\n`, 'utf-8');
}

/**
 * 单条新闻摘要(失败抛错,自动重试 2 次)
 */
export async function summarize(title, content, env = loadEnv()) {
  if (!env.DEEPSEEK_API_KEY) throw new Error('DEEPSEEK_API_KEY 未配置');

  const url = `${env.DEEPSEEK_BASE_URL || 'https://api.deepseek.com'}/chat/completions`;
  const body = {
    model: env.DEEPSEEK_MODEL || 'deepseek-chat',
    messages: [
      { role: 'system', content: SYSTEM_PROMPT },
      { role: 'user', content: `标题:${title}\n摘要:${(content || '').slice(0, 800)}\n请输出严格 JSON。` }
    ],
    temperature: 0.3,
    max_tokens: 800,
    response_format: { type: 'json_object' }
  };

  let lastErr;
  for (let attempt = 1; attempt <= 2; attempt++) {
    try {
      const ctrl = new AbortController();
      const timer = setTimeout(() => ctrl.abort(), 25000);
      const res = await fetch(url, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${env.DEEPSEEK_API_KEY}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(body),
        signal: ctrl.signal
      });
      clearTimeout(timer);

      if (!res.ok) {
        const errText = await res.text();
        throw new Error(`HTTP ${res.status}: ${errText.slice(0, 200)}`);
      }

      const data = await res.json();
      const choice = data.choices?.[0];
      if (!choice) throw new Error('无 choices 返回');

      const tokens = data.usage?.total_tokens || 0;
      const cost = loadCost();
      cost.calls += 1;
      cost.tokens += tokens;
      saveCost(cost);
      logLine(`OK calls=${cost.calls} tokens=${tokens} title="${title.slice(0, 30)}..."`);

      let parsed;
      try {
        parsed = JSON.parse(choice.message.content);
      } catch (e) {
        const cleaned = choice.message.content.replace(/^```json\n?/i, '').replace(/\n?```$/, '').trim();
        parsed = JSON.parse(cleaned);
      }
      return parsed;
    } catch (e) {
      lastErr = e;
      logLine(`FAIL attempt=${attempt} error="${e.message}"`);
      if (attempt < 2) await new Promise(r => setTimeout(r, 1500));
    }
  }
  throw lastErr;
}

/**
 * 批量摘要 · 仅 Top N + 每日限额
 */
export async function summarizeBatch(items, opts = {}) {
  if (!isEnabled()) {
    warn('LLM 未启用(缺少 DEEPSEEK_API_KEY),跳过批量摘要');
    return items;
  }

  const env = loadEnv();
  const dailyLimit = parseInt(env.DAILY_LLM_LIMIT || '200');
  const cost = loadCost();
  const remaining = Math.max(0, dailyLimit - cost.calls);

  if (remaining === 0) {
    warn(`LLM 每日限额已用完 (${cost.calls}/${dailyLimit}),跳过`);
    return items;
  }

  // 按"权重"排序:7 天内 + 命中关键词多
  const ranked = items
    .map((it, idx) => ({ idx, it, score: scoreForLLM(it) }))
    .sort((a, b) => b.score - a.score)
    .slice(0, Math.min(remaining, opts.maxItems || 20));

  info(`LLM 摘要: ${ranked.length}/${items.length} 条(剩余 ${remaining}/${dailyLimit})`);

  let ok = 0, fail = 0;
  for (const { idx, it } of ranked) {
    try {
      const result = await summarize(it.title, it.summary || it.content || '', env);
      if (!result.is_related) {
        items[idx].llm_skipped = true;
        items[idx].llm_reason = result.reason;
        continue;
      }
      items[idx].title_zh = result.title_zh || it.title;
      items[idx].llm_summary = result.summary;
      items[idx].llm_key_points = result.key_points || [];
      items[idx].llm_impact = result.impact;
      items[idx].llm_audience = result.audience || [];
      items[idx].confidence = result.confidence;
      items[idx].tags = result.tags || items[idx].tags;
      items[idx].category = mapCategory(result.category) || items[idx].category;
      items[idx].sensitive = result.sensitive || items[idx].sensitive;
      items[idx].llm_processed_at = new Date().toISOString();
      ok++;
    } catch (e) {
      fail++;
      items[idx].llm_error = e.message.slice(0, 100);
      warn(`LLM 摘要失败: ${it.title?.slice(0, 30)}... ${e.message}`);
    }
    await new Promise(r => setTimeout(r, 500));
  }
  success(`LLM 摘要完成: OK=${ok} FAIL=${fail}`);
  return items;
}

function scoreForLLM(it) {
  let s = 0;
  const ts = new Date(it.date || 0).getTime();
  const ageDays = (Date.now() - ts) / 86400000;
  if (ageDays <= 1) s += 10;
  else if (ageDays <= 3) s += 5;
  else if (ageDays <= 7) s += 2;

  const text = `${it.title || ''} ${it.summary || ''}`.toLowerCase();
  const high = ['sora', '可灵', '海螺', 'wan', 'comfyui', '千川', '管理办法'];
  high.forEach(k => { if (text.includes(k)) s += 3; });
  return s;
}

function mapCategory(llmCat) {
  const map = {
    '政策监管': 'policy',
    '技术前沿': 'tech',
    '产品工具': 'tool',
    '平台动态': 'platform',
    '市场商业': 'business',
    '创作运营': 'creation',
    '案例教程': 'case',
    '版权合规': 'copyright',
    '海外资讯': 'overseas'
  };
  return map[llmCat];
}
