# SOPHI Deal Room — Rename Map for V1 Consistency Sweep

**Status:** Planned for Commit 2. Working document — do not treat as final until executed.
**Companion:** `NAMING_CONVENTIONS.md` (canonical names) — this doc is the mechanical change list to apply them.
**Last updated:** August 31, 2026

---

## Scope of changes

- **189** references to "v3" across 16 HTML files + 5 MD files
- **26** references to "Blend Wealth" across 8 HTML files + 3 MD files
- **8** references to "15 markets" or "15-market" (all in HTML, all ghosts of a superseded iteration)
- **File renames:** 4 files (3 MD, 1 HTML)
- **URL/href updates:** every internal link to the renamed HTML file

---

## Part A · Text sweeps (applied via find-and-replace across all live files)

Each row lists (old string, new string, note). Apply case-sensitively unless noted.

### A1. Growth models & P&L labels

| Old string | New string | Note |
|---|---|---|
| `Blend Wealth 5-year P&L` | `Organic Growth Model — 5-year P&L` | Also `5-yr P&L` variants |
| `Blend Wealth 5-Year P&L` | `Organic Growth Model — 5-Year P&L` | Title-case variant |
| `Blend Wealth workbook` | `Organic Growth Model workbook` | |
| `Blend Wealth plan` | `Organic 6-market growth plan` | |
| `Blend Wealth expansion plan` | `Organic 6-market growth plan` | |
| `Blend Wealth 15-market expansion plan` | `Organic 6-market growth plan` | Kills 15-market ghost |
| `Blend Wealth expansion support` | `Organic growth plan support` | |
| `organic Blend Wealth plan` | `Organic Growth Model` | |
| `Blend Wealth,` *(as an investor)* | `Blend Wealth,` | **KEEP** — Blend Wealth is also the name of an investor firm; only rename P&L references |

### A2. Methodology / engine

| Old string | New string | Note |
|---|---|---|
| `v3 penetration engine` | `SOPHI Growth Engine` | |
| `v3 Penetration Engine` | `SOPHI Growth Engine` | |
| `v3 methodology` | `SOPHI Growth Engine methodology` | |
| `v3 model` | `Acquisition Growth Model` | Context: revenue/SOM |
| `v3 six-market` | `Acquisition Growth Model` | |
| `v3 six-market model` | `Acquisition Growth Model` | |
| `v3 DCF` | `Acquisition Growth Valuation` | |
| `v3 base case` | `Acquisition base case` | |
| `v3 · base` *(label)* | `Base · Acquisition` | |
| `v3 parking` | `Acquisition parking revenue` | Context: revenue lines |
| `v3 SOM` | `Acquisition SOM` | |
| `v3 valuation` | `Acquisition Growth Valuation` | |
| `v3 base MOIC` | `Base-case MOIC` | |
| `v3-anchored` | `Anchored to Acquisition Growth Valuation` | |
| `v2 model` | `earlier iteration` | Historical mentions only |
| `v3` *(standalone)* | *(context-dependent — do NOT global-replace)* | Manual audit each occurrence |

### A3. Organic valuation

| Old string | New string | Note |
|---|---|---|
| `Organic DCF` | `Organic Growth Valuation` | |
| `organic DCF` | `Organic Growth Valuation` | |
| `organic valuation` | `Organic Growth Valuation` | |
| `Organic Valuation` *(page title)* | `Organic Growth Valuation` | |

### A4. Six markets

| Old string | New string | Note |
|---|---|---|
| `six-market portfolio` | `SOPHI 6 portfolio` | |
| `six markets` | `SOPHI 6` | On first mention in a page keep "the six modeled markets" once |
| `6-market` | `SOPHI 6` | e.g., "6-market P&L" → "SOPHI 6 P&L" |
| `six-market SOM` | `SOPHI 6 SOM` | |

### A5. 15-market ghost eradication

All 8 references are inline in prose. These require case-by-case rewrites, not blanket replacement.

**Specific instances to rewrite:**

1. `capital-strategy.html:85` — "Blend Wealth 15-market expansion plan already in motion"
   → "Organic 6-market growth plan already in motion"

2. `questions.html:65` — "As we scale toward 15 markets, I expect 300–500 bps of compression"
   → "As we scale toward 15+ markets under the Expansion Growth Model, I expect 300–500 bps of compression"
   *(this preserves the compression logic while explicitly labeling that 15+ is a future scenario)*

