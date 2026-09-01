# SOPHI TAM Rerun Playbook

**Purpose.** A self-contained protocol for adding a new market (or a new batch of accounts inside an existing market) to the SOPHI TAM universe. It captures the research inputs, the formulas, the locked assumptions, and the output artifacts so the model can be rerun by any operator without re-deriving methodology from scratch.

**Reference of record.** For deep rule justifications and full methodology history, see `sophi_methodology_export_v2.md` (the master v2 doc, 5,300 lines). Section refs are cited inline below (§X.Y). This playbook is the actionable checklist — the master doc is the audit trail.

**Related artifacts (locked).**
- v2 rollup: 6-market $150.3M TAM · $57.3M SAM (38.1%) · Y5 SOM $52.6M (35.0% of TAM, 91.8% of SAM), 3.12× Y1→Y5 growth
- v3 expansion: 14-market portfolio (originals + 8 expansion markets: Charleston, Cincinnati, Columbus, Fort Lauderdale, Fort Wayne, Minneapolis, Raleigh, St. Louis)
- v3 ad revenue overlay: moderate case (parking-lead + SMS), see `sophi_v3_ad_revenue_memo.md` and repo `/model/sophi_v3_ad_revenue_model.py`
- v3 ingest pipeline: `projects/financial-model-DBiYwBMdT12QJkLwoC2gAQ/files/tam_v3/_ingest_pipeline.py`

---

## The three research inputs required per account

For every new account added to the universe, you need three things:

1. **Valet operator** — who runs the valet stand today (in-house / regional 3PV / enterprise 3PV / bundled-preferred / none / unknown)
2. **Valet rate** — the daily overnight valet rate ($/day) at that property
3. **Estimated account TAM revenue** — computed from the two inputs above plus the account's size (rooms or seats) and geography

Everything else in the playbook (structural filters, WAS scoring, S-curves, capacity ramp) is deterministic once you have these three.

---

## Locked rules (do not change without explicit approval)

From methodology §5:

1. **Cold A Y1 capture = 40%** across all markets (LOCKED)
2. **TAM universe = hotels + qualifying restaurants only**. Hospitals / venues / airports are qualitative pipeline; $0 TAM contribution
3. **Restaurants: steakhouse or fine-dining ONLY, and must have ACTIVE INDEPENDENT VALET** (chain-branded corporate operators excluded)
4. **Restaurant valet conversion = 12.5%** (LOCKED)
5. **Restaurant operating days = 260/yr** (5 nights/wk) (LOCKED)
6. **Restaurant peak-modifier = +8%** (LOCKED)
7. **Hotel occupancy default = 60% flat**
8. **Hotel operating days = 360** (year minus 5-day slack)
9. **WAS never touches SAM** — WAS is a SOM-layer prioritizer only
10. **SAM/TAM ceiling ≤ 50%** — if any structural pool math produces SAM > 50% of TAM, apply a top-down haircut to SAM back to 50%
11. **SOPHI Global was acquired by Denison in 2019** — Denison is NOT SOPHI (do not confuse the two in operator research)
12. **Building status filter (v3 ingest):** keep only `Existing`, `Under Construction`, `Proposed`, `Final Planning`; exclude `Abandoned`, `Cancelled`, `On Hold`, `Deferred`, `Demolished`, `Converted`, `Under Renovation`, `Rumored`
13. **Extended-stay auto-exclude brands (structural filter):** Home2, Homewood, Hyatt House, SpringHill Suites, Element
14. **Top-5 nationals (enterprise pool):** LAZ, SP+ (SP Plus), Towne Park, Ace, Impark
15. **Preferred Parking-style bundled contracts** → partnership pool
16. **Micro filter:** account TAM < $150,000 → micro pool

---

## Step 1 — Build the research-target JSON

For each new account, write one JSON object into `research_targets.json` (batch file per market). Schema (methodology §B1):

