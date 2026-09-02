/* Sophi Mobility — market view (v3 penetration engine) */
(function() {
  'use strict';
  const DATA = window.SOPHI_DATA_V3_1 || window.SOPHI_DATA;
  if (!DATA) { console.error('SOPHI_DATA missing'); return; }

  const MARKET_ORDER = ['charlotte', 'indianapolis', 'denver', 'houston', 'detroit', 'south_bend'];

  // Defensive: hide any market tagged Expansion Growth Model from the map view.
  function isAcquisitionMarket(mkt) {
    return mkt && mkt.growth_model !== 'expansion';
  }

  const POOL_LABEL = {
    anchor:        'Anchor',
    cold_sam:      'Cold SAM',
    ma_sam:        'M&A SAM',
    partnership:   'Partnership / PMC',
    enterprise:    'Enterprise operator',
    extended_stay: 'Extended-stay brand',
    micro:         'Micro (<$150K TAM)',
  };
  const IN_SAM_POOLS = new Set(['anchor', 'cold_sam', 'ma_sam']);

  const V7_LABEL = {
    hometown_displaced:  { label: 'Indy v7 — Hometown Displaced', cls: 'positive', detail: 'Re-classified into Cold SAM via hometown advantage (Denison/Severin legacy + co-located dependency).' },
    hometown_was_boost:  { label: 'Indy v7 — Hometown +0.5 WAS', cls: 'positive', detail: 'Denison-era goodwill applies a +0.5 WAS lift on this account.' },
    ma_absorption:       { label: 'Indy v7 — M&A Absorption',   cls: 'neutral',  detail: 'Carry-in revenue from acquired hometown operator (Denison roll-in). $0.95M/yr Y2-Y5 portfolio contribution.' },
  };

  // ---- Resolve active market from ?m= query param -------------------------
  const params = new URLSearchParams(location.search);
  let mKey = (params.get('m') || 'charlotte').toLowerCase();
  if (!DATA.markets[mKey] || !isAcquisitionMarket(DATA.markets[mKey])) mKey = 'charlotte';
  const market = DATA.markets[mKey];
  const accounts = market.accounts;
  const summary = market.summary;

  // ---- Quartile assignment (absolute TAM bands, market-agnostic) ---------
  // Quartile 1: >$500K · Q2: $250-500K · Q3: $100-250K · Q4: <$100K
  function assignQuartile(tam) {
    const t = Number(tam) || 0;
    if (t > 500000) return 1;
    if (t > 250000) return 2;
    if (t > 100000) return 3;
    return 4;
  }
  accounts.forEach(a => {
    a._quartile = assignQuartile(a.tam);
    a._signYear = a.acquisition_year || 0; // 0 = unacquired by Y5
    // rank within quartile (for chip sizing) — 1..N by TAM desc
  });
  // Rank within each quartile for market view chip sizing
  [1,2,3,4].forEach(q => {
    const bucket = accounts.filter(a => a._quartile === q)
                           .sort((a,b) => (b.tam||0) - (a.tam||0));
    bucket.forEach((a, i) => { a._quartileRank = i / Math.max(bucket.length - 1, 1); });
  });
  // Rank within each sign year by revenue contribution (for portfolio chip sizing)
  [1,2,3,4,5].forEach(y => {
    const bucket = accounts.filter(a => a._signYear === y)
                           .sort((a,b) => (b.y5||0) - (a.y5||0));
    bucket.forEach((a, i) => { a._yearRank = i / Math.max(bucket.length - 1, 1); });
  });
  accounts.filter(a => a._signYear === 0).forEach(a => { a._yearRank = 1; });

  // ---- Derived market KPIs ------------------------------------------------
  const acquired = accounts.filter(a => a._signYear > 0);
  const nWins = acquired.length;
  const totalY5 = acquired.reduce((s,a) => s + (Number(a.y5)||0), 0);
  const avgY5 = nWins > 0 ? totalY5 / nWins : 0;

  // ---- Header / summary ---------------------------------------------------
  document.title = `${market.name} — Sophi Mobility Market Map`;
  document.getElementById('page-title').textContent = `${market.name} — Sophi Mobility`;
  document.getElementById('market-name').textContent = market.name;
  document.getElementById('market-subtitle').textContent =
    `Sophi Mobility · ${summary.n_accounts} accounts · ${summary.n_in_sam} in SAM`;

  document.getElementById('h-tam').textContent = '$' + fmtM(summary.tam);
  document.getElementById('h-sam').textContent = '$' + fmtM(summary.sam);
  document.getElementById('h-sam-ratio').textContent =
    `(${(summary.sam_tam_ratio * 100).toFixed(0)}% of TAM)`;
  document.getElementById('h-y5').textContent = '$' + fmtM(summary.y5_som);
  document.getElementById('h-y5-ratio').textContent =
    `(${(summary.y5_tam_ratio * 100).toFixed(0)}% of TAM)`;
  document.getElementById('h-wins').textContent = nWins;
  document.getElementById('h-avg').textContent = '$' + fmtM(avgY5);

  // v3: market cap badge
  const cap = market.cap;
  const nAcquired = market.n_acquired || 0;
  const stateBadge = document.getElementById('state-badge');
  const capLabel = cap ? ` · ${(cap*100).toFixed(0)}% Y5 cap` : '';
  if (summary.state === 'WARM') {
    stateBadge.textContent = `Warm · 4 Charlotte anchors${capLabel}`;
    stateBadge.className = 'state-badge warm';
  } else if (mKey === 'indianapolis') {
    stateBadge.textContent = `Cold · v7 hometown advantage${capLabel}`;
    stateBadge.className = 'state-badge cold v7';
  } else {
    stateBadge.textContent = `Cold start${capLabel}`;
    stateBadge.className = 'state-badge cold';
  }

  // Market switcher
  const sw = document.getElementById('market-switcher');
  sw.innerHTML = MARKET_ORDER.map(k => {
    const nm = DATA.markets[k].name;
    return `<option value="${k}" ${k === mKey ? 'selected' : ''}>${nm}</option>`;
  }).join('');
  sw.addEventListener('change', e => {
    const isEmbed = new URLSearchParams(location.search).get('embed') === '1';
    location.href = `./market.html?m=${e.target.value}` + (isEmbed ? '&embed=1' : '');
  });

  // ---- Derive search text for every account -----------------------------
  accounts.forEach(a => {
    a._search = [a.name, a.address, a.valet_operator, a.garage_operator,
                 a.management, a.gm, a.type, a.pool_raw, a.tam_class,
                 a.gate_status, a.group_key]
                 .filter(Boolean).join(' ').toLowerCase();
  });

  // ---- Populate quartile counts ------------------------------------------
  [1,2,3,4].forEach(q => {
    const c = accounts.filter(a => a._quartile === q).length;
    const el = document.getElementById('count-q' + q);
    if (el) el.textContent = c;
  });

  // ---- Populate acquisition year counts (portfolio view) ----------------
  [1,2,3,4,5,0].forEach(y => {
    const c = accounts.filter(a => a._signYear === y).length;
    const el = document.getElementById('count-y' + y);
    if (el) el.textContent = c;
  });

  // ---- Populate account type filters (portfolio view) --------------------
  const typeCounts = {};
  accounts.forEach(a => {
    const t = a.type || 'Unknown';
    typeCounts[t] = (typeCounts[t] || 0) + 1;
  });
  const typeFilters = document.getElementById('type-filters');
  const sortedTypes = Object.keys(typeCounts).sort((a, b) => typeCounts[b] - typeCounts[a]);
  typeFilters.innerHTML = sortedTypes.map(t => `
    <label class="filter-item">
      <input type="checkbox" checked data-type="${escAttr(t)}">
      <span class="type-icon-swatch type-${escAttr(t.toLowerCase())}">${iconSvgFor(t)}</span>
      <span class="filter-label">${escHtml(t)}</span>
      <span class="filter-count">${typeCounts[t]}</span>
    </label>
  `).join('');

  // ---- View state (Market vs Portfolio, session-persistent) --------------
  const VIEW_KEY = 'sophi_deal_room_map_view';
  let currentView = sessionStorage.getItem(VIEW_KEY) || 'market';
  if (currentView !== 'market' && currentView !== 'portfolio') currentView = 'market';

  function renderKpiMiniRow() {
    const el = document.getElementById('kpi-mini-row');
    if (currentView === 'market') {
      el.innerHTML = `
        <div class="summary-mini"><span class="smini-val">${summary.n_accounts}</span><span class="smini-lbl">Accounts</span></div>
        <div class="summary-mini"><span class="smini-val">${summary.n_in_sam}</span><span class="smini-lbl">In SAM</span></div>
        <div class="summary-mini"><span class="smini-val accent">$${fmtM(summary.tam)}</span><span class="smini-lbl">TAM</span></div>
      `;
    } else {
      el.innerHTML = `
        <div class="summary-mini"><span class="smini-val">${nWins}</span><span class="smini-lbl">Wins</span></div>
        <div class="summary-mini"><span class="smini-val accent">$${fmtM(summary.y5_som)}</span><span class="smini-lbl">Y5 Run</span></div>
        <div class="summary-mini"><span class="smini-val">$${fmtM(totalY5 + (summary.y1_som||0)*0)}</span><span class="smini-lbl">5-yr Cum</span></div>
      `;
      // 5-yr cumulative = sum of y1..y5 across all acquired accounts
      const cum = acquired.reduce((s,a) => s + (Number(a.y1)||0) + (Number(a.y2)||0) + (Number(a.y3)||0) + (Number(a.y4)||0) + (Number(a.y5)||0), 0);
      el.querySelectorAll('.summary-mini')[2].innerHTML =
        `<span class="smini-val">$${fmtM(cum)}</span><span class="smini-lbl">5-yr Cum</span>`;
    }
  }

  function applyViewMode() {
    document.body.setAttribute('data-view', currentView);
    document.querySelectorAll('#view-toggle .vt-btn').forEach(b => {
      b.classList.toggle('active', b.dataset.view === currentView);
    });
    document.querySelectorAll('.view-market-only').forEach(el => {
      el.style.display = currentView === 'market' ? '' : 'none';
    });
    document.querySelectorAll('.view-portfolio-only').forEach(el => {
      el.style.display = currentView === 'portfolio' ? '' : 'none';
    });
    // Legend hint
    const hint = document.getElementById('legend-hint');
    if (hint) {
      hint.textContent = currentView === 'market'
        ? 'Chip color = quartile · Chip size = rank within quartile'
        : 'Chip color = sign year · Chip size = revenue contribution';
    }
    renderKpiMiniRow();
  }
  document.querySelectorAll('#view-toggle .vt-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      currentView = btn.dataset.view;
      sessionStorage.setItem(VIEW_KEY, currentView);
      applyViewMode();
      updateAllMarkers();
      applyFilters();
    });
  });

  // ---- Icon SVGs (used for both markers and legend) ---------------------
  function iconSvgFor(type) {
    const t = (type || '').toLowerCase();
    if (t.includes('hotel') || t.includes('lodging') || t.includes('extended')) {
      // Building/hotel glyph
      return '<svg viewBox="0 0 24 24" fill="none"><path d="M4 22V4a1 1 0 0 1 1-1h14a1 1 0 0 1 1 1v18M4 22h16M8 7h2M8 11h2M8 15h2M14 7h2M14 11h2M14 15h2M10 22v-4h4v4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>';
    }
    if (t.includes('restaurant') || t.includes('food') || t.includes('dining')) {
      // Fork + knife
      return '<svg viewBox="0 0 24 24" fill="none"><path d="M8 3v9a2 2 0 0 1-2 2v7M8 3a2 2 0 0 0-2 2v5a2 2 0 0 0 2 2M16 3v18M16 3a3 3 0 0 1 3 3v5a3 3 0 0 1-3 3" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>';
    }
    // Fallback: generic dot glyph
    return '<svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="3" fill="currentColor"/></svg>';
  }

  // ---- Build map ---------------------------------------------------------
  const center = market.center || [-98, 39];
  const ZOOM_BY_MARKET = {
    charlotte: 11,
    indianapolis: 11,
    denver: 10.3,
    houston: 10.5,
    detroit: 10.5,
    south_bend: 11.5,
  };
  const zoom = ZOOM_BY_MARKET[mKey] || 11;

  const map = new maplibregl.Map({
    container: 'map',
    style: {
      version: 8,
      glyphs: 'https://fonts.openmaptiles.org/{fontstack}/{range}.pbf',
      sources: {
        'osm-raster': {
          type: 'raster',
          tiles: [
            'https://tile.openstreetmap.org/{z}/{x}/{y}.png'
          ],
          tileSize: 256,
          maxzoom: 19,
          attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }
      },
      layers: [{ id: 'osm', type: 'raster', source: 'osm-raster' }]
    },
    center: center,
    zoom: zoom,
    attributionControl: { compact: true }
  });
  map.addControl(new maplibregl.NavigationControl({ showCompass: false }), 'top-right');

  // Build icon-on-chip markers
  const markers = [];
  let activePopup = null;

  function chipSizeFor(a) {
    // Chip size scales inversely with rank (top of bucket = large, bottom = small)
    // Range 24-38px
    const r = currentView === 'market' ? (a._quartileRank ?? 0.5) : (a._yearRank ?? 0.5);
    return Math.round(38 - r * 14); // 38 -> 24
  }
  function iconSizeFor(size) { return Math.round(size * 0.5); }

  function chipClassFor(a) {
    if (currentView === 'market') {
      return 'chip-q' + a._quartile;
    } else {
      return 'chip-y' + a._signYear;
    }
  }

  function updateMarkerStyle(el, a) {
    const size = chipSizeFor(a);
    const iconSz = iconSizeFor(size);
    el.style.width = size + 'px';
    el.style.height = size + 'px';
    const svg = el.querySelector('svg');
    if (svg) {
      svg.style.width = iconSz + 'px';
      svg.style.height = iconSz + 'px';
    }
    // Reset chip classes
    el.classList.remove('chip-q1','chip-q2','chip-q3','chip-q4','chip-y0','chip-y1','chip-y2','chip-y3','chip-y4','chip-y5');
    el.classList.add(chipClassFor(a));
    // Muted state for portfolio view unacquired
    el.classList.toggle('chip-muted', currentView === 'portfolio' && a._signYear === 0);
  }

  function updateAllMarkers() {
    markers.forEach(({ el, account }) => updateMarkerStyle(el, account));
  }

  accounts.forEach((a, idx) => {
    if (!a.lng || !a.lat) return;
    const el = document.createElement('div');
    const fbCls = a.geocoded === false ? ' chip-fallback' : '';
    el.className = `map-marker chip-marker${fbCls}`;
    el.dataset.idx = idx;
    el.innerHTML = iconSvgFor(a.type);
    updateMarkerStyle(el, a);

    const marker = new maplibregl.Marker({ element: el, anchor: 'center' })
      .setLngLat([a.lng, a.lat])
      .addTo(map);

    el.addEventListener('click', e => {
      e.stopPropagation();
      openModal(a);
    });

    el.addEventListener('mouseenter', () => {
      if (activePopup) activePopup.remove();
      const tamLine = (a.tam && a.tam > 0) ? `$${fmtM(a.tam)} TAM` : '';
      const quartileLine = ` · Quartile ${a._quartile}`;
      const yearLine = a._signYear > 0 ? ` · Y${a._signYear}` : ' · Unacquired';
      const contextLine = currentView === 'market' ? quartileLine : yearLine;
      activePopup = new maplibregl.Popup({ closeButton: false, closeOnClick: false, offset: 20 })
        .setLngLat([a.lng, a.lat])
        .setHTML(`
          <div class="popup-title">${escHtml(a.name)}</div>
          <div class="popup-meta">${escHtml(a.type || 'Account')}${tamLine ? ' · ' + tamLine : ''}${contextLine}</div>
        `)
        .addTo(map);
    });
    el.addEventListener('mouseleave', () => {
      if (activePopup) { activePopup.remove(); activePopup = null; }
    });

    markers.push({ marker, el, account: a, idx });
  });

  // ---- Filter state & apply ----------------------------------------------
  let currentSearch = '';
  function getActiveFilterSet(selector, attr) {
    const set = new Set();
    document.querySelectorAll(`${selector} input[type="checkbox"]`).forEach(cb => {
      if (cb.checked) set.add(cb.dataset[attr]);
    });
    return set;
  }

  function applyFilters() {
    const hideUnacq = document.getElementById('hide-unacquired')?.checked;
    let visible = 0;
    if (currentView === 'market') {
      const quartiles = new Set();
      document.querySelectorAll('#quartile-filters input[type="checkbox"]').forEach(cb => {
        if (cb.checked) quartiles.add(Number(cb.dataset.quartile));
      });
      markers.forEach(({ el, account }) => {
        const qMatch = quartiles.has(account._quartile);
        const searchMatch = !currentSearch || account._search.includes(currentSearch);
        const show = qMatch && searchMatch;
        el.style.display = show ? '' : 'none';
        if (show) visible++;
      });
    } else {
      const years = new Set();
      document.querySelectorAll('#year-filters input[type="checkbox"][data-year]').forEach(cb => {
        if (cb.checked) years.add(Number(cb.dataset.year));
      });
      const types = getActiveFilterSet('#type-filters', 'type');
      markers.forEach(({ el, account }) => {
        const yMatch = years.has(account._signYear);
        const unacqOk = !(hideUnacq && account._signYear === 0);
        const tMatch = types.size === 0 || types.has(account.type || 'Unknown');
        const searchMatch = !currentSearch || account._search.includes(currentSearch);
        const show = yMatch && unacqOk && tMatch && searchMatch;
        el.style.display = show ? '' : 'none';
        if (show) visible++;
      });
    }
    document.querySelector('#stat-visible .stat-num').textContent = visible;
  }

  document.querySelectorAll('#sidebar input[type="checkbox"]').forEach(cb => {
    cb.addEventListener('change', applyFilters);
  });
  document.getElementById('search-input').addEventListener('input', e => {
    currentSearch = e.target.value.trim().toLowerCase();
    applyFilters();
  });

  // Initialize view mode + filters
  applyViewMode();
  applyFilters();

  // ---- Modal -------------------------------------------------------------
  const overlay = document.getElementById('modal-overlay');
  const modalContent = document.getElementById('modal-content');
  document.getElementById('modal-close').addEventListener('click', closeModal);
  overlay.addEventListener('click', e => { if (e.target === overlay) closeModal(); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModal(); });

  function closeModal() { overlay.classList.add('hidden'); }

  function openModal(a) {
    const poolKey = a.pool || 'micro';
    const poolLabel = POOL_LABEL[poolKey] || poolKey;
    const tamStr = (a.tam && a.tam > 0) ? '$' + fmtM(a.tam) + ' TAM' : null;
    const samBadge = a.in_sam
      ? `<span class="modal-sam-chip in-sam">In SAM</span>`
      : `<span class="modal-sam-chip out-sam">Out of SAM · ${escHtml(poolLabel)}</span>`;

    // V7 callout
    const v7 = a.v7_layer && V7_LABEL[a.v7_layer];
    const v7Block = v7
      ? `<div class="v7-callout ${v7.cls}">
           <div class="v7-callout-label">${escHtml(v7.label)}</div>
           <div class="v7-callout-detail">${escHtml(v7.detail)}</div>
         </div>`
      : '';

    // SAM/SOM trajectory bars
    const trajectoryHtml = renderTrajectory(a);

    // Tier display (still useful as a secondary signal)
    const tierShort = a.tier || '—';
    const tierFull = a.tier_full || 'Unscored';
    const tierCls = (a.tier || 'd').toString().toLowerCase();

    modalContent.innerHTML = `
      <div class="modal-hero">
        <div class="modal-hero-row">
          <span class="modal-pool-chip pool-${poolKey}">
            <span class="pool-dot pool-${poolKey}-dot"></span>
            ${escHtml(poolLabel)}
          </span>
          ${samBadge}
          ${tamStr ? `<span class="modal-tam-chip">${tamStr}</span>` : ''}
          ${a.tier ? `<span class="modal-tier ${tierCls}">Tier ${tierShort}</span>` : ''}
        </div>
        <h2 class="modal-title">${escHtml(a.name)}</h2>
        <div class="modal-subtitle">
          <span>${escHtml(a.type || 'Account')}</span>
          ${a.address ? `<span>·</span><span>${escHtml(a.address)}</span>` : ''}
          ${a.area === 'YES' ? `<span>·</span><span>Downtown</span>` : ''}
        </div>
        ${v7Block}
      </div>

      <div class="modal-body">

        ${a.in_sam ? `
        <div class="modal-group">
          <div class="modal-group-title">v3 lifecycle — acquisition &amp; trajectory</div>
          ${renderV3LifecycleBlock(a)}
          ${trajectoryHtml}
          <div class="modal-fields modal-fields-tight">
            <div class="modal-field"><span class="modal-field-lbl">Annual TAM (post-acq)</span><span class="modal-field-val">${fmtVal(a.tam, v => '$' + fmtM(v))}</span></div>
            <div class="modal-field"><span class="modal-field-lbl">SAM contribution</span><span class="modal-field-val">${fmtVal(a.sam_contrib, v => '$' + fmtM(v))}</span></div>
            <div class="modal-field"><span class="modal-field-lbl">Ownership group</span><span class="modal-field-val">${fmtVal(a.group_key, v => v.replace(/_/g,' '))}</span></div>
            <div class="modal-field"><span class="modal-field-lbl">Group wins at acq.</span><span class="modal-field-val">${a.acquisition_year ? (a.group_wins_at_acquisition ?? 0) : '—'}</span></div>
          </div>
        </div>
        ` : `
        <div class="modal-group">
          <div class="modal-group-title">Why excluded from SAM</div>
          <div class="modal-exclusion">${escHtml(samExclusionReason(a))}</div>
        </div>
        `}

        <div class="modal-group">
          <div class="modal-group-title">Parking economics &amp; TAM</div>
          <div class="modal-fields">
            <div class="modal-field"><span class="modal-field-lbl">TAM</span><span class="modal-field-val">${fmtVal(a.tam, v => '$' + fmtM(v))}</span></div>
            <div class="modal-field"><span class="modal-field-lbl">TAM class</span><span class="modal-field-val">${fmtVal(a.tam_class)}</span></div>
            <div class="modal-field"><span class="modal-field-lbl">Valet rate</span><span class="modal-field-val">${fmtVal(a.valet_rate, v => '$' + v)}</span></div>
            <div class="modal-field"><span class="modal-field-lbl">Self-park rate</span><span class="modal-field-val">${fmtVal(a.self_park_rate, v => '$' + v)}</span></div>
            <div class="modal-field"><span class="modal-field-lbl">Rooms</span><span class="modal-field-val">${fmtVal(a.rooms)}</span></div>
            <div class="modal-field"><span class="modal-field-lbl">Seats</span><span class="modal-field-val">${fmtVal(a.seats)}</span></div>
            <div class="modal-field"><span class="modal-field-lbl">Occupancy</span><span class="modal-field-val">${fmtVal(a.occupancy, v => (v <= 1 ? Math.round(v*100) : v) + '%')}</span></div>
            <div class="modal-field"><span class="modal-field-lbl">Valet conv.</span><span class="modal-field-val">${fmtVal(a.valet_conv, v => (v <= 1 ? (v*100).toFixed(1) : v) + '%')}</span></div>
            ${a.tam_status ? `<div class="modal-field wide"><span class="modal-field-lbl">TAM status</span><span class="modal-field-val">${escHtml(a.tam_status)}</span></div>` : ''}
            ${a.tam_notes ? `<div class="modal-field wide"><span class="modal-field-lbl">TAM notes</span><span class="modal-field-val">${escHtml(a.tam_notes)}</span></div>` : ''}
          </div>
        </div>

        <div class="modal-group">
          <div class="modal-group-title">WAS scoring</div>
          <div class="modal-fields">
            <div class="modal-field"><span class="modal-field-lbl">WAS score</span><span class="modal-field-val">${fmtVal(a.was, v => Number(v).toFixed(2))}</span></div>
            <div class="modal-field"><span class="modal-field-lbl">Tier</span><span class="modal-field-val">${escHtml(tierFull)}</span></div>
            ${a.was_base != null ? `<div class="modal-field"><span class="modal-field-lbl">WAS base</span><span class="modal-field-val">${Number(a.was_base).toFixed(2)}</span></div>` : ''}
            ${a.was_boost != null ? `<div class="modal-field"><span class="modal-field-lbl">WAS boost</span><span class="modal-field-val">+${Number(a.was_boost).toFixed(2)}</span></div>` : ''}
          </div>
        </div>

        <div class="modal-group">
          <div class="modal-group-title">Operator &amp; management</div>
          <div class="modal-fields">
            <div class="modal-field"><span class="modal-field-lbl">Valet operator</span><span class="modal-field-val">${fmtVal(a.valet_operator)}</span></div>
            <div class="modal-field"><span class="modal-field-lbl">Garage operator</span><span class="modal-field-val">${fmtVal(a.garage_operator)}</span></div>
            <div class="modal-field"><span class="modal-field-lbl">Management</span><span class="modal-field-val">${fmtVal(a.management)}</span></div>
            <div class="modal-field"><span class="modal-field-lbl">GM</span><span class="modal-field-val">${fmtVal(a.gm)}</span></div>
          </div>
        </div>

        <div class="modal-group">
          <div class="modal-group-title">Contact</div>
          <div class="modal-fields">
            <div class="modal-field"><span class="modal-field-lbl">Phone</span><span class="modal-field-val">${a.phone ? `<a href="tel:${escAttr(a.phone)}">${escHtml(a.phone)}</a>` : '<span class="empty">—</span>'}</span></div>
            <div class="modal-field"><span class="modal-field-lbl">Email</span><span class="modal-field-val">${a.email ? `<a href="mailto:${escAttr(a.email)}">${escHtml(a.email)}</a>` : '<span class="empty">—</span>'}</span></div>
            <div class="modal-field wide"><span class="modal-field-lbl">Website</span><span class="modal-field-val">${a.url ? `<a href="${escAttr(a.url)}" target="_blank" rel="noopener">${escHtml(shortUrl(a.url))}</a>` : '<span class="empty">—</span>'}</span></div>
          </div>
        </div>

      </div>
    `;

    overlay.classList.remove('hidden');
  }

  function samExclusionReason(a) {
    const map = {
      partnership:   'Partnership / PMC bundled — surface via Preferred or PMC channel rather than direct displacement.',
      enterprise:    'Enterprise operator (LAZ / SP+ / Towne / Ace / Impark) — multi-property contract, harder to displace single-asset.',
      extended_stay: 'Extended-stay brand (Home2 / Homewood / Hyatt House / SpringHill / Element) — limited valet upside per asset.',
      micro:         'Micro account (TAM < $150K) — not worth direct sales motion.',
    };
    return map[a.pool] || 'Out of structural SAM.';
  }

  function renderTrajectory(a) {
    const years = [a.y1, a.y2, a.y3, a.y4, a.y5].map(v => Number(v) || 0);
    const max = Math.max(...years, a.tam || 0, 1);
    const acqYr = a.acquisition_year;
    return `
      <div class="trajectory">
        ${years.map((v, i) => {
          const yr = i + 1;
          const isAcquired = acqYr && yr >= acqYr;
          const cls = isAcquired ? 'acquired' : 'pre-acq';
          const minH = v > 0 ? 0 : 2; // sliver for pre-acq years so pattern is visible
          const barH = v > 0 ? (v / max) * 100 : minH;
          return `
          <div class="trajectory-col ${cls}">
            <div class="trajectory-bar-wrap">
              <div class="trajectory-bar" style="height: ${barH}%"></div>
            </div>
            <div class="trajectory-val">${v > 0 ? '$'+fmtM(v) : '—'}</div>
            <div class="trajectory-lbl">Y${yr}${acqYr === yr ? ' ★' : ''}</div>
          </div>`;
        }).join('')}
      </div>
    `;
  }

  function renderV3LifecycleBlock(a) {
    const ay = a.acquisition_year;
    const gs = a.gate_status || '';
    const gsLow = gs.toLowerCase();
    let pillCls = '';
    let pillTxt = '';
    let yearTxt = '';
    if (ay) {
      yearTxt = `Acquired Y${ay}`;
      if (gsLow.startsWith('anchor:')) {
        pillCls = 'anchor';
        pillTxt = 'SOPHI Anchor';
      } else if (gsLow.startsWith('v7_hometown')) {
        pillCls = 'anchor';
        pillTxt = 'v7 Hometown';
      } else if (gsLow.startsWith('v7_ma_absorption')) {
        pillCls = 'anchor';
        pillTxt = 'v7 M&A Absorption';
      } else {
        pillTxt = 'Won via gate + cap';
      }
    } else {
      yearTxt = 'Not acquired by Y5';
      if (gsLow.startsWith('gated:')) {
        pillCls = 'gated';
        pillTxt = 'Operator-gated';
      } else if (gsLow.includes('cap-deferred')) {
        pillCls = 'deferred';
        pillTxt = 'Cap-deferred';
      } else if (gsLow.startsWith('in-pool')) {
        pillCls = 'deferred';
        pillTxt = 'Below cap line';
      } else {
        pillCls = 'deferred';
        pillTxt = 'Outside 5-yr window';
      }
    }
    const detailLines = [];
    if (gs) detailLines.push(escHtml(gs));
    if (a.operator_gate) detailLines.push(`Operator gate: <strong>${escHtml(a.operator_gate)}</strong>`);
    if (ay && a.group_wins_at_acquisition != null && a.group_wins_at_acquisition > 0) {
      const m = a.group_wins_at_acquisition >= 3 ? '3×' : (a.group_wins_at_acquisition === 2 ? '2×' : '1.5×');
      detailLines.push(`Sister-property wins at acquisition: <strong>${a.group_wins_at_acquisition}</strong> (relationship multiplier ${m})`);
    }
    return `
      <div class="v3-acq-block">
        <div class="v3-acq-head">
          <span class="v3-acq-year ${ay ? '' : 'never'}">${yearTxt}</span>
          ${pillTxt ? `<span class="v3-acq-pill ${pillCls}">${pillTxt}</span>` : ''}
        </div>
        ${detailLines.length ? `<div class="v3-acq-detail">${detailLines.join(' · ')}</div>` : ''}
      </div>
    `;
  }

  // ---- Sidebar toggle (mobile) -------------------------------------------
  document.getElementById('sidebar-toggle').addEventListener('click', () => {
    document.body.classList.toggle('sidebar-open');
  });

  // ---- Helpers ------------------------------------------------------------
  function fmtM(n) {
    if (n == null) return '—';
    n = Number(n);
    if (!isFinite(n)) return '—';
    if (n >= 1e9) return (n/1e9).toFixed(2) + 'B';
    if (n >= 1e6) return (n/1e6).toFixed(2) + 'M';
    if (n >= 1e3) return (n/1e3).toFixed(0) + 'K';
    if (n === 0) return '0';
    return String(Math.round(n));
  }
  function fmtVal(v, formatter) {
    if (v == null || v === '' || v === 'TBD') return '<span class="empty">—</span>';
    return formatter ? formatter(v) : escHtml(String(v));
  }
  function escHtml(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/'/g, '&#039;');
  }
  function escAttr(s) { return escHtml(s); }
  function shortUrl(u) {
    try { return new URL(u).hostname.replace(/^www\./,''); } catch(e) { return u; }
  }
})();
