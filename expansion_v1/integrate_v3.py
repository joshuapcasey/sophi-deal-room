"""
integrate_v3.py — apply v2-style SAM exclusions to the 8 expansion markets,
merge into accounts_v2.json shape, run v3 penetration engine, write
accounts_v3.json with all 14 markets.

User direction (May 7, 2026):
  - WAS NOT applied to new markets (set was=null). Engine reads was as 0,
    which is fine — pure rubric is now: pool tier + TAM + group multiplier
    + operator gate + S-curve cap. Sales attention (WAS) is decoupled.
  - All 8 new markets COLD (Y5 cap = 30%, S-curve 10/30/50/70/85 scaled).
  - No v7 overrides anywhere new.

SAM EXCLUSION RULES (from v2 methodology, METHODOLOGY_v2.md §1):
  1. Partnership (operator type 'PMC' explicitly flagged as Partnership) → out
  2. Enterprise (operator = Towne Park, with Towne Park enterprise contract) → out
  3. Extended-stay brand (Homewood Suites, Residence Inn, etc.) → out
  4. Micro (TAM < $150K) → out
  Plus: zero-TAM accounts → out (no_capacity venues)

POOL ASSIGNMENT FOR NEW MARKETS:
  - No SOPHI presence in any new market → no 'anchor' pool
  - No M&A trigger flagged → no 'ma_sam' pool
  - All in-SAM accounts → 'cold_sam'
  - All excluded → matching exclusion pool name (partnership/enterprise/extended_stay/micro/no_tam)
"""

import json, copy
from pathlib import Path
from collections import Counter

EXPANSION_PATH = Path('/home/user/workspace/sophi-market-map/expansion_v1/expansion_accounts.json')
V2_PATH = Path('/home/user/workspace/sophi-market-map/src/accounts_v2.json')
V2_OUT_PATH = Path('/home/user/workspace/sophi-market-map/src/accounts_v2_14mkt.json')

# State codes per market
MARKET_STATE = {
    'ft_wayne':      'IN',
    'cincinnati':    'OH',
    'columbus':      'OH',
    'minneapolis':   'MN',
    'st_louis':      'MO',
    'raleigh':       'NC',
    'charleston':    'SC',
    'ft_lauderdale': 'FL',
}

MARKET_DISPLAY = {
    'ft_wayne':      'Fort Wayne',
    'cincinnati':    'Cincinnati',
    'columbus':      'Columbus',
    'minneapolis':   'Minneapolis',
    'st_louis':      'St. Louis',
    'raleigh':       'Raleigh',
    'charleston':    'Charleston',
    'ft_lauderdale': 'Fort Lauderdale',
}

MICRO_TAM_THRESHOLD = 150_000

# Per user direction (May 7, 2026):
# Venues, Hospitals, Airports stay in TAM but are EXCLUDED from SAM.
# Zero acquisitions modeled in any of these verticals — SOM is hotels + restaurants only.
SAM_EXCLUDED_TYPES = {'Venue', 'Hospital', 'Airport'}

EXTENDED_STAY_KEYWORDS = [
    'homewood suites', 'residence inn', 'extended stay', 'extendedstay',
    'staybridge suites', 'candlewood suites', 'townplace suites',
    'towneplace suites', 'home2 suites', 'sonesta es suites',
    'element hotel', 'element by westin', 'home2suites', 'hyatt house',
]

def is_extended_stay(name):
    n = (name or '').lower()
    return any(k in n for k in EXTENDED_STAY_KEYWORDS)

def is_partnership(operator):
    """Partnership pool = explicit PMC ownership/operator partnership.
    Per v2: Le Méridien Indianapolis and Bottleworks Hotel were flagged as
    Partnership PMC. We mirror that — only flag when operator string is
    explicitly 'PMC' as a partnership signal AND the property is hotel-class.
    For the new markets, no explicit partnership relationships have been
    declared, so we leave Partnership unused unless valet_operator string
    contains 'PMC partnership' or similar.
    """
    if not operator:
        return False
    s = operator.lower()
    # Conservative: only flag if explicitly tagged
    return ('pmc partnership' in s) or ('partnership pmc' in s)

