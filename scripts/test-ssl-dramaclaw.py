"""测试 DramaClaw CDN 用 Python ssl 能否下载(绕开老 libcurl)"""
import ssl, urllib.request, socket, time

urls = [
    'https://nfg-web-assets.cdnfg.com/dramaclaw/guilingsi/guilingsi-ep01.mp4',
    'https://nfg-web-assets.cdnfg.com/dramaclaw/luban/luban-ep01.mp4',
    'https://github.com/agentic-commerce-lab/shopware-claude-commerce/releases/download/v0.1.0-preview/explainer.mp4',
]

for u in urls:
    print('='*60)
    print('URL:', u)
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0)'})
        t = time.time()
        resp = urllib.request.urlopen(req, timeout=10)
        print(f'HTTP {resp.status} | content-type={resp.headers.get("Content-Type")} | content-length={resp.headers.get("Content-Length")} | time={time.time()-t:.2f}s')
        # read first 256 bytes
        data = resp.read(256)
        print(f'first bytes hex: {data[:32].hex()}')
    except Exception as e:
        print(f'FAIL: {type(e).__name__}: {e}')