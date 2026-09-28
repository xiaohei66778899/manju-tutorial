"""获取 veo3 视频的真实 prompt 内容(查 metadata)"""
import urllib.request, json

# 列出 veo3-video-prompts 数据集顶层
print('=== Top-level files ===')
api = 'https://huggingface.co/api/datasets/artificialguybr/veo3-video-prompts/tree/main'
data = json.loads(urllib.request.urlopen(api, timeout=15).read())
for f in data[:30]:
    sz = f.get('size', 0)
    print(f'  {f["type"]:8s} {f["path"]:60s} {sz:>12,d}')

# 试 metadata 真实路径
print('\n=== Metadata API ===')
candidates = [
    'https://huggingface.co/datasets/artificialguybr/veo3-video-prompts/resolve/main/README.md',
    'https://huggingface.co/datasets/artificialguybr/veo3-video-prompts/resolve/main/dataset_infos.json',
    'https://huggingface.co/datasets/artificialguybr/veo3-video-prompts/resolve/main/prompts.csv',
    'https://huggingface.co/datasets/artificialguybr/veo3-video-prompts/resolve/main/videos/veo3/train.parquet',
]
for u in candidates:
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
        resp = urllib.request.urlopen(req, timeout=10)
        sz = resp.headers.get('Content-Length', '?')
        print(f'  OK {sz:>10s} {u}')
    except Exception as e:
        print(f'  FAIL {u}: {type(e).__name__}')