# Design Log

Running log of team decisions and mission design choices.
**Append only** — never edit or delete past entries.
Claude reads this at the start of every session. Entries marked `Status: Pending` are work to pick up.

---

## Entry format

```
## YYYY-MM-DD — <topic>
**Decision:** <what was decided>
**Participants:** <who was involved>
**Context:** <why, what alternatives were considered>
**Action for AI:** <what Claude should do with this>
**Status:** Pending / Done
```

---

## 2026-03-21 — Repository and toolchain setup

**Decision:** Use Markdown + Pandoc + Claude Code as the authoring workflow. One student acts as driver per session, briefs Claude, reviews output. Others review async via git.
**Participants:** Simon
**Context:** Team has no time for meetings. This workflow lets any teammate pick up where the last session left off without synchronous coordination.
**Action for AI:** Read this log at the start of every session. All Pending entries are actionable items.
**Status:** Done

---

## 2026-03-23 — Mission concept decision

**Decision:** 3U CubeSat, Sun-Synchronous Orbit, UV + SWIR sensors for ozone and CO monitoring over conflict regions (European resilience angle).
**Participants:** Simon, Alissa, Maiju
**Context:** Team discussed via chat. Climate/environmental monitoring selected as theme. Mission framing: studying how armed conflict (e.g., Ukraine) affects atmospheric chemistry (ozone depletion, CO pollution) compared to baseline regions (e.g., Finland). SSO chosen for repeatable local solar time coverage enabling consistent multi-region comparisons. Polar orbit allows Earth rotation coverage.
**Status:** Done

## 2026-03-23 — Satellite form factor

**Decision:** 3U CubeSat.
**Participants:** Simon
**Context:** Compact sensor suite (UV + SWIR + optional camera) fits 3U form factor. TRL and mass constraints support this class.
**Status:** Done

## 2026-03-23 — Orbit selection

**Decision:** Sun-Synchronous Orbit (SSO), inclination ~98°, altitude 700–850 km (working value: 750 km pending lock-in).
**Participants:** Simon, Maiju
**Context:** Maiju confirmed 700–850 km is typical for ozone monitoring satellites. SSO at ~98° gives consistent local solar time for repeatable UV measurements. Simon noted need to account for solar angle in multi-site comparisons. Exact altitude not locked — needs team confirmation.
**Action for AI:** Flag altitude as TBD until team confirms. Use 750 km as working value in mission_config.yaml.
**Status:** Done

## 2026-03-23 — Payload selection

**Decision:** Primary: UV spectrometer (ozone column), SWIR spectrometer (CO). Secondary/nice-to-have: visible/NIR camera (albedo).
**Participants:** Simon, Alissa, Maiju
**Context:** UV sensor measures ozone (reflected UV / Dobson units). SWIR spectrometer detects CO absorption lines (CO is highly localized — useful for conflict region attribution). Camera for albedo. Simon noted IR also possible. Payload combination gives ozone + CO + albedo in a single 3U platform.
**Status:** Done

## 2026-03-23 — Mission motivation framing

**Decision:** Mission studies environmental impact of conflict on atmospheric chemistry (ozone + CO) in Europe. Framed under "European Resilience and Societal Security" course theme.
**Participants:** Simon, Alissa, Maiju
**Context:** Alissa proposed comparing ozone above Finland vs Ukraine. Simon extended to CO via spectrometry. Provides actionable environmental data in regions where ground infrastructure may be damaged or unavailable.
**Status:** Done

---

## 2026-04-19 — Payload classification correction

**Decision:** Navigation system (star trackers, gyroscopes, GPS receivers) is spacecraft BUS, not payload. Correcting earlier team conversation that listed it as payload.
**Participants:** Simon (session), AI flagged per course slide
**Context:** Course slide "Correct classification" states: Payload = sensors/scientific instruments + mission communication equipment (transponders, user data antennas). Navigation system = bus (used to control and operate spacecraft, not achieve mission goal). AtmoSat-1 payload remains: UV spectrometer, SWIR spectrometer, visible/NIR camera (secondary). Communication unit (downlink transponder/antenna) is also payload.
**Action for AI:** Do not list navigation system under payload in any section. ADCS subsystem covers attitude sensors (star tracker, gyro, GPS) as bus.
**Status:** Done

---

## 2026-04-19 — Finnish satellite operation licence

**Decision:** AtmoSat-1 requires Finnish satellite operation authorisation as it is operated from Finland.
**Participants:** Simon (session), course slide source
**Context:** The Act on Space Activities (Finland) entered into force 23 January 2018. Every Finnish satellite needs "Authorisation for space activities" granted by the Ministry of Economic Affairs and Employment (tem.fi/en/spacelaw). This is a legal compliance requirement.
**Action for AI:** Add to requirements.yaml as compliance requirement. Draft content/08_permits.md with this information.
**Status:** Done

---

## 2026-04-19 — Radio frequency licence

