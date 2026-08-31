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

Against that Y5 revenue, we're raising **$500K at $4.5M pre / $5.0M post** for a **10% seed**. The DCF against the v3 Y5 P&L values the seed at **$3.63M (7.26× MOIC, 48.7% IRR)** over a 5-year hold; the SP+ trading-comp floor still returns **~4× at 31.7% IRR**. Full scenario table further down.

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

## Seed round terms and return scenarios

*Added August 29, 2026 to reconcile the returns math against the v3 Y5 numbers above. Live version with sensitivity tables lives on the deal room's [Growth Valuation → Cap Table & Returns](https://joshuapcasey.github.io/sophi-deal-room/v3-valuation.html#cap) tab.*

### Terms

| Item | Value |
|---|---|
| Raise | $500K |
| Pre-money | $4.50M ($45.00 / share) |
| Post-money | $5.00M (111,111 FDSO) |
| Seed equity | 10% (11,111 shares) |
| Instrument | Priced round OR post-money SAFE @ $5M cap |
| Minimum check | $25K (555 shares) |
| Hold assumption (base) | 5 years — Jan 2027 close through end of 2031 |

### Valuation anchors

The DCF anchor uses WACC 12%, terminal growth 3%, and a 13.0× terminal EBITDA multiple against the Y5 v3 P&L ($28.29M revenue, 25% EBIT). That produces **$36.30M equity value at end of 2031**. Adding the SMS retrieval ad layer (moderate case, $8.62M Y5) lifts equity to **$47.36M**.

### Return scenarios · $500K seed at 10% · 5-year hold

| Scenario | Exit equity | Seed value | MOIC | IRR |
|---|---|---|---|---|
| Downside — miss Y5 by one year | $3.89M | $389K | 0.78× | **−4.8%** |
| Entry at cost ($45/share) | $5.00M | $500K | 1.00× | 0.0% |
| SP+ trading comp · 0.7× revenue | $19.80M | $1.98M | 3.96× | **31.7%** |
| **v3 DCF anchor — parking only (base case)** | **$36.30M** | **$3.63M** | **7.26×** | **48.7%** |
| **v3 DCF anchor — parking + SMS ad layer** | **$47.36M** | **$4.74M** | **9.47×** | **56.8%** |
| NAICS median · 1.7× revenue | $48.09M | $4.81M | 9.62× | 57.3% |

IRR = MOIC^(1/years) − 1, assuming single-shot exit at end of 2031. No interim distributions modeled.

### The two numbers that matter for the underwriting decision

**Base case: 7.26× / 48.7% IRR.** This is the DCF against the v3 Y5 P&L above. It's the number the round is priced against, and it's what an underwriting file should carry.

**Downside protection: 3.96× / 31.7% IRR at the SP+ trading comp.** If SOPHI hits Y5 revenue but the market prices it as commodity parking services rather than as a services-plus-software business, the seed still returns roughly 4× at ~32% IRR. That's the floor the model can defend, not the ceiling it hopes for.

The **v3 + SMS ad layer** case (9.47× / 56.8% IRR) is the base case with one revenue stream added back in — it's already inside the sales pipeline, it just isn't priced into the DCF anchor. Treat it as upside, not as the underwriting target.

### Hold-period sensitivity · v3 DCF anchor (7.26× MOIC)

| Hold | Exit year | IRR | What triggers it |
|---|---|---|---|
| 4 years | Y4 (2030) | 64.1% | Strategic acquirer arrives early (Metropolis-scale, PE roll-up) |
| **5 years (base)** | **Y5 (2031)** | **48.7%** | Priced against the Y5 v3 P&L — the underwriting number |
| 6 years | Y6 (2032) | 39.2% | Series A executes, seed rides through — same equity, longer hold |
| 7 years | Y7 (2033) | 32.7% | Strategic exit slips or IPO path opens |

The seed is priced on the 5-year assumption. Anything faster is upside from a strategic acquirer showing up early; anything slower is still a healthy IRR relative to how most seed rounds resolve.

### Path to Series A

At end of Y2 (Dec 2028), SOPHI is at $9.0M+ revenue run-rate with $5.19M cash on the balance sheet (see the deal room's [Cash Model](https://joshuapcasey.github.io/sophi-deal-room/cash-model.html)) and 12 accounts won across the six-market portfolio. That's the position from which the Series A is raised — targeted at $8–15M on a $20–35M pre-money range (7–13× revenue). Seed dilution at Series A is modeled at 15–20% depending on round size.

The seed doesn't need to bridge to a Series A of desperation. The operating cash flow does that on its own.

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
