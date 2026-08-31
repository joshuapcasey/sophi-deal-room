# Sophi Mobility — Investor Memo

**Subject:** v3 Penetration Model — methodology summary, five-year SOM, and seed-round returns
**From:** Joshua Casey, Sophi Mobility (jcasey@sophimobility.com)
**Date:** April 30, 2026 · updated August 29, 2026
**Live model:** https://joshuapcasey.github.io/sophi-market-map/
**Deal room:** https://joshuapcasey.github.io/sophi-deal-room/

---

## TL;DR

We rebuilt the SOM model from the ground up. The TAM ($150.35M across six markets) and SAM ($57.27M / 93 accounts) are unchanged. What changed is **how we model winning those accounts**: instead of every in-SAM account contributing a fractional ramp, each account now has a binary acquisition year governed by a credibility-weighted penetration engine — operator gates, ownership-group multipliers, and conservative per-market caps.

The result is a more defensible curve: lower in Y1 (we don't book revenue from accounts we haven't won), heavier in Y4–Y5 (full-TAM accrual from the day we win), and a five-year cumulative SOM of **$75.52M** with a **$28.29M Y5 run-rate** off only **34 of 93 in-SAM accounts won** — leaving 59 accounts of remaining runway in the same six markets.

Against that plan, SOPHI is raising in **two rounds**: a **$500K F&F refinance (Round 1)** priced against the organic DCF at a 64% discount ($4.5M pre / $5.0M post), then a **$4.5M Acquisition Seed (Round 2)** priced against the v3 DCF ($12M pre placeholder / $16.5M post) to fund two valet-operator acquisitions — one in Indianapolis, one in Denver. Founder retains **70.4% ownership (78.3% including ESOP pool)** through both rounds. Round 1 investors see **6.31× / 44.6% IRR** at v3 base case. Round 2 investors see **2.63× / 27.4% IRR** at v3 base case, expanding to **3.99×** with acquisitions integrated. Full scenario tables further down.

---

## Why we rebuilt the model

The v2 model used an implicit penetration ramp: every in-SAM account contributed a fractional share of its TAM each year, growing toward full TAM by Y5. That approach front-loaded revenue from accounts we haven't actually closed yet, and it didn't model the two real-world frictions that shape any new operator-displacement sale:

1. **Operator credibility gates.** National operators (Towne Park, LAZ, SP+, Propark, Park Inc, Epic Valet, Elite) don't lose accounts to an unproven challenger until the challenger has demonstrated wins across enough properties and verticals. We can't book displaced-Towne-Park revenue in Y1 if we haven't beaten them anywhere yet.
2. **Ownership-group network effects.** Once we win one Darden / Huse / Marriott-managed property, sister properties in the same market move materially faster. v2 had no mechanic for this.

v3 makes both of these explicit, plus it caps per-market penetration at conservative levels (50% Charlotte/Indianapolis where we have the strongest unlock stories; 30% elsewhere) so the curve can't run away on us.

---

## Methodology, in one page

**Per account, the engine produces a single field:** `acquisition_year ∈ {1, 2, 3, 4, 5, never}`.

**The selection logic each year:**

- **Cumulative S-curve** sets the upper bound of penetration in a market: 10% / 30% / 50% / 70% / 85% by Y1–Y5 of the candidate set, multiplied by the per-market cap.
- **Operator gates** require minimum prior wins and verticals before that operator's accounts unlock — Towne Park 8 accts/3 verticals, Propark 4/2, Park Inc 3/1, Epic 2/1, Elite 2/1, independents are open. Until the gate clears, those accounts can't be selected.
- **Group multiplier** boosts priority for sister properties: 1 prior in-market win in the same group → 1.5×, 2 → 2.0×, 3+ → 3.0×.
- **Anchor and v7 layers force Y1.** Sophi anchor accounts force Y1. Indianapolis hometown_displaced and was_boost accounts force Y1; ma_absorption accounts force Y2 (the M&A trigger event).

**Once acquired, an account contributes its full annual TAM every year forward — no fractional ramp.**

That's the entire model. Full canonical doc: `METHODOLOGY_v3.md` in the repo.

---

## Five-year financial summary

### Portfolio

| Metric | Value |
|---|---|
| TAM (six markets) | $150.35M |
| SAM (in-SAM only) | $57.27M |
| Accounts in SAM | 93 |
| **Acquired by Y5** | **34** |
| **5-year cumulative SOM** | **$75.52M** |
| **Y5 run-rate SOM** | **$28.29M** |
| Y5-on-TAM share | 18.8% |
| Y5-on-SAM share | 49.4% |

