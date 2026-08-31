# SOPHI Deal Room — Naming Conventions

**Status:** Canonical. Single source of truth for all external and internal names in the deal room V1.
**Last updated:** August 31, 2026
**Scope:** Deal room HTML, memo, methodology, README, pitch deck, and any file created going forward.

---

## Purpose

The deal room's methodology is bottom-up and interconnected: **account-level parameters → market rollup → SOPHI portfolio rollup → 5-year P&L → valuation → returns → risk milestones.** A change at the account level (e.g., valet capture rate) propagates through every layer. To keep this defensible, every layer needs one canonical name.

This doc locks those names.

---

## The three growth models

There are **exactly three growth models** in the SOPHI narrative. They share one methodology (the SOPHI Growth Engine) but differ in which levers are activated.

### 1. Organic Growth Model *(the downside case)*

- **Scope:** SOPHI 6 markets, organic account acquisition only (no operator acquisitions).
- **5-year P&L:** Organic Growth Model — 5-year P&L (formerly "Blend Wealth 5-year P&L").
- **Valuation anchor:** Organic Growth Valuation ($12.43M current DCF).
- **Pricing anchor for:** Round 1 F&F Refinance.
- **What it answers:** "What is SOPHI worth on its own numbers, without capital, without acquisitions?"

### 2. Acquisition Growth Model *(the base case)*

- **Scope:** SOPHI 6 markets, organic acquisition + two operator acquisitions (Indianapolis + Denver).
- **5-year P&L:** Acquisition Growth Model — 5-year P&L (formerly the "v3 six-market model" numbers).
- **Valuation anchor:** Acquisition Growth Valuation ($36.30M current DCF · placeholder).
- **Pricing anchor for:** Round 2 Acquisition Seed.
- **What it answers:** "What is SOPHI worth once R2 capital funds the two operator acquisitions and the growth engine fires against the SOPHI 6?"

### 3. Expansion Growth Model *(the upside case — deferred)*

- **Scope:** SOPHI 6 markets + additional markets beyond the current six (specific markets TBD).
- **Status:** **Not modeled in V1.** Placeholder concept only. Same methodology applied to a broader market set. Account universe research required before this becomes a real number.
- **Valuation anchor:** Expansion Growth Valuation *(placeholder, not populated)*.
- **What it will answer:** "What is SOPHI worth once the same growth engine is applied to markets beyond the SOPHI 6?"

**Historical context (for future iterations, not for V1):** An earlier iteration extended the SOPHI 6 methodology to 8 additional expansion markets (Fort Wayne, Cincinnati, Columbus, Minneapolis, St. Louis, Raleigh, Charleston, Fort Lauderdale) for a 14-market universe of 895 scored accounts and $574.54M TAM. That work is preserved in session `8d590dde` and includes the enrichment, operator cross-reference, and self-park repricing passes that reframed expansion as a Towne Park / LAZ / SP+ / Propark partnership-unlock strategy. It will inform (but not directly feed) the Expansion Growth Model when it's populated with the same rigor as the SOPHI 6. Note: session `07d6c972` — sometimes cited as the "15-market" source — is actually the origin of the SOPHI 6 methodology itself, not the expansion work.

---

## The methodology framework

The engine that produces all three models above:

- **Name:** SOPHI Growth Engine
- **What it does:** Given an account-level universe (TAM/SAM inputs), applies the penetration engine (operator gates, ownership-group multipliers, per-market caps, S-curve targets) to produce SOM by market by year.
- **Output:** Each account gets `acquisition_year ∈ {1, 2, 3, 4, 5, never}`. Aggregated up, this becomes the market SOM, the portfolio SOM, the 5-year P&L, and the DCF.
- **Formerly called:** "v3 Penetration Engine." All versioning language is retired from investor-facing surfaces.
- **Internal versioning:** Preserved in git history and internal memos, but not surfaced in the deal room.

---

## The market portfolio

