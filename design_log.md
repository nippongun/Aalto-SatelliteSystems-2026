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
