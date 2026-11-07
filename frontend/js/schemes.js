/**
 * schemes.js — JanMitra Citizen Portal
 * Static embedded scheme data (22 central schemes) & rendering engine.
 * Connects to live API in Phase 2.
 */
'use strict';

const SCHEMES_DATA = [
  { id: 1, scheme_name: 'PM-Kisan Samman Nidhi', hindi_name: 'प्रधानमंत्री किसान सम्मान निधि', ministry: 'Ministry of Agriculture & Farmers Welfare', category: 'Agriculture', benefit_amount: 'Rs.6,000 per year', benefits: 'Direct income support of Rs.6,000/year in 3 installments of Rs.2,000 directly to bank account.', age_min: 18, age_max: 70, income_limit: 'Land holding up to 2 hectares', income_annual_max: null, gender: 'All', caste_category: 'All', documents_required: 'Aadhaar Card, Bank Passbook, Land Records (Khatoni), Self-declaration', portal_url: 'https://pmkisan.gov.in', helpline: '155261', status: 'Active' },
  { id: 2, scheme_name: 'PM Fasal Bima Yojana (PMFBY)', hindi_name: 'प्रधानमंत्री फसल बीमा योजना', ministry: 'Ministry of Agriculture & Farmers Welfare', category: 'Agriculture', benefit_amount: 'Full sum insured (crop-dependent)', benefits: 'Comprehensive crop insurance against natural calamities, pests, and diseases at 1.5%-5% premium.', age_min: 18, age_max: 999, income_limit: 'No income limit for enrolled farmers', income_annual_max: null, gender: 'All', caste_category: 'All', documents_required: 'Aadhaar, Bank account, Land records, Sowing certificate', portal_url: 'https://pmfby.gov.in', helpline: '14447', status: 'Active' },
  { id: 3, scheme_name: 'Kisan Credit Card (KCC)', hindi_name: 'किसान क्रेडिट कार्ड', ministry: 'Ministry of Agriculture & Farmers Welfare', category: 'Agriculture', benefit_amount: 'Up to Rs.3 Lakh (collateral-free)', benefits: 'Short-term subsidized credit at 4% effective interest for agricultural inputs and livestock maintenance.', age_min: 18, age_max: 75, income_limit: 'Based on cultivated land and crop scale', income_annual_max: null, gender: 'All', caste_category: 'All', documents_required: 'Aadhaar, PAN, Land records, Passport photo, Bank account', portal_url: 'https://agricoop.gov.in', helpline: '0120-6025109', status: 'Active' },
  { id: 4, scheme_name: 'Ayushman Bharat PM-JAY', hindi_name: 'आयुष्मान भारत प्रधानमंत्री जन आरोग्य योजना', ministry: 'Ministry of Health & Family Welfare', category: 'Health', benefit_amount: 'Rs.5 Lakh per family per year', benefits: 'Cashless secondary and tertiary health insurance coverage covering 1,900+ treatments and procedures.', age_min: 0, age_max: 999, income_limit: 'SECC 2011 database / State BPL list', income_annual_max: null, gender: 'All', caste_category: 'All', documents_required: 'Aadhaar, Ration Card, Mobile number', portal_url: 'https://pmjay.gov.in', helpline: '14555', status: 'Active' },
  { id: 5, scheme_name: 'Pradhan Mantri Suraksha Bima Yojana (PMSBY)', hindi_name: 'प्रधानमंत्री सुरक्षा बीमा योजना', ministry: 'Ministry of Finance', category: 'Health', benefit_amount: 'Rs.2 Lakh (accidental death/disability)', benefits: 'Accidental death and disability insurance cover at Rs.20/year premium debited from bank account.', age_min: 18, age_max: 70, income_limit: 'No income limit', income_annual_max: null, gender: 'All', caste_category: 'All', documents_required: 'Aadhaar, Bank account linked to Aadhaar', portal_url: 'https://jansuraksha.gov.in', helpline: '1800-180-1111', status: 'Active' },
  { id: 6, scheme_name: 'Pradhan Mantri Jeevan Jyoti Bima Yojana (PMJJBY)', hindi_name: 'प्रधानमंत्री जीवन ज्योति बीमा योजना', ministry: 'Ministry of Finance', category: 'Health', benefit_amount: 'Rs.2 Lakh on death (any cause)', benefits: 'Life insurance cover of Rs.2 Lakh for death due to any reason at an annual premium of Rs.436.', age_min: 18, age_max: 50, income_limit: 'No income limit', income_annual_max: null, gender: 'All', caste_category: 'All', documents_required: 'Aadhaar, Bank savings account', portal_url: 'https://jansuraksha.gov.in', helpline: '1800-180-1111', status: 'Active' },
  { id: 7, scheme_name: 'PM Awas Yojana - Urban (PMAY-U)', hindi_name: 'प्रधानमंत्री आवास योजना - शहरी', ministry: 'Ministry of Housing & Urban Affairs', category: 'Housing', benefit_amount: 'Subsidy up to Rs.2.35 Lakh', benefits: 'Interest subsidy on home loans for EWS, LIG, and MIG categories constructing or buying a home.', age_min: 21, age_max: 999, income_limit: 'EWS (<Rs.3L), LIG (<Rs.6L), MIG (<Rs.18L)', income_annual_max: 1800000, gender: 'All', caste_category: 'All', documents_required: 'Aadhaar, Income certificate, Property registry, Bank account', portal_url: 'https://pmaymis.gov.in', helpline: '1800-11-6163', status: 'Active' },
  { id: 8, scheme_name: 'PM Awas Yojana - Gramin (PMAY-G)', hindi_name: 'प्रधानमंत्री आवास योजना - ग्रामीण', ministry: 'Ministry of Rural Development', category: 'Housing', benefit_amount: 'Rs.1.2 Lakh to Rs.1.3 Lakh grant', benefits: 'Financial grant for construction of pucca house with basic amenities for homeless rural families.', age_min: 18, age_max: 999, income_limit: 'SECC 2011 / Rural BPL list', income_annual_max: null, gender: 'All', caste_category: 'All', documents_required: 'Aadhaar, BPL Ration card, Bank account, Land paper', portal_url: 'https://pmayg.gov.in', helpline: '1800-11-6446', status: 'Active' },
  { id: 9, scheme_name: 'Atal Pension Yojana (APY)', hindi_name: 'अटल पेंशन योजना', ministry: 'Ministry of Finance / PFRDA', category: 'Pension', benefit_amount: 'Rs.1,000–5,000/month after 60', benefits: 'Guaranteed government-backed pension for unorganized workers based on monthly contribution.', age_min: 18, age_max: 40, income_limit: 'Non-income tax payers', income_annual_max: null, gender: 'All', caste_category: 'All', documents_required: 'Aadhaar, Savings bank account, Mobile number', portal_url: 'https://www.npscra.nsdl.co.in', helpline: '1800-110-069', status: 'Active' },
  { id: 10, scheme_name: 'Indira Gandhi National Old Age Pension (IGNOAPS)', hindi_name: 'इंदिरा गांधी राष्ट्रीय वृद्धावस्था पेंशन', ministry: 'Ministry of Rural Development', category: 'Pension', benefit_amount: 'Rs.200–500/month + state top-up', benefits: 'Monthly central pension assistance for destitute senior citizens living below poverty line.', age_min: 60, age_max: 999, income_limit: 'BPL household', income_annual_max: null, gender: 'All', caste_category: 'All', documents_required: 'Aadhaar, Age proof certificate, BPL card, Bank passbook', portal_url: 'https://nsap.nic.in', helpline: '1800-111-555', status: 'Active' },
  { id: 11, scheme_name: 'Sukanya Samriddhi Yojana (SSY)', hindi_name: 'सुकन्या समृद्धि योजना', ministry: 'Ministry of Finance', category: 'Women & Child', benefit_amount: '~8.2% p.a. interest, tax-free', benefits: 'Government small-deposit savings scheme for girl child education and welfare with maximum tax benefits.', age_min: 0, age_max: 10, income_limit: 'No income limit', income_annual_max: null, gender: 'Female', caste_category: 'All', documents_required: 'Birth certificate of girl child, Guardian Aadhaar & photo', portal_url: 'https://www.india.gov.in', helpline: '1800-266-6868', status: 'Active' },
  { id: 12, scheme_name: 'Pradhan Mantri Matru Vandana Yojana (PMMVY)', hindi_name: 'प्रधानमंत्री मातृ वंदना योजना', ministry: 'Ministry of Women & Child Development', category: 'Women & Child', benefit_amount: 'Rs.5,000 to Rs.6,000 cash transfer', benefits: 'Direct cash maternity incentive to compensate for wage loss and support nutrition during pregnancy.', age_min: 18, age_max: 999, income_limit: 'No limit for eligible mothers', income_annual_max: null, gender: 'Female', caste_category: 'All', documents_required: 'Aadhaar, MCP Card, Bank passbook, Child birth certificate', portal_url: 'https://pmmvy.wcd.gov.in', helpline: '1800-111-555', status: 'Active' },
  { id: 13, scheme_name: 'PM Mudra Yojana (PMMY)', hindi_name: 'प्रधानमंत्री मुद्रा योजना', ministry: 'Ministry of Finance / SIDBI', category: 'Business & Loans', benefit_amount: 'Up to Rs.10 Lakh collateral-free', benefits: 'Micro and small business loans in three tiers: Shishu (Rs.50k), Kishore (Rs.5L), and Tarun (Rs.10L).', age_min: 18, age_max: 65, income_limit: 'Non-farm micro enterprise', income_annual_max: null, gender: 'All', caste_category: 'All', documents_required: 'Aadhaar, PAN, Business proof, 6-month bank statement', portal_url: 'https://www.mudra.org.in', helpline: '1800-180-1111', status: 'Active' },
  { id: 14, scheme_name: 'PM SVANidhi (Street Vendors)', hindi_name: 'पीएम स्वनिधि — स्ट्रीट वेंडर आत्मनिर्भर निधि', ministry: 'Ministry of Housing & Urban Affairs', category: 'Business & Loans', benefit_amount: 'Rs.10,000–50,000 working capital', benefits: 'Affordable working capital credit with 7% interest subsidy and cashback rewards for digital transactions.', age_min: 18, age_max: 999, income_limit: 'Urban street vendors', income_annual_max: null, gender: 'All', caste_category: 'All', documents_required: 'Vending Certificate / ULB letter, Aadhaar, Bank account', portal_url: 'https://pmsvanidhi.mohua.gov.in', helpline: '1800-11-1979', status: 'Active' },
  { id: 15, scheme_name: 'Stand-Up India', hindi_name: 'स्टैंड-अप इंडिया', ministry: 'Ministry of Finance / SIDBI', category: 'Business & Loans', benefit_amount: 'Rs.10 Lakh to Rs.1 Crore loan', benefits: 'Bank loans for establishing greenfield manufacturing, service, or trading units by SC/ST and women founders.', age_min: 18, age_max: 999, income_limit: 'First-time greenfield unit', income_annual_max: null, gender: 'All', caste_category: 'SC / ST / Women ONLY', documents_required: 'Aadhaar, PAN, Caste certificate (if SC/ST), Project report', portal_url: 'https://www.standupmitra.in', helpline: '1800-180-1111', status: 'Active' },
  { id: 16, scheme_name: 'Pradhan Mantri Jan Dhan Yojana (PMJDY)', hindi_name: 'प्रधानमंत्री जन-धन योजना', ministry: 'Ministry of Finance', category: 'Financial Inclusion', benefit_amount: 'Zero-balance account + insurance', benefits: 'Universal banking access with zero balance, RuPay debit card, Rs.2 Lakh accidental cover, and overdraft.', age_min: 10, age_max: 999, income_limit: 'No income limit', income_annual_max: null, gender: 'All', caste_category: 'All', documents_required: 'Aadhaar Card or Voter ID / Officially Valid Document', portal_url: 'https://pmjdy.gov.in', helpline: '1800-11-0001', status: 'Active' },
  { id: 17, scheme_name: 'National Scholarship Portal (NSP)', hindi_name: 'राष्ट्रीय छात्रवृत्ति पोर्टल', ministry: 'Ministry of Electronics & IT', category: 'Education', benefit_amount: 'Rs.1,000–20,000+ per year', benefits: 'Central scholarship hub providing pre-matric, post-matric, and merit-cum-means financial aid.', age_min: 5, age_max: 30, income_limit: 'Family income < Rs.2.5 Lakh/year', income_annual_max: 250000, gender: 'All', caste_category: 'SC/ST/OBC/Minority/General', documents_required: 'Aadhaar, Income certificate, Marksheets, Enrollment proof', portal_url: 'https://scholarships.gov.in', helpline: '0120-6619540', status: 'Active' },
  { id: 18, scheme_name: 'Indira Gandhi National Disability Pension (IGNDPS)', hindi_name: 'इंदिरा गांधी राष्ट्रीय विकलांगता पेंशन', ministry: 'Ministry of Rural Development', category: 'Disability', benefit_amount: 'Rs.300/month + state top-up', benefits: 'Monthly financial assistance for persons aged 18-79 living in BPL households with 80%+ severe disability.', age_min: 18, age_max: 79, income_limit: 'BPL household', income_annual_max: null, gender: 'All', caste_category: 'All', documents_required: 'Aadhaar, Disability certificate (80%+), BPL card, Bank passbook', portal_url: 'https://nsap.nic.in', helpline: '1800-111-555', status: 'Active' },
  { id: 19, scheme_name: 'PM Kaushal Vikas Yojana 4.0 (PMKVY)', hindi_name: 'प्रधानमंत्री कौशल विकास योजना', ministry: 'Ministry of Skill Development', category: 'Skill & Employment', benefit_amount: 'Free training + Rs.8,000 stipend', benefits: 'Free industry-aligned short term technical skill training, assessment certification, and placement.', age_min: 15, age_max: 45, income_limit: 'Family income < Rs.3 Lakh/year', income_annual_max: 300000, gender: 'All', caste_category: 'All', documents_required: 'Aadhaar, Educational certificate, Bank passbook', portal_url: 'https://www.pmkvyofficial.org', helpline: '1800-123-9626', status: 'Active' },
  { id: 20, scheme_name: 'Mahatma Gandhi NREGS (MGNREGA)', hindi_name: 'महात्मा गांधी राष्ट्रीय ग्रामीण रोजगार गारंटी', ministry: 'Ministry of Rural Development', category: 'Skill & Employment', benefit_amount: '100 days guaranteed wage labor', benefits: 'Legal guarantee of at least 100 days of wage employment per financial year for rural adult members.', age_min: 18, age_max: 999, income_limit: 'Rural households', income_annual_max: null, gender: 'All', caste_category: 'All', documents_required: 'Job Card, Aadhaar card, Bank account details', portal_url: 'https://nregs.nic.in', helpline: '1800-111-555', status: 'Active' },
  { id: 21, scheme_name: 'PM Ujjwala Yojana (PMUY)', hindi_name: 'प्रधानमंत्री उज्ज्वला योजना', ministry: 'Ministry of Petroleum & Natural Gas', category: 'Women & Child', benefit_amount: 'Free LPG connection + refill subsidy', benefits: 'Deposit-free clean LPG connection for poor women with safety kit and subsidized first cylinder.', age_min: 18, age_max: 999, income_limit: 'BPL / SECC 2011 criteria', income_annual_max: null, gender: 'Female', caste_category: 'All', documents_required: 'Aadhaar of applicant and family, BPL card, Bank passbook', portal_url: 'https://www.pmuy.gov.in', helpline: '1906', status: 'Active' },
  { id: 22, scheme_name: 'Deen Dayal Upadhyaya Grameen Kaushalya (DDU-GKY)', hindi_name: 'दीन दयाल उपाध्याय ग्रामीण कौशल्य योजना', ministry: 'Ministry of Rural Development', category: 'Skill & Employment', benefit_amount: 'Free residential training + job', benefits: 'Government-funded residential vocational skill training and guaranteed placement (min Rs.6,000/mo).', age_min: 15, age_max: 35, income_limit: 'Rural BPL household', income_annual_max: null, gender: 'All', caste_category: 'All', documents_required: 'Aadhaar, BPL card or MGNREGA Job card, Marksheet', portal_url: 'https://ddugky.gov.in', helpline: '1800-180-6127', status: 'Active' }
];

