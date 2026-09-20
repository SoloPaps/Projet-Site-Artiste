# Prompts à coller par phase

Les règles permanentes sont dans `.cursor/rules/`. Si Cursor ne les charge pas seul, joins-les à la main au début de chaque nouveau chat avec `@` (au minimum `00-project` et `10-legal-and-data`). Un chat par phase.

Avant de commencer : copie le dossier du site en entier (sauvegarde).

---

## Phase 0 — Audit sans modification (mode Plan si disponible)

```
Lis @docs/CAHIER-DES-CHARGES.md, @AGENTS.md et les règles jointes.
Ne modifie aucun fichier. Confirme en quelques lignes le périmètre et les limites.
Puis fais l'inventaire du projet :
1. la liste des fichiers du site,
2. toutes les références à la boutique, au panier, à Stripe et à PayPal (fichier et ligne),
   y compris dans tools/*.py et AGENTS.md,
3. la Content Security Policy de chaque page, et si les en-têtes de sécurité sont des balises <meta> ou de vrais en-têtes,
4. les données structurées Schema.org qui mentionnent une offre ou l'achat,
5. les liens de réseaux sociaux par page,
6. pour chaque œuvre : le lien dans oeuvres/*.html (existence réelle, vérifiée dans le
   dossier du projet), l'entrée du sitemap, l'entrée dans les données JS, et le nom du
   fichier image correspondant — signale toute page manquante ou tout nom qui ne
   correspond pas entre ces quatre endroits,
7. tous les placeholders (VOTRE_, À COMPLÉTER, XXXX),
8. le contenu de tools/ (build_pages.py, check_site.py, render_test.py) : dis-moi si
   oeuvres/*.html (ou d'autres fichiers) sont générés par ces scripts plutôt qu'écrits
   à la main, et ce que ça change pour éditer le texte ou supprimer la boutique.
Attends ma validation.
```

## Phase 1 — Suppression de la boutique

```
Tâche 1 du cahier des charges : supprime la boutique et toutes ses références,
remplace le flux « Acquérir l'œuvre » par le défilement vers le formulaire de contact
(sujet « Acquisition d'une œuvre », nom de l'œuvre ajouté au message).
Si une référence à la boutique existe dans un fichier généré par tools/build_pages.py,
corrige la source/le template, pas la sortie générée, et dis-le moi.
Ensuite, liste tous les fichiers modifiés ou supprimés, tous les liens retirés,
et tout code de panier supprimé. Ne touche pas au design.
```

## Phase 2 — Formulaire de contact

```
Joins aussi @20-security.mdc à ce chat.
Tâche 2 : ajoute le champ honeypot et laisse le placeholder Formspree clairement
signalé (TODO-OWNER) à l'endroit exact. N'invente aucun identifiant.
Vérifie que la CSP autorise l'envoi vers Formspree, sans l'élargir davantage.
Dis-moi ce qu'il manque pour que le formulaire fonctionne réellement.
```

## Phase 3 — Textes (un bloc par chat ou par échange)

```
Tâche 3 : propose la réécriture du bloc <hero | bio Portrait | panneau 1 de « Ma démarche créative » | ...>
selon @docs/GUIDE-REDACTION.md. Si le bloc se trouve dans une page générée par
tools/build_pages.py, dis-le moi avant de proposer quoi que ce soit : on édite la
source, pas la page générée.
Montre le texte actuel, le texte proposé et ce qui a changé.
N'ajoute aucun fait. Attends ma validation avant de l'appliquer et de passer au bloc suivant.
```

## Phase 4 — Vérifications techniques et sécurité

```
Joins aussi @20-security.mdc à ce chat.
Tâche 4 : vérifie la CSP après suppression de la boutique, l'incohérence des liens
de réseaux sociaux (signale-la, demande-moi lesquels sont vrais), et l'existence
réelle de chaque page oeuvres/*.html face au sitemap et aux données JS (voir Phase 0
point 6). Signale aussi toute incohérence des pages légales
(sans les réécrire). Donne un rapport par gravité.
```

## Phase 5 — Contrôle final

```
Recherche dans TOUT le projet, y compris tools/*.py et AGENTS.md : boutique, stripe,
paypal, panier, cart, VOTRE_, À COMPLÉTER, TODO-OWNER, XXXX.
Explique chaque résultat restant.
Vérifie que tous les liens internes et les entrées du sitemap mènent à des pages
existantes, et que chaque slug d'œuvre est cohérent entre sitemap, données JS et
noms de fichiers images.
Si tools/check_site.py ou tools/render_test.py existent pour ça, lance-les (ou
dis-moi comment les lancer) plutôt que de tout revérifier à la main.
Puis rappelle-moi la liste des éléments que seule la propriétaire peut fournir.
```
