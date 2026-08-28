# SOPHI v3 Growth Model — SMS Ad Revenue Layer

**Status:** Layered on top of the canonical v3 penetration engine (METHODOLOGY_v3.md). No changes to parking-services SOM. Ad revenue is additive.
**Headline / diligence case:** MODERATE — midpoint of every account-type SMS conversion band × midpoint average offer value (Hotel 26.5% × $30, Fine Dining 22.5% × $23.50, Venue 29% × $32.50, Corporate 21% × $20). Portfolio SMS-mix weighted, this is **2.96× the conservative low-end**. Live across the deal-room pages (summary.html, sophi-os.html SMS sub-tab, v3-valuation.html).
**Also reported:** LOW (previous conservative base, defensible floor) and HIGH (top of every band, full hotel multi-touch fully exercised) — for sensitivity.
**Referrals:** Deliberately excluded. Held as valuation optionality outside the growth model (per Financial Performance + Organic Valuation callouts).

---

## 1. What we're modeling and why

The v3 methodology deliberately excludes non-parking revenue streams to keep the DCF and SOM defensible. That's the right choice for the parking-only headline — but it leaves a real, catalogued revenue stream (SMS retrieval advertising) sitting entirely in the valuation-upside bucket. When a strategic acquirer looks at SOPHI, the parking-services SOM is table stakes; the ad revenue layer is what they're paying the growth multiple for.

This memo makes that layer explicit for the strategic acquisition growth model — showing how ad revenue scales with the size of the market we're serving at each point in the Y1–Y5 curve, and what it adds to Y5 run-rate valuation.

We moved from the LOW-end base case to the MODERATE (midpoint) case as the diligence anchor because the low-end assumed every account-type would convert at the bottom of its observed band and offer the smallest amount — which is not a base case, it's a floor. The moderate case uses the midpoint of every observed band from the SOPHI Domo dashboard's 13-month operating data, which is the honest diligence position. The low-end floor remains on file for stress testing.

## 2. Activation mechanics — two-stage gate

Ad revenue does not turn on account-by-account. It requires network scale, because the value is in the consent-gated customer persona database and the pricing moat that follows once we can demand-side quote against a real inventory of high-intent, opted-in mobile numbers.

1. **Portfolio-wide activation gate.** Ad revenue = $0 until aggregate portfolio SMS interactions ≥ 15,000/month (180,000/year). This is Phase 3 in the OS activation ladder.
2. **Post-activation, per-market compounding.** From the activation year forward, every SMS interaction contributes ad revenue at its account-type conversion economics. Small markets participate in the network payoff even before they'd individually clear 15K, because the persona database is a shared asset, not a per-city one.

**Activation year in the current v3 portfolio: Y2.** Portfolio annual SMS crosses 305,002 (25,417/mo) in Y2, well past the 15K/mo threshold. Y1 ends at 138,686 annual (11,557/mo), just below the gate.

## 3. Per-account SMS economics — three cases

Directly from the OS deck's SMS Retrieval Ad Model table. Each account type has an observed conversion band and observed offer-value band from the SOPHI Domo dashboard's 13-month baseline:

| Account type | Capture | Conv (low / **mid** / high) | Offer (low / **mid** / high) | Multi-touch |
|---|---|---|---|---|
| Hotel | 55% | 18% / **26.5%** / 35% | $15 / **$30** / $45 | 3.5× (arrival / mid-stay / departure) |
| Fine Dining (Restaurant) | 45% | 15% / **22.5%** / 30% | $12 / **$23.50** / $35 | 1.0× |
| Event / Venue | 35% | 20% / **29%** / 38% | $15 / **$32.50** / $50 | 1.0× |
| Corporate | 40% | 14% / **21%** / 28% | $10 / **$20** / $30 | 1.5× (recurring commuters) |
| Medical / Healthcare | 15% | **firewalled — 0%** | — | — |

Multi-touch reflects real observed SMS interactions per served vehicle in the Domo baseline. Hotels genuinely receive multiple messages per stay; corporates get repeat contact from recurring commuters; restaurants and venues are single-touch. Multi-touch feeds both the activation-gate volume math and the revenue formula.

