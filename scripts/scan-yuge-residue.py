# -*- coding: utf-8 -*-
"""全站扫描 '玉哥' 残留位置,分类保留/清理"""
import os, sys, re
sys.stdout.reconfigure(encoding='utf-8')

ROOT = r'E:\AIGC\课件\12小说'

# 扫描所有 HTML
results = []
for root, dirs, files in os.walk(ROOT):
    if any(seg in root for seg in ['node_modules', '.git', 'backup', '_brainmap', '_debug-archives', '_trash-removed']):
        continue
    for f in files:
        if not f.endswith('.html'):
            continue
        fp = os.path.join(root, f)
        try:
            with open(fp, 'rb') as fh:
                text = fh.read().decode('utf-8-sig' if fh.read(3) == b'\xef\xbb\xbf' else 'utf-8', errors='ignore')
        except:
            continue
        # 找玉哥出现位置(精确)
        count = text.count('玉哥')
        if count > 0:
            results.append((fp, count))

results.sort(key=lambda x: -x[1])

print(f"\n{'文件':<70} {'玉哥次数':>8}")
print('-' * 90)
for fp, n in results:
    name = os.path.relpath(fp, ROOT)
    print(f"{name:<70} {n:>8}")

print(f"\n共 {len(results)} 个 HTML 含 '玉哥'")
print(f"总次数: {sum(n for _, n in results)}")