# Session Handoff — 2026-04-19

## What was completed this session

- Created `KNOWLEDGE_BASE.md` at repo root (was missing)
- Added OBJ-04 + REQ-15..18 (compliance/permit requirements)
- Drafted `content/08_permits.md` (Finnish space law, FICORA/ITU, disposal, testing, export)
- Corrected payload classification (navigation system = bus, not payload)
- Lowered orbit: 750 km → 500 km SSO, inclination 97.4°
- Relaxed REQ-03: swath ≥ 200 km → ≥ 150 km
- Relaxed REQ-04: revisit ≤ 5 days → ≤ 14 days (physics: ~10–11 days at 500 km / 150 km swath)
- Relaxed REQ-05: geolocation ≤ 2 km → ≤ 10 km (consistent with 1° pointing)
- Fixed REQ-02: CO ppb mixing ratio → CO total column ≥ 50% above baseline
- Relaxed OBS-03: 0.1 nm FWHM → ≤ 10 nm FWHM (COTS achievable); CO = secondary best-effort
- Fixed SMART violations: OBS-01 ("UV spectrometer" → "ozone measurement channel"), OBS-03 ("SWIR spectrometer" → "CO detection channel"), REQ-07 (envelope dimensions, no standard name)
- Drafted `content/09_ai_usage.md`
- All changes verified by agent — build clean, 18 tests pass

## Open items — Concept Review (due 2026-04-23)

### MUST DO (graded)
1. **RTM in SoW 4-column format** — `rtm_generator.py` needs rewrite
   - Current output: 3 columns (Req ID | Text | Parent Objective)
   - Required: Objectives & Drivers | Requirements | Observation Reqs | Instrument Reqs
   - Must go into `content/02_requirements.md`

2. **Objectives/requirements flow chart** — 2p grade item
   - Hierarchy diagram: Objectives → Mission Top Reqs → Observation Reqs → Instrument Reqs
   - Can be a Markdown ASCII diagram or described as a table if no image tooling available

3. **`content/02_requirements.md`** — currently placeholder
   - Needs: objectives list, requirements hierarchy, RTM table

4. **`content/03_payload.md`** — currently placeholder, 2p grade item
   - Payload trade-off table: UV channel vs alternatives, SWIR vs alternatives
   - Criteria: mass, power, data rate, performance, 3U compatibility
   - Justify final selection

### Secondary
- REQ-07 borderline SMART (envelope dimensions) — student decision: leave or rephrase
- REQ-13 (downlink ≥ 1 Mbps) — still TBD pending frequency band decision
- Budget CSVs still all zeros — needed for Preliminary Design (May 7), not Concept Review

## Key confirmed decisions
- Mission: AtmoSat-1, 3U CubeSat, SSO 500 km / 97.4°
- Primary: ozone (UV, ≤ 1 nm, DOAS retrieval, ≤ 5 DU accuracy)
- Secondary: CO (SWIR, ≤ 10 nm broadband, ≥ 50% column enhancement detection)
- Ground station: Aalto
- Passive 25-year deorbit satisfied at 500 km (~7–12 year natural decay)
- RF licence: TBD (X-band placeholder in mission_config.yaml — inconsistent with UHF if chosen)

## SoW RTM format (from vault PDF p.12)
4 columns, one row per instrument requirement flowing left to right:
| Objectives and Drivers | Requirements | Observation Requirements | Instrument requirements |
