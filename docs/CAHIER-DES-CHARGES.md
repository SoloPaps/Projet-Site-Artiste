# Refonte partielle de angeliqueheduin.fr — Cahier des charges

Ce document est la **source unique de vérité** du chantier. Il est issu de l'analyse du site existant (index.html, boutique.html/js/css, cgv.html, mentions-legales.html/css/js, politique-confidentialite.html, sitemap.xml, robots.txt, main.js, style.css). Les règles Cursor (`.cursor/rules/`) en sont le résumé opérationnel.

Les sections marquées **« ajout proposé »** ne figuraient pas dans l'analyse d'origine : ce sont des points de vigilance ajoutés à la relecture, à valider par la propriétaire.

---

## 1. Résumé de l'analyse

Le site est techniquement bien construit sur plusieurs plans : en-têtes de sécurité déjà présents sur les 5 pages HTML (à vérifier, voir section 6), structure sémantique soignée, données structurées Schema.org détaillées, accessibilité globalement prise en compte.

L'analyse fait toutefois ressortir trois catégories de problèmes, à traiter différemment :

1. **Des éléments non fonctionnels** : le formulaire de contact et le système de paiement de la boutique ne fonctionnent pas (section 2).
2. **Un déficit de conformité légale** : des informations obligatoires manquent dans les mentions légales (section 3).
3. **Un style rédactionnel trop marqué « généré par IA »** dans les textes de présentation (section 4).

La première et la troisième catégorie peuvent être corrigées par Cursor. La seconde nécessite des informations réelles que **seule la propriétaire du site peut fournir** : aucune donnée légale ne doit être inventée en cours de développement.

## 2. Éléments non fonctionnels (priorité haute)

| # | Élément | Constat | Fichier |
|---|---|---|---|
| 1 | Formulaire de contact | Pointe vers `formspree.io/f/VOTRE_ID_FORMSPREE`, identifiant jamais renseigné : tout envoi échoue. | `main.js` |
| 2 | Paiement Stripe | Lien `buy.stripe.com/VOTRE_LIEN`, jamais renseigné. | `boutique.js` |
| 3 | Paiement PayPal | Lien `www.paypal.com/paypalme/VOTRE_COMPTE`, jamais renseigné. | `boutique.js` |
| 4 | Paiement par virement | IBAN factice codé en dur (`FR76 XXXX XXXX...`). | `boutique.js` |
| 5 | Pages détail des œuvres | Le sitemap et la galerie pointent vers `oeuvres/*.html`, absentes des fichiers fournis : à vérifier sur le site en ligne. | `sitemap.xml`, `main.js` |
| 6 | Réseaux sociaux incohérents | `index.html` : Pinterest et un Facebook « Angélique Héduin Ostéopathe » ; `boutique.html` : Instagram et un autre Facebook. Les deux jeux ne peuvent pas être corrects. | `index.html`, `boutique.html` |

La boutique n'a jamais eu de système de paiement opérationnel : sa suppression retire une interface non finalisée, pas une fonctionnalité réelle.

## 3. Conformité légale (à compléter par la propriétaire)

`mentions-legales.html` contient des champs obligatoires laissés en placeholder :

- **Numéro SIRET/SIREN : absent** (`[NUMÉRO SIRET / SIREN — à compléter]`). Obligation pour un site professionnel en France.
- **Identité de l'hébergeur (nom, adresse, URL) : absente.** Également obligatoire.
- TVA intracommunautaire : marquée non applicable (franchise en base, article 293 B du CGI). Semble correct, à confirmer.

Ces champs restent des emplacements clairement signalés jusqu'à ce que la propriétaire les remplisse. C'est une limite volontaire. Ce document n'est pas un avis juridique : à faire relire par une personne qualifiée.

## 4. Contenu rédactionnel à corriger

- Métaphores répétées et peu concrètes : « passeurs d'énergie », « force souveraine », « acte de soin », « énergie essentielle ».
- Emphase systématique en gras/italique qui dilue l'effet.
- **Barres de compétence en pourcentage** (« Huile sur toile — 92 % ») : format sans sens pour une pratique artistique. À reformuler ou retirer, après validation.
- **Témoignages potentiellement fabriqués** (« Un collectionneur, Hérault », « Un médecin, Bessan », tous à 5 étoiles, sans attribution vérifiable). Publier de faux avis est un risque au regard du droit de la consommation. S'ils sont réels mais anonymisés, il faut pouvoir le justifier ; sinon ils sont à retirer ou remplacer par de vrais retours avec accord des personnes. **Ne pas les supprimer sans décision de la propriétaire.**
- Bandeau défilant de mots-clés (« Animaux Totémiques · Vitrail Moderne · Art Occitanie... ») : à conserver seulement s'il sert visuellement la page.

