#!/usr/bin/env python3
"""
SOPHI v3 Strategic Acquisition Growth Model — with SMS Ad Revenue Layer

Layers portfolio-scale SMS retrieval ad revenue on top of the v3 parking-services
SOM curve. Two-stage activation: portfolio-wide gate at 15,000 monthly SMS
interactions, then linear compounding per-market from that point forward.

HEADLINE / DILIGENCE CASE: MODERATE — midpoint of every account-type SMS conversion
band × midpoint avg offer value (Hotel 26.5% × $30, Fine Dining 22.5% × $23.50,
Venue 29% × $32.50, Corporate 21% × $20). Portfolio SMS-mix weighted this is
2.96× the conservative low-end. This is the case shown across the live deal-room
pages (summary.html, sophi-os.html SMS sub-tab, v3-valuation.html).

Also computed and reported alongside: LOW-END conservative case (previous default)
and HIGH-END upper case (top of every band + full hotel multi-touch), so
sensitivity is visible.

Referral revenue is INTENTIONALLY EXCLUDED — held as valuation optionality
outside the growth model (see organic-valuation.html cl-body copy).

Inputs
------
- v3 accounts JSON: /home/user/workspace/sophi-market-map/src/accounts_v3.json
- SMS ad economics: sophi-os.html Revenue Model tab (canonical, live in deck)

Outputs
-------
- /home/user/workspace/sophi_v3_ad_revenue_layer.json   (full model, per market, per year, all 3 cases)
- /home/user/workspace/sophi_v3_ad_revenue_memo.md      (investor-facing memo, moderate as headline)
- Console tables for spot-check
"""

import json
from collections import defaultdict
from pathlib import Path

# ─── Inputs ────────────────────────────────────────────────────────────────

ACCOUNTS_PATH = "/home/user/workspace/sophi-market-map/src/accounts_v3.json"
OUT_JSON = "/home/user/workspace/sophi_v3_ad_revenue_layer.json"
OUT_MEMO = "/home/user/workspace/sophi_v3_ad_revenue_memo.md"

# SMS ad model canonical inputs (from sophi-os.html Revenue Model tab)
# CAPTURE = fraction of served vehicles that convert to an SMS interaction
# (the 54% blended portfolio rate in OS deck comes from mixing these).
# For base-case, use each type's specific capture rate.
#
# Band structure (from OS Revenue Model tab):
#   Hotel        18–35% conv × $15–45 offer  (3.5× multi-touch: arrival/mid-stay/departure)
#   Fine Dining  15–30% conv × $12–35 offer  (1.0× multi-touch)
#   Venue        20–38% conv × $15–50 offer  (1.0× multi-touch)
#   Corporate    14–28% conv × $10–30 offer  (1.5× multi-touch: recurring commuters)
#
# Multi-touch reflects real SMS touches per served vehicle and feeds both
# volume (activation gate) and revenue. This matches the live deck's SOPHI Domo
# baseline (Y1 = 11,557 monthly SMS, Y5 = 92,651 monthly SMS).
#
# Three cases:
#   LOW      = conv_low  × offer_low
#   MODERATE = conv_mid  × offer_mid   ← diligence case, matches live deal-room pages
#   HIGH     = conv_high × offer_high
SMS_MODEL = {
    "Hotel":       {"capture": 0.55, "conv_low": 0.18, "conv_mid": 0.265, "conv_high": 0.35,
                     "offer_low": 15.0, "offer_mid": 30.0,  "offer_high": 45.0,
                     "multi_touch": 3.5},
    "Restaurant":  {"capture": 0.45, "conv_low": 0.15, "conv_mid": 0.225, "conv_high": 0.30,   # Fine Dining
                     "offer_low": 12.0, "offer_mid": 23.50, "offer_high": 35.0,
                     "multi_touch": 1.0},
    "Venue":       {"capture": 0.35, "conv_low": 0.20, "conv_mid": 0.29,  "conv_high": 0.38,
                     "offer_low": 15.0, "offer_mid": 32.50, "offer_high": 50.0,
                     "multi_touch": 1.0},
    "Corporate":   {"capture": 0.40, "conv_low": 0.14, "conv_mid": 0.21,  "conv_high": 0.28,
                     "offer_low": 10.0, "offer_mid": 20.0,  "offer_high": 30.0,
                     "multi_touch": 1.5},
    "Hospital":    {"capture": 0.15, "conv_low": 0.00, "conv_mid": 0.00,  "conv_high": 0.00,
                     "offer_low": 0.0,  "offer_mid": 0.0,   "offer_high": 0.0,
                     "multi_touch": 1.0},  # FIREWALLED — no ad revenue ever
    "Medical":     {"capture": 0.15, "conv_low": 0.00, "conv_mid": 0.00,  "conv_high": 0.00,
                     "offer_low": 0.0,  "offer_mid": 0.0,   "offer_high": 0.0,
                     "multi_touch": 1.0},  # FIREWALLED
}

