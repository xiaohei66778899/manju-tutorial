"""Static pre-deploy audit for the tutorial site.

Checks local links/assets and high-value HTML quality signals without changing files.
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
EXCLUDED_DIRS = {"repos", "node_modules", ".git"}
SKIP_SCHEMES = ("http:", "https:", "mailto:", "tel:", "javascript:", "data:", "blob:")


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.attrs: list[tuple[str, dict[str, str]]] = []
        self.ids: list[str] = []
        self.title_depth = 0
        self.title = ""
        self.html_attrs: dict[str, str] = {}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {k.lower(): (v or "") for k, v in attrs}
        tag = tag.lower()
        self.attrs.append((tag, values))
        if tag == "html":
            self.html_attrs = values
        if tag == "title":
            self.title_depth += 1
        if values.get("id"):
            self.ids.append(values["id"])

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "title" and self.title_depth:
            self.title_depth -= 1

    def handle_data(self, data: str) -> None:
        if self.title_depth:
            self.title += data


def resolve_local(page: Path, raw: str) -> tuple[Path | None, str]:
    raw = raw.strip()
    if not raw or raw.startswith(SKIP_SCHEMES) or raw.startswith("//"):
        return None, ""
    parts = urlsplit(raw)
    path_text = unquote(parts.path)
    if not path_text:
        return page, parts.fragment
    if path_text.startswith("/"):
        target = SITE / path_text.lstrip("/")
    else:
        target = page.parent / path_text
    target = target.resolve()
    if path_text.endswith("/"):
        target = target / "index.html"
    return target, unquote(parts.fragment)


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    pages = sorted(
        page for page in SITE.rglob("*.html")
        if not any(part in EXCLUDED_DIRS for part in page.relative_to(SITE).parts)
    )
    parsed: dict[Path, PageParser] = {}
    issues: dict[str, list[str]] = defaultdict(list)
    counts = Counter()

    for page in pages:
        rel = page.relative_to(SITE).as_posix()
        try:
            text = page.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError:
            issues["non_utf8"].append(rel)
            continue
        parser = PageParser()
        try:
            parser.feed(text)
        except Exception as exc:  # HTMLParser is tolerant; any failure is notable.
            issues["parse_error"].append(f"{rel}: {exc}")
        parsed[page.resolve()] = parser

        if not parser.title.strip():
            issues["missing_title"].append(rel)
        if "</title>" not in text.lower():
            issues["malformed_title"].append(rel)
        if not parser.html_attrs.get("lang"):
            issues["missing_lang"].append(rel)
        metas = [a for t, a in parser.attrs if t == "meta"]
        if not any(a.get("name", "").lower() == "viewport" for a in metas):
            issues["missing_viewport"].append(rel)
        if not any(a.get("name", "").lower() == "description" and a.get("content", "").strip() for a in metas):
            issues["missing_description"].append(rel)
        dupes = [key for key, n in Counter(parser.ids).items() if n > 1]
        if dupes:
            issues["duplicate_ids"].append(f"{rel}: {', '.join(dupes[:8])}")

        for tag, attrs in parser.attrs:
            if tag == "img" and not attrs.get("alt", "").strip():
                counts["img_without_alt"] += 1
                if len(issues["img_without_alt"]) < 50:
                    issues["img_without_alt"].append(rel)
            if tag == "a" and attrs.get("target") == "_blank":
                rel_tokens = set(attrs.get("rel", "").lower().split())
                if "noopener" not in rel_tokens:
                    counts["blank_without_noopener"] += 1
                    if len(issues["blank_without_noopener"]) < 50:
                        issues["blank_without_noopener"].append(rel)
            for attr in ("href", "src", "poster"):
                raw = attrs.get(attr, "")
                if not raw:
                    continue
                target, fragment = resolve_local(page.resolve(), raw)
                if target is None:
                    if raw.startswith("http://"):
                        issues["http_resource"].append(f"{rel}: {raw[:120]}")
                    continue
                if not target.exists():
                    issues["missing_local_target"].append(f"{rel}: {raw}")
                elif fragment and target.suffix.lower() == ".html":
                    target_parser = parsed.get(target)
                    if target_parser is not None and fragment not in target_parser.ids:
                        issues["missing_fragment"].append(f"{rel}: {raw}")

    # Second pass for fragments pointing forward to pages parsed later.
    missing_fragments = []
    for item in issues.pop("missing_fragment", []):
        rel, raw = item.split(": ", 1)
        page = (SITE / rel).resolve()
        target, fragment = resolve_local(page, raw)
        if target in parsed and fragment and fragment not in parsed[target].ids:
            missing_fragments.append(item)
    if missing_fragments:
        issues["missing_fragment"] = missing_fragments

    report = {
        "pages": len(pages),
        "issue_counts": {key: len(value) for key, value in sorted(issues.items()) if value},
        "occurrence_counts": dict(counts),
        "samples": {key: value[:20] for key, value in sorted(issues.items()) if value},
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    severe = len(issues.get("missing_local_target", [])) + len(issues.get("missing_viewport", []))
    return 1 if severe else 0


if __name__ == "__main__":
    raise SystemExit(main())
