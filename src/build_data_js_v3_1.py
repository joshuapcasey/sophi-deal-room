#!/usr/bin/env python3
"""Build v3.1 data.js from accounts_v3_1.json.

DRAFT — pending CFO advisor review. Non-destructive: writes to `data.v3_1.js`
alongside the existing `data.js` so the live app is unaffected.

Adds three new market centers (Houston, Detroit, South Bend) + caps.
Everything else is a byte-for-byte port of build_data_js_v3.py.
"""
import json
from pathlib import Path

HERE = Path(__file__).parent
REPO = HERE.parent
SRC = HERE
OUT = REPO / "data.v3_1.js"

with open(SRC / "accounts_v3_1.json") as f:
    data = json.load(f)

# Geocode lookup from v2
with open(SRC / "accounts_v2_geocoded.json") as f:
    v2 = json.load(f)

GEOCODES = {}
for mkey, m in v2["markets"].items():
    for a in m["accounts"]:
        GEOCODES[(mkey, a["name"])] = {
            "lat": a.get("lat"),
            "lng": a.get("lng"),
            "geocoded": a.get("geocoded", False),
        }

# v3.1 additions: new market centers for Houston / Detroit / South Bend
MARKET_CENTERS = {
    "denver":       [-104.9903, 39.7392],
    "charlotte":    [-80.8431, 35.2271],
    "indianapolis": [-86.1581, 39.7684],
    "phoenix":      [-112.0740, 33.4484],
    "cleveland":    [-81.6944, 41.4993],
    "louisville":   [-85.7585, 38.2527],
    # v3.1 new markets
    "houston":      [-95.3698, 29.7604],
    "detroit":      [-83.0458, 42.3314],
    "south_bend":   [-86.2520, 41.6764],
}

# v3.1 caps — high on new named-anchor markets (per refinement_v3_1.py MARKET_Y5_CAP_v31)
MARKET_CAP = {
    "charlotte":    0.50,
    "indianapolis": 0.50,
    "phoenix":      0.30,
    "denver":       0.30,
    "cleveland":    0.30,
    "louisville":   0.30,
    "houston":      0.85,  # v3.1
    "detroit":      0.85,  # v3.1
    "south_bend":   0.85,  # v3.1
}


def _tier(was):
    if was is None: return None
    if was >= 4.0: return "A"
    if was >= 3.4: return "B"
    if was >= 2.8: return "C"
    return "D"


def _tier_full(was):
    if was is None: return None
    if was >= 4.0: return "A — Hero"
    if was >= 3.4: return "B — Core"
    if was >= 2.8: return "C — Opportunistic"
    return "D — Skip / De-prioritize"


def trim_account(a, mkey):
    geo = GEOCODES.get((mkey, a["name"]), {})
    return {
        # Identity
        "name": a["name"],
        "type": a.get("type") or "Other",
        "pool": a.get("pool"),
        "in_sam": a.get("in_sam"),
        "rank": a.get("rank"),
        # v3 lifecycle
        "acquisition_year": a.get("acquisition_year"),
        "gate_status": a.get("gate_status") or "",
        "group_key": a.get("group_key") or "",
        "group_wins_at_acquisition": a.get("group_wins_at_acquisition"),
        "operator_gate": a.get("operator_gate") or "",
        # v3.1 additions
        "flagship_hotel": a.get("flagship_hotel", False),
        "owner_group": a.get("owner_group") or "",
        # Money
        "tam": round(a.get("tam") or 0),
        "sam_contrib": round(a.get("sam_contrib") or 0),
        "y1": round(a.get("y1") or 0),
        "y2": round(a.get("y2") or 0),
        "y3": round(a.get("y3") or 0),
        "y4": round(a.get("y4") or 0),
        "y5": round(a.get("y5") or 0),
        # Scoring
        "was": a.get("was"),
        "was_base": a.get("was_base"),
        "was_boost": a.get("was_boost"),
        "tier": _tier(a.get("was")),
        "tier_full": _tier_full(a.get("was")),
        # Legacy lifecycle (from v2)
        "sign_yr": a.get("sign_yr"),
        "curve": a.get("curve"),
        # Geo
        "lng": geo.get("lng"),
        "lat": geo.get("lat"),
        "geocoded": geo.get("geocoded", False),
        "address": a.get("address") or "",
        "area": a.get("area") or "",
        # Contact / property
        "phone": a.get("phone") or "",
        "email": a.get("email") or "",
        "url": a.get("url") or "",
        "rooms": a.get("rooms"),
        "seats": a.get("seats"),
        "valet_rate": a.get("valet_rate"),
        "self_park_rate": a.get("self_park_rate"),
        "occupancy": a.get("occupancy"),
        "valet_conv": a.get("valet_conv"),
        "gm": a.get("gm") or "",
        "gm_role": a.get("gm_role") or "",
        "management": a.get("management") or "",
        "garage_operator": a.get("garage_operator") or "",
        "valet_operator": a.get("valet_operator") or "",
        "tam_class": a.get("tam_class") or "",
        "tam_status": a.get("tam_status") or "",
        "tam_notes": a.get("tam_notes") or "",
        "location_notes": a.get("location_notes") or "",
        "pool_raw": a.get("pool_raw") or "",
        # Indy v7
        "v7_layer": a.get("v7_layer"),
        "chain_scale": a.get("chain_scale"),
        "brand": a.get("brand"),
    }


# Build output
output = {"markets": {}, "meta": data.get("meta", {})}
output["meta"]["methodology_version"] = "v3.1"
output["meta"]["market_caps"] = MARKET_CAP
output["meta"]["draft"] = True
output["meta"]["draft_note"] = "DRAFT — pending CFO advisor review. Includes §2.7 canonical SOPHI 6 update (Houston/Detroit/South Bend), §2.8 flagship hotel gate, §4 Elite Q1 2027 + VIP Q1 2028 named account additions."