```json
{
  "name": "string — MUST match the WAS_Scoring sheet spelling exactly",
  "type": "Hotel | Restaurant | Hospital | Venue | Casino | Airport | Commercial",
  "tam": null,
  "rooms": 372,
  "seats": null,
  "area": "Downtown | Cherry Creek | Scottsdale | ...",
  "address": "1200 W Market St, Indianapolis, IN 46204",
  "mgmt": "White Lodging (brand-mgmt company)",
  "known_valet_op": "Towne Park [source](https://linkedin.com/…)"
}
```

Notes:
- `tam` is left `null` at target-creation time — it is computed in Step 4.
- `rooms` / `seats` are mutually exclusive (hotel → rooms, restaurant → seats).
- `area` is a submarket string, not a lat/lon. It drives the downtown-vs-suburban split (Step 5).
- `known_valet_op` may be `null` on first pass; it gets filled during operator research (Step 2). Always include a markdown source link if a value is known.

**Example (from Indianapolis §B1):**
```json
{"name":"JW Marriott Indianapolis","type":"Hotel","tam":null,"rooms":1005,"area":"Downtown","address":"10 S West St, Indianapolis, IN 46204","mgmt":"White Lodging","known_valet_op":"Towne Park [source](https://linkedin.com/…)"}
```

---

## Step 2 — Operator research CSV

Fill `operator_research_<market>.csv` (one row per account). Schema (methodology §B2):

| Column | Values | Notes |
|---|---|---|
| `Account` | free text | Must match `name` in the JSON exactly |
| `Submarket` | Downtown / Cherry Creek / ... | Matches `area` |
| `Mgmt Company` | brand-mgmt company (owner/mgr) | White Lodging, Aimbridge, Pyramid, HEI, Highgate, StepStone, etc. |
| `Valet Operator` | canonical operator name or `in-house` / `none` / `unknown` | See canonical list below |
| `Valet Op Type` | `in-house` / `regional-3PV` / `enterprise-3PV` / `bundled-preferred` / `unknown` | |
| `Parking Bundled?` | `yes` / `no` / `unknown` | If yes → partnership pool candidate |
| `Structural Pool` | `anchor` / `partnership` / `enterprise` / `extended-stay` / `micro` / `cold-sam` / `unknown` | Assigned in Step 6 |
| `Confidence` | `high` / `med` / `low` | See evidence hierarchy below |
| `Sources` | comma-separated markdown links | Required for every non-`unknown` value |

**Canonical operator names** (use these exactly):
`Towne Park`, `LAZ Parking`, `SP+` (SP Plus), `Ace Parking`, `Impark`, `Propark`, `AAA Parking`, `Reimagined Parking`, `Republic Parking`, `Five Star Parking`, `ABM`, `REEF`, `Premier Parking`, `Elite Management Services`, `Peak Parking`, `Denison Parking` (⚠️ NOT SOPHI), `Parking Management Company` (PMC), `in-house`, `none`, `unknown`.

**Evidence hierarchy** (priority order — pick the highest-priority source available):
1. Hotel brand parking page (Marriott Bonvoy, Hilton Honors, Hyatt.com) — explicit valet rate + sometimes operator name
2. Operator career sites (Towne Park, LAZ, SP+, Propark careers) — confirms operator by property name
3. LinkedIn employees with title "Valet Attendant at [Hotel]" or "Valet Supervisor at [Hotel]"
4. Parking aggregators (ParkWhiz, SpotHero, BestParking, ParkMe) — rates only, not operator
5. Recent guest reviews (TripAdvisor, Google Reviews within last 12 months) — rates + occasional operator mention
6. Direct call to the property (fallback for high-value SAM accounts only)

**Confidence tiers:**
- `high` — operator confirmed via #1, #2, or #3 above; rate confirmed via #1 or hotel's own site
- `med` — operator inferred from brand-mgmt patterns (e.g., White Lodging + downtown Marriott full-service ⇒ ~90% Towne Park) plus at least one soft source
- `low` — best guess from market patterns, no direct evidence

