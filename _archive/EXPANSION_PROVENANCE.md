# Expansion Growth Model — Provenance Note

**Status:** Reference document for a **deferred** workstream. Not part of Deal Room V1.
**Created:** August 31, 2026
**Purpose:** Single source of truth for what the prior expansion research produced, where it lives, what it's worth reusing, and what needs to be redone before it can feed a valuation.

---

## Scope of this note

The **Expansion Growth Model** is the upside scenario in the [three-growth-model framework](../NAMING_CONVENTIONS.md#the-three-growth-models). It applies the SOPHI Growth Engine methodology to markets beyond the SOPHI 6. It is **not modeled in V1** — the current deal room prices Round 1 F&F Refinance against the Organic Growth Valuation and Round 2 Acquisition Seed against the Acquisition Growth Valuation. Expansion is a future-round scenario.

However, real research work was done on an 8-market expansion universe in May 2026. This note preserves that provenance so the next iteration knows exactly what to reuse and what to redo.

---

## Two sessions, two different bodies of work

Older copy in this repo conflated two Perplexity sessions. They are distinct:

| Session | Dates | Scope | Output |
|---|---|---|---|
| `07d6c972` | Apr 18 – Aug 26, 2026 | **SOPHI 6 methodology origin** | 203 in-SAM accounts, $150.35M TAM, $57.27M SAM, $52.6M Y5 SOM. The layered TAM/SAM/SOM engine, WAS decoupling from SAM, and per-market TAM/SOM workbooks were all produced here. This is the canonical source for the Acquisition Growth Model. |
| `8d590dde` | May 7 – Aug 28, 2026 | **8-market expansion research** | Extended the SOPHI 6 methodology to 8 additional markets for a 14-market universe (895 accounts, $574.54M TAM). This is the actual source for future Expansion Growth Model work. |

If anything in older doc copy or memos cites `07d6c972` as the "15-market" or "expansion" source, that is a misattribution — the correct citation is `8d590dde`. There is no 15-market model; the "15" in old copy was a rounding artifact of the 14-market build (SOPHI 6 + 8 expansion).

---

## The 8 expansion markets

Fort Wayne · Cincinnati · Columbus · Minneapolis · St. Louis · Raleigh · Charleston · Fort Lauderdale.

Market selection rationale (from session 8d590dde) was regional adjacency to the SOPHI 6 (Midwest tier: Fort Wayne, Cincinnati, Columbus, St. Louis, Minneapolis), Carolinas expansion off the Charlotte anchor (Raleigh, Charleston), and one warm-climate hospitality bet (Fort Lauderdale).

---

## Latest state of the 14-market model

**Build date:** May 11, 2026
**Engine:** `src/normalize_v3_14mkt.py` in `joshuapcasey/sophi-market-map`

| Metric | SOPHI 6 (locked) | + 8 expansion | 14-market total |
|---|---:|---:|---:|
| Accounts | 203 | 692 | **895** |
| TAM | $150.35M | $424.20M | **$574.54M** |
| SAM | $57.27M | $212.37M | **$269.64M** |
| In-SAM accounts | 93 | 315 | **408** |
| Y5 SOM | $27.58M | $61.80M | **$89.38M** |
| 5-yr cumulative SOM | $73.39M | $172.10M | **$245.50M** |
| Accounts won by Y5 | 34 / 93 | 86 / 315 | **120 / 408** |

**Regression property:** The locked 6-market v3 regression passes bit-for-bit. Enrichment, operator xref, and self-park repricing were applied *only* to the 8 expansion markets, so the live 6-market bundle (`data.js`) is unchanged.

### Per-market Y5 (8 expansion markets)

| Market | TAM | SAM | Y5 SOM | 5-yr cum | In-SAM |
|---|---:|---:|---:|---:|---:|
| Fort Wayne | $9.10M | $1.40M | $0.36M | $0.36M | 5 |
| Cincinnati | $60.26M | $19.08M | $6.24M | $17.54M | 35 |
| Columbus | $50.88M | $25.64M | $10.38M | $22.33M | 42 |
| Minneapolis | $72.77M | $38.20M | $8.25M | $25.17M | 51 |
| St. Louis | $64.02M | $23.43M | $4.35M | $13.70M | 30 |
| Raleigh | $34.23M | $18.29M | $7.20M | $20.72M | 39 |
| Charleston | $34.97M | $20.90M | $8.46M | $25.59M | 43 |
| Fort Lauderdale | $97.97M | $65.43M | $16.55M | $46.69M | 70 |

---

## Methodology deltas from the SOPHI 6 engine

The 14-market engine layers three additions on top of the SOPHI 6 methodology. These would carry forward into an Expansion Growth Model:

1. **WAS-dominant priority reweight** — `base_priority = pool_base + v7_bump + WAS×300 + min(TAM/$1M × 10, 80)`. 1.0 WAS gap ≈ $30M TAM equivalent. This prevents cold expansion markets from picking the largest hotel first when no relationships exist.
2. **New-cold-market Y1 lockout** — The 8 expansion markets cannot organically acquire in Y1 (only forced anchors or v7 carve-outs). This encodes the "no field presence yet" reality.
3. **Self-park repricing for no-valet properties** — Hotels without valet get `rooms × occ × 0.40 × sp_rate × 365`; restaurants get `seats × turnover × 0.10 × sp_rate × op_days`. Verified free-parking accounts get moved out of SAM entirely.

All other engine components (operator gates for Towne Park / LAZ / SP+ / Propark / ABM / PMC / Reimagined, ownership-group multipliers, S-curve targets, per-market caps, WAS/SAM decoupling, $150K micro-pool floor) come directly from the SOPHI 6 methodology and are unchanged.

---

## Build trajectory — three refinement passes

| Stage | 14-mkt Y5 SOM | 14-mkt 5-yr cum | What changed |
|---|---:|---:|---|
| Pre-enrichment baseline | $130.36M | $410.22M | Raw account universe research |
| + Operator + rate enrichment | $115.17M | $361.82M | 364 accounts enriched with actual valet operators + published rates |
| + Operator cross-reference | $86.56M | $246.58M | 71 accounts moved from "in-house" to gated national operators |
| + Self-park repricing (current) | **$89.38M** | **$245.50M** | 28 no-valet accounts repriced or removed from SAM |

The single biggest reveal from this work: **1 in 3 accounts initially tagged "in-house" or "unknown" was actually run by a national operator** (Towne Park, LAZ, SP+, Propark). That finding **reframed expansion as a partnership/M&A unlock strategy** rather than a pure organic sales motion — a strategic conclusion that survives regardless of whether the underlying numbers get refreshed.

---

## What partnership unlocks look like

If SOPHI secures national operator agreements before entering these markets, the Y5 profile shifts materially. Order of importance from the xref research:

1. **Towne Park** — Largest unlock. ~58 properties portfolio-wide (31 new + 27 in SOPHI 6). Anchors include Diplomat, W Fort Lauderdale, Four Seasons Minneapolis, Westin Beach, the Marriott Renaissance family, Margaritaville, Sonesta Fort Lauderdale Beach, JW Marriott MOA, and multiple healthcare flagships.
2. **SP+ / Metropolis** — ~9 new accounts including Hilton Cincinnati Netherland, Hilton Minneapolis, Hilton Fort Lauderdale Marina, Marquette Hotel, and Hotel Ivy Luxury Collection.
3. **LAZ Parking** — ~10 new accounts including Hyatt Regency St. Louis at the Arch, Hyatt Regency Columbus, Hyatt Regency Minneapolis, and Four Seasons St. Louis.
4. **Propark** — ~10 new accounts including Conrad Fort Lauderdale, Marriott St. Louis Grand, Le Méridien St. Louis, and Dewberry Charleston.

Hospital operators (Towne Park, LAZ, Reimagined) overlap heavily with hotel operators — a single partnership can unlock multiple verticals in the same market.

---

## Where the data lives

**Primary preservation:** [Google Drive folder — SOPHI Expansion Research (Deferred) — Session 8d590dde](https://drive.google.com/drive/folders/1o0Z87e9b8OsSIwhMilQ0k_6Pd2nGeTIv). Contains all 4 memos, both account JSONs, all 3 research CSVs, the per-market ZIP, and a README with the full "do not quote" disclaimer. Preserved on August 31, 2026 to protect these artifacts from session drift.

**Not in `joshuapcasey/sophi-market-map`** — despite what older memos referenced. The 14-market files were sandbox working files during session `8d590dde` that never landed in the repo. Two of them (`normalize_v3_14mkt.py`, the engine; `data_14mkt.js`, the front-end bundle) exist only as references in the memos and would need to be re-implemented from the methodology description in `V3_14MARKET_RESULTS.md`. See [`sophi-market-map/EXPANSION_PROVENANCE.md`](https://github.com/joshuapcasey/sophi-market-map/blob/main/EXPANSION_PROVENANCE.md) for the full account of what's missing and the rules for future 14-market integration.

**In Perplexity session `8d590dde`** (original research memos and CSVs — also mirrored in the Drive folder above):

| File | Purpose |
|---|---|
| `V3_14MARKET_RESULTS.md` | Final results memo, engine spec, per-market Y5 breakdown |
| `NEW_MARKET_ENRICHMENT_MEMO.md` | 364-account enrichment (operators, rates, brand mix) with per-market detail |
| `OPERATOR_XREF_MEMO.md` | 291-account operator cross-reference research and application rules |
| `SELF_PARK_REPRICING_MEMO.md` | 28-account repricing methodology and per-account audit |
| `enrichment_clean.csv` | Master enrichment table (364 rows) |
| `xref_combined.csv` | Full operator research output (291 rows) |
| `repricing_audit.csv` | Self-park repricing audit (28 rows) |
| `new_market_enrichment_csvs.zip` | Per-market drop-in CSVs |

---

## Reuse guidance for the Expansion Growth Model

**Ready to reuse as-is:**

- Engine spec (`normalize_v3_14mkt.py` methodology, including the three deltas above)
- Market selection (the 8 expansion markets are geographically defensible)
- Operator gate structure and partnership-unlock strategic framing
- Self-park repricing formula and free-parking exclusion rule

**Requires validation before feeding a valuation:**

1. **Data freshness** — Enrichment is May 2026. Hotel operators, published valet rates, and property status will have moved. A fresh enrichment pass on the 692 expansion accounts should precede any valuation work.
2. **135 inconclusive operator rows** — Left as-is (mostly "in-house") in the source data. On-the-ground sales-team validation would materially improve accuracy on this tail.
3. **46 unrepriced ambiguous accounts** — 23 "op=none but valet_rate populated" (likely in-house valet) + 23 "unknown operator + no valet rate." Should be resolved before another engine run.
4. **WAS re-scoring** — All 692 expansion accounts were WAS-auto-scored with v2 rubric heuristics. A manual pass by sales leadership would replace heuristic ownership-boost scores with real relationship data.
5. **Anchor identification** — Each expansion market needs its Charlotte-equivalent warm anchor identified before the Y1 lockout can be selectively released.
6. **Reconciliation against Acquisition Growth Model** — The 14-market model was built parallel to the SOPHI 6 acquisition work. The Expansion Growth Model needs to layer on top of the Acquisition Growth Model (SOPHI 6 + Indy/Denver operator acquisitions) rather than parallel to the pre-acquisition SOPHI 6.

**Do not reuse:**

- The final Y5 SOM of $89.38M as a valuation input. It is a research artifact, not a defensible number for an investor deck. Every input listed under "Requires validation" flows through to this figure.
- Any headline language that says "15 markets," "13 expansion markets," or "Markets by 2031: 15." Those are retired per [NAMING_CONVENTIONS.md](../NAMING_CONVENTIONS.md#versioning-language--retired).

---

## Naming for the future model

When the Expansion Growth Model gets built out, it should follow the [three-growth-model naming framework](../NAMING_CONVENTIONS.md#the-three-growth-models):

- **Model name:** Expansion Growth Model
- **Valuation anchor:** Expansion Growth Valuation
- **5-year P&L:** Expansion Growth Model — 5-year P&L
- **Portfolio label:** "SOPHI 14" is the natural extension of "SOPHI 6" if the current 8 expansion markets carry forward; a different market set would take a different label
- **What it answers:** "What is SOPHI worth once the same growth engine is applied to markets beyond the SOPHI 6?"

---

## See also

- [`../NAMING_CONVENTIONS.md`](../NAMING_CONVENTIONS.md) — canonical names for models, rounds, valuations, and portfolios
- [`../RENAME_MAP.md`](../RENAME_MAP.md) — historical rename map (Ambiguity Log item #4 references this note)
- `joshuapcasey/sophi-market-map` — source repo for the map app and the 14-market data files
