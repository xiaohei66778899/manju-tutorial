"""测试 Hugging Face 数据集 / YouTube CDN / GitHub Releases 直链下载"""
import ssl, urllib.request, time

urls = [
    # Hugging Face 标准 SSL(已成功过 GitHub Releases,HF 类似)
    ('Hugging Face ZTY01/CutCraft veo3.1', 'https://huggingface.co/datasets/ZTY01/CutCraft/resolve/main/veo3.1.zip'),
    ('Hugging Face ZTY01/CutCraft seedance2.5', 'https://huggingface.co/datasets/ZTY01/CutCraft/resolve/main/seedance2.5.zip'),
    ('Hugging Face 单个 mp4 veo3', 'https://huggingface.co/datasets/artificialguybr/veo3-video-prompts/resolve/main/videos/veo3/train/00000001.mp4'),
    # YouTube CDN(预期 TLS 1.3,会失败)
    ('YouTube CDN googlevideo', 'https://rr2---sn-25ge7ns7.googlevideo.com/videoplayback?expire=9999999999'),
    ('YouTube CDN generic', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'),
    # Facebook 视频(预期失败)
    ('Facebook video CDN', 'https://video.fpat1-1.fna.fbcdn.net/'),
    # GitHub raw 标准 SSL
    ('GitHub raw seedance client README', 'https://raw.githubusercontent.com/letorig/video-generator-client/main/README.md'),
]

for name, u in urls:
    print('='*70)
    print(f'[{name}]')
    print(f'URL: {u[:90]}...' if len(u) > 90 else f'URL: {u}')
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0)'})
        t = time.time()
        resp = urllib.request.urlopen(req, timeout=15)
        cl = resp.headers.get('Content-Length')
        ct = resp.headers.get('Content-Type')
        print(f'HTTP {resp.status} | type={ct} | length={cl} | time={time.time()-t:.2f}s')
    except Exception as e:
        print(f'FAIL: {type(e).__name__}: {str(e)[:120]}')