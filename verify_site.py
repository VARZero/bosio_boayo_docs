#!/usr/bin/env python3
"""Check generated pages and local links before publishing."""
from __future__ import annotations

import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

from build_site import PAGES, ROOT


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.lang = None
        self.h1 = 0

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "html":
            self.lang = attributes.get("lang")
        if tag == "h1":
            self.h1 += 1
        for key in ("href", "src"):
            if key in attributes:
                self.links.append(attributes[key])


def main():
    errors = []
    for slug, *_ in PAGES:
        page = ROOT / f"{slug}.html"
        if not page.is_file():
            errors.append(f"missing page: {page.name}")
            continue
        parser = PageParser()
        parser.feed(page.read_text(encoding="utf-8"))
        if parser.lang != "ko" or parser.h1 != 1:
            errors.append(f"invalid language or heading count: {page.name}")
        for link in parser.links:
            parsed = urlsplit(link)
            if parsed.scheme or parsed.netloc or link.startswith("#"):
                continue
            target = (ROOT / unquote(parsed.path)).resolve() if parsed.path else page
            if target.is_dir():
                target /= "index.html"
            if not target.is_relative_to(ROOT) or not target.is_file():
                errors.append(f"broken local link: {page.name} → {link}")
    search = json.loads((ROOT / "assets" / "search-index.json").read_text(encoding="utf-8"))
    if len(search) != len(PAGES):
        errors.append("search index page count differs")
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    if sitemap.count("<loc>") != len(PAGES):
        errors.append("sitemap page count differs")
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"verified {len(PAGES)} pages, local links, search index and sitemap")


if __name__ == "__main__":
    main()