### Year-by-year SOM

| Year | SOM | Cumulative | YoY |
|---|---|---|---|
| Y1 | $4.02M | $4.02M | — |
| Y2 | $9.00M | $13.01M | +124% |
| Y3 | $14.74M | $27.75M | +64% |
| Y4 | $19.48M | $47.23M | +32% |
| Y5 | $28.29M | $75.52M | +45% |

The Y5 step-up reflects two things: (a) Charlotte and Indianapolis approaching their per-market caps with their full-TAM accounts on the books, and (b) Denver's Towne Park gate clearing in Y4, allowing two Y5 acquisitions to start accruing full TAM.

### Per-market

| Market | Cap | In-SAM | Won by Y5 | 5-yr SOM | Y5 SOM |
|---|---|---|---|---|---|
| Denver | 30% | 21 | 6 | $23.81M | $11.26M |
| Charlotte | 50% | 24 | 12 | $20.17M | $7.75M |
| Indianapolis | 50% | 14 | 7 | $19.42M | $4.04M |
| Phoenix | 30% | 19 | 5 | $9.27M | $3.92M |
| Louisville | 30% | 7 | 2 | $2.12M | $0.98M |
| Cleveland | 30% | 8 | 2 | $0.72M | $0.34M |
| **Portfolio** | | **93** | **34** | **$75.52M** | **$28.29M** |

---

## What this means for the investor narrative

**The model now matches our sales motion.** v3 says we win Charlotte and Indianapolis early because we have anchor relationships and credible unlock stories there, and we earn the rest of the portfolio across years 3–5 as gates clear and group effects compound. That's exactly how we plan to execute, and it's exactly what the numbers now show.

**The 5-year total is conservative on purpose.** 34 of 93 accounts is a 37% acquisition rate over five years, against per-market caps of 30–50%. That's deliberate headroom: 59 unwon in-SAM accounts is runway, not failure. The investor takeaway is "this $75.5M is what we believe we can defend, not what we hope we can claim."

**Y5 run-rate ($28.3M) is the headline metric.** It compounds beyond the five-year window, it's a clean ARR analog for parking-management software-plus-operations economics, and it's tied to a known account list — every dollar in that number is a named property with a documented gate and group history.

**Cleveland is small and we're documenting it honestly.** With 8 in-SAM accounts and Propark dominance, Cleveland comes in at $720K cumulative. We could soften the gate model to lift Cleveland; we chose not to. The credibility cost of one underperforming small market is far lower than the credibility cost of a model that hides its assumptions.

---

## Two-round capital strategy

*Restructured August 31, 2026 from a single-round seed narrative into a two-round F&F + Acquisition Seed plan. Live cap table evolution and return scenarios by round on the deal room's [Capital Strategy](https://joshuapcasey.github.io/sophi-deal-room/capital-strategy.html) page. This section is a working-file draft — final terms pending CFO and business advisor review.*

### Round 1 · F&F Refinance (now)

| Item | Value |
|---|---|
| Raise | $500K |
| Pre-money | $4.50M (64% discount to $12.43M organic DCF) |
| Post-money | $5.00M |
| Share price | $4.50 |
| New shares issued | 111,111 (Round 1 = 10% at post) |
| Instrument | Priced round OR post-money SAFE @ $5M cap |
| Investor pool | Bryce Tolle, Blend Wealth, board participants, early movers |
| Hold assumption | 5 years (Jan 2027 close → end of 2031) |
| Use of funds | Refinance, Blend Wealth expansion support, Hub MVP, R2 diligence prep |

**What Round 1 investors see:**

| Scenario | Exit equity | R1 value at exit | MOIC | IRR (5yr) |
|---|---|---|---|---|
| Downside — organic DCF only | $12.43M | $1.08M | **2.16×** | **16.7%** |
| Base — v3 DCF (6 markets) | $36.30M | $3.16M | **6.31×** | **44.6%** |
| v3 + SMS ad layer | $47.36M | $4.12M | 8.24× | 52.5% |
| v3 + acquisitions integrated | $55.00M | $4.78M | 9.56× | 56.9% |
| Upside — expansion beyond 6 markets | $75.00M | $6.52M | **13.04×** | **67.0%** |

### Round 2 · Acquisition Seed (~early 2028)

