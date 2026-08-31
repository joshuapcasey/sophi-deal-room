/* Shared shell: sidebar nav injection + active-page highlight */
(function () {
  const NAV = [
    { group: 'OVERVIEW', items: [
      { href: 'summary.html', label: 'Summary', icon: 'sparkle' },
      { href: 'capital-strategy.html', label: 'Capital Strategy', icon: 'split' },
    ]},
    { group: 'THE OPPORTUNITY', items: [
      { href: 'company-history.html', label: 'Company History', icon: 'clock' },
      { href: 'sophi-os.html', label: 'SOPHI OS', icon: 'layers' },
      { href: 'competition.html', label: 'Competition', icon: 'crosshair' },
      { href: 'growth-model.html', label: 'Growth Model', icon: 'trending' },
    ]},
    { group: 'THE DEAL', items: [
      { href: 'financial-performance.html', label: 'Financial Performance', icon: 'chart' },
      { href: 'use-of-funds.html', label: 'Use of Funds', icon: 'coins' },
      { href: 'v3-valuation.html', label: 'Valuation', icon: 'rocket' },
      { href: 'risk-milestones.html', label: 'Risk Mitigating Milestones', icon: 'shield' },
    ]},
    { group: 'ADVISOR WORKING FILE', items: [
      { href: 'advisor-questions.html', label: 'Advisor Questions', icon: 'help' },
      { href: 'methodology.html', label: 'Methodology', icon: 'book' },
      { href: 'downloads.html', label: 'Documents', icon: 'folder', badge: 14 },
    ]},
  ];

  // Rendered separately, pinned to the footer just above the viewer chip
  const FOOTER_ITEM = { href: 'your-access.html', label: 'Your Access', icon: 'key' };

  const ICONS = {
    sparkle: '<path d="M12 3l1.6 4.6L18 9l-4.4 1.4L12 15l-1.6-4.6L6 9l4.4-1.4L12 3zM19 15l.8 2.2L22 18l-2.2.8L19 21l-.8-2.2L16 18l2.2-.8L19 15z" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>',
    clock: '<circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M12 7v5l3 2" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>',
    layers: '<path d="M12 3l9 5-9 5-9-5 9-5zM3 13l9 5 9-5M3 17l9 5 9-5" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>',
    trending: '<path d="M3 17l6-6 4 4 8-8M15 7h6v6" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>',
    chart: '<path d="M3 21V5M3 21h18M7 17V11M11 17V8M15 17v-4M19 17V6" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>',
    shield: '<path d="M12 3l8 3v6c0 5-3.5 8.5-8 9-4.5-.5-8-4-8-9V6l8-3z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>',
    file: '<path d="M6 3h9l4 4v14H6V3zM14 3v5h5" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>',
    folder: '<path d="M3 6.5A1.5 1.5 0 0 1 4.5 5h4L11 7h8.5A1.5 1.5 0 0 1 21 8.5v10a1.5 1.5 0 0 1-1.5 1.5h-15A1.5 1.5 0 0 1 3 18.5v-12z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>',
    chat: '<path d="M4 5h16v11H8l-4 4V5z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>',
    key: '<circle cx="7.5" cy="14.5" r="3.5" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M10 12l9-9M15.5 5.5l2 2M13 8l2 2" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>',
    book: '<path d="M4 4h6a3 3 0 0 1 3 3v14a2 2 0 0 0-2-2H4V4zM20 4h-6a3 3 0 0 0-3 3v14a2 2 0 0 1 2-2h7V4z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>',
    seedling: '<path d="M12 20v-6M12 14c0-3 2-6 6-6-.5 3-2.5 6-6 6zM12 14c0-3-2-6-6-6 .5 3 2.5 6 6 6z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>',
    rocket: '<path d="M12 3c3 2 5 5.5 5 9v4l-2 2h-6l-2-2v-4c0-3.5 2-7 5-9zM9 20l-1 2M15 20l1 2M12 20v2M8 12H5l-1 5 4-2M16 12h3l1 5-4-2" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/><circle cx="12" cy="10" r="1.5" fill="none" stroke="currentColor" stroke-width="1.6"/>',
    grid: '<path d="M3 3h7v7H3zM14 3h7v7h-7zM3 14h7v7H3zM14 14h7v7h-7z" fill="none" stroke="currentColor" stroke-width="1.6"/>',
    coins: '<circle cx="8" cy="8" r="5" fill="none" stroke="currentColor" stroke-width="1.6"/><circle cx="15" cy="15" r="5" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M8 5v6M6 8h4M15 12v6M13 15h4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>',
    wallet: '<path d="M3 7a2 2 0 0 1 2-2h14v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V7z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><path d="M3 10h18M17 15h.01" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>',
    crosshair: '<circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="1.6"/><circle cx="12" cy="12" r="3" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M12 3v3M12 18v3M3 12h3M18 12h3" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>',
    split: '<path d="M6 3v6a3 3 0 0 0 3 3h6a3 3 0 0 1 3 3v6M6 21v-6" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/><circle cx="6" cy="3" r="1.5" fill="currentColor"/><circle cx="18" cy="21" r="1.5" fill="currentColor"/><circle cx="6" cy="21" r="1.5" fill="currentColor"/>',
    help: '<circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M9.5 9a2.5 2.5 0 0 1 5 0c0 1.5-2.5 2-2.5 3.5M12 16.5h.01" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>',
  };

  function esc(str) {
    return String(str).replace(/[&<>"']/g, ch => ({
      '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'
    }[ch]));
  }

  function ensureAccess() {
    try {
      let ok = false;
      try { ok = window.sessionStorage.getItem('deal_room_ok') === '1'; } catch (e) {}
      if (!ok && window.name === 'DEAL_ROOM_OK') ok = true;
      if (!ok) {
        window.location.replace('./index.html');
        return false;
      }
    } catch (e) {}
    return true;
  }

  function renderNav(activeHref) {
    const groups = NAV.map(g => {
      const items = g.items.map(it => {
        const active = it.href === activeHref;
        const icon = ICONS[it.icon] || '';
        const badge = it.badge != null ? `<span class="nav-badge">${it.badge}</span>` : '';
        return `<a href="./${it.href}" class="nav-item ${active ? 'active' : ''}" data-testid="nav-${it.icon}">
          <svg width="18" height="18" viewBox="0 0 24 24">${icon}</svg>
          <span class="nav-label">${esc(it.label)}</span>
          ${badge}
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
          <div class="brand-name">SOPHI</div>
          <div class="brand-sub">ADVISOR WORKING FILE · 2026</div>
        </div>
      </div>
      ${groups}
      <div class="nav-footer">
        <a href="./${FOOTER_ITEM.href}" class="nav-item ${FOOTER_ITEM.href === activeHref ? 'active' : ''}" data-testid="nav-${FOOTER_ITEM.icon}" style="margin-bottom: 12px;">
          <svg width="18" height="18" viewBox="0 0 24 24">${ICONS[FOOTER_ITEM.icon] || ''}</svg>
          <span class="nav-label">${esc(FOOTER_ITEM.label)}</span>
        </a>
        <div class="viewer-chip">
          <span class="viewer-avatar">CFO</span>
          <span class="viewer-meta">
            <span class="viewer-email">advisor@sophimobility.com</span>
            <span class="viewer-role">CFO / Business advisor</span>
          </span>
        </div>
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
