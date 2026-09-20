# En-têtes de sécurité sur OVH

Les balises `<meta http-equiv>` du HTML **ne suffisent pas**. `X-Frame-Options`, `frame-ancestors` et `X-Content-Type-Options` n’ont d’effet que s’ils arrivent en **vrais en-têtes HTTP**, via le fichier `.htaccess` à la racine du site.

## 1. Où coller le fichier

1. Dans FileZilla (ou le gestionnaire de fichiers OVH), ouvrir le dossier racine du site — celui qui contient déjà `index.html`.
2. Y déposer le fichier `.htaccess` (même nom, avec le point).
3. Ne pas le mettre dans un sous-dossier (`css/`, `oeuvres/`, etc.).

Sur Windows, le fichier peut être masqué. Dans FileZilla : *Serveur → Forcer l’affichage des fichiers cachés*.

## 2. Ne pas tout uploader

Le dossier de travail contient des fichiers **internes**. Ne pas les copier sur le FTP :

- `tools/`
- `docs/`
- `.cursor/`
- `AGENTS.md`
- tous les `*.py` et `*.md`

Le `.htaccess` refuse aussi ces chemins s’ils sont tout de même envoyés. Mieux vaut ne pas les envoyer.

À envoyer : `index.html`, les pages légales, `oeuvres/`, `css/`, `js/`, `images/`, `vendor/`, `sitemap.xml`, `robots.txt`, `.htaccess`.

## 3. Vérifier après mise en ligne

1. Ouvrir `https://angeliqueheduin.fr/` dans le navigateur.
2. Outils développeur (F12) → onglet **Réseau** → clic sur `index.html` (ou le document) → **En-têtes**.
3. Contrôler la présence de :
   - `content-security-policy`
   - `x-frame-options: DENY`
   - `x-content-type-options: nosniff`
   - `strict-transport-security`
4. Optionnel : [securityheaders.com](https://securityheaders.com) sur l’URL publique.

Si ces lignes sont absentes, Apache n’applique pas le `.htaccess` (fichier mal placé, ou module `headers` désactivé). Dans ce cas, le site s’affiche encore, mais **le clickjacking n’est pas bloqué**.

## 4. Formspree (spam)

L’identifiant du formulaire est public par conception. Dans le compte Formspree : activer le filtre anti-spam / les quotas. Le honeypot `_gotcha` du site réduit le spam, ce n’est pas une garantie.
