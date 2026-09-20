'use strict';

/* ══════════════════════════════
   HAMBURGER MENU (mobile)
══════════════════════════════ */
(function () {
  const btn    = document.getElementById('hamburger');
  const drawer = document.getElementById('nav-drawer');
  if (!btn || !drawer) return;

  function openDrawer() {
    btn.classList.add('open');
    btn.setAttribute('aria-expanded', 'true');
    drawer.classList.add('open');
    drawer.setAttribute('aria-hidden', 'false');
  }
  function closeDrawer() {
    btn.classList.remove('open');
    btn.setAttribute('aria-expanded', 'false');
    drawer.classList.remove('open');
    drawer.setAttribute('aria-hidden', 'true');
  }

  btn.addEventListener('click', () => {
    btn.classList.contains('open') ? closeDrawer() : openDrawer();
  });

  // Close on link click
  drawer.querySelectorAll('.nav-drawer-link, .nav-drawer-cta').forEach(link => {
    link.addEventListener('click', closeDrawer);
  });

  // Close on outside click
  document.addEventListener('click', e => {
    if (!btn.contains(e.target) && !drawer.contains(e.target)) closeDrawer();
  });

  // Close on scroll
  window.addEventListener('scroll', closeDrawer, { passive: true });

  // Sync active state in drawer
  const drawerLinks = Array.from(drawer.querySelectorAll('.nav-drawer-link[data-section]'));
  const sectionObserverDrawer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const id = entry.target.id;
        drawerLinks.forEach(link => {
          link.classList.toggle('active', link.dataset.section === id);
        });
      }
    });
  }, { rootMargin: '-40% 0px -55% 0px', threshold: 0 });

  ['hero','gallery-section','portfolio-section','contact-section'].forEach(id => {
    const el = document.getElementById(id);
    if (el) sectionObserverDrawer.observe(el);
  });
})();

/* ══════════════════════════════
   NAV — scroll + active au scroll
══════════════════════════════ */
const navbar = document.getElementById('navbar');

// Fond opaque au scroll
window.addEventListener('scroll', () => {
  if (navbar) navbar.classList.toggle('scrolled', window.scrollY > 40);
}, { passive: true });

// Active link selon la section visible
const navLinks = Array.from(document.querySelectorAll('.nav-link[data-section]'));

const sectionObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const id = entry.target.id;
      navLinks.forEach(link => {
        link.classList.toggle('active', link.dataset.section === id);
      });
    }
  });
}, {
  rootMargin: '-40% 0px -55% 0px',   // déclenche quand la section est au centre de l'écran
  threshold: 0
});

// Observer hero + gallery-section
['hero', 'gallery-section'].forEach(id => {
  const el = document.getElementById(id);
  if (el) sectionObserver.observe(el);
});