**Decision:** RF frequency licence required via FICORA (Finnish Communications Regulatory Authority / Viestintävirasto), coordinated with ITU.
**Participants:** Simon (session), course slide source
**Context:** In Finland, frequency coordination handled by FICORA. Radio amateur licences applied from national Radio Amateur Organization, which coordinates with ITU. Exact frequency band for AtmoSat-1 not yet selected (X-band placeholder in mission_config.yaml may not be realistic for a student CubeSat — UHF amateur band is more typical). Frequency selection drives licence process.
**Action for AI:** Flag X-band placeholder as potentially inconsistent with CubeSat capability. Add RF licence requirement to requirements.yaml. Include FICORA/ITU process in content/08_permits.md.
**Status:** Done

---

## 2026-04-19 — Testing requirements

**Decision:** Vibration test report is required for every satellite launched. Additional tests required per product assurance plan.
**Participants:** Simon (session), course slide source
**Context:** Course slide confirms vibration test is mandatory for launch. Standard CubeSat test campaign also includes thermal vacuum (TV), EMC, and radiation tests. Testing requirements apply at the altitude target (~700–750 km). These tests belong in Section 6 (Product Assurance) and should have corresponding requirements in requirements.yaml.
**Action for AI:** Add testing compliance requirements to requirements.yaml. Ensure Section 6 placeholder references vibration, TV, EMC, radiation tests.
**Status:** Done

---

## 2026-04-19 — Orbit altitude change: 750 km → 500 km

**Decision:** Operational orbit altitude lowered from 750 km to 500 km SSO. Inclination updated to 97.4°.
**Participants:** Simon (session)
**Context:** 750 km failed the ESA 25-year passive de-orbit rule (decay ~50–150 years). 500 km gives natural decay in 7–12 years, satisfying the rule without propulsion or drag sail. Aalto-1 reference mission used 505 km for the same reason. Trade-offs: swath shrinks proportionally (REQ-03 relaxed to ≥ 150 km), radiation dose slightly lower (better), more ground station passes per day (better).
**Action for AI:** Update mission_config.yaml, requirements.yaml (OBJ-02, REQ-03, REQ-05, REQ-11, REQ-18), content/01_motivation.md (all altitude references), KNOWLEDGE_BASE.md.
**Status:** Done

---

## 2026-04-19 — REQ-04 revisit relaxed to ≤ 14 days

**Decision:** Revisit period requirement relaxed from ≤ 5 days to ≤ 14 days at 50° N.
**Participants:** Simon (session)
**Context:** At 500 km SSO with 150 km swath, estimated revisit is ~10–11 days — physically unachievable at 5 days without a ~350 km swath or cross-track pointing. 14-day threshold is scientifically justified: CO atmospheric lifetime ~1–2 months; mission goal is seasonal trend attribution over conflict vs reference regions, not event-triggered response. 14 days gives comfortable margin over the ~10–11 day physics estimate.
**Status:** Done

---

## 2026-04-19 — CO measurement reframed as secondary best-effort objective

**Decision:** CO measurement kept but relaxed from precision retrieval to broadband best-effort detection. OBS-03 resolution relaxed from ≤ 0.1 nm to ≤ 10 nm FWHM. REQ-02 unit corrected from ppb mixing ratio to total column percentage enhancement.
**Participants:** Simon (session)
**Context:** 0.1 nm FWHM SWIR requires resolving power ~23,000 — unachievable in 3U form factor (COTS SWIR spectrometers achieve 5–20 nm). Reframed as broadband band-depth detection: detects CO column enhancements ≥ 50% above baseline (large fires, industrial events), not line-resolved retrieval. Ozone (UV, ≤ 1 nm) remains the primary precise measurement. CO is secondary/exploratory.
**Status:** Done

---

## 2026-04-19 — Requirements SMART compliance check

**Decision:** Existing requirements in requirements.yaml flagged for potential SMART violations — student team must review before Concept Review submission.
**Participants:** AI flagged per course slide
**Context:** Course slide states requirements shall be SMART (Specific, Measurable, Achievable, Relevant, Timely), quantitative and verifiable, traceable, one sentence, no clarification text in requirement, must not suggest solutions. Flags on current draft:
  1. OBS-01/OBS-03 say "UV spectrometer" / "SWIR spectrometer" — names the solution. Should say "the primary instrument" or "the ozone measurement channel".
  2. REQ-07 says "comply with the 3U CubeSat standard" — solution-prescriptive. Consider separating mass (≤4 kg) from envelope (≤10×10×30 cm).
  3. REQ-13 "Downlink rate ≥ 1 Mbps" — verify achievability against selected frequency band (1 Mbps is feasible on X-band but not UHF amateur band at ~9.6 kbps max). INCONSISTENCY RISK if frequency shifts from X-band to UHF.
**Action for AI:** Do not change requirement wording without student confirmation. These are flagged for student review.
**Status:** Pending — student review required