let activeFilter = 'All';
let searchQuery = '';

function getCategoryBadgeClass(cat) {
  if (!cat) return 'Financial';
  if (cat.includes('Agri')) return 'Agriculture';
  if (cat.includes('Health')) return 'Health';
  if (cat.includes('Hous')) return 'Housing';
  if (cat.includes('Pens')) return 'Pension';
  if (cat.includes('Women')) return 'Women';
  if (cat.includes('Busi')) return 'Business';
  if (cat.includes('Fin')) return 'Financial';
  if (cat.includes('Edu')) return 'Education';
  if (cat.includes('Disab')) return 'Disability';
  if (cat.includes('Skill')) return 'Skill';
  return 'Financial';
}

function buildSchemeCard(s) {
  const ageStr = s.age_max >= 999 ? `${s.age_min}+ yrs / वर्ष` : `${s.age_min}–${s.age_max} yrs / वर्ष`;
  const badgeClass = getCategoryBadgeClass(s.category);
  return `
    <article class="scheme-card">
      <div class="scheme-card-body">
        <span class="badge badge-${badgeClass}">${s.category}</span>
        <h3 class="scheme-name">${s.scheme_name}</h3>
        <p class="scheme-hindi-name">${s.hindi_name || ''}</p>
        <div class="scheme-row"><span class="scheme-row-label" data-en="Benefit" data-hi="लाभ">Benefit</span><span class="scheme-row-value">${s.benefit_amount || '—'}</span></div>
        <div class="scheme-row"><span class="scheme-row-label" data-en="Age" data-hi="आयु">Age</span><span class="scheme-row-value">${ageStr}</span></div>
        <div class="scheme-row"><span class="scheme-row-label" data-en="Income" data-hi="आय सीमा">Income</span><span class="scheme-row-value">${s.income_limit || 'No limit'}</span></div>
        <div class="scheme-row"><span class="scheme-row-label" data-en="Gender" data-hi="लिंग">Gender</span><span class="scheme-row-value">${s.gender === 'All' ? 'All / सभी' : s.gender}</span></div>
      </div>
      <div class="scheme-card-footer">
        <span class="scheme-helpline-label">☎ <strong>${s.helpline || '—'}</strong></span>
        <button class="scheme-detail-btn" onclick="openSchemeModal(${s.id})" data-en="View Details ↗" data-hi="विवरण देखें ↗">View Details ↗</button>
      </div>
    </article>`;
}

