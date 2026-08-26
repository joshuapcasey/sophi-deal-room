/* Shared shell: sidebar nav injection + active-page highlight */
(function () {
  const NAV = [
    { group: 'DEAL ROOM', items: [
      { href: 'rollup.html', label: '6-Market Rollup', icon: 'grid' },
      { href: 'growth-engine.html', label: 'Growth Engine', icon: 'trending' },
      { href: 'market.html', label: 'Markets Map', icon: 'map' },
      { href: 'portfolio.html', label: 'Portfolio Detail', icon: 'grid' },
    ]},
    { group: 'DILIGENCE', items: [
      { href: 'methodology.html', label: 'Methodology', icon: 'book' },
      { href: 'levers.html', label: 'Acquisition Levers', icon: 'target' },
    ]},
    { group: 'DOWNLOADS', items: [
      { href: 'downloads.html', label: 'Data Room', icon: 'download' },
    ]},
  ];

  const ICONS = {
    grid: '<path d="M3 3h7v7H3zM14 3h7v7h-7zM3 14h7v7H3zM14 14h7v7h-7z" fill="none" stroke="currentColor" stroke-width="1.6"/>',
    trending: '<path d="M3 17l6-6 4 4 8-8M15 7h6v6" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>',
    map: '<path d="M9 3L3 5v16l6-2 6 2 6-2V3l-6 2-6-2zM9 3v16M15 5v16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>',
    book: '<path d="M4 4h6a3 3 0 0 1 3 3v14a2 2 0 0 0-2-2H4V4zM20 4h-6a3 3 0 0 0-3 3v14a2 2 0 0 1 2-2h7V4z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>',
    table: '<path d="M3 5h18v14H3zM3 10h18M3 15h18M9 5v14M15 5v14" fill="none" stroke="currentColor" stroke-width="1.6"/>',
    target: '<circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="1.6"/><circle cx="12" cy="12" r="5" fill="none" stroke="currentColor" stroke-width="1.6"/><circle cx="12" cy="12" r="1.5" fill="currentColor"/>',
    download: '<path d="M12 4v12m-5-5l5 5 5-5M4 20h16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>',
    lock: '<rect x="5" y="11" width="14" height="10" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M8 11V7a4 4 0 0 1 8 0v4" fill="none" stroke="currentColor" stroke-width="1.6"/>',
  };

  function esc(str) {
    return String(str).replace(/[&<>"']/g, ch => ({
      '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'
    }[ch]));
  }

  function ensureAccess() {
    // Check gate; if not accepted, redirect to gate.
    try {
      let ok = false;
      try { ok = window.sessionStorage.getItem('deal_room_ok') === '1'; } catch (e) {}
      if (!ok && window.name === 'DEAL_ROOM_OK') ok = true;
      if (!ok) {
        window.location.replace('./index.html');
        return false;
      }
    } catch (e) { /* be permissive if storage blocked */ }
    return true;
  }

  function renderNav(activeHref) {
    const groups = NAV.map(g => {
      const items = g.items.map(it => {
        const active = it.href === activeHref;
        const icon = ICONS[it.icon] || '';
        return `<a href="./${it.href}" class="nav-item ${active ? 'active' : ''}" data-testid="nav-${it.icon}">
          <svg width="18" height="18" viewBox="0 0 24 24">${icon}</svg>
          <span>${esc(it.label)}</span>
        </a>`;
      }).join('');
      return `<div class="nav-group">
        <div class="nav-group-label">${esc(g.group)}</div>
        ${items}
      </div>`;
    }).join('');

    return `
      <div class="brand">
        <div class="mark">S</div>
        <div class="brand-text">
          <div class="brand-name">Sophi Mobility</div>
          <div class="brand-sub">Investor Deal Room · 2026</div>
        </div>
      </div>
      ${groups}
      <div class="nav-footer">
        <div>Built ${new Date().toLocaleDateString('en-US', { month:'short', day:'numeric', year:'numeric' })}</div>
        <div>v3 · 6-market model</div>
      </div>
    `;
  }

  window.SOPHI_SHELL = {
    mount(activeHref) {
      if (!ensureAccess()) return;
      const nav = document.getElementById('side-nav');
      if (nav) nav.innerHTML = renderNav(activeHref);
    },
    grantAccess() {
      try { window.sessionStorage?.setItem('deal_room_ok', '1'); } catch (e) {}
      window.name = 'DEAL_ROOM_OK';
    },
  };
})();