3. `summary.html:200` — "the organic line is SOPHI's own P&L projection at 51.4% revenue CAGR on 15 markets by 2031"
   → "the organic line is the Organic Growth Model 5-year P&L projection at 51.4% revenue CAGR on the SOPHI 6"
   *(51.4% CAGR flagged for math reconciliation — see open item #3 below)*

4. `use-of-funds.html:58` — "support the Blend Wealth 15-market expansion plan already in motion"
   → "support the Organic 6-market growth plan already in motion"

5. `v3-valuation.html:283` — "current playbook, current 15-market expansion"
   → "current playbook, current SOPHI 6 scope"

6. Any "Markets by 2031: 15" KPI → "Markets by 2031: 6" (or remove the KPI — the SOPHI 6 stays at 6 by definition)

7. `financial-performance.html` at-a-glance caption — "Charlotte carry into Indy/Denver/Louisville expansion"
   → "Charlotte carry into the SOPHI 6 buildout"
   *(missing Phoenix and Cleveland from the current caption)*

### A6. Retire "Investor Deal Room" from V1 surfaces

| Old string | New string | Note |
|---|---|---|
| `SOPHI Investor Deal Room` | `SOPHI Deal Room · Advisor Working File` | V1 identifier |
| `Sophi Investor Deal Room` | `SOPHI Deal Room · Advisor Working File` | Case-fix bundled |
| `Sophi Mobility` *(brand)* | `SOPHI Mobility` | Match brand case everywhere |
| `INVESTOR DEAL ROOM · 2026` *(banner)* | `ADVISOR WORKING FILE · 2026` | Fix on index.html gate |

---

## Part B · File renames

| Old path | New path | Notes |
|---|---|---|
| `INVESTOR_MEMO_v3.md` | `INVESTOR_MEMO.md` | Drop version suffix |
| `METHODOLOGY_v3.md` | `METHODOLOGY.md` | Drop version suffix |
| `V3_METHODOLOGY_DELTAS.md` | `_archive/V3_METHODOLOGY_DELTAS.md` | Move to archive folder — historical only |
| `METHODOLOGY_v2.md` | `_archive/METHODOLOGY_v2.md` | Move to archive — superseded |
| `v3-valuation.html` | `valuation.html` | Public URL cleanup |
| `organic-valuation.html` *(redirect stub)* | `_archive/organic-valuation.html` | Was already a redirect; move to archive |
| `cash-model.html` *(redirect stub)* | *(keep in place)* | Still needed as inbound-link redirect |

**Consequences of file renames:**

- Every `href="./v3-valuation.html"` becomes `href="./valuation.html"` — search all HTML + JS
- Every `INVESTOR_MEMO_v3.md` link (in README, in downloads.html, in your-access.html) becomes `INVESTOR_MEMO.md`
- `assets/shell.js` nav entry `{ href: 'v3-valuation.html', ... }` becomes `{ href: 'valuation.html', ... }`
- `build_deck.py` may reference these paths in its captions — audit before rebuilding the deck

---

## Part C · Page-level updates

### C1. Sidebar (`assets/shell.js`)

Current nav under THE DEAL:
```
Financial Performance · Use of Funds · Valuation · Risk Mitigating Milestones
```

Update the "Valuation" href from `v3-valuation.html` to `valuation.html`.

### C2. `v3-valuation.html` → `valuation.html`

- Update page title and H1: strip any "v3" language
- Column headers: **Downside · Organic Growth · Base · Acquisition Growth · Upside · Expansion Growth (placeholder)**
- The "Downside detail" subtab renames to "Organic Growth Valuation detail"

### C3. `financial-performance.html`

- P&L wrapper title `Blend Wealth 5-year P&L · organic plan` → `Organic Growth Model — 5-year P&L · SOPHI 6`
- Header lede: remove "Blend Wealth"; the P&L is the Organic Growth Model
- At-a-glance caption: fix the Charlotte-into-Indy/Denver/Louisville ghost (missing Phoenix + Cleveland)
- R2 narrative card: "converts v3 SOM into acquired portfolio" → "converts Acquisition Growth SOM into acquired portfolio"

### C4. `capital-strategy.html`

- All "priced against organic DCF" / "priced against v3 DCF" language → "priced against Organic Growth Valuation" / "priced against Acquisition Growth Valuation"
- R1 investor pool line: "Blend Wealth, board participants" — keep `Blend Wealth,` because that's the investor firm

### C5. `summary.html`

- Chart legend line 200 (see A5 item 3) — full rewrite
- Two-line "Organic plan vs. penetration model" subtitle → "Organic Growth Model vs. Acquisition Growth Model"

### C6. `use-of-funds.html`

- R1 section framing: strip "Blend Wealth expansion" language, use "Organic 6-market growth plan"

### C7. `methodology.html` + `METHODOLOGY.md`

- Every "v3" instance → "SOPHI Growth Engine"
- Version banner "**Status:** Live in app. Supersedes METHODOLOGY_v2.md" → "**Status:** Live. Canonical methodology for the deal room."

### C8. `INVESTOR_MEMO.md`

- Subject line: "v3 Penetration Model — methodology summary..." → "SOPHI Growth Engine — methodology summary..."
- Body: every "v3" → context-appropriate ("SOPHI Growth Engine" for methodology mentions, "Acquisition Growth Model" for scenario mentions)

### C9. `pitch deck` (`build_deck.py`)

- Slide 11 (Capital Strategy) header line "priced against v3 DCF" → "priced against Acquisition Growth Valuation"
- Any other v3 mentions on other slides

### C10. `advisor-questions.html`

- All 9 questions reference model names — audit each. The 4 P1 questions all touch pricing anchors that get renamed.

---

## Part D · Follow-on P5 consistency polish (Commit 3, not Commit 2)

Bundled here for planning visibility. Not part of the rename sweep.

- All `<title>` tags → pattern `"<Page Name> — SOPHI Deal Room · Advisor Working File"`
- `index.html` gate: update hero copy, brand casing (Sophi → SOPHI), CONFIDENTIAL banner
- Breadcrumb pattern: standardize `ph-eyebrow` to one of a fixed set of values (Overview / The Opportunity / The Deal / Advisor Working File)
- Watermark opacity: reduce so it doesn't cross header text
- "Your Access" in sidebar: decide if it joins "Advisor Working File" group or stays ungrouped

---

## Open reconciliation items (require Joshua's input before executing)

### 1. The Organic Growth Model 5-year P&L needs a source-of-truth workbook

Current site:
- 2026A: $1.38M
- 2027: $1.72M *(+24.6%)*
- 2028: $2.10M *(+22.1%)*
- 2029: $3.70M *(+76.2%)*
- 2030: $6.50M *(+75.7%)*
- 2031: $11.00M *(+69.2%)*
- **51.4% geometric CAGR**

Two concerns:

- **Where do these numbers come from?** The `sophi_6market_rollup.xlsx` rollup has SAM/SOM by market by year but does not contain a P&L trajectory in this exact shape. The methodology docs don't contain the P&L either. It appears to live only in the HTML.
- **The curve shape looks acquisition-driven, not organic.** Growth of 24%/22%/76%/76%/69% front-flat then back-loaded matches the SOPHI Growth Engine ramp (accounts win in Y3-Y5), not a smooth organic curve. If this P&L is scoped to organic-only (no operator acquisitions), it should either grow more smoothly or explicitly reference the account-win ramp as its driver.

**Ask Joshua:**
- (a) Is there a workbook that produces the current $1.38M → $11.00M trajectory we can point to?
- (b) Is the current curve intentionally showing the ramp from account wins under the SOPHI Growth Engine applied with acquisitions=off (which would explain the back-loaded shape)?
- (c) If (a) is no and (b) is no, do we want to smooth the P&L to a more organic-looking curve, or leave it as-is and simply annotate that the back-loading is a feature of the growth engine?

### 2. Historical CAGR gut-check

**Ask Joshua:** What are SOPHI's historical revenue numbers 2022–2025 (or whatever years are available)? A 51.4% forward CAGR is defensible if it's roughly consistent with historical trajectory; it's a red flag to advisors if forward > historical by 2× or more.

### 3. R1 investor pool includes an investor named "Blend Wealth"

The Blend Wealth firm is listed as an early investor. That's why every rename here has to be careful — some "Blend Wealth" instances refer to the P&L (rename), some refer to the investor firm (keep).

**Ask Joshua:** Confirm that the Blend Wealth investor firm and the Blend Wealth P&L name are related historically — was the P&L named after the firm because it was originally shared with the firm's owner? If yes, we should note that in the methodology doc.

### 4. Expansion Growth Model — historical iteration

The prior expansion work extended the SOPHI 6 methodology to 8 additional markets (14 markets total: 895 scored accounts, $574.54M TAM). That data is preserved in session `8d590dde` and represents real research work — enrichment, operator cross-reference, and self-park repricing — that shouldn't be discarded. (Session `07d6c972` is the SOPHI 6 methodology source, not the expansion source, despite older copy citing it that way.)

**Ask Joshua:** When we build the Expansion Growth Model in a future iteration, do we start from that 14-market work, or start fresh with additional markets identified through the current pipeline? The former is faster; the latter is more rigorous.

---

## Execution plan for Commit 2

1. Move `METHODOLOGY_v2.md`, `V3_METHODOLOGY_DELTAS.md`, `organic-valuation.html` (redirect stub) → `_archive/`
2. Rename `INVESTOR_MEMO_v3.md` → `INVESTOR_MEMO.md`, `METHODOLOGY_v3.md` → `METHODOLOGY.md`, `v3-valuation.html` → `valuation.html`
3. Update `assets/shell.js` (nav href)
4. Sweep all HTML files with the Part A text replacements
5. Handle the 8 15-market ghost instances one-by-one (Part A5)
6. Update `INVESTOR_MEMO.md` + `METHODOLOGY.md`
7. Update `README.md`
8. Update `build_deck.py` and rebuild the pitch deck
9. Commit + push
10. Verify with a live-page review pass

---

## Not in scope for this rename sweep

- No mathematical or numerical changes (except fixing the two obvious ghosts: "15 markets" → "SOPHI 6", and missing Phoenix/Cleveland in Financial Performance caption)
- No layout or visual changes
- No new pages
- No changes to cap table math, valuation numbers, or return metrics
- P5 polish (see Part D) — separate Commit 3
