/**
 * checker.js — JanMitra Citizen Portal
 * 4-step eligibility wizard (UI only — Phase 1).
 * Phase 2 will POST collected data to /api/match.
 *
 * Steps:
 *   1. Age
 *   2. Annual Income
 *   3. Gender
 *   4. Category (interest area)
 *
 * On completion the wizard filters SCHEMES_DATA locally and shows matched cards.
 */

'use strict';

/** Current active wizard step (1-indexed) */
let wizardStep = 1;
const TOTAL_STEPS = 4;

/** Collected form values */
const wizardData = {
  age: null,
  income_annual: null,
  gender: '',
  category: '',
};

/**
 * Navigate to a specific step.
 * Updates progress bar dots, lines, and shows the correct panel.
 *
 * @param {number} step - 1 to TOTAL_STEPS
 */
function goToStep(step) {
  if (step < 1 || step > TOTAL_STEPS) return;
  wizardStep = step;

  // Update step panel visibility
  document.querySelectorAll('.wizard-step-panel').forEach((panel, idx) => {
    panel.classList.toggle('active', idx + 1 === step);
  });

  // Update progress dots
  document.querySelectorAll('.wizard-step-dot').forEach((dot, idx) => {
    const dotStep = idx + 1;
    dot.classList.remove('active', 'done');
    if (dotStep < step)  dot.classList.add('done');
    if (dotStep === step) dot.classList.add('active');
  });

  // Update connector lines
  document.querySelectorAll('.wizard-step-line').forEach((line, idx) => {
    // Line at index i connects dot i+1 to dot i+2
    line.classList.toggle('done', idx + 1 < step);
  });

  // Update Back button visibility
  const backBtn = document.getElementById('wizardBackBtn');
  if (backBtn) backBtn.style.display = step > 1 ? 'inline-flex' : 'none';

  // Update Next/Submit button label
  const nextBtn = document.getElementById('wizardNextBtn');
  if (nextBtn) {
    if (step === TOTAL_STEPS) {
      nextBtn.setAttribute('data-en', 'Find My Schemes →');
      nextBtn.setAttribute('data-hi', 'योजनाएं खोजें →');
    } else {
      nextBtn.setAttribute('data-en', 'Next →');
      nextBtn.setAttribute('data-hi', 'अगला →');
    }
    /* Re-apply current language so the button label updates immediately */
    if (typeof applyLang === 'function') applyLang(typeof currentLang !== 'undefined' ? currentLang : 'en');
  }

  // Clear any error
  clearWizardError();

  // Focus the first input in the new panel (accessibility)
  const activePanel = document.querySelector('.wizard-step-panel.active');
  if (activePanel) {
    const firstInput = activePanel.querySelector('input, select');
    if (firstInput) firstInput.focus();
  }
}

/**
 * Validate the current step's input.
 * Returns true if valid; shows an error and returns false if not.
 *
 * @returns {boolean}
 */
function validateCurrentStep() {
  switch (wizardStep) {
    case 1: {
      const val = parseInt(document.getElementById('wizardAge').value, 10);
      if (!val || val < 1 || val > 120) {
        showWizardError('Please enter a valid age between 1 and 120. / कृपया 1-120 के बीच आयु दर्ज करें।');
        return false;
      }
      wizardData.age = val;
      return true;
    }
    case 2: {
      const raw = document.getElementById('wizardIncome').value.trim();
      // Income is optional — empty means "not provided / no limit"
      if (raw === '') {
        wizardData.income_annual = null;
        return true;
      }
      const val = parseInt(raw, 10);
      if (isNaN(val) || val < 0) {
        showWizardError('Please enter a valid annual income (or leave blank). / कृपया वार्षिक आय दर्ज करें।');
        return false;
      }
      wizardData.income_annual = val;
      return true;
    }
    case 3: {
      wizardData.gender = document.getElementById('wizardGender').value;
      return true; // gender is always valid (dropdown has defaults)
    }
    case 4: {
      wizardData.category = document.getElementById('wizardCategory').value;
      return true; // category is optional
    }
    default:
      return true;
  }
}

/**
 * Show an error message below the current step's form field.
 * @param {string} msg
 */
function showWizardError(msg) {
  const errEl = document.getElementById('wizardError');
  if (!errEl) return;
  errEl.textContent = msg;
  errEl.style.display = 'block';
}