def is_enterprise(operator):
    """Enterprise pool = locked into national enterprise contract — currently
    Towne Park is the only operator we treat as full lockout. Others (LAZ,
    SP+, ABM, etc.) get gated but not excluded — they remain in SAM."""
    if not operator:
        return False
    return 'towne park' in operator.lower()

def assign_pool_and_sam(account):
    """Returns (pool, in_sam, sam_contrib, exclusion_reason)."""
    name = account.get('name', '')
    operator = account.get('valet_operator') or ''
    tam = float(account.get('tam') or 0)
    typ = account.get('type', '')

    # Hard exclusion 0: no TAM → can't be in SAM
    if tam <= 0:
        return ('no_tam', False, 0.0, 'no usable TAM (capacity field missing)')

    # Hard exclusion (NEW, May 7, 2026): Venues / Hospitals / Airports excluded
    # from SAM/SOM. They remain in TAM totals but contribute zero acquisitions.
    # SOM penetration is modeled only against hotels and restaurants.
    if typ in SAM_EXCLUDED_TYPES:
        return (f'tam_only_{typ.lower()}', False, 0.0, f'{typ} — TAM-only, excluded from SAM/SOM per May 2026 directive')

    # Hard exclusion 1: Enterprise (Towne Park lock)
    if is_enterprise(operator):
        return ('enterprise', False, 0.0, 'Towne Park enterprise contract')

    # Hard exclusion 2: Partnership PMC
    if is_partnership(operator):
        return ('partnership', False, 0.0, 'PMC partnership lockout')

    # Hard exclusion 3: Extended-stay brand (hotels only)
    if typ == 'Hotel' and is_extended_stay(name):
        return ('extended_stay', False, 0.0, 'extended-stay brand (low valet utilization)')

    # Hard exclusion 4: Micro (TAM < $150K)
    if tam < MICRO_TAM_THRESHOLD:
        return ('micro', False, 0.0, f'TAM ${tam/1000:.0f}K below micro threshold')

    # Default for new markets: cold_sam (no SOPHI anchors)
    return ('cold_sam', True, tam, None)

def normalize_account_to_v2_shape(acct):
    """Map expansion-format account to v2 schema fields used by normalize_v3.py."""
    pool, in_sam, sam_contrib, exclusion = assign_pool_and_sam(acct)

    # Build management/group source notes
    notes_parts = []
    if acct.get('ownership_group'):
        notes_parts.append(f"Ownership: {acct['ownership_group']}")
    if acct.get('management'):
        notes_parts.append(f"Mgmt: {acct['management']}")
    if exclusion:
        notes_parts.append(f"SAM excluded: {exclusion}")
    tam_notes = ' | '.join(notes_parts) if notes_parts else ''

    rec = {
        'name': acct['name'],
        'market': acct['market'],
        'type': acct.get('type', 'Other'),
        'tam': float(acct.get('tam') or 0),
        'sam_contrib': sam_contrib,
        'pool': pool,
        'in_sam': in_sam,
        'rank': '—',
        'was': None,         # PER USER DIRECTION: WAS not applied to new markets
        'was_base': None,
        'was_boost': None,
        'sign_yr': 'N/A',
        'curve': 'v3 penetration engine',
        # y1..y5 will be overwritten by engine
        'y1': 0, 'y2': 0, 'y3': 0, 'y4': 0, 'y5': 0,
        'address': acct.get('address', '') or '',
        'area': '',  # downtown flag — not used by v3 engine
        'phone': acct.get('phone', '') or '',
        'email': acct.get('email', '') or '',
        'url': acct.get('url', '') or '',
        'self_park_rate': acct.get('self_park_rate'),
        'valet_rate': acct.get('valet_rate'),
        'rooms': acct.get('rooms'),
        'seats': acct.get('seats'),
        'occupancy': acct.get('occupancy'),
        'turnover': acct.get('turnover'),
        'valet_conv': acct.get('valet_conv'),
        'gm': acct.get('gm', '') or '',
        'gm_role': '',
        'management': acct.get('management', '') or '',
        'garage_operator': acct.get('garage_operator', '') or '',
        'valet_operator': acct.get('valet_operator', '') or '',
        'sourcing_notes': acct.get('sourcing_notes', '') or '',
        'location_notes': acct.get('location_notes', '') or '',
        'tam_class': f"{acct.get('type','')} — {acct.get('tam_status', 'expansion v1')}",
        'tam_status': acct.get('tam_status', ''),
        'tam_notes': tam_notes,
        'pool_raw': pool.title(),
        'v7_layer': None,    # PER USER DIRECTION: no v7 overrides
        # Extra fields for engine helpers
        'beds': acct.get('beds'),
        'capacity': acct.get('capacity'),
        'op_days': acct.get('op_days'),
        'peak_mod': acct.get('peak_mod'),
        'ownership_group': acct.get('ownership_group', '') or '',
        'rate_source': acct.get('rate_source', ''),
    }
    return rec

