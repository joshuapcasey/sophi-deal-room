# SOPHI Deal Room — Naming Conventions

**Status:** Canonical. Single source of truth for all external and internal names in the deal room.
**Last updated:** September 1, 2026 (Sept 2026 refinement layer)
**Scope:** Deal room HTML, memo, methodology, README, pitch deck, and any file created going forward.

**Internal versioning trace:** Live deal room reflects the September 2026 refinement layer (internally: v3.1) applied to the SOPHI Growth Engine. The refinement adjusts SOPHI 6 market composition, adds a Y1–Y2 flagship hotel gate, and updates named accounts per operator lock-in evidence. The underlying methodology framework (bottom-up TAM/SAM/SOM engine) is unchanged from v3. All version labels remain internal to git history and this note — they do not surface in investor prose.

---

## Purpose

The deal room's methodology is bottom-up and interconnected: **account-level parameters → market rollup → SOPHI portfolio rollup → 5-year P&L → valuation → returns → risk milestones.** A change at the account level (e.g., valet capture rate) propagates through every layer. To keep this defensible, every layer needs one canonical name.

This doc locks those names.

---

## The three growth models

There are **exactly three growth models** in the SOPHI narrative. They share one methodology (the SOPHI Growth Engine) but differ in which levers are activated and which markets are in scope.

### 1. Organic Growth Model *(the downside case)*

- **Scope:** Charlotte carry + Indianapolis + Denver, organic account acquisition only (no operator acquisitions, no ancillaries).
- **5-year P&L:** Organic Growth Model — 5-year P&L (formerly "Blend Wealth 5-year P&L").
- **Revenue trajectory:** $1.38M (2026A) → $11.00M (2031). 7.97× over 5 years. 51.4% CAGR.
- **Valuation anchor:** Organic Growth Valuation ($12.43M DCF).
- **Pricing anchor for:** Round 1 F&F Refinance.
- **What it answers:** "What is SOPHI worth on its own numbers, without capital, without acquisitions?"

### 2. Acquisition Growth Model *(the base case)*

- **Scope:** SOPHI 6 markets, organic acquisition + committed operator relationships (Guard & Grace portfolio across Denver/Houston/Detroit + Elite Management Indianapolis + VIP Parking Solutions Denver).
- **5-year P&L:** Acquisition Growth Model — 5-year P&L.
- **SOM trajectory:** Y1 $3.72M → Y5 $31.04M · 5-yr cumulative $75.47M.
- **Valuation anchor:** Acquisition Growth Valuation ($38.88M DCF).
- **Pricing anchor for:** Round 2 Acquisition Seed.
- **What it answers:** "What is SOPHI worth once R2 capital funds the operator acquisitions and the growth engine fires against the SOPHI 6?"

### 3. Expansion Growth Model *(the upside case — held out of base case)*

- **Scope:** Expansion Markets (Phoenix, Louisville, Cleveland) using the same SOPHI Growth Engine methodology.
- **Status:** Data loaded but held out of the Acquisition rollup pending CFO advisor conversation on Series A scope.
- **Valuation anchor:** Expansion Growth Valuation *(placeholder, not surfaced in the current base case)*.
- **What it will answer:** "What is SOPHI worth once the same growth engine is applied to Expansion Markets beyond the SOPHI 6?"

**Historical context (for future iterations):** An earlier iteration extended a prior SOPHI 6 composition to 8 additional expansion markets (Fort Wayne, Cincinnati, Columbus, Minneapolis, St. Louis, Raleigh, Charleston, Fort Lauderdale) for a 14-market universe of 895 scored accounts and $574.54M TAM. That work is preserved in session `8d590dde` and includes the enrichment, operator cross-reference, and self-park repricing passes that reframed expansion as a Towne Park / LAZ / SP+ / Propark partnership-unlock strategy. It will inform (but not directly feed) any future Expansion Growth Model buildout. Full details, file inventory, and reuse guidance: [`_archive/EXPANSION_PROVENANCE.md`](_archive/EXPANSION_PROVENANCE.md).

---

## The methodology framework

The engine that produces all three models above:

- **Name:** SOPHI Growth Engine
- **What it does:** Given an account-level universe (TAM/SAM inputs), applies the penetration engine (operator gates, ownership-group multipliers, per-market caps, S-curve targets) to produce SOM by market by year.
- **Output:** Each account gets `acquisition_year ∈ {1, 2, 3, 4, 5, never}`. Aggregated up, this becomes the market SOM, the portfolio SOM, the 5-year P&L, and the DCF.
- **Refinement layers:** The September 2026 refinement layer adds three additional mechanics on top of the base engine: the SOPHI 6 market composition update (§2.7), the Y1–Y2 flagship hotel gate (§2.8), and named account additions/corrections (§4). See `methodology.html` Section 05b for full derivation.
- **Formerly called:** "v3 Penetration Engine." All versioning language is retired from investor-facing surfaces.
- **Internal versioning:** Preserved in git history and internal memos, but not surfaced in the deal room.

---

## The market portfolio

### SOPHI 6 (Acquisition Growth Model)

- **Markets:** Charlotte · Indianapolis · Denver · Houston · Detroit · South Bend
- **Portfolio scope:** 134 named accounts · 77 in-SAM · 34 acquired by Y5 · $98.10M TAM · $48.70M SAM (49.6%)
- **Per-market Y5 SOM caps:** Charlotte 50% · Indianapolis 50% · Denver 30% · Houston 30% · Detroit 30% · South Bend 30%
- **What "SOPHI 6" means in copy:** Use "SOPHI 6" as the shorthand in captions and callouts. Use "the six markets" or "the six modeled markets" in prose when introducing the concept.

### Expansion Markets (Expansion Growth Model)

- **Markets:** Phoenix · Louisville · Cleveland
- **Status:** Held out of the Acquisition rollup. Data-loaded but not surfaced in base-case valuation.
- **What "Expansion Markets" means in copy:** Use "Expansion Markets" when the three-market group needs to be named. Do not surface individual Expansion Market numbers in investor-facing prose until CFO advisor sign-off.

---

## The two rounds

Every reference to the capital plan uses these exact names:

- **Round 1 · F&F Refinance** — $500K priced against the **Organic Growth Valuation**.
- **Round 2 · Acquisition Seed** — $4.5M priced against the **Acquisition Growth Valuation**.

