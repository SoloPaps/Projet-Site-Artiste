# angeliqueheduin.fr — agent guide

Partial redesign of a static showcase site for a painter.

Visual freeze: `#gallery-section` and `#contact-section` (map included) stay as they are.
Elsewhere on the home page, layout may be simplified so it does not look like a generated template.
Do not invent facts. Palette and type (cream, terracotta, Cormorant / DM Sans) stay.

Scope otherwise: text content, shop already removed, broken features, security.

- Specification (source of truth): `docs/CAHIER-DES-CHARGES.md`
- Detailed rules: `.cursor/rules/` (project, legal data, security, content)
- Writing guide: `docs/GUIDE-REDACTION.md`
- What only the owner can provide: `docs/A-FAIRE-PAR-LA-PROPRIETAIRE.md`
- Prompts to paste per phase: `docs/PROMPTS.md`

## Non-negotiables
- Never invent legal or official data (SIRET, hosting, Formspree ID, payment links). Use visible placeholders and report them.
- Do not change the collection or contact design.
- Testimonials: removed from the page by owner decision (2026-09-20); do not put them back without a new decision.
- One task at a time unless the owner asks otherwise.
- Replies in French.

## Cursor Cloud specific instructions

No package install. From this repository root, `python3 tools/check_site.py` is the site check. It uses the Python standard library only.

On boot, the shared environment serves this site at `http://127.0.0.1:4173` (tmux session `site-artiste`) and the sibling osteopathy site `angelique-osteo` at `http://127.0.0.1:4174` (tmux session `site-osteo`). The osteopathy server maps an extensionless path such as `/tarifs-et-horaires` to the matching `.html` file.

`tools/render_test.py` needs Playwright and `tools/optimize_images.py` needs Pillow. Neither package is installed.

`Projet-Logiciel-de-performance` is a specification only. There is no application to start.
