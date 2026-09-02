"""
refinement_v3_1.py — SOPHI Growth Engine v3.1 (§2.7 + §2.8 + §4 refinements)

DRAFT — pending CFO advisor review. Does not modify normalize_v3.py or accounts_v3.json.

Layered on top of the v3 engine. Reads src/accounts_v3.json (the current locked
output), applies the following non-destructive refinements, and writes
src/accounts_v3_1.json + a diff report.

Changes applied (all reversible — original v3 files untouched):

  §2.7 CANONICAL SOPHI 6 FOOTPRINT UPDATE
    - Retag Phoenix, Cleveland, Louisville as growth_model = "expansion"
    - Add new market blocks: Houston, Detroit, South Bend as growth_model =
      "acquisition" with G&G anchors + halo candidates
    - Existing Charlotte/Indianapolis/Denver stay as growth_model = "acquisition"

  §2.8 FLAGSHIP HOTEL GATE
    - flagship_hotel = chain_scale in {Luxury, Upper Upscale} OR name matches
      known flagship brand keyword
    - When flagship_hotel AND acquisition_year <= 2 AND NOT anchor_unlock:
      strip acquisition_year (moved to Y3+ pool via re-scoring)
    - anchor_unlock = True if operator matches SOPHI-acquisition-target operator
      for the acquisition close year OR SOPHI-actual t=0 OR hometown_displaced
      confirmed relationship (NOT the auto-selection kind)

  §4 NAMED ACCOUNT ADDITIONS + CORRECTIONS
    Indianapolis (Elite Management Q1 2027):
      - REMOVE hometown_displaced flag from Omni Severin + Conrad IND
        (not actually SOPHI-hometown; §2.8 flagship gate now handles them)
      - REMOVE hometown_displaced from The Capital Grille IND; retag as
        ma_absorption (Y2, Elite acquisition brings it)
      - REMOVE ma_absorption from Eddie Merlot's (Josh named 6 Elite restaurants;
        Eddie Merlot's not on that list)
      - ADD ma_absorption to Hyde Park Prime Steakhouse + Del Frisco's Double
        Eagle (Josh-confirmed Elite lineup), inserted as new accounts
      - ADD InterContinental Indianapolis + Sheraton Indianapolis City Centre
        as new accounts, operator = Elite Mgmt, owner_group = Keystone Group,
        pool = anchor (SOPHI-anchor via acquisition), v7_layer =
        hometown_displaced (confirmed Elite acquisition relationship = Y1)

    Denver (VIP Parking Solutions Q1 2028):
      - ADD G&G Denver + G&G second concept as new accounts, pool = anchor
        (SOPHI-committed launch), v7_layer = hometown_displaced (forced Y1 2027)
      - ADD Morton's Denver, Maggiano's Denver, Linger as new accounts,
        operator = VIP Parking Solutions
      - Add operator gate entry: "vip parking solutions": min 5 accts / 2 verticals
        (similar to Park Inc / Denison — independent regional operator)
      - When VIP acquisition closes Jan 2028, VIP-operated accounts unlock Y2

    Expansion Growth Model (Houston / Detroit / South Bend):
      - New market blocks NOT scored under the Acquisition Growth Model
      - Placeholder — data-loaded but not surfaced in canonical Y1-Y5 outputs
      - Houston: G&G Q2 2027 + Vic & Anthony's + Steak 48
      - Detroit: G&G Q3 2027 + Big Rock Italian Chophouse + The Whitney + Prime & Proper
      - South Bend: Courtyard SB t=0 + halo pipeline

OUTPUT:
  src/accounts_v3_1.json — engine output with refinements applied
  refinement_v3_1_diff.json — per-market diff vs v3
  refinement_v3_1_report.md — human-readable diff report

USAGE:
  python3 src/refinement_v3_1.py
"""
import json, os, sys, copy, math
from pathlib import Path
from collections import defaultdict, Counter

sys.path.insert(0, str(Path(__file__).parent))
from normalize_v3 import (
    MARKET_Y5_CAP, SCURVE_SHAPE, OPERATOR_GATES, GROUP_MULTIPLIER,
    penetration_curve_for_market, normalize_operator, detect_ownership_group,
    group_multiplier_for_count, base_priority, POOL_BASE_PRIORITY, V7_PRIORITY_BUMP
)

HERE = Path(__file__).parent

# ============================================================
# §2.7 — Growth model tagging + new expansion market caps
# ============================================================
ACQUISITION_MARKETS = {'charlotte', 'indianapolis', 'denver', 'houston', 'detroit', 'south_bend'}
EXPANSION_MARKETS = {'phoenix', 'cleveland', 'louisville'}  # was in SOPHI 6, moved to expansion

# Extend Y5 caps for new markets
MARKET_Y5_CAP_v31 = {
    **MARKET_Y5_CAP,
    # New expansion markets: use higher caps because our SAM universe here is
    # NAMED-anchor-only (we've filtered to accounts with a real relationship path)
    # rather than the full universe. If we've priced 3 accounts in Houston (G&G + 2
    # named halo), a 30% cap on 3 = 0 slots is nonsense.
    'houston':    0.85,  # tight, high-conviction named universe
    'detroit':    0.85,
    'south_bend': 0.85,  # Established, small named universe
}

