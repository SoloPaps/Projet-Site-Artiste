#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Monogramme AH vitrail — Angélique Héduin.

Génère les SVG du dossier images/logo/ (mêmes dimensions que les fichiers
d'origine) et les aperçus PNG associés. Le nom est en Cormorant Garamond,
le sous-titre en DM Sans, tous deux convertis en tracés.

Polices variables attendues (OFL, non versionnées) :
  --cormorant  chemin vers CormorantGaramond[wght].ttf
  --dmsans     chemin vers DMSans[opsz,wght].ttf
"""
from __future__ import annotations

import argparse
import math
import os

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGO = os.path.join(ROOT, "images", "logo")
IMG = os.path.join(ROOT, "images")

# Géométrie du monogramme, dans le repère du logo principal (1000 × 820).
APEX = (248.0, 24.0)
LO = (52.0, 575.0)     # pied extérieur gauche du A
LI = (158.0, 575.0)    # pied intérieur gauche
RI = (338.0, 575.0)    # pied intérieur droit
RO = (444.0, 575.0)    # pied extérieur droit
CA = (248.0, 112.0)    # sommet du contre du A — laisse un grand jour

H_TOP = 112.0
H_BOT = 575.0
HL0, HL1 = 528.0, 626.0   # jambage gauche du H
HR0, HR1 = 818.0, 916.0   # jambage droit du H
RIBBON_Y = 332.0          # hauteur de la barre du H


def lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def x_at(p, q, y):
    return p[0] + (y - p[1]) / (q[1] - p[1]) * (q[0] - p[0])


def pt(edge_a, edge_b, y):
    return (x_at(edge_a, edge_b, y), y)


def mid(a, b):
    return ((a[0] + b[0]) * 0.5, (a[1] + b[1]) * 0.5)


def path_of(pts):
    x, y = pts[0]
    bits = [f"M{x:.2f} {y:.2f}"]
    for x, y in pts[1:]:
        bits.append(f"L{x:.2f} {y:.2f}")
    bits.append("Z")
    return " ".join(bits)


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rgb_hex(r, g, b):
    return "#{:02x}{:02x}{:02x}".format(
        max(0, min(255, int(r))),
        max(0, min(255, int(g))),
        max(0, min(255, int(b))),
    )


def mix(a, b, t):
    ra, ga, ba = hex_rgb(a)
    rb, gb, bb = hex_rgb(b)
    return rgb_hex(ra + (rb - ra) * t, ga + (gb - ga) * t, ba + (bb - ba) * t)


def lighten(h, t):
    return mix(h, "#ffffff", t)


def darken(h, t):
    return mix(h, "#07060d", t)


# Verre : violet profond, indigo, bleu ardoise, sarcelle.
PALETTE_VITRAIL = {
    "a": ["#3a1464", "#2a2378", "#54288e", "#1c3a68", "#6a3aaa", "#243e72", "#43186e", "#3d5688"],
    "hl": ["#2c415c", "#4a6584", "#1e3348", "#5d7b99", "#314860", "#24384c", "#6a88a6", "#3a5270"],
    "hr": ["#0c4e50", "#127e78", "#0a3a40", "#1aa396", "#0e6460", "#168f86", "#08383c", "#2eb0a6"],
    "ribbon": ["#4c1d7a", "#5e2e96", "#37145f", "#6d3eae", "#2a1054", "#7b52b8", "#431868", "#58308f"],
    "lead": "#b8893a",
    "lead_hi": "#f6e7b5",
    "ribbon_metal": "#e0bc62",
    "name": "#3a342e",
    "sub": "#7d756d",
    "bg": "#ffffff",
}

PALETTE_SOMBRE = {
    **PALETTE_VITRAIL,
    "lead": "#e7cb7e",
    "lead_hi": "#fbf3d4",
    "ribbon_metal": "#f0d48a",
    "name": "#f6f1e9",
    "sub": "#e4d8c8",
    "bg": "#1c1710",
}

# Variante « Ensoleillée » : terracotta, or, encre. Artefact seulement.
PALETTE_SOLEIL = {
    "a": ["#c94b22", "#a33b18", "#e07a42", "#8c3012", "#d4652e", "#b8915a", "#9a3c14", "#c9a56a"],
    "hl": ["#1c1710", "#3a2a22", "#6a4030", "#2a2018", "#8a5a32", "#241c16", "#4a3428", "#b8915a"],
    "hr": ["#c94b22", "#b8915a", "#a33c16", "#e8c98a", "#8f3414", "#d4a86a", "#c45a28", "#7a4a28"],
    "ribbon": ["#c94b22", "#a83812", "#d86a32", "#9a3414", "#e07a45", "#b8451c", "#c94b22", "#a33b18"],
    "lead": "#1c1710",
    "lead_hi": "#b8915a",
    "ribbon_metal": "#b8915a",
    "name": "#1c1710",
    "sub": "#8a5a32",
    "bg": "#f6f1e9",
}


def bands(out_a, out_b, in_a, in_b, y0, y1, n):
    """Bandes entre deux arêtes. Arêtes partagées exactes, pas de jour."""
    facets = []
    for i in range(n):
        ya = y0 + (y1 - y0) * i / n
        yb = y0 + (y1 - y0) * (i + 1) / n
        ym = (ya + yb) / 2
        o0, om, o1 = pt(out_a, out_b, ya), pt(out_a, out_b, ym), pt(out_a, out_b, yb)
        i0, im, i1 = pt(in_a, in_b, ya), pt(in_a, in_b, ym), pt(in_a, in_b, yb)
        m0, mm, m1 = mid(o0, i0), mid(om, im), mid(o1, i1)
        # Deux colonnes, coupe alternée pour des éclats irréguliers.
        if i % 2 == 0:
            facets.extend([[o0, om, m0], [om, mm, m0], [om, o1, mm], [o1, m1, mm]])
            facets.extend([[m0, mm, i0], [mm, im, i0], [mm, m1, im], [m1, i1, im]])
        else:
            facets.extend([[o0, mm, m0], [o0, om, mm], [om, o1, m1], [om, m1, mm]])
            facets.extend([[m0, im, i0], [m0, mm, im], [mm, i1, im], [mm, m1, i1]])
    return facets


def cap_facets():
    """Pointe pleine du A, au-dessus du jour du contre."""
    y1 = CA[1] * 0.55 + APEX[1] * 0.45
    y2 = CA[1]
    L1, R1 = pt(APEX, LO, y1), pt(APEX, RO, y1)
    L2, R2 = pt(APEX, LO, y2), pt(APEX, RO, y2)
    c = (mid(L1, R1)[0] - 10, mid(L1, R1)[1] - 4)
    return [
        [APEX, L1, c],
        [APEX, c, R1],
        [L1, L2, c],
        [L2, R2, c],
        [c, R2, R1],
    ]


def letter_facets():
    a_left = bands(APEX, LO, CA, LI, CA[1], LO[1], 3)
    a_right = bands(APEX, RO, CA, RI, CA[1], RO[1], 3)
    # Jambages du H : arêtes verticales.
    hl_out = ((HL0, H_TOP), (HL0, H_BOT))
    hl_in = ((HL1, H_TOP), (HL1, H_BOT))
    hr_in = ((HR0, H_TOP), (HR0, H_BOT))
    hr_out = ((HR1, H_TOP), (HR1, H_BOT))
    h_left = bands(hl_out[0], hl_out[1], hl_in[0], hl_in[1], H_TOP, H_BOT, 4)
    h_right = bands(hr_out[0], hr_out[1], hr_in[0], hr_in[1], H_TOP, H_BOT, 4)
    return {
        "a": cap_facets() + a_left + a_right,
        "hl": h_left,
        "hr": h_right,
    }


def cubic(p0, p1, p2, p3, t):
    u = 1 - t
    return (
        u**3 * p0[0] + 3 * u**2 * t * p1[0] + 3 * u * t**2 * p2[0] + t**3 * p3[0],
        u**3 * p0[1] + 3 * u**2 * t * p1[1] + 3 * u * t**2 * p2[1] + t**3 * p3[1],
    )


def ribbon_center(n=64):
    """S continu : part bas dans la jambe gauche, monte dans le contre, barre du H."""
    y0 = 476.0
    outer = x_at(APEX, LO, y0)
    inner = x_at(CA, LI, y0)
    p0 = ((outer + inner) / 2.0, y0)
    # Crête dans le jour du A, assez bas pour laisser le triangle du contre.
    shoulder = (APEX[0] + 16, 300.0)
    segs = [
        (p0, (p0[0] + 30, p0[1] - 78), (shoulder[0] - 55, shoulder[1] + 40), shoulder),
        (shoulder, (shoulder[0] + 78, shoulder[1] - 6), (455, RIBBON_Y - 2), (HL0 + 18, RIBBON_Y)),
        ((HL0 + 18, RIBBON_Y), (700, RIBBON_Y), (830, RIBBON_Y), (HR1, RIBBON_Y)),
    ]
    pts = []
    for i, (a, b, c, d) in enumerate(segs):
        steps = n
        start = 0 if i == 0 else 1
        for k in range(start, steps + 1):
            pts.append(cubic(a, b, c, d, k / steps))
    return pts


def offset_band(pts, dist):
    left, right = [], []
    n = len(pts)
    for i in range(n):
        if i == 0:
            dx, dy = pts[1][0] - pts[0][0], pts[1][1] - pts[0][1]
        elif i == n - 1:
            dx, dy = pts[-1][0] - pts[-2][0], pts[-1][1] - pts[-2][1]
        else:
            dx = pts[i + 1][0] - pts[i - 1][0]
            dy = pts[i + 1][1] - pts[i - 1][1]
        L = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / L, dx / L
        left.append((pts[i][0] + nx * dist, pts[i][1] + ny * dist))
        right.append((pts[i][0] - nx * dist, pts[i][1] - ny * dist))
    return left, right


def ribbon_geometry(half=27.0, inner=15.5):
    center = ribbon_center()
    outer_l, outer_r = offset_band(center, half)
    inner_l, inner_r = offset_band(center, inner)
    # Facettes du cœur violet : bandes le long du ruban.
    facets = []
    step = 8
    for i in range(0, len(center) - step, step):
        j = min(len(center) - 1, i + step)
        facets.append([inner_l[i], inner_l[j], inner_r[j], inner_r[i]])
    outer = outer_l + list(reversed(outer_r))
    return {"outer": outer, "facets": facets, "center": center}


def silhouette_paths():
    """Contours extérieurs du A et du H, pour le filet d'or."""
    a = path_of([APEX, LO, LI, CA, RI, RO])
    # Le contre et l'ouverture sous le ruban sont déjà le fond :
    # le tracé A-CA relie les deux jambes par le sommet du contre.
    # On veut le contour de chaque jambe + la pointe, pas un triangle plein.
    # Pointe + jambe gauche + jambe droite, en trois tracés qui se touchent.
    cap_l = pt(APEX, LO, CA[1])
    cap_r = pt(APEX, RO, CA[1])
    pointe = path_of([APEX, cap_l, CA, cap_r])
    jambe_g = path_of([cap_l, LO, LI, CA])
    jambe_d = path_of([cap_r, CA, RI, RO])
    h_g = path_of([(HL0, H_TOP), (HL0, H_BOT), (HL1, H_BOT), (HL1, H_TOP)])
    h_d = path_of([(HR0, H_TOP), (HR0, H_BOT), (HR1, H_BOT), (HR1, H_TOP)])
    return [pointe, jambe_g, jambe_d, h_g, h_d]


def gradient_for(poly, color, gid, angle):
    # Lumière venue du haut-gauche, avec une variation légère.
    x1, y1 = 8 + (angle % 5) * 4, 0
    x2, y2 = 92, 100 - (angle % 7) * 3
    hi = lighten(color, 0.55)
    mid = color
    lo = darken(color, 0.38)
    return (
        f'<linearGradient id="{gid}" x1="{x1}%" y1="{y1}%" x2="{x2}%" y2="{y2}%" gradientUnits="objectBoundingBox">'
        f'<stop offset="0" stop-color="{hi}"/>'
        f'<stop offset=".28" stop-color="{mid}"/>'
        f'<stop offset="1" stop-color="{lo}"/>'
        f'</linearGradient>'
    )


def gloss_triangle(poly):
    """Petit éclat clair sur le sommet le plus haut du tesson."""
    top = min(poly, key=lambda p: p[1] + p[0] * 0.15)
    cx = sum(p[0] for p in poly) / len(poly)
    cy = sum(p[1] for p in poly) / len(poly)
    a = top
    b = (top[0] + (cx - top[0]) * 0.55, top[1] + (cy - top[1]) * 0.55)
    # Deuxième point : voisin le plus proche du sommet.
    others = [p for p in poly if p != top]
    near = min(others, key=lambda p: (p[0] - top[0]) ** 2 + (p[1] - top[1]) ** 2)
    c = (top[0] + (near[0] - top[0]) * 0.42, top[1] + (near[1] - top[1]) * 0.42)
    return [a, b, c]


def emit_facets(facets, colors, id_prefix):
    defs, body = [], []
    for i, poly in enumerate(facets):
        gid = f"{id_prefix}{i}"
        color = colors[i % len(colors)]
        defs.append(gradient_for(poly, color, gid, (i * 47) % 100))
        d = path_of(poly)
        body.append(f'<path fill="url(#{gid})" d="{d}"/>')
        g = gloss_triangle(poly)
        body.append(f'<path fill="#fff" fill-opacity=".13" d="{path_of(g)}"/>')
    return defs, body


def emit_strokes(paths, palette, width, color=None):
    """Filet d'or fin. Un seul trait, pour que les plombs restent métalliques."""
    col = color or palette["lead"]
    out = []
    for d in paths:
        out.append(
            f'<path fill="none" stroke="{col}" stroke-width="{width:.2f}" '
            f'stroke-linejoin="round" stroke-linecap="round" d="{d}"/>'
        )
    return out


def monogram_defs_and_body(palette, id_prefix="v"):
    parts = letter_facets()
    rib = ribbon_geometry()
    defs, body = [], []
    masked = []
    for key in ("a", "hl", "hr"):
        d, b = emit_facets(parts[key], palette[key], f"{id_prefix}{key}")
        defs.extend(d)
        masked.extend(b)
        masked.extend(emit_strokes([path_of(p) for p in parts[key]], palette, 2.35))
    # Filet extérieur des lettres, interrompu là où passe le ruban.
    masked.extend(emit_strokes(silhouette_paths(), palette, 3.05))
    rib_d = path_of(rib["outer"])
    defs.append(
        f'<mask id="{id_prefix}cut" maskUnits="userSpaceOnUse" x="0" y="0" width="1000" height="820">'
        f'<rect width="1000" height="820" fill="#fff"/>'
        f'<path fill="#000" d="{rib_d}"/>'
        f'</mask>'
    )
    rd, rb = emit_facets(rib["facets"], palette["ribbon"], f"{id_prefix}rb")
    defs.extend(rd)
    ribbon_body = []
    defs.append(
        f'<linearGradient id="{id_prefix}gold" x1="0%" y1="0%" x2="100%" y2="30%">'
        f'<stop offset="0" stop-color="{palette["lead_hi"]}"/>'
        f'<stop offset=".45" stop-color="{palette["ribbon_metal"]}"/>'
        f'<stop offset="1" stop-color="{palette["lead"]}"/>'
        f'</linearGradient>'
    )
    ribbon_body.append(f'<path fill="url(#{id_prefix}gold)" d="{rib_d}"/>')
    # Cœur de verre posé sur l'or, un peu en retrait : liseré d'or visible.
    ribbon_body.extend(rb)
    ribbon_body.extend(emit_strokes([rib_d], palette, 2.15))
    # Filet clair au centre du ruban, pour le reflet métallique.
    center = rib["center"]
    c_bits = [f"M{center[0][0]:.2f} {center[0][1]:.2f}"]
    for x, y in center[1:]:
        c_bits.append(f"L{x:.2f} {y:.2f}")
    ribbon_body.append(
        f'<path fill="none" stroke="{palette["lead_hi"]}" stroke-width="1.35" '
        f'stroke-linecap="round" d="{" ".join(c_bits)}"/>'
    )
    group = (
        f'<g mask="url(#{id_prefix}cut)">{"".join(masked)}</g>'
        f'<g>{"".join(ribbon_body)}</g>'
    )
    return defs, group


def load_font(path, axes):
    font = TTFont(path)
    return instantiateVariableFont(font, axes, inplace=False)


def text_paths(font, text, size, tracking, x, y, fill):
    gs = font.getGlyphSet()
    cmap = font.getBestCmap()
    upem = font["head"].unitsPerEm
    scale = size / upem
    cursor = x
    out = []
    for ch in text:
        name = cmap[ord(ch)]
        glyph = gs[name]
        pen = SVGPathPen(gs)
        glyph.draw(pen)
        d = pen.getCommands()
        if d:
            out.append(
                f'<path fill="{fill}" transform="translate({cursor:.2f} {y:.2f}) '
                f'scale({scale:.6f} {-scale:.6f})" d="{d}"/>'
            )
        cursor += glyph.width * scale + tracking
    width = cursor - x - tracking
    return out, width


def measure_width(font, text, size, tracking):
    gs = font.getGlyphSet()
    cmap = font.getBestCmap()
    upem = font["head"].unitsPerEm
    scale = size / upem
    width = sum(gs[cmap[ord(ch)]].width * scale for ch in text)
    width += tracking * max(0, len(text) - 1)
    return width


def fit_tracking(font, text, size, target_width):
    gs = font.getGlyphSet()
    cmap = font.getBestCmap()
    upem = font["head"].unitsPerEm
    scale = size / upem
    width = sum(gs[cmap[ord(ch)]].width * scale for ch in text)
    gaps = max(1, len(text) - 1)
    return (target_width - width) / gaps


def wordmark(font_name, font_sub, palette, cx, name_y, sub_y, name_size, sub_size, name_width, sub_width):
    name = "ANGÉLIQUE HÉDUIN"
    sub = "ARTISTE PEINTRE"
    tr_n = max(fit_tracking(font_name, name, name_size, name_width), name_size * 0.04)
    tr_s = max(fit_tracking(font_sub, sub, sub_size, sub_width), sub_size * 0.22)
    w_n = measure_width(font_name, name, name_size, tr_n)
    w_s = measure_width(font_sub, sub, sub_size, tr_s)
    paths_n, _ = text_paths(font_name, name, name_size, tr_n, cx - w_n / 2, name_y, palette["name"])
    paths_s, _ = text_paths(font_sub, sub, sub_size, tr_s, cx - w_s / 2, sub_y, palette["sub"])
    return "".join(paths_n + paths_s)


def svg_doc(width, height, viewbox, title, desc, body_defs, body, extra_attrs=""):
    vb = f' viewBox="{viewbox}"' if viewbox else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}"{vb} '
        f'role="img" aria-labelledby="title desc"{extra_attrs}>'
        f'<title id="title">{title}</title>'
        f'<desc id="desc">{desc}</desc>'
        f'<defs>{"".join(body_defs)}</defs>'
        f'{body}'
        f'</svg>\n'
    )


