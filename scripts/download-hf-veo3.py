"""下载 Hugging Face veo3 视频样例(分散挑 15 个不同 index)"""
import urllib.request, os, time, json

DST = r'E:\AIGC\课件\12小说\site\works\videos\external'
os.makedirs(DST, exist_ok=True)

# 分散挑 15 个不同 index(0 - 999,分散多样性)
PICK = [0, 1, 2, 3, 4, 9, 19, 49, 99, 199, 299, 399, 499, 599, 799, 899, 999]

# 先获取 prompt 列表以挑选有意义的
print('Loading prompts...')
api = 'https://huggingface.co/api/datasets/artificialguybr/veo3-video-prompts/tree/main/videos/veo3/train'
data = json.loads(urllib.request.urlopen(api, timeout=15).read())

# 也拉 metadata 看 prompt 内容
md_api = 'https://huggingface.co/datasets/artificialguybr/veo3-video-prompts/resolve/main/metadata.csv'
try:
    md_data = urllib.request.urlopen(md_api, timeout=15).read().decode('utf-8', errors='ignore')
    # 简单解析 csv
    lines = md_data.split('\n')
    print(f'metadata lines: {len(lines)}')
except Exception as e:
    print(f'metadata fail: {e}')

# 下载 15 个分散 index
base = 'https://huggingface.co/datasets/artificialguybr/veo3-video-prompts/resolve/main/videos/veo3/train/'
results = []
for idx in PICK:
    fname = f'{idx:08d}.mp4'
    url = base + fname
    out = os.path.join(DST, f'hf-veo3-{fname}')
    if os.path.exists(out) and os.path.getsize(out) > 1000:
        print(f'  [skip] {fname} already exists')
        results.append((idx, out, os.path.getsize(out)))
        continue
    t = time.time()
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=30) as resp, open(out, 'wb') as f:
            data = resp.read()
            f.write(data)
        sz = len(data)
        print(f'  [OK] {fname} {sz:>10,d}B in {time.time()-t:.1f}s')
        results.append((idx, out, sz))
    except Exception as e:
        print(f'  [FAIL] {fname}: {type(e).__name__}: {str(e)[:80]}')

print('='*60)
print(f'Downloaded: {len(results)} / {len(PICK)}')
total = sum(sz for _, _, sz in results)
print(f'Total size: {total:,d} bytes = {total/1024/1024:.1f} MB')