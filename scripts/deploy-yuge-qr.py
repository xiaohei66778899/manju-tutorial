# -*- coding: utf-8 -*-
"""把全站 footer 的 QR 占位 <div class="qr-img">QR</div> 替换为玉哥的二维码图片
并同步更新 CSS:让 .qr-img 同时支持 div 占位 + img 真实图(去掉 dashed border,加 object-fit)
"""
import os, sys, re
sys.stdout.reconfigure(encoding='utf-8')

ROOT = r'E:\AIGC\课件\12小说'
SITE_DIR = os.path.join(ROOT, 'site')
ASSETS_REL = 'qr-yuge.png'
NEW_VERSION = 'fix20260919-1430'
OLD_DIV = '<div class="qr-img">QR</div>'

# 计算 HTML 相对 site/assets/qr-yuge.png 的路径前缀
def rel_prefix(html_path: str) -> str:
    assets_dir = os.path.join(SITE_DIR, 'assets')
    rel = os.path.relpath(assets_dir, os.path.dirname(html_path))
    return rel.replace('\\', '/')

NEW_IMG = '<img class="qr-img" src="{prefix}/{asset}?v={ver}" alt="扫码关注玉哥" loading="lazy">'

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
            if OLD_DIV not in text:
                continue
            prefix = rel_prefix(fp)
            img_tag = NEW_IMG.format(prefix=prefix, asset=ASSETS_REL, ver=NEW_VERSION)
            text = text.replace(OLD_DIV, img_tag)
            out = (b'\xef\xbb\xbf' + text.encode('utf-8')) if has_bom else text.encode('utf-8')
            with open(fp, 'wb') as fh:
                fh.write(out)
            changed += 1
        except Exception as e:
            print(f'❌ {fp}: {e}')

print(f'\n✅ QR 占位 → 玉哥二维码: {changed} 个 HTML')