# Sophi 8-Market Expansion — v1 Summary

**Date:** May 7, 2026
**Author:** Computer (research + assembly), Joshua Casey (review)
**Scope:** Build Charlotte-equivalent account inventory for 8 new markets to extend the Sophi growth model from 6 → 14 markets.

---

## Headline Numbers

| Metric | Value |
|---|---|
| New markets added | 8 |
| New accounts inventoried | **692** |
| New TAM (conservative, capped) | **$424.20M** |
| Existing 6-market TAM (v3) | $150.35M |
| Combined 14-market TAM | **$574.55M** |
| Avg TAM / account (new) | $613K |
| Avg TAM / account (existing v3) | ~$1.62M (skewed by mature/dense markets) |

The new-market average is lower than v3 because the new set adds mid-size metros (Ft Wayne, Charleston, Raleigh) alongside venue-heavy markets (Minneapolis, St. Louis, Cincinnati). The mix is intentional and consistent with Sophi's stated diversification thesis.

---

## Per-Market Totals

| Market | Accounts | TAM Total | Avg TAM/Acct | Mix Profile |
|---|---:|---:|---:|---|
| Ft Wayne, IN | 65 | $9.10M | $140K | Light — limited downtown density, no major sports |
| Cincinnati, OH | 81 | $60.26M | $744K | Sports + convention heavy (3 venues capped) |
| Columbus, OH | 80 | $50.88M | $636K | Convention + Ohio State spillover |
| Minneapolis, MN | 100 | $72.77M | $728K | Acquisition target — twin-stadium profile |
| St. Louis, MO | 79 | $64.02M | $810K | Stadium + casino district |
| Raleigh, NC | 84 | $34.23M | $407K | Hospital-heavy (Duke/UNC corridor adjacency) |
| Charleston, SC | 100 | $34.97M | $350K | Hospitality-dense, smaller venue base |
| Ft Lauderdale, FL | 103 | $97.97M | $951K | Convention + cruise + arena — highest ceiling |
| **TOTAL** | **692** | **$424.20M** | **$613K** | |

## Account Mix (Combined)

| Type | Count | TAM | Share |
|---|---:|---:|---:|
| Hotels | 269 | $206.09M | 48.6% |
| Venues | 108 | $173.61M | 40.9% |
| Restaurants | 263 | $38.68M | 9.1% |
| Hospitals | 52 | $5.82M | 1.4% |
| **Total** | **692** | **$424.20M** | 100% |

Venues drive ~41% of TAM despite being only 16% of accounts — consistent with Charlotte/Denver/Cleveland v3 patterns. **All venue values are conservatively capped (see below).**

---

## Capped Accounts — Manual Review Recommended

17 venues hit the **$5M/account TAM cap** during assembly. The raw computed value is preserved in each row's `tam_status` field for your review. These are likely understated in the conservative number; you may want to relax the cap or rebuild venue formulas in `normalize_v3.py` before final SOM.

| Market | Venue |
|---|---|
| Cincinnati | Great American Ball Park, Heritage Bank Center, Duke Energy Convention Center, Hard Rock Casino Cincinnati, Riverbend Music Center |
| Columbus | Greater Columbus Convention Center, Nationwide Arena |
| Minneapolis | Target Field, Target Center, Grand Casino Arena |
| St. Louis | Busch Stadium, Enterprise Center, America's Center Convention Complex |
| Charleston | North Charleston Coliseum |
| Ft Lauderdale | Greater Fort Lauderdale Convention Center, Amerant Bank Arena, Port Everglades Cruise Terminal |

## Zero-TAM Accounts — Capacity Field Missing

6 accounts produced $0 TAM because no usable capacity / event-day data was sourced. They are kept in inventory (with `no_capacity` flag in `tam_status`) so you can fill the field manually without re-running research:

- Grand Wayne Convention Center (Ft Wayne)
- Saint Louis Art Museum, City Museum (St. Louis)
- Charleston Area Convention Center, Edmund's Oast Brewing Co (Charleston)
- Sawgrass Mills Mall (Ft Lauderdale)

