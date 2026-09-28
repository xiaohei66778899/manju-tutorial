# -*- coding: utf-8 -*-
"""测试 getTutorialIndexPath 在所有路径场景下的输出"""
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def getTutorialIndexPath(pathname):
    parts = [p for p in pathname.split('/') if p]
    site_idx = parts.index('site') if 'site' in parts else -1
    tutorial_idx = parts.index('tutorial') if 'tutorial' in parts else -1

    # 情况 1:在 tutorial/ 下,兼容本地 /site/ 前缀和线上根目录部署
    if tutorial_idx != -1:
        after_tutorial = parts[tutorial_idx + 1:]
        if len(after_tutorial) == 1 and after_tutorial[0] in ('index.html', 'all-courses.html'):
            return ''
        is_directory = pathname.endswith('/')
        up_levels = max(0, len(after_tutorial) - (0 if is_directory else 1))
        return '../' * up_levels + 'all-courses.html'

    # 情况 2:在 site/ 下但不在 tutorial/ 下
    if site_idx != -1:
        after_site = parts[site_idx + 1:]
        if len(after_site) == 1:
            return 'tutorial/index.html'
        up_levels = len(after_site) - 1 + 1
        return '../' * up_levels + 'tutorial/index.html'

    # 情况 3:不在 site/ 下
    return 'tutorial/all-courses.html'


cases = [
    ('/site/tutorial/all-courses.html', ''),
    ('/site/tutorial/A-manju-basic/A-1.html', '../all-courses.html'),
    ('/site/tutorial/C-character/C-1.html', '../all-courses.html'),
    ('/site/tutorial/A-manju-basic/', '../all-courses.html'),
    ('/site/index.html', 'tutorial/index.html'),
    ('/site/changelog.html', 'tutorial/index.html'),
    ('/site/H-publish/H-3.html', '../../tutorial/index.html'),  # 出 H-publish/ + site/
    ('/剧本.html', 'tutorial/all-courses.html'),
    ('/剧本-01-选题.html', 'tutorial/all-courses.html'),
    # 部署后场景(去掉 /site/)
    ('/tutorial/all-courses.html', ''),
    ('/tutorial/A-manju-basic/A-1.html', '../all-courses.html'),
    ('/index.html', 'tutorial/all-courses.html'),
    # 嵌套深目录
    ('/some/deep/path/site/tutorial/A/B/C.html', '../../all-courses.html'),
]

print(f"{'路径':<60} {'期望':<45} {'实际':<45} {'OK'}")
print('-' * 160)
all_ok = True
for path, expected in cases:
    actual = getTutorialIndexPath(path)
    ok = '✓' if actual == expected else '✗'
    if actual != expected:
        all_ok = False
    print(f"{path:<60} {expected:<45} {actual:<45} {ok}")

print()
print('🎉 全部通过' if all_ok else '⚠️  有失败用例')
