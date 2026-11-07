/**
 * lang.js — JanMitra Citizen Portal
 * Bilingual English/Hindi toggle.
 *
 * Usage: add data-en="..." and data-hi="..." attributes to any element.
 * The active language is stored in localStorage as 'janmitra-lang'.
 * On page load, the last-used language is restored.
 */

'use strict';

/** @type {'en' | 'hi'} */
let currentLang = 'en';

/**
 * Apply the given language to every element that has data-en / data-hi attributes.
 * Also updates <html lang="..."> and toggles active state on the language buttons.
 *
 * @param {'en' | 'hi'} lang
 */
function applyLang(lang) {
  if (lang !== 'en' && lang !== 'hi') return;

  currentLang = lang;

  // Update every translatable element
  document.querySelectorAll('[data-en]').forEach((el) => {
    const text = el.getAttribute(`data-${lang}`);
    if (text === null) return; // attribute not set for this lang — leave unchanged

    // Use innerHTML only for elements that explicitly opt in with data-html="true"
    if (el.dataset.html === 'true') {
      el.innerHTML = text;
    } else {
      el.textContent = text;
    }
  });

  // Update <html lang> for accessibility and SEO
  document.documentElement.lang = lang === 'hi' ? 'hi' : 'en';

  // Toggle active class on language buttons
  document.querySelectorAll('.lang-btn').forEach((btn) => {
    btn.classList.toggle('active', btn.dataset.lang === lang);
    btn.setAttribute('aria-pressed', btn.dataset.lang === lang ? 'true' : 'false');
  });

  // Update placeholder text on the search input (not a data-en/hi element itself)
  const searchInput = document.getElementById('schemeSearchInput');
  if (searchInput) {
    searchInput.placeholder =
      lang === 'hi'
        ? 'योजना नाम, श्रेणी, या लाभ से खोजें…'
        : 'Search by scheme name, category, or benefit…';
  }

  // Persist preference
  try {
    localStorage.setItem('janmitra-lang', lang);
  } catch {
    // localStorage unavailable — silently ignore
  }
}

/**
 * Toggle between English and Hindi.
 * Called from onclick handlers on the language buttons.
 *
 * @param {'en' | 'hi'} lang
 */
function setLang(lang) {
  applyLang(lang);
}

/**
 * Initialise language system on DOM ready.
 * Reads saved preference from localStorage; defaults to 'en'.
 */
function initLang() {
  let saved = 'en';
  try {
    saved = localStorage.getItem('janmitra-lang') || 'en';
  } catch {
    // ignore
  }
  applyLang(saved);
}

// Initialise when the DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initLang);
} else {
  initLang();
}