function renderSchemes() {
  const grid = document.getElementById('schemeGrid');
  if (!grid) return;
  const q = searchQuery.toLowerCase().trim();
  const filtered = SCHEMES_DATA.filter((s) => {
    if (activeFilter !== 'All' && s.category !== activeFilter) return false;
    if (q) {
      const text = [s.scheme_name, s.hindi_name, s.category, s.benefits, s.benefit_amount, s.ministry].join(' ').toLowerCase();
      if (!text.includes(q)) return false;
    }
    return true;
  });
  const countEl = document.getElementById('resultsCount');
  if (!filtered.length) {
    if (countEl) { countEl.setAttribute('data-en', 'No schemes found'); countEl.setAttribute('data-hi', 'कोई योजना नहीं मिली'); }
    grid.innerHTML = '<p class="empty-state" data-en="No schemes found. Try a different search." data-hi="कोई योजना नहीं मिली। अलग खोज आज़माएं।">No schemes found. Try a different search.</p>';
    if (typeof applyLang === 'function') applyLang(typeof currentLang !== 'undefined' ? currentLang : 'en');
    return;
  }
  grid.innerHTML = filtered.map(buildSchemeCard).join('');
  if (countEl) {
    countEl.setAttribute('data-en', `Showing ${filtered.length} scheme${filtered.length !== 1 ? 's' : ''}`);
    countEl.setAttribute('data-hi', `${filtered.length} योजना${filtered.length !== 1 ? 'एं' : ''} दिखाई जा रही हैं`);
  }
  /* Re-apply language so newly injected data-en/data-hi labels are translated */
  if (typeof applyLang === 'function') applyLang(typeof currentLang !== 'undefined' ? currentLang : 'en');
}

