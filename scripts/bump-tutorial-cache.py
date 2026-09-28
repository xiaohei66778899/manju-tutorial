import os, sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'E:\AIGC\课件\12小说'
OLD = 'tutorial.js?v=fix20260918-1220'
NEW = 'tutorial.js?v=fix20260919-1151'

changed = 0
for root, dirs, files in os.walk(ROOT):
    if 'node_modules' in root or '.git' in root or 'backup' in root or '_brainmap' in root or '_debug-archives' in root:
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
            if OLD in text:
                text = text.replace(OLD, NEW)
                out = (b'\xef\xbb\xbf' + text.encode('utf-8')) if has_bom else text.encode('utf-8')
                with open(fp, 'wb') as fh:
                    fh.write(out)
                changed += 1
        except Exception as e:
            print(f'❌ {fp}: {e}')

print(f'\n✅ 共更新 {changed} 个 HTML 的 tutorial.js cache-bust 版本号')
