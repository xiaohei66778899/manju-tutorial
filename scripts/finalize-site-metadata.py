"""Apply safe, repeatable launch metadata and placeholder cleanup to public pages."""

from __future__ import annotations

import html
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"


def public_pages():
    for path in SITE.rglob("*.html"):
        relative_parts = path.relative_to(SITE).parts
        if "repos" in relative_parts or "legacy" in relative_parts:
            continue
        yield path


def plain_title(source: str) -> str:
    match = re.search(r"<title>(.*?)</title>", source, flags=re.I | re.S)
    if not match:
        return "漫剧制作教程"
    title = re.sub(r"<[^>]+>", "", match.group(1))
    title = html.unescape(re.sub(r"\s+", " ", title)).strip()
    return title or "漫剧制作教程"


def update_page(path: Path) -> bool:
    source = path.read_text(encoding="utf-8")
    updated = source

    if not re.search(r'<meta\s+name=["\']description["\']', updated, flags=re.I):
        description = f"{plain_title(updated)}。玉哥整理的 AI 漫剧与短剧制作实用教程，包含步骤、案例和练习。"
        meta = f'<meta name="description" content="{html.escape(description, quote=True)}">'
        viewport = re.search(r'<meta\s+name=["\']viewport["\'][^>]*>', updated, flags=re.I)
        charset = re.search(r'<meta\s+charset=[^>]*>', updated, flags=re.I)
        anchor = viewport or charset
        if anchor:
            updated = updated[: anchor.end()] + "\n" + meta + updated[anchor.end() :]

    updated = re.sub(
        r'(<a\b[^>]*\btarget=["\']_blank["\'])(?![^>]*\brel=)([^>]*>)',
        r'\1 rel="noopener noreferrer"\2',
        updated,
        flags=re.I,
    )
    updated = re.sub(
        r'(<a\b[^>]*\btarget=["\']_blank["\'][^>]*\brel=["\'])(?![^"\']*noopener)([^"\']*)(["\'])',
        r'\1noopener noreferrer \2\3',
        updated,
        flags=re.I,
    )

    updated = re.sub(
        r'\s*<li><a href="mailto:yuge@local\.demo">✉\s*联系玉哥</a></li>',
        "",
        updated,
    )
    updated = updated.replace(" · 京 ICP 备 XXXXXXXX 号(待补)", "")
    updated = updated.replace('title="后期放公众号二维码"', 'title="扫码关注玉哥"')

    if path.name == "AI写小说实战课.html":
        updated = re.sub(
            r'(<div class="md-body">\s*)<h1>(.*?)</h1>',
            r'\1<h2 class="chapter-title">\2</h2>',
            updated,
            flags=re.S,
        )
        updated = updated.replace(".md-body h1{", ".md-body .chapter-title{")
        updated = updated.replace(".md-body h1{font-size:22px}", ".md-body .chapter-title{font-size:22px}")
        updated = updated.replace("body&&body.querySelector('h1')", "body&&body.querySelector('.chapter-title')")
        updated = updated.replace("body.querySelector('h1').textContent", "body.querySelector('.chapter-title').textContent")
        updated = updated.replace("nxt.querySelector('.md-body h1')", "nxt.querySelector('.md-body .chapter-title')")

    if updated == source:
        return False
    path.write_text(updated, encoding="utf-8", newline="")
    return True


def main() -> None:
    changed = [path for path in public_pages() if update_page(path)]
    print(f"updated={len(changed)}")


if __name__ == "__main__":
    main()
