/**
 * 统一 HTTP 客户端 · Node 内置 fetch
 * - 超时控制
 * - 重试机制(默认 1 次)
 * - 错误归类(超时/网络/HTTP 状态)
 */
import { warn } from './logger.js';

const DEFAULT_TIMEOUT_MS = 15000;

export async function httpGet(url, options = {}) {
  const {
    timeoutMs = DEFAULT_TIMEOUT_MS,
    retries = 1,
    retryDelayMs = 2000,
    headers = {}
  } = options;

  const ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36';

  let lastError = null;
  for (let attempt = 0; attempt <= retries; attempt++) {
    const ctrl = new AbortController();
    const timer = setTimeout(() => ctrl.abort(), timeoutMs);

    try {
      const res = await fetch(url, {
        headers: {
          'User-Agent': ua,
          'Accept': 'application/json, text/xml, application/xml, text/html, */*',
          'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
          ...headers
        },
        signal: ctrl.signal,
        redirect: 'follow'
      });

      clearTimeout(timer);

      if (!res.ok) {
        throw new Error(`HTTP ${res.status} ${res.statusText}`);
      }

      const contentType = res.headers.get('content-type') || '';
      if (contentType.includes('json')) {
        return { ok: true, data: await res.json(), contentType };
      }
      return { ok: true, data: await res.text(), contentType };
    } catch (e) {
      clearTimeout(timer);
      lastError = e;
      const isTimeout = e.name === 'AbortError';
      const errType = isTimeout ? 'timeout' : (e.message.includes('HTTP') ? 'http' : 'network');
      warn(`HTTP 请求失败 [${errType}] attempt=${attempt + 1}/${retries + 1}`, {
        url: url.slice(0, 80),
        error: e.message
      });
      if (attempt < retries) {
        await new Promise(r => setTimeout(r, retryDelayMs));
      }
    }
  }
  return { ok: false, error: lastError?.message || 'unknown error' };
}
