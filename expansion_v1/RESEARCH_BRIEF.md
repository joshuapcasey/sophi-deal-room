# Sophi Mobility — New Market Inventory Research Brief

## Goal
Catalogue every account in the **CBD + inner-ring valet-relevant** zone of the assigned market. The inventory feeds Sophi's TAM/SAM/SOM model. Mirror the schema and conventions used in the existing 6 markets (Charlotte, Indianapolis, Denver, Phoenix, Cleveland, Louisville).

## Account Universe (comprehensive)
Catalogue ALL of the following that could conceivably support a paid valet or paid self-park operation:

1. **Hotels** — full-service, lifestyle, boutique, upper-upscale, luxury, AND select-service in CBD/airport/event-district zones (Marriott CY/Residence Inn, Hilton GI/HGI, Hyatt Place/House, AC). Include conference center hotels.
2. **Restaurants** — fine-dining, upscale-casual, steakhouses, chef-driven independents, hotel restaurants where notable. Skip QSR, fast casual, neighborhood spots without valet.
3. **Entertainment / event venues** — concert venues, theaters, sports arenas/stadiums, performing-arts centers, casino-resorts, museums with valet, large event spaces.
4. **Hospitals** — major medical centers in or near the CBD with patient/visitor parking demand.

Aim for **60–120 accounts per market**. Quality > quantity — every account must be real, currently operating (as of May 2026), and have a plausible valet/paid-parking economic profile.

## Required Per-Account Fields (mirror Charlotte v3 schema)

| Field | Source | Notes |
|---|---|---|
| name | venue website / Google | exact display name |
| type | classified | one of: Hotel · Restaurant · Venue · Hospital |
| address | Google Maps | street, city, state, zip |
| url | venue website | primary site |
| rooms | hotel website / brand directory | hotels only — # of guest rooms |
| seats | restaurant site / OpenTable | restaurants only — interior seats (not patio) |
| beds | hospital website | hospitals only — staffed beds |
| capacity | venue site | venues only — concert/event capacity |
| self_park_rate | venue/garage page or Spothero | $/day, integer dollars; "n/a" if unknown |
| valet_rate | venue/garage page | $/day, integer; "n/a" if unknown |
| occupancy | STR / hotel data | hotels only — annual occupancy rate as decimal (default 0.60 if unknown) |
| turnover | restaurant standard | restaurants only — daily seat turnover (default 1.5 if unknown) |
| valet_conv | brand standard | hotels: default 0.40 (downtown), 0.30 (select-service); restaurants: default 0.125 |
| op_days | venue type default | 365 hotel/restaurant; venue/hospital varies |
| peak_mod | venue type default | 1.0 unless seasonal swing material |
| valet_operator | review of valet contract / property pages | known national operators: Towne Park, LAZ, SP+, Propark, Park Inc, Epic Valet, Elite Mgmt, USA Parking. Otherwise "Independent" or unknown |
| garage_operator | parking-garage signage / city DOT | same operator dictionary |
| management | hotel: management co (Marriott managed, Aimbridge, White Lodging, etc); restaurant: parent company (Darden, ONE Group, etc) |
| ownership_group | parent owner / REIT / family office | used for v3 group multiplier — same group_key across sister properties in same market |
| gm | LinkedIn / hotel directory | best-effort, leave blank if not findable |
| email | LinkedIn / public site | best-effort |
| phone | venue contact page | best-effort |
| location_notes | observation | "downtown convention", "event-district", "near hospital corridor", "patio-heavy", etc |
| sourcing_notes | research log | which URL or data point you used |

## Defaults Cookbook (Charlotte v3 conventions)
Use these when source data is silent. Mark them as defaults in `sourcing_notes`.

**Hotels:**
- Downtown / convention center, 200+ rooms: occupancy 0.60, valet_conv 0.40, valet_rate $40–55, op_days 365
- Lifestyle / boutique, 100–200 rooms: occupancy 0.65, valet_conv 0.45, valet_rate $35–50
- Select-service downtown, <200 rooms: occupancy 0.55, valet_conv 0.30, valet_rate $25–35
- Resort / convention / event-heavy: peak_mod 1.10–1.15

**Restaurants:**
- Fine-dining steakhouse: seats 250 if unknown, turnover 1.5, valet_conv 0.125, valet_rate $15–20 (city-dependent)
- Upscale-casual: seats 200, turnover 1.75, valet_conv 0.10
- Chef-driven independent: seats 100–150, turnover 1.5, valet_conv 0.125

**Venues:**
- Stadium/arena: capacity, op_days = event count (~100–150 NBA/NHL, ~80 MLB, ~10 NFL, +concerts)
- Theater / PAC: capacity, op_days = show count, peak_mod higher
- Casino: 365 days, valet_conv much higher (~0.55), valet_rate often $0 (comp'd)

**Hospitals:**
- Major medical center: visitor cars/day from beds × visitor multiplier; valet_rate often $0–10 (validated)

## Operator Dictionary (use exact strings)
- `towne park`, `laz`, `sp_plus`, `propark`, `park_inc`, `epic_valet`, `elite_mgmt`, `usa_parking`, `pmc`, `ace_parking`, `lanier`, `republic_parking`
- `independent` (single-site or local operator)
- `sophi` (only if the property is a Sophi anchor)
- leave blank if genuinely unknown

## Output Format

Save to `/home/user/workspace/sophi-market-map/expansion_v1/raw/<market_key>_inventory.csv` with EXACTLY these column headers in this order:

```
name,type,address,url,rooms,seats,beds,capacity,self_park_rate,valet_rate,occupancy,turnover,valet_conv,op_days,peak_mod,valet_operator,garage_operator,management,ownership_group,gm,email,phone,location_notes,sourcing_notes
```

One row per account. Empty cells where N/A. No commas inside cells unless quoted.

Also write `/home/user/workspace/sophi-market-map/expansion_v1/memos/<market_key>_memo.md` (1 page, ≤500 words) covering:
- Market overview: CBD geography, demand drivers, hospitality density
- Operator landscape: which national operators dominate, which independents
- Top 5 highest-priority accounts (anchor candidates)
- Notable risks: operator gates, ownership concentration, seasonality
- 3–5 sources used (URLs)

## Quality Bar
- Every hotel must have rooms+address+management identified
- Every restaurant must have seats (or sourced default)+address
- Every hospital must have beds+address
- Every venue must have capacity+address
- Operator/ownership left blank only if you genuinely cannot find it after a reasonable search
- Defaults are FINE but must be flagged in sourcing_notes
