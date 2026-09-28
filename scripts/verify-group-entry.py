# -*- coding: utf-8 -*-
from urllib.parse import urljoin
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# 测试 sidebar 大类 entry 相对路径在不同页面的解析结果
entries = {
    'A': 'A-manju-basic/A-1.html',
    'B': '../../剧本.html#view-1-1',
    'C': 'C-character/C-1.html',
    'D': 'D-storyboard/D-1.html',
    'E': 'E-ai-image/E-1.html',
    'F': 'F-ai-video/F-1.html',
    'G': 'G-audio-edit/G-1.html',
    'H': 'H-publish/H-1.html',
    'I': 'I-appendix/I-1.html',
    'J': 'J-comfyui/ComfyUI漫剧工作流.html',
    'K': 'K-投流/千川投流SOP.html',
    'L': 'L-airepo/短剧AI仓库.html',
}

paths = [
    '/site/tutorial/index.html',  # 教程 index
    '/site/tutorial/A-manju-basic/A-1.html',
    '/site/tutorial/A-manju-basic/',  # 目录
    '/site/tutorial/C-character/C-5.html',  # 不同子目录
    '/site/index.html',  # site 根
    '/site/H-publish/H-3.html',
    '/site/changelog.html',
    # 部署后(无 site/)
    '/tutorial/index.html',
    '/tutorial/A-manju-basic/A-1.html',
    '/index.html',
]

print(f"{'当前路径':<55} {'A entry':<30} {'B entry':<30}")
print('-' * 120)
for path in paths:
    a = urljoin(path, entries['A'])
    b = urljoin(path, entries['B'])
    a_ok = '✅' if a.endswith('A-manju-basic/A-1.html') or a.endswith('A-1.html') else '?'
    b_ok = '✅' if '剧本.html' in b and 'view-1-1' in b else '?'
    print(f"{path:<55} {a_ok}{a:<28} {b_ok}{b:<28}")