**Objectif :** garder la voix et les informations réelles (parcours d'ostéopathe vers la peinture, ancrage en Occitanie, technique du vitrail fragmenté), avec des phrases plus sobres et concrètes. Voir `GUIDE-REDACTION.md`.

## 5. Périmètre de travail

| Demande | Tâche concrète |
|---|---|
| Garder le même design | Aucune modification de la structure visuelle, des couleurs, de la mise en page. |
| Enlever le style « IA » | Réécriture des textes de la section 4, un bloc à la fois. |
| Enlever la page boutique | Suppression de `boutique.html`, `boutique.css`, `boutique.js` ; retrait de tous les liens (nav, footer, drawer mobile, pages légales) ; entrée du sitemap ; remplacement du flux « Acquérir ». |
| Vérifier que tout fonctionne | Corriger ou signaler chaque point de la section 2 ; scénarios de la section 9. |
| Ajouter des éléments si pertinent | Propositions de la section 7, à valider. |
| Vérifier la sécurité | Section 6. |

## 6. Sécurité

Points positifs : en-têtes `Content-Security-Policy`, `X-Frame-Options`, `X-Content-Type-Options` et `Referrer-Policy` présents sur les 5 pages ; données injectées dans le DOM issues d'un tableau interne (`works`), pas d'une entrée utilisateur.

À vérifier ou renforcer :

- Formulaire de contact sans protection anti-spam : ajouter un champ honeypot.
- Après suppression de la boutique, retirer de la CSP les domaines Stripe/PayPal s'ils ne servaient qu'à elle.
- Vérifier qu'aucune clé ou jeton n'est codé en dur ailleurs.

**Ajouts proposés :**

- **Balises `<meta>` ou vrais en-têtes ?** Si les en-têtes sont des balises `<meta http-equiv>`, `X-Frame-Options`, `frame-ancestors` et `X-Content-Type-Options` n'ont aucun effet dans ce cas : seuls de vrais en-têtes HTTP posés par l'hébergeur protègent. À vérifier dans le code et selon l'hébergeur.
- **Formspree et CSP :** vérifier que la CSP autorise bien l'envoi vers Formspree, et utiliser le nom de champ honeypot que Formspree reconnaît (souvent `_gotcha`, à confirmer dans leur documentation).
- **Scripts externes (Leaflet) :** version figée et attribut `integrity` (SRI).
- **Préremplissage du formulaire :** valeur insérée via `value`/`textContent`, jamais `innerHTML`, surtout si le nom de l'œuvre passe par l'URL.

## 7. Que devient « Acquérir une œuvre » ?

Le bouton ajoute aujourd'hui l'œuvre à un panier (`localStorage`) sans paiement fonctionnel.

**Proposition (à valider) :** le clic fait défiler vers le formulaire de contact, sujet prérempli « Acquisition d'une œuvre » et nom de l'œuvre ajouté au message. Cohérent avec le fait que chaque œuvre est unique (`isUnique: true`). Alternatives possibles : simple lien `mailto`, ou autre approche.

Autres suggestions, optionnelles :

- Honeypot sur le formulaire (voir section 6).
- Compléter ou retirer les liens vers `oeuvres/*.html` selon leur existence réelle.
- Harmoniser les liens de réseaux sociaux (un seul jeu de liens réels).

**Ajouts proposés (conséquences de la suppression de la boutique) :**

- Retirer le code devenu mort : icône ou compteur de panier, styles et scripts du panier, clé `localStorage` du panier.
- Chercher les références à la boutique dans les données structurées Schema.org (offres, URL d'achat), les balises Open Graph/canonical, `robots.txt` et le sitemap.
- Vérifier la cohérence des pages légales : CGV, politique de confidentialité (mentions de Stripe, PayPal, panier ; mention de Formspree ; tuiles de carte Leaflet). Signaler, sans réécrire.

## 8. Ce qui reste à la propriétaire

Voir `A-FAIRE-PAR-LA-PROPRIETAIRE.md`.

## 9. Scénarios de test après le travail de Cursor

1. Envoyer un message test via le formulaire et vérifier sa réception réelle (une fois l'identifiant Formspree fourni).
2. Vérifier qu'aucun lien (nav, footer, drawer mobile) ne pointe encore vers `boutique.html`.
3. Cliquer sur « Acquérir une œuvre » pour chaque œuvre de la galerie et vérifier le nouveau flux.
4. Vérifier la carte Leaflet (mini et agrandie) sur mobile et desktop.
5. Vérifier le menu mobile (hamburger) sur toutes les pages restantes, y compris les pages légales.
6. Vérifier qu'aucune règle de CSP ne référence encore Stripe ou PayPal.
7. Relire à voix haute tous les textes modifiés.
8. **Ajout proposé :** rechercher dans tout le projet `boutique`, `stripe`, `paypal`, `panier`/`cart`, `VOTRE_`, `À COMPLÉTER`, `TODO-OWNER`, `XXXX` et expliquer chaque résultat restant.
9. **Ajout proposé :** contrôler que tous les liens internes et les entrées du sitemap mènent à des pages existantes.
