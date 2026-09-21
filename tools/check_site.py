#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Vérifie la cohérence du site. Usage : python3 check_site.py  (depuis la racine du site)
Sort avec le code 1 s'il y a au moins une erreur."""
import os, re, sys, json
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
errors, warns = [], []
def err(m):  errors.append(m)
def warn(m): warns.append(m)

VOID = {"meta","link","img","br","hr","input","source","area","base","col","embed","param","track","wbr"}
class Balance(HTMLParser):
    def __init__(s): super().__init__(); s.stack=[]; s.errs=[]; s.ids=[]; s.links=[]; s.imgs=[]; s.imgs_noalt=0
    def handle_starttag(s, t, a):
        d=dict(a)
        if "id" in d: s.ids.append(d["id"])
        if t=="a" and d.get("href"): s.links.append(d["href"])
        if t=="img":
            if d.get("src"): s.imgs.append(d["src"])
            if "alt" not in d: s.imgs_noalt += 1
        if t=="link" and d.get("href") and d.get("rel") in ("stylesheet","preload","icon"): s.links.append(d["href"])
        if t=="script" and d.get("src"): s.links.append(d["src"])
        if t in VOID: return
        s.stack.append((t, s.getpos()[0]))
    def handle_endtag(s, t):
        if t in VOID: return
        if s.stack and s.stack[-1][0]==t: s.stack.pop(); return
        names=[x for x,_ in s.stack]
        if t in names:
            while s.stack and s.stack[-1][0]!=t:
                x,l=s.stack.pop(); s.errs.append(f"<{x}> ligne {l} non fermée")
            s.stack.pop()
        else: s.errs.append(f"</{t}> orpheline ligne {s.getpos()[0]}")

def read(p): return open(os.path.join(ROOT,p),encoding="utf-8").read()
def exists(rel_from, href):
    if href.startswith(("http://","https://","mailto:","tel:","data:","#","//")): return True
    path=unquote(urlparse(href).path)
    if not path: return True
    return os.path.exists(os.path.normpath(os.path.join(ROOT, os.path.dirname(rel_from), path)))

pages = (
    ["index.html", "404.html", "mentions-legales.html", "cgv.html", "politique-confidentialite.html"]
    + sorted("oeuvres/"+f for f in os.listdir(os.path.join(ROOT,"oeuvres")) if f.endswith(".html"))
)

for p in pages:
    s = read(p)
    b = Balance(); b.feed(s)
    for e in b.errs: err(f"{p}: {e}")
    if b.stack: err(f"{p}: balises non fermées en fin de fichier: {[x for x,_ in b.stack][:5]}")
    if re.search(r'<[a-zA-Z][^>]*<!--', s): err(f"{p}: commentaire HTML coincé dans une balise")
    dup = {i for i in b.ids if b.ids.count(i)>1}
    if dup: err(f"{p}: id en double {sorted(dup)}")
    if b.imgs_noalt: err(f"{p}: {b.imgs_noalt} <img> sans attribut alt")
    for h in b.links:
        if not exists(p,h):
            err(f"{p}: ressource introuvable → {h}")
    for src in b.imgs:
        if not exists(p,src): err(f"{p}: image introuvable → {src}")
    # JSON-LD valide
    for j in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try: json.loads(j)
        except Exception as e: err(f"{p}: JSON-LD invalide ({e})")
    if 'Format libre' in s: err(f"{p}: contient encore « Format libre »")

# ── images : extension = format réel, et .jpg qui existent ──
# Format lu dans les octets de signature : portable, sans dépendre du binaire Unix `file`.
def image_format(path):
    with open(path, "rb") as fh: head = fh.read(12)
    if head.startswith(b"\xff\xd8\xff"):                    return "jpeg"
    if head.startswith(b"\x89PNG\r\n\x1a\n"):               return "png"
    if head[:4]==b"RIFF" and head[8:12]==b"WEBP":           return "webp"
    if head[:4]==b"\x00\x00\x01\x00":                       return "ico"
    if head.startswith((b"GIF87a",b"GIF89a")):              return "gif"
    if head[:2]==b"BM":                                     return "bmp"
    return "inconnu"

EXT_FORMAT = {"jpg":"jpeg","jpeg":"jpeg","png":"png","webp":"webp","gif":"gif","bmp":"bmp","ico":"ico"}
imgdir=os.path.join(ROOT,"images")
for f in sorted(os.listdir(imgdir)):
    real=image_format(os.path.join(imgdir,f))
    ext=f.rsplit(".",1)[-1].lower()
    if EXT_FORMAT.get(ext)!=real: err(f"images/{f}: extension .{ext} ≠ format réel ({real})")