/* ══════════════════════════════
   DONNÉES ŒUVRES
══════════════════════════════ */
const works = [
  {
    slug:     "oeuvres/souvenirs-de-blonville.html",
    img:      "images/souvenirs-de-blonville.jpg",
    imgDecor: "images/souvenirs-de-blonville+decors.jpg",
    svgId:    "svg-0",
    imgAlt:   "Souvenirs de Blonville — peinture acrylique, jeune femme au ballon rouge sur les planches normandes",
    title:    "Souvenirs de <em>Blonville</em>",
    medium:   "Peinture acrylique sur toile · Juillet 2025",
    dims:     "50 × 50 cm",
    desc:     "Une jeune femme au ballon rouge s'avance vers la mer sur les planches normandes, entre cabines de plage aux toits bleus et vagues écumantes. Une toile solaire et poétique, chargée de la douce nostalgie des étés d'enfance — lumière éclatante, couleurs pures, émotion universelle.",
    price:    "300",
    tags:     [{ l: "Figuratif", c: "tag-b" }, { l: "Nostalgie", c: "tag-o" }, { l: "Mer", c: "tag-g" }],
    series:   "mer",
    bg:       "#e8d080"
  },
  {
    slug:     "oeuvres/lane-de-b100-2025.html",
    img:      "images/lane-de-b100-2025.jpg",
    imgDecor: "images/lane-de-b100-2025+decors.jpg",
    svgId:    "svg-1",
    imgAlt:   "L'Âne de Bessan 2025 — peinture acrylique, âne totémique aux motifs géométriques africains et berbères",
    title:    "L'Âne de <em>Bessan</em>",
    medium:   "Acrylique sur toile · 2025",
    dims:     "60 × 80 cm",
    desc:     "Figure totémique par excellence de l'Hérault, cet âne explose en motifs géométriques africains et berbères — losanges, chevrons, cercles concentriques en bleu, orange, brun et or. Un hymne vibrant à la terre occitane et au symbolisme chamanique, où l'animal gardien devient œuvre d'art totale.",
    price:    "470",
    tags:     [{ l: "Animal Totémique", c: "tag-o" }, { l: "Géométrique", c: "tag-b" }, { l: "Occitanie", c: "tag-g" }],
    series:   "totem",
    bg:       "#d4901a"
  },
  {
    slug:     "oeuvres/raconte-moi-une-histoire.html",
    img:      "images/raconte-moi-une-histoire.jpg",
    imgDecor: "images/raconte-moi-une-histoire+decors.jpg",
    svgId:    "svg-2",
    imgAlt:   "Raconte-moi une histoire ! — peinture acrylique, chat aux grands yeux bleus déconstruit en vitrail multicolore",
    title:    "Raconte-moi <em>une histoire !</em>",
    medium:   "Acrylique sur toile · Septembre 2023",
    dims:     "58 × 77 cm",
    desc:     "Un chat aux grands yeux bleus rêveurs, déconstruit en fragments de vitrail multicolore sur fond jaune soleil et rose fuchsia. Chaque morceau raconte une histoire différente — géométries vives, taches rondes, chaos joyeux. Une œuvre qui interpelle, surprend et ne se lasse pas de dévoiler de nouveaux détails.",
    price:    "380",
    tags:     [{ l: "Chat Sacré", c: "tag-p" }, { l: "Vitrail", c: "tag-b" }, { l: "Pop Art", c: "tag-o" }],
    series:   "totem",
    bg:       "#f0e020"
  },
  {
    slug:     "oeuvres/le-guetteur-silencieux-2024.html",
    img:      "images/le-guetteur-silencieux-2024.jpg",
    imgDecor: "images/le-guetteur-silencieux-2024+decors.jpg",
    svgId:    "svg-3",
    imgAlt:   "Le Guetteur Silencieux 2024 — peinture acrylique, chat en majesté sur fond de mandala orange brûlé",
    title:    "Le Guetteur <em>Silencieux</em>",
    medium:   "Peinture acrylique sur toile · 2024",
    dims:     "50 × 60 cm",
    desc:     "Un chat en majesté, profil altier sur fond de mandala blanc et orange brûlé — œil doré en amande, museau délicat, robe découpée en facettes de vitrail bleu, vert, mauve et or. L'animal totémique dans toute sa puissance silencieuse : gardien, guide, passeur d'énergie. Dorures et collage sur toile.",
    price:    "450",
    tags:     [{ l: "Chat Totémique", c: "tag-o" }, { l: "Mandala", c: "tag-p" }, { l: "Dorures", c: "tag-b" }],
    series:   "totem",
    bg:       "#e86820"
  },
  {
    slug:     "oeuvres/klimt-juin-2023.html",
    img:      "images/klimt-juin-2023.jpg",
    imgDecor: "images/klimt-juin-2023+decors.jpg",
    svgId:    "svg-4",
    imgAlt:   "Klimt — Hommage au Baiser, peinture acrylique avec dorures, deux amants enlacés dans un flot d'or",
    title:    "<em>Klimt</em> — Hommage au Baiser",
    medium:   "Peinture acrylique · Juin 2023",
    dims:     "60 × 80 cm",
    desc:     "Réinterprétation personnelle du chef-d'œuvre de Gustav Klimt, peinte à l'acrylique avec une maîtrise saisissante des dorures, des motifs géométriques et des cercles caractéristiques. Deux amants enlacés dans un flot d'or et de fleurs — un exercice d'admiration qui révèle la profondeur technique et la sensibilité de l'artiste.",
    price:    "400",
    tags:     [{ l: "Hommage Klimt", c: "tag-o" }, { l: "Dorures", c: "tag-b" }, { l: "Figuratif", c: "tag-p" }],
    series:   "hommage",
    bg:       "#c8a820"
  },
  {
    slug:     "oeuvres/le-flamboyant-juin-2023.html",
    img:      "images/le-flamboyant-juin-2023.jpg",
    imgDecor: "images/le-flamboyant-juin-2023+decors.jpg",
    svgId:    "svg-5",
    imgAlt:   "Le Flamboyant — peinture acrylique, ara macaw en plein vol aux plumes rouges orangées et vertes sur fond jaune",
    title:    "Le <em>Flamboyant</em>",
    medium:   "Peinture acrylique · Juin 2023",
    dims:     "50 × 60 cm",
    desc:     "Un ara en plein vol, ailes déployées dans un embrasement de rouges, orangés et verts sur fond jaune-soleil. Les plumes s'élancent en fines stries fluides comme des flammes — puissance, liberté, lumière tropicale. Un totem ailé d'une énergie irrésistible, idéal pour illuminer un espace de vie ou professionnel.",
    price:    "350",
    tags:     [{ l: "Oiseau Totémique", c: "tag-o" }, { l: "Tropical", c: "tag-b" }, { l: "Énergie", c: "tag-g" }],
    series:   "totem",
    bg:       "#f0b010"
  },
  {
    slug:     "oeuvres/le-cheval-soleil-2026.html",
    img:      "images/cheval2026.jpg",
    imgDecor: "images/cheval2026+decors.jpg",
    svgId:    "svg-6",
    imgAlt:   "Le Cheval Soleil — peinture acrylique et feuilles d'or, cheval de profil devant un halo solaire, crinière de plumes turquoise et orangées",
    title:    "Le Cheval <em>Soleil</em>",
    medium:   "Acrylique et feuilles d'or sur toile · 2026",
    dims:     "100 × 130 cm",
    desc:     "Un cheval de profil, noble et calme, devant un halo solaire aux rayons orange, jaunes et turquoise. Sa crinière se change en plumes turquoise et ambrées, son encolure est parée de colliers et de motifs graphiques, et des feuilles d'or captent la lumière. Un totem de force tranquille, sur grand format.",
    price:    null,
    tags:     [{ l: "Cheval Totémique", c: "tag-o" }, { l: "Dorures", c: "tag-b" }, { l: "Soleil", c: "tag-g" }],
    series:   "totem",
    bg:       "#f0b010"
  },
  {
    slug:     "oeuvres/taureau-feria-2026.html",
    img:      "images/taureau2026.jpg",
    imgDecor: "images/taureau2026+decors.jpg",
    svgId:    "svg-7",
    imgAlt:   "Féria — peinture acrylique et feuilles d'or, taureau en facettes rouges et turquoise face à un torero à la cape rouge",
    title:    "<em>Féria</em>",
    medium:   "Acrylique et feuilles d'or sur toile · 2026",
    dims:     "100 × 130 cm",
    desc:     "Le taureau et l'homme se font face dans un tourbillon de formes. L'animal, découpé en facettes rouges, turquoise et brunes comme un vitrail, a le mufle et une corne rehaussés de feuille d'or. Le torero tient une cape rouge couverte de losanges et de chevrons. Une œuvre de fête, de tension et de couleur.",
    price:    null,
    tags:     [{ l: "Taureau Totémique", c: "tag-o" }, { l: "Dorures", c: "tag-b" }, { l: "Géométrique", c: "tag-p" }],
    series:   "totem",
    bg:       "#c0281e"
  },
  {
    slug:     "oeuvres/deux-voiles-2026.html",
    img:      "images/bateau2026.jpg",
    imgDecor: "images/bateau2026+decors.jpg",
    svgId:    "svg-8",
    imgAlt:   "Deux Voiles — peinture acrylique, deux voiliers aux voiles ocre et violettes sur une mer turquoise",
    title:    "Deux <em>Voiles</em>",
    medium:   "Peinture acrylique sur toile · 2026",
    dims:     "50 × 50 cm",
    desc:     "Deux voiliers filent côte à côte sur une mer turquoise travaillée en larges gestes. Leurs voiles cuivre, ocre et violet profond se répondent, l'une gonflée en arc, l'autre tendue comme une aile. L'écume blanche dessine le sillage des coques. Une peinture de mouvement et de respiration.",
    price:    null,
    tags:     [{ l: "Marine", c: "tag-b" }, { l: "Voiliers", c: "tag-g" }, { l: "Mouvement", c: "tag-o" }],
    series:   "mer",
    bg:       "#40b0c0"
  },
  {
    slug:     "oeuvres/le-cerf-des-mille-signes-2025.html",
    img:      "images/cerf2025.jpg",
    imgDecor: "images/cerf2025+decors.jpg",
    svgId:    "svg-9",
    imgAlt:   "Le Cerf des Mille Signes — peinture acrylique, cerf de face aux bois ornés de feuilles et de baies, entouré de signes et de petits singes",
    title:    "Le Cerf des <em>Mille Signes</em>",
    medium:   "Peinture acrylique sur toile · 2025",
    dims:     "50 × 50 cm",
    desc:     "Un cerf nous regarde en face, calme et attentif. Ses bois s'ornent de feuilles vertes et de baies rouges, des plumes pendent de ses oreilles. Autour de lui, un monde de signes : spirales, triangles, chevrons, lettres, et quelques petits singes suspendus. Un totem de la forêt, doux et plein de mystères.",
    price:    null,
    tags:     [{ l: "Cerf Totémique", c: "tag-o" }, { l: "Symboles", c: "tag-p" }, { l: "Nature", c: "tag-g" }],
    series:   "totem",
    bg:       "#40a0e0"
  },
  {
    slug:     "oeuvres/flamenco-2025.html",
    img:      "images/flamenco2025.jpg",
    imgDecor: "images/flamenco2025+decors.jpg",
    svgId:    "svg-10",
    imgAlt:   "Flamenco — peinture acrylique et dentelle, un âne au harnais rouge et une danseuse en robe à volants dans une ruelle ensoleillée",
    title:    "<em>Flamenco</em>",
    medium:   "Acrylique et dentelle sur toile · 2025",
    dims:     "50 × 50 cm",
    desc:     "Une ruelle ensoleillée aux façades ocre et aux volets bleus. Au premier plan, un âne au regard doux, harnaché de rouge, porte un châle dont la dentelle est appliquée dans la matière. Plus loin, une danseuse de flamenco lève le bras : robe rouge à volants, éventail de dentelle blanche. Une toile de fête, de rythme et de couleur.",
    price:    null,
    tags:     [{ l: "Flamenco", c: "tag-o" }, { l: "Dentelle", c: "tag-b" }, { l: "Âne", c: "tag-g" }],
    bg:       "#f0a020"
  },
  {
    slug:     "oeuvres/lesprit-du-fauve-2026.html",
    img:      "images/rudby2026.jpg",
    imgDecor: "images/rudby2026+decors.jpg",
    svgId:    "svg-11",
    imgAlt:   "L'Esprit du Fauve — peinture acrylique, joueur de rugby en course dans un tourbillon bleu où surgit un fauve en mosaïque colorée",
    title:    "L'Esprit du <em>Fauve</em>",
    medium:   "Peinture acrylique sur toile · 2026",
    dims:     "70 × 50 cm",
    desc:     "Un joueur de rugby file ballon en main sur un terrain de gazon. Autour de lui, un tourbillon bleu strié de jaune, de rouge et d'orange donne à la toile toute sa vitesse. À sa gauche, un fauve en mosaïque, taillé comme un vitrail de pièces colorées, semble surgir de l'élan. Puissance, vitesse, instinct.",
    price:    null,
    tags:     [{ l: "Sport", c: "tag-o" }, { l: "Fauve Totémique", c: "tag-p" }, { l: "Mouvement", c: "tag-b" }],
    series:   "totem",
    bg:       "#30a0e0"
  },
  {
    slug:     "oeuvres/les-quatre-verres-2026.html",
    img:      "images/vin2026.jpg",
    imgDecor: "images/vin2026+decors.jpg",
    svgId:    "svg-12",
    imgAlt:   "Les Quatre Verres — peinture acrylique, quatre verres de vin rouge, grappe de raisin et feuilles de vigne sur un fond ocre et bleu",
    title:    "Les Quatre <em>Verres</em>",
    medium:   "Peinture acrylique sur toile · 2026",
    dims:     "50 × 50 cm",
    desc:     "Quatre verres de vin alignés captent les reflets du fond : le violet du vin, les bleus, les jaunes. Devant eux, une grappe de raisin aux grains luisants et des feuilles de vigne. Le fond est coupé en deux, ocre chaud à gauche avec sa vigne et ses tonneaux, bleus francs à droite rehaussés d'un motif de dentelle blanche.",
    price:    null,
    tags:     [{ l: "Nature Morte", c: "tag-p" }, { l: "Vin & Vigne", c: "tag-o" }, { l: "Couleur", c: "tag-b" }],
    bg:       "#7a3a8a"
  }
];

