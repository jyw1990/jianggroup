/* =========================================================
   JIANG GROUP — Shared JS Utilities
   ========================================================= */

// ── Path resolution for GitHub Pages subpaths ──────────────
const ROOT = (() => {
  // Works both locally and on GitHub Pages at /jianggroup/
  const scripts = document.querySelectorAll('script[src*="main.js"]');
  if (scripts.length) {
    const src = scripts[scripts.length - 1].src;
    return src.replace(/assets\/js\/main\.js.*/, '');
  }
  return '/';
})();

function rootPath(p) {
  return ROOT + p;
}

// ── Fetch JSON data ─────────────────────────────────────────
async function fetchData(filename) {
  const res = await fetch(rootPath('data/' + filename));
  if (!res.ok) throw new Error('Could not load ' + filename);
  return res.json();
}

// ── Navigation ──────────────────────────────────────────────
function initNav() {
  // Logo href
  const logo = document.querySelector('.nav-logo');
  if (logo) logo.href = rootPath('index.html');

  // Active link
  const links = document.querySelectorAll('.nav-links a');
  const current = location.pathname.split('/').filter(Boolean).pop() || 'index.html';
  links.forEach(a => {
    const href = a.getAttribute('href') || '';
    const page = href.split('/').filter(Boolean).pop() || 'index.html';
    if (page === current) a.classList.add('active');
  });

  // Hamburger
  const toggle = document.getElementById('navToggle');
  const navLinks = document.getElementById('navLinks');
  if (toggle && navLinks) {
    toggle.addEventListener('click', () => {
      const open = navLinks.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open);
    });
  }
}

// ── Person photo with fallback ──────────────────────────────
function personPhoto(src, alt, cls) {
  if (!src) {
    return `<div class="placeholder-person ${cls || ''}">👤</div>`;
  }
  return `<img src="${rootPath(src)}" alt="${alt}" onerror="this.parentElement.innerHTML='<div class=\\'placeholder-person\\'>👤</div>'" loading="lazy">`;
}

// ── Generic image with placeholder ─────────────────────────
function researchImgOrPlaceholder(src, alt) {
  if (!src) return `<div class="research-img-placeholder">Image coming soon</div>`;
  return `<img src="${rootPath(src)}" alt="${alt || ''}" onerror="this.style.display='none'" loading="lazy">`;
}

// ── Carousel ────────────────────────────────────────────────
function initCarousel() {
  const track = document.querySelector('.carousel-track');
  const slides = document.querySelectorAll('.carousel-slide');
  const dotsContainer = document.querySelector('.carousel-dots');
  if (!track || !slides.length) return;

  let current = 0;
  const total = slides.length;

  // Build dots
  const dots = [];
  slides.forEach((_, i) => {
    const d = document.createElement('button');
    d.className = 'carousel-dot' + (i === 0 ? ' active' : '');
    d.setAttribute('aria-label', 'Go to slide ' + (i + 1));
    d.addEventListener('click', () => goTo(i));
    dotsContainer.appendChild(d);
    dots.push(d);
  });

  function goTo(index) {
    current = (index + total) % total;
    track.style.transform = `translateX(-${current * 100}%)`;
    dots.forEach((d, i) => d.classList.toggle('active', i === current));
  }

  document.querySelector('.carousel-prev')?.addEventListener('click', () => goTo(current - 1));
  document.querySelector('.carousel-next')?.addEventListener('click', () => goTo(current + 1));

  // Auto-advance every 5 seconds
  let timer = setInterval(() => goTo(current + 1), 5000);
  track.closest('.carousel').addEventListener('mouseenter', () => clearInterval(timer));
  track.closest('.carousel').addEventListener('mouseleave', () => {
    timer = setInterval(() => goTo(current + 1), 5000);
  });
}

// ── Footer ──────────────────────────────────────────────────
function renderFooter() {
  const year = new Date().getFullYear();
  const footer = document.querySelector('.site-footer');
  if (footer) footer.innerHTML = `© ${year} by Yuanwen Jiang. All rights reserved.`;
}

// ── Init on DOM ready ───────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  initNav();
  renderFooter();
});