# ============================================================
# §2.8 — Flagship hotel gate
# ============================================================
FLAGSHIP_KEYWORDS = {
    "jw marriott", "ritz-carlton", "ritz carlton", "four seasons", "st regis", "st. regis",
    "waldorf", "conrad", "park hyatt", "mandarin oriental", "peninsula",
    "aman", "rosewood", "montage", "westin", "sheraton",
    "renaissance hotel", "grand hyatt", "hyatt regency", "intercontinental",
    "omni ", "kimpton", "w hotel", "sofitel", "loews", "signia",
    "1 hotel", "raffles",
}

def is_flagship_hotel(account):
    """Return True if account is a flagship-tier hotel by chain-scale or brand keyword."""
    if account.get('type') != 'Hotel':
        return False
    cs = str(account.get('chain_scale') or '').lower()
    if 'luxury' in cs or 'upper upscale' in cs or 'upper-upscale' in cs:
        return True
    nm = str(account.get('name') or '').lower()
    return any(kw in nm for kw in FLAGSHIP_KEYWORDS)

# ============================================================
# §4 — Named account additions to accounts_v3.json
# ============================================================

# Indianapolis Elite Management acquisition (Q1 2027)
IND_ELITE_ADDITIONS = [
    # Hyde Park Prime - Josh confirmed Elite lineup, not in universe
    {
        'name': 'Hyde Park Prime Steakhouse',
        'type': 'Restaurant',
        'chain_scale': None,
        'brand': None,
        'management': 'Elite Management Services (Elite Restaurant Group)',
        'valet_operator': 'Elite Management Services',
        'tam': 300000.0,  # Peer to St. Elmo/Ruth's IND (~$150K-350K band)
        'was': 4.0,
        'pool': 'ma_sam',
        'v7_layer': 'ma_absorption',
        'in_sam': True,
        'tam_notes': 'Added §4 refinement: Josh-confirmed Elite Management restaurant lineup Q1 2027. Downtown Indy steakhouse.',
        'owner_group': None,
    },
    # Del Frisco's Double Eagle - Josh confirmed Elite lineup, not in universe
    {
        'name': "Del Frisco's Double Eagle Steakhouse (Indianapolis)",
        'type': 'Restaurant',
        'chain_scale': None,
        'brand': None,
        'management': 'Elite Management Services (Elite Restaurant Group)',
        'valet_operator': 'Elite Management Services',
        'tam': 350000.0,  # Larger flagship steakhouse, top of IND restaurant band
        'was': 4.0,
        'pool': 'ma_sam',
        'v7_layer': 'ma_absorption',
        'in_sam': True,
        'tam_notes': 'Added §4 refinement: Josh-confirmed Elite Management restaurant lineup Q1 2027.',
        'owner_group': None,
    },
    # InterContinental Indianapolis (Keystone-owned, Elite-operated, new-build)
    {
        'name': 'InterContinental Indianapolis',
        'type': 'Hotel',
        'chain_scale': 'Upper Upscale',
        'brand': 'InterContinental',
        'management': 'IHG (Keystone Group owned)',
        'valet_operator': 'Elite Management Services',
        'tam': 950000.0,  # New-build downtown; conservative estimate vs Omni Severin $2.2M
        'was': 4.5,
        'pool': 'anchor',
        'v7_layer': 'hometown_displaced',  # SOPHI-anchor via Elite acquisition = day-1 win
        'in_sam': True,
        'tam_notes': 'Added §4 refinement: Keystone Group-owned new-build downtown Indianapolis hotel. Elite Management holds valet contract; acquisition delivers day-1. Satisfies §2.8 flagship gate via operator anchor_unlock.',
        'owner_group': 'keystone_group',
    },
    # Sheraton Indianapolis City Centre Hotel (Keystone-owned, Elite-operated, Downtown)
    {
        'name': 'Sheraton Indianapolis City Centre Hotel',
        'type': 'Hotel',
        'chain_scale': 'Upper Upscale',
        'brand': 'Sheraton',
        'management': 'Marriott (Keystone Group owned)',
        'valet_operator': 'Elite Management Services',
        'tam': 850000.0,  # Downtown Sheraton; peer to Conrad IND $846K
        'was': 4.5,
        'pool': 'anchor',
        'v7_layer': 'hometown_displaced',
        'in_sam': True,
        'tam_notes': 'Added §4 refinement: Keystone Group-owned Downtown Sheraton (City Centre, not Keystone Crossing north-side). Elite Management holds valet; acquisition delivers day-1. Satisfies §2.8 via operator anchor_unlock.',
        'owner_group': 'keystone_group',
    },
]

