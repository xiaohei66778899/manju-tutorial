# -*- coding: utf-8 -*-
"""清理全站 HTML 中重复的 </script></script> 关闭标签
原因:之前复制 tutorial.js 时遗留,会导致脚本报错
修法:把 </script></script> 替换成 </script>
"""
import os, sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = r'E:\AIGC\课件\12小说'
OLD = '</script></script>'
NEW = '</script>'

changed = 0
for root, dirs, files in os.walk(ROOT):
    if any(seg in root for seg in ['node_modules', '.git', 'backup', '_brainmap', '_debug-archives', '_trash-removed']):
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

print(f'\n✅ 共清理 {changed} 个 HTML 的重复 </script></script> 标签')