| Item | Value |
|---|---|
| Raise | $4.5M |
| Pre-money | $12.00M (67% discount to $36.30M v3 DCF) · illustrative placeholder |
| Post-money | $16.50M |
| Share price | $10.80 (2.4× step-up from Round 1) |
| New shares issued | 416,667 (Round 2 = 13.04% at post) |
| Instrument | Priced preferred (structure TBD with advisor) |
| Investor pool | Institutional seed / family office / strategic hospitality operator |
| Hold assumption | ~4 years (early 2028 → end of 2031) |
| Use of funds | Indianapolis operator acquisition + Denver operator acquisition + integration |

**What Round 2 investors see:**

| Scenario | Exit equity | R2 value at exit | MOIC | IRR (4yr) |
|---|---|---|---|---|
| Downside — organic DCF only | $12.43M | $1.62M | 0.36× | −21.7% |
| Base — v3 DCF (6 markets) | $36.30M | $4.74M | **2.63×** | **27.4%** |
| v3 + SMS ad layer | $47.36M | $6.18M | 3.43× | 36.1% |
| **v3 + acquisitions integrated** | **$55.00M** | **$7.17M** | **3.99×** | **41.3%** |
| Upside — expansion beyond 6 markets | $75.00M | $9.78M | **5.44×** | **52.6%** |

Round 2's underwriting narrative is the **v3 + acquisitions case ($55M exit, 3.99× MOIC)** — not the pure v3 case. The acquisitions are the reason Round 2 exists; the base scenario for Round 2 investors already assumes those acquisitions perform as expected.

### Cap table evolution · Option C issuance (1,000,000 starting cap)

| Holder | Today | After R1 | After R2 |
|---|---|---|---|
| Joshua Casey · Founder | 900,000 (90.00%) | 900,000 (81.00%) | 900,000 (**70.43%**) |
| ESOP / Board pool | 100,000 (10.00%) | 100,000 (9.00%) | 100,000 (7.83%) |
| Round 1 F&F Seed | — | 111,111 (10.00%) | 111,111 (8.70%) |
| Round 2 Acquisition Seed | — | — | 166,667 (13.04%) |
| **Total FDSO** | **1,000,000** | **1,111,111** | **1,277,778** |
| Founder + ESOP (control) | 100.00% | 90.00% | **78.26%** |

Founder retains supermajority control through Round 2. Round 3 (Series A) would target another 15–20% dilution against a Series-A-priced valuation — leaving founder at ~55% and still founder-controlled.

### Open questions for the advisor conversation

Nine open decisions live on the deal room's [Advisor Questions](https://joshuapcasey.github.io/sophi-deal-room/advisor-questions.html) page. The four Priority-1 items that block further progress:

1. **Round 1 discount to organic DCF** — is 64% the right F&F pricing, or should Round 1 pre-money move?
2. **Round 2 base-case MOIC** — 2.63× is thin for institutional seed. Levers: lower pre-money, smaller raise, or lean on the integrated-case narrative ($55M exit).
3. **Expansion-beyond-6 upside scenario** — which markets, timeline, gate discipline? Currently a $75M placeholder; needs a defensible construction.
4. **Acquisition target operators** — which specific Indy and Denver operators, at what confirmed price range, with what deal structure?

---

## What's in the live app

https://joshuapcasey.github.io/sophi-market-map/

- **Landing page:** portfolio hero ($150M TAM / $28.3M Y5 / "Conservative, gated, defensible") and four methodology cards (binary acquisition, operator gates, group multiplier, per-market caps).
- **Portfolio page:** $75.5M / $28.3M / 7.0× multiple hero, stacked acquisition timeline by market by year, market table with Cap and Won/In-SAM columns.
- **Per-market pages:** acquisition-year filter, per-account modal showing v3 lifecycle (acquisition year, gate detail, group multiplier), trajectory bars (dashed pre-acquisition, solid post-acquisition, ★ on acquisition year).
- **Status pills:** SOPHI Anchor · v7 Hometown · v7 M&A Absorption · Operator-gated · Cap-deferred · Below cap line.

Repo (private): https://github.com/joshuapcasey/sophi-market-map. Engine in `src/normalize_v3.py`, build pipeline in `src/build_data_js_v3.py`, full methodology in `METHODOLOGY_v3.md`.

---

*Questions or specific scenarios you want modeled — happy to run them. The engine is parameterized, so loosening a single gate or raising a market cap is a one-line change and a 30-second rebuild.*