# Denver additions: G&G anchors + VIP-named accounts
DEN_ADDITIONS = [
    {
        'name': 'Guard & Grace Denver',
        'type': 'Restaurant',
        'chain_scale': None, 'brand': None,
        'management': 'TAG Restaurant Group (Troy Guard)',
        'valet_operator': 'SOPHI (launching Q1 2027)',
        'tam': 250000.0,  # Bryce Denver Hotels R21: G&G Denver $150K + halo lift
        'was': 5.0,
        'pool': 'anchor',
        'v7_layer': 'hometown_displaced',  # SOPHI committed anchor
        'in_sam': True,
        'tam_notes': 'Added §4 refinement: SOPHI-committed G&G launch Q1 2027 (Bryce Assumptions). Michelin star anchor unlocks Denver halo effect.',
        'owner_group': None,
    },
    {
        'name': 'Guard & Grace Denver (second concept)',
        'type': 'Restaurant',
        'chain_scale': None, 'brand': None,
        'management': 'TAG Restaurant Group (Troy Guard)',
        'valet_operator': 'SOPHI (launching Q1 2027)',
        'tam': 200000.0,
        'was': 5.0,
        'pool': 'anchor',
        'v7_layer': 'hometown_displaced',
        'in_sam': True,
        'tam_notes': 'Added §4 refinement: SOPHI-committed second G&G concept Q1 2027.',
        'owner_group': None,
    },
    {
        'name': "Morton's the Steakhouse (Denver)",
        'type': 'Restaurant',
        'chain_scale': None, 'brand': None,
        'management': "Landry's (Morton's)",
        'valet_operator': 'VIP Parking Solutions',
        'tam': 200000.0,
        'was': 3.5,
        'pool': 'cold_sam',
        'v7_layer': None,
        'in_sam': True,
        'tam_notes': "Added §4 refinement: Named on VIP Parking Solutions' Denver client roster (vipparkingsolutions.com/valet-company-denver). Unlocks Y2 (2028) when VIP acquisition closes.",
        'owner_group': None,
    },
    {
        'name': "Maggiano's Little Italy (Denver)",
        'type': 'Restaurant',
        'chain_scale': None, 'brand': None,
        'management': "Brinker International",
        'valet_operator': 'VIP Parking Solutions',
        'tam': 180000.0,
        'was': 3.0,
        'pool': 'cold_sam',
        'v7_layer': None,
        'in_sam': True,
        'tam_notes': "Added §4 refinement: Named on VIP Parking Solutions' Denver client roster. Unlocks Y2 (2028).",
        'owner_group': None,
    },
    {
        'name': 'Linger (Denver)',
        'type': 'Restaurant',
        'chain_scale': None, 'brand': None,
        'management': 'Edible Beats (Justin Cucci)',
        'valet_operator': 'VIP Parking Solutions',
        'tam': 150000.0,
        'was': 3.5,
        'pool': 'cold_sam',
        'v7_layer': None,
        'in_sam': True,
        'tam_notes': "Added §4 refinement: Named on VIP Parking Solutions' Denver client roster (LoHi/Highland location). Unlocks Y2 (2028).",
        'owner_group': None,
    },
]

# ============================================================
# Expansion Growth Model — new market blocks (placeholder, not scored in canonical outputs)
# ============================================================

def build_expansion_market_block(market_key, market_name, state, accounts):
    """Build a market block for Houston/Detroit/South Bend in the same shape as existing markets."""
    tam = sum(a.get('tam', 0) for a in accounts)
    sam = sum(a.get('tam', 0) for a in accounts if a.get('in_sam'))
    return {
        'summary': {
            'market': market_name,
            'state': state,
            'tam': tam,
            'sam': sam,
            'y1_som': 0.0, 'y2_som': 0.0, 'y3_som': 0.0, 'y4_som': 0.0, 'y5_som': 0.0,
            'som_by_year': {f'y{y}': 0.0 for y in range(1, 6)},
            'acquisition_year_counts': {},
            'growth_model': 'acquisition',
        },
        'accounts': accounts,
    }

# Houston: G&G Q2 2027 + halo candidates
HOU_ACCOUNTS = [
    {
        'name': 'Guard & Grace Houston',
        'type': 'Restaurant',
        'chain_scale': None, 'brand': None,
        'management': 'TAG Restaurant Group (Troy Guard)',
        'valet_operator': 'SOPHI (launching Q2 2027)',
        'tam': 220000.0,
        'was': 5.0,
        'pool': 'anchor',
        'v7_layer': 'hometown_displaced',
        'in_sam': True,
        'tam_notes': 'Added §2.7 refinement: SOPHI-committed G&G Houston Q2 2027 launch.',
        'owner_group': None,
    },
    {
        'name': "Vic & Anthony's Steakhouse (Houston Downtown)",
        'type': 'Restaurant',
        'chain_scale': None, 'brand': None,
        'management': "Landry's",
        'valet_operator': None,
        'tam': 280000.0,
        'was': 3.5,
        'pool': 'cold_sam',
        'v7_layer': None,
        'in_sam': True,
        'tam_notes': 'Added §2.7 refinement: Houston halo candidate post-G&G (Josh Q5).',
        'owner_group': None,
    },
    {
        'name': 'Steak 48 (Houston)',
        'type': 'Restaurant',
        'chain_scale': None, 'brand': None,
        'management': 'Steak 48 / Sam Fox group',
        'valet_operator': None,
        'tam': 300000.0,
        'was': 3.5,
        'pool': 'cold_sam',
        'v7_layer': None,
        'in_sam': True,
        'tam_notes': 'Added §2.7 refinement: Houston halo candidate post-G&G (Josh Q5).',
        'owner_group': None,
    },
]

