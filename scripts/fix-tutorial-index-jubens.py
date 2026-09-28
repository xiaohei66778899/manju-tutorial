# -*- coding: utf-8 -*-
"""修复 site/tutorial/index.html 的 8 个 B 模块卡片链接路径
   href="../../剧本.html" → href="../剧本.html"
"""
import os, sys
sys.stdout.reconfigure(encoding='utf-8')

fp = r'E:\AIGC\课件\12小说\site\tutorial\index.html'
OLD = 'href="../../剧本.html'
NEW = 'href="../剧本.html'

with open(fp, 'rb') as fh:
    raw = fh.read()
has_bom = raw.startswith(b'\xef\xbb\xbf')
text = raw.decode('utf-8-sig') if has_bom else raw.decode('utf-8')

count = text.count(OLD)
text = text.replace(OLD, NEW)

out = (b'\xef\xbb\xbf' + text.encode('utf-8')) if has_bom else text.encode('utf-8')
with open(fp, 'wb') as fh:
    fh.write(out)

print(f'✅ {fp}: 修复 {count} 个链接')