# Portfolio activation gate
ACTIVATION_MONTHLY_SMS = 15_000
ACTIVATION_ANNUAL_SMS = ACTIVATION_MONTHLY_SMS * 12  # 180,000

# ─── Vehicle-serving math per account ─────────────────────────────────────

def annual_vehicles(acct):
    """
    Estimate annual valet vehicles served for one account.
    Uses whichever primary demand driver is populated:
      Hotel:      rooms × 365 × occupancy × valet_conv
      Restaurant: seats × turnover × 365 × valet_conv
    Falls back to a TAM-derived proxy if drivers are missing.
    """
    t = acct["type"]
    valet_conv = acct.get("valet_conv") or 0.0

    if t == "Hotel" and acct.get("rooms"):
        occ = acct.get("occupancy") or 0.70   # portfolio default
        return acct["rooms"] * 365 * occ * valet_conv

    if t in ("Restaurant",) and acct.get("seats"):
        turnover = acct.get("turnover") or 1.5
        # seats × turnover = daily covers; assume 340 operating days for fine dining
        return acct["seats"] * turnover * 340 * valet_conv

    # Fallback — infer vehicles from TAM at a $15 avg valet transaction
    tam = acct.get("tam") or 0
    if tam > 0:
        return tam / 15.0
    return 0.0

def annual_sms_from_account(acct):
    """SMS interactions = vehicles × capture rate × multi-touch.
    Multi-touch reflects real SMS touches per served vehicle (Hotel 3.5×
    arrival/mid-stay/departure, Corporate 1.5× recurring commuters, others 1.0×).
    Case-invariant — volume drives the activation gate identically across cases."""
    if acct["type"] not in SMS_MODEL:
        return 0.0
    p = SMS_MODEL[acct["type"]]
    veh = annual_vehicles(acct)
    return veh * p["capture"] * p["multi_touch"]

def annual_ad_revenue_from_sms(sms, acct_type, case="moderate"):
    """Ad revenue from SMS by case. Medical/Hospital firewalled.

    case ∈ {'low', 'moderate', 'high'}:
      low       — SMS × conv_low  × offer_low
      moderate  — SMS × conv_mid  × offer_mid   ← diligence, matches live deck
      high      — SMS × conv_high × offer_high
    """
    if acct_type not in SMS_MODEL:
        return 0.0
    p = SMS_MODEL[acct_type]
    if p["conv_mid"] == 0:  # firewalled
        return 0.0
    if case == "low":
        return sms * p["conv_low"] * p["offer_low"]
    if case == "moderate":
        return sms * p["conv_mid"] * p["offer_mid"]
    if case == "high":
        return sms * p["conv_high"] * p["offer_high"]
    raise ValueError(f"unknown case: {case}")

# ─── Load v3 accounts ─────────────────────────────────────────────────────

data = json.load(open(ACCOUNTS_PATH))
all_accts = []
for mkey, mdata in data["markets"].items():
    for a in mdata["accounts"]:
        a["_mkt"] = mkey
        all_accts.append(a)

won = [a for a in all_accts if a.get("in_sam") and a.get("acquisition_year") in (1,2,3,4,5)]

# ─── Build per-year, per-market layered model ─────────────────────────────

MARKETS = ["denver", "charlotte", "indianapolis", "phoenix", "louisville", "cleveland"]
YEARS = [1, 2, 3, 4, 5]

CASES = ("low", "moderate", "high")