# Detroit: G&G Q3 2027 + halo
DET_ACCOUNTS = [
    {
        'name': 'Guard & Grace Detroit',
        'type': 'Restaurant',
        'chain_scale': None, 'brand': None,
        'management': 'TAG Restaurant Group (Troy Guard)',
        'valet_operator': 'SOPHI (launching Q3 2027)',
        'tam': 200000.0,
        'was': 5.0,
        'pool': 'anchor',
        'v7_layer': 'hometown_displaced',
        'in_sam': True,
        'tam_notes': 'Added §2.7 refinement: SOPHI-committed G&G Detroit Q3 2027 launch.',
        'owner_group': None,
    },
    {
        'name': 'Big Rock Italian Chophouse (Detroit)',
        'type': 'Restaurant',
        'chain_scale': None, 'brand': None,
        'management': 'Independent',
        'valet_operator': None,
        'tam': 200000.0,
        'was': 3.0,
        'pool': 'cold_sam',
        'v7_layer': None,
        'in_sam': True,
        'tam_notes': 'Added §2.7 refinement: Detroit halo candidate post-G&G (Josh Q5).',
        'owner_group': None,
    },
    {
        'name': 'The Whitney (Detroit)',
        'type': 'Restaurant',
        'chain_scale': None, 'brand': None,
        'management': 'Independent (Bud Liebler)',
        'valet_operator': None,
        'tam': 180000.0,
        'was': 3.5,
        'pool': 'cold_sam',
        'v7_layer': None,
        'in_sam': True,
        'tam_notes': 'Added §2.7 refinement: Detroit halo candidate post-G&G (Josh Q5). Historic mansion venue.',
        'owner_group': None,
    },
    {
        'name': 'Prime & Proper (Detroit)',
        'type': 'Restaurant',
        'chain_scale': None, 'brand': None,
        'management': 'Heirloom Hospitality',
        'valet_operator': None,
        'tam': 250000.0,
        'was': 3.5,
        'pool': 'cold_sam',
        'v7_layer': None,
        'in_sam': True,
        'tam_notes': 'Added §2.7 refinement: Detroit halo candidate post-G&G (Josh Q5 addition).',
        'owner_group': None,
    },
]

# South Bend: Courtyard t=0 anchor + halo
SBN_ACCOUNTS = [
    {
        'name': 'Courtyard by Marriott South Bend Downtown',
        'type': 'Hotel',
        'chain_scale': 'Upper Midscale',
        'brand': 'Courtyard',
        'management': 'Marriott',
        'valet_operator': 'SOPHI',
        'tam': 295000.0,  # Per Bryce Assumptions
        'was': 5.0,
        'pool': 'anchor',
        'v7_layer': 'hometown_displaced',
        'in_sam': True,
        'tam_notes': 'Added §2.7 refinement: SOPHI-actual t=0 (South Bend anchor).',
        'owner_group': None,
    },
    {
        'name': 'DoubleTree by Hilton South Bend',
        'type': 'Hotel',
        'chain_scale': 'Upscale',
        'brand': 'DoubleTree',
        'management': 'Hilton',
        'valet_operator': None,
        'tam': 200000.0,
        'was': 3.0,
        'pool': 'cold_sam',
        'v7_layer': None,
        'in_sam': True,
        'tam_notes': 'Added §2.7 refinement: South Bend halo (Bryce Assumptions R8 — Doubletree SB pipeline).',
        'owner_group': None,
    },
]

# ============================================================
# ENGINE — modified normalize_v3 that respects §2.8 flagship gate
# ============================================================

VIP_ACQUISITION_YEAR = 2  # VIP Parking Solutions closes Q1 2028 = Y2

def anchor_unlock(account, year, elite_acquired=True, vip_acquired_by_year=None):
    """Return True if a flagship hotel account is anchor-unlocked for the given year.

    Elite is acquired at start of Y1 (Q1 2027). VIP is acquired at start of Y2 (Jan 2028).
    """
    op = str(account.get('valet_operator') or '').lower()

    # SOPHI-actual t=0 anchor accounts
    if account.get('pool') == 'anchor':
        return True

    # v7 hometown_displaced (genuinely SOPHI-hometown, not auto-selected)
    if account.get('v7_layer') == 'hometown_displaced':
        return True

    # Elite Management operator — unlocked as of Y1 (Elite acquisition close)
    if elite_acquired and ('elite management' in op or 'elite parking' in op):
        if year >= 1:
            return True

    # VIP Parking Solutions operator — unlocked when VIP closes
    if vip_acquired_by_year is not None and 'vip parking solutions' in op:
        if year >= vip_acquired_by_year:
            return True

    return False


