#!/usr/bin/env python3
"""Synchronize project-card structure from English while retaining localized copy.

Run: python3 scripts/sync_portfolio.py
English is canonical for tile order, CSS classes, inline styles and image sources.
Other language pages retain their own titles, descriptions, alt text and aria labels.
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
LANGUAGES = ("", "es", "it")
MOSAIC = re.compile(r"(<div class='mosaic' id='trabalhos'>)(.*?)(</div>)", re.S)
TILE = re.compile(r'(<button\b[^>]*\bdata-case="([^"]+)"[^>]*>.*?</button>)', re.S)
IMAGE = re.compile(r'<img\b[^>]*>', re.S)
CAPTION = re.compile(r'<span class="cap">.*?</span></span>', re.S)
ARIA = re.compile(r'aria-label="[^"]*"')
SRC = re.compile(r'\bsrc="([^"]*)"')
ALT = re.compile(r'\balt="[^"]*"')

def section(html, path):
    match = MOSAIC.search(html)
    if not match:
        raise ValueError(f"Missing project mosaic: {path}")
    return match

def cards(html, path):
    match = section(html, path)
    result = dict((key, markup) for markup, key in TILE.findall(match.group(2)))
    if not result:
        raise ValueError(f"No cards found: {path}")
    return result

def localized_card(master, existing, prefix):
    # Keep the translated accessible name and card caption.
    aria = ARIA.search(existing)
    caption = CAPTION.search(existing)
    image = IMAGE.search(existing)
    output = master
    if aria:
        output = ARIA.sub(lambda _: aria.group(0), output, count=1)
    if caption:
        output = CAPTION.sub(lambda _: caption.group(0), output, count=1)
    if image:
        alt = ALT.search(image.group(0))
        if alt:
            output = IMAGE.sub(lambda m: ALT.sub(lambda _: alt.group(0), m.group(0), count=1), output, count=1)
    # Image paths in English are ../img/; root PT uses img/.
    if prefix == "":
        output = output.replace('src="../img/', 'src="img/')
    return output

def main():
    source_path = ROOT / "en" / "index.html"
    source = source_path.read_text(encoding="utf-8")
    canonical = cards(source, source_path)
    order = list(canonical)
    changed = []
    for lang in LANGUAGES:
        path = ROOT / lang / "index.html" if lang else ROOT / "index.html"
        html = path.read_text(encoding="utf-8")
        local = cards(html, path)
        if set(local) != set(canonical):
            raise ValueError(f"Card mismatch in {path}: missing={set(canonical)-set(local)}, extra={set(local)-set(canonical)}")
        match = section(html, path)
        new_tiles = "".join(localized_card(canonical[key], local[key], "" if not lang else "../") for key in order)
        # Preserve surrounding whitespace outside tile markup.
        original = match.group(2)
        if TILE.sub("", original).strip():
            raise ValueError(f"Unexpected mosaic content in {path}; refusing destructive rewrite")
        updated = html[:match.start(2)] + new_tiles + html[match.end(2):]
        if updated != html:
            path.write_text(updated, encoding="utf-8")
            changed.append(str(path.relative_to(ROOT)))
    print("Synchronized:", ", ".join(changed) if changed else "already current")

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"Sync failed: {exc}", file=sys.stderr)
        sys.exit(1)
