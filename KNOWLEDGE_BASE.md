# Aalto Satellite Systems 2026 — Knowledge Base

**Course:** ELEC-E4240 Satellite Systems, Aalto University School of Electrical Engineering
**Mission Theme:** *Small Satellite Missions for European Resilience and Societal Security*
**Last updated:** 2026-04-19

> **Source of truth hierarchy:** `mission_config.yaml` owns all mission parameters. `requirements/requirements.yaml` owns all requirements. This file is a navigational reference — never copy numbers here that live in those files.

---

## 1. Project Overview

Team project producing a **Mission Feasibility Study** for a small satellite. Design-only — no hardware built. AI tools allowed and encouraged; usage must be documented.

**Mission:** AtmoSat-1 — 3U CubeSat measuring ozone column and CO total column over European conflict and reference regions from Sun-Synchronous Orbit.

**Team:** Maiju Alavuotunki · Alissa Lebedeva · Simon Bauer
**Key stakeholders:** Jaan Praks (course lead), Marius, Tomas, Ville, Nemanja, Anton, Maria

---

## 2. Schedule & Deadlines

| Date | Event | Deliverable | Status |
|------|-------|-------------|--------|
| Mar 19 | Workshop: Communications | — | Done |
| **Mar 26** | Workshop: Attitude | **Idea Review** (HW2, 10p) | Done |
| **Mar 30** | OBDH & Software lecture | HW3 due | — |
| **Apr 23** | Workshop | **Concept Review** (HW4, 20p) | Upcoming |
| **May 7** | Workshop | **Preliminary Design** (HW6) | — |
| **May 21** | Workshop + Lab visit | **Detailed Design** (HW7, 13p) | — |
| **May 28** | Workshop | Critical Design Review | — |
| **Jun 1–4** | Student presentations | **Live Presentation** (90p) | — |

---

## 3. Concept Review — Grading Criteria (HW4, 20p)

Total 20p (includes Idea Review points):

| Points | Criterion |
|--------|-----------|
| 2p | Report graphical outline: file name, cover page, removed instructions, chapter outline, figures and references organized |
| 4p | Objectives and requirements (science, mission, instrument) finalized; mission success criteria |
| 2p | Payload selection |
| 2p | Objectives and requirements matrix or flowchart (RTM) |

**Key goal:** Nail down objectives, requirements, payload trade-off so mission technical concept and budget calculations can proceed toward PDR.

---

## 4. Deliverables

1. Mission Feasibility Study PDF — submitted to MyCourses at each milestone
2. Online living document — primary version reviewed by instructors (Google Docs)
3. Requirement Traceability Matrix — separate document
4. Key Budgets — mass, power, communication/data (separate document)
5. Presentation slides — uploaded individually by each team member
6. Live 20-min presentation — Jun 1 or 4, with Q&A

---

## 5. Mission Parameters (Current Values)

All values sourced from `mission_config.yaml`:

| Parameter | Value | Status |
|-----------|-------|--------|
| Mission name | AtmoSat-1 | Working name — confirm |
| Platform | 3U CubeSat (10×10×30 cm, ≤4 kg) | Confirmed |
| Orbit type | Sun-Synchronous Orbit (SSO) | Confirmed |
| Altitude | 500 km | Confirmed 2026-04-19 (lowered from 750 km for passive 25-year deorbit compliance) |
| Inclination | 97.4° | SSO at 500 km |
| Primary payload | UV spectrometer + SWIR spectrometer | Confirmed |
| Secondary payload | Visible/NIR camera (albedo) | Nice-to-have |
| Downlink band | X-band (8.0 GHz) | Placeholder — to be confirmed |
| TX power | 30 dBm | Placeholder |
| EPS power | 10 W | 3U estimate; to be refined |
| Ground station | Aalto | Confirmed |

---

## 6. Document Status

| Section | File | Status |
|---------|------|--------|
| 1. Mission Motivation & Objectives | `content/01_motivation.md` | AI draft 2026-03-23 — awaiting student review |
| 2. Requirement Analysis | `content/02_requirements.md` | Placeholder |
| 3. Payload Selection | `content/03_payload.md` | Placeholder |
| 4. Mission Design | `content/04_mission_design.md` | Placeholder |
| 5. Spacecraft Design | `content/05_spacecraft_design.md` | Placeholder |
| 6. Product Assurance | `content/06_product_assurance.md` | Placeholder |
| 7. Project Description | `content/07_project_description.md` | Placeholder |
| 8. Permits & Licences | `content/08_permits.md` | AI draft 2026-04-19 — awaiting student review |

---

## 7. Requirements Status

Sourced from `requirements/requirements.yaml` (AI draft 2026-03-23 — **awaiting student confirmation**).