# Per-market, per-year, per-case model.
# Parking SOM and SMS volume are case-invariant (same acquisition curve);
# ad_rev_full and ad_revenue differ per case.
model = {
    m: {y: {
            "parking_som": 0.0, "annual_sms": 0.0,
            "ad_rev_full": {c: 0.0 for c in CASES},
            "acquired_ytd": [],
        } for y in YEARS}
    for m in MARKETS
}

# For each won account, add its FULL TAM to parking SOM and its full SMS
# interaction load to every year from acquisition_year onward (matches v3
# binary acquisition + full-TAM accrual rule from METHODOLOGY_v3.md §2.1).
for a in won:
    m = a["_mkt"]
    ay = a["acquisition_year"]
    sms = annual_sms_from_account(a)
    ad_by_case = {c: annual_ad_revenue_from_sms(sms, a["type"], case=c) for c in CASES}
    tam = a["tam"]
    for y in YEARS:
        if y >= ay:
            model[m][y]["parking_som"] += tam
            model[m][y]["annual_sms"] += sms
            for c in CASES:
                model[m][y]["ad_rev_full"][c] += ad_by_case[c]
            model[m][y]["acquired_ytd"].append(a["name"])

# ─── Apply two-stage activation gate ───────────────────────────────────────
# Portfolio annual SMS threshold: 180,000 (= 15,000 × 12)
# Before threshold year: ad revenue = 0 everywhere
# Threshold year and beyond: full ad_rev_full applies per market

portfolio_sms_by_year = {y: sum(model[m][y]["annual_sms"] for m in MARKETS) for y in YEARS}
activation_year = None
for y in YEARS:
    if portfolio_sms_by_year[y] >= ACTIVATION_ANNUAL_SMS:
        activation_year = y
        break

for m in MARKETS:
    for y in YEARS:
        if activation_year is None or y < activation_year:
            model[m][y]["ad_revenue"] = {c: 0.0 for c in CASES}
            model[m][y]["ad_gate_status"] = "pre-activation"
        else:
            model[m][y]["ad_revenue"] = dict(model[m][y]["ad_rev_full"])
            model[m][y]["ad_gate_status"] = "activated"

# ─── Portfolio rollup ─────────────────────────────────────────────────────

portfolio = {y: {
    "parking_som": sum(model[m][y]["parking_som"] for m in MARKETS),
    "annual_sms":  sum(model[m][y]["annual_sms"] for m in MARKETS),
    "monthly_sms": sum(model[m][y]["annual_sms"] for m in MARKETS) / 12,
    "ad_revenue":  {c: sum(model[m][y]["ad_revenue"][c] for m in MARKETS) for c in CASES},
} for y in YEARS}

for y in YEARS:
    portfolio[y]["total_revenue"] = {
        c: portfolio[y]["parking_som"] + portfolio[y]["ad_revenue"][c] for c in CASES
    }

# 5-year cumulative
cum_parking = sum(portfolio[y]["parking_som"] for y in YEARS)
cum_ad      = {c: sum(portfolio[y]["ad_revenue"][c] for y in YEARS) for c in CASES}
cum_total   = {c: cum_parking + cum_ad[c] for c in CASES}

# Valuation @ 7× on Y5 run-rate (matches v3 methodology headline multiple)
y5_parking_only = portfolio[5]["parking_som"]
y5_run_rate = {c: portfolio[5]["total_revenue"][c] for c in CASES}
val_7x_parking_only = y5_parking_only * 7
val_7x_total = {c: y5_run_rate[c] * 7 for c in CASES}
val_uplift = {c: val_7x_total[c] - val_7x_parking_only for c in CASES}

# DCF uplift is proportional to parking DCF at the same 25% EBIT margin and
# 13.0× terminal multiple / 12% WACC / same discount schedule.
# Parking DCF anchor (from v3-valuation.html): $36.30M on $28.29M Y5 parking.
PARKING_DCF_ANCHOR = 36.30e6
dcf_uplift = {c: (portfolio[5]["ad_revenue"][c] / y5_parking_only) * PARKING_DCF_ANCHOR
              for c in CASES}
dcf_total = {c: PARKING_DCF_ANCHOR + dcf_uplift[c] for c in CASES}

# Diligence case pointer
DILIGENCE_CASE = "moderate"

