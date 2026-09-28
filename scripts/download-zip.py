"""下载 veo3.1.zip + seedance2.5.zip(后台)"""
import urllib.request, os, time

DST = r'E:\AIGC\课件\12小说\_downloads'
os.makedirs(DST, exist_ok=True)

# 两个 zip 包
zips = [
    ('veo3.1.zip', 'https://huggingface.co/datasets/ZTY01/CutCraft/resolve/main/veo3.1.zip', 1334683418),
    ('seedance2.5.zip', 'https://huggingface.co/datasets/ZTY01/CutCraft/resolve/main/seedance2.5.zip', 1493532993),
]

for fname, url, expected_size in zips:
    out = os.path.join(DST, fname)
    if os.path.exists(out) and os.path.getsize(out) == expected_size:
        print(f'[SKIP] {fname} already downloaded ({expected_size:,} bytes)')
        continue

    print(f'[START] {fname} ({expected_size:,} bytes)')
    t = time.time()
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=300) as resp:
            downloaded = 0
            chunk_size = 8 * 1024 * 1024  # 8 MB chunks
            with open(out, 'wb') as f:
                last_log = time.time()
                while True:
                    chunk = resp.read(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)
                    # 每 30s 输出进度
                    if time.time() - last_log >= 30:
                        pct = 100 * downloaded / expected_size
                        speed = downloaded / (time.time() - t) / 1024 / 1024
                        print(f'  [{pct:.1f}%] {downloaded:,}/{expected_size:,} bytes ({speed:.1f} MB/s)', flush=True)
                        last_log = time.time()
        print(f'[DONE] {fname} {downloaded:,} bytes in {time.time()-t:.1f}s')
    except Exception as e:
        print(f'[FAIL] {fname}: {type(e).__name__}: {e}')
        # 删除部分下载
        if os.path.exists(out):
            os.remove(out)

print('='*60)
print('Final state:')
for fname, _, _ in zips:
    p = os.path.join(DST, fname)
    if os.path.exists(p):
        print(f'  {fname}: {os.path.getsize(p):,} bytes')
    else:
        print(f'  {fname}: NOT DOWNLOADED')