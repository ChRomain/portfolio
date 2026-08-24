#!/usr/bin/env python3
"""
One-off / re-runnable maintenance script: extracts inline base64 LQIP JPEGs
embedded in the `style="background-image: url(data:image/jpeg;base64,...)"`
attribute of <img> tags inside content/gallery/*/index*.md, writes each LQIP
as a separate static file under static/gallery/<destination>/lqip/<name>.jpg,
and rewrites the markdown to point at that file URL instead of the inline
data URI.

Why: sync_photos.py used to bake each LQIP inline as base64, which bloats
every gallery page's HTML by tens of KB per page and defeats HTTP caching
(re-downloaded on every page view). Extracting them to small static files
lets the browser cache them normally.

This script only ever touches text inside <img ...> tags, and only the
`style` attribute's base64 payload — every other attribute (alt, title,
loading, decoding, data-lqip, onload, width, height, src) and everything
outside of <img> tags (frontmatter, other HTML blocks, etc.) is left
byte-for-byte identical.

Usage:
    python3 scripts/extract_lqip.py

Safe to re-run: images already using a file-based LQIP are left untouched
(the style regex only matches the base64 data-URI form), and identical
LQIPs sharing the same destination+basename are decoded/written only once.
"""
import base64
import glob
import os
import re

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT_ROOT = os.path.join(REPO_ROOT, "content", "gallery")
STATIC_ROOT = os.path.join(REPO_ROOT, "static", "gallery")

IMG_RE = re.compile(r"<img\b.*?/>", re.DOTALL)
SRC_RE = re.compile(r'src="([^"]+)"')
STYLE_RE = re.compile(
    r'style="background-image:\s*url\(data:image/jpeg;base64,([A-Za-z0-9+/=]+)\);\s*background-size:\s*cover;"'
)


def main():
    written_cache = {}  # (dest, basename) -> lqip_rel_url, avoids redundant decode/write

    stats = {
        "files_scanned": 0,
        "files_changed": 0,
        "lqip_written": 0,
        "tags_updated": 0,
        "tags_skipped": 0,
    }

    def process_tag(m):
        tag = m.group(0)
        src_m = SRC_RE.search(tag)
        style_m = STYLE_RE.search(tag)
        if not src_m or not style_m:
            stats["tags_skipped"] += 1
            return tag  # no base64 LQIP or no src -> leave completely untouched

        src = src_m.group(1)
        b64 = style_m.group(1)

        parts = src.strip("/").split("/")
        if len(parts) < 3 or parts[0] != "gallery":
            stats["tags_skipped"] += 1
            return tag

        dest = parts[1]
        filename = parts[-1]
        basename = os.path.splitext(filename)[0]

        key = (dest, basename)
        lqip_rel_url = f"/gallery/{dest}/lqip/{basename}.jpg"

        if key not in written_cache:
            lqip_dir = os.path.join(STATIC_ROOT, dest, "lqip")
            os.makedirs(lqip_dir, exist_ok=True)
            lqip_path = os.path.join(lqip_dir, f"{basename}.jpg")
            data = base64.b64decode(b64)
            with open(lqip_path, "wb") as out:
                out.write(data)
            written_cache[key] = lqip_rel_url
            stats["lqip_written"] += 1

        new_style = f'style="background-image: url({lqip_rel_url}); background-size: cover;"'
        new_tag = tag[: style_m.start()] + new_style + tag[style_m.end():]
        stats["tags_updated"] += 1
        return new_tag

    md_files = sorted(glob.glob(os.path.join(CONTENT_ROOT, "*", "index*.md")))
    stats["files_scanned"] = len(md_files)

    for md_path in md_files:
        with open(md_path, "r", encoding="utf-8") as f:
            text = f.read()

        new_text = IMG_RE.sub(process_tag, text)

        if new_text != text:
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(new_text)
            stats["files_changed"] += 1

    print(f"MD files scanned: {stats['files_scanned']}")
    print(f"MD files changed: {stats['files_changed']}")
    print(f"LQIP files written: {stats['lqip_written']}")
    print(f"<img> tags updated: {stats['tags_updated']}")
    print(f"<img> tags skipped (no base64 lqip): {stats['tags_skipped']}")


if __name__ == "__main__":
    main()
