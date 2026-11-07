/**
 * Live scheme search, rendering, and detail modal.
 */
'use strict';

const API_BASE = window.API_BASE_URL || '';
let activeFilter = '';
let searchQuery = '';
let schemes = [];

function getCategoryBadgeClass(category) {
  if (!category) return 'Financial';
  if (category.includes('Agri')) return 'Agriculture';
  if (category.includes('Health')) return 'Health';
  if (category.includes('Hous')) return 'Housing';
  if (category.includes('Pens')) return 'Pension';
  if (category.includes('Women')) return 'Women';
  if (category.includes('Busi')) return 'Business';
  if (category.includes('Fin')) return 'Financial';
  if (category.includes('Edu')) return 'Education';
  if (category.includes('Disab')) return 'Disability';
  if (category.includes('Skill')) return 'Skill';
  return 'Financial';
}

function buildSchemeCard(scheme) {
  const age = scheme.age_max >= 999
    ? `${scheme.age_min}+ yrs / वर्ष`
    : `${scheme.age_min}–${scheme.age_max} yrs / वर्ष`;
  return `<article class="scheme-card">
    <div class="scheme-card-body">
      <span class="badge badge-${getCategoryBadgeClass(scheme.category)}">${scheme.category}</span>
      <h3 class="scheme-name">${scheme.scheme_name}</h3>
      <p class="scheme-hindi-name">${scheme.hindi_name || ''}</p>
      <div class="scheme-row"><span class="scheme-row-label">Benefit</span><span class="scheme-row-value">${scheme.benefit_amount || '—'}</span></div>
      <div class="scheme-row"><span class="scheme-row-label">Age</span><span class="scheme-row-value">${age}</span></div>
      <div class="scheme-row"><span class="scheme-row-label">Income</span><span class="scheme-row-value">${scheme.income_limit || 'No limit'}</span></div>
      <div class="scheme-row"><span class="scheme-row-label">Gender</span><span class="scheme-row-value">${scheme.gender === 'All' ? 'All / सभी' : scheme.gender}</span></div>
    </div>
    <div class="scheme-card-footer">
      <span class="scheme-helpline-label">☎ <strong>${scheme.helpline || '—'}</strong></span>
      <button class="scheme-detail-btn" onclick="openSchemeModal(${scheme.id})">View Details ↗</button>
    </div>
  </article>`;
}

function setState(message, className) {
  const grid = document.getElementById('schemeGrid');
  if (grid) grid.innerHTML = `<p class="${className}">${message}</p>`;
}

function renderSchemes() {
  const grid = document.getElementById('schemeGrid');
  const count = document.getElementById('resultsCount');
  if (!grid) return;
  if (!schemes.length) {
    setState('No schemes found. Try a different search. / कोई योजना नहीं मिली।', 'empty-state');
    if (count) {
      count.setAttribute('data-en', 'No schemes found');
      count.setAttribute('data-hi', 'कोई योजना नहीं मिली');
      count.textContent = 'No schemes found / कोई योजना नहीं मिली';
    }
    return;
  }
  grid.innerHTML = schemes.map(buildSchemeCard).join('');
  if (count) {
    count.setAttribute('data-en', `Showing ${schemes.length} schemes`);
    count.setAttribute('data-hi', `${schemes.length} योजनाएं दिखाई जा रही हैं`);
    count.textContent = `Showing ${schemes.length} schemes / ${schemes.length} योजनाएं`;
  }
  if (typeof applyLang === 'function') applyLang(typeof currentLang === 'undefined' ? 'en' : currentLang);
}

async function loadSchemes() {
  const params = new URLSearchParams({ page: '1', limit: '100' });
  if (searchQuery) params.set('search', searchQuery);
  if (activeFilter) params.set('category', activeFilter);
  setState('Loading schemes… / योजनाएं लोड हो रही हैं…', 'state-loading');
  try {
    const response = await fetch(`${API_BASE}/api/schemes?${params}`);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const payload = await response.json();
    schemes = payload.schemes || [];
    renderSchemes();
    updateFilterCounts();
  } catch (error) {
    console.error('Unable to load schemes', error);
    setState('Unable to load schemes. Please try again. / योजनाएं लोड नहीं हो सकीं।', 'error-state');
  }
}

function setSchemeFilter(category) {
  activeFilter = category === 'All' ? '' : category;
  document.querySelectorAll('.filter-btn').forEach((button) => {
    button.classList.toggle('active', button.dataset.filter === (activeFilter || 'All'));
  });
  loadSchemes();
}

function onSchemeSearch(event) {
  searchQuery = event.target.value.trim();
  loadSchemes();
}

async function updateFilterCounts() {
  try {
    const response = await fetch(`${API_BASE}/api/categories`);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const categories = await response.json();
    const counts = Object.fromEntries(categories.map((item) => [item.category, item.count]));
    document.querySelectorAll('.filter-btn[data-filter]').forEach((button) => {
      const category = button.dataset.filter;
      const base = button.dataset.baseEn || button.textContent.trim();
      button.dataset.baseEn = base.replace(/\s+\(\d+\)$/, '');
      button.textContent = `${button.dataset.baseEn} (${category === 'All' ? categories.reduce((sum, item) => sum + item.count, 0) : counts[category] || 0})`;
    });
    document.querySelectorAll('.category-card[data-category]').forEach((card) => {
      const badge = card.querySelector('.category-count');
      if (badge) badge.textContent = counts[card.dataset.category] || 0;
    });
  } catch (error) {
    console.error('Unable to load category counts', error);
  }
}

async function openSchemeModal(id) {
  let scheme = schemes.find((item) => item.id === id);
  if (!scheme) {
    try {
      const response = await fetch(`${API_BASE}/api/schemes/${id}`);
      if (response.ok) scheme = await response.json();
    } catch (err) {
      console.error('Unable to fetch scheme details', err);
    }
  }
  const modal = document.getElementById('schemeModal');
  if (!scheme || !modal) return;
  const age = scheme.age_max >= 999 ? `${scheme.age_min}+ years / वर्ष` : `${scheme.age_min}–${scheme.age_max} years / वर्ष`;
  const values = {
    modalTitle: scheme.scheme_name, modalHindi: scheme.hindi_name || '',
    modalMinistry: scheme.ministry || '—', modalCategory: scheme.category || '—',
    modalBenefit: scheme.benefit_amount || '—', modalBenefits: scheme.benefits || '—',
    modalAge: age, modalIncome: scheme.income_limit || 'No income limit',
    modalGender: scheme.gender || '—', modalCaste: scheme.caste_category || 'All',
    modalDocs: scheme.documents_required || '—', modalHelpline: scheme.helpline || '—',
  };
  Object.entries(values).forEach(([key, value]) => { modal.querySelector(`#${key}`).textContent = value; });
  modal.querySelector('#modalPortalLink').href = scheme.portal_url || '#';
  modal.classList.add('open');
  document.body.style.overflow = 'hidden';
}

function closeSchemeModal() {
  const modal = document.getElementById('schemeModal');
  if (modal) modal.classList.remove('open');
  document.body.style.overflow = '';
}

document.addEventListener('DOMContentLoaded', () => {
  const modal = document.getElementById('schemeModal');
  if (modal) modal.addEventListener('click', (event) => {
    if (event.target === modal) closeSchemeModal();
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') closeSchemeModal();
  });
  loadSchemes();
});
