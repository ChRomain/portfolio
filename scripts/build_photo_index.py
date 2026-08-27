#!/usr/bin/env python3
"""Construit data/photos.json : un enregistrement par photo, toutes langues confondues.

Ce fichier alimente content/photo/_content.gotmpl, qui génère une page par photo
(permalien partageable + indexable, ce que la lightbox seule ne permet pas).

La source de vérité reste content/gallery/*/index*.md : on en extrait les balises
<img> déjà générées par sync_photos.py plutôt que de relire la photothèque, qui
n'est pas versionnée. Le script est idempotent et réexécutable.
"""

import json
import pathlib
import re
import sys

CONTENT = pathlib.Path("content/gallery")
OUT = pathlib.Path("data/photos.json")
LANGS = {"en": "index.md", "fr": "index.fr.md", "es": "index.es.md"}

IMG_RE = re.compile(r"<img\s+([^>]*?)/?>", re.S)
ATTR_RE = re.compile(r'([a-zA-Z-]+)="([^"]*)"')


def attrs_of(tag_body):
    return dict(ATTR_RE.findall(tag_body))


def front_matter(text):
    """Retourne le frontmatter brut entre les deux marqueurs ---."""
    if not text.startswith("---"):
        return ""
    end = text.find("\n---", 3)
    return text[3:end] if end != -1 else ""


def scalar(fm, key):
    m = re.search(rf'^{key}:\s*"?(.*?)"?\s*$', fm, re.M)
    return m.group(1) if m else ""


def main():
    if not CONTENT.is_dir():
        sys.exit("content/gallery introuvable — lancer depuis la racine du projet")

    photos = {}
    order = []

    for gallery_dir in sorted(CONTENT.iterdir()):
        if not gallery_dir.is_dir():
            continue
        gallery = gallery_dir.name

        for lang, fname in LANGS.items():
            md = gallery_dir / fname
            if not md.exists():
                continue
            text = md.read_text(encoding="utf-8")
            fm = front_matter(text)
            gallery_title = scalar(fm, "title")
            country_code = scalar(fm, "country_code")

            for body in IMG_RE.findall(text):
                a = attrs_of(body)
                src = a.get("src", "")
                if not src.startswith("/gallery/") or not src.endswith(".webp"):
                    continue

                slug = src.rsplit("/", 1)[-1][: -len(".webp")]
                rec = photos.get(slug)
                if rec is None:
                    raw_tags = a.get("data-tags", "")
                    rec = {
                        "slug": slug,
                        "gallery": gallery,
                        "src": src,
                        "width": int(a.get("width") or 0),
                        "height": int(a.get("height") or 0),
                        "exif": a.get("title", ""),
                        "gps": a.get("data-gps", ""),
                        "date": a.get("data-date", ""),
                        "color": a.get("data-color", ""),
                        "tone": a.get("data-tone", ""),
                        "tags": [t for t in raw_tags.split(",") if t],
                        "country": country_code,
                        "alt": {},
                        "galleryTitle": {},
                    }
                    photos[slug] = rec
                    order.append(slug)

                rec["alt"][lang] = a.get("alt", "")
                rec["galleryTitle"][lang] = gallery_title

    records = [photos[s] for s in order]
    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w", encoding="utf-8") as f:
        json.dump({"photos": records}, f, ensure_ascii=False, indent=1)
        f.write("\n")

    missing_alt = sum(1 for r in records if len(r["alt"]) != 3)
    with_gps = sum(1 for r in records if r["gps"])
    with_date = sum(1 for r in records if r["date"])
    print(f"{len(records)} photos -> {OUT}")
    print(f"  galeries       : {len({r['gallery'] for r in records})}")
    print(f"  alt incomplets : {missing_alt}")
    print(f"  avec GPS       : {with_gps}")
    print(f"  avec date      : {with_date}")


if __name__ == "__main__":
    main()
