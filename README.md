# 🌱 Better Habits

A simple, private daily habit tracker. Open `index.html` in any browser — no
install, no account, no server. Your data stays on your machine.

👉 **New here?** Read [`TUTORIAL.md`](./TUTORIAL.md) for a feature walkthrough.

## Features
- One-tap daily check-off for each habit
- Streak counters (🔥) per habit
- Move between days to backfill or review history
- Editable habit names
- Per-habit 28-day history grid (click to backfill)
- Stats: today %, best streak, last-30-days %, and a 30-day chart
- Export / Import backup (your data lives in browser localStorage)
- Optional macOS "wind-down" nudge + auto-shutdown (see `nudge/`)

## Project layout
```
index.html      The entire app (HTML + CSS + JS, single file)
TUTORIAL.md     Feature walkthrough for users
HANDOFF.md      Reusable summary for continuing development
nudge/          macOS wind-down notification system
```

## Running it
Double-click `index.html`, or:
```
open index.html
```

---

## Changelog
All notable changes are tracked here, newest first.

### v0.2 — 2026-06-05
- **Added** editable habit names (✎ button)
- **Added** per-habit 28-day history grid (click squares to toggle days)
- **Added** Export / Import JSON backup
- **Added** `TUTORIAL.md` and `HANDOFF.md`
- **Added** macOS wind-down nudge system in `nudge/`
- **Changed** README into a documented, changelog-tracked file

### v0.1 — 2026-06-05
- Initial MVP: add habits, daily check-off, streaks, date navigation,
  stats (today %, best streak, 30-day %), and a 30-day bar chart
- Data persisted in browser localStorage
