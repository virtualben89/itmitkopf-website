/* Hell/Dunkel-Umschalter. Speichert die Wahl nur lokal im Browser (localStorage), kein Cookie. */
(function () {
  var root = document.documentElement, KEY = "theme";
  try {
    var saved = localStorage.getItem(KEY);
    if (saved === "light" || saved === "dark") root.setAttribute("data-theme", saved);
  } catch (e) {}

  function current() {
    return root.getAttribute("data-theme") ||
      (window.matchMedia && matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
  }

  document.addEventListener("DOMContentLoaded", function () {
    var btn = document.getElementById("theme-toggle");
    if (!btn) return;
    btn.hidden = false;
    btn.setAttribute("aria-pressed", String(current() === "dark"));
    btn.addEventListener("click", function () {
      var next = current() === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      btn.setAttribute("aria-pressed", String(next === "dark"));
      try { localStorage.setItem(KEY, next); } catch (e) {}
    });
  });
})();