def run_penetration_v31(accounts, market_key, market_state):
    """v3.1 penetration engine with §2.8 flagship hotel gate.

    Otherwise identical to run_penetration in normalize_v3.py.
    """
    in_sam = [a for a in accounts if a.get('in_sam')]

    # Pre-compute
    for a in accounts:
        a['operator_gate'] = normalize_operator(a.get('valet_operator'))
        a['group_key'] = a.get('owner_group') or detect_ownership_group(a)
        a['acquisition_year'] = None
        a['gate_status'] = None
        a['group_wins_at_acquisition'] = 0
        a['flagship_hotel'] = is_flagship_hotel(a)
        for i in range(1, 6):
            a[f'y{i}'] = 0.0

    n_in_sam = len(in_sam)
    if n_in_sam == 0:
        return

    pen_curve = penetration_curve_for_market(market_key)
    # Use v3.1 cap table for new markets
    cap = MARKET_Y5_CAP_v31.get(market_key, 0.30)
    pen_curve = {y: (SCURVE_SHAPE[y] / SCURVE_SHAPE[5]) * cap for y in range(1, 6)}
    targets = {y: max(0, math.floor(n_in_sam * pen_curve[y])) for y in range(1, 6)}

    won = []
    won_by_group = Counter()
    won_by_vertical = set()

    cap_total = targets[5]
    forced_count = 0

    # 1) Anchors forced Y1
    anchors = [a for a in in_sam if a.get('pool') == 'anchor']
    anchors.sort(key=lambda a: -base_priority(a))
    for a in anchors:
        if forced_count >= cap_total:
            a['gate_status'] = 'anchor (cap-deferred — competes normally)'
            continue
        a['acquisition_year'] = 1
        a['gate_status'] = 'anchor: SOPHI-already/committed (forced Y1, counts toward cap)'
        forced_count += 1

    # 2) v7 forced, with §2.8 gate check for flagship hotels in Y1-Y2
    v7_accts = [a for a in in_sam
                if a.get('v7_layer') in V7_PRIORITY_BUMP
                and a['acquisition_year'] is None]
    v7_accts.sort(key=lambda a: -base_priority(a))
    for a in v7_accts:
        v7_target_year = 1 if a['v7_layer'] in ('hometown_displaced', 'hometown_was_boost') else 2

        # §2.8 flagship gate applied to v7 forced acquisitions
        if a.get('flagship_hotel') and v7_target_year <= 2:
            if not anchor_unlock(a, v7_target_year):
                a['gate_status'] = (
                    f'§2.8 flagship gate: {a["name"]} flagged as Upper Upscale/Luxury; '
                    f'no anchor unlock (operator={a.get("valet_operator","?")}); moved to Y3+ pool'
                )
                a['acquisition_year'] = None  # goes into general pool
                continue

        if forced_count >= cap_total:
            a['gate_status'] = f'v7_{a["v7_layer"]} (cap-deferred — competes normally)'
            continue
        a['acquisition_year'] = v7_target_year
        a['gate_status'] = f'v7_{a["v7_layer"]} (forced Y{v7_target_year}, counts toward cap)'
        forced_count += 1

    # Refresh state
    for a in in_sam:
        if a['acquisition_year'] is not None:
            won.append(a)
            if a.get('group_key'):
                won_by_group[a['group_key']] += 1
            if a.get('type'):
                won_by_vertical.add(a['type'])

    # 3) Year-by-year loop
    for year in range(1, 6):
        target_won = targets[year]
        already = sum(1 for a in in_sam if a['acquisition_year'] is not None and a['acquisition_year'] <= year)
        slots = target_won - already
        if slots <= 0:
            continue

        candidates = []
        for a in in_sam:
            if a['acquisition_year'] is not None:
                continue

            # §2.8 flagship gate check for Y1-Y2 selection
            if a.get('flagship_hotel') and year <= 2:
                if not anchor_unlock(a, year, elite_acquired=True, vip_acquired_by_year=VIP_ACQUISITION_YEAR):
                    a['gate_status'] = (
                        f'§2.8 flagship gate: Upper Upscale/Luxury blocked in Y{year} '
                        f'(operator={a.get("valet_operator","?")[:30]}); competes Y3+'
                    )
                    continue

            # Existing operator gate check
            gate_key = a.get('operator_gate')
            gate_ok = True
            gate_reason = None
            if gate_key and gate_key in OPERATOR_GATES:
                g = OPERATOR_GATES[gate_key]
                accts_won = len(won)
                verticals_won = len(won_by_vertical)
                if accts_won < g['min_accts'] or verticals_won < g['min_verticals']:
                    gate_ok = False
                    gate_reason = f"gated: {gate_key} unlock requires {g['min_accts']} accts / {g['min_verticals']} verticals (have {accts_won}/{verticals_won})"
            elif gate_key == 'other_regional':
                if len(won) < 3 or len(won_by_vertical) < 1:
                    gate_ok = False
                    gate_reason = f"gated: unknown regional operator"
            elif gate_key == 'elite':
                # Elite Management — light gate (§2.8 anchor_unlock handles flagships)
                if len(won) < 3 or len(won_by_vertical) < 1:
                    gate_ok = False
                    gate_reason = f"gated: Elite Management"

            if not gate_ok:
                a['gate_status'] = gate_reason
                continue

            base = base_priority(a)
            grp = a.get('group_key')
            grp_count = won_by_group[grp] if grp else 0
            mult = group_multiplier_for_count(grp_count) if grp else 1.0
            effective = base * mult
            candidates.append((effective, mult, grp_count, a))

        candidates.sort(key=lambda x: -x[0])
        for eff, mult, grp_count, a in candidates[:slots]:
            a['acquisition_year'] = year
            a['gate_status'] = (
                f"acquired Y{year} (priority {eff:.0f}, group×{mult:.1f})"
                if a.get('group_key') else
                f"acquired Y{year} (priority {eff:.0f})"
            )
            a['group_wins_at_acquisition'] = grp_count
            won.append(a)
            if a.get('group_key'):
                won_by_group[a['group_key']] += 1
            if a.get('type'):
                won_by_vertical.add(a['type'])

        for eff, mult, grp_count, a in candidates[slots:]:
            if a['acquisition_year'] is None:
                a['gate_status'] = (
                    f"in-pool, not yet acquired (priority {eff:.0f}, group×{mult:.1f})"
                    if a.get('group_key') else
                    f"in-pool, not yet acquired (priority {eff:.0f})"
                )

    # Apply revenue
    for a in in_sam:
        ay = a.get('acquisition_year')
        tam_annual = float(a.get('tam', 0) or 0)
        if ay is None:
            if not a.get('gate_status'):
                a['gate_status'] = 'not yet acquired in 5-yr window'
            continue
        for y in range(ay, 6):
            a[f'y{y}'] = tam_annual