| ID | Short description | Verification | Status |
|----|-------------------|-------------|--------|
| OBJ-01 | Monitor ozone + CO over conflict/reference regions | — | Draft |
| REQ-01 | Detect ozone column change ≥ 5 DU | Analysis | Draft |
| REQ-02 | Detect CO anomaly ≥ 50 ppb | Analysis | Draft |
| REQ-03 | Swath width ≥ 150 km | Analysis | Relaxed 2026-04-19 (was 200 km) |
| REQ-04 | Revisit period ≤ 14 days at 50° N | Analysis | Relaxed 2026-04-19 (was 5 days) — matches ~10–11 day estimate at 500 km / 150 km swath |
| REQ-05 | Geolocation accuracy ≤ 10 km (1σ) | Test | Relaxed 2026-04-19 (was 2 km) |
| REQ-06 | Radiometric calibration ≤ 3% absolute | Test | Draft |
| OBJ-02 | 3U CubeSat platform, SSO 500 km | — | Draft |
| REQ-07 | 3U standard, mass ≤ 4 kg | Inspection | Draft |
| REQ-08 | Operational lifetime ≥ 90 days | Demonstration | Draft |
| REQ-09 | Payload power ≥ 3 W (sunlit) | Analysis | Draft |
| REQ-10 | Nadir pointing ≤ 1° (3σ) | Test | Draft |
| REQ-11 | Orbital lifetime after EOM ≤ 25 years | Analysis | Draft |
| OBJ-03 | Science data delivered within 24 h | — | Draft |
| REQ-12 | Downlink within 24 h of acquisition | Demonstration | Draft |
| REQ-13 | Downlink rate ≥ 1 Mbps at 750 km slant | Test | Draft — **FLAG: inconsistent with UHF band** |
| REQ-14 | On-board storage ≥ 24 h of science data | Inspection | Draft |
| OBJ-04 | Comply with legal/regulatory/launch requirements | — | Draft 2026-04-19 |
| REQ-15 | Finnish MoEAE space activities authorisation before launch | Inspection | Draft |
| REQ-16 | Operate only on FICORA/ITU-licensed frequencies | Inspection | Draft |
| REQ-17 | Pass vibration test campaign per launch provider requirements | Test | Draft |
| REQ-18 | ESA debris mitigation: re-entry within 25 years (see also REQ-11) | Analysis | Draft |

---

## 8. Budget Status

All budgets in `budgets/`. Currently stub values — **need population for Concept Review**.

| Budget | File | Status | Warning threshold |
|--------|------|--------|------------------|
| Mass | `budgets/mass_budget.csv` | All zeros (TBD) | System margin < 20% |
| Power | `budgets/power_budget.csv` | All zeros (TBD) | Subsystem margin < 10% |
| Link | `budgets/link_budget.csv` | TBD | Link margin < 3 dB |
| Cost | `budgets/cost_estimate.csv` | TBD | Flag if implausible |

---

## 9. Feasibility Study Document Structure (SoW)

### 9.1 Mission Motivation and Objectives
- Problem to be solved (why space? why small sat?)
- Mission goal (concise, measurable)
- Product of the mission (data type, delivery)
- Success criteria (minimal / full / extended)
- Target orbit (altitude, inclination, justification)

### 9.2 Requirement Analysis
- Objectives — specific, measurable, numbered
- Mission Top Requirements
- Observation Requirements (resolution, accuracy, frequency — with numbers)
- Instrument Requirements
- Mission Design Requirements
- RTM — columns: Objective → Mission Req → Obs Req → Instrument Req

### 9.3 Payload Selection
- Payload options list
- Trade-off analysis (mass, power, data rate, performance, compatibility)
- Final selection justification

### 9.4 Mission and Spacecraft Design Overview
- Mission environment
- Space segment (number of sats, type, class, orbit)
- Ground segment (operations concept, ground stations)
- Launcher (vehicle selection)
- Concept of Operations (mission phases, data flow, timeline)

### 9.5 Spacecraft Design
- Architecture overview (form factor, standard, payload integration)
- Structure and payload accommodation
- Subsystems: OBC, EPS, COM, ADCS
- System budgets: mass, power, communication/data

### 9.6 Product Assurance Plan
- Testing strategy
- Model philosophy (BB → STM → EQM → FM → FSP)
- Model-test matrix
- Functional, thermal vacuum, vibration tests

### 9.7 Spacecraft Development Project Description
- Development concept (COTS vs custom)
- Project schedule — Gantt chart
- Cost estimate (range: 0.5–10 M€)
- Risk analysis (≥5 risks: likelihood, impact, mitigation)

### 9.8 Permits and Licences
- Satellite operation permit (Finnish legislation)
- Satellite disposal strategy
- Radio frequency licence
- Export/import licences (EAR, ITAR)

---

## 10. Systems Engineering Framework

