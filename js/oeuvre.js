/* oeuvre.js — scripts communs des fiches œuvres */
"use strict";

/* Navbar : fond opaque au scroll */
(function () {
  var nav = document.getElementById("navbar");
  if (!nav) return;
  window.addEventListener("scroll", function () {
    nav.classList.toggle("scrolled", window.scrollY > 40);
  }, { passive: true });
})();

/* Menu mobile */
(function () {
  var btn = document.getElementById("hamburger");
  var drawer = document.getElementById("nav-drawer");
  if (!btn || !drawer) return;
  function open()  { btn.classList.add("open");    btn.setAttribute("aria-expanded", "true");  drawer.classList.add("open");    drawer.setAttribute("aria-hidden", "false"); }
  function close() { btn.classList.remove("open"); btn.setAttribute("aria-expanded", "false"); drawer.classList.remove("open"); drawer.setAttribute("aria-hidden", "true"); }
  btn.addEventListener("click", function () { btn.classList.contains("open") ? close() : open(); });
  drawer.querySelectorAll(".nav-drawer-link, .nav-drawer-cta").forEach(function (l) { l.addEventListener("click", close); });
  document.addEventListener("click", function (e) { if (!btn.contains(e.target) && !drawer.contains(e.target)) close(); });
  window.addEventListener("scroll", close, { passive: true });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") close(); });
})();

/* Retour collection : mémoriser l'œuvre pour la remettre en scène */
(function () {
  var m = location.pathname.match(/([^/]+)\.html$/);
  var key = (m && /^[a-z0-9-]+$/.test(m[1])) ? m[1] : "";
  if (key) {
    try { sessionStorage.setItem("ah_gallery_slug", "oeuvres/" + key + ".html"); } catch (e) {}
  }
  var href = "../index.html" + (key ? ("?oeuvre=" + encodeURIComponent(key)) : "") + "#gallery-section";

  document.querySelectorAll("a[href]").forEach(function (a) {
    var h = a.getAttribute("href") || "";
    if (h.indexOf("index.html") === -1 || h.indexOf("gallery-section") === -1) return;
    a.setAttribute("href", href);
  });

  if (!document.getElementById("oeuvre-back-css")) {
    var st = document.createElement("style");
    st.id = "oeuvre-back-css";
    st.textContent =
      ".oeuvre-back{position:absolute;top:12px;left:12px;z-index:3;width:44px;height:44px;display:flex;align-items:center;justify-content:center;border-radius:50%;background:rgba(253,250,246,.94);color:#1c1710;text-decoration:none;border:1px solid rgba(28,23,16,.1);box-shadow:0 2px 12px rgba(28,23,16,.12);transition:transform .18s,background .18s}" +
      ".oeuvre-back:hover{background:#fdfaf6;transform:translateX(-3px)}" +
      ".oeuvre-back svg{display:block}";
    document.head.appendChild(st);
  }

  if (document.querySelector(".oeuvre-back")) return;
  var wrap = document.querySelector(".oeuvre-img-wrap");
  if (!wrap) return;
  var a = document.createElement("a");
  a.className = "oeuvre-back";
  a.href = href;
  a.setAttribute("aria-label", "Retour à la collection");
  var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  svg.setAttribute("width", "18");
  svg.setAttribute("height", "18");
  svg.setAttribute("viewBox", "0 0 18 18");
  svg.setAttribute("fill", "none");
  svg.setAttribute("aria-hidden", "true");
  var path = document.createElementNS("http://www.w3.org/2000/svg", "path");
  path.setAttribute("d", "M11.5 3.5L6 9l5.5 5.5");
  path.setAttribute("stroke", "currentColor");
  path.setAttribute("stroke-width", "1.7");
  path.setAttribute("stroke-linecap", "round");
  path.setAttribute("stroke-linejoin", "round");
  svg.appendChild(path);
  a.appendChild(svg);
  wrap.appendChild(a);
})();
