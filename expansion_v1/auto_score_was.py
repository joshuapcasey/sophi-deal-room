"""
auto_score_was.py — Deterministic v2 WAS rubric auto-scorer for expansion markets.

Encodes the patterns observed in shipped scored XLSX files (Charlotte, Denver,
Phoenix, Indianapolis) and applies a COLD-market addressability dampener so that
properties without local anchor proof points score realistically (resolving the
"Diplomat Beach Resort wins Y1" issue).

Sub-scores (0-5):
  Fit         (25%) — hotel/restaurant quality fit for SOPHI valet model
  Size        (25%) — TAM banding
  Owner Base  (20%) — independent vs portfolio vs REIT
  Addr        (15%) — operator lock + market state (cold = harder access)
  Adj         (15%) — downtown / co-located dependency

Plus relationship lift (additive, capped 5.0):
  Current operator group:    +1.00
  Historical operator group: +0.50
  Brand familiarity (cur):   +0.30  (Hilton, Marriott, Hyatt, IHG family)
  Brand familiarity (hist):  +0.15

Tier thresholds: A>=4.0, B>=3.4, C>=2.8, D<2.8

USAGE:
  python3 auto_score_was.py                  # scores all 14 markets
  python3 auto_score_was.py --new-only       # scores only the 8 expansion markets
"""

import json, sys
from pathlib import Path

V2_PATH = Path('/home/user/workspace/sophi-market-map/src/accounts_v2_14mkt.json')

# Markets that are WARM (>=3 SOPHI anchors); all others COLD.
WARM_MARKETS = {'charlotte'}  # Per existing v2 methodology — only Charlotte is WARM today
NEW_MARKETS = {'ft_wayne','cincinnati','columbus','minneapolis','st_louis',
               'raleigh','charleston','ft_lauderdale'}

# Brand families for relationship lift (current = SOPHI has direct relationship; we
# treat brand familiarity as +0.15 historical-only since SOPHI doesn't manage these brands)
BRAND_FAMILY_HISTORICAL = {
    'marriott': 'marriott_family',
    'sheraton': 'marriott_family',
    'westin': 'marriott_family',
    'w hotel': 'marriott_family',
    'le meridien': 'marriott_family',
    'le méridien': 'marriott_family',
    'aloft': 'marriott_family',
    'autograph': 'marriott_family',
    'jw marriott': 'marriott_family',
    'ritz-carlton': 'marriott_family',
    'courtyard': 'marriott_family',
    'fairfield': 'marriott_family',
    'springhill': 'marriott_family',
    'residence inn': 'marriott_family',
    'ac hotel': 'marriott_family',
    'element': 'marriott_family',
    'tribute portfolio': 'marriott_family',
    'gaylord': 'marriott_family',
    'hilton': 'hilton_family',
    'hilton garden inn': 'hilton_family',
    'doubletree': 'hilton_family',
    'embassy suites': 'hilton_family',
    'hampton': 'hilton_family',
    'home2': 'hilton_family',
    'homewood': 'hilton_family',
    'tru by hilton': 'hilton_family',
    'curio': 'hilton_family',
    'canopy': 'hilton_family',
    'tapestry': 'hilton_family',
    'waldorf': 'hilton_family',
    'conrad': 'hilton_family',
    'lxr': 'hilton_family',
    'hyatt': 'hyatt_family',
    'andaz': 'hyatt_family',
    'park hyatt': 'hyatt_family',
    'thompson': 'hyatt_family',
    'grand hyatt': 'hyatt_family',
    'hyatt regency': 'hyatt_family',
    'hyatt place': 'hyatt_family',
    'hyatt house': 'hyatt_family',
    'unbound collection': 'hyatt_family',
    'ihg': 'ihg_family',
    'intercontinental': 'ihg_family',
    'kimpton': 'ihg_family',
    'crowne plaza': 'ihg_family',
    'holiday inn': 'ihg_family',
    'staybridge': 'ihg_family',
    'candlewood': 'ihg_family',
    'voco': 'ihg_family',
    'hotel indigo': 'ihg_family',
}