### Requirements Hierarchy
```
Scientific Theme / Objective
  └─ Scientific Secondary Objectives
       └─ Scientific Requirements
            └─ Observation Requirements
                 └─ Instrument Requirements
                      └─ System Requirements
```

### Requirements Must Be (SMART+)
Traceable, Verifiable (with numbers/units), Unitary, Complete, Consistent, Unambiguous.

### Three Core Budgets
| Budget | Purpose | Margin Practice |
|--------|---------|----------------|
| Mass | Subsystem allocation | System margin 10–20% |
| Power | Peak/nominal/safe modes | Contingency per mode |
| Link | SNR, path loss, Eb/N0 | Link margin ≥3 dB |

---

## 11. Key Spacecraft Subsystems Reference

| Subsystem | Options/Technology | Key Parameters |
|-----------|-------------------|----------------|
| Structure | Frame / Central tube / Monocoque / Truss | Mass, stiffness, envelope |
| Propulsion | Monoprop / Biprop / Solid / Hybrid / Electric | Isp, delta-V, mass |
| EPS | Solar array + battery, RTG | Power W, capacity Wh |
| ADCS | Spin-stabilized / 3-axis | Pointing accuracy deg |
| Thermal | Passive coatings / MLI / heaters / louvers | Temp range °C |
| COM | UHF / S-band / X-band / Ka-band | Data rate, link margin |
| OBC | Processing architecture | MIPS, memory, interfaces |

---

## 12. Tools & Scripts

| Script | Purpose |
|--------|---------|
| `scripts/build_doc.py` | Assembles all `content/*.md` → styled `.docx` via pandoc |
| `scripts/check_consistency.py` | Scans content for contradictions, orphaned requirements |
| `scripts/rtm_generator.py` | Generates RTM table from `requirements/requirements.yaml` |
| `scripts/pre_submit_check.py` | Milestone-aware pre-submission checklist |
| `scripts/link_budget.py` | Link budget calculator |
| `scripts/mass_power_budget.py` | Mass + power budget tool |
| `scripts/orbit_analysis.py` | Orbital analysis (period, contact time, eclipse fraction) |

### Pre-commit checklist
```bash
python scripts/build_doc.py
python -m pytest tests/ -x -q
python scripts/check_consistency.py content/
```

---

## 13. Tools & Resources

| Type | Resource |
|------|----------|
| Mission design | https://app.open-cosmos.com/msd |
| CubeSat standards | https://www.cubesat.org/ |
| Component search | https://satsearch.co/ |
| NASA SST SoA | https://www.nasa.gov/smallsat-institute/sst-soa |
| Orbital mechanics | https://sos-orbital-mechanics.com/ |
| GMAT | https://software.nasa.gov/software/GSC-17177-1 |

---

## 14. AI Usage Policy

All AI tools allowed and recommended. **Required:** dedicated chapter describing usage, validation method, critical analysis.
Key question: *How do you verify that AI-provided information is correct and logical?*

---

## 15. Payload Classification (Important)

Per course slide "Correct classification":

**IS payload:**
- Sensors / scientific instruments (cameras, spectrometers, radar)
- Mission communication equipment (transponders, user data antennas)

**NOT payload (spacecraft bus):**
- Navigation system: star trackers, gyroscopes, GPS receivers — these go under ADCS subsystem

AtmoSat-1 payload: UV spectrometer + SWIR spectrometer + visible/NIR camera (secondary). Downlink transponder/antenna is also payload. Navigation system (ADCS sensors) is bus.

---

## 16. Open Items — Concept Review

- [ ] **STUDENT REVIEW REQUIRED**: Confirm/approve `requirements.yaml` — requirements are team's engineering decision
- [ ] **SMART FLAGS** in requirements (see design_log 2026-04-19): OBS-01/03 name solution instrument; REQ-07 solution-prescriptive; REQ-13 data rate depends on unconfirmed frequency band
- [ ] Review and approve `content/01_motivation.md` (AI draft 2026-03-23)
- [ ] Author `content/02_requirements.md` — RTM required for Concept Review grade (2p)
- [ ] Author `content/03_payload.md` — payload trade-off required for Concept Review grade (2p)
- [ ] Populate `budgets/mass_budget.csv` and `budgets/power_budget.csv` with real estimates
- [ ] **CONFIRM frequency band**: X-band (8 GHz) placeholder may not be realistic for 3U CubeSat. UHF amateur band is simpler to license but limits data rate to ~9.6 kbps — inconsistent with REQ-13 (≥1 Mbps). Team must decide and update mission_config.yaml.
- [x] Orbit altitude confirmed: 500 km SSO, 97.4° inclination (2026-04-19)
- [ ] Confirm mission name (AtmoSat-1 working name)
- [ ] Review `content/08_permits.md` AI draft (2026-04-19)
