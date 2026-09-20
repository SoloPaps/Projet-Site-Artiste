# À faire par la propriétaire (ni Cursor ni l'IA)

Rien de ceci ne doit être inventé pendant le développement. Cases à cocher avant publication.

## Bloquant avant publication
- [ ] Numéro SIRET/SIREN réel, à fournir pour les mentions légales.
- [ ] Identité réelle de l'hébergeur (nom, adresse, URL).
- [ ] Compte Formspree créé et identifiant de formulaire réel (remplace `VOTRE_ID_FORMSPREE`).
- [ ] Décision sur les témoignages : vrais (avec accord des personnes), anonymisés justifiables, ou à retirer.
- [ ] Liens de réseaux sociaux réels (Pinterest, Facebook, Instagram : lesquels et lesquels ne sont pas à jour).
- [ ] Vérification que les pages `oeuvres/*.html` existent sur le site en ligne.
- [ ] Déposer `.htaccess` à la racine du FTP OVH (voir `docs/SECURITE-OVH.md`) et vérifier les en-têtes HTTP. Sans ça, le clickjacking n’est pas bloqué.
- [ ] Activer le filtre anti-spam / les quotas dans le compte Formspree.

## Décisions à prendre
- [ ] Valider (ou changer) le flux de remplacement de « Acquérir l'œuvre » (section 7 du cahier des charges).
- [ ] Choisir l'alternative aux barres de compétence en pourcentage.
- [ ] Décider si l'adresse postale complète de l'atelier reste publique.
- [ ] Fournir un échantillon de sa voix pour `GUIDE-REDACTION.md`.
- [ ] Faire relire les pages légales (CGV, politique de confidentialité) par une personne qualifiée après suppression de la boutique.

## Avant de lancer Cursor
- [ ] Faire une copie complète du dossier du site (sauvegarde) : l'agent va supprimer des fichiers.
