/**
 * 微博热搜 · JSON API · 不需鉴权
 * 端点:https://weibo.com/ajax/side/hotSearch
 * 过滤:含 AI/短剧/视频/工具相关关键词的条目
 */
import { BaseFetcher } from './base.js';
import { httpGet } from '../http.js';

const RELEVANT = ['AI', '短剧', '漫剧', '视频', 'Sora', '可灵', '海螺', 'Wan',
                  'ComfyUI', 'Midjourney', '即梦', 'Flux', 'Runway', '千川',
                  '广电', '网信', '管理办法', '微短剧', '番茄', '红果', 'ReelShort'];

export class WeiboHotFetcher extends BaseFetcher {
  async fetch() {
    const r = await httpGet(this.source.url, {
      headers: {
        'Referer': 'https://weibo.com/',
        'Accept': 'application/json'
      }
    });
    if (!r.ok) throw new Error(r.error);

    const data = r.data;
    const list = data?.data?.realtime || [];
    const items = [];

    for (const item of list) {
      const word = item.word || item.note || '';
      if (!word) continue;
      const text = `${word} ${item.label_scheme || ''}`.toLowerCase();
      if (!RELEVANT.some(k => text.includes(k.toLowerCase()))) continue;

      const note = item.note || '';
      items.push({
        title: `[微博热搜] ${word}`,
        url: `https://s.weibo.com/weibo?q=${encodeURIComponent(note || word)}`,
        summary: `微博热搜词:${word}${item.label_scheme ? ' · 标签:' + item.label_scheme : ''} · 热度 ${item.num || item.raw_hot || '未知'}`,
        date: BaseFetcher.normalizeDate(new Date()),
        source: this.source.name,
        _heat: item.num
      });
    }

    return items;
  }
}
