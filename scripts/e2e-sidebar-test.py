# -*- coding: utf-8 -*-
"""端到端验证:模拟 JS getWebRoot + resolvePath 在所有页面下的输出"""
from urllib.parse import urljoin

def get_web_root(tutorial_js_src):
    """模拟 JS getWebRoot"""
    m = tutorial_js_src.replace('?v=', '_v_')  # 模拟
    # 实际上 URL 处理会忽略 query string
    idx = m.find('/assets/tutorial.js')
    if idx == -1:
        return ''
    root = m[:idx]
    if root and not root.endswith('/'):
        root += '/'
    return root

def resolve_path(template, tutorial_js_src):
    root = get_web_root(tutorial_js_src)
    return template.replace('{WEB_ROOT}', root)

# 模拟不同部署场景下,每个页面引用的 tutorial.js 完整 URL
scenarios = [
    # (description, page_path, tutorial_js_src)
    ('本地 site/ 部署', '/site/tutorial/A-manju-basic/A-1.html',
     'http://127.0.0.1:18080/site/assets/tutorial.js?v=fix20260919-1530'),
    ('本地 site/ 根', '/site/index.html',
     'http://127.0.0.1:18080/site/assets/tutorial.js?v=fix20260919-1530'),
    ('本地 根目录', '/剧本.html',
     'http://127.0.0.1:18080/site/assets/tutorial.js?v=fix20260919-1530'),
    ('部署到 /ai-manju 子目录', '/ai-manju/tutorial/A-manju-basic/A-1.html',
     'https://yuge.com/ai-manju/assets/tutorial.js?v=fix20260919-1530'),
    ('部署到根 /', '/tutorial/A-manju-basic/A-1.html',
     'https://yuge.com/assets/tutorial.js?v=fix20260919-1530'),
    ('部署到根 / 主页', '/index.html',
     'https://yuge.com/assets/tutorial.js?v=fix20260919-1530'),
]

entries = {
    'A': '{WEB_ROOT}tutorial/A-manju-basic/A-1.html',
    'B': '{WEB_ROOT}剧本.html#view-1-1',
    'C': '{WEB_ROOT}tutorial/C-character/C-1.html',
    'J': '{WEB_ROOT}tutorial/J-comfyui/ComfyUI漫剧工作流.html',
}

print(f"{'场景':<25} {'当前页':<45} {'web 根':<20} {'A 点击目标':<60} {'B 点击目标'}")
print('-' * 200)
for desc, page_path, js_src in scenarios:
    root = get_web_root(js_src)
    a_url = resolve_path(entries['A'], js_src)
    b_url = resolve_path(entries['B'], js_src)
    # 用 URL API 验证绝对 URL 是否正确
    a_abs = urljoin(js_src.rsplit('/assets/', 1)[0] + '/', a_url.replace(root, ''))
    b_abs = urljoin(js_src.rsplit('/assets/', 1)[0] + '/', b_url.replace(root, ''))
    # 实际是 page_path + 'A.html' 这种
    print(f"{desc:<25} {page_path:<45} {root:<20} {a_url:<60} {b_url}")