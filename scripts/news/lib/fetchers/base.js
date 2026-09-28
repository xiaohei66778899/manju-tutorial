/**
 * Fetcher 基类 · 所有抓取器继承这个
 * - 必须实现 async fetch() 返回标准化条目数组
 * - 标准条目:{ title, url, summary, source, date, ...extras }
 * - 错误处理 + 重试由基类统一
 */
import { httpGet } from '../http.js';
import { warn } from '../logger.js';

export class BaseFetcher {
  constructor(source) {
    this.source = source;
  }

  get id() { return this.source.id; }
  get name() { return this.source.name; }

  async fetch() {
    throw new Error(`${this.constructor.name}.fetch() not implemented`);
  }

  async safeFetch() {
    const start = Date.now();
    try {
      const items = await this.fetch();
      return {
        ok: true,
        items,
        duration: Date.now() - start
      };
    } catch (e) {
      warn(`Fetcher [${this.name}] 失败`, { error: e.message });
      return { ok: false, items: [], error: e.message, duration: Date.now() - start };
    }
  }

  static normalizeDate(input) {
    if (!input) return new Date().toISOString().split('T')[0];
    if (input instanceof Date) return input.toISOString().split('T')[0];
    const ts = Date.parse(input);
    if (isNaN(ts)) return new Date().toISOString().split('T')[0];
    return new Date(ts).toISOString().split('T')[0];
  }

  static stripHtml(html) {
    if (!html) return '';
    return html
      .replace(/<script[\s\S]*?<\/script>/gi, '')
      .replace(/<style[\s\S]*?<\/style>/gi, '')
      .replace(/<[^>]+>/g, ' ')
      .replace(/&nbsp;/g, ' ')
      .replace(/&amp;/g, '&')
      .replace(/&lt;/g, '<')
      .replace(/&gt;/g, '>')
      .replace(/&quot;/g, '"')
      .replace(/&#39;/g, "'")
      .replace(/\s+/g, ' ')
      .trim();
  }
}

export { httpGet };