# Operators that act as enterprise locks (already excluded from SAM, but for
# accounts that snuck through we still penalize Addressability)
LOCKED_OPERATORS = ['towne park', 'park inc']
HARD_OPERATORS  = ['laz', 'sp+', 'abm', 'ace parking', 'metropolis', 'reef']
LIGHT_OPERATORS = ['propark', 'pmc', 'parkwell', 'preferred', 'epic']
INHOUSE_MARKERS = ['in-house', 'in house', 'self-park', 'hotel-managed',
                   'marriott-managed', 'hyatt-managed', 'hotel managed',
                   'managed by', 'self park']


def detect_brand_family(name):
    n = (name or '').lower()
    # Order matters — most specific first
    for kw in sorted(BRAND_FAMILY_HISTORICAL.keys(), key=lambda k: -len(k)):
        if kw in n:
            return BRAND_FAMILY_HISTORICAL[kw]
    return None


def score_fit(account):
    """Fit (1-5): how well does SOPHI's valet model match this property?"""
    typ = account.get('type', '')
    name = (account.get('name') or '').lower()

    if typ == 'Restaurant':
        seats = account.get('seats') or 0
        # Steakhouse / fine dining = 5; mid-tier = 4; casual = 3
        if any(k in name for k in ['capital grille','ruth\'s chris','ruth chris','st. elmo',
                                    'st elmo','prime','del frisco','morton','sullivan',
                                    'fleming','steakhouse','mastro','bourbon steak']):
            return 5
        if seats >= 200:
            return 4
        if seats >= 100:
            return 3
        return 2

    if typ == 'Hotel':
        rooms = account.get('rooms') or 0
        # Ultra-luxury / convention anchors
        if any(k in name for k in ['four seasons','ritz-carlton','ritz carlton','st. regis',
                                    'st regis','waldorf','park hyatt','mandarin oriental',
                                    'edition','peninsula','rosewood','aman']):
            return 5
        # Full-service / convention HQ
        if any(k in name for k in ['marriott','sheraton','hilton','hyatt regency','westin',
                                    'jw marriott','intercontinental','grand hyatt',
                                    'conrad','signia','le meridien','le méridien','omni',
                                    'gaylord','seminole hard rock','diplomat']) and rooms >= 200:
            return 5
        if any(k in name for k in ['marriott','sheraton','hilton','hyatt','westin','intercontinental','omni','crowne plaza']):
            return 4
        # Select-service / branded mid-tier
        if any(k in name for k in ['courtyard','fairfield','springhill','residence inn',
                                    'hampton','hilton garden inn','doubletree','aloft',
                                    'hyatt place','hyatt house','holiday inn','element',
                                    'home2','homewood','candlewood','staybridge',
                                    'tru by hilton','autograph','curio','canopy',
                                    'tapestry','tribute','indigo','kimpton','ac hotel',
                                    'moxy','aloft','element']):
            return 4 if rooms >= 150 else 3
        # Boutique / independent
        if rooms >= 100:
            return 3
        if rooms >= 50:
            return 2
        return 2  # tiny boutique

    return 2  # default


def score_size(tam):
    """Size (1-5): TAM banding (matches v2 patterns)."""
    if tam >= 2_000_000:  return 5
    if tam >= 1_000_000:  return 4
    if tam >= 500_000:    return 3
    if tam >= 150_000:    return 2
    return 1


