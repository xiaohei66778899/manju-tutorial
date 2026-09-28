# -*- coding: utf-8 -*-
from urllib.parse import urljoin
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# 验证正确的相对路径
print('=== 验证 sidebar 大类跳转正确的相对路径 ===\n')
cases = [
    ('/tutorial/index.html', '#A', '当前 = tutorial/index.html,直接 #A'),
    ('/tutorial/A-manju-basic/A-1.html', 'A-manju-basic/index.html', '错误:目标是 tutorial/index.html 不是 A-manju-basic/index.html'),
    ('/tutorial/A-manju-basic/A-1.html', '../index.html', '试../index.html'),
    ('/tutorial/A-manju-basic/A-1.html', '../../index.html', '试../../index.html'),
    ('/site/tutorial/A-manju-basic/A-1.html', '../index.html', 'site/版本 ../index.html'),
    ('/site/tutorial/A-manju-basic/A-1.html', '../../index.html', 'site/版本 ../../index.html'),
    ('/index.html', 'tutorial/index.html', 'site/根进 tutorial/'),
    ('/site/index.html', 'tutorial/index.html', 'site/根进 tutorial/(含 site/)'),
    ('/site/H-publish/H-3.html', '../../tutorial/index.html', 'site/H-publish 出两层'),
    ('/site/H-publish/H-3.html', '../tutorial/index.html', 'site/H-publish 出一层'),
    ('/site/H-publish/H-3.html', '../../index.html', 'site/H-publish ../../'),
    ('/site/H-publish/H-3.html', '../index.html', 'site/H-publish ../'),
    ('/some/deep/path/site/tutorial/A/B/C.html', '../../../index.html', '深目录'),
]
for cur, rel, note in cases:
    joined = urljoin(cur, rel)
    marker = '✅' if 'tutorial/index.html' in joined and 'tutorial/tutorial' not in joined else '❌'
    print(f"{marker} {cur} + {rel}")
    print(f"     → {joined}")
    print(f"     ({note})\n")