- **Name:** SOPHI 6
- **Markets:** Charlotte · Indianapolis · Denver · Phoenix · Louisville · Cleveland
- **Portfolio scope:** 203 named accounts · $150.35M TAM · $57.27M SAM
- **Per-market caps:** Charlotte 50% · Indianapolis 50% · Denver 30% · Phoenix 30% · Louisville 30% · Cleveland 30%
- **What "SOPHI 6" means in copy:** Use "SOPHI 6" as the shorthand in captions and callouts. Use "the six modeled markets" in prose when introducing the concept.

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

The following terms are **retired from all investor-facing surfaces**. They stay in git commit messages and older archived docs.

- "v2" · "v3" · "v3 Penetration Engine" · "v3-six-market" · "v3 DCF" · "v3 base case"
- "Blend Wealth 5-year P&L" · "Blend Wealth expansion plan" · "Blend Wealth workbook"
- "15 markets" · "15-market model" · "13 expansion markets" · "Markets by 2031: 15"

---

## Rename lookup table

For anyone doing a rename or writing new copy — quick reference.

| Old term | Use instead |
|---|---|
| Blend Wealth 5-year P&L | Organic Growth Model — 5-year P&L |
| Blend Wealth expansion plan | Organic 6-market growth plan |
| Blend Wealth workbook | Organic Growth Model workbook |
| v3 six-market model | Acquisition Growth Model |
| v3 DCF | Acquisition Growth Valuation |
| v3 base case | Acquisition base case |
| v3 penetration engine | SOPHI Growth Engine |
| Organic DCF | Organic Growth Valuation |
| Six markets / six-market model | SOPHI 6 |
| Growth Model page (nav item) | Growth Model *(stays — refers to the account-level model)* |
| Expansion beyond 6 markets | Expansion Growth Model *(placeholder)* |
| 15-market expansion | *(remove — this scope was superseded)* |
| Investor deal room | *(context-dependent — see below)* |

---

## Working file identity — advisor V1 vs. investor V2

The deal room has two states:

- **V1 · Advisor working file** *(current state)* — watermark: "ADVISOR WORKING FILE," visible to advisors only, includes Advisor Questions page and pre-final terms. Purpose: kick the tires on methodology and finalize deal terms.
- **V2 · Investor room** *(future state)* — advisor artifacts hidden, terms finalized. Purpose: fundraising for R2 Acquisition Seed.

Both use the same naming conventions above. The V1 → V2 transition swaps watermark, hides `advisor-questions.html`, and finalizes any placeholders — but does not rename models or scenarios.

---

## Canonical numbers (SOPHI 6 methodology output)

For any doc citing portfolio-level metrics, use these numbers verbatim:

| Metric | Value | Source |
|---|---|---|
| Named accounts (in-SAM) | 203 | `sophi_6market_rollup.xlsx` |
| Portfolio TAM | $150.35M | rollup |
| Portfolio SAM | $57.27M | rollup |
| Y1 Portfolio SOM *(acquisition case)* | $16.85M | rollup |
| Y5 Portfolio SOM *(acquisition case)* | $52.60M | rollup |
| Acquired accounts by Y5 | 34 of 93 in-SAM | site + rollup consistent |
| SAM / TAM ratio | 38.1% | rollup |
| Y5 / SAM ratio *(acquisition case)* | 91.8% | rollup |
| Y1→Y5 SOM CAGR *(acquisition case)* | 32.9% | rollup |

**Note on the Organic Growth Model P&L:** The current site's Blend Wealth P&L trajectory ($1.38M → $11.00M at 51.4% CAGR) does not have a canonical source-of-truth workbook. The trajectory needs to be reconciled — see `RENAME_MAP.md` open item #3.

---

## Governance

Any new file, page, or document added to the deal room must use the names in this doc. If a new concept is needed that doesn't have a name here, add it here first, then use it in code.

Changes to naming go in one commit with `NAMING_CONVENTIONS.md` updated in the same commit as the code that uses the new name.