function setSchemeFilter(cat) {
  activeFilter = cat;
  document.querySelectorAll('.filter-btn').forEach((b) => b.classList.toggle('active', b.dataset.filter === cat));
  renderSchemes();
  updateFilterCounts();
}

/** Update filter button text with live counts, and populate category card count badges */
function updateFilterCounts() {
  document.querySelectorAll('.filter-btn[data-filter]').forEach((btn) => {
    const cat = btn.dataset.filter;
    const count = cat === 'All'
      ? SCHEMES_DATA.length
      : SCHEMES_DATA.filter((s) => s.category === cat).length;
    /* Store base label once so repeated calls don't stack brackets */
    if (!btn.dataset.baseEn) btn.dataset.baseEn = btn.getAttribute('data-en') || cat;
    if (!btn.dataset.baseHi) btn.dataset.baseHi = btn.getAttribute('data-hi') || cat;
    btn.setAttribute('data-en', `${btn.dataset.baseEn} (${count})`);
    btn.setAttribute('data-hi', `${btn.dataset.baseHi} (${count})`);
  });
  /* Inject count into category card badges */
  document.querySelectorAll('.category-card[data-category]').forEach((card) => {
    const cat = card.dataset.category;
    const count = SCHEMES_DATA.filter((s) => s.category === cat).length;
    const badge = card.querySelector('.category-count');
    if (badge) badge.textContent = count;
  });
  if (typeof applyLang === 'function') applyLang(typeof currentLang !== 'undefined' ? currentLang : 'en');
}

