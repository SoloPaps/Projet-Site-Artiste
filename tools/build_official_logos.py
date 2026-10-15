#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Versions web des logos officiels (commit « Logos themes »).

Les JPG d'origine dans images/logo/ ne sont pas modifiés.
Le fond uni (crème / noir) est retiré : il ne fait pas partie du vitrail.
Le disque de navigation et les favicons ne gardent que la tête de cheval
et le cercle doré.
"""
import math
import os
from collections import deque

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGO = os.path.join(ROOT, "images", "logo")
IMG = os.path.join(ROOT, "images")

SRC_DARK = "ChatGPT Image 15 oct. 2026, 00_19_45.jpg"
SRC_LIGHT = "ChatGPT Image 15 oct. 2026, 00_19_55.jpg"

CREAM = (246, 241, 233)   # --cream / fond clair du site
INK = (28, 23, 16)        # --ink / fond sombre du site


def dist(c, bg):
    return math.sqrt((c[0] - bg[0]) ** 2 + (c[1] - bg[1]) ** 2 + (c[2] - bg[2]) ** 2)


def sample_bg(im):
    rgb = im.convert("RGB")
    w, h = rgb.size
    px = rgb.load()
    acc = [0, 0, 0]
    n = 0
    for y in list(range(0, 24)) + list(range(h - 24, h)):
        for x in list(range(0, 24)) + list(range(w - 24, w)):
            p = px[x, y]
            acc[0] += p[0]
            acc[1] += p[1]
            acc[2] += p[2]
            n += 1
    return tuple(int(round(c / n)) for c in acc)


def knockout(im, bg, tol=14, tol_soft=36, area_cut=2500):
    """Rend transparent le fond uni relié au bord, et les grandes plages
    intérieures de la même couleur (le champ autour du cheval). Les plombs
    et les éclats, plus petits, restent."""
    im = im.convert("RGBA")
    w, h = im.size
    px = im.load()
    near = bytearray(w * h)
    for y in range(h):
        for x in range(w):
            if dist(px[x, y][:3], bg) <= tol:
                near[y * w + x] = 1
    seen = bytearray(w * h)
    remove = bytearray(w * h)
    for y in range(h):
        for x in range(w):
            i = y * w + x
            if seen[i] or not near[i]:
                continue
            q = deque([(x, y)])
            seen[i] = 1
            cells = [(x, y)]
            touch = x == 0 or y == 0 or x == w - 1 or y == h - 1
            while q:
                cx, cy = q.popleft()
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = cx + dx, cy + dy
                    if nx < 0 or ny < 0 or nx >= w or ny >= h:
                        continue
                    j = ny * w + nx
                    if seen[j] or not near[j]:
                        continue
                    seen[j] = 1
                    q.append((nx, ny))
                    cells.append((nx, ny))
                    if nx == 0 or ny == 0 or nx == w - 1 or ny == h - 1:
                        touch = True
            if touch or len(cells) >= area_cut:
                for cx, cy in cells:
                    remove[cy * w + cx] = 1
    for y in range(h):
        for x in range(w):
            r, g, b, _a = px[x, y]
            if remove[y * w + x]:
                px[x, y] = (r, g, b, 0)
                continue
            d = dist((r, g, b), bg)
            if d >= tol_soft:
                continue
            neigh = False
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h and remove[ny * w + nx]:
                    neigh = True
                    break
            if not neigh:
                continue
            t = (d - tol) / float(tol_soft - tol)
            if t <= 0.04:
                px[x, y] = (r, g, b, 0)
                continue
            if t > 1:
                t = 1
            fr = int(round((r - bg[0] * (1 - t)) / t))
            fg = int(round((g - bg[1] * (1 - t)) / t))
            fb = int(round((b - bg[2] * (1 - t)) / t))
            px[x, y] = (
                max(0, min(255, fr)),
                max(0, min(255, fg)),
                max(0, min(255, fb)),
                int(round(t * 255)),
            )
    return im


def artwork_circle(src, bg, tol=18):
    """Cercle du médaillon : premier bloc de contenu, au-dessus du nom."""
    rgb = src.convert("RGB")
    w, h = rgb.size
    px = rgb.load()
    rows = []
    for y in range(h):
        n = 0
        for x in range(0, w, 2):
            if dist(px[x, y], bg) > tol:
                n += 1
        rows.append(n)
    runs = []
    on = False
    start = 0
    for y, n in enumerate(rows):
        if n > 4 and not on:
            start = y
            on = True
        elif n <= 4 and on:
            runs.append((start, y - 1))
            on = False
    if on:
        runs.append((start, len(rows) - 1))
    runs = [r for r in runs if r[1] - r[0] > 80]
    if not runs:
        raise SystemExit("cercle introuvable")
    y0, y1 = runs[0]
    minx, maxx, miny, maxy = w, 0, h, 0
    for y in range(y0, y1 + 1):
        for x in range(w):
            if dist(px[x, y], bg) > tol:
                if x < minx:
                    minx = x
                if x > maxx:
                    maxx = x
                if y < miny:
                    miny = y
                if y > maxy:
                    maxy = y
    cx = (minx + maxx) / 2.0
    cy = (miny + maxy) / 2.0
    r = max(maxx - minx, maxy - miny) / 2.0 + 2
    return cx, cy, r


def circle_crop(im, cx, cy, r, pad_ratio=0.0):
    side = int(math.ceil(r * 2))
    left = int(round(cx - r))
    top = int(round(cy - r))
    crop = im.crop((left, top, left + side, top + side)).convert("RGBA")
    w, h = crop.size
    mask = Image.new("L", (w, h), 0)
    mp = mask.load()
    cxm = (w - 1) / 2.0
    cym = (h - 1) / 2.0
    rad = (min(w, h) - 1) / 2.0
    for y in range(h):
        for x in range(w):
            d = math.hypot(x - cxm, y - cym)
            if d <= rad - 1.2:
                mp[x, y] = 255
            elif d >= rad + 0.3:
                mp[x, y] = 0
            else:
                mp[x, y] = int(max(0, min(255, (rad + 0.3 - d) / 1.5 * 255)))
    alpha = crop.getchannel("A")
    ap = alpha.load()
    for y in range(h):
        for x in range(w):
            ap[x, y] = ap[x, y] * mp[x, y] // 255
    crop.putalpha(alpha)
    if pad_ratio:
        pad = int(round(side * pad_ratio))
        framed = Image.new("RGBA", (side + pad * 2, side + pad * 2), (0, 0, 0, 0))
        framed.paste(crop, (pad, pad), crop)
        crop = framed
    return crop


def trim(im, margin=12):
    bbox = im.getbbox()
    if not bbox:
        return im
    x0, y0, x1, y1 = bbox
    x0 = max(0, x0 - margin)
    y0 = max(0, y0 - margin)
    x1 = min(im.size[0], x1 + margin)
    y1 = min(im.size[1], y1 + margin)
    return im.crop((x0, y0, x1, y1))


def save_png(im, path):
    im.save(path, "PNG", optimize=True)


def save_webp(im, path):
    im.save(path, "WEBP", quality=82, method=6)


def flatten(im, color, size):
    mark = im.resize((size, size), Image.Resampling.LANCZOS)
    bg = Image.new("RGBA", (size, size), color + (255,))
    return Image.alpha_composite(bg, mark).convert("RGB")


def save_ico(im32, path):
    im16 = im32.resize((16, 16), Image.Resampling.LANCZOS)
    im32.save(path, format="ICO", sizes=[(16, 16), (32, 32)], append_images=[im16])


def build_one(filename):
    src = Image.open(os.path.join(LOGO, filename))
    bg = sample_bg(src)
    cut = knockout(src, bg)
    full = trim(cut)
    long_side = max(full.size)
    if long_side > 1000:
        scale = 1000 / float(long_side)
        full = full.resize(
            (max(1, int(round(full.size[0] * scale))), max(1, int(round(full.size[1] * scale)))),
            Image.Resampling.LANCZOS,
        )
    cx, cy, r = artwork_circle(src, bg)
    disc = circle_crop(cut, cx, cy, r, pad_ratio=0.045)
    disc = disc.resize((256, 256), Image.Resampling.LANCZOS)
    icon = circle_crop(cut, cx, cy, r, pad_ratio=0.0)
    return full, disc, icon, bg


def main():
    light_full, light_disc, light_icon, light_bg = build_one(SRC_LIGHT)
    dark_full, dark_disc, dark_icon, dark_bg = build_one(SRC_DARK)
    print("fond mesuré clair", light_bg, "sombre", dark_bg)

    save_png(light_full, os.path.join(LOGO, "logo-clair.png"))
    save_webp(light_full, os.path.join(LOGO, "logo-clair.webp"))
    save_png(dark_full, os.path.join(LOGO, "logo-sombre.png"))
    save_webp(dark_full, os.path.join(LOGO, "logo-sombre.webp"))
    save_png(light_disc, os.path.join(LOGO, "marque-clair.png"))
    save_png(dark_disc, os.path.join(LOGO, "marque-sombre.png"))

    light32 = light_icon.resize((32, 32), Image.Resampling.LANCZOS)
    dark32 = dark_icon.resize((32, 32), Image.Resampling.LANCZOS)
    save_png(light32, os.path.join(IMG, "favicon-32.png"))
    save_png(dark32, os.path.join(IMG, "favicon-32-sombre.png"))
    save_ico(light32, os.path.join(IMG, "favicon.ico"))
    save_ico(dark32, os.path.join(IMG, "favicon-sombre.ico"))
    save_png(flatten(light_icon, CREAM, 180), os.path.join(IMG, "apple-touch-icon.png"))
    save_png(flatten(dark_icon, INK, 180), os.path.join(IMG, "apple-touch-icon-sombre.png"))

    for name, im in (
        ("logo-clair.png", light_full),
        ("logo-sombre.png", dark_full),
        ("marque-clair.png", light_disc),
        ("marque-sombre.png", dark_disc),
    ):
        path = os.path.join(LOGO, name)
        print(f"{name}: {im.size} {os.path.getsize(path)} octets")


if __name__ == "__main__":
    main()
