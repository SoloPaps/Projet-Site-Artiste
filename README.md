# Site angeliqueheduin.fr — guide de maintenance

## Arborescence

```
index.html            Page d'accueil (hero, portfolio, galerie, contact)
main.js               Logique de l'index + TABLEAU `works` (source de vérité de la galerie)
css/style.css         Styles de l'index
css/oeuvre.css        Styles partagés de TOUTES les fiches œuvres (nouvelles pages)
js/oeuvre.js          Scripts partagés des fiches (navbar, menu mobile)
js/contact-prefill.js Fiches œuvres : pré-remplit le formulaire de contact de l'accueil
                      (nom de l'œuvre, via sessionStorage) — chargé par les 13 fiches
oeuvres/*.html        Une fiche par œuvre (13)
images/               <nom>.jpg (œuvre intégrale) + <nom>+decors.jpg (mise en scène)
sitemap.xml, robots.txt
tools/                Scripts de vérification et de génération (voir plus bas)
```

## Les 13 œuvres (ordre du tableau `works` — NE PAS RÉORDONNER)

L'indice numérique de l'œuvre dans `works` sert de référence stable (miniatures,
puces de navigation, contrôle de cohérence de `tools/check_site.py`).
**Toujours ajouter à la fin.**

| Indice | Œuvre | Format | Prix |
|---|---|---|---|
| 0 | Souvenirs de Blonville | 50 × 50 | 300 € |
| 1 | L'Âne de Bessan | 60 × 80 | 470 € |
| 2 | Raconte-moi une histoire ! | 58 × 77 | 380 € |
| 3 | Le Guetteur Silencieux | 50 × 60 | 450 € |
| 4 | Klimt — Hommage au Baiser | 60 × 80 | 400 € |
| 5 | Le Flamboyant | 50 × 60 | 350 € |
| 6 | Le Cheval Soleil | 100 × 130 | à compléter |
| 7 | Féria | 100 × 130 | à compléter |
| 8 | Deux Voiles | 50 × 50 | à compléter |
| 9 | Le Cerf des Mille Signes | 50 × 50 | à compléter |
| 10 | Flamenco | 50 × 50 | à compléter |
| 11 | L'Esprit du Fauve | 70 × 50 | à compléter |
| 12 | Les Quatre Verres | 50 × 50 | à compléter |

## Renseigner un prix (œuvres 6 à 12)

Un prix doit être modifié à **4 endroits**, sinon le site se contredit :

1. `main.js` → dans `works[i]`, remplacer `price: null` par `price: "450"`.
2. `oeuvres/<page>.html` → remplacer le bloc `oeuvre-price on-request` par le bloc
   avec `itemprop="offers"` (copier celui de `oeuvres/klimt-juin-2023.html`) et
   remplacer le bouton « Demander le prix » par « Acquérir cette œuvre ».
3. `index.html` → dans le JSON-LD, ajouter un bloc `"offers"` à l'œuvre (voir Klimt).
4. `tools/build_pages.py` → ajouter le prix dans `PRICES` (cartes « Vous aimerez aussi »).

Tant que `price` vaut `null`, la galerie affiche « Prix sur demande » et le bouton
mène au formulaire de contact avec un message pré-rempli. Aucune donnée de prix
n'est envoyée à Google (pas de bloc `Offer`).

## Ajouter une nouvelle œuvre

1. Déposer `images/<nom>.jpg` et `images/<nom>+decors.jpg`.
2. Ajouter une entrée **à la fin** de `WORKS` dans `tools/build_pages.py`, puis :
   `python3 tools/build_pages.py`  → génère la fiche dans `oeuvres/`.
3. Ajouter l'objet correspondant **à la fin** du tableau `works` dans `main.js`
   (avec un `svgId` inédit `svg-13`, etc.).
4. Ajouter le bloc caché `<div id="svg-13">…</div>` dans `index.html`
   (copier `svg-12`), mettre à jour le compteur `01 — 13` → `01 — 14`.
5. Ajouter l'URL au `sitemap.xml` et le bloc `VisualArtwork` au JSON-LD de l'index.
6. Vérifier : `python3 tools/check_site.py`

## Vérifications automatiques

```
python3 tools/check_site.py      # HTML, liens, images, JSON-LD, cohérence main.js ↔ pages ↔ sitemap
python3 tools/render_test.py     # rendu réel Chromium à 360/768/1280/1920 px (nécessite playwright)
```

## Points d'attention connus (hors périmètre de cette mise à jour)

- `mentions-legales.html`, `cgv.html`, `politique-confidentialite.html`
  sont référencés par la navigation et le pied de page mais **absents de ce dossier**.
- La boutique et le panier ont été retirés : plus aucun lien vers `boutique.html`,
  plus de `localStorage`, plus de badge de panier.
- Formulaire de contact : `main.js` contient encore le placeholder
  `https://formspree.io/f/VOTRE_ID_FORMSPREE` → les messages ne partent pas tant
  qu'il n'est pas remplacé.
- `frame-ancestors` dans la CSP est **ignoré** en balise `<meta>` : pour protéger contre
  l'intégration en iframe, l'envoyer en en-tête HTTP côté hébergeur.
- Les 6 fiches d'origine gardent leur CSS incorporé. Les 7 nouvelles utilisent
  `css/oeuvre.css` + `js/oeuvre.js`. Migrer les 6 anciennes est possible, sans changement visuel.
- Le portrait de l'artiste (bloc Portfolio) est encore une illustration SVG de substitution.
- Images de décor : elles sont nommées `+decors` (avec un `+`). Sur certains hébergeurs le
  `+` dans une URL doit être encodé (`%2B`). À surveiller si une image de décor ne s'affiche pas.
