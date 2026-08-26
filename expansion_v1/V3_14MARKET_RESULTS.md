# Sophi v3 — 14-Market Penetration Results

**Latest build:** May 11, 2026 (post self-park repricing)
**Engine:** `src/normalize_v3_14mkt.py` (WAS-reincorporated, WAS×300 + new-cold-market Y1 lockout)
**Source data:** `src/accounts_v2_14mkt.json` (895 accounts, 14 markets — enriched + operator cross-referenced + self-park repriced)
**Outputs:** `src/accounts_v3_14mkt.json`, `data_14mkt.js`

---

## Headline (current state)

| Metric | 6-Mkt locked | + 8 New | **14-Mkt total** |
|---|---:|---:|---:|
| Accounts | 203 | 692 | **895** |
| TAM | $150.35M | $424.20M | **$574.54M** |
| SAM | $57.27M | $212.37M | **$269.64M** |
| In-SAM accounts | 93 | 315 | **408** |
| Y1 SOM | $4.02M | $0.00M | **$4.02M** |
| Y2 SOM | $7.45M | $26.75M | **$34.20M** |
| Y3 SOM | $13.36M | $36.07M | **$49.43M** |
| Y4 SOM | $20.97M | $47.50M | **$68.47M** |
| Y5 SOM | $27.58M | $61.80M | **$89.38M** |
| 5-yr cumulative | $73.39M | $172.10M | **$245.50M** |
| Accounts won | 34 / 93 | 86 / 315 | **120 / 408** |

> **Locked 6-market regression: PASSED bit-for-bit** across the v3 engine path. Live `data.js` is unchanged. Self-park repricing was applied **only to the 8 expansion markets** to preserve the locked baseline.

---

## Methodology Stack (v3, current)

1. **WAS auto-scoring** (`expansion_v1/auto_score_was.py`): v2 rubric (Fit 25% / Size 25% / Owner 20% / Addr 15% / Adj 15%). Cold-market and new-market addressability dampeners.
2. **WAS-dominant priority**: `base_priority = pool_base + v7_bump + WAS×300 + min(TAM/$1M × 10, 80)` — 1.0 WAS gap ≈ $30M TAM.
3. **New-cold-market Y1 lockout**: the 8 expansion markets cannot organically acquire Y1 (only forced anchors / v7 carve-outs).
4. **Operator gates**: Towne Park / LAZ / SP+ / ABM / Propark / PMC / Reimagined enforced via `normalize_operator()` in engine.
5. **SAM exclusions**: Venues, hospitals, airports = TAM-only (no SOM). Plus `extended_stay`, `micro` (<$150K TAM), `partnership`, `enterprise` pools excluded.
6. **Self-park repricing**: accounts with no valet service are repriced to self-park-only TAM (`rooms × occ × 0.40 × sp_rate × 365` for hotels; restaurants use `seats × turnover × 0.10 × sp_rate × op_days`). Free-parking properties moved out of SAM.

---

## Build Trajectory This Round

| Milestone | 6-Mkt Y5 | 14-Mkt Y5 | 14-Mkt 5-yr cum |
|---|---:|---:|---:|
| Pre-enrichment baseline | $28.29M | $130.36M | $410.22M |
| Post enrichment (operator + rates) | $28.29M | $115.17M | $361.82M |
| Post operator cross-reference | $28.29M | $86.56M | $246.58M |
| **Post self-park repricing (current)** | **$27.58M*** | **$89.38M** | **$245.50M** |

\* The previously memo-quoted $28.29M Y5 / $75.52M cum5 6-market baseline was inadvertently carried forward from the pre-xref state. Verified post-xref baseline is $27.58M Y5 / $73.39M cum5 — and self-park repricing did not touch it. Live `data.js` (6-market) was never regenerated from the 14-market build and remains unchanged.

---

## Per-market Y5 (8 expansion markets)

| Market | TAM | SAM | Y5 SOM | 5-yr cum | In-SAM |
|---|---:|---:|---:|---:|---:|
| ft_wayne | $9.10M | $1.40M | $0.36M | $0.36M | 5 |
| cincinnati | $60.26M | $19.08M | $6.24M | $17.54M | 35 |
| columbus | $50.88M | $25.64M | $10.38M | $22.33M | 42 |
| minneapolis | $72.77M | $38.20M | $8.25M | $25.17M | 51 |
| st_louis | $64.02M | $23.43M | $4.35M | $13.70M | 30 |
| raleigh | $34.23M | $18.29M | $7.20M | $20.72M | 39 |
| charleston | $34.97M | $20.90M | $8.46M | $25.59M | 43 |
| ft_lauderdale | $97.97M | $65.43M | $16.55M | $46.69M | 70 |

---

## Self-Park Repricing Impact (this round)

- **29 in-SAM accounts** in the 8 expansion markets repriced as self-park-only
- **18 moved out of SAM** (confirmed free parking — Sophi has no monetization path)
- **11 retained in cold_sam** at reduced TAM (paid self-park product fit remains)
- TAM removed from the 29 accounts: **$5.92M** ($9.58M → $3.66M)
- Net 14-mkt 5-yr cum impact: roughly flat ($246.58M → $245.50M); WAS reshuffled some replacements forward by a year

See `/home/user/workspace/self_park_reprice/SELF_PARK_REPRICING_MEMO.md` for the full methodology and per-account audit.
