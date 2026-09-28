from pathlib import Path
from html import escape
import re

import markdown


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "site" / "tutorial" / "N-aixiexiaoshuo"
OUT = BASE / "AI写小说实战课.html"


def md_html(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    return markdown.markdown(
        text,
        extensions=["extra", "tables", "fenced_code", "sane_lists"],
        output_format="html5",
    )


chapters = sorted(
    BASE.joinpath("tutorials").glob("chapter-*.md"),
    key=lambda p: int(re.search(r"chapter-(\d+)", p.name).group(1)),
)
articles = [p for p in sorted(BASE.joinpath("articles").glob("*.md")) if p.name != "_index.md"]

chapter_nav = "".join(
    f'<a href="#chapter-{i}"><span>{i:02d}</span>{escape(p.stem.replace(f"chapter-{i}-", ""))}</a>'
    for i, p in enumerate(chapters, 1)
)
article_nav = "".join(
    f'<a href="#article-{i}">{escape(p.stem)}</a>' for i, p in enumerate(articles, 1)
)
chapter_sections = "".join(
    f'<article class="lesson" id="chapter-{i}"><div class="section-kicker">第 {i} 章</div>{md_html(p)}'
    f'<a class="back-top" href="#course-top">返回目录 ↑</a></article>'
    for i, p in enumerate(chapters, 1)
)
article_sections = "".join(
    f'<article class="lesson resource" id="article-{i}"><div class="section-kicker">延伸阅读 {i}</div>{md_html(p)}'
    f'<a class="back-top" href="#articles">返回文章目录 ↑</a></article>'
    for i, p in enumerate(articles, 1)
)

html = f'''<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<meta name="description" content="AI 写小说实战课：15 章完整教程、工具选型、提示词、世界观、大纲、章节创作、一致性检查与发布运营。">
<title>AI 写小说实战课 · 玉哥漫剧教程站</title>
<link rel="icon" type="image/svg+xml" href="../../favicon.svg?v=fix20260927-2215">
<link rel="stylesheet" href="../../assets/site.css?v=fix20260927-2215">
<style>
:root{{--n-blue:#3b72f0;--n-soft:#eef3fb;--n-card:#fff;--n-line:#dbe5f4}}
html{{scroll-behavior:smooth;scroll-padding-top:72px}}
body.ainovel-page{{background:linear-gradient(135deg,#eef3fb 0,#fafbfc 36%,#fffaf2 100%);color:#182235}}
.n-shell{{width:min(1180px,calc(100% - 32px));margin:0 auto;padding:34px 0 80px}}
.n-hero{{padding:54px clamp(22px,5vw,68px);border:1px solid var(--n-line);border-radius:24px;background:linear-gradient(135deg,#e8f0ff,#fafbfc 55%,#fff);box-shadow:0 18px 60px rgba(45,88,160,.10)}}
.n-hero h1{{font-size:clamp(30px,5vw,56px);margin:0 0 14px;line-height:1.12}}
.n-hero p{{max-width:760px;color:#536277;font-size:17px;line-height:1.8}}
.n-stats{{display:flex;gap:10px;flex-wrap:wrap;margin-top:24px}}.n-stats span{{padding:8px 14px;border-radius:999px;background:#fff;border:1px solid var(--n-line);font-weight:700}}
.n-panel,.lesson{{margin-top:24px;padding:clamp(20px,4vw,42px);background:rgba(255,255,255,.94);border:1px solid var(--n-line);border-radius:20px;box-shadow:0 10px 34px rgba(45,88,160,.07)}}
.n-panel h2{{margin-top:0}}.chapter-grid,.article-grid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}}
.chapter-grid a,.article-grid a{{display:flex;gap:10px;align-items:center;min-height:52px;padding:12px 14px;border:1px solid var(--n-line);border-radius:12px;background:#f8fbff;color:#22395f;text-decoration:none}}
.chapter-grid a:hover,.article-grid a:hover{{border-color:var(--n-blue);transform:translateY(-1px)}}.chapter-grid span{{color:var(--n-blue);font-weight:800}}
.lesson{{line-height:1.85;overflow-wrap:anywhere}}.lesson h1{{font-size:clamp(26px,4vw,40px)}}.lesson h2{{margin-top:32px;border-left:4px solid var(--n-blue);padding-left:12px}}.lesson h3{{margin-top:24px}}
.lesson img{{max-width:100%;height:auto}}.lesson table{{width:100%;border-collapse:collapse;display:block;overflow-x:auto}}.lesson th,.lesson td{{border:1px solid var(--n-line);padding:10px;text-align:left;min-width:110px}}.lesson pre{{overflow:auto;padding:16px;border-radius:12px;background:#13213a;color:#eef5ff}}.lesson blockquote{{margin:18px 0;padding:12px 18px;border-left:4px solid var(--n-blue);background:var(--n-soft)}}
.section-kicker{{color:var(--n-blue);font-weight:800;letter-spacing:.08em}}.back-top{{display:inline-block;margin-top:24px;color:var(--n-blue)}}
@media(max-width:820px){{.chapter-grid,.article-grid{{grid-template-columns:1fr 1fr}}.n-shell{{width:min(100% - 20px,1180px);padding-top:18px}}}}
@media(max-width:520px){{.chapter-grid,.article-grid{{grid-template-columns:1fr}}.n-hero{{border-radius:16px;padding:30px 20px}}.n-panel,.lesson{{border-radius:14px;padding:18px}}}}
</style>
</head>
<body class="ainovel-page" id="course-top">
<header class="topbar">
  <div class="logo">🎬 漫剧教程站 <small>v3 · 玉哥</small></div>
  <nav>
    <a href="../../index.html">首页</a><a href="../all-courses.html" class="active">漫剧教程</a><a href="../../prompts/image-prompts.html">图片作品</a><a href="../../works/index.html">视频作品</a><a href="../../prompts/prompts.html">prompt 模板</a><a href="../../tools/toolkit.html">工具箱</a><a href="../../qa/troubleshooting.html">问题库</a><a href="../../news/industry.html">行业新闻</a>
  </nav>
  <button class="theme-toggle" id="yugeThemeBtn" title="深浅主题切换" aria-label="切换深浅主题">🌙</button>
</header>
<main class="n-shell">
  <section class="n-hero"><div>📖 玉哥原创专题</div><h1>AI 写小说实战课</h1><p>从工具选择、提示词和世界观，到大纲、章节创作、一致性检查、润色、评估与发布运营。15 章完整路径，按顺序学，也可直接跳到当前问题。</p><div class="n-stats"><span>15 章教程</span><span>12 篇延伸阅读</span><span>本地静态 · 手机适配</span></div></section>
  <section class="n-panel"><h2>课程目录</h2><div class="chapter-grid">{chapter_nav}</div></section>
  {chapter_sections}
  <section class="n-panel" id="articles"><h2>延伸阅读</h2><div class="article-grid">{article_nav}</div></section>
  {article_sections}
</main>
<script src="../../assets/site-enhance.js?v=fix20260927-2215" defer></script>
</body>
</html>'''

OUT.write_text(html, encoding="utf-8", newline="\n")
print(f"rebuilt {OUT} ({OUT.stat().st_size} bytes)")