# ============================================================
# MAIN
# ============================================================

def main():
    # Load current v3 output as baseline
    with open(HERE / 'accounts_v3.json') as f:
        data_v3 = json.load(f)

    # Baseline totals
    baseline = extract_totals(data_v3, tag='v3 (current live)')

    # Build v3.1 by copying v3 and applying refinements
    data_v31 = copy.deepcopy(data_v3)

    # ---- §4: Apply Elite corrections in Indianapolis ----
    ind_accounts = data_v31['markets']['indianapolis']['accounts']

    # 1) Strip hometown_displaced from Omni Severin + Conrad IND
    for a in ind_accounts:
        nm = a.get('name', '').lower()
        if 'omni severin' in nm or 'conrad indianapolis' in nm:
            if a.get('v7_layer') == 'hometown_displaced':
                a['v7_layer'] = None
                a['tam_notes'] = str(a.get('tam_notes', '') or '') + ' [§4 refinement: stripped hometown_displaced — not SOPHI-hometown; §2.8 flagship gate now applies]'

    # 2) Move Capital Grille IND from hometown_displaced (Y1) to ma_absorption (Y2 Elite)
    for a in ind_accounts:
        nm = a.get('name', '').lower()
        if nm == 'the capital grille' and a.get('v7_layer') == 'hometown_displaced':
            # Confirm this is IND Capital Grille (not Charlotte's)
            a['v7_layer'] = 'ma_absorption'
            a['pool'] = 'ma_sam'
            a['tam_notes'] = str(a.get('tam_notes', '') or '') + ' [§4 refinement: retagged from hometown_displaced (Y1) to ma_absorption (Y2 — Elite acquisition brings it)]'
            a['valet_operator'] = a.get('valet_operator') or 'Elite Management Services'

    # 3) Remove Eddie Merlot's from ma_absorption (not on Josh's Elite 6)
    for a in ind_accounts:
        nm = a.get('name', '').lower()
        if "eddie merlot" in nm and a.get('v7_layer') == 'ma_absorption':
            a['v7_layer'] = None
            a['pool'] = 'cold_sam'
            a['tam_notes'] = str(a.get('tam_notes', '') or '') + ' [§4 refinement: not on Josh-confirmed Elite 6 lineup; retagged to cold_sam]'

    # 4) Add new IND accounts (Hyde Park, Del Frisco's, InterContinental, Sheraton City Centre)
    for new_a in IND_ELITE_ADDITIONS:
        ind_accounts.append(new_a)

    # ---- §4: Apply Denver additions ----
    den_accounts = data_v31['markets']['denver']['accounts']
    for new_a in DEN_ADDITIONS:
        den_accounts.append(new_a)

    # ---- §2.7: Tag Phoenix/Cleveland/Louisville as expansion ----
    for mk in EXPANSION_MARKETS:
        data_v31['markets'][mk]['summary']['growth_model'] = 'expansion'
        data_v31['markets'][mk]['summary']['expansion_note'] = 'Moved to Expansion Growth Model per §2.7 canonical SOPHI 6 update. Not surfaced in Acquisition Growth Model outputs.'

    # ---- §2.7: Add new market blocks ----
    data_v31['markets']['houston']    = build_expansion_market_block('houston', 'Houston', 'COLD', HOU_ACCOUNTS)
    data_v31['markets']['detroit']    = build_expansion_market_block('detroit', 'Detroit', 'COLD', DET_ACCOUNTS)
    data_v31['markets']['south_bend'] = build_expansion_market_block('south_bend', 'South Bend', 'WARM', SBN_ACCOUNTS)

    # Tag acquisition markets
    for mk in ACQUISITION_MARKETS:
        if mk in data_v31['markets']:
            data_v31['markets'][mk]['summary']['growth_model'] = 'acquisition'

    # ---- Run refined engine on all acquisition markets ----
    for mk in ACQUISITION_MARKETS:
        if mk not in data_v31['markets']: continue
        m = data_v31['markets'][mk]
        run_penetration_v31(m['accounts'], mk, m['summary'].get('state', 'COLD'))
        # Recompute summary
        accts = m['accounts']
        y_som = {f'y{y}': sum(a.get(f'y{y}', 0) for a in accts) for y in range(1, 6)}
        m['summary']['y1_som'] = y_som['y1']
        m['summary']['y5_som'] = y_som['y5']
        m['summary']['som_by_year'] = y_som
        ay_counts = Counter(a.get('acquisition_year') for a in accts if a.get('in_sam'))
        m['summary']['acquisition_year_counts'] = {
            str(k) if k is not None else 'never': v for k, v in sorted(ay_counts.items(), key=lambda x: (x[0] is None, x[0]))
        }
        m['summary']['tam'] = sum(a.get('tam', 0) for a in accts)
        m['summary']['sam'] = sum(a.get('tam', 0) for a in accts if a.get('in_sam'))

    # Metadata
    data_v31['meta']['methodology'] = 'v3.1 (Sept 2026) — refinements: §2.7 canonical SOPHI 6 → Houston/Detroit/South Bend; §2.8 flagship hotel gate; §4 named accounts (Elite Q1 2027 corrections + VIP Q1 2028 additions)'
    data_v31['meta']['refinements_applied'] = ['§2.7 SOPHI 6 canonical update', '§2.8 flagship hotel gate', '§4 named accounts (Elite + VIP)']
    data_v31['meta']['flagship_keywords'] = list(FLAGSHIP_KEYWORDS)

    # Save v3.1
    with open(HERE / 'accounts_v3_1.json', 'w') as f:
        json.dump(data_v31, f, indent=2)

    # Compute diff
    v31_acquisition = extract_totals(data_v31, tag='v3.1 (refinements applied)', filter_growth_model='acquisition')
    v31_expansion = extract_totals(data_v31, tag='v3.1 expansion placeholder', filter_growth_model='expansion')

    # Print + save report
    report = build_report(baseline, v31_acquisition, v31_expansion, data_v3, data_v31)
    print(report)

    with open(HERE.parent / 'refinement_v3_1_report.md', 'w') as f:
        f.write(report)

    # Save diff json
    diff = {
        'baseline_v3': baseline,
        'v3_1_acquisition_model': v31_acquisition,
        'v3_1_expansion_placeholder': v31_expansion,
    }
    with open(HERE.parent / 'refinement_v3_1_diff.json', 'w') as f:
        json.dump(diff, f, indent=2, default=str)

    print(f"\n✓ Wrote {HERE / 'accounts_v3_1.json'}")
    print(f"✓ Wrote {HERE.parent / 'refinement_v3_1_report.md'}")
    print(f"✓ Wrote {HERE.parent / 'refinement_v3_1_diff.json'}")