# Split acquisition vs expansion for portfolio rollup
acquisition_y = {"y1": 0, "y2": 0, "y3": 0, "y4": 0, "y5": 0}
expansion_y = {"y1": 0, "y2": 0, "y3": 0, "y4": 0, "y5": 0}
acquisition_tam = expansion_tam = 0
acquisition_sam = expansion_sam = 0
acquisition_n = expansion_n = 0
acquisition_in_sam = expansion_in_sam = 0
acquisition_won = expansion_won = 0

for mkey, m in data["markets"].items():
    accts = [trim_account(a, mkey) for a in m["accounts"]]
    summary = m.get("summary", {}) or {}
    sby = summary.get("som_by_year", {}) or {}
    acq_counts = summary.get("acquisition_year_counts", {}) or {}
    n_acquired = sum(int(v) for k, v in acq_counts.items() if k != "never")
    growth_model = summary.get("growth_model", "acquisition")

    output["markets"][mkey] = {
        "name": m.get("name", mkey),
        "state": m.get("state", summary.get("state", "")),
        "center": MARKET_CENTERS.get(mkey),
        "cap": MARKET_CAP.get(mkey),
        "growth_model": growth_model,
        "accounts": accts,
        "summary": summary,
        "som_by_year": sby,
        "acquisition_year_counts": acq_counts,
        "n_acquired": n_acquired,
        "pool_counts": m.get("pool_counts", {}),
        "pool_tam": m.get("pool_tam", {}),
        "tier_counts": m.get("tier_counts", {}),
        "rollup": m.get("rollup"),
        "pool_structure_rollup": m.get("pool_structure_rollup"),
    }

    # Roll up separately by growth model
    if growth_model == "expansion":
        for y in ("y1", "y2", "y3", "y4", "y5"):
            expansion_y[y] += sby.get(y, 0) or 0
        expansion_tam += summary.get("tam", 0) or 0
        expansion_sam += summary.get("sam", 0) or 0
        expansion_n += len(accts)
        expansion_in_sam += len([a for a in accts if a.get("in_sam")])
        expansion_won += n_acquired
    else:
        for y in ("y1", "y2", "y3", "y4", "y5"):
            acquisition_y[y] += sby.get(y, 0) or 0
        acquisition_tam += summary.get("tam", 0) or 0
        acquisition_sam += summary.get("sam", 0) or 0
        acquisition_n += len(accts)
        acquisition_in_sam += len([a for a in accts if a.get("in_sam")])
        acquisition_won += n_acquired

output["portfolio"] = {
    "acquisition": {
        "tam": round(acquisition_tam),
        "sam": round(acquisition_sam),
        "n_accounts": acquisition_n,
        "n_in_sam": acquisition_in_sam,
        "n_acquired": acquisition_won,
        "som_by_year": {y: round(v) for y, v in acquisition_y.items()},
        "som_5yr_cumulative": round(sum(acquisition_y.values())),
    },
    "expansion": {
        "tam": round(expansion_tam),
        "sam": round(expansion_sam),
        "n_accounts": expansion_n,
        "n_in_sam": expansion_in_sam,
        "n_acquired": expansion_won,
        "som_by_year": {y: round(v) for y, v in expansion_y.items()},
        "som_5yr_cumulative": round(sum(expansion_y.values())),
    },
    # Combined for backward compat with existing front-end
    "tam": round(acquisition_tam + expansion_tam),
    "sam": round(acquisition_sam + expansion_sam),
    "n_accounts": acquisition_n + expansion_n,
    "n_in_sam": acquisition_in_sam + expansion_in_sam,
    "n_acquired": acquisition_won + expansion_won,
    "som_by_year": {y: round(acquisition_y[y] + expansion_y[y]) for y in ("y1", "y2", "y3", "y4", "y5")},
    "som_5yr_cumulative": round(sum(acquisition_y.values()) + sum(expansion_y.values())),
}

# Write data.v3_1.js (NOT overwriting live data.js)
with open(OUT, "w") as f:
    f.write("/* Auto-generated by build_data_js_v3_1.py — DRAFT — do not deploy */\n")
    f.write("window.SOPHI_DATA_V3_1 = ")
    json.dump(output, f, separators=(",", ":"), default=str)
    f.write(";\n")

print(f"Wrote {OUT} ({OUT.stat().st_size:,} bytes)")
print(f"Markets: {list(output['markets'].keys())}")
print(f"Total accounts: {sum(len(m['accounts']) for m in output['markets'].values())}")
print()
print("Portfolio v3.1:")
print(f"  ACQUISITION GROWTH MODEL:")
acq = output["portfolio"]["acquisition"]
print(f"    Y1={acq['som_by_year']['y1']:>12,}  Y5={acq['som_by_year']['y5']:>12,}  cumulative={acq['som_5yr_cumulative']:>12,}")
print(f"    accounts_won={acq['n_acquired']}/{acq['n_in_sam']}  TAM={acq['tam']:,}  SAM={acq['sam']:,}")
print(f"  EXPANSION GROWTH MODEL (placeholder):")
exp = output["portfolio"]["expansion"]
print(f"    Y1={exp['som_by_year']['y1']:>12,}  Y5={exp['som_by_year']['y5']:>12,}  cumulative={exp['som_5yr_cumulative']:>12,}")
print(f"    accounts_won={exp['n_acquired']}/{exp['n_in_sam']}  TAM={exp['tam']:,}  SAM={exp['sam']:,}")
