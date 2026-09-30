#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Génère les 7 nouvelles fiches œuvres à partir d'un gabarit unique.
Source de vérité des données : la liste WORKS ci-dessous."""
import html, json, os, re

SITE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE = "https://angeliqueheduin.fr"

def esc(s):  # échappe pour attributs / texte
    return html.escape(s, quote=True)

HEX_COLOR = re.compile(r"^#[0-9A-Fa-f]{3,8}$")
TAG_CLASS_OK = {"tag-o", "tag-b", "tag-g", "tag-p", "tag-gold", "tag-sun", "tag-t", "tag-r", "tag-decor"}
RICH_SPLIT = re.compile(r"(</?(?:strong|em)>)", re.I)

def css_color(s, fallback="#c94b22"):
    return s if isinstance(s, str) and HEX_COLOR.match(s) else fallback

def rich(s):
    if not s:
        return ""
    out = []
    for part in RICH_SPLIT.split(s):
        low = part.lower()
        if low in ("<strong>", "</strong>", "<em>", "</em>"):
            out.append(low)
        else:
            out.append(esc(part))
    return "".join(out)

def tag_class(c):
    return c if c in TAG_CLASS_OK else ""

# ───────────────────────────── DONNÉES ─────────────────────────────
# num : numéro de fiche (suite logique après N°19 existant)
# art / art_bg : couleur d'accent de la page et fond de la colonne image
# rel : slugs des 3 œuvres suggérées en bas de page
WORKS = [
  dict(
    slug="le-cheval-soleil-2026", file="cheval2026", year="2026",
    title_html="Cheval <em>Céleste</em>", title="Cheval Céleste",
    dims=(100, 130), dorures=True,
    medium="Acrylique et feuilles d'or sur toile · 2026",
    technique="Acrylique + feuilles d'or",
    num="N° 20 · Collection 2026 · Cheval Totémique",
    cat_eyebrow="Cheval totémique",
    tags=[("Cheval Totémique","tag-o"),("Dorures","tag-gold"),("Soleil","tag-sun"),("Plumes","tag-t")],
    art="#c88010", art_bg="#f0b01018", badge="Grand format",
    short="Cheval de profil couronné d'un halo solaire, crinière de plumes turquoise et orangées, harnachement ornementé et feuilles d'or sur fond de rayons.",
    keywords="cheval, totem, soleil, halo, plumes, turquoise, orange, feuille d'or, symbole, grand format",
    genre=["Art figuratif","Animal totémique","Art chamanique","Feuille d'or"],
    alt="Cheval Céleste — peinture acrylique d'Angélique Héduin. Cheval noir et gris de profil, crinière de plumes turquoise et orange, harnais ornementé de motifs graphiques, halo solaire jaune et orange rayonnant avec touches de feuille d'or. 100×130 cm, 2026.",
    desc=("Un cheval de profil, noble et calme, se détache devant un <strong>halo solaire</strong> aux rayons orange, jaunes et turquoise. "
          "Sa crinière se change en <strong>plumes turquoise et ambrées</strong>, son encolure est parée de colliers, de perles et de motifs graphiques, "
          "et des <strong>feuilles d'or</strong> viennent capter la lumière dans les plumes et dans le halo. "
          "Un animal totémique qui porte la force tranquille, la dignité et l'élan vital. "
          "Un <strong>grand format</strong> pensé pour occuper un mur et lui donner sa lumière."),
    context="Comme dans toute ma série d'animaux totémiques, le cheval n'est pas un simple portrait : il est un guide. Le halo solaire l'installe dans une présence presque sacrée.",
    usage="Grand salon · Entrée · Bureau de direction · Hall d'accueil · Galerie",
    usage_title="Idéal pour",
    og_h=1440, rel=["taureau-feria-2026","le-flamboyant-juin-2023","lane-de-b100-2025"],
    rel_title="Autres animaux totémiques",
    ld_desc="Cheval de profil devant un halo solaire, crinière de plumes turquoise et orangées, harnachement ornementé et feuilles d'or. Acrylique et feuilles d'or sur toile, 100×130 cm, 2026.",
    img_size=(844, 1129), aw=480,
  ),
  dict(
    slug="taureau-feria-2026", file="taureau2026", year="2026",
    title_html="La <em>Féria</em>", title="La Féria",
    dims=(100, 130), dorures=True,
    medium="Acrylique et feuilles d'or sur toile · 2026",
    technique="Acrylique + feuilles d'or",
    num="N° 21 · Collection 2026 · Taureau Totémique",
    cat_eyebrow="Taureau totémique",
    tags=[("Taureau Totémique","tag-o"),("Dorures","tag-gold"),("Géométrique","tag-b"),("Fête","tag-r")],
    art="#c0281e", art_bg="#e0301c14", badge="Grand format",
    short="Taureau en facettes rouges, turquoise et brunes face à un torero à la cape rouge, sur fond de motifs géométriques. Le mot « Féria » est peint en bas de la toile.",
    keywords="taureau, torero, féria, cape rouge, géométrique, feuille d'or, fête, corrida, grand format",
    genre=["Art figuratif","Animal totémique","Vitrail moderne","Feuille d'or"],
    alt="La Féria — peinture acrylique d'Angélique Héduin. Taureau en facettes rouges, turquoise et brunes, mufle rehaussé de feuille d'or, face à un torero en habit de lumière jaune tenant une cape rouge ornée de motifs, fond de losanges et chevrons. Le mot Féria est peint en bas. 100×130 cm, 2026.",
    desc=("Le <strong>taureau</strong> et l'homme se font face dans un tourbillon de formes. "
          "L'animal est découpé en <strong>facettes rouges, turquoise et brunes</strong>, comme un vitrail, avec un mufle et une corne rehaussés de <strong>feuille d'or</strong>. "
          "Le torero, en habit jaune brodé, tient une <strong>cape rouge</strong> couverte de losanges et de chevrons. "
          "Derrière eux, des rayons, des motifs graphiques et des aplats de couleur vive scandent la scène. "
          "Le mot <strong>« Féria »</strong> signe le bas de la toile. Une œuvre de fête, de tension et de couleur, sur grand format."),
    context="Ici, le taureau est traité comme un totem : puissance, fierté, énergie brute. La géométrie colorée transforme la scène en une célébration plus qu'en un récit.",
    usage="Salle à manger · Espace de réception · Restaurant · Bar · Séjour spacieux",
    usage_title="Idéal pour",
    og_h=1440, rel=["le-cheval-soleil-2026","lane-de-b100-2025","le-flamboyant-juin-2023"],
    rel_title="Autres animaux totémiques",
    ld_desc="Taureau en facettes de vitrail face à un torero à la cape rouge, motifs géométriques et feuilles d'or. Acrylique et feuilles d'or sur toile, 100×130 cm, 2026.",
    img_size=(718, 973), aw=480,
  ),
  dict(
    slug="deux-voiles-2026", file="bateau2026", year="2026",
    title_html="Les <em>Voiliers</em>", title="Les Voiliers",
    dims=(50, 50), dorures=False,
    medium="Peinture acrylique sur toile · 2026",
    technique="Acrylique sur toile",
    num="N° 22 · Collection 2026 · Mer & Voiliers",
    cat_eyebrow="Mer & voiliers",
    tags=[("Marine","tag-b"),("Voiliers","tag-t"),("Mouvement","tag-o"),("Carré 50×50","tag-g")],
    art="#2a8ea0", art_bg="#40b0c018", badge="Disponible",
    short="Deux voiliers aux voiles ocre et violettes glissent sur une mer turquoise, au couteau, sous un ciel de nuages légers.",
    keywords="voilier, bateau, mer, turquoise, voile, marine, couteau, ocre, violet, mouvement",
    genre=["Art figuratif","Marine","Paysage"],
    alt="Les Voiliers — peinture acrylique d'Angélique Héduin. Deux voiliers aux voiles ocre, cuivre et violettes et aux coques brunes glissent sur une mer turquoise striée d'écume blanche, sous un ciel de nuages bleutés. 50×50 cm, 2026.",
    desc=("Deux voiliers filent côte à côte sur une <strong>mer turquoise</strong> travaillée en larges gestes. "
          "Leurs voiles, <strong>cuivre, ocre et violet profond</strong>, se répondent : l'une gonflée en arc, l'autre tendue comme une aile. "
          "L'écume blanche, posée en touches franches, dessine le sillage des coques. "
          "Le ciel, tout en nuages bleutés et lavande, laisse la lumière traverser la toile. "
          "Une peinture de <strong>mouvement et de respiration</strong>, à la fois libre et rythmée."),
    context=None,
    usage="Salon · Chambre · Bureau · Entrée · Salle de bain lumineuse",
    usage_title="Idéal pour",
    og_h=1200, rel=["souvenirs-de-blonville","le-guetteur-silencieux-2024","la-barque-catalane-2026"],
    rel_title="Autres œuvres de la collection",
    ld_desc="Deux voiliers aux voiles ocre et violettes sur une mer turquoise au couteau. Peinture acrylique sur toile, 50×50 cm, 2026.",
    img_size=(894, 898), aw=520,
  ),
  dict(
    slug="le-cerf-des-mille-signes-2025", file="cerf2025", year="2025",
    title_html="Le Cerf des <em>Mille Signes</em>", title="Le Cerf des Mille Signes",
    dims=(50, 50), dorures=False,
    medium="Peinture acrylique sur toile · 2025",
    technique="Acrylique sur toile",
    num="N° 23 · Collection 2025 · Cerf Totémique",
    cat_eyebrow="Cerf totémique",
    tags=[("Cerf Totémique","tag-o"),("Symboles","tag-p"),("Nature","tag-g"),("Plumes","tag-b")],
    art="#3a8a5a", art_bg="#40a0e018", badge="Disponible",
    short="Cerf de face aux bois ornés de feuilles et de baies, plumes suspendues, entouré de signes, de petits singes et de motifs sur fond turquoise.",
    keywords="cerf, totem, symboles, signes, feuilles, plumes, singes, nature, turquoise, chamanique",
    genre=["Art figuratif","Animal totémique","Art chamanique","Symbolisme"],
    alt="Le Cerf des Mille Signes — peinture acrylique d'Angélique Héduin. Cerf de face aux grands bois ornés de feuilles vertes et de baies rouges, plumes suspendues aux oreilles, entouré de signes graphiques, de petits singes et de formes colorées sur fond turquoise et terre. 50×50 cm, 2025.",
    desc=("Un <strong>cerf</strong> nous regarde en face, calme et attentif. "
          "Ses bois s'ornent de <strong>feuilles vertes et de baies rouges</strong>, et des <strong>plumes</strong> pendent de ses oreilles. "
          "Autour de lui, tout un monde de <strong>signes</strong> : spirales, triangles, chevrons, chiffres, lettres, et quelques petits singes suspendus. "
          "Le fond turquoise, les touches de jaune et de vert et la terre rouge en bas composent un paysage de symboles où chaque détail invite à s'attarder. "
          "Un totem de la forêt, à la fois doux et plein de mystères."),
    context="Cette toile aime les petits secrets : plus on la regarde, plus elle dévoile de signes. Le cerf en est le gardien.",
    usage="Salon · Chambre · Bureau · Chambre d'enfant · Cabinet",
    usage_title="Idéal pour",
    og_h=1200, rel=["le-guetteur-silencieux-2024","lane-de-b100-2025","le-flamboyant-juin-2023"],
    rel_title="Autres animaux totémiques",
    ld_desc="Cerf de face aux bois ornés de feuilles et de baies, entouré de signes, de plumes et de petits singes. Peinture acrylique sur toile, 50×50 cm, 2025.",
    img_size=(842, 867), aw=520,
  ),
  dict(
    slug="flamenco-2025", file="flamenco2025", year="2025",
    title_html="Danseuse de <em>flamenco</em>", title="Danseuse de flamenco",
    dims=(50, 50), dorures=False, dentelle=True,
    medium="Acrylique et dentelle sur toile · 2025",
    technique="Acrylique + dentelle",
    num="N° 24 · Collection 2025 · Scène du Sud",
    cat_eyebrow="Scène du Sud",
    tags=[("Flamenco","tag-r"),("Dentelle","tag-gold"),("Ruelle du Sud","tag-o"),("Âne","tag-b")],
    art="#c0392b", art_bg="#f0a02018", badge="Disponible",
    short="Un âne au harnais rouge et une danseuse en robe à volants rouge et blanche dans une ruelle ensoleillée, avec dentelle réelle marouflée dans la toile.",
    keywords="flamenco, danseuse, âne, robe rouge, dentelle, ruelle, sud, fleurs, tonneaux, volants",
    genre=["Art figuratif","Scène de rue","Technique mixte","Dentelle"],
    alt="Danseuse de flamenco — peinture acrylique d'Angélique Héduin. Un âne gris et blanc au harnais rouge et châle à franges au premier plan, une danseuse en robe rouge à volants de dentelle blanche dans une ruelle aux façades ocre, volets bleus, boutique de fleurs et tonneaux. 50×50 cm, 2025.",
    desc=("Une <strong>ruelle ensoleillée</strong> aux façades ocre, aux volets bleus et aux fleurs en pot. "
          "Au premier plan, un <strong>âne</strong> au regard doux, harnaché de rouge, porte un châle à franges dont la <strong>dentelle</strong> est réelle, appliquée dans la matière. "
          "Plus loin, une <strong>danseuse de flamenco</strong> lève le bras : robe rouge à volants, éventail de dentelle blanche, chevelure de feu. "
          "Tonneaux, boutique de fleurs, arcades : toute la chaleur du Sud est là. "
          "Une toile de <strong>fête, de rythme et de couleur</strong>, où la dentelle apporte un relief délicat."),
    context=None,
    usage="Salon · Salle à manger · Cuisine · Espace de réception · Chambre",
    usage_title="Idéal pour",
    og_h=1200, rel=["le-rose-de-bessan-2026","taureau-feria-2026","lane-de-b100-2025"],
    rel_title="Autres œuvres de la collection",
    ld_desc="Âne au harnais rouge et danseuse de flamenco dans une ruelle du Sud, avec dentelle marouflée. Acrylique et dentelle sur toile, 50×50 cm, 2025.",
    img_size=(857, 870), aw=520,
  ),
  dict(
    slug="lesprit-du-fauve-2026", file="rudby2026", year="2026",
    title_html="La force du <em>rugby</em>", title="La force du rugby",
    dims=(70, 50), dorures=False, landscape=True,
    medium="Peinture acrylique sur toile · 2026",
    technique="Acrylique sur toile",
    num="N° 25 · Collection 2026 · Sport & Totem",
    cat_eyebrow="Sport & totem",
    tags=[("Sport","tag-o"),("Fauve Totémique","tag-p"),("Mouvement","tag-b"),("Rugby","tag-r")],
    art="#c0392b", art_bg="#30a0e018", badge="Format paysage",
    short="Un joueur de rugby en course, ballon sous le bras, emporté par un tourbillon bleu où surgit un fauve en mosaïque colorée.",
    keywords="rugby, joueur, sport, fauve, tourbillon, mosaïque, vitrail, mouvement, bleu, rouge",
    genre=["Art figuratif","Sport","Animal totémique","Vitrail moderne"],
    alt="La force du rugby — peinture acrylique d'Angélique Héduin. Un joueur de rugby en maillot rouge portant le numéro 8 court ballon en main sur un terrain vert, dans un tourbillon de traits colorés sur fond bleu, avec une tête de fauve en mosaïque multicolore qui surgit à sa gauche. 70×50 cm, 2026.",
    desc=("Un <strong>joueur de rugby</strong> file ballon en main sur un terrain de gazon, poteaux en fond. "
          "Autour de lui, un <strong>tourbillon bleu</strong> strié de jaune, de rouge et d'orange donne à la toile toute sa vitesse. "
          "À sa gauche, un <strong>fauve en mosaïque</strong>, taillé comme un vitrail de pièces colorées, semble surgir de l'élan. "
          "L'homme et l'animal ne font qu'un : <strong>puissance, vitesse, instinct</strong>. "
          "Une peinture pour les amateurs de sport et d'énergie, au format paysage."),
    context="Le fauve représente ici l'esprit du joueur : la force intérieure qui se libère au moment de l'action.",
    usage="Salon · Bureau · Salle de sport · Espace de réception · Chambre d'ado",
    usage_title="Idéal pour",
    og_h=860, rel=["taureau-feria-2026","le-cheval-soleil-2026","deux-voiles-2026"],
    rel_title="Autres œuvres de la collection",
    ld_desc="Joueur de rugby en course, emporté par un tourbillon bleu où surgit un fauve en mosaïque. Peinture acrylique sur toile, 70×50 cm, 2026.",
    img_size=(848, 607), aw=560,
  ),
  dict(
    slug="les-quatre-verres-2026", file="vin2026", year="2026",
    title_html="À <em>table</em>", title="À table",
    dims=(50, 50), dorures=False,
    medium="Peinture acrylique sur toile · 2026",
    technique="Acrylique sur toile",
    num="N° 26 · Collection 2026 · Nature Morte",
    cat_eyebrow="Nature morte",
    tags=[("Nature Morte","tag-p"),("Vin & Vigne","tag-o"),("Couleur","tag-b"),("Convivialité","tag-g")],
    art="#7a3a8a", art_bg="#7a3a8a14", badge="Disponible",
    short="Quatre verres de vin rouge, une grappe de raisin et des feuilles de vigne, sur un fond partagé entre ocre chaud et bleus vifs, avec un motif de dentelle blanche.",
    keywords="vin, verres, raisin, vigne, nature morte, tonneaux, violet, bleu, convivialité, couleur",
    genre=["Art figuratif","Nature morte","Vitrail moderne"],
    alt="À table — peinture acrylique d'Angélique Héduin. Quatre verres de vin rouge alignés, grappe de raisin violet et feuilles de vigne vertes devant un fond partagé en deux : ocre orangé avec tonneaux à gauche, bleus vifs avec motif de dentelle blanche à droite. 50×50 cm, 2026.",
    desc=("Quatre <strong>verres de vin</strong> alignés captent les reflets du fond : le <strong>violet du vin</strong>, les bleus, les jaunes. "
          "Devant eux, une <strong>grappe de raisin</strong> aux grains luisants et des feuilles de vigne rappellent la terre d'où tout vient. "
          "Le fond est coupé en deux, <strong>ocre et orange chaud</strong> à gauche avec sa vigne et ses tonneaux, <strong>bleus francs</strong> à droite rehaussés d'un motif de dentelle blanche. "
          "Une toile de <strong>couleur, de partage et de convivialité</strong>."),
    context=None,
    usage="Cuisine · Salle à manger · Bar · Cave · Restaurant · Cadeau",
    usage_title="Idéal pour",
    og_h=1200, rel=["flamenco-2025","souvenirs-de-blonville","le-rose-de-bessan-2026"],
    rel_title="Autres œuvres de la collection",
    ld_desc="Quatre verres de vin rouge, grappe de raisin et feuilles de vigne sur un fond ocre et bleu. Peinture acrylique sur toile, 50×50 cm, 2026.",
    img_size=(822, 870), aw=520,
  ),
  dict(
    slug="le-rose-de-bessan-2026", file="le-rose-de-bessan", year="2026",
    title_html="Le Rosé de <em>Bessan</em>", title="Le Rosé de Bessan",
    dims=(50, 50), dorures=False,
    medium="Peinture acrylique sur toile · 2026",
    technique="Acrylique sur toile",
    num="N° 27 · Collection 2026 · Âne & Vigne",
    cat_eyebrow="Âne & vigne",
    tags=[("Âne Totémique","tag-o"),("Vin & Vigne","tag-b"),("Bessan","tag-g"),("Vitrail","tag-p")],
    art="#b04a62", art_bg="#c45a6a18", badge="Disponible",
    short="Un âne au museau baissé vers une bassine, le corps en facettes de vitrail, un tonneau qui verse le vin, l'étiquette « Rosé de Bessan », la vigne et le village derrière.",
    keywords="âne, rosé, Bessan, vigne, tonneau, vitrail, facettes, vin, village, Occitanie",
    genre=["Art figuratif","Animal totémique","Vitrail moderne"],
    alt="Le Rosé de Bessan — peinture acrylique d'Angélique Héduin. Un âne de profil, museau baissé vers une bassine, le corps découpé en facettes orange, bleu, rose, jaune et turquoise. Un tonneau cerclé verse le vin par un robinet, étiquette Rosé de Bessan. Vignes et village aux toits clairs derrière. 50×50 cm, 2026.",
    desc=("Un <strong>âne</strong> baisse le museau vers une bassine. "
          "Son corps est découpé en <strong>facettes</strong> orange, bleu, rose, jaune et turquoise, comme un vitrail. "
          "À droite, un <strong>tonneau</strong> cerclé laisse couler le vin par un robinet : l'étiquette porte <strong>Rosé de Bessan</strong>. "
          "Derrière, les rangs de vigne montent vers un village aux toits clairs. "
          "Une toile de <strong>terroir, de couleur et de soif</strong>."),
    context=None,
    usage="Cave · Salle à manger · Cuisine · Bar · Restaurant",
    usage_title="Idéal pour",
    og_h=1200, rel=["lane-de-b100-2025","les-quatre-verres-2026","flamenco-2025"],
    rel_title="Autres œuvres de la collection",
    ld_desc="Âne en facettes de vitrail penché vers une bassine, tonneau étiqueté Rosé de Bessan, vignes et village. Peinture acrylique sur toile, 50×50 cm, 2026.",
    img_size=(881, 865), aw=520,
  ),
  dict(
    slug="la-barque-catalane-2026", file="la-barque-catalane", year="2026",
    title_html="La barque <em>catalane</em>", title="La barque catalane",
    dims=(50, 50), dorures=False,
    medium="Peinture acrylique sur toile · 2026",
    technique="Acrylique sur toile",
    num="N° 28 · Collection 2026 · Mer",
    cat_eyebrow="Mer",
    tags=[("Marine","tag-b"),("Barque","tag-o"),("Plage","tag-g"),("Carré 50×50","tag-t")],
    art="#1f6fbf", art_bg="#2a8ec018", badge="Disponible",
    short="Une barque catalane à la voile jaune rayée de rouge, coque bleue et rouge, tirée sur le sable face à une mer bleu franc.",
    keywords="barque, catalane, voile, rouge, jaune, mer, plage, sable, marine, bateau",
    genre=["Art figuratif","Marine","Paysage"],
    alt="La barque catalane — peinture acrylique d'Angélique Héduin. Une barque à la voile jaune barrée de bandes rouges et à la coque bleue, jaune et rouge est tirée sur le sable. Mer bleu franc, écume, rochers et un petit bateau à l'horizon sous un ciel pâle. 50×50 cm, 2026.",
    desc=("Une <strong>barque catalane</strong> est tirée sur le sable, voile jaune barrée de <strong>bandes rouges</strong>. "
          "La coque est bleue, avec un liston jaune et un fond rouge. "
          "L'eau, <strong>bleu franc</strong>, vient mousser au bord de la plage. "
          "Plus loin, des rochers et un petit bateau sur la ligne d'horizon. "
          "Une toile de <strong>mer, de lumière et de couleur</strong>."),
    context=None,
    usage="Salon · Salle à manger · Entrée · Chambre · Bureau",
    usage_title="Idéal pour",
    og_h=1200, rel=["deux-voiles-2026","souvenirs-de-blonville","flamenco-2025"],
    rel_title="Autres œuvres de la collection",
    ld_desc="Barque catalane à la voile jaune et rouge, coque bleue et rouge, tirée sur le sable face à la mer. Peinture acrylique sur toile, 50×50 cm, 2026.",
    img_size=(1390, 1386), aw=520,
  ),
]

# Œuvres existantes pour la section « Vous aimerez aussi » (titre, image, page)
EXISTING = {
  "souvenirs-de-blonville":      ("Souvenirs de Blonville", "souvenirs-de-blonville.jpg", "souvenirs-de-blonville.html"),
  "lane-de-b100-2025":           ("L'Âne de B100", "lane-de-b100-2025.jpg", "lane-de-b100-2025.html"),
  "raconte-moi-une-histoire":    ("Raconte-moi une histoire !", "raconte-moi-une-histoire.jpg", "raconte-moi-une-histoire.html"),
  "le-guetteur-silencieux-2024": ("Le Guetteur Silencieux", "le-guetteur-silencieux-2024.jpg", "le-guetteur-silencieux-2024.html"),
  "le-flamboyant-juin-2023":     ("Le Flamboyant", "le-flamboyant-juin-2023.jpg", "le-flamboyant-juin-2023.html"),
  "klimt-juin-2023":             ("Le Baiser", "klimt-juin-2023.jpg", "klimt-juin-2023.html"),
}
for w in WORKS:
    EXISTING[w["slug"]] = (w["title"], w["file"] + ".jpg", w["slug"] + ".html")

# Prix affichés sur la fiche et dans « Vous aimerez aussi »
PRICES = {
  "souvenirs-de-blonville": "150 €",
  "lane-de-b100-2025": "470 €",
  "raconte-moi-une-histoire": "240 €",
  "le-guetteur-silencieux-2024": "240 €",
  "klimt-juin-2023": "240 €",
  "le-flamboyant-juin-2023": "180 €",
  "le-cheval-soleil-2026": "1350 €",
  "taureau-feria-2026": "1500 €",
  "deux-voiles-2026": "150 €",
  "le-cerf-des-mille-signes-2025": "180 €",
  "flamenco-2025": "230 €",
  "lesprit-du-fauve-2026": "240 €",
  "les-quatre-verres-2026": "180 €",
  "le-rose-de-bessan-2026": "230 €",
  "la-barque-catalane-2026": "170 €",
}

def dim_txt(w):
    a, b = w["dims"]; return f"{a} × {b} cm"

def render(w):
    slug, f = w["slug"], w["file"]
    url = f"{BASE}/oeuvres/{slug}.html"
    img = f"{BASE}/images/{f}.jpg"
    W, H = w["dims"]
    iw, ih = w["img_size"]
    # ratio réel de l'image -> width/height HTML (anti-CLS, exact)
    hw = 800
    hh = round(hw * ih / iw)
    title_full = w["title"]
    price_label = PRICES.get(slug)
    price_num = "".join(ch for ch in price_label if ch.isdigit()) if price_label else ""
    price_phrase = f"{price_num} €" if price_num else "Prix sur demande"
    # META
    page_title = f"{title_full} — Angélique Héduin · {w['year']}"
    meta_desc = (f"« {title_full} » — {w['short']} {dim_txt(w)}, {w['year']}. "
                 f"Œuvre d'Angélique Héduin, artiste peintre à Bessan (Hérault). {price_phrase}.")
    og_desc = f"{w['short']} {dim_txt(w)}, {w['year']}. Œuvre originale — {price_phrase}."
    tw_desc = f"{w['technique']} · {dim_txt(w)} · {w['year']} · {price_phrase}"
    # JSON-LD (Offer seulement si le prix est renseigné)
    ld = {
      "@context": "https://schema.org", "@type": "VisualArtwork",
      "@id": url + "#artwork", "name": title_full, "url": url,
      "image": img, "thumbnailUrl": img, "description": w["ld_desc"],
      "artMedium": w["medium"].split(" · ")[0],
      "artworkSurface": "Toile",
      "width":  {"@type":"QuantitativeValue","value":W,"unitCode":"CMT"},
      "height": {"@type":"QuantitativeValue","value":H,"unitCode":"CMT"},
      "dateCreated": w["year"], "artEdition": "Œuvre unique originale",
      "genre": w["genre"], "keywords": w["keywords"],
      "artist": {"@type":"Person","@id":BASE+"/#artist","name":"Angélique Héduin","url":BASE+"/"},
      "isPartOf": {"@type":"Collection","name":f"Collection {w['year']}"}
    }
    if price_num:
        ld["offers"] = {
          "@type": "Offer",
          "url": url,
          "priceCurrency": "EUR",
          "price": price_num,
          "priceValidUntil": "2027-01-01",
          "availability": "https://schema.org/InStock",
          "itemCondition": "https://schema.org/NewCondition",
          "seller": {"@id": BASE + "/#atelier"},
        }
    if price_num:
        price_html = (
            '<div class="oeuvre-price-row" itemprop="offers" itemscope itemtype="https://schema.org/Offer">\n'
            f'        <span class="oeuvre-price" itemprop="price" content="{esc(price_num)}">{esc(price_num)}</span>\n'
            '        <span class="oeuvre-price-cur" itemprop="priceCurrency" content="EUR">€</span>\n'
            '        <span class="oeuvre-price-tax">TTC</span>\n'
            '        <meta itemprop="availability" content="https://schema.org/InStock">\n'
            '      </div>'
        )
        acq_label = "Acquérir cette œuvre"
    else:
        price_html = (
            '<div class="oeuvre-price-row">\n'
            '        <span class="oeuvre-price on-request">Prix sur demande</span>\n'
            '      </div>'
        )
        acq_label = "Demander le prix"
    bc = {
      "@context":"https://schema.org","@type":"BreadcrumbList",
      "itemListElement":[
        {"@type":"ListItem","position":1,"name":"Accueil","item":BASE+"/"},
        {"@type":"ListItem","position":2,"name":"Collection","item":BASE+"/#gallery-section"},
        {"@type":"ListItem","position":3,"name":title_full}]
    }
    tags_html = "\n        ".join(
        f'<span class="oeuvre-tag {tag_class(c)}">{esc(t)}</span>' for t, c in w["tags"]
    )
    ctx_html = (f'\n      <div class="oeuvre-context">\n        {rich(w["context"])}\n      </div>' if w.get("context") else "")
    usage_html = (f'''
      <div class="oeuvre-usage">
        <span class="oeuvre-usage-title">{esc(w["usage_title"])}</span>
        <span class="oeuvre-usage-list">{esc(w["usage"])}</span>
      </div>''')
    # cartes « vous aimerez aussi » — 3 œuvres, différentes selon la fiche
    cards = []
    for r in w["rel"]:
        t, im, pg = EXISTING[r]
        cards.append(f'''      <a href="{pg}" class="related-card">
        <div class="related-card-img"><picture><source type="image/webp" srcset="../images/{im.rsplit('.',1)[0]}-400.webp 400w, ../images/{im.rsplit('.',1)[0]}-800.webp 800w" sizes="400px"><img src="../images/{im}" alt="{esc(t)}" width="400" height="400" loading="lazy" decoding="async"></picture></div>
        <span class="related-card-title">{esc(t)}</span><span class="related-card-price">{PRICES.get(r, "Prix sur demande")}</span>
      </a>''')
    cards_html = "\n".join(cards)

    return f'''<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <title>{esc(page_title)}</title>
  <meta name="description" content="{esc(meta_desc)}">
  <meta name="author" content="Angélique Héduin">
  <meta name="theme-color" content="#c94b22">
  <meta name="referrer" content="strict-origin-when-cross-origin">
  <meta name="robots" content="index, follow">
  <meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data: https://*.tile.openstreetmap.fr https://tile.openstreetmap.fr; connect-src 'self' https://formspree.io; form-action 'none'; base-uri 'self'; object-src 'none'; frame-src 'none'; frame-ancestors 'none'; upgrade-insecure-requests">
  <meta http-equiv="X-Frame-Options" content="DENY">
  <meta http-equiv="X-Content-Type-Options" content="nosniff">
  <meta http-equiv="Permissions-Policy" content="camera=(), microphone=(), geolocation=(), payment=(), browsing-topics=()">

  <link rel="canonical" href="{url}">

  <meta property="og:type"        content="article">
  <meta property="og:title"       content="{esc(page_title)}">
  <meta property="og:description" content="{esc(og_desc)}">
  <meta property="og:url"         content="{url}">
  <meta property="og:image"       content="{img}">
  <meta property="og:image:alt"   content="{esc(w['alt'])}">
  <meta property="og:locale"      content="fr_FR">
  <meta property="og:site_name"   content="Angélique Héduin — Peintre">

  <meta name="twitter:card"        content="summary_large_image">
  <meta name="twitter:title"       content="{esc(page_title)}">
  <meta name="twitter:description" content="{esc(tw_desc)}">
  <meta name="twitter:image"       content="{img}">

  <script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=2)}
  </script>

  <script type="application/ld+json">
{json.dumps(bc, ensure_ascii=False, indent=2)}
  </script>

  <link rel="preload" as="image" href="../images/{f}.jpg">
  <link rel="icon" href="../images/favicon.ico" sizes="any">
  <link rel="icon" type="image/png" sizes="32x32" href="../images/favicon-32.png">
  <link rel="apple-touch-icon" sizes="180x180" href="../images/apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">

  <!-- Styles partagés des fiches œuvres -->
  <link rel="stylesheet" href="../css/oeuvre.css">
  <!-- Accent propre à cette œuvre -->
  <style>
    :root {{ --art: {css_color(w['art'])}; --art-bg: {css_color(w['art_bg'], '#f0b01018')}; --art-w: {int(w['aw'])}px; }}
  </style>
</head>
<body>

  <a href="#main-content" class="skip-link">Aller au contenu principal</a>
  <nav id="navbar" aria-label="Navigation principale">
    <a href="../index.html" class="logo">
      <div class="logo-mark"><svg width="17" height="17" viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M10 3C10 3 6 7 6 10.5C6 12.985 7.791 15 10 15C12.209 15 14 12.985 14 10.5C14 7 10 3 10 3Z" fill="white"/><circle cx="10" cy="10.5" r="2" fill="#c94b22"/></svg></div>
      <div class="logo-text"><span class="logo-name">Angélique Héduin</span><span class="logo-sub">Peintre · Bessan, Occitanie</span></div>
    </a>
    <div class="nav-links">
      <a href="../index.html" class="nav-link">Accueil</a>
      <a href="../index.html#portfolio-section" class="nav-link">Portfolio</a>
      <a href="../index.html#gallery-section" class="nav-link">Collection</a>
      <a href="../index.html#contact-section" class="nav-link">Contact</a>
    </div>
    <button type="button" class="hamburger" id="hamburger" aria-label="Ouvrir le menu" aria-expanded="false" aria-controls="nav-drawer">
      <span></span><span></span><span></span>
    </button>
  </nav>
  <nav id="nav-drawer" class="nav-drawer" aria-hidden="true" aria-label="Menu mobile">
    <a href="../index.html" class="nav-drawer-link">Accueil</a>
    <a href="../index.html#portfolio-section" class="nav-drawer-link">Portfolio</a>
    <a href="../index.html#gallery-section" class="nav-drawer-link">Collection</a>
    <a href="../index.html#contact-section" class="nav-drawer-link">Contact</a>
  </nav>

  <main id="main-content">
  <article class="oeuvre-hero" itemscope itemtype="https://schema.org/VisualArtwork" aria-label="Fiche œuvre">
    <div class="oeuvre-image-col">
      <div class="oeuvre-img-wrap">
        <picture>
          <source type="image/webp" srcset="../images/{f}-400.webp 400w, ../images/{f}-800.webp 800w" sizes="(max-width: 768px) 100vw, 42vw">
          <img src="../images/{f}.jpg"
             alt="{esc(w['alt'])}"
             width="{hw}" height="{hh}" itemprop="image" loading="eager" decoding="async">
        </picture>
        <span class="oeuvre-img-badge">{esc(w['badge'])}</span>
      </div>
    </div>
    <div class="oeuvre-info-col">
      <nav class="oeuvre-breadcrumb" aria-label="Fil d'Ariane">
        <a href="../index.html">Accueil</a><span aria-hidden="true">›</span>
        <a href="../index.html#gallery-section">Collection</a><span aria-hidden="true">›</span>
        <span>{esc(title_full)}</span>
      </nav>
      <p class="oeuvre-num">{esc(w['num'])}</p>
      <h1 class="oeuvre-title" itemprop="name">{rich(w['title_html'])}</h1>
      <p class="oeuvre-medium" itemprop="artMedium">{esc(w['medium'])}</p>
      <div class="oeuvre-tags">
        {tags_html}
      </div>
      <div class="oeuvre-sep"></div>
      <p class="oeuvre-desc" itemprop="description">
        {rich(w['desc'])}
      </p>{ctx_html}{usage_html}
      <div class="oeuvre-specs">
        <div class="spec-item"><span class="spec-label">Format</span><span class="spec-val">{dim_txt(w)}</span></div>
        <div class="spec-item"><span class="spec-label">Technique</span><span class="spec-val">{esc(w['technique'])}</span></div>
        <div class="spec-item"><span class="spec-label">Date</span><span class="spec-val" itemprop="dateCreated">{esc(w['year'])}</span></div>
        <div class="spec-item"><span class="spec-label">Édition</span><span class="spec-val">Œuvre unique originale</span></div>
        <div class="spec-item"><span class="spec-label">Certificat</span><span class="spec-val">Certificat d'authenticité inclus</span></div>
      </div>
      <div class="oeuvre-avail"><div class="avail-dot" aria-hidden="true"></div>Disponible</div>
      {price_html}
      <div class="oeuvre-btns">
        <a href="../index.html#contact-section" class="btn-acq">{acq_label}</a>
        <a href="../index.html#contact-section" class="btn-contact">Poser une question</a>
      </div>
      <p class="oeuvre-note">Emballage soigné · Certificat d'authenticité inclus<br>
        Commandes personnalisées disponibles — <a href="../index.html#contact-section" class="link-soft">contactez-moi</a></p>
    </div>
  </article>
  <section class="related-section" aria-label="Autres œuvres">
    <div class="related-head"><p class="related-eyebrow">Vous aimerez aussi</p><h2 class="related-title">Autres œuvres de la collection</h2></div>
    <div class="related-grid">
{cards_html}
    </div>
  </section>
  </main>
  <footer role="contentinfo">
    <span>© 2026 Angélique Héduin · Bessan, Occitanie</span>
    <a href="mailto:angeliqueheduin@gmail.com">angeliqueheduin@gmail.com</a>
    <a href="../mentions-legales.html">Mentions légales</a>
    <a href="../cgv.html">CGV</a>
    <a href="../politique-confidentialite.html">Confidentialité</a>
  </footer>
  <script src="../js/oeuvre.js" defer></script>
  <script src="../js/contact-prefill.js" defer></script>
</body>
</html>
'''

if __name__ == "__main__":
    for w in WORKS:
        path = os.path.join(SITE, "oeuvres", w["slug"] + ".html")
        open(path, "w", encoding="utf-8").write(render(w))
        print("écrit:", path)