def extract_totals(data, tag='', filter_growth_model=None):
    """Extract per-market + portfolio totals from a data dict."""
    result = {'tag': tag, 'markets': {}}
    port_y = {y: 0 for y in range(1, 6)}
    port_tam = port_sam = port_insam = port_won = 0
    for mk, m in data['markets'].items():
        if filter_growth_model and m['summary'].get('growth_model') != filter_growth_model:
            continue
        s = m['summary']
        y = s.get('som_by_year', {f'y{i}': 0 for i in range(1, 6)})
        ay = s.get('acquisition_year_counts', {})
        won = sum(v for k, v in ay.items() if k != 'never')
        insam = len([a for a in m['accounts'] if a.get('in_sam')])
        result['markets'][mk] = {
            'y1_som': y.get('y1', 0), 'y2_som': y.get('y2', 0),
            'y3_som': y.get('y3', 0), 'y4_som': y.get('y4', 0),
            'y5_som': y.get('y5', 0),
            'tam': s.get('tam', 0), 'sam': s.get('sam', 0),
            'in_sam': insam, 'won_y5': won,
            'acquisition_year_counts': ay,
        }
        for yi in range(1, 6):
            port_y[yi] += y.get(f'y{yi}', 0)
        port_tam += s.get('tam', 0)
        port_sam += s.get('sam', 0)
        port_insam += insam
        port_won += won
    result['portfolio'] = {
        'y1_som': port_y[1], 'y2_som': port_y[2], 'y3_som': port_y[3],
        'y4_som': port_y[4], 'y5_som': port_y[5],
        'cumulative_5yr': sum(port_y.values()),
        'tam': port_tam, 'sam': port_sam,
        'in_sam': port_insam, 'won_y5': port_won,
    }
    return result


