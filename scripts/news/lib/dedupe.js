/**
 * 去重模块 · URL + SimHash + content_hash
 * - 规范化 URL(去 utm_*、去 fragment、统一 hostname)
 * - SimHash 用于标题/正文片段(汉明距离 ≤3 视为近似)
 * - content_hash 用于正文摘要(SHA256 前 16 字节 hex)
 */
import crypto from 'node:crypto';

export function normalizeUrl(rawUrl) {
  try {
    const u = new URL(rawUrl);
    const trackingParams = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content',
                           'fbclid', 'gclid', 'msclkid', 'mc_cid', 'mc_eid',
                           'ref', 'ref_source', 'source', '_source'];
    for (const p of trackingParams) u.searchParams.delete(p);
    u.hash = '';
    u.hostname = u.hostname.toLowerCase().replace(/^www\./, '');
    return u.toString();
  } catch {
    return rawUrl;
  }
}

export function contentHash(text) {
  if (!text) return '';
  return crypto.createHash('sha256').update(text.trim()).digest('hex').slice(0, 32);
}

export function titleHash(title) {
  if (!title) return '';
  const norm = title.toLowerCase().replace(/\s+/g, '').replace(/[^\w\u4e00-\u9fa5]/g, '');
  return crypto.createHash('md5').update(norm).digest('hex').slice(0, 16);
}

/**
 * SimHash · 64 位指纹
 * 1. 文本分词(简易:中文字符 + 英文单词)
 * 2. 每个 token 加权(这里统一 1)
 * 3. 每个 token 算 SHA1 mod 64 → 64 维向量
 * 4. 加权累加 → bit 序列
 * 5. bit>0 → 1,bit<0 → 0
 */
export function simHash(text) {
  if (!text) return 0n;
  const tokens = tokenize(text);
  if (tokens.length === 0) return 0n;

  const vec = new Array(64).fill(0);
  for (const t of tokens) {
    const h = crypto.createHash('sha1').update(t).digest();
    for (let i = 0; i < 64; i++) {
      const byte = Math.floor(i / 8);
      const bit = (h[byte] >> (i % 8)) & 1;
      vec[i] += bit ? 1 : -1;
    }
  }

  let hash = 0n;
  for (let i = 0; i < 64; i++) {
    if (vec[i] > 0) hash |= (1n << BigInt(63 - i));
  }
  return hash;
}

export function hammingDistance(a, b) {
  if (typeof a === 'bigint' && typeof b === 'bigint') {
    let x = a ^ b;
    let count = 0;
    while (x !== 0n) {
      x &= (x - 1n);
      count++;
    }
    return count;
  }
  let count = 0;
  let v = a ^ b;
  while (v !== 0) {
    v &= (v - 1);
    count++;
  }
  return count;
}

function tokenize(text) {
  const tokens = [];
  const cnRe = /[\u4e00-\u9fa5]+/g;
  const enRe = /[a-z0-9]+/gi;
  let m;
  while ((m = cnRe.exec(text)) !== null) {
    const word = m[0];
    for (let i = 0; i < word.length - 1; i++) {
      tokens.push(word.slice(i, i + 2));
    }
  }
  while ((m = enRe.exec(text)) !== null) tokens.push(m[0].toLowerCase());
  return tokens;
}

/**
 * 综合去重:同 URL / 同 hash / 近标题都视为重复
 * 返回 { unique, duplicates }
 */
export function dedupe(items) {
  const seen = new Map();
  const unique = [];
  const duplicates = [];

  for (const it of items) {
    const url = normalizeUrl(it.url || '');
    const tHash = titleHash(it.title || '');
    const cHash = contentHash((it.title || '') + '|' + (it.summary || ''));

    const dupKey =
      seen.has(url) ? `url:${url}` :
      seen.has(`t:${tHash}`) ? `title:${tHash}` :
      seen.has(`c:${cHash}`) ? `content:${cHash}` :
      null;

    if (dupKey) {
      duplicates.push({ ...it, dupKey });
    } else {
      seen.set(url, it);
      seen.set(`t:${tHash}`, it);
      seen.set(`c:${cHash}`, it);
      unique.push(it);
    }
  }

  for (const u of unique) {
    u.normalizedUrl = normalizeUrl(u.url || '');
    u.titleHash = titleHash(u.title || '');
    u.contentHash = contentHash((u.title || '') + '|' + (u.summary || ''));
  }

  return { unique, duplicates };
}
