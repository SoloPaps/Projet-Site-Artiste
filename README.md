# Site angeliqueheduin.fr — guide de maintenance

## Arborescence

```
index.html            Page d'accueil (hero, portfolio, galerie, contact)
main.js               Logique de l'index + TABLEAU `works` (source de vérité de la galerie)
css/style.css         Styles de l'index
css/oeuvre.css        Styles partagés de TOUTES les fiches œuvres (nouvelles pages)
js/oeuvre.js          Scripts partagés des fiches (navbar, menu mobile)
js/contact-prefill.js Fiches œuvres : pré-remplit le formulaire de contact de l'accueil
                      (nom de l'œuvre, via sessionStorage) — chargé par les fiches
oeuvres/*.html        Une fiche par œuvre (15)
images/               <nom>.jpg (œuvre intégrale) + <nom>+decors.jpg (mise en scène)
sitemap.xml, robots.txt
tools/                Scripts de vérification et de génération (voir plus bas)
```

## Les 15 œuvres (ordre du tableau `works` — NE PAS RÉORDONNER)

L'indice numérique de l'œuvre dans `works` sert de référence stable (miniatures,
puces de navigation, contrôle de cohérence de `tools/check_site.py`).
**Toujours ajouter à la fin.**

| Indice | Œuvre | Format | Prix |
|---|---|---|---|
| 0 | Souvenirs de Blonville | 50 × 50 | 150 € |
| 1 | L'Âne de B100 | 60 × 80 | 470 € |
| 2 | Raconte-moi une histoire ! | 58 × 77 | 240 € |
| 3 | Le Guetteur Silencieux | 50 × 60 | 240 € |
| 4 | Le Baiser | 60 × 80 | 240 € |
| 5 | Le Flamboyant | 50 × 60 | 180 € |
| 6 | Cheval Céleste | 100 × 130 | 1350 € |
| 7 | La Féria | 100 × 130 | 1500 € |
| 8 | Les Voiliers | 50 × 50 | 150 € |
| 9 | Le Cerf des Mille Signes | 50 × 50 | 180 € |
| 10 | Danseuse de flamenco | 50 × 50 | 230 € |
| 11 | La force du rugby | 70 × 50 | 240 € |
| 12 | À table | 50 × 50 | 180 € |
| 13 | Le Rosé de Bessan | 50 × 50 | 230 € |
| 14 | La barque catalane | 50 × 50 | 170 € |

## Renseigner un prix

Toutes les œuvres ont un prix. Pour en changer un, le modifier aux **4 endroits** suivants, sinon le site se contredit :

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
   (avec un `svgId` inédit `svg-15`, etc.).
4. Mettre à jour le compteur de la galerie (`01 — 15` → `01 — 16`).
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