/** Clear the wizard error message. */
function clearWizardError() {
  const errEl = document.getElementById('wizardError');
  if (!errEl) return;
  errEl.textContent = '';
  errEl.style.display = 'none';
}

/**
 * Advance to the next step, or submit on the last step.
 * Validates before proceeding.
 */
function wizardNext() {
  if (!validateCurrentStep()) return;

  if (wizardStep < TOTAL_STEPS) {
    goToStep(wizardStep + 1);
  } else {
    submitWizard();
  }
}

/** Go back one step. */
function wizardBack() {
  if (wizardStep > 1) goToStep(wizardStep - 1);
}

/**
 * Run the local eligibility filter against SCHEMES_DATA and display results.
 * Phase 2: replace this with a POST to /api/match.
 */
function submitWizard() {
  const { age, income_annual, gender, category } = wizardData;

  /* Eligibility logic (mirrors matching.py from ARCHITECTURE.md):
   *   age >= scheme.age_min
   *   AND age <= scheme.age_max (999 = no upper limit)
   *   AND (income_annual <= scheme.income_annual_max OR income_annual_max IS NULL)
   *   AND (scheme.gender = "All" OR scheme.gender = requested gender)
   *   AND (category is blank OR scheme.category = requested category)
   */
  const matched = SCHEMES_DATA.filter((s) => {
    if (age !== null) {
      if (age < s.age_min) return false;
      if (s.age_max < 999 && age > s.age_max) return false;
    }
    if (income_annual !== null && s.income_annual_max !== null) {
      if (income_annual > s.income_annual_max) return false;
    }
    if (gender && s.gender !== 'All' && s.gender !== gender) return false;
    if (category && s.category !== category) return false;
    return true;
  });

  showWizardResults(matched);
}

/**
 * Render matched schemes in the wizard results area.
 * @param {Array<Object>} schemes
 */
function showWizardResults(schemes) {
  const resultsSection = document.getElementById('wizardResults');
  const countLine = document.getElementById('wizardResultCount');
  const grid = document.getElementById('wizardResultGrid');

  if (!resultsSection || !countLine || !grid) return;

  if (schemes.length === 0) {
    countLine.textContent =
      'No schemes matched your profile. Try broadening your criteria, or call the helpline.';
    countLine.textContent +=
      ' / कोई योजना नहीं मिली। श्रेणी खुली रखें या हेल्पलाइन पर कॉल करें।';
    grid.innerHTML = '';
  } else {
    countLine.textContent =
      `${schemes.length} scheme${schemes.length !== 1 ? 's' : ''} may match your profile. ` +
      `Please verify your eligibility on the official portal before applying. ` +
      `/ ${schemes.length} योजना${schemes.length !== 1 ? 'एं' : ''} आपके लिए उपयुक्त हो सकती हैं।`;

    // Reuse buildSchemeCard from schemes.js
    grid.innerHTML = schemes.map((s) => buildSchemeCard(s)).join('');
  }

  resultsSection.style.display = 'block';
  resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/**
 * Reset the wizard to step 1 and clear results.
 */
function resetWizard() {
  wizardData.age = null;
  wizardData.income_annual = null;
  wizardData.gender = '';
  wizardData.category = '';

  // Clear inputs
  const ageInput = document.getElementById('wizardAge');
  const incomeInput = document.getElementById('wizardIncome');
  const genderSelect = document.getElementById('wizardGender');
  const catSelect = document.getElementById('wizardCategory');
  if (ageInput)    ageInput.value = '';
  if (incomeInput) incomeInput.value = '';
  if (genderSelect) genderSelect.value = '';
  if (catSelect)   catSelect.value = '';

  // Hide results
  const resultsSection = document.getElementById('wizardResults');
  if (resultsSection) resultsSection.style.display = 'none';

  goToStep(1);
  /* Re-apply language after reset so button labels are translated */
  if (typeof applyLang === 'function') applyLang(typeof currentLang !== 'undefined' ? currentLang : 'en');
}

/** Allow pressing Enter to advance wizard steps. */
function wizardKeyHandler(e) {
  if (e.key === 'Enter') {
    e.preventDefault();
    wizardNext();
  }
}

// Initialise wizard on DOM ready
document.addEventListener('DOMContentLoaded', () => {
  goToStep(1);

  // Attach keyboard handler to all wizard inputs
  document.querySelectorAll('.wizard-input, .wizard-select').forEach((el) => {
    el.addEventListener('keydown', wizardKeyHandler);
  });
});

