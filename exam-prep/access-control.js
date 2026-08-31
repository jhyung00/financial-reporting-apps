(function () {
  "use strict";

  const config = window.BFIN_EXAM_PASSWORDS || {};
  const STORAGE_PREFIX = "bfin367_exam_unlocked_";
  const markerAttr = "data-bfin-exam-key";
  const basePath = "/financial-reporting-apps/exam-prep/";

  function normalizePath(value) {
    return String(value || "")
      .replace(/^\.?\//, "")
      .replace(/index\.html?$/i, "")
      .replace(/\/+$/, "") + "/";
  }

  function storageKey(key) { return STORAGE_PREFIX + key; }

  function isUnlocked(key) {
    try { return localStorage.getItem(storageKey(key)) === "1"; }
    catch (_) { return false; }
  }

  function rememberUnlock(key) {
    try { localStorage.setItem(storageKey(key), "1"); }
    catch (_) {}
  }

  function detectPageKey() {
    const marker = document.documentElement.getAttribute(markerAttr);
    if (marker && config[marker]) return marker;

    const pathname = window.location.pathname.replace(/\/+$/, "") + "/";
    for (const [key, item] of Object.entries(config)) {
      const tail = basePath + normalizePath(item.path);
      if (pathname.endsWith(tail)) return key;
    }
    return null;
  }

  function iconMarkup() {
    return `<div class="bfin-access-icon" aria-hidden="true">
      <svg viewBox="0 0 24 24">
        <rect x="5" y="10" width="14" height="10" rx="2"></rect>
        <path d="M8 10V7a4 4 0 0 1 8 0v3"></path>
        <path d="M12 14v2"></path>
      </svg>
    </div>`;
  }

  function showPrompt(key, options) {
    options = options || {};
    const item = config[key];
    if (!item) return;

    const layer = document.createElement("div");
    layer.className = "bfin-access-layer";
    layer.innerHTML = `
      <div class="bfin-access-card" role="dialog" aria-modal="true">
        ${iconMarkup()}
        <p class="bfin-access-kicker">BFIN 367 · Classroom Access</p>
        <h2>${item.label}</h2>
        <p class="bfin-access-copy">Enter the password provided in class to open this module.</p>
        <form class="bfin-access-form">
          <label class="bfin-access-label">Password</label>
          <input class="bfin-access-input" type="password" autocomplete="off" spellcheck="false">
          <p class="bfin-access-error" aria-live="polite"></p>
          <div class="bfin-access-actions">
            <button type="submit" class="bfin-access-button">Open Module</button>
            ${options.allowCancel ? '<button type="button" class="bfin-access-button secondary" data-access-cancel>Cancel</button>' : ""}
          </div>
        </form>
      </div>`;

    document.body.appendChild(layer);

    const input = layer.querySelector(".bfin-access-input");
    const error = layer.querySelector(".bfin-access-error");
    const form = layer.querySelector(".bfin-access-form");
    const cancel = layer.querySelector("[data-access-cancel]");

    function close() {
      layer.remove();
      document.documentElement.classList.remove("bfin-access-pending");
    }

    form.addEventListener("submit", function (event) {
      event.preventDefault();
      if (input.value === item.password) {
        rememberUnlock(key);
        if (options.navigateTo) window.location.href = options.navigateTo;
        else close();
      } else {
        error.textContent = "That password does not match. Try again.";
        input.select();
      }
    });

    if (cancel) cancel.addEventListener("click", close);
    setTimeout(() => input.focus(), 20);
  }

  function decorateLandingCards() {
    const links = Array.from(document.querySelectorAll("a[href]"));

    for (const [key, item] of Object.entries(config)) {
      const expected = normalizePath(item.path);
      const link = links.find(a => normalizePath(a.getAttribute("href") || "") === expected);
      if (!link) continue;

      link.classList.remove("hidden", "disabled");
      link.removeAttribute("aria-hidden");
      link.style.removeProperty("display");

      if (!link.querySelector(".bfin-access-pill")) {
        const pill = document.createElement("span");
        pill.className = "bfin-access-pill";
        pill.textContent = isUnlocked(key) ? "Unlocked on this browser" : "Password required";
        link.appendChild(pill);
      }

      link.addEventListener("click", function (event) {
        if (isUnlocked(key)) return;
        event.preventDefault();
        showPrompt(key, { allowCancel: true, navigateTo: link.href });
      });
    }
  }

  function init() {
    const pageKey = detectPageKey();

    if (pageKey) {
      if (isUnlocked(pageKey)) {
        document.documentElement.classList.remove("bfin-access-pending");
      } else {
        showPrompt(pageKey, { allowCancel: false });
      }
      return;
    }

    document.documentElement.classList.remove("bfin-access-pending");
    decorateLandingCards();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init, { once: true });
  } else {
    init();
  }
})();