def build_lockup(palette, fonts, prefix):
    """Logo principal 1000 × 820, sans viewBox (comme les fichiers d'origine)."""
    defs, mono = monogram_defs_and_body(palette, prefix)
    text = wordmark(
        fonts["name"], fonts["sub"], palette,
        cx=500, name_y=688, sub_y=758,
        name_size=58, sub_size=15,
        name_width=860, sub_width=560,
    )
    body = f'<rect width="1000" height="820" fill="{palette["bg"]}"/>{mono}{text}'
    return svg_doc(
        1000, 820, None,
        "Angélique Héduin — monogramme",
        "Monogramme AH en vitrail, or, avec le nom Angélique Héduin et le sous-titre Artiste peintre.",
        defs, body,
    )


def build_mark(palette, bg, ring, ring_gold, prefix):
    """Disque de navigation : width 272, height 272, viewBox 16 16 272 272."""
    defs, mono = monogram_defs_and_body(palette, prefix)
    # Le monogramme occupe environ x 86–910, y 28–568.
    bw, bh = HR1 - LO[0], H_BOT - APEX[1]
    cx, cy = (LO[0] + HR1) / 2, (APEX[1] + H_BOT) / 2
    # Tient dans le cercle de clip (r = 112 utiles).
    s = 214 / bw
    tx = 152 - cx * s
    ty = 158 - cy * s
    body = (
        f'<circle cx="152" cy="152" r="130" fill="{bg}"/>'
        f'<g clip-path="url(#{prefix}clip)">'
        f'<g transform="translate({tx:.2f} {ty:.2f}) scale({s:.5f})">{mono}</g>'
        f'</g>'
        f'<circle cx="152" cy="152" r="126" fill="none" stroke="{ring}" stroke-width="8"/>'
        f'<circle cx="152" cy="152" r="118" fill="none" stroke="{ring_gold}" stroke-width="2.5"/>'
    )
    defs = [f'<clipPath id="{prefix}clip"><circle cx="152" cy="152" r="120"/></clipPath>'] + defs
    return svg_doc(
        272, 272, "16 16 272 272",
        "Angélique Héduin",
        "Disque de navigation : monogramme AH en vitrail.",
        defs, body,
    )


