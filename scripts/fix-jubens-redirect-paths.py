# -*- coding: utf-8 -*-
"""修复 site/剧本-XX-XX.html 的 src 路径错误
原:`site/assets/site-enhance.js` (假设在根目录)
现:`assets/site-enhance.js` (在 site/ 下)
"""
import os, sys, glob
sys.stdout.reconfigure(encoding='utf-8')

SITE_DIR = r'E:\AIGC\课件\12小说\site'
files = glob.glob(os.path.join(SITE_DIR, '剧本-*.html'))
files = [f for f in files if not os.path.basename(f).endswith('-01-选题.html') or True]
# 其实都改

changed = 0
for fp in files:
    with open(fp, 'rb') as fh:
        raw = fh.read()
    has_bom = raw.startswith(b'\xef\xbb\xbf')
    text = raw.decode('utf-8-sig') if has_bom else raw.decode('utf-8')
    original = text
    # 修正路径:site/assets/ → assets/
    text = text.replace('site/assets/', 'assets/')
    if text != original:
        out = (b'\xef\xbb\xbf' + text.encode('utf-8')) if has_bom else text.encode('utf-8')
        with open(fp, 'wb') as fh:
            fh.write(out)
        changed += 1
        print(f'✅ {os.path.basename(fp)}')

print(f'\n共修复 {changed} 个引导页路径')