def build_report(baseline, v31_acq, v31_exp, data_v3, data_v31):
    lines = []
    lines.append('# SOPHI Growth Engine v3.1 — Numeric Diff Report')
    lines.append('')
    lines.append('**DRAFT** — pending CFO advisor review. No PRs drafted, no live deal-room push. Data-layer diff only.')
    lines.append('')
    lines.append('## Portfolio-level diff')
    lines.append('')
    lines.append('| Metric | v3 (current live) | v3.1 Acquisition Growth Model | Δ ($) | Δ (%) |')
    lines.append('|---|---:|---:|---:|---:|')
    for label, key in [('Y1 SOM (2027)', 'y1_som'), ('Y2 SOM (2028)', 'y2_som'),
                        ('Y3 SOM (2029)', 'y3_som'), ('Y4 SOM (2030)', 'y4_som'),
                        ('Y5 SOM (2031)', 'y5_som'), ('5-yr cumulative', 'cumulative_5yr'),
                        ('TAM', 'tam'), ('SAM', 'sam')]:
        v0 = baseline['portfolio'].get(key, 0)
        v1 = v31_acq['portfolio'].get(key, 0)
        d = v1 - v0
        pct = (d / v0 * 100) if v0 else 0
        lines.append(f'| {label} | ${v0/1e6:,.2f}M | ${v1/1e6:,.2f}M | ${d/1e6:+,.2f}M | {pct:+.1f}% |')
    v0 = baseline['portfolio']['won_y5']; v1 = v31_acq['portfolio']['won_y5']
    lines.append(f'| Accounts won by Y5 | {v0} | {v1} | {v1-v0:+d} | — |')
    v0 = baseline['portfolio']['in_sam']; v1 = v31_acq['portfolio']['in_sam']
    lines.append(f'| Total in-SAM | {v0} | {v1} | {v1-v0:+d} | — |')

    lines.append('')
    lines.append('## Per-market diff')
    lines.append('')
    lines.append('| Market | Growth Model | v3 Y5 SOM | v3.1 Y5 SOM | Δ | v3 InSAM | v3.1 InSAM |')
    lines.append('|---|---|---:|---:|---:|---:|---:|')
    all_markets = sorted(set(list(baseline['markets'].keys()) + list(v31_acq['markets'].keys()) + list(v31_exp['markets'].keys())))
    for mk in all_markets:
        v0m = baseline['markets'].get(mk, {})
        v1m_acq = v31_acq['markets'].get(mk, {})
        v1m_exp = v31_exp['markets'].get(mk, {})
        v1m = v1m_acq if v1m_acq else v1m_exp
        model = 'Acquisition' if v1m_acq else ('Expansion' if v1m_exp else '(dropped)')
        v0_y5 = v0m.get('y5_som', 0)
        v1_y5 = v1m.get('y5_som', 0) if v1m else 0
        d = v1_y5 - v0_y5
        v0_ins = v0m.get('in_sam', '-')
        v1_ins = v1m.get('in_sam', '-') if v1m else '-'
        lines.append(f'| {mk} | {model} | ${v0_y5/1e6:.2f}M | ${v1_y5/1e6:.2f}M | ${d/1e6:+.2f}M | {v0_ins} | {v1_ins} |')

    lines.append('')
    lines.append('## Expansion Growth Model (placeholder)')
    lines.append('')
    lines.append('| Metric | Value |')
    lines.append('|---|---:|')
    for label, key in [('Y1 SOM', 'y1_som'), ('Y5 SOM', 'y5_som'),
                        ('5-yr cumulative', 'cumulative_5yr'), ('TAM', 'tam'), ('SAM', 'sam')]:
        v = v31_exp['portfolio'].get(key, 0)
        lines.append(f'| {label} | ${v/1e6:,.2f}M |')
    lines.append(f'| In-SAM accounts | {v31_exp["portfolio"]["in_sam"]} |')

    lines.append('')
    lines.append('## §2.8 flagship gate audit — which flagships moved out of Y1-Y2?')
    lines.append('')
    lines.append('| Market | Account | v3 acq_year | v3.1 acq_year | Reason |')
    lines.append('|---|---|:-:|:-:|---|')
    for mk in ACQUISITION_MARKETS:
        if mk not in data_v3['markets']: continue
        v3_accts = {a.get('name'): a for a in data_v3['markets'][mk]['accounts']}
        v31_accts = {a.get('name'): a for a in data_v31['markets'].get(mk, {}).get('accounts', [])}
        for nm, a3 in v3_accts.items():
            a31 = v31_accts.get(nm, {})
            if a3.get('type') != 'Hotel': continue
            if not is_flagship_hotel(a3): continue
            y3 = a3.get('acquisition_year')
            y31 = a31.get('acquisition_year')
            if y3 in (1, 2) and (y31 is None or y31 > 2):
                reason = 'flagship gate: no anchor unlock'
                lines.append(f'| {mk} | {nm} | Y{y3} | {"Y"+str(y31) if y31 else "never"} | {reason} |')
            elif y3 in (1, 2) and y31 in (1, 2):
                lines.append(f'| {mk} | {nm} | Y{y3} | Y{y31} | anchor unlocked (SOPHI actual / Elite / VIP) |')

    lines.append('')
    lines.append('## Named account additions')
    lines.append('')
    lines.append('### Indianapolis (Elite Q1 2027)')
    lines.append('| Account | TAM | Wave | Rationale |')
    lines.append('|---|---:|---|---|')
    for a in IND_ELITE_ADDITIONS:
        wave = a.get('v7_layer') or a.get('pool')
        lines.append(f'| {a["name"]} | ${a["tam"]:,.0f} | {wave} | {a["tam_notes"][:80]} |')

    lines.append('')
    lines.append('### Denver (VIP Q1 2028 + G&G committed)')
    lines.append('| Account | TAM | Operator | Rationale |')
    lines.append('|---|---:|---|---|')
    for a in DEN_ADDITIONS:
        op = a.get('valet_operator', '')[:30]
        lines.append(f'| {a["name"]} | ${a["tam"]:,.0f} | {op} | {a["tam_notes"][:80]} |')

    lines.append('')
    lines.append('### Expansion Growth Model (Houston/Detroit/South Bend)')
    for mk, accts in [('Houston', HOU_ACCOUNTS), ('Detroit', DET_ACCOUNTS), ('South Bend', SBN_ACCOUNTS)]:
        lines.append(f'\n**{mk}** — {len(accts)} accounts, TAM ${sum(a["tam"] for a in accts)/1e6:.2f}M')
        for a in accts:
            wave = 'anchor' if a.get('pool') == 'anchor' else 'halo'
            lines.append(f'  - {a["name"]} ({wave}) — TAM ${a["tam"]:,.0f}')

    lines.append('')
    lines.append('## What this diff does NOT include')
    lines.append('- No changes to `data.js` (front-end bundle) yet — needs `build_data_js_v3.py` rerun')
    lines.append('- No changes to investor-facing HTML pages')
    lines.append('- No changes to `METHODOLOGY.md` or `METHODOLOGY_v3.md`')
    lines.append('- No PRs drafted against either repo')
    lines.append('- Organic Growth Model curve ($1.72M 2027 → $11M 2031) is untouched')
    lines.append('')

    return '\n'.join(lines)


if __name__ == '__main__':
    main()
