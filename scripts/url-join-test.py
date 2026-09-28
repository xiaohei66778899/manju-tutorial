# -*- coding: utf-8 -*-
from urllib.parse import urljoin
cases = [
    ('/site/tutorial/A-manju-basic/A-1.html', '../index.html'),
    ('/site/tutorial/A-manju-basic/A-1.html', '../../index.html'),
    ('/site/tutorial/A-manju-basic/A-1.html', '../../tutorial/index.html'),
    ('/site/index.html', 'tutorial/index.html'),
    ('/site/H-publish/H-3.html', '../../tutorial/index.html'),
    ('/site/tutorial/index.html', '#B'),
    ('/site/tutorial/A-manju-basic/', '../index.html'),
    ('/some/deep/path/site/tutorial/A/B/C.html', '../../../index.html'),
    ('/some/deep/path/site/tutorial/A/B/C.html', '../../index.html'),
    ('/tutorial/A-manju-basic/A-1.html', '../index.html'),  # 部署后
    ('/index.html', 'tutorial/index.html'),  # 部署后
    ('/剧本.html', 'site/tutorial/index.html'),
]
print(f"{'当前':<55} {'相对路径':<35} {'→ 实际URL'}")
print('-' * 130)
for cur, rel in cases:
    joined = urljoin(cur, rel)
    print(f"{cur:<55} {rel:<35} → {joined}")