# ── cohérence js/main.js ↔ fichiers ──
js = read("js/main.js")
m = re.search(r'const works = (\[.*?\n\]);', js, re.S)
works=[]
if not m: err("js/main.js: tableau works introuvable")
else:
    for blk in re.findall(r'\{\s*slug:.*?bg:\s*"[^"]*"\s*\}', m.group(1), re.S):
        g=lambda k: (re.search(k+r':\s*"([^"]*)"',blk) or [None,None])[1]
        works.append(dict(slug=g("slug"),img=g("img"),decor=g("imgDecor"),dims=g("dims"),
                          price=(re.search(r'price:\s*(null|"[^"]*")',blk) or [None,None])[1]))
    for i,w in enumerate(works):
        for k in("slug","img","decor"):
            if not w[k] or not os.path.exists(os.path.join(ROOT,w[k])): err(f"js/main.js works[{i}]: {k} introuvable → {w[k]}")
        if not re.search(r'\d+ × \d+ cm', w["dims"] or ""): err(f"js/main.js works[{i}]: dimensions invalides « {w['dims']} »")
    idx=read("index.html")
    if f'01 — {len(works):02d}' not in idx: err(f"index.html: compteur statique ≠ {len(works):02d}")
    # les 6 premières doivent garder leur ordre (indices de référence stables)
    order=["souvenirs-de-blonville","lane-de-b100-2025","raconte-moi-une-histoire","le-guetteur-silencieux-2024","klimt-juin-2023","le-flamboyant-juin-2023"]
    for i,o in enumerate(order):
        if not works[i]["slug"].endswith(o+".html"): err(f"js/main.js: l'ordre des œuvres existantes a changé à l'indice {i}")

# ── pages œuvres ↔ sitemap ↔ dimensions JSON-LD ↔ main.js ──
sm=read("sitemap.xml")
for w in works:
    if w["slug"] and ("https://angeliqueheduin.fr/"+w["slug"]) not in sm: err(f"sitemap.xml: {w['slug']} manquant")
    page=read(w["slug"]) if w["slug"] and os.path.exists(os.path.join(ROOT,w["slug"])) else ""
    dm=re.search(r'"width":\s*\{[^}]*"value":\s*(\d+)[^}]*\},\s*"height":\s*\{[^}]*"value":\s*(\d+)',page)
    if dm and w["dims"]:
        exp=f"{dm.group(1)} × {dm.group(2)} cm"
        if exp!=w["dims"]: err(f"{w['slug']}: dimensions page ({exp}) ≠ js/main.js ({w['dims']})")
    elif not dm: warn(f"{w['slug']}: pas de width/height dans le JSON-LD")

# ── sécurité ──
if not os.path.exists(os.path.join(ROOT, ".htaccess")):
    err(".htaccess manquant")
leaflet_js = os.path.join(ROOT, "vendor", "leaflet", "leaflet.min.js")
leaflet_css = os.path.join(ROOT, "vendor", "leaflet", "leaflet.min.css")
if not os.path.exists(leaflet_js): err("vendor/leaflet/leaflet.min.js manquant")
if not os.path.exists(leaflet_css): err("vendor/leaflet/leaflet.min.css manquant")
idx = read("index.html")
js_main = read("js/main.js")
if "cdnjs.cloudflare.com" in idx: err("index.html: cdnjs encore référencé")
if "vendor/leaflet/leaflet.min.js" not in idx and "vendor/leaflet/leaflet.min.js" not in js_main:
    err("Leaflet local non chargé (index.html ou js/main.js)")
if re.search(r"name=\"_gotcha\"[^>]*style=", idx): err("index.html: honeypot avec style inline")
if re.search(r"\.innerHTML\s*=", js_main): err("js/main.js: assignment innerHTML encore présent")

def script_src_of(csp):
    m = re.search(r"script-src\s+([^;]+)", csp)
    return (m.group(1) if m else "")

for p in pages:
    s = read(p)
    cm = re.search(r'http-equiv="Content-Security-Policy"[^>]*content="([^"]*)"', s, re.I)
    if not cm:
        err(f"{p}: CSP meta manquante")
        continue
    if "'unsafe-inline'" in script_src_of(cm.group(1)):
        err(f"{p}: script-src contient 'unsafe-inline'")
    if re.search(r"<script(?![^>]*\bsrc=)(?![^>]*type=\"application/ld\+json\")[^>]*>", s):
        err(f"{p}: script exécutable inline")
    if "onfocus=" in s or "onblur=" in s:
        err(f"{p}: gestionnaire d'événement inline")

print(f"\n{len(pages)} pages · {len(works)} œuvres · {len(os.listdir(imgdir))} images")
import collections
_miss=collections.Counter(re.sub(r'^.*→ (?:\.\./)?','',w) for w in warns if "→" in w)
for f,n in _miss.items(): print(f"  ⚠  {f} : référencé {n}× mais absent du dossier (à ajouter plus tard)")
for w in warns:
    if "→" not in w: print("  ! ", w)
for e in errors: print("  x ", e)
print("\n[OK] TOUT EST OK" if not errors else f"\n[ERR] {len(errors)} ERREUR(S)")
sys.exit(1 if errors else 0)