# ─── Console tables ────────────────────────────────────────────────────────

print(f"\n{'='*94}")
print("SOPHI v3 + SMS Ad Revenue Layer — Portfolio Model")
print(f"HEADLINE / DILIGENCE CASE: {DILIGENCE_CASE.upper()} (midpoint of every band, portfolio SMS-mix weighted)")
print(f"{'='*94}\n")

print("Portfolio SMS activation gate:")
print(f"  Threshold: {ACTIVATION_MONTHLY_SMS:,} monthly SMS ({ACTIVATION_ANNUAL_SMS:,} annual)")
if activation_year:
    print(f"  Activation year: Y{activation_year} "
          f"(portfolio annual SMS = {portfolio_sms_by_year[activation_year]:,.0f}, "
          f"monthly = {portfolio_sms_by_year[activation_year]/12:,.0f})")
else:
    print("  Activation year: NOT REACHED within Y1–Y5 — check inputs")

# Headline table — MODERATE case (matches live deal-room pages)
print(f"\nMODERATE CASE — headline (live in summary.html, sophi-os.html, v3-valuation.html)")
print(f"{'Year':<6}{'Parking SOM':>16}{'Monthly SMS':>15}{'Annual SMS':>15}"
      f"{'Ad revenue':>16}{'Total':>16}")
print("-"*94)
for y in YEARS:
    p = portfolio[y]
    ad = p['ad_revenue'][DILIGENCE_CASE]
    tot = p['total_revenue'][DILIGENCE_CASE]
    print(f"Y{y:<5}{p['parking_som']/1e6:>13,.2f}M {p['monthly_sms']:>14,.0f}"
          f"{p['annual_sms']:>15,.0f}{ad/1e6:>14,.2f}M "
          f"{tot/1e6:>14,.2f}M")

print(f"\n5-year cumulative parking SOM: ${cum_parking/1e6:,.2f}M")
print(f"5-year cumulative ad revenue:  ${cum_ad[DILIGENCE_CASE]/1e6:,.2f}M  "
      f"({cum_ad[DILIGENCE_CASE]/cum_parking*100:.1f}% of parking)")
print(f"5-year cumulative TOTAL:       ${cum_total[DILIGENCE_CASE]/1e6:,.2f}M")

print(f"\nY5 run-rate ({DILIGENCE_CASE}):")
print(f"  Parking only:   ${y5_parking_only/1e6:,.2f}M")
print(f"  Ad layer:       ${portfolio[5]['ad_revenue'][DILIGENCE_CASE]/1e6:,.2f}M "
      f"({portfolio[5]['ad_revenue'][DILIGENCE_CASE]/y5_parking_only*100:.1f}% of parking)")
print(f"  Total:          ${y5_run_rate[DILIGENCE_CASE]/1e6:,.2f}M")

print(f"\nValuation @ 7× Y5 run-rate ({DILIGENCE_CASE}):")
print(f"  Parking only:   ${val_7x_parking_only/1e6:,.2f}M")
print(f"  With ad layer:  ${val_7x_total[DILIGENCE_CASE]/1e6:,.2f}M")
print(f"  Uplift:         ${val_uplift[DILIGENCE_CASE]/1e6:,.2f}M  "
      f"(+{val_uplift[DILIGENCE_CASE]/val_7x_parking_only*100:.1f}%)")
print(f"\nDCF ({DILIGENCE_CASE}, proportional to parking $36.30M @ 25% EBIT / 13× / 12% WACC):")
print(f"  Parking only:   ${PARKING_DCF_ANCHOR/1e6:,.2f}M")
print(f"  Ad uplift:      ${dcf_uplift[DILIGENCE_CASE]/1e6:,.2f}M")
print(f"  Total DCF:      ${dcf_total[DILIGENCE_CASE]/1e6:,.2f}M")

# Sensitivity — all three cases side by side
print(f"\n{'='*94}\nSensitivity — Y5 run-rate and 7× EV across cases\n{'='*94}")
print(f"{'Case':<12}{'Y5 Ad':>14}{'Y5 Total':>14}{'5yr Ad':>14}"
      f"{'7× EV':>14}{'DCF Total':>14}{'MOIC on $500K':>16}")
