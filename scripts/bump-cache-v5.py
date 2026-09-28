# -*- coding: utf-8 -*-
"""升级 tutorial.js cache-bust 版本号 + CSS
   tutorial.js?v=fix20260919-1300 → ?v=fix20260919-1500
   tutorial.css?v=fix20260919-1300 → ?v=fix20260919-1500
"""
import os, sys, re
sys.stdout.reconfigure(encoding='utf-8')

ROOT = r'E:\AIGC\课件\12小说'
OLD_JS = 'tutorial.js?v=fix20260919-1300'
OLD_CSS = 'tutorial.css?v=fix20260919-1300'
NEW_VERSION = 'fix20260919-1500'
NEW_JS = f'tutorial.js?v={NEW_VERSION}'
NEW_CSS = f'tutorial.css?v={NEW_VERSION}'

js_changed = 0
css_changed = 0

for root, dirs, files in os.walk(ROOT):
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
            original = text
            if OLD_JS in text:
                text = text.replace(OLD_JS, NEW_JS)
                js_changed += 1
            if OLD_CSS in text:
                text = text.replace(OLD_CSS, NEW_CSS)
                css_changed += 1
            if text != original:
                out = (b'\xef\xbb\xbf' + text.encode('utf-8')) if has_bom else text.encode('utf-8')
                with open(fp, 'wb') as fh:
                    fh.write(out)
        except Exception as e:
            print(f'❌ {fp}: {e}')

print(f'\n✅ JS 升级: {js_changed} · CSS 升级: {css_changed} · 新版本: {NEW_VERSION}')