def build_header(palette, fonts, prefix):
    """Bandeau 748 × 292, viewBox 6 6 748 292."""
    defs, mono = monogram_defs_and_body(palette, prefix)
    bw = HR1 - LO[0]
    bh = H_BOT - APEX[1]
    cx, cy = (LO[0] + HR1) / 2, (APEX[1] + H_BOT) / 2
    # Carré intérieur utile : environ 42–262.
    s = min(206 / bw, 206 / bh)
    tx = 152 - cx * s
    ty = 152 - cy * s
    text = wordmark(
        fonts["name"], fonts["sub"], palette,
        cx=530, name_y=140, sub_y=188,
        name_size=28, sub_size=10,
        name_width=380, sub_width=300,
    )
    body = (
        f'<rect x="6" y="6" width="748" height="292" fill="{palette["bg"]}"/>'
        f'<rect x="16" y="16" width="272" height="272" fill="none" stroke="{palette["name"]}" stroke-width="12"/>'
        f'<rect x="30" y="30" width="244" height="244" fill="none" stroke="{palette["lead"]}" stroke-width="2.5"/>'
        f'<g transform="translate({tx:.2f} {ty:.2f}) scale({s:.5f})">{mono}</g>'
        f'{text}'
    )
    return svg_doc(
        748, 292, "6 6 748 292",
        "Angélique Héduin",
        "Bandeau : monogramme AH en vitrail et nom.",
        defs, body,
    )


def build_medallion(palette, fonts, prefix):
    """Médaillon 1000 × 1000."""
    defs, mono = monogram_defs_and_body(palette, prefix)
    bw = HR1 - LO[0]
    bh = H_BOT - APEX[1]
    cx, cy = (LO[0] + HR1) / 2, (APEX[1] + H_BOT) / 2
    s = 560 / bw
    tx = 500 - cx * s
    ty = 400 - cy * s
    text = wordmark(
        fonts["name"], fonts["sub"], palette,
        cx=500, name_y=735, sub_y=788,
        name_size=40, sub_size=12,
        name_width=560, sub_width=380,
    )
    ink = "#1c1710" if palette["bg"] != "#1c1710" else "#f6f1e9"
    body = (
        f'<rect width="1000" height="1000" fill="{palette["bg"]}"/>'
        f'<circle cx="500" cy="500" r="468" fill="none" stroke="{ink}" stroke-width="26"/>'
        f'<circle cx="500" cy="500" r="446" fill="none" stroke="{palette["lead"]}" stroke-width="4"/>'
        f'<circle cx="500" cy="500" r="428" fill="none" stroke="{ink}" stroke-width="10"/>'
        f'<g transform="translate({tx:.2f} {ty:.2f}) scale({s:.5f})">{mono}</g>'
        f'{text}'
    )
    return svg_doc(
        1000, 1000, None,
        "Angélique Héduin",
        "Médaillon : monogramme AH en vitrail, nom et sous-titre.",
        defs, body,
    )


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    print("écrit", path)