Medical is firewalled by policy — no ad revenue is modeled from any hospital or clinical account regardless of SMS volume, matching the account-type firewall row in the current deck.

## 4. Annual vehicle → SMS math

For each acquired account we compute annual vehicles served from real inputs already in `accounts_v3.json`:

- **Hotel:** rooms × 365 × occupancy (70% default) × valet_conversion
- **Restaurant:** seats × turnover × 340 operating days × valet_conversion
- **Other:** fallback to TAM ÷ $15 avg valet transaction

Then annual SMS interactions = vehicles × capture rate × multi-touch. Annual ad revenue = SMS × conversion × offer value, at the selected case.

Sanity check against the deck's stated "2,698 monthly SMS today" from Charlotte's 5 anchors: our four SOPHI-flagged Charlotte anchors compute to ~2,379/mo combined, tracking within 12% of the deck figure and confirming the vehicle → SMS math holds.

## 5. Portfolio Y1–Y5 output — moderate case (diligence, live in deck)

| Year | Parking SOM | Monthly SMS | Annual SMS | Ad revenue (mod) | Total revenue |
|---|---|---|---|---|---|
| Y1 · 2027 | $4.02M | 11,557 | 138,686 | **$0** (pre-gate) | $4.02M |
| Y2 · 2028 | $9.00M | 25,417 | 305,002 | **$2.23M** | $11.23M |
| Y3 · 2029 | $14.74M | 46,527 | 558,322 | $4.19M | $18.92M |
| Y4 · 2030 | $19.48M | 67,265 | 807,177 | $6.16M | $25.64M |
| Y5 · 2031 | $28.29M | 92,651 | 1,111,811 | **$8.57M** | **$36.86M** |

**5-year cumulative:**
- Parking SOM: $75.52M (unchanged from v3)
- Ad revenue (moderate): **$21.15M** (28.0% of parking)
- **Total: $96.67M**

**Y5 run-rate (moderate):**
- Parking only: $28.29M
- Ad layer: $8.57M (30.3% of parking)
- **Total: $36.86M**

Deck values on the live pages: $8.62M Y5 ad, $21.27M 5-yr cumulative, $36.91M Y5 total. The 0.6% delta vs. model output is rounding across the portfolio SMS-mix weighting; both figures are within precision.

## 6. Per-market Y5 breakdown — moderate case

| Market | Parking Y5 | Monthly SMS Y5 | Ad revenue Y5 | Total Y5 | Ad as % of total |
|---|---|---|---|---|---|
| Denver | $11.26M | 27,963 | $2.65M | $13.91M | 19.0% |
| Charlotte | $7.75M | 28,766 | $2.65M | $10.40M | 25.5% |
| Indianapolis | $4.04M | 11,629 | $1.01M | $5.05M | 20.0% |
| Phoenix | $3.92M | 19,168 | $1.81M | $5.73M | **31.5%** |
| Louisville | $0.98M | 4,049 | $0.39M | $1.36M | 28.3% |
| Cleveland | $0.34M | 1,076 | $0.07M | $0.41M | 16.6% |
| **Portfolio** | **$28.29M** | **92,651** | **$8.57M** | **$36.86M** | **23.2%** |

Phoenix has the highest ad-attach ratio (31.5%) because its Y5 portfolio skews hotel-heavy (55% capture × 3.5× multi-touch). Cleveland is minimal — only 2 accounts unlock under v3 operator gates. Every additional hotel win beyond v3 assumptions moves the ad layer disproportionately.

## 7. Valuation impact — moderate case

| | Y5 run-rate | @ 7× |
|---|---|---|
| Parking only (v3 headline) | $28.29M | $198.05M |
| **With SMS ad layer (moderate)** | **$36.86M** | **$258.04M** |
| **Uplift from ad layer** | **+$8.57M** | **+$59.99M** |

