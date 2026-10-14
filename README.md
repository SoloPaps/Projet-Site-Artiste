# Site angeliqueheduin.fr — guide de maintenance

## Arborescence

```
index.html            Page d'accueil (hero, portfolio, galerie, contact)
js/main.js            Logique de l'index + TABLEAU `works` (source de vérité de la galerie)
css/style.css         Styles de l'index
css/oeuvre.css        Styles partagés des fiches générées par tools/build_pages.py
css/oeuvre-legacy-nav.css
css/legacy/*.css      Les 6 fiches d'origine : même CSS qu'avant, plus dans le HTML
js/oeuvre.js          Scripts partagés des fiches (navbar, menu mobile)
js/contact-prefill.js Fiches œuvres : pré-remplit le formulaire de contact de l'accueil
                      (nom de l'œuvre, via sessionStorage) — chargé par les fiches
oeuvres/*.html        Une fiche par œuvre (15)
images/               <nom>.jpg (œuvre intégrale) + <nom>+decors.jpg (mise en scène)
sitemap.xml, robots.txt, .htaccess, .nojekyll
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

## Déploiement

Le site public est publié par GitHub Actions (`.github/workflows/static.yml`) sur
`https://solopaps.github.io/Projet-Site-Artiste/`. Le workflow lance `tools/check_site.py`,
puis n'envoie que les fichiers du site (pas `tools/`, `docs/`, `.cursor/`, ni les notes).

Le 29 septembre 2026, le build Jekyll de GitHub Pages (`pages-build-deployment`) a échoué
trois fois : `Document_suivre.md` est un document Word, et Jekyll a refusé ses octets
(« invalid characters for the used encoding UTF-8 »). Le fichier s'appelle maintenant
`Document_suivre.docx`. `.nojekyll` empêche Jekyll de se relancer si la source Pages
repassait sur la branche.

`angeliqueheduin.fr` n'a **aucun enregistrement DNS** (NXDOMAIN, vérifié le 14 octobre 2026).
GitHub Pages n'a pas de domaine personnalisé configuré (`cname` vide). Ne pas ajouter de
fichier `CNAME` tant que le domaine ne résout pas : GitHub redirigerait l'adresse
`github.io` vers un nom qui n'existe pas. Quand le nom sera enregistré, les enregistrements
à créer chez le bureau d'enregistrement sont les quatre adresses A de GitHub Pages
(`185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`) et, pour
`www`, un CNAME vers `solopaps.github.io`. Ensuite seulement, déclarer le domaine dans
les réglages Pages.

## Points d'attention

- Les pages `mentions-legales.html`, `cgv.html` et `politique-confidentialite.html`
  sont dans le dépôt et liées depuis le pied de page.
- La boutique et le panier ont été retirés : plus aucun lien vers `boutique.html`.
  Les favoris de la galerie utilisent encore `localStorage` (clé `ah-favoris`), ce n'est pas un panier.
- Formulaire : `js/main.js` envoie vers `https://formspree.io/f/mjykyvno` (honeypot `_gotcha`).
  Ce n'est plus un identifiant de remplacement. Un essai réel, reçu dans la boîte Formspree,
  reste à faire par la propriétaire. Sans JavaScript, un message indique l'adresse e-mail.
- `frame-ancestors`, `X-Frame-Options` et `X-Content-Type-Options` dans une balise
  `<meta http-equiv>` sont **ignorés** par le navigateur. Le fichier `.htaccess` les envoie
  pour Apache (OVH). **GitHub Pages ne lit pas `.htaccess`** : sur l'adresse `github.io`,
  ces en-têtes ne sont pas posés. Les mentions légales indiquent encore OVH comme hébergeur.
- Les 6 fiches d'origine ne gardent plus leur CSS dans le HTML. Le rendu est le même :
  `css/oeuvre-legacy-nav.css` (partie commune) et `css/legacy/<slug>.css` (partie propre
  à la fiche). Les autres fiches utilisent `css/oeuvre.css` + `js/oeuvre.js`.
- Le portrait du bloc Portfolio est la photo `images/profil.jpg` (versions WebP à côté).
- Les fichiers de décor restent nommés `+decors`. `js/main.js` encode le `+` en `%2B`
  au moment de la requête. Les URL écrites dans le HTML doivent faire de même.
