/* Applique le thème avant le rendu. Choix : auto | light | dark, mémorisé dans localStorage. */
(function () {
  var KEY = "ah-theme";
  var NEXT = { auto: "light", light: "dark", dark: "auto" };
  var LABEL = { auto: "Auto", light: "Clair", dark: "Sombre" };

  function stored() {
    try {
      var v = localStorage.getItem(KEY);
      if (v === "light" || v === "dark" || v === "auto") return v;
    } catch (e) {}
    return "auto";
  }

  function isDark(choice) {
    if (choice === "dark") return true;
    if (choice === "light") return false;
    return window.matchMedia("(prefers-color-scheme: dark)").matches;
  }

  function apply(choice) {
    document.documentElement.setAttribute("data-theme", choice);
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.setAttribute("content", isDark(choice) ? "#1c1710" : "#c94b22");
    syncFavicons(choice);
    var btn = document.getElementById("theme-toggle");
    if (!btn) return;
    var label = btn.querySelector(".theme-toggle-label");
    if (label) label.textContent = LABEL[choice];
    btn.setAttribute("aria-label", "Thème : " + LABEL[choice] + ". Passer à " + LABEL[NEXT[choice]] + ".");
  }

  function syncFavicons(choice) {
    var dark = isDark(choice);
    var forced = choice === "light" || choice === "dark";
    var nodes = document.querySelectorAll("link[data-favicon]");
    for (var i = 0; i < nodes.length; i++) {
      var which = nodes[i].getAttribute("data-favicon");
      if (!forced) {
        nodes[i].media = which === "dark"
          ? "(prefers-color-scheme: dark)"
          : "(prefers-color-scheme: light)";
      } else {
        nodes[i].media = (which === "dark") === dark ? "all" : "not all";
      }
    }
  }

  apply(stored());

  document.addEventListener("DOMContentLoaded", function () {
    apply(stored());
    var btn = document.getElementById("theme-toggle");
    if (!btn) return;
    btn.addEventListener("click", function () {
      var next = NEXT[stored()];
      try { localStorage.setItem(KEY, next); } catch (e) {}
      apply(next);
    });
  });
})();