def score_owner_base(account):
    """Owner Base (1-5): relationship leverage potential.

    Higher = portfolio with multiple properties; lower = single-property indie.
    Matches Charlotte patterns: independent indie/Marriott single-flag = 2,
    multi-property mgmt company = 3, REIT/branded portfolio with sister =3.
    """
    mgmt = (account.get('management') or '').lower()
    own = (account.get('ownership_group') or '').lower()
    name = (account.get('name') or '').lower()

    # Major hotel brands managed properties (Marriott-managed, Hilton-managed) = 3
    if any(k in mgmt for k in ['marriott','hilton','hyatt','ihg','crescent','sage',
                                'pyramid','aimbridge','remington','white lodging',
                                'aparium','stonebridge','driftwood','hcw','paragon',
                                'davidson','interstate','highgate','hersha']):
        return 3
    if any(k in own for k in ['portfolio','reit','partners','ventures','holdings','group','llc']):
        return 3
    # Restaurants that are part of named groups (Darden, Huse, Elite) = 3
    if any(k in name for k in ['capital grille','ruth\'s chris','ruth chris','st. elmo',
                                'st elmo','harry & izzy','olive garden','longhorn',
                                'seasons 52','yard house','bahama breeze']):
        return 3
    # Independent / single-property
    return 2


def score_addressability(account, market_state, market_key):
    """Addressability (1-5): how reachable is the decision-maker?

    Adjusted by:
      - Operator lock (Towne Park = 1; LAZ/SP+ = 2; PMC = 3; in-house = 5; none = 4)
      - Cold market dampener: in COLD markets, cap at 4 (no warm intros)
      - New-market dampener: even tighter cap at 3 for non-independent properties
        (no proof points, no anchor, no co-located reference)
    """
    op = (account.get('valet_operator') or '').lower()
    is_cold = market_state == 'COLD'
    is_new_market = market_key in NEW_MARKETS

    # Operator-driven base
    if any(o in op for o in LOCKED_OPERATORS):
        base = 1  # Towne Park enterprise lock
    elif any(o in op for o in HARD_OPERATORS):
        base = 2  # LAZ/SP+/ABM hard gates
    elif any(o in op for o in LIGHT_OPERATORS):
        base = 3  # PMC/Propark light
    elif any(m in op for m in INHOUSE_MARKERS):
        base = 5  # In-house valet — easiest decision-maker access
    elif op.strip() in ('','none','-','tbd','independent','unknown'):
        base = 4  # Independent or unknown — assume hotel-managed direct access
    else:
        base = 3

    # COLD-market dampener: no anchor proof points
    if is_cold:
        base = min(base, 4)
    # NEW-market dampener: zero proof points, zero local relationships
    # Only independent / in-house properties retain higher scores
    if is_new_market:
        if base > 3 and base < 5:
            base = 3  # cap branded-managed properties at 3 in new markets
        elif base == 5:
            base = 4  # in-house: still strong but no warm intro yet

    return base


def score_adjacency(account, market_state, market_key):
    """Adjacency (1-5): co-located dependencies, downtown anchor effects.

    Charlotte pattern: downtown hotel without operator lock = 4; non-downtown = 2;
    co-located w/ stadium/convention = 4-5
    """
    notes = (account.get('location_notes') or '').lower()
    addr = (account.get('address') or '').lower()
    name = (account.get('name') or '').lower()

    # Strong adjacency markers — convention HQ, stadium-co-located, beachfront
    if any(k in notes for k in ['convention','stadium','arena','co-located','attached',
                                 'connected','skywalk','adjacent','airport','cruise',
                                 'beachfront','beach access','oceanfront','waterfront']):
        # In a NEW cold market we don't yet have proof from these adjacencies
        if market_key in NEW_MARKETS:
            return 3  # adjacency present but not yet leveraged
        return 4
    # Downtown
    if 'downtown' in notes or 'downtown' in addr:
        if market_key in NEW_MARKETS:
            return 3
        return 4
    # Co-located with major hospital / corporate campus
    if any(k in notes for k in ['hospital campus','corporate campus','medical center']):
        return 3
    # Suburban / standalone
    return 2


def relationship_lift(account):
    """Additive lift, capped at 5.0 final WAS."""
    name = account.get('name') or ''
    family = detect_brand_family(name)
    op = (account.get('valet_operator') or '').lower()

    lift = 0.0
    tag = []
    # SOPHI as current operator (won't trigger in new markets, but kept for completeness)
    if 'sophi' in op:
        lift += 1.00
        tag.append('SOPHI current operator (+1.0)')
    # Brand familiarity historical (SOPHI has worked with brand-family properties before)
    if family:
        lift += 0.15
        tag.append(f'Brand familiarity (historical): {family} (+0.15)')

    return lift, '; '.join(tag) if tag else ''


def compute_was(account, market_state, market_key):
    fit = score_fit(account)
    size = score_size(float(account.get('tam') or 0))
    own = score_owner_base(account)
    addr = score_addressability(account, market_state, market_key)
    adj = score_adjacency(account, market_state, market_key)
    raw = fit * 0.25 + size * 0.25 + own * 0.20 + addr * 0.15 + adj * 0.15

    lift, tag = relationship_lift(account)
    final = min(5.0, raw + lift)

    return {
        'fit': fit, 'size': size, 'owner_base': own, 'addr': addr, 'adj': adj,
        'was_base': round(raw, 3),
        'was_boost': round(lift, 3),
        'was': round(final, 3),
        'tier': tier_for(final),
        'lift_tag': tag,
    }


def tier_for(was):
    if was >= 4.0: return 'A'
    if was >= 3.4: return 'B'
    if was >= 2.8: return 'C'
    return 'D'


def main():
    new_only = '--new-only' in sys.argv
    with open(V2_PATH) as f:
        data = json.load(f)

    counts_by_market = {}
    for mk, m in data['markets'].items():
        # Only re-score new markets (existing 6 already have hand-scored WAS)
        if new_only and mk not in NEW_MARKETS:
            continue
        if mk not in NEW_MARKETS and mk not in WARM_MARKETS and mk not in {'phoenix','denver','indianapolis','cleveland','louisville','charlotte'}:
            continue
        # Skip existing 6 by default — preserve hand-scored WAS
        if mk not in NEW_MARKETS:
            continue

        state = m['summary'].get('state', 'COLD')
        tier_count = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'no_score': 0}
        for a in m['accounts']:
            # Only score in-SAM accounts (out-of-SAM stays WAS=null per v2)
            if not a.get('in_sam'):
                a['was'] = None
                a['was_base'] = None
                a['was_boost'] = None
                tier_count['no_score'] += 1
                continue
            scores = compute_was(a, state, mk)
            a['was'] = scores['was']
            a['was_base'] = scores['was_base']
            a['was_boost'] = scores['was_boost']
            a['was_fit'] = scores['fit']
            a['was_size'] = scores['size']
            a['was_owner_base'] = scores['owner_base']
            a['was_addr'] = scores['addr']
            a['was_adj'] = scores['adj']
            a['was_lift_tag'] = scores['lift_tag']
            a['tier'] = scores['tier']
            tier_count[scores['tier']] += 1
        counts_by_market[mk] = tier_count

    # Write back
    with open(V2_PATH, 'w') as f:
        json.dump(data, f, indent=2, default=str)

    print(f'Auto-scored WAS for {len(counts_by_market)} markets ({"new only" if new_only else "all"}):')
    print(f'{"Market":15s}  A    B    C    D    no_score')
    for mk, tc in counts_by_market.items():
        print(f'  {mk:14s}  {tc["A"]:3d}  {tc["B"]:3d}  {tc["C"]:3d}  {tc["D"]:3d}  {tc["no_score"]:3d}')

    # Sanity sample: show top 5 highest-WAS hotels in each new market
    print('\n=== Top 3 WAS in each new market ===')
    for mk in NEW_MARKETS:
        accts = [a for a in data['markets'][mk]['accounts'] if a.get('was') is not None]
        accts.sort(key=lambda a: -a['was'])
        print(f'\n{mk}:')
        for a in accts[:3]:
            print(f'  WAS={a["was"]:.2f} ({a["tier"]})  {a["name"][:45]:45s}  '
                  f'TAM=${a["tam"]/1e6:.2f}M  Fit={a["was_fit"]} Sz={a["was_size"]} '
                  f'Own={a["was_owner_base"]} Addr={a["was_addr"]} Adj={a["was_adj"]} +{a["was_boost"]}')


if __name__ == '__main__':
    main()
