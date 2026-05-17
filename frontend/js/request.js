/* request.js — Repair request form logic */

const form       = document.getElementById('request-form');
const submitBtn  = document.getElementById('submit-btn');
const addressRow = document.getElementById('address-row');
const modalOverlay = document.getElementById('success-modal');
const tidDisplay   = document.getElementById('tracking-id-value');
const copyBtn      = document.getElementById('copy-tid');
const closeModal   = document.getElementById('close-modal');

// Toggle address field based on service type
document.querySelectorAll('input[name="service_type"]').forEach(radio => {
  radio.addEventListener('change', () => {
    if (addressRow) {
      addressRow.style.display = radio.value === 'Home Service' ? 'flex' : 'none';
      const addrInput = document.getElementById('address');
      if (addrInput) addrInput.required = (radio.value === 'Home Service');
    }
  });
});

// Form submission
if (form) {
  form.addEventListener('submit', async e => {
    e.preventDefault();
    clearErrors();

    const fd = new FormData(form);
    const data = {
      name:                fd.get('name').trim(),
      phone:               fd.get('phone').trim(),
      address:             fd.get('address')?.trim() || '',
      appliance_type:      fd.get('appliance_type'),
      appliance_brand:     fd.get('appliance_brand')?.trim() || '',
      problem_description: fd.get('problem_description').trim(),
      service_type:        fd.get('service_type'),
    };

    // Basic client-side validation
    let valid = true;
    if (!data.name)                { showErr('err-name',    'Name is required.'); valid = false; }
    if (!data.phone)               { showErr('err-phone',   'Phone is required.'); valid = false; }
    if (!data.appliance_type)      { showErr('err-appliance','Select an appliance type.'); valid = false; }
    if (!data.problem_description) { showErr('err-problem', 'Describe the problem.'); valid = false; }
    if (!data.service_type)        { showErr('err-service', 'Choose a service type.'); valid = false; }
    if (data.service_type === 'Home Service' && !data.address) {
      showErr('err-address', 'Address is required for Home Service.'); valid = false;
    }
    if (!valid) return;

    submitBtn.disabled = true;
    submitBtn.textContent = 'Submitting…';

    try {
      const res = await fetch('/api/request', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
        credentials: 'include'
      });
      const json = await res.json();

      if (json.success) {
        tidDisplay.textContent = json.tracking_id;
        modalOverlay.classList.add('show');
        form.reset();
        if (addressRow) addressRow.style.display = 'none';
      } else {
        window.showToast('Submission Failed', json.error || 'Please try again.', 'error');
      }
    } catch {
      window.showToast('Network Error', 'Could not reach the server.', 'error');
    } finally {
      submitBtn.disabled = false;
      submitBtn.textContent = 'Submit Repair Request';
    }
  });
}

// Copy tracking ID
if (copyBtn) {
  copyBtn.addEventListener('click', () => {
    navigator.clipboard.writeText(tidDisplay.textContent);
    copyBtn.textContent = '✅ Copied!';
    setTimeout(() => copyBtn.textContent = '📋 Copy ID', 1800);
  });
}
if (tidDisplay) {
  tidDisplay.addEventListener('click', () => {
    navigator.clipboard.writeText(tidDisplay.textContent);
    window.showToast('Copied!', 'Tracking ID copied to clipboard.', 'success');
  });
}
if (closeModal) {
  closeModal.addEventListener('click', () => modalOverlay.classList.remove('show'));
}
if (modalOverlay) {
  modalOverlay.addEventListener('click', e => {
    if (e.target === modalOverlay) modalOverlay.classList.remove('show');
  });
}

function showErr(id, msg) {
  const el = document.getElementById(id);
  if (el) { el.textContent = msg; el.style.display = 'block'; }
}
function clearErrors() {
  document.querySelectorAll('.form-error').forEach(e => { e.style.display = 'none'; e.textContent = ''; });
}
