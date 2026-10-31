/*
 * Injects a "Contribute" CTA pill into the Material header, right next to
 * the palette toggle and source link. Done in JS (rather than via a
 * partial override of header.html) so we don't have to keep our copy in
 * sync with the upstream Material template.
 */
(function () {
  function mount() {
    var inner = document.querySelector(".md-header__inner");
    if (!inner) return;
    if (inner.querySelector(".kb-header-contribute")) return;

    var btn = document.createElement("a");
    btn.className = "kb-header-contribute";
    btn.href =
      "https://github.com/mathummacisco/knowledge-base/blob/main/CONTRIBUTING.md";
    btn.target = "_blank";
    btn.rel = "noopener";
    btn.setAttribute("aria-label", "Open the contributing guide on GitHub");
    btn.innerHTML =
      '<span class="kb-header-contribute__label">Contribute</span>' +
      '<span class="kb-header-contribute__arrow" aria-hidden="true">→</span>';

    var palette = inner.querySelector('[data-md-component="palette"]');
    var source = inner.querySelector(".md-header__source");
    var anchor = palette || source || null;

    if (anchor) {
      inner.insertBefore(btn, anchor);
    } else {
      inner.appendChild(btn);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", mount);
  } else {
    mount();
  }

  // Material uses instant navigation — when the page is swapped, the header
  // is re-rendered without a full reload. Re-mount on those events.
  if (typeof document$ !== "undefined" && document$.subscribe) {
    document$.subscribe(mount);
  }
})();