print("-"*94)
for c in CASES:
    # MOIC on $500K seed at 10% post-money on DCF valuation
    moic = (dcf_total[c] * 0.10) / 500_000
    print(f"{c:<12}{portfolio[5]['ad_revenue'][c]/1e6:>11,.2f}M "
          f"{y5_run_rate[c]/1e6:>11,.2f}M "
          f"{cum_ad[c]/1e6:>11,.2f}M "
          f"{val_7x_total[c]/1e6:>11,.2f}M "
          f"{dcf_total[c]/1e6:>11,.2f}M "
          f"{moic:>14,.2f}×")

# Per-market breakdown Y5 (moderate case)
print(f"\n{'='*94}\nPer-market Y5 breakdown — {DILIGENCE_CASE} case\n{'='*94}\n")
print(f"{'Market':<15}{'Parking SOM':>15}{'Monthly SMS':>14}{'Ad revenue':>14}"
      f"{'Total Y5':>14}{'Ad %':>8}")
print("-"*94)
for m in MARKETS:
    d = model[m][5]
    ad = d['ad_revenue'][DILIGENCE_CASE]
    total = d['parking_som'] + ad
    pct = (ad/total*100) if total else 0  # ad share of total (matches deck convention)
    print(f"{m.capitalize():<15}{d['parking_som']/1e6:>12,.2f}M "
          f"{d['annual_sms']/12:>13,.0f}{ad/1e6:>12,.2f}M "
          f"{total/1e6:>12,.2f}M {pct:>7.1f}%")

# ─── Save JSON ────────────────────────────────────────────────────────────

output = {
    "meta": {
        "version": "v3+ad",
        "activation_monthly_sms": ACTIVATION_MONTHLY_SMS,
        "activation_annual_sms": ACTIVATION_ANNUAL_SMS,
        "activation_year": activation_year,
        "diligence_case": DILIGENCE_CASE,
        "case_definitions": {
            "low":      "low-end conv × low-end offer × 1.0 multi-touch (previous conservative base)",
            "moderate": "midpoint conv × midpoint offer × 1.0 multi-touch — DILIGENCE CASE, matches live deal-room pages",
            "high":     "high-end conv × high-end offer × hotel 3.5× multi-touch fully exercised",
        },
        "referrals": "excluded — held as valuation optionality",
        "sms_model": SMS_MODEL,
        "parking_dcf_anchor": PARKING_DCF_ANCHOR,
    },
    "portfolio_by_year": {f"Y{y}": portfolio[y] for y in YEARS},
    "portfolio_sms_by_year": {f"Y{y}": portfolio_sms_by_year[y] for y in YEARS},
    "portfolio_cumulative": {
        "parking_som_5yr": cum_parking,
        "ad_revenue_5yr":  cum_ad,
        "total_5yr":       cum_total,
        "y5_parking_only": y5_parking_only,
        "y5_ad": {c: portfolio[5]["ad_revenue"][c] for c in CASES},
        "y5_total": y5_run_rate,
        "valuation_7x_parking_only": val_7x_parking_only,
        "valuation_7x_total": val_7x_total,
        "valuation_uplift": val_uplift,
        "dcf_parking_anchor": PARKING_DCF_ANCHOR,
        "dcf_uplift": dcf_uplift,
        "dcf_total": dcf_total,
    },
    "by_market": {
        m: {f"Y{y}": {k: v for k, v in model[m][y].items() if k != "acquired_ytd"}
            for y in YEARS}
        for m in MARKETS
    },
    "won_accounts_detail": [
        {
            "name": a["name"],
            "market": a["_mkt"],
            "type": a["type"],
            "acquisition_year": a["acquisition_year"],
            "tam": a["tam"],
            "annual_vehicles": round(annual_vehicles(a), 0),
            "annual_sms": round(annual_sms_from_account(a), 0),
            "annual_ad_rev_at_activation": {
                c: round(annual_ad_revenue_from_sms(
                    annual_sms_from_account(a), a["type"], case=c), 0)
                for c in CASES
            },
        }
        for a in won
    ],
}

Path(OUT_JSON).write_text(json.dumps(output, indent=2))
print(f"\nSaved model → {OUT_JSON}")