function onSchemeSearch(e) {
  searchQuery = e.target.value;
  renderSchemes();
}

function openSchemeModal(id) {
  const s = SCHEMES_DATA.find((x) => x.id === id);
  const modal = document.getElementById('schemeModal');
  if (!s || !modal) return;
  const ageStr = s.age_max >= 999 ? `${s.age_min} years and above / ${s.age_min}+ वर्ष` : `${s.age_min} to ${s.age_max} years / वर्ष`;
  modal.querySelector('#modalTitle').textContent = s.scheme_name;
  modal.querySelector('#modalHindi').textContent = s.hindi_name || '';
  modal.querySelector('#modalMinistry').textContent = s.ministry || '—';
  modal.querySelector('#modalCategory').textContent = s.category || '—';
  modal.querySelector('#modalBenefit').textContent = s.benefit_amount || '—';
  modal.querySelector('#modalAge').textContent = ageStr;
  modal.querySelector('#modalIncome').textContent = s.income_limit || 'No income limit';
  modal.querySelector('#modalGender').textContent = s.gender || '—';
  modal.querySelector('#modalCaste').textContent = s.caste_category || 'All';
  modal.querySelector('#modalDocs').textContent = s.documents_required || '—';
  modal.querySelector('#modalBenefits').textContent = s.benefits || '—';
  modal.querySelector('#modalHelpline').textContent = s.helpline || '—';
  const portalLink = modal.querySelector('#modalPortalLink');
  portalLink.href = s.portal_url || '#';
  /* Use data-en/data-hi so lang.js keeps the button label translated — no textContent override */
  portalLink.setAttribute('data-en', 'Apply on Official Portal ↗');
  portalLink.setAttribute('data-hi', 'आधिकारिक पोर्टल पर आवेदन करें ↗');
  if (typeof applyLang === 'function') applyLang(typeof currentLang !== 'undefined' ? currentLang : 'en');
  modal.classList.add('open');
  document.body.style.overflow = 'hidden';
  modal.querySelector('.modal-close').focus();
}

function closeSchemeModal() {
  const modal = document.getElementById('schemeModal');
  if (!modal) return;
  modal.classList.remove('open');
  document.body.style.overflow = '';
}

document.addEventListener('DOMContentLoaded', () => {
  const modal = document.getElementById('schemeModal');
  if (modal) modal.addEventListener('click', (e) => { if (e.target === modal) closeSchemeModal(); });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeSchemeModal(); });
  renderSchemes();
  updateFilterCounts();
});
