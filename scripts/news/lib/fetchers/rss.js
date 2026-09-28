/**
 * 通用 RSS 解析器
 * 支持 RSS 2.0 和 Atom 1.0
 * 自动提取 title / link / description / pubDate / author
 */
import { BaseFetcher } from './base.js';

const ITEM_RE_RSS = /<item\b[^>]*>([\s\S]*?)<\/item>/gi;
const ITEM_RE_ATOM = /<entry\b[^>]*>([\s\S]*?)<\/entry>/gi;

function extractBlock(block, tag) {
  const patterns = [
    new RegExp(`<${tag}[^>]*><!\\[CDATA\\[([\\s\\S]*?)\\]\\]></${tag}>`, 'i'),
    new RegExp(`<${tag}[^>]*>([\\s\\S]*?)</${tag}>`, 'i')
  ];
  for (const p of patterns) {
    const m = block.match(p);
    if (m) return m[1].trim();
  }
  return '';
}

function extractAttr(block, tag, attr) {
  const re = new RegExp(`<${tag}[^>]*\\s${attr}=["']([^"']+)["']`, 'i');
  return block.match(re)?.[1] || '';
}

export class RSSFetcher extends BaseFetcher {
  async fetch() {
    const result = await this.httpGet();
    if (!result.ok) throw new Error(result.error || 'fetch failed');

    const xml = result.data;
    const items = [];

    let matches = [...xml.matchAll(ITEM_RE_RSS)];
    let isAtom = false;
    if (matches.length === 0) {
      matches = [...xml.matchAll(ITEM_RE_ATOM)];
      isAtom = true;
    }

    for (const m of matches.slice(0, 80)) {
      const block = m[1];
      const title = this.stripCdata(extractBlock(block, 'title'));
      let url = '';
      if (isAtom) {
        const linkBlock = block.match(/<link\b([^>]*?)\/?>([\s\S]*?)<\/link>/i);
        if (linkBlock) {
          url = extractAttr(block, 'link', 'href') || linkBlock[2].trim();
        }
      } else {
        url = extractBlock(block, 'link') || extractBlock(block, 'guid');
      }
      const desc = this.stripCdata(extractBlock(block, 'description') || extractBlock(block, 'summary') || extractBlock(block, 'content'));
      const pubDate = extractBlock(block, 'pubDate') || extractBlock(block, 'published') || extractBlock(block, 'updated');
      const author = extractBlock(block, 'author') || extractBlock(block, 'dc:creator');

      if (!title || !url) continue;

      items.push({
        title,
        url,
        summary: BaseFetcher.stripHtml(desc).slice(0, 500),
        date: BaseFetcher.normalizeDate(pubDate),
        author: BaseFetcher.stripHtml(author).slice(0, 80),
        source: this.source.name,
        _raw_block_len: block.length
      });
    }

    return items;
  }

  stripCdata(text) {
    if (!text) return '';
    return text.replace(/<!\[CDATA\[([\s\S]*?)\]\]>/g, '$1');
  }

  async httpGet() {
    return await import('../http.js').then(m => m.httpGet(this.source.url, {
      timeoutMs: 15000,
      retries: 1,
      headers: { 'Accept': 'application/rss+xml, application/xml, text/xml, */*' }
    }));
  }
}
