"""列 Hugging Face veo3-video-prompts train 目录的 mp4 文件清单"""
import urllib.request, json

# HF API 列出 veo3 train 文件
api = 'https://huggingface.co/api/datasets/artificialguybr/veo3-video-prompts/tree/main/videos/veo3/train'
req = urllib.request.Request(api, headers={'User-Agent': 'Mozilla/5.0'})
try:
    data = json.loads(urllib.request.urlopen(req, timeout=15).read())
    print(f'Total files: {len(data)}')
    # 列前 25 个 + 4 个中间抽样
    sample_idx = [0, 1, 2, 3, 4, 9, 19, len(data)//4, len(data)//2, len(data)*3//4, len(data)-2, len(data)-1]
    for i, f in enumerate(data):
        if i in sample_idx or i < 5:
            sz = f.get('size', 0)
            print(f'  [{i:5d}] {f["path"].split("/")[-1]:30s} {sz:>10,d} bytes')
except Exception as e:
    print(f'FAIL: {e}')

# 列出 ZTY01/CutCraft 顶层
print('='*60)
print('ZTY01/CutCraft 顶层文件:')
api2 = 'https://huggingface.co/api/datasets/ZTY01/CutCraft/tree/main'
try:
    data = json.loads(urllib.request.urlopen(api2, timeout=15).read())
    for f in data:
        sz = f.get('size', 0)
        print(f'  {f["type"]:8s} {f["path"]:50s} {sz:>12,d} bytes')
except Exception as e:
    print(f'FAIL: {e}')