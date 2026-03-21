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