/* ══════════════════════════════
   SUJET DU FORMULAIRE DE CONTACT
   Utilisé par la galerie et par l'arrivée depuis une fiche œuvre.
══════════════════════════════ */
function appliquerSujetContact(sujet) {
  const chips = Array.from(document.querySelectorAll('.subj-chip'));
  const chip  = chips.find(c => c.dataset.val === sujet);
  if (chip) { chip.click(); return; }
  // Aucune puce ne correspond : on renseigne le champ et on n'en laisse aucune
  // sélectionnée, pour ne pas afficher un libellé contredisant le sujet envoyé.
  chips.forEach(c => c.classList.remove('active'));
  const champ = document.getElementById('cf-subject');
  if (champ) champ.value = sujet;
}

/* ══════════════════════════════
   GALERIE
══════════════════════════════ */
(function () {

  let current       = 0;
  let transitioning = false;
  const liked       = new Set();

  const strip  = document.getElementById('strip');
  const awrap  = document.getElementById('awrap');
  const cdots  = document.getElementById('cdots');
  const pbar   = document.getElementById('pbar');
  const btnAcq = document.getElementById('btnacq');
  const btnFav = document.getElementById('btnfav');

  const TAG_CLASS = new Set(['tag-b', 'tag-o', 'tag-g', 'tag-p', 'tag-gold', 'tag-sun', 'tag-t', 'tag-r', 'tag-decor']);
  const IMG_SRC_OK = /^images\/[A-Za-z0-9._+-]+\.(jpe?g|png|webp)$/;
  const SLUG_OK = /^oeuvres\/[a-z0-9-]+\.html$/;

  function safeImgSrc(src) {
    return (typeof src === 'string' && IMG_SRC_OK.test(src)) ? src : '';
  }
  function safeSlug(slug) {
    return (typeof slug === 'string' && SLUG_OK.test(slug)) ? slug : '#gallery-section';
  }
  function fillEmTitle(el, html) {
    el.textContent = '';
    if (typeof html !== 'string') return;
    const re = /<em>([^<]*)<\/em>|([^<]+)/g;
    let m;
    while ((m = re.exec(html))) {
      if (m[1] !== undefined) {
        const em = document.createElement('em');
        em.textContent = m[1];
        el.appendChild(em);
      } else {
        el.appendChild(document.createTextNode(m[2]));
      }
    }
  }
  function appendArtworkImage(parent, src, alt, w, h) {
    const safe = safeImgSrc(src);
    if (!safe) return;
    const img = document.createElement('img');
    img.src = safe;
    img.alt = typeof alt === 'string' ? alt : '';
    if (w) img.width = w;
    if (h) img.height = h;
    parent.appendChild(img);
  }

  /* ── BUILD DOM ── */
  works.forEach((w, i) => {

    // Artwork canvas — image avec décor si disponible, sinon SVG original
    const a = document.createElement('div');
    a.className = 'artwork ' + (i === 0 ? 'in' : 'out');
    a.id = 'aw-' + i;
    if (w.imgDecor) {
      appendArtworkImage(a, w.imgDecor, w.imgAlt, 600, 600);
    } else {
      const svgSource = document.getElementById(w.svgId);
      if (svgSource) {
        Array.from(svgSource.childNodes).forEach(function (n) {
          a.appendChild(n.cloneNode(true));
        });
      } else {
        appendArtworkImage(a, w.img, w.imgAlt, 600, 600);
      }
    }
    awrap.appendChild(a);

    // Miniature strip — toujours l'image originale sans décor
    const th = document.createElement('div');
    th.className = 'thumb' + (i === 0 ? ' active' : '');
    appendArtworkImage(th, w.img, w.imgAlt, 32, 32);
    const thumbImg = th.querySelector('img');
    if (thumbImg) thumbImg.loading = 'lazy';
    th.addEventListener('click', () => go(i));
    strip.appendChild(th);

    // Dot
    const cd = document.createElement('div');
    cd.className = 'cdot' + (i === 0 ? ' active' : '');
    cdots.appendChild(cd);
  });

  const artEls   = Array.from(awrap.querySelectorAll('.artwork'));
  const thumbEls = Array.from(strip.querySelectorAll('.thumb'));
  const dotEls   = Array.from(cdots.querySelectorAll('.cdot'));

  let filterSeries = '';
  function visibleList() {
    return works.map(function (_, i) { return i; }).filter(function (i) {
      return !filterSeries || works[i].series === filterSeries;
    });
  }
  function applyFilter(series) {
    filterSeries = series || '';
    const list = visibleList();
    thumbEls.forEach(function (th, i) {
      th.classList.toggle('is-off', list.indexOf(i) === -1);
    });
    if (list.length && list.indexOf(current) === -1) {
      transitioning = false;
      go(list[0]);
    } else {
      updatePanel(current, false);
    }
  }

  const galFilters = document.getElementById('gal-filters');
  if (galFilters) {
    galFilters.querySelectorAll('.gal-filter').forEach(function (btn) {
      btn.addEventListener('click', function () {
        galFilters.querySelectorAll('.gal-filter').forEach(function (b) {
          b.classList.remove('active');
        });
        btn.classList.add('active');
        applyFilter(btn.dataset.series || '');
      });
    });
  }

  /* ── UPDATE PANEL ── */
  function updatePanel(i, animate) {
    const w = works[i];
    const targets = [
      document.getElementById('p-title'),
      document.getElementById('p-desc')
    ];

    if (animate) targets.forEach(el => el.classList.add('panel-fade-out'));

    setTimeout(() => {
      const list = visibleList();
      const pos = Math.max(0, list.indexOf(i));
      const total = list.length || works.length;
      document.getElementById('p-counter').textContent =
        String(pos + 1).padStart(2, '0') + ' — ' + String(total).padStart(2, '0');
      document.getElementById('strip-idx').textContent =
        String(pos + 1).padStart(2, '0');
      fillEmTitle(document.getElementById('p-title'), w.title);
      document.getElementById('p-medium').textContent = w.medium;
      document.getElementById('p-dims').textContent   = w.dims;
      document.getElementById('p-desc').textContent   = w.desc;
      const priceEl = document.getElementById('p-price');
      const hasPrice = w.price !== null && w.price !== undefined && w.price !== '';
      priceEl.textContent = hasPrice ? w.price : 'Prix sur demande';
      priceEl.classList.toggle('on-request', !hasPrice);
      const priceRow = priceEl.closest('.price-row');
      if (priceRow) priceRow.classList.toggle('on-request-row', !hasPrice);
      // Le bouton mène toujours au formulaire de contact ; seul le libellé change
      btnAcq.dataset.mode = hasPrice ? 'acquisition' : 'quote';
      btnAcq.setAttribute('aria-label', hasPrice
        ? "Acquérir l'œuvre — aller au formulaire de contact"
        : "Demander le prix de cette œuvre — aller au formulaire de contact");
      const lbl = btnAcq.querySelector('.btn-label');
      if (lbl) lbl.textContent = hasPrice ? "Acquérir l'œuvre" : 'Demander le prix';
      const tagsEl = document.getElementById('p-tags');
      tagsEl.textContent = '';
      (w.tags || []).forEach(function (t) {
        const span = document.createElement('span');
        const cls = (t && TAG_CLASS.has(t.c)) ? t.c : '';
        span.className = cls ? ('tag ' + cls) : 'tag';
        span.textContent = t && t.l ? String(t.l) : '';
        tagsEl.appendChild(span);
      });
      if (w.imgDecor) {
        const decor = document.createElement('span');
        decor.className = 'tag tag-decor';
        decor.textContent = 'En décor';
        tagsEl.appendChild(decor);
      }
      const href = safeSlug(w.slug);
      const btnDetail = document.getElementById('btn-detail');
      if (btnDetail) btnDetail.href = href;
      const canvasLink = document.getElementById('canvas-link');
      if (canvasLink) canvasLink.href = href;
      pbar.style.width = ((pos + 1) / total * 100) + '%';
      btnFav.classList.toggle('liked', liked.has(i));

      if (animate) {
        targets.forEach(el => {
          el.classList.remove('panel-fade-out');
          el.classList.add('panel-fade-in');
          setTimeout(() => el.classList.remove('panel-fade-in'), 320);
        });
      }
    }, animate ? 120 : 0);
  }

  /* ── NAVIGATE ── */
  function go(i) {
    if (transitioning || i === current) return;
    transitioning = true;

    artEls[current].className  = 'artwork out';
    thumbEls[current].classList.remove('active');
    dotEls[current].classList.remove('active');

    current = ((i % works.length) + works.length) % works.length;

    artEls[current].className  = 'artwork in';
    thumbEls[current].classList.add('active');
    dotEls[current].classList.add('active');

    updatePanel(current, true);
    setTimeout(() => { transitioning = false; }, 460);
  }

  function step(dir) {
    const list = visibleList();
    if (!list.length) return;
    let pos = list.indexOf(current);
    if (pos < 0) { go(list[0]); return; }
    go(list[(pos + dir + list.length) % list.length]);
  }

  /* ── EVENTS ── */
  document.getElementById('btn-prev').addEventListener('click', e => {
    e.preventDefault();
    e.stopPropagation();
    step(-1);
  });
  document.getElementById('btn-next').addEventListener('click', e => {
    e.preventDefault();
    e.stopPropagation();
    step(1);
  });

  document.addEventListener('keydown', e => {
    if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
    const t = e.target;
    if (t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' || t.tagName === 'SELECT' || t.isContentEditable)) return;
    if (e.key === 'ArrowRight') step(1);
    if (e.key === 'ArrowLeft')  step(-1);
  });

  // Swipe
  let touchX = 0;
  let swiped = false;
  const ca = document.getElementById('canvas-area');
  const canvasLink = document.getElementById('canvas-link');
  ca.addEventListener('touchstart', e => { touchX = e.touches[0].clientX; swiped = false; }, { passive: true });
  ca.addEventListener('touchend',   e => {
    const dx = e.changedTouches[0].clientX - touchX;
    if (Math.abs(dx) > 40) {
      swiped = true;
      step(dx < 0 ? 1 : -1);
    }
  }, { passive: true });
  if (canvasLink) {
    canvasLink.addEventListener('click', e => {
      if (swiped) { e.preventDefault(); swiped = false; }
    });
  }

  // Acquérir / Demander le prix : défilement vers le formulaire de contact
  btnAcq.addEventListener('click', e => {
    e.stopPropagation();

    const prix = btnAcq.dataset.mode === 'quote';
    appliquerSujetContact(prix ? 'Demande de prix' : "Acquisition d'une œuvre");

    // Nom de l'œuvre ajouté au message (via value, jamais innerHTML)
    const msg = document.getElementById('cf-msg');
    if (msg && !msg.value) {
      const titre = works[current].title.replace(/<[^>]+>/g, '');
      msg.value = prix
        ? "Bonjour, je souhaiterais connaître le prix de l'œuvre « " + titre + " »."
        : "Bonjour, je souhaite acquérir l'œuvre « " + titre + " ».";
      msg.dispatchEvent(new Event('input'));
    }

    const contact = document.getElementById('contact-section');
    if (contact) contact.scrollIntoView({ behavior: 'smooth' });
  });

  // Favori
  btnFav.addEventListener('click', e => {
    e.stopPropagation();
    liked.has(current) ? liked.delete(current) : liked.add(current);
    btnFav.classList.toggle('liked', liked.has(current));
  });

  /* ── INIT ── */
  (function restoreFromFiche() {
    var raw = '';
    try {
      raw = new URLSearchParams(location.search).get('oeuvre') || '';
    } catch (e) {}
    if (!raw) {
      try { raw = sessionStorage.getItem('ah_gallery_slug') || ''; } catch (e2) {}
    }
    try { sessionStorage.removeItem('ah_gallery_slug'); } catch (e3) {}
    if (!raw) return;
    var key = String(raw).replace(/^.*\//, '').replace(/\.html$/, '');
    if (!/^[a-z0-9-]+$/.test(key)) return;
    var i = works.findIndex(function (w) { return w.slug === 'oeuvres/' + key + '.html'; });
    if (i < 0 || i === current) return;
    artEls[current].className = 'artwork out';
    thumbEls[current].classList.remove('active');
    dotEls[current].classList.remove('active');
    current = i;
    artEls[current].className = 'artwork in';
    thumbEls[current].classList.add('active');
    dotEls[current].classList.add('active');
  })();
  updatePanel(current, false);

})();

/* ══════════════════════════════
   NAV: observe new sections
══════════════════════════════ */
['portfolio-section','contact-section'].forEach(id => {
  const el = document.getElementById(id);
  if (el) sectionObserver.observe(el);
});

/* ══════════════════════════════
   PARCOURS — années / toiles
══════════════════════════════ */
(function () {
  const list = document.getElementById('parcours-list');
  if (!list) return;
  const shots = Array.from(document.querySelectorAll('.parcours-shot'));
  const items = Array.from(list.querySelectorAll('li'));

  function show(year) {
    shots.forEach(fig => {
      const on = fig.dataset.year === year;
      fig.classList.toggle('is-on', on);
      fig.setAttribute('aria-hidden', on ? 'false' : 'true');
    });
    items.forEach(li => {
      const on = li.querySelector('button')?.dataset.year === year;
      li.classList.toggle('is-on', on);
      const btn = li.querySelector('button');
      if (btn) btn.setAttribute('aria-pressed', on ? 'true' : 'false');
    });
  }

  list.querySelectorAll('button').forEach(btn => {
    btn.addEventListener('click', () => show(btn.dataset.year));
  });
})();

/* ══════════════════════════════
   DÉMARCHE — mur de toiles
══════════════════════════════ */
(function () {
  const wall = document.getElementById('demarche-wall');
  if (!wall) return;
  const tiles = Array.from(wall.querySelectorAll('.demarche-tile'));
  const panels = Array.from(document.querySelectorAll('.demarche-panel'));

  function open(idx) {
    tiles.forEach(t => {
      const on = t.dataset.panel === idx;
      t.classList.toggle('is-on', on);
      t.setAttribute('aria-pressed', on ? 'true' : 'false');
    });
    panels.forEach(p => {
      const on = p.dataset.panel === idx;
      p.classList.toggle('is-on', on);
      p.hidden = !on;
    });
  }

  tiles.forEach(t => t.addEventListener('click', () => open(t.dataset.panel)));
})();

/* ══════════════════════════════
   CONTACT FORM
══════════════════════════════ */
(function () {
  const rdv = document.getElementById('btn-rdv-atelier');
  if (rdv) {
    rdv.addEventListener('click', () => appliquerSujetContact('atelier'));
  }

  document.querySelectorAll('.subj-chip').forEach(chip => {
    chip.addEventListener('click', () => {
      if (chip.closest('.atelier-when') || chip.closest('.pref-chips')) return;
      document.querySelectorAll('#subj-chips .subj-chip').forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      const subjectInput = document.getElementById('cf-subject');
      if (subjectInput) subjectInput.value = chip.dataset.val;
      syncAtelierSlot();
      updateMissing();
    });
  });

  const atelierSlot = document.getElementById('atelier-slot');
  const atelierJour = document.getElementById('cf-atelier-jour');
  let atelierWhen = '';
  function isAtelierSujet() {
    const subjectInput = document.getElementById('cf-subject');
    return !!(subjectInput && subjectInput.value === 'atelier');
  }
  function syncAtelierSlot() {
    if (!atelierSlot) return;
    const on = isAtelierSujet();
    atelierSlot.hidden = !on;
    if (!on) {
      atelierWhen = '';
      if (atelierJour) {
        atelierJour.value = '';
        atelierJour.classList.remove('error');
      }
      document.querySelectorAll('.atelier-when .subj-chip').forEach(function (c) {
        c.classList.remove('active');
      });
    }
  }
  document.querySelectorAll('.atelier-when .subj-chip').forEach(function (chip) {
    chip.addEventListener('click', function () {
      document.querySelectorAll('.atelier-when .subj-chip').forEach(function (c) {
        c.classList.remove('active');
      });
      chip.classList.add('active');
      atelierWhen = chip.dataset.when || '';
      updateMissing();
    });
  });
  if (atelierJour) {
    atelierJour.addEventListener('change', function () {
      atelierJour.classList.remove('error');
      updateMissing();
    });
  }

  const msgEl = document.getElementById('cf-msg');
  const ccEl  = document.getElementById('char-count');
  if (msgEl && ccEl) {
    msgEl.addEventListener('input', () => {
      const n = msgEl.value.length;
      ccEl.textContent = n + ' / 600';
      ccEl.classList.toggle('is-warn', n > 550);
      if (n > 600) msgEl.value = msgEl.value.slice(0, 600);
    });
  }

  /* Indicatif pays + format national (pas de librairie externe) */
  const PHONE_COUNTRIES = [
    { iso: 'FR', name: 'France',              dial: '33',  mask: 'X XX XX XX XX' },
    { iso: 'DE', name: 'Allemagne',           dial: '49',  mask: 'XXXX XXXXXXXX' },
    { iso: 'AD', name: 'Andorre',             dial: '376', mask: 'XXX XXX' },
    { iso: 'SA', name: 'Arabie saoudite',     dial: '966', mask: 'XX XXX XXXX' },
    { iso: 'AR', name: 'Argentine',           dial: '54',  mask: 'XX XXXX XXXX' },
    { iso: 'AU', name: 'Australie',           dial: '61',  mask: 'XXX XXX XXX' },
    { iso: 'AT', name: 'Autriche',            dial: '43',  mask: 'XXX XXXXXXX' },
    { iso: 'BE', name: 'Belgique',            dial: '32',  mask: 'XXX XX XX XX' },
    { iso: 'BR', name: 'Brésil',              dial: '55',  mask: 'XX XXXXX XXXX' },
    { iso: 'BG', name: 'Bulgarie',            dial: '359', mask: 'XXX XXX XXX' },
    { iso: 'CA', name: 'Canada',              dial: '1',   mask: '(XXX) XXX-XXXX' },
    { iso: 'CL', name: 'Chili',               dial: '56',  mask: 'X XXXX XXXX' },
    { iso: 'CY', name: 'Chypre',              dial: '357', mask: 'XX XXXXXX' },
    { iso: 'CO', name: 'Colombie',            dial: '57',  mask: 'XXX XXX XXXX' },
    { iso: 'KR', name: 'Corée du Sud',        dial: '82',  mask: 'XX XXXX XXXX' },
    { iso: 'CI', name: 'Côte d\'Ivoire',      dial: '225', mask: 'XX XX XX XX XX' },
    { iso: 'HR', name: 'Croatie',             dial: '385', mask: 'XX XXX XXXX' },
    { iso: 'DK', name: 'Danemark',            dial: '45',  mask: 'XX XX XX XX' },
    { iso: 'AE', name: 'Émirats arabes unis', dial: '971', mask: 'XX XXX XXXX' },
    { iso: 'ES', name: 'Espagne',             dial: '34',  mask: 'XXX XX XX XX' },
    { iso: 'EE', name: 'Estonie',             dial: '372', mask: 'XXXX XXXX' },
    { iso: 'US', name: 'États-Unis',          dial: '1',   mask: '(XXX) XXX-XXXX' },
    { iso: 'FI', name: 'Finlande',            dial: '358', mask: 'XX XXX XXXX' },
    { iso: 'GR', name: 'Grèce',               dial: '30',  mask: 'XXX XXX XXXX' },
    { iso: 'HU', name: 'Hongrie',             dial: '36',  mask: 'XX XXX XXXX' },
    { iso: 'IN', name: 'Inde',                dial: '91',  mask: 'XXXXX XXXXX' },
    { iso: 'IE', name: 'Irlande',             dial: '353', mask: 'XX XXX XXXX' },
    { iso: 'IS', name: 'Islande',             dial: '354', mask: 'XXX XXXX' },
    { iso: 'IL', name: 'Israël',              dial: '972', mask: 'XX XXX XXXX' },
    { iso: 'IT', name: 'Italie',              dial: '39',  mask: 'XXX XXX XXXX' },
    { iso: 'JP', name: 'Japon',               dial: '81',  mask: 'XX XXXX XXXX' },
    { iso: 'LV', name: 'Lettonie',            dial: '371', mask: 'XX XXX XXX' },
    { iso: 'LT', name: 'Lituanie',            dial: '370', mask: 'XXX XXXXX' },
    { iso: 'LU', name: 'Luxembourg',          dial: '352', mask: 'XXX XXX XXX' },
    { iso: 'MA', name: 'Maroc',               dial: '212', mask: 'X XX XX XX XX' },
    { iso: 'MX', name: 'Mexique',             dial: '52',  mask: 'XX XXXX XXXX' },
    { iso: 'MC', name: 'Monaco',              dial: '377', mask: 'XX XX XX XX' },
    { iso: 'NO', name: 'Norvège',             dial: '47',  mask: 'XXX XX XXX' },
    { iso: 'NZ', name: 'Nouvelle-Zélande',    dial: '64',  mask: 'XX XXX XXXX' },
    { iso: 'NL', name: 'Pays-Bas',            dial: '31',  mask: 'X XXXXXXXX' },
    { iso: 'PL', name: 'Pologne',             dial: '48',  mask: 'XXX XXX XXX' },
    { iso: 'PT', name: 'Portugal',            dial: '351', mask: 'XXX XXX XXX' },
    { iso: 'CZ', name: 'République tchèque',  dial: '420', mask: 'XXX XXX XXX' },
    { iso: 'RO', name: 'Roumanie',            dial: '40',  mask: 'XXX XXX XXX' },
    { iso: 'GB', name: 'Royaume-Uni',         dial: '44',  mask: 'XXXX XXXXXX' },
    { iso: 'SN', name: 'Sénégal',             dial: '221', mask: 'XX XXX XX XX' },
    { iso: 'SG', name: 'Singapour',           dial: '65',  mask: 'XXXX XXXX' },
    { iso: 'SK', name: 'Slovaquie',           dial: '421', mask: 'XXX XXX XXX' },
    { iso: 'SI', name: 'Slovénie',            dial: '386', mask: 'XX XXX XXX' },
    { iso: 'SE', name: 'Suède',               dial: '46',  mask: 'XX XXX XXXX' },
    { iso: 'CH', name: 'Suisse',              dial: '41',  mask: 'XX XXX XX XX' },
    { iso: 'TN', name: 'Tunisie',             dial: '216', mask: 'XX XXX XXX' },
    { iso: 'TR', name: 'Turquie',             dial: '90',  mask: 'XXX XXX XX XX' },
    { iso: 'UA', name: 'Ukraine',             dial: '380', mask: 'XX XXX XXXX' },
    { iso: 'DZ', name: 'Algérie',             dial: '213', mask: 'XXX XX XX XX' }
  ];

  function flagEmoji(iso) {
    return String.fromCodePoint(
      ...[...iso.toUpperCase()].map(function (c) { return 127397 + c.charCodeAt(0); })
    );
  }
  function maskDigitCount(mask) {
    return (mask.match(/X/g) || []).length;
  }
  function applyPhoneMask(digits, mask) {
    var i = 0, out = '', ch;
    for (var n = 0; n < mask.length; n++) {
      ch = mask.charAt(n);
      if (i >= digits.length) break;
      if (ch === 'X') { out += digits.charAt(i); i++; }
      else out += ch;
    }
    return out;
  }
  function nationalDigits(raw, country) {
    var d = String(raw || '').replace(/\D/g, '');
    if (country.iso === 'FR' || country.iso === 'BE' || country.iso === 'CH' ||
        country.iso === 'LU' || country.iso === 'MA' || country.iso === 'DZ' ||
        country.iso === 'TN' || country.iso === 'IT' || country.iso === 'ES') {
      if (d.charAt(0) === '0') d = d.slice(1);
    }
    var max = maskDigitCount(country.mask);
    if (d.length > max) d = d.slice(0, max);
    return d;
  }
  function detectFromDigits(all) {
    var list = PHONE_COUNTRIES.slice().sort(function (a, b) { return b.dial.length - a.dial.length; });
    for (var i = 0; i < list.length; i++) {
      if (all.indexOf(list[i].dial) === 0) {
        return { country: list[i], rest: all.slice(list[i].dial.length) };
      }
    }
    return null;
  }

  function initTelField() {
    var wrap = document.getElementById('tel-field');
    var btn = document.getElementById('tel-cc');
    var flagEl = document.getElementById('tel-cc-flag');
    var dialEl = document.getElementById('tel-cc-dial');
    var tel = document.getElementById('cf-tel');
    var hidden = document.getElementById('cf-tel-full');
    var panel = document.getElementById('tel-cc-panel');
    var search = document.getElementById('tel-cc-search');
    var list = document.getElementById('tel-cc-list');
    if (!wrap || !btn || !tel || !hidden || !panel || !list) return null;

    var current = PHONE_COUNTRIES[0];

    function syncHidden() {
      var d = nationalDigits(tel.value, current);
      hidden.value = d ? ('+' + current.dial + d) : '';
    }
    function paintCountry() {
      flagEl.textContent = flagEmoji(current.iso);
      dialEl.textContent = '+' + current.dial;
      tel.placeholder = current.mask;
      tel.maxLength = current.mask.length;
      btn.setAttribute('aria-label', 'Indicatif pays, ' + current.name + ' plus ' + current.dial);
      Array.prototype.forEach.call(list.children, function (li) {
        var on = li.getAttribute('data-iso') === current.iso;
        li.classList.toggle('is-active', on);
        var opt = li.querySelector('[role="option"]');
        if (opt) opt.setAttribute('aria-selected', on ? 'true' : 'false');
      });
    }
    function persistIso(iso) {
      try { sessionStorage.setItem('ah_tel_iso', iso); } catch (e) {}
    }
    function savedIso() {
      try {
        var iso = sessionStorage.getItem('ah_tel_iso');
        if (iso && PHONE_COUNTRIES.some(function (c) { return c.iso === iso; })) return iso;
      } catch (e) {}
      return null;
    }
    function setCountry(iso, keepDigits) {
      var next = PHONE_COUNTRIES.filter(function (c) { return c.iso === iso; })[0];
      if (!next) return;
      var digits = keepDigits ? nationalDigits(tel.value, current) : '';
      current = next;
      persistIso(current.iso);
      tel.value = applyPhoneMask(digits, current.mask);
      paintCountry();
      syncHidden();
    }
    function formatFromInput() {
      var raw = tel.value.trim();
      var all = raw.replace(/\D/g, '');
      var intl = raw.charAt(0) === '+' || raw.indexOf('00') === 0;
      if (intl && all.length > 4) {
        if (all.indexOf('00') === 0) all = all.slice(2);
        var hit = detectFromDigits(all);
        if (hit && hit.rest.length) {
          current = hit.country;
          persistIso(current.iso);
          tel.value = applyPhoneMask(nationalDigits(hit.rest, current), current.mask);
          paintCountry();
          syncHidden();
          return;
        }
      }
      var d = nationalDigits(raw, current);
      tel.value = applyPhoneMask(d, current.mask);
      syncHidden();
    }

    PHONE_COUNTRIES.forEach(function (c) {
      var li = document.createElement('li');
      li.setAttribute('data-iso', c.iso);
      li.setAttribute('data-q', (c.name + ' ' + c.iso + ' +' + c.dial).toLowerCase());
      var opt = document.createElement('button');
      opt.type = 'button';
      opt.className = 'tel-cc-option';
      opt.setAttribute('role', 'option');
      opt.setAttribute('aria-selected', c.iso === current.iso ? 'true' : 'false');
      var fl = document.createElement('span');
      fl.className = 'tel-cc-option-flag';
      fl.setAttribute('aria-hidden', 'true');
      fl.textContent = flagEmoji(c.iso);
      var nm = document.createElement('span');
      nm.className = 'tel-cc-option-name';
      nm.textContent = c.name;
      var di = document.createElement('span');
      di.className = 'tel-cc-option-dial';
      di.textContent = '+' + c.dial;
      opt.appendChild(fl);
      opt.appendChild(nm);
      opt.appendChild(di);
      opt.addEventListener('click', function () {
        setCountry(c.iso, true);
        closePanel();
        tel.focus();
      });
      li.appendChild(opt);
      list.appendChild(li);
    });

    function openPanel() {
      panel.hidden = false;
      btn.setAttribute('aria-expanded', 'true');
      if (search) {
        search.value = '';
        filter('');
        search.focus();
      }
    }
    function closePanel() {
      panel.hidden = true;
      btn.setAttribute('aria-expanded', 'false');
    }
    function filter(q) {
      q = String(q || '').toLowerCase().trim();
      Array.prototype.forEach.call(list.children, function (li) {
        var show = !q || (li.getAttribute('data-q') || '').indexOf(q) !== -1;
        li.hidden = !show;
      });
    }

    btn.addEventListener('click', function (e) {
      e.preventDefault();
      if (panel.hidden) openPanel(); else closePanel();
    });
    if (search) {
      search.addEventListener('input', function () { filter(search.value); });
      search.addEventListener('keydown', function (e) {
        if (e.key === 'Enter') e.preventDefault();
        if (e.key === 'Escape') { closePanel(); btn.focus(); }
      });
    }
    tel.addEventListener('input', formatFromInput);
    tel.addEventListener('paste', function () {
      setTimeout(formatFromInput, 0);
    });
    document.addEventListener('click', function (e) {
      if (!wrap.contains(e.target)) closePanel();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !panel.hidden) { closePanel(); btn.focus(); }
    });

    paintCountry();
    var restored = savedIso();
    if (restored) setCountry(restored, false);
    syncHidden();
    return {
      reset: function () {
        var keep = savedIso();
        if (keep) current = PHONE_COUNTRIES.filter(function (c) { return c.iso === keep; })[0] || PHONE_COUNTRIES[0];
        tel.value = '';
        paintCountry();
        syncHidden();
        closePanel();
      }
    };
  }
  const telField = initTelField();

  const form    = document.getElementById('contact-form');
  const success = document.getElementById('form-success');
  const btnSend = document.getElementById('btn-send');
  const formReadyAt = Date.now() + 3000;
  const missingEl = document.getElementById('form-missing');
  const prefBox = document.getElementById('contact-pref');
  const telInput = document.getElementById('cf-tel');
  if (!form) return;
  if (success) success.setAttribute('aria-live', 'polite');

  function missingFields() {
    const list = [];
    const prenom = document.getElementById('cf-prenom');
    const nom = document.getElementById('cf-nom');
    const email = document.getElementById('cf-email');
    const msg = document.getElementById('cf-msg');
    const privacy = document.getElementById('cf-privacy');
    if (prenom && !prenom.value.trim()) list.push('prénom');
    if (nom && !nom.value.trim()) list.push('nom');
    if (email && !email.value.trim()) list.push('email');
    if (msg && !msg.value.trim()) list.push('message');
    if (privacy && !privacy.checked) list.push('case confidentialité');
    if (isAtelierSujet()) {
      if (!atelierJour || !atelierJour.value) list.push('jour de visite');
      if (!atelierWhen) list.push('matin ou après-midi');
    }
    return list;
  }
  function updateMissing() {
    if (!missingEl) return;
    const list = missingFields();
    missingEl.textContent = list.length ? ('Il manque : ' + list.join(', ') + '.') : '';
  }
  function syncPref() {
    const has = !!(telInput && /\d/.test(telInput.value));
    if (prefBox) prefBox.hidden = !has;
    if (!has) {
      const emailRadio = form.querySelector('input[name="contact_pref"][value="email"]');
      if (emailRadio) emailRadio.checked = true;
    }
  }

  form.addEventListener('submit', e => {
    e.preventDefault();
    const gotcha = form.querySelector('input[name="_gotcha"]');
    if (gotcha && gotcha.value) return;
    if (Date.now() < formReadyAt) return;
    let valid = true;
    ['cf-prenom','cf-nom','cf-email','cf-msg'].forEach(id => {
      const el = document.getElementById(id);
      if (el && !el.value.trim()) { el.classList.add('error'); valid = false; }
      else if (el) el.classList.remove('error');
    });
    if (!document.getElementById('cf-privacy')?.checked) valid = false;
    if (isAtelierSujet()) {
      if (!atelierJour || !atelierJour.value) {
        if (atelierJour) atelierJour.classList.add('error');
        valid = false;
      }
      if (!atelierWhen) valid = false;
    }
    updateMissing();
    if (!valid) return;
    if (isAtelierSujet() && msgEl) {
      const line = 'Créneau souhaité : ' + atelierJour.value + ' · ' + atelierWhen;
      if (msgEl.value.indexOf('Créneau souhaité :') === -1) {
        msgEl.value = msgEl.value.replace(/\s+$/, '') + '\n\n' + line;
        msgEl.dispatchEvent(new Event('input'));
      }
    }
    btnSend.disabled = true;
    btnSend.querySelector('.btn-send-label').textContent = 'Envoi en cours…';
    fetch('https://formspree.io/f/mjykyvno', {
      method: 'POST',
      body: new FormData(form),
      headers: { 'Accept': 'application/json' }
    })
    .then(res => {
      if (res.ok) {
        if (success) {
          success.classList.add('show');
          success.setAttribute('aria-hidden', 'false');
        }
        form.reset();
        if (telField) telField.reset();
        atelierWhen = '';
        syncAtelierSlot();
        syncPref();
        updateMissing();
      } else {
        btnSend.disabled = false;
        btnSend.querySelector('.btn-send-label').textContent = 'Réessayer';
        alert('Une erreur est survenue. Merci de réessayer ou d\'écrire directement à angeliqueheduin@gmail.com');
      }
    })
    .catch(() => {
      btnSend.disabled = false;
      btnSend.querySelector('.btn-send-label').textContent = 'Réessayer';
      alert('Problème de connexion. Merci d\'écrire directement à angeliqueheduin@gmail.com');
    });
  });

  ['cf-prenom','cf-nom','cf-email','cf-msg'].forEach(id => {
    document.getElementById(id)?.addEventListener('input', function () {
      this.classList.remove('error');
      updateMissing();
    });
  });
  const privacyEl = document.getElementById('cf-privacy');
  if (privacyEl) privacyEl.addEventListener('change', updateMissing);
  if (telInput) telInput.addEventListener('input', function () { syncPref(); updateMissing(); });
  syncAtelierSlot();
  syncPref();
  updateMissing();

  /* Arrivée depuis une fiche œuvre : sujet et message déposés par js/contact-prefill.js */
  (function () {
    let sujet, message;
    try {
      sujet   = sessionStorage.getItem('ah_contact_sujet');
      message = sessionStorage.getItem('ah_contact_message');
      sessionStorage.removeItem('ah_contact_sujet');
      sessionStorage.removeItem('ah_contact_message');
    } catch (e) { return; }
    if (!sujet && !message) return;

    if (sujet) appliquerSujetContact(sujet);
    if (message && msgEl && !msgEl.value) {
      msgEl.value = message;
      msgEl.dispatchEvent(new Event('input'));
    }
    updateMissing();
  })();
})();

/* ══════════════════════════════
   LEAFLET INTERACTIVE MAP
   17 Chemin du Mairoual, Bessan
   lat: 43.3448, lng: 3.4158
══════════════════════════════ */
(function () {
  const mapEl     = document.getElementById('leaflet-map');
  const mapElFull = document.getElementById('leaflet-map-full');
  if (!mapEl || typeof L === 'undefined') return;

  // Coordonnées précises : Chemin du Mairoual, Bessan
  const LAT = 43.35667144154177, LNG = 3.4191283889352744;

  const POPUP_HTML = `
    <div style="font-family:'DM Sans',sans-serif;padding:4px 2px">
      <div style="font-family:'Cormorant Garamond',serif;font-size:.95rem;font-weight:500;font-style:italic;color:#1c1710;margin-bottom:4px">Angélique Héduin</div>
      <div style="font-size:.66rem;color:#6a6057;line-height:1.6">
        Atelier · 17 Chemin du Mairoual<br>
        34550 Bessan<br>
        <span style="color:#3a7a54;font-weight:500">sur rendez-vous · Mar–Sam 10h–18h</span>
      </div>
    </div>`;

  const ICON_HTML = `<div style="width:36px;height:42px;display:flex;flex-direction:column;align-items:center;filter:drop-shadow(0 3px 8px rgba(28,23,16,.28));">
    <svg width="28" height="36" viewBox="0 0 28 36" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M14 0C6.27 0 0 6.27 0 14C0 24.5 14 36 14 36C14 36 28 24.5 28 14C28 6.27 21.73 0 14 0Z" fill="#c94b22"/>
      <circle cx="14" cy="14" r="6" fill="white"/>
      <circle cx="14" cy="14" r="3" fill="#c94b22"/>
    </svg>
  </div>`;

  function makeIcon() {
    return L.divIcon({ className: '', html: ICON_HTML, iconSize: [36,42], iconAnchor: [18,42], popupAnchor: [0,-44] });
  }

  function applySepia(mapInstance) {
    const tp = mapInstance.getPane('tilePane');
    if (tp) tp.style.filter = 'sepia(22%) saturate(0.85) brightness(1.04)';
  }

  function createMap(el, zoom, scrollWheel, isMini) {
    const m = L.map(el, {
      center: [LAT, LNG],
      zoom,
      zoomControl: true,
      scrollWheelZoom: scrollWheel,
      attributionControl: true
    });
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      maxZoom: 19,
      detectRetina: false,
      referrerPolicy: 'strict-origin-when-cross-origin'
    }).addTo(m);
    applySepia(m);
    const isMobile = window.innerWidth < 600;
    const marker = L.marker([LAT, LNG], { icon: makeIcon() }).addTo(m)
      .bindPopup(POPUP_HTML, {
        className: 'ah-popup',
        maxWidth: isMini && isMobile ? 200 : (isMobile ? 220 : 240),
        maxHeight: isMini ? 130 : 220,
        autoPan: true,
        keepInView: true,
        autoPanPaddingTopLeft: isMini ? [52, 56] : [40, 40],
        autoPanPaddingBottomRight: isMini ? [16, 40] : [40, 40]
      });
    if (isMini) {
      marker.on('popupopen', function () { el.classList.add('popup-open'); });
      marker.on('popupclose', function () { el.classList.remove('popup-open'); });
    }
    marker.openPopup();
    return { map: m, marker: marker };
  }

  // ── Carte mini — créée seulement quand elle est visible
  // (évite de télécharger des tuiles OSM tant que la section n'est pas vue)
  let mini = null;
  let map = null;

  mapEl.addEventListener('click', function onMapClick() {
    if (!map) return;
    map.scrollWheelZoom.enable();
    mapEl.classList.add('scroll-active');
    mapEl.removeEventListener('click', onMapClick);
  });

  const mapObs = new IntersectionObserver(function (entries) {
    if (!entries[0].isIntersecting) return;
    if (!mini) {
      mini = createMap(mapEl, 15, false, true);
      map = mini.map;
    }
    setTimeout(function () {
      map.invalidateSize();
      mini.marker.openPopup();
    }, 200);
    mapObs.disconnect();
  }, { threshold: 0.1 });
  mapObs.observe(mapEl);

  // ── Carte full — pré-initialisée dès le chargement ──
  // Le conteneur est rendu temporairement mesurable (visibility:hidden, pas display:none)
  // pour que Leaflet calcule les bonnes dimensions dès le départ.
  // À l'ouverture du modal : simple invalidateSize() → aucun délai, aucune saccade.
  const btnExpand = document.getElementById('map-expand-btn');
  const modal     = document.getElementById('map-modal');
  const btnClose  = document.getElementById('map-modal-close');
  let   mapFull   = null;

  if (btnExpand && modal && mapElFull) {

    btnExpand.addEventListener('click', function () {
      modal.classList.add('open');
      document.body.style.overflow = 'hidden';
      requestAnimationFrame(function () {
        if (!mapFull) {
          var full = createMap(mapElFull, 16, true, false);
          mapFull = full.map;
        }
        mapFull.invalidateSize({ animate: false });
        mapFull.setView([LAT, LNG], 16);
      });
      setTimeout(function () { if (btnClose) btnClose.focus(); }, 120);
    });

    function closeModal() {
      modal.classList.remove('open');
      document.body.style.overflow = '';
      if (btnExpand) btnExpand.focus();
    }
    modal.addEventListener('keydown', e => {
      if (!modal.classList.contains('open')) return;
      const focusable = modal.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
      const first = focusable[0];
      const last  = focusable[focusable.length - 1];
      if (e.key === 'Tab') {
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      }
    });

    btnClose.addEventListener('click', closeModal);
    modal.addEventListener('click', e => { if (e.target === modal) closeModal(); });
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape' && modal.classList.contains('open')) closeModal();
    });
  }
})();