**Example rows (from Indianapolis §B2):**
```csv
Account,Submarket,Mgmt Company,Valet Operator,Valet Op Type,Parking Bundled?,Structural Pool,Confidence,Sources
JW Marriott Indianapolis,Downtown,White Lodging,Towne Park,enterprise-3PV,no,enterprise,high,"[LinkedIn](https://linkedin.com/…), [Towne Park careers](https://townepark.com/careers/…)"
Bottleworks Hotel,Mass Ave,Bottleworks Hospitality,Peak Parking,bundled-preferred,yes,partnership,high,"[Peak Parking client list](https://peakparking.com/portfolio)"
Le Méridien Indianapolis,Downtown,StepStone Hospitality,in-house,in-house,no,partnership,high,"[Hotel website](https://…), [LinkedIn]"
Hotel Carmichael,Carmel,Parking Management Company,PMC,regional-3PV,no,cold-sam,med,"[PMC portfolio](https://…)"
St. Elmo Steak House,Downtown,Huse Culinary,Elite Management Services,regional-3PV,no,cold-sam,high,"[Elite website](https://…), [LinkedIn]"
Homewood Suites Downtown,Downtown,Hilton (brand-mgmt),Denison Parking,regional-3PV,no,extended-stay,high,"[Denison portfolio](https://…)"
```

---

## Step 3 — Valet rate research

For every account with a non-`none`/`unknown` operator, source a **daily overnight valet rate** ($/day).

**Sourcing ladder (in order):**
1. Hotel's own **parking/directions/FAQ page** (best — often quotes exact rate)
2. Marriott / Hilton / Hyatt **brand parking page** for the property
3. **Parking aggregators**: ParkWhiz, SpotHero, BestParking, ParkMe (rates only)
4. **Recent guest reviews** (last 12 months only — older rates are stale)
5. **Direct call** to the property (only for high-value SAM accounts if online sourcing fails)

**Rate benchmarks by tier** (from May 2026 enrichment across 8 markets, N=204):
- Portfolio median: **$42/day**
- 25th percentile: $30 | 75th percentile: $50
- Range: $0 (complimentary) to $67

**Fallback rate cards** (when no rate can be sourced — use as last resort, flag as `low` confidence):

| Tier | Trigger | Fallback Rate |
|---|---|---|
| Downtown luxury / convention | 4-5⭐, downtown, ≥400 rooms | $55/day |
| Downtown full-service | 4⭐, downtown, 300–399 rooms | $45/day |
| Downtown select-service | 3-4⭐, downtown, <300 rooms | $35/day |
| Suburban full-service | 4⭐, non-downtown, ≥250 rooms | $30/day |
| Suburban select-service | 3⭐, non-downtown, <250 rooms | $22/day |
| Steakhouse / fine-dining (any) | active indep valet | $18/day |

**Record the rate in `enrichment_<market>.csv` per the schema** (see Step 2's schema.json below):

```csv
name,market,address,valet_operator,valet_rate_daily,self_park_rate_daily,rate_evidence,brand_or_flag,management_company,ownership_group,rooms_or_seats,confidence,sources
Hotel Bennett,charleston,"404 King St, Charleston, SC",in-house,59,,"Hotel Bennett FAQ says $59 overnight valet",independent luxury,Salamander Collection,,179,high,"[Hotel Bennett FAQ](https://…)"
```

---

## Step 4 — Compute account-level TAM

**Hotel formula (§2):**
```
TAM_hotel = Rooms × Occupancy × ValetConv × ValetRate × 360
```
- Occupancy = 0.60 (LOCKED)
- ValetConv is tiered — see Step 5
- ValetRate from Step 3
- 360 = year minus 5-day slack (LOCKED)

**Restaurant formula (§2):**
```
TAM_restaurant = Seats × Turn × 0.125 × ValetRate × 260 × 1.08
```
- Turn = 2.0–2.5 covers/seat/night (concept-dependent; use 2.0 for fine-dining, 2.5 for steakhouse)
- 0.125 = 12.5% valet conversion (LOCKED)
- 260 = 5 nights/wk × 52 (LOCKED)
- 1.08 = +8% peak modifier (LOCKED)
- Applies ONLY to steakhouses / fine-dining with an active independent valet

**Non-target types → $0 TAM** (Hospital, Venue, Airport, Casino, Commercial). They enter the qualitative pipeline only.

**Example TAM computations** (Indianapolis §B1):
- JW Marriott Indianapolis: 1,005 rooms × 0.60 × 0.40 (downtown+convention) × $80 × 360 = **$6,946,560**
- Marriott Indianapolis Downtown: 622 rooms × 0.60 × 0.40 × $80 × 360 = **$4,299,264** (uses $79.86 exact)
- Hyatt Regency Indianapolis: 499 rooms × 0.60 × 0.40 × $80 × 360 = **$3,449,088**
- St. Elmo Steak House: 500 seats × 2.5 × 0.125 × $18.20 × 260 × 1.08 = **$265,781.25**
- Ruth's Chris Steak House: 300 seats × 2.5 × 0.125 × $22 × 260 × 1.08 = **$189,843.75** (approx)

---

## Step 5 — Hotel valet-conversion tiers

| Class | Trigger | ValetConv |
|---|---|---|
| Downtown + Convention | area = downtown AND rooms ≥ 400 | **40%** |
| Downtown Full-Service | area = downtown AND 300 ≤ rooms < 400 | **30%** |
| Downtown Select-Service | area = downtown AND rooms < 300 | **25%** |
| Suburban Full-Service | area ≠ downtown AND rooms ≥ 250 | **25%** |
| Suburban Select-Service | area ≠ downtown AND rooms < 250 | **20%** |

**"Downtown" definition** — one of: the central business district, convention-district hotel row, or any submarket the local market considers the primary anchor (e.g., Uptown Charlotte, Downtown Denver, Mass Ave in Indianapolis). Cherry Creek (Denver), Scottsdale (Phoenix), and Buckhead (Atlanta) are **not** downtown for this rule — they get suburban tiers.

---

## Step 6 — SAM structural filters (4 pools, no WAS)

Assign every hotel/restaurant to exactly ONE structural pool. Order of precedence (assign top-down):

1. **Micro Pool** — Account TAM < $150,000 → drops out of SAM (goes to `micro`)
2. **Extended-stay Pool** — Brand ∈ {Home2, Homewood, Hyatt House, SpringHill, Element} → drops out of SAM (goes to `extended-stay`)
3. **Enterprise Pool** — Valet operator ∈ {LAZ, SP+, Towne Park, Ace, Impark} → in SAM as `enterprise` (structural blocker: enterprise contracts are hard to displace without a national play)
4. **Partnership Pool** — Parking Bundled = yes AND operator is bundled-preferred (Preferred Parking style, Peak Parking-style regional bundles) → in SAM as `partnership` (structural blocker: bundled into management contract)

**Everything else** → `cold-sam` (the addressable SAM). In-house valet, unknown-operator, and regional 3PV accounts that don't fit the four pools above are the primary sales targets.

**Pool → SAM contribution:**
- `micro`, `extended-stay` → **excluded from SAM**
- `enterprise`, `partnership` → **counted in SAM** but structurally slower (feed into Warm A / Warm B in the SOM layer, not Cold A)
- `cold-sam` → **primary SAM**, feeds Cold A

---

## Step 7 — Apply the 50% SAM/TAM ceiling

After summing SAM across all pools that count toward SAM, check:

```
if SAM_total > 0.50 × TAM_total:
    haircut_ratio = (0.50 × TAM_total) / SAM_total
    apply haircut_ratio to each in-SAM account's SAM contribution proportionally
```

Report both pre-haircut and post-haircut SAM in the market memo. If a haircut is applied, note the ratio and which pool(s) were most affected.

---

## Step 8 — WAS scoring for SOM (SOM-layer only)

WAS (Weighted Account Score) is the **SOM prioritizer**. It never touches TAM or SAM totals — it only decides ORDER of pursuit within Cold A and the boosts for higher-priority accounts.

**WAS components** (methodology §A3):
- Structural fit (0–5)
- Market density / walk-in adjacency (0–5)
- Operator switchability (0–5)
- Rate ceiling headroom (0–5)
- Ownership-group priority (0–5)

Compute WAS as the weighted average per the master doc's rubric, then bucket:

| Tier | WAS score | Y1 capture boost |
|---|---|---|
| A | ≥ 4.00 | +1.00 |
| B | 3.40–3.99 | +0.50 |
| C | 2.80–3.39 | +0.30 |
| D | < 2.80 | +0.15 |

**Tiered ownership boost** (applied additively on top of the base Cold A 40% Y1 capture): a Tier-A account in `cold-sam` gets `40% + 1.0pp = 41%` Y1 capture, etc. (Yes, small — the 40% base is the dominant driver; WAS is a tiebreaker for sequencing, not a big lever.)

---

## Step 9 — S-curves (Y1–Y5 capture progression)

| Cohort | Y1 | Y2 | Y3 | Y4 | Y5 |
|---|---|---|---|---|---|
| **Cold A** (cold-sam accounts) | 40% | 50% | 70% | 85% | 95% |
| **Warm A** (enterprise + partnership pool converts) | 50% | 65% | 80% | 90% | 95% |
| **PMC Gate** (portfolio mgmt company national plays) | 30% | 50% | 70% | 85% | 95% |

Apply per account: `Account SOM_Y_n = Account SAM × cohort_curve[n] × (1 + WAS_boost/100)` (WAS boost expressed as pp, converted to fraction). Sum across accounts for market SOM per year.

---

## Step 10 — Capacity ramp (staffing constraint)

The BDR/AM team can onboard only so many accounts per year. This is the **hard cap** — market TAM can be huge, but if the team can only take on 6 accounts in Y1, that's the ceiling for Y1 wins across ALL markets combined.

| Year | New accounts onboarded | Cumulative live |
|---|---|---|
| Y1 | 6 | 6 |
| Y2 | 8 | 14 |
| Y3 | 9 | 23 |
| Y4 | 10 | 33 |
| Y5 | 10 | 43 |

If aggregate SOM implies more accounts than the ramp allows, apply a top-down cap and re-sequence by WAS rank across all markets. This is the constraint that turns TAM × capture into ACTUAL bookable revenue.

---

## Step 11 — Ingest into the v3 pipeline (mechanical)

Once research is complete, the v3 pipeline (`projects/financial-model-…/files/tam_v3/_ingest_pipeline.py`) does the mechanical work:

1. Drop the new-account uploads (CoStar/LE-style exports) into `uploaded_attachments/<batch-id>/`
2. Drop the enrichment CSV into `enrichment/enriched_csvs/<market>_enrichment.csv`
3. Run the ingest — it:
   - Normalizes account types (§ACCOUNT_TYPE_REMAP)
   - Filters by building status (§BUILDING_STATUS_KEEP)
   - Routes to canonical markets (§UPLOAD_MARKET_TO_CANONICAL + CITY_TO_MARKET)
   - Reconciles against originals via Jaccard name matching (threshold 0.6)
   - Merges enrichment fields into the canonical 34-column Accounts schema
   - Writes one `TAM_<Market>_v3.xlsx` per market with sheets: `Accounts`, `Related_Entities`, `Excluded_Status`, `Ingest_Log`
4. Run TAM/SAM/SOM computation on the reconciled `Accounts` sheet using Steps 4–10 above
5. Write market memo (`<market>_tam_refined_memo.md`) with headline numbers + audit trail

---

## Example workflow: adding "Nashville" to the universe

1. **Pull the raw universe** — CoStar/LE-style export for Nashville (all hospitality). Save to `uploaded_attachments/<batch>/Nashville.xlsx`.
2. **Filter** — keep hotels (all classes) + steakhouses / fine-dining. Building Status ∈ {Existing, UC, Proposed, Final Planning}. Expect ~80–120 primary accounts.
3. **Build `research_targets_nashville.json`** — one JSON object per account per Step 1 schema.
4. **Operator research** — for each account, work down the evidence hierarchy in Step 2. Populate `operator_research_nashville.csv`. Target: ≥60% high-confidence coverage across the top 30% of accounts by rooms/seats.
5. **Rate research** — Step 3 sourcing ladder. Fill `enrichment_nashville.csv`.
6. **Compute account TAM** — apply Step 4 formulas with Step 5 tiers. Sanity-check against benchmarks: downtown 4⭐ hotel ≈ $2–4M; downtown 5⭐ / convention ≈ $5–8M; steakhouse ≈ $150–300K.
7. **Assign structural pools** — Step 6, in the order listed.
8. **Sum SAM** — apply Step 7 ceiling if triggered.
9. **Compute WAS** — Step 8 rubric. Bucket to A/B/C/D.
10. **Apply S-curves × capacity** — Steps 9–10.
11. **Write `nashville_2026_scored_v5.xlsx`** with tabs: `Universe`, `WAS_Scoring`, `TAM_Conservative`, `SAM_Structural`, `SOM_Buildout`, `Memo`.
12. **Update rollup** — append Nashville numbers to `sophi_Nmarket_rollup.xlsx`; regenerate rollup memo.
13. **Commit** to `sophi-deal-room` under `/model/tam_v3/`.

---

## File output locations & naming conventions

**Workspace paths:**
- `research_targets_<market>.json` → per-market target list (Step 1)
- `operator_research_<market>.csv` → operator lookup (Step 2)
- `enrichment/enriched_csvs/<market>_enrichment.csv` → rates + evidence (Step 3)
- `<market>_2026_scored_v5.xlsx` → the market workbook (canonical output)
- `<market>_tam_refined_memo.md` → market memo (audit trail)
- `sophi_Nmarket_rollup.xlsx` + `sophi_Nmarket_rollup_memo.md` → portfolio roll-up

**Repo paths (`sophi-deal-room`):**
- Source: `/model/tam_v3/<market>_scored_v5.xlsx`
- Methodology: `/methodology/sophi_tam_rerun_playbook.md` (this file)
- Data JSON (for the deal room UI): `/src/accounts_v3_<N>mkt_json`

**Naming rules:**
- Markets: hyphenated proper case (`Raleigh-Durham`, `Greensboro-Winston-Salem`, `Saint Louis`, `Fort Wayne`, `Fort Lauderdale`)
- Years in filenames: the year of the underlying data pull (`_2026_`), not the model version
- Model version suffix: `v5` current; bump when methodology changes (not when new markets are added)

---

## Version history

- **v1** (Feb 2026) — Original 6-market build (South Bend, Charlotte, Indianapolis, Denver, Houston, Detroit)
- **v2** (Mar–Apr 2026) — 6-market rollup with locked assumptions (Cold A 40%, 50% ceiling, restaurant rules)
- **v3** (May–Aug 2026) — 14-market expansion (added Charleston, Cincinnati, Columbus, Fort Lauderdale, Fort Wayne, Minneapolis, Raleigh, St. Louis); ad-revenue overlay (moderate case); operator xref + self-park repricing memos
- **This playbook (Sep 2026)** — Codifies v3 rerun protocol for future markets

---

**Source of truth:** `sophi_methodology_export_v2.md` (master v2 doc). This playbook is the operational checklist; when in doubt, defer to the master doc.