---

## Methodology — What Was Held Constant From Charlotte v3

- **24-column CSV schema** mirrored exactly (name, type, address, url, rooms, seats, beds, capacity, self_park_rate, valet_rate, occupancy, turnover, valet_conv, op_days, peak_mod, valet_operator, garage_operator, management, ownership_group, gm, email, phone, location_notes, sourcing_notes).
- **TAM formulas** unchanged:
  - Hotel: `rooms × occ × valet_conv × valet_rate × op_days × peak_mod`
  - Restaurant: `seats × turnover × valet_conv × valet_rate × op_days × peak_mod`
  - Hospital: `beds × 0.6 visitor_mult × valet_conv × valet_rate × op_days × peak_mod`
  - Venue: `min(capacity, 22000) × valet_conv × avg_rate × op_days × peak_mod`
- **Defaults** per Charlotte cookbook: hotel occ 0.60, valet_conv 0.40 (200+ rooms) / 0.30 (smaller); restaurant turnover 1.5, valet_conv 0.125; hospital valet_conv 0.20 + 0.6 visitor mult; venue valet_conv 0.15.
- **Rate imputation waterfall:** sourced valet → sourced self-park × 2 → market+type median → type default ($35 hotel / $25 venue / $12 restaurant / $8 hospital).
- **Sanity caps:** venue capacity 22K, venue TAM $5M, hotel TAM $8M, restaurant TAM $1M (no hotel/restaurant hit the cap; only venues did).

## What's New / Different vs Charlotte

- **Auto-classed defaults explicitly logged** in `sourcing_notes` per row so you can audit which fields were imputed vs sourced.
- **Operational fields (operator, mgmt, ownership, GM, contact)** filled best-effort from public sources; gaps marked `unknown` rather than guessed.
- **Minneapolis treated as standard market** per your direction — no acquisition overlay applied. Acquisition multiples can be modeled separately in the financial model.

---

## File Inventory

All under `/home/user/workspace/sophi-market-map/expansion_v1/`:

```
RESEARCH_BRIEF.md              — schema + cookbook handed to research subagents
assemble.py                    — TAM compute + XLSX/JSON assembler
expansion_accounts.json        — combined drop-in for normalize_v3.py (692 accts)
raw/<market>_inventory.csv     — 8 files, raw research output
memos/<market>_memo.md         — 8 files, per-market 1-page narrative
xlsx/<market>_2026_scored.xlsx — 8 files, 3-sheet workbooks matching charlotte_2026_scored
```

Each `*_2026_scored.xlsx` contains:
- **Accounts** — full inventory with all 24 columns + computed TAM + tam_status
- **TAM_Conservative** — TAM rollup by type, with capped/raw split
- **WAS_Scoring_v2** — stub WAS columns ready for your scoring pass

---

## Recommended Next Steps

1. **Spot-check 2-3 high-TAM accounts per market** (especially venues) against the `tam_status` raw values to decide whether to lift the venue cap.
2. **Fill capacity** for the 6 zero-TAM accounts if you want them in SAM/SOM.
3. **WAS scoring** — the WAS_Scoring_v2 sheets are stubbed; run your scoring pass before integration.
4. **Integration** — when ready, merge `expansion_accounts.json` into `src/accounts_v3.json` and re-run `normalize_v3.py`. I have not auto-merged; awaiting your sign-off on caps + WAS scores first.
5. **Front-end** — `build_data_js_v3.py` will need to be re-run after integration to refresh `data.js` for the live map.

---

## Open Questions for You

- **Venue cap:** keep $5M conservative, lift to $10M, or rebuild venue formula by event-night model?
- **WAS scoring:** want me to score the 692 new accounts using the same v3 rubric, or hold for your hand-tuned pass?
- **Combined SOM:** ready to run the 14-market combined SOM, or wait until WAS is finalized?
