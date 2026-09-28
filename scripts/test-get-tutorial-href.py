# -*- coding: utf-8 -*-
"""用 Python URL API 模拟 JS 函数,确保所有场景返回正确"""
from urllib.parse import urljoin

def get_tutorial_href(path, code='B'):
    """模拟 JS getTutorialHref"""
    # 特殊情况:当前页就是 tutorial/index.html
    if path.endswith('/tutorial/index.html'):
        return f'#{code}'

    # 找路径中 tutorial/ 的位置
    tutorial_marker = '/tutorial/'
    tutorial_idx = path.find(tutorial_marker)

    if tutorial_idx == -1:
        # 没有 tutorial/ 前缀
        site_marker = '/site/'
        if site_marker in path:
            # 在 site/ 下
            after_site = path.split('/site/', 1)[1]
            # 去掉尾部 /
            after_site = after_site.rstrip('/')
            if after_site == 'index.html' or after_site == '':
                return f'tutorial/index.html#{code}'
            # 在 site/ 子目录下
            segs = [s for s in after_site.split('/') if s]
            return '../' * len(segs) + f'tutorial/index.html#{code}'
        # 不在 site/ 下(根目录 HTML)
        return f'site/tutorial/index.html#{code}'

    # 在 tutorial/ 下
    after_tutorial = path[tutorial_idx + len(tutorial_marker):]
    # 去掉尾部 /
    after_tutorial = after_tutorial.rstrip('/')
    segs = [s for s in after_tutorial.split('/') if s]
    # upLevels:从 segs 最后一层回到 tutorial/ 目录
    # segs = ['A-manju-basic', 'A-1.html'] (2 个),../ 出 1 层 (../ 是从 segs[0] 开始,不是从文件名)
    # 等等,urljoin 的 ../ 是从 path 的目录部分起算,不是从文件名
    # 所以 segs.length - 1 才是正确的出层数(去掉最后一段文件名)
    # /tutorial/A-manju-basic/A-1.html → segs 2 个,../ = ../../index.html?不对,是 ../index.html
    # 实际规则:../ 从 path 的目录部分算起,只算到目录
    # segs = ['A-manju-basic', 'A-1.html'],path 的目录部分 = /tutorial/A-manju-basic/
    # ../index.html = /tutorial/index.html ✅ (出 1 层)
    # 所以规则:upLevels = segs.length - 1 (减掉文件名)
    # 但是目录 path:/tutorial/A-manju-basic/ → segs = ['A-manju-basic'],length = 1
    # ../index.html = /tutorial/index.html ✅ (出 1 层)
    # segs.length - 1 = 0 ❌
    # 所以:目录 path 要算成 segs.length
    # 通用规则:upLevels = segs.length,但最后是 index.html 时 -1
    if len(segs) == 1 and segs[0] == 'index.html':
        return f'#{code}'  # 已处理
    up_levels = len(segs) - 1  # 默认减掉文件名
    # 但如果是目录 path(末尾没有文件名),需要 +1
    # 简化:看 path 是否以 / 结尾,或者 segs 最后一个是不是 .html
    if not segs[-1].endswith('.html'):
        up_levels += 1
    return '../' * up_levels + f'index.html#{code}'


cases = [
    ('/site/tutorial/index.html', '../index.html', '用 #'),
    ('/site/tutorial/A-manju-basic/A-1.html', '../index.html', ''),
    ('/site/tutorial/A-manju-basic/', '../index.html', ''),
    ('/site/tutorial/A/B/C.html', '../../index.html', ''),
    ('/site/tutorial/C-character/C-5.html', '../index.html', ''),
    ('/site/index.html', 'tutorial/index.html', ''),
    ('/site/changelog.html', 'tutorial/index.html', ''),
    ('/site/H-publish/H-3.html', '../../tutorial/index.html', ''),
    ('/剧本.html', 'site/tutorial/index.html', ''),
    ('/剧本-01-选题.html', 'site/tutorial/index.html', ''),
    ('/tutorial/index.html', 'inline #', '部署后'),
    ('/tutorial/A-manju-basic/A-1.html', '../index.html', '部署后'),
    ('/index.html', 'tutorial/index.html', '部署后'),
    ('/some/deep/path/site/tutorial/A/B/C.html', '../../../index.html', '深目录'),
]

print(f"{'当前路径':<60} {'期望':<45} {'实际 href':<40} {'解析后 URL'}")
print('-' * 200)
all_ok = True
for cur, expected, note in cases:
    href = get_tutorial_href(cur)
    if href.startswith('#'):
        joined = cur + href
    else:
        joined = urljoin(cur, href)
    ok = '✅' if expected in href or (href.startswith('#') and 'inline' in expected) else '❌'
    if 'inline' in expected and href.startswith('#'):
        ok = '✅'
    elif expected not in href:
        ok = '❌'
        all_ok = False
    print(f"{cur:<60} {expected:<45} {href:<40} {joined}  {ok}  {note}")

print()
print('🎉 全部通过' if all_ok else '⚠️  有失败用例')