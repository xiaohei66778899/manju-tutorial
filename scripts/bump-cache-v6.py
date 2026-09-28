# -*- coding: utf-8 -*-
"""统一升级主站 CSS/JS cache-bust；重复执行不会反复改写。"""
import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = r'E:\AIGC\课件\12小说'
NEW_VERSION = 'fix20260927-2215'
ASSET_RE = re.compile(
    r'((?:site|page|tutorial|nav-active|site-enhance|classroom-picker)\.(?:css|js)\?v=)fix\d{8}-\d{4}'
)

changed = 0
for root, dirs, files in os.walk(ROOT):
    if any(seg in root for seg in ['node_modules', '.git', 'backup', '_brainmap', '_debug-archives', os.sep + 'repos' + os.sep]):
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
            original = text
            text = ASSET_RE.sub(rf'\g<1>{NEW_VERSION}', text)
            if text != original:
                changed += 1
                out = (b'\xef\xbb\xbf' + text.encode('utf-8')) if has_bom else text.encode('utf-8')
                with open(fp, 'wb') as fh:
                    fh.write(out)
        except Exception as e:
            print(f'❌ {fp}: {e}')

print(f'\n✅ 更新页面: {changed} · 新版本: {NEW_VERSION}')