Do not use "seed round" alone (it's ambiguous between R1 and R2). Always qualify with "F&F Refinance" or "Acquisition Seed."

---

## The three valuation scenarios

Displayed as bands or columns in this order across the deal room:

| Column | Label | Scenario source |
|---|---|---|
| Downside | Organic Growth Valuation | Organic Growth Model — 5-year P&L |
| Base | Acquisition Growth Valuation | Acquisition Growth Model — 5-year P&L |
| Upside | Expansion Growth Valuation *(placeholder)* | Expansion Growth Model *(deferred)* |

---

## Versioning language — retired

The following terms are **retired from all investor-facing surfaces**. They stay in git commit messages, this doc's internal-versioning notes, and older archived docs.

- "v2" · "v3" · "v3.1" · "v3 Penetration Engine" · "v3-six-market" · "v3 DCF" · "v3 base case" · "v3.1 refinement"
- "Blend Wealth 5-year P&L" · "Blend Wealth expansion plan" · "Blend Wealth workbook"
- "15 markets" · "15-market model" · "13 expansion markets" · "Markets by 2031: 15"

Where a public deal-room page needs to acknowledge a refresh happened (e.g., the "retired figures" note on `methodology.html`), reference it by date ("September 2026 refinement") or by the operator relationship that drove it ("Guard & Grace / Elite portfolio deployment"), never by version number.

---

## Rename lookup table

For anyone doing a rename or writing new copy — quick reference.

| Old term | Use instead |
|---|---|
| Blend Wealth 5-year P&L | Organic Growth Model — 5-year P&L |
| Blend Wealth expansion plan | Organic 3-market growth plan |
| Blend Wealth workbook | Organic Growth Model workbook |
| v3 six-market model | Acquisition Growth Model |
| v3.1 refinement | *(internal only — never investor-facing)* |
| v3 DCF | Acquisition Growth Valuation |
| v3 base case | Acquisition base case |
| v3 penetration engine | SOPHI Growth Engine |
| Organic DCF | Organic Growth Valuation |
| Six markets / six-market model | SOPHI 6 |
| Prior SOPHI 6 (with Phoenix + Louisville + Cleveland) | SOPHI 6 *(refers to current composition — the prior list is superseded)* |
| Phoenix / Louisville / Cleveland (in Acquisition context) | Expansion Markets |
| Growth Model page (nav item) | Growth Model *(stays — refers to the account-level model)* |
| Expansion beyond 6 markets | Expansion Growth Model *(placeholder)* |
| 15-market expansion | *(remove — this scope was superseded)* |

---

## Working file identity

The deal room has two states:

- **Advisor Working File** *(current state)* — watermark: "ADVISOR WORKING FILE," visible to advisors only, includes Advisor Questions page and pre-final terms. Purpose: kick the tires on methodology and finalize deal terms.
- **Investor Room** *(future state)* — advisor artifacts hidden, terms finalized. Purpose: fundraising for R2 Acquisition Seed.

Both use the same naming conventions above. The Advisor Working File → Investor Room transition swaps watermark, hides `advisor-questions.html`, and finalizes any placeholders — but does not rename models or scenarios.

---

## Canonical numbers

For any doc citing portfolio-level metrics, use these numbers verbatim. Values below are the **live Acquisition Growth Model output** and reconcile bit-for-bit with `data.js`, `valuation.html`, `methodology.html`, and `summary.html` in the deployed deal room.

### Organic Growth Model (downside floor)

| Metric | Value | Source |
|---|---|---|
| Y1 (2027) revenue | $1.72M | Organic Growth Model — 5-year P&L |
| Y5 (2031) revenue | $11.00M | Organic Growth Model — 5-year P&L |
| Y5 EBIT margin | 25.0% | Organic Growth Model — 5-year P&L |
| Y2 (2028) close cash position | $5.19M | 24-month cash trajectory |
| DCF equity value | $12.43M | `financial-performance.html` + `valuation.html` |
| Per-share (post-R2 FDSO 1,277,778) | $9.73 | derived |

### Acquisition Growth Model (base case)

| Metric | Value | Source |
|---|---|---|
| Total scored accounts | 134 | `data.js` portfolio.acquisition block |
| In-SAM accounts | 77 | `data.js` portfolio.acquisition block |
| Portfolio TAM | $98.10M | `data.js` portfolio.acquisition.tam |
| Portfolio SAM | $48.70M | `data.js` portfolio.acquisition.sam |
| Y1 Portfolio SOM | $3.72M | `data.js` som_by_year.y1 |
| Y5 Portfolio SOM | $31.04M | `data.js` som_by_year.y5 |
| 5-yr cumulative SOM | $75.47M | `data.js` som_5yr_cumulative |
| Accounts acquired by Y5 | 34 of 77 in-SAM | `data.js` n_acquired |
| SAM / TAM ratio | 49.6% | derived |
| Y5 / TAM ratio | 31.6% | derived |
| Y5 / SAM ratio | 63.7% | derived |
| Y1→Y5 SOM CAGR | 69.7% | derived |
| DCF equity value | $38.88M | `valuation.html` |
| Per-share (post-R2 FDSO 1,277,778) | $30.43 | derived |
| + SMS ad layer DCF equity | $50.47M | `valuation.html` |
| SMS Y5 moderate ad revenue | $9.46M | derived from SMS Growth Engine |

**Retired figures (do not use).**

An earlier draft cited Y1 = $16.85M, Y5 = $52.60M, and Y5/SAM = 91.8% for the acquisition case. Those numbers came from the 14-market build's `meta.sensitivity` block ("Base case: all 6 markets, Indy v7 w/ M&A" scenario) and do **not** match what the live engine produces or what the deal room displays. Corrected August 31, 2026 based on reconciliation against `data.js` and `valuation.html`.

**September 2026 refinement:** Y5 Acquisition Growth Model updated from $28.29M to $31.04M and DCF from $36.30M to $38.88M reflecting the redistribution of accounts under the Guard & Grace and Elite portfolio deployment schedule. Prior figures ($150.35M TAM, $57.27M SAM, $28.29M Y5 SOM, 203 accounts, $36.30M DCF) are preserved in git history and `_archive/data.v3.js`. See `methodology.html` Section 05b for the derivation.

**Note on the Organic Growth Model P&L:** The current site's Organic Growth Model P&L trajectory ($1.38M → $11.00M at 51.4% CAGR) is authoritative as displayed on `financial-performance.html`. The September 2026 refinement did not modify the Organic curve.

---

## Governance

Any new file, page, or document added to the deal room must use the names in this doc. If a new concept is needed that doesn't have a name here, add it here first, then use it in code.

Changes to naming go in one commit with `NAMING_CONVENTIONS.md` updated in the same commit as the code that uses the new name.
