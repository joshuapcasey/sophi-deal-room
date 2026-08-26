/* Deal-room top strip + gate check for the original landing/market/portfolio pages.
   Inserts a sticky nav at document.body top, and redirects to gate if access not granted. */
(function () {
  // Gate check (session-scoped)
  try {
    let ok = false;
    try { ok = window.sessionStorage.getItem('deal_room_ok') === '1'; } catch (e) {}
    if (!ok && window.name === 'DEAL_ROOM_OK') ok = true;
    if (!ok) {
      window.location.replace('./index.html');
      return;
    }
  } catch (e) {}

  const active = (location.pathname.split('/').pop() || 'rollup.html').toLowerCase();

  const CSS = `
  .dr-topstrip {
    position: sticky; top: 0; z-index: 500;
    background: #0e1013;
    border-bottom: 1px solid rgba(255,255,255,0.08);
    padding: 10px 32px;
    display: flex; align-items: center; justify-content: space-between;
    font-family: 'Inter', sans-serif;
    font-size: 13px;
  }
  .dr-topstrip .dr-brand { display: flex; align-items: center; gap: 10px; color: #e8e6e0; font-weight: 500; }
  .dr-topstrip .dr-brand-mark { width: 22px; height: 22px; border-radius: 5px; background: linear-gradient(135deg,#d4a24c,#a67c3a); display: grid; place-items: center; color: #14171c; font-family: 'Fraunces', 'Georgia', serif; font-weight: 700; font-size: 13px; }
  .dr-topstrip .dr-brand-sub { color: #6b6f78; font-size: 11px; text-transform: uppercase; letter-spacing: 0.08em; margin-left: 4px; }
  .dr-topstrip nav { display: flex; align-items: center; gap: 4px; }
  .dr-topstrip nav a { padding: 6px 12px; border-radius: 6px; color: #a0a4ad; text-decoration: none; transition: all 140ms ease; font-weight: 500; }
  .dr-topstrip nav a:hover { color: #e8e6e0; background: rgba(255,255,255,0.05); }
  .dr-topstrip nav a.active { color: #d4a24c; background: rgba(212,162,76,0.1); }
  @media (max-width: 720px) {
    .dr-topstrip { padding: 8px 12px; font-size: 12px; }
    .dr-topstrip nav { gap: 0; overflow-x: auto; }
    .dr-topstrip nav a { padding: 6px 8px; white-space: nowrap; }
  }
  /* Market view has fixed header — push topstrip above it */
  body.market-view .dr-topstrip { position: sticky; top: 0; }
  body.market-view #header { top: 45px; }
  body.market-view #sidebar { top: 45px; height: calc(100vh - 45px); }
  body.market-view #map { top: 45px; height: calc(100vh - 45px); }
  `;

  const NAV = [
    ['rollup.html',        'Rollup'],
    ['growth-engine.html', 'Growth Engine'],
    ['portfolio.html',     'Portfolio'],
    ['market.html',        'Markets Map'],
    ['methodology.html',   'Methodology'],
    ['accounts.html',      'Accounts'],
    ['levers.html',        'Acquisition'],
    ['downloads.html',     'Data Room'],
  ];

  const links = NAV.map(([href, label]) => {
    const isActive = href === active;
    return `<a href="./${href}"${isActive ? ' class="active"' : ''}>${label}</a>`;
  }).join('');

  const strip = document.createElement('div');
  strip.className = 'dr-topstrip';
  strip.innerHTML = `
    <div class="dr-brand">
      <div class="dr-brand-mark">S</div>
      <span>Sophi Investor Deal Room</span>
      <span class="dr-brand-sub">2026 · v3</span>
    </div>
    <nav>${links}</nav>
  `;

  const style = document.createElement('style');
  style.textContent = CSS;
  document.head.appendChild(style);

  // Insert at top of body
  function mount() {
    document.body.insertBefore(strip, document.body.firstChild);
  }
  if (document.body) mount();
  else document.addEventListener('DOMContentLoaded', mount);
})();
