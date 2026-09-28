/**
 * GitHub Trending · HTML 抓取 + 关键词过滤
 * 端点:https://github.com/trending?since=daily
 * 只收录与 AI / 视频生成 / 短剧相关的仓库
 */
import { BaseFetcher } from './base.js';
import { httpGet } from '../http.js';

const RELEVANT = [
  'ai', 'video', 'comfyui', 'stable-diffusion', 'sora', 'kling',
  'hailuo', 'wan', 'pika', 'luma', 'runway', 'midjourney', 'flux',
  'short', 'drama', 'anime', 'cartoon', 'manga', 'webtoon',
  'tts', 'lip-sync', 'talking', 'agent', 'llm', 'lora',
  'animate', 'diffusion', 'transformer', 'multimodal'
];

export class GitHubTrendingFetcher extends BaseFetcher {
  async fetch() {
    const r = await httpGet(this.source.url, {
      headers: {
        'Accept': 'text/html'
      }
    });
    if (!r.ok) throw new Error(r.error);

    const html = r.data;
    const items = [];
    const articleRe = /<article[^>]*class="[^"]*Box-row[^"]*"[^>]*>([\s\S]*?)<\/article>/g;

    let m;
    while ((m = articleRe.exec(html)) !== null) {
      const block = m[1];

      const repoMatch = block.match(/<h2[^>]*>\s*<a[^>]*href="(\/[^"]+)"[^>]*>([\s\S]*?)<\/a>/);
      if (!repoMatch) continue;
      const repoPath = repoMatch[1].trim();
      const titleHtml = repoMatch[2].replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim();
      const fullTitle = titleHtml || repoPath.replace(/^\//, '');

      const lower = fullTitle.toLowerCase();
      if (!RELEVANT.some(k => lower.includes(k))) continue;

      const descMatch = block.match(/<p class="col-9[^"]*">([\s\S]*?)<\/p>/);
      const desc = descMatch ? BaseFetcher.stripHtml(descMatch[1]) : '';

      const langMatch = block.match(/<span itemprop="programmingLanguage">([^<]+)<\/span>/);
      const lang = langMatch?.[1] || '';

      const starsMatch = block.match(/<a[^>]*href="\/[^"]+\/stargazers"[^>]*>[\s\S]*?<span[^>]*>([\s\S]*?)<\/span>/);
      const stars = BaseFetcher.stripHtml(starsMatch?.[1] || '');

      items.push({
        title: `[GitHub Trending] ${fullTitle}${lang ? ' (' + lang + ')' : ''}`,
        url: `https://github.com${repoPath}`,
        summary: `${desc || 'AI/视频相关热门仓库'}${stars ? ' · ⭐ ' + stars : ''}`,
        date: BaseFetcher.normalizeDate(new Date()),
        source: this.source.name,
        _stars: stars,
        _lang: lang
      });
    }

    return items;
  }
}