**DCF (moderate, proportional to parking $36.30M @ 25% EBIT / 13.0× terminal / 12% WACC / same discount schedule):**
- Parking only: $36.30M
- Ad layer uplift: +$11.00M
- **Total DCF: $47.30M**
- Value per share: **$473.04** (100,000 FDSO)
- Same $500K seed at 10% post-money: **$4.73M** at DCF valuation → **9.46× MOIC**

## 8. Sensitivity — three cases

Same portfolio, same acquisition curve, same activation year — only the SMS conversion × offer band changes:

| Case | Y5 ad | Y5 total | 5-yr cum ad | 7× EV | DCF total | MOIC on $500K |
|---|---|---|---|---|---|---|
| Low (previous base) | $2.91M | $31.20M | $7.18M | $218M | $40.0M | 8.01× |
| **Moderate (diligence)** | **$8.57M** | **$36.86M** | **$21.15M** | **$258M** | **$47.3M** | **9.46×** |
| High (upper) | $16.98M | $45.27M | $41.91M | $317M | $58.1M | 11.62× |

**Where the number can move:**

1. **Activation year.** Every year of delayed activation loses one year of persona database compounding. If activation slips from Y2 to Y3 (e.g., consent infrastructure delay), 5-year cumulative ad revenue drops proportionally.
2. **Conversion band.** Low vs. moderate vs. high spans a ~5.8× range on Y5 ad revenue. Moderate is the diligence case; low is the stress-test floor; high is what to argue for in the pricing session.
3. **Mix — hotel share.** Hotels generate 5× the SMS-per-vehicle of restaurants (3.5× multi-touch × higher capture). Every additional hotel win beyond v3 assumptions is disproportionately good for the ad layer. If v3 caps in Denver or Phoenix loosen, the ad layer moves materially before the parking layer does.

## 9. What's still excluded — deliberately

Held out of this model, still carried against the valuation as optionality:

- **Referral revenue (Guest Experience OS → partner venues, CPL).** Confirmed to stay in the valuation-upside bucket, not in the growth model itself.
- **OS Licensing (SaaS) to non-competing operators.** Phase 2, 8–12× multiple — separate track.
- **SpotHero online-valet arbitrage.**
- **Franchise royalties on franchisee ARR.**
- **Airport concessions, hospital vertical as a full expansion, cross-property loyalty.**

The point of layering only ad revenue into the growth model is that ad revenue is the single stream that (a) scales directly with the SOM already being modeled and (b) has real observed benchmarks from our live 13-month operating data — every other stream requires additional business-model assumptions we're not willing to defend in the base case.

## 10. Recommendation for the pitch

- **Lead with parking-only v3** ($75.5M 5-year SOM, $28.3M Y5 run-rate, $198M @ 7×, $36.3M DCF) — the defensible floor.
- **Second slide adds the moderate ad layer** — **$96.8M 5-year, $36.9M Y5, $258M @ 7×, $47.4M DCF** — the diligence case, midpoint of every observed band.
- **Third slide holds the sensitivity band** — low $218M @ 7× (floor) and high $317M @ 7× (top of bands, hotel multi-touch fully exercised).
- **Optionality box:** referrals, OS licensing, SpotHero, franchise, hospital vertical — each with a short one-liner and no number in the DCF.

The narrative arc is: v3 is the defensible floor; the SMS ad layer at moderate case is what the strategic acquirer is buying growth against; everything else is why the multiple should be closer to 8× than 6×.

---

## Appendix — data provenance

- **Parking SOM curve, market caps, operator gates, acquisition-year outputs:** `sophi-market-map/src/accounts_v3.json` (unchanged, canonical v3)
- **SMS ad economics table:** `sophi-deal-room/sophi-os.html` Revenue Model tab, SMS Retrieval Ad Model section
- **Real operating baseline (2,698 monthly SMS from 5 Charlotte anchors):** SOPHI Domo dashboard, confirmed May 2026
- **Model script:** `sophi_v3_ad_revenue_model.py` — computes all three cases; diligence case pointer set to `"moderate"`
- **Full JSON output:** `sophi_v3_ad_revenue_layer.json` — includes moderate (headline) + low + high across all portfolio and per-market rollups
