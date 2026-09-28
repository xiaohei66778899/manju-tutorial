# -*- coding: utf-8 -*-
"""补丁:修复根目录 HTML 的 QR 图片路径
   把 `src="./qr-yuge.png"` → `src="assets/qr-yuge.png"`
"""
import os, sys, re
sys.stdout.reconfigure(encoding='utf-8')

ROOT = r'E:\AIGC\课件\12小说'
SITE_DIR = os.path.join(ROOT, 'site')
PATTERN = re.compile(r'src="\./qr-yuge\.png(\?v=[^"]*)"')

changed = 0
for root, dirs, files in os.walk(SITE_DIR):
    if any(seg in root for seg in ['node_modules', '.git', 'backup', '_brainmap', '_debug-archives']):
        continue
    for f in files:
        if not f.endswith('.html'):
            continue
        fp = os.path.join(root, f)
        try:
            with open(fp, 'rb') as fh:
                raw = fh.read()
            has_bom = raw.startswith(b'\xef\xbb\xbf')
            text = raw.decode('utf-8-sig') if has_bom else raw.decode('utf-8')
            if PATTERN.search(text):
                text = PATTERN.sub(r'src="assets/qr-yuge.png\1"', text)
                out = (b'\xef\xbb\xbf' + text.encode('utf-8')) if has_bom else text.encode('utf-8')
                with open(fp, 'wb') as fh:
                    fh.write(out)
                changed += 1
        except Exception as e:
            print(f'❌ {fp}: {e}')

print(f'\n✅ 修复根目录 QR 路径: {changed} 个 HTML')