/* main.js — Global JS: nav, scroll animations, toast */

// ── Mobile Nav ───────────────────────────────────────────────
const navToggle = document.querySelector('.nav-toggle');
const navLinks  = document.querySelector('.nav-links');
if (navToggle && navLinks) {
  navToggle.addEventListener('click', () => {
    navLinks.classList.toggle('open');
    navToggle.textContent = navLinks.classList.contains('open') ? '✕' : '☰';
  });
  document.addEventListener('click', e => {
    if (!navToggle.contains(e.target) && !navLinks.contains(e.target)) {
      navLinks.classList.remove('open');
      navToggle.textContent = '☰';
    }
  });
}

// ── Active Nav Link ─────────────────────────────────────────
(function markActive() {
  const path = window.location.pathname.replace(/\/$/, '') || '/index.html';
  document.querySelectorAll('.nav-links a').forEach(a => {
    const href = a.getAttribute('href') || '';
    if (href && path.endsWith(href.replace(/^\//, ''))) {
      a.classList.add('active');
    }
  });
})();

// ── Scroll Reveal ───────────────────────────────────────────
const observer = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.style.opacity = '1';
      e.target.style.transform = 'translateY(0)';
    }
  });
}, { threshold: 0.12 });

document.querySelectorAll('.card, .service-card, .step-card, .contact-card').forEach(el => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(28px)';
  el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
  observer.observe(el);
});

// ── Toast ────────────────────────────────────────────────────
function showToast(title, message, type = 'success') {
  let toast = document.getElementById('global-toast');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'global-toast';
    toast.className = 'toast';
    toast.innerHTML = `
      <span class="toast-icon"></span>
      <div class="toast-body"><h4></h4><p></p></div>`;
    document.body.appendChild(toast);
  }
  toast.querySelector('.toast-icon').textContent = type === 'success' ? '✅' : '❌';
  toast.querySelector('h4').textContent = title;
  toast.querySelector('p').textContent  = message;
  toast.className = `toast toast-${type}`;
  setTimeout(() => toast.classList.add('show'), 10);
  setTimeout(() => toast.classList.remove('show'), 4000);
}

// expose globally
window.showToast = showToast;
