#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Génère WebP (plein + 400/800), favicons, et enveloppe les <img> JPG/PNG
dans un <picture> avec srcset. Usage : python tools/optimize_images.py"""
import os, re, glob
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "images")
SKIP_STEMS = {"og-image"}  # OG/Twitter : rester en JPG
WEBP_Q = 80
FONT_OLD = "family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,300;1,400;1,500&family=DM+Sans:wght@200;300;400;500"
FONT_NEW = "family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400&family=DM+Sans:wght@300;400;500"
UNUSED = [
    "bateau2026+decors - Copie.jpg",
    "cheval2026 - Copie.jpg",
    "cheval2026+decors - Copie.jpg",
    "bateau2026 - Copie.jpg",
    "le-flamboyant-juin-2023.png",
]


def stem_of(name):
    return re.sub(r"\.(jpe?g|png)$", "", name, flags=re.I)


def resize_max(im, max_side):
    w, h = im.size
    if max(w, h) <= max_side:
        return im
    if w >= h:
        nw, nh = max_side, max(1, int(round(h * max_side / w)))
    else:
        nh, nw = max_side, max(1, int(round(w * max_side / h)))
    return im.resize((nw, nh), Image.Resampling.LANCZOS)


def save_webp(im, path):
    rgb = im.convert("RGB")
    rgb.save(path, "WEBP", quality=WEBP_Q, method=6)


def convert_jpgs():
    n = 0
    for name in sorted(os.listdir(IMG)):
        if not re.search(r"\.(jpe?g|png)$", name, re.I):
            continue
        if " - Copie" in name or " - copie" in name:
            continue
        st = stem_of(name)
        if st in SKIP_STEMS:
            continue
        src = os.path.join(IMG, name)
        with Image.open(src) as im:
            im.load()
            save_webp(im, os.path.join(IMG, st + ".webp"))
            save_webp(resize_max(im, 400), os.path.join(IMG, st + "-400.webp"))
            save_webp(resize_max(im, 800), os.path.join(IMG, st + "-800.webp"))
            n += 1
            print("webp:", name, im.size)
    return n


def paint_mark(size, square=True):
    terracotta = (201, 75, 34, 255)
    white = (255, 255, 255, 255)
    if square:
        im = Image.new("RGBA", (size, size), terracotta)
    else:
        im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        d0 = ImageDraw.Draw(im)
        d0.ellipse((0, 0, size - 1, size - 1), fill=terracotta)
    d = ImageDraw.Draw(im)

    def s(x, y):
        return x / 20.0 * size, y / 20.0 * size

    pts = [
        s(10, 3), s(7.5, 6), s(6.2, 8.5), s(6, 10.5),
        s(6.4, 12.6), s(7.8, 14.3), s(10, 15),
        s(12.2, 14.3), s(13.6, 12.6), s(14, 10.5),
        s(13.8, 8.5), s(12.5, 6),
    ]
    d.polygon(pts, fill=white)
    cx, cy = s(10, 10.5)
    r = 2.0 / 20.0 * size
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=terracotta)
    return im


def make_favicons():
    paint_mark(180, square=True).save(os.path.join(IMG, "apple-touch-icon.png"), "PNG")
    mark32 = paint_mark(32, square=True)
    mark32.save(os.path.join(IMG, "favicon-32.png"), "PNG")
    mark32.save(os.path.join(IMG, "favicon.ico"), format="ICO", sizes=[(16, 16), (32, 32)])
    print("favicon: ico / 32.png / apple-touch 180")


def delete_unused():
    for name in UNUSED:
        path = os.path.join(IMG, name)
        if os.path.isfile(path):
            os.remove(path)
            print("supprimé:", name)


def wrap_html(text):
    """Enveloppe les <img> JPG/PNG (hors <picture> déjà là) d'un source WebP 400/800."""
    out = []
    i = 0
    n = len(text)
    in_picture = 0
    while i < n:
        if text.startswith("<picture", i):
            in_picture += 1
            out.append("<picture")
            i += 8
            continue
        if text.startswith("</picture>", i):
            in_picture = max(0, in_picture - 1)
            out.append("</picture>")
            i += 10
            continue
        if in_picture == 0 and text.startswith("<img", i):
            end = text.find(">", i)
            if end < 0:
                out.append(text[i])
                i += 1
                continue
            tag = text[i : end + 1]
            src_m = re.search(
                r'''src=["']((?:\.\./)?images/[^"']+\.(?:jpe?g|png))["']''',
                tag,
                re.I,
            )
            if src_m:
                src = src_m.group(1)
                prefix, fname = src.rsplit("/", 1)
                st = stem_of(fname)
                recent = "".join(out[-400:])
                if "related-card-img" in recent:
                    sizes = "400px"
                elif "pf-portrait" in recent or "profil.jpg" in src:
                    sizes = "(max-width: 960px) 70vw, 400px"
                else:
                    sizes = "(max-width: 700px) 400px, 800px"
                out.append(
                    "<picture>"
                    f'<source type="image/webp" srcset="{prefix}/{st}-400.webp 400w, {prefix}/{st}-800.webp 800w" sizes="{sizes}">'
                    f"{tag}"
                    "</picture>"
                )
                i = end + 1
                continue
        out.append(text[i])
        i += 1
    return "".join(out)


def rewrite_html_files():
    paths = [os.path.join(ROOT, "index.html")]
    odir = os.path.join(ROOT, "oeuvres")
    for f in sorted(os.listdir(odir)):
        if f.endswith(".html"):
            paths.append(os.path.join(odir, f))
    for path in paths:
        raw = open(path, encoding="utf-8").read()
        new = wrap_html(raw)
        new = new.replace(FONT_OLD, FONT_NEW)
        if new != raw:
            open(path, "w", encoding="utf-8", newline="\n").write(new)
            print("html:", os.path.relpath(path, ROOT))


def rewrite_fonts_and_favicons():
    extra = [
        "404.html",
        "mentions-legales.html",
        "cgv.html",
        "politique-confidentialite.html",
        os.path.join("tools", "build_pages.py"),
    ]
    fav_files = (
        '<link rel="icon" href="images/favicon.ico" sizes="any">\n'
        '  <link rel="icon" type="image/png" sizes="32x32" href="images/favicon-32.png">\n'
        '  <link rel="apple-touch-icon" sizes="180x180" href="images/apple-touch-icon.png">'
    )
    icon_data = re.compile(
        r"""<link rel="icon" type="image/svg\+xml" href="data:image/svg\+xml,[^"]+">"""
    )
    apple_data = re.compile(
        r"""<link rel="apple-touch-icon"[^>]*href="data:image/svg\+xml,[^"]+">"""
    )
    for rel in extra:
        path = os.path.join(ROOT, rel)
        raw = open(path, encoding="utf-8").read()
        new = raw.replace(FONT_OLD, FONT_NEW)
        if rel.endswith(".html") and rel != "404.html":
            new2 = icon_data.sub(fav_files, new, count=1)
            new2 = apple_data.sub("", new2)
            new2 = re.sub(r"\n[ \t]*\n[ \t]*\n", "\n\n", new2)
            new = new2
        if new != raw:
            open(path, "w", encoding="utf-8", newline="\n").write(new)
            print("meta:", rel)


def profil_dims():
    p = os.path.join(IMG, "profil.jpg")
    with Image.open(p) as im:
        print("profil.jpg:", im.size)


if __name__ == "__main__":
    profil_dims()
    delete_unused()
    convert_jpgs()
    make_favicons()
    rewrite_html_files()
    rewrite_fonts_and_favicons()
    print("ok")