def build_market(market_key, market_data):
    """Convert one expansion market to v2 schema."""
    accts_v2 = [normalize_account_to_v2_shape(a) for a in market_data['accounts']]

    pool_counts = Counter(a['pool'] for a in accts_v2)
    pool_tam = {p: 0.0 for p in pool_counts}
    for a in accts_v2:
        pool_tam[a['pool']] += a['tam']

    n_in_sam = sum(1 for a in accts_v2 if a['in_sam'])
    market_tam = sum(a['tam'] for a in accts_v2)
    market_sam = sum(a['sam_contrib'] for a in accts_v2 if a['in_sam'])

    return {
        'name': MARKET_DISPLAY[market_key],
        'state': MARKET_STATE[market_key],
        'accounts': accts_v2,
        'pool_counts': dict(pool_counts),
        'pool_tam': pool_tam,
        'tier_counts': {},
        'summary': {
            'tam': market_tam,
            'sam': market_sam,
            'y1_som': 0,    # engine will set
            'y5_som': 0,    # engine will set
            'n_accounts': len(accts_v2),
            'n_in_sam': n_in_sam,
            'state': 'COLD',
            'sam_tam_ratio': (market_sam / market_tam) if market_tam else 0,
            'y5_tam_ratio': 0,
            'y5_sam_ratio': 0,
        },
        'rollup': {},
        'pool_structure_rollup': {},
    }

def main():
    # Load expansion accounts
    with open(EXPANSION_PATH) as f:
        exp = json.load(f)
    print(f'Loaded {sum(len(m["accounts"]) for m in exp["markets"].values())} expansion accounts across {len(exp["markets"])} markets')

    # Load existing v2
    with open(V2_PATH) as f:
        v2 = json.load(f)
    print(f'Loaded existing v2: {len(v2["markets"])} markets, {sum(len(m["accounts"]) for m in v2["markets"].values())} accounts')

    # Convert each expansion market
    for mk, mdata in exp['markets'].items():
        v2['markets'][mk] = build_market(mk, mdata)
        s = v2['markets'][mk]['summary']
        print(f"  {mk:14s}  N={s['n_accounts']:3d}  in_SAM={s['n_in_sam']:3d}  "
              f"TAM=${s['tam']/1e6:6.2f}M  SAM=${s['sam']/1e6:6.2f}M  "
              f"({s['sam_tam_ratio']*100:.0f}% sam/tam)")

    # Write merged v2 file
    with open(V2_OUT_PATH, 'w') as f:
        json.dump(v2, f, indent=2, default=str)
    print(f'\nWrote {V2_OUT_PATH}')
    print(f'Total markets: {len(v2["markets"])}')
    print(f'Total accounts: {sum(len(m["accounts"]) for m in v2["markets"].values())}')

if __name__ == '__main__':
    main()
