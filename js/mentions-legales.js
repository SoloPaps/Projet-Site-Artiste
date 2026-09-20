'use strict';

/* ── Hamburger menu (mobile) ── */
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

  drawer.querySelectorAll('.nav-drawer-link, .nav-drawer-cta').forEach(link => {
    link.addEventListener('click', closeDrawer);
  });

  document.addEventListener('click', e => {
    if (!btn.contains(e.target) && !drawer.contains(e.target)) closeDrawer();
  });

  window.addEventListener('scroll', closeDrawer, { passive: true });
})();

/* ── Nav scroll ── */
const navbar = document.getElementById('navbar');
if (navbar) {
  window.addEventListener('scroll', () => {
    navbar.classList.toggle('scrolled', window.scrollY > 40);
  }, { passive: true });
}

/* ── Barre de progression de lecture ── */
const progressBar = document.getElementById('ml-progress');
if (progressBar) {
  window.addEventListener('scroll', () => {
    const scrollTop    = window.scrollY;
    const docHeight    = document.documentElement.scrollHeight - window.innerHeight;
    const pct          = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
    const clamped = Math.min(pct, 100);
    progressBar.style.width = clamped + '%';
    progressBar.setAttribute('aria-valuenow', Math.round(clamped));
  }, { passive: true });
}

/* ── Scroll reveal des sections ── */
(function () {
  const sections = Array.from(document.querySelectorAll('.ml-section'));
  if (!sections.length) return;

  const obs = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add('visible');
        obs.unobserve(e.target);
      }
    });
  }, { threshold: 0.06 });

  sections.forEach(s => obs.observe(s));
})();

/* ── TOC — mise à jour du lien actif au scroll ── */
(function () {
  const tocLinks = Array.from(document.querySelectorAll('.ml-toc-link[data-section]'));
  const sections = Array.from(document.querySelectorAll('.ml-section[data-section]'));
  if (!tocLinks.length || !sections.length) return;

  function setActive(id) {
    tocLinks.forEach(link => {
      link.classList.toggle('active', link.dataset.section === id);
    });
  }

  // Scroll smooth au clic

  // IntersectionObserver pour l'actif
  const sectionObs = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        setActive(entry.target.dataset.section);
      }
    });
  }, {
    rootMargin: '-30% 0px -60% 0px',
    threshold: 0
  });

  sections.forEach(s => sectionObs.observe(s));
})();

/* ── Bouton retour en haut ── */
(function () {
  const btn = document.getElementById('ml-btn-top');
  if (!btn) return;
  btn.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
})();



/* ── Micro-interaction : copier l'email au clic ── */
(function () {
  const emailLinks = Array.from(document.querySelectorAll('a[href^="mailto:"]'));
  emailLinks.forEach(link => {
    link.addEventListener('click', e => {
      // On laisse le comportement par défaut (ouverture client mail)
      // Mais on ajoute un feedback visuel
      const original = link.textContent;
      link.style.transition = 'all .25s';
    });
  });
})();

/* ── Highlight des éléments à compléter (placeholders) ── */
(function () {
  const placeholders = Array.from(document.querySelectorAll('.ml-placeholder'));

  // Tooltip au survol
  placeholders.forEach(el => {
    el.setAttribute('title', 'À compléter avec vos informations');
    el.style.cursor = 'help';
  });
})();

/* ── Animations staggerées sur les cartes de droits ── */
(function () {
  const items = Array.from(document.querySelectorAll('.ml-right-item'));
  items.forEach((item, i) => {
    item.style.opacity = '0';
    item.style.transform = 'translateY(12px)';
    item.style.transition = `opacity .4s ${i * 60}ms ease, transform .4s ${i * 60}ms ease`;
  });

  const obs = new IntersectionObserver(entries => {
    if (entries[0].isIntersecting) {
      items.forEach(item => {
        item.style.opacity = '1';
        item.style.transform = 'translateY(0)';
      });
      obs.disconnect();
    }
  }, { threshold: 0.2 });

  const grid = document.querySelector('.ml-rights-grid');
  if (grid) obs.observe(grid);
})();

/* ── Animation des étapes du processus ── */
(function () {
  const steps = Array.from(document.querySelectorAll('.ml-step'));
  const connectors = Array.from(document.querySelectorAll('.ml-step-connector'));

  [...steps, ...connectors].forEach((el, i) => {
    el.style.opacity = '0';
    el.style.transform = 'translateX(-8px)';
    el.style.transition = `opacity .45s ${i * 80}ms ease, transform .45s ${i * 80}ms ease`;
  });

  const obs = new IntersectionObserver(entries => {
    if (entries[0].isIntersecting) {
      [...steps, ...connectors].forEach(el => {
        el.style.opacity = '1';
        el.style.transform = 'translateX(0)';
      });
      obs.disconnect();
    }
  }, { threshold: 0.15 });

  const container = document.querySelector('.ml-process-steps');
  if (container) obs.observe(container);
})();