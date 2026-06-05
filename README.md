# 🌱 Better Habits

A simple, private daily habit tracker. Open `index.html` in any browser — no
install, no account, no server. Your data stays on your machine.

👉 **New here?** Read [`TUTORIAL.md`](./TUTORIAL.md) for a feature walkthrough.

## Features
- **Cross-device sync** — link your phone & laptop with a private sync code
- One-tap daily check-off for each habit
- Streak counters (🔥) per habit
- Move between days to backfill or review history
- Editable habit names
- Per-habit 28-day history grid (click to backfill)
- Records the **time** you check off each habit (daily timing data)
- Stats: today %, best streak, last-30-days %, avg check-in time, 30-day chart
- Export / Import backup (your data lives in browser localStorage)
- **Installable on your phone** (PWA, works offline) — see `DEPLOY.md`
- Optional macOS "wind-down" nudge + auto-shutdown (see `nudge/`)

## Project layout
```
index.html      The app (HTML + CSS + JS, single file)
manifest.json   PWA manifest (installable app metadata)
sw.js           Service worker (offline app-shell cache)
vendor/         Vendored Chart.js (local copy, for offline)
icons/          App icons
TUTORIAL.md     Feature walkthrough for users
DEPLOY.md       How to host it + install on your phone
HANDOFF.md      Reusable summary for continuing development
nudge/          macOS wind-down notification system
```

## Running it
Double-click `index.html`, or:
```
open index.html
```
> Note: the offline/installable features need the site served over http(s)
> (see `DEPLOY.md`). Opening the file directly still works for normal use.

---

## Changelog
All notable changes are tracked here, newest first.

### v0.4 — 2026-06-05
- **Added** cross-device sync via Supabase — set the same **sync code** on each
  device and your habits stay in sync (near-live: polls while open + pulls on
  focus). Edits merge safely: check-offs union, deletes/unchecks use timestamped
  tombstones, latest rename wins. Works offline; localStorage stays the cache.
- **Added** "⇅ Sync" button in the footer (shows status: off / syncing / synced)

### v0.3 — 2026-06-05
- **Added** check-off timestamps — each completion records the time of day
- **Added** "Avg check-in" stat and check-in times in the history grid tooltip
- **Added** PWA support: `manifest.json`, service worker (`sw.js`), app icons —
  installable on phone, works offline
- **Added** `DEPLOY.md` (hosting + phone install steps)
- **Changed** Chart.js from a CDN link to a vendored local copy (`vendor/`)

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
