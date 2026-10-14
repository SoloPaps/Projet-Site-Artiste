# À faire par la propriétaire (ni Cursor ni l'IA)

Rien de ceci ne doit être inventé pendant le développement. Cases à cocher avant publication.

## Bloquant avant publication
- [ ] Confirmer que le SIRET déjà écrit dans `mentions-legales.html` est le bon. Ne pas le remplacer par une valeur devinée.
- [ ] Dire quel est l'hébergeur réel. Les mentions légales indiquent OVH (nom, adresse et URL déjà rédigés). Le dépôt, lui, est publié par GitHub Pages, et `angeliqueheduin.fr` n'a aucun DNS (NXDOMAIN au 14 octobre 2026). Ne pas réécrire cette section sans cette confirmation.
- [ ] Enregistrer ou renouveler `angeliqueheduin.fr`, créer les enregistrements DNS indiqués dans le README, puis seulement déclarer le domaine dans GitHub Pages. Tant que le nom ne résout pas, ne pas ajouter de fichier `CNAME`.
- [ ] Envoyer un message test depuis le formulaire et vérifier qu'il arrive. L'identifiant Formspree déjà dans `js/main.js` est `mjykyvno`. Activer le filtre anti-spam et les quotas dans ce compte.
- [ ] Confirmer les réseaux réellement utilisés. Le site affiche Pinterest `https://fr.pinterest.com/angiehed/` et le Facebook « Angélique Héduin Ostéopathe ». Instagram n'est plus lié. Ne pas en choisir un autre à la place.
- [ ] Les 15 fiches `oeuvres/*.html` sont dans le dépôt. Vérifier qu'elles sont bien celles à montrer.
- [ ] Si le site reste aussi sur OVH : déposer `.htaccess` à la racine du FTP (voir `docs/SECURITE-OVH.md`) et contrôler les en-têtes HTTP. GitHub Pages ignore ce fichier : `frame-ancestors` et `X-Frame-Options` n'y protègent pas contre le détournement de clic.

## Décisions à prendre
- [x] Témoignages : retirés de la page d'accueil le 20 septembre 2026. Ne pas les remettre sans une nouvelle décision.
- [ ] Valider (ou changer) le flux de remplacement de « Acquérir l'œuvre » (section 7 du cahier des charges). Le clic mène au formulaire, sujet « Acquisition d'une œuvre ».
- [ ] Les barres de compétence en pourcentage ne sont plus sur la page. Confirmer que cette absence convient.
- [ ] Décider si l'adresse postale complète de l'atelier reste publique.
- [ ] Fournir un échantillon de sa voix pour `GUIDE-REDACTION.md`.
- [ ] Faire relire les pages légales (CGV, politique de confidentialité, mentions) par une personne qualifiée. Écart connu : l'hébergeur écrit (OVH) n'est pas l'hébergeur du déploiement actuel (GitHub Pages).

## Avant de lancer Cursor
- [ ] Faire une copie complète du dossier du site (sauvegarde) : l'agent va supprimer des fichiers.