def render_png(svg_path, png_path, w, h):
    import cairosvg
    cairosvg.svg2png(url=svg_path, write_to=png_path, output_width=w, output_height=h)
    print("png", png_path, w, h)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cormorant", required=True)
    ap.add_argument("--dmsans", required=True)
    ap.add_argument("--artifacts", default="")
    args = ap.parse_args()

    fonts = {
        "name": load_font(args.cormorant, {"wght": 500}),
        "sub": load_font(args.dmsans, {"opsz": 14, "wght": 300}),
    }

    centre = os.path.join(LOGO, "ah-monogramme-centre.svg")
    sombre = os.path.join(LOGO, "ah-monogramme-sombre.svg")
    mark = os.path.join(LOGO, "ah-mark.svg")
    mark_s = os.path.join(LOGO, "ah-mark-sombre.svg")
    header = os.path.join(LOGO, "ah-header.svg")
    med = os.path.join(LOGO, "ah-medaillon.svg")

    write(centre, build_lockup(PALETTE_VITRAIL, fonts, "c"))
    write(sombre, build_lockup(PALETTE_SOMBRE, fonts, "s"))
    write(mark, build_mark(PALETTE_VITRAIL, "#f6f1e9", "#1c1710", "#d4af5a", "m"))
    write(mark_s, build_mark(PALETTE_SOMBRE, "#1c1710", "#e6c97a", "#f6f1e9", "d"))
    write(header, build_header(PALETTE_VITRAIL, fonts, "h"))
    write(med, build_medallion(PALETTE_VITRAIL, fonts, "e"))

    render_png(centre, os.path.join(LOGO, "ah-monogramme-centre.png"), 1000, 820)
    render_png(sombre, os.path.join(LOGO, "ah-monogramme-sombre.png"), 1000, 820)
    render_png(header, os.path.join(LOGO, "ah-header.png"), 748, 292)
    render_png(med, os.path.join(LOGO, "ah-medaillon.png"), 1000, 1000)

    # Favicons aux tailles déjà en place : 180, 32, et ico 16+32.
    import io
    from PIL import Image
    import cairosvg
    big = cairosvg.svg2png(url=mark, output_width=512, output_height=512)
    im = Image.open(io.BytesIO(big)).convert("RGBA")
    im.resize((180, 180), Image.Resampling.LANCZOS).save(os.path.join(IMG, "apple-touch-icon.png"), "PNG")
    im32 = im.resize((32, 32), Image.Resampling.LANCZOS)
    im32.save(os.path.join(IMG, "favicon-32.png"), "PNG")
    im16 = im.resize((16, 16), Image.Resampling.LANCZOS)
    im32.save(os.path.join(IMG, "favicon.ico"), format="ICO", sizes=[(16, 16), (32, 32)], append_images=[im16])
    print("favicons")

    if args.artifacts:
        os.makedirs(args.artifacts, exist_ok=True)
        sun_svg = os.path.join(args.artifacts, "logo-ensoleillee.svg")
        write(sun_svg, build_lockup(PALETTE_SOLEIL, fonts, "z"))
        render_png(sun_svg, os.path.join(args.artifacts, "logo-ensoleillee.png"), 1000, 820)
        render_png(centre, os.path.join(args.artifacts, "logo-clair.png"), 1000, 820)
        render_png(sombre, os.path.join(args.artifacts, "logo-sombre.png"), 1000, 820)
        render_png(mark, os.path.join(args.artifacts, "logo-nav-mark.png"), 544, 544)


if __name__ == "__main__":
    main()
