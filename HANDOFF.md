# Better Habits — Development Handoff

> **Purpose:** A living summary you (or a fresh Claude session) can read to pick up
> development instantly. Update the "Current state" and "Recent changes" sections
> whenever you make a change. Keep it short and accurate.

---

## Project goal
A private, dependency-light daily habit tracker. Born from a personal goal:
**stop watching screens late at night.** The app pairs with a macOS wind-down
nudge + auto-shutdown to support that goal directly.

## Architecture (keep it simple on purpose)
- **App is one file:** `index.html` contains all HTML, CSS, and JS. No build step,
  no framework, no server.
- **Only dependency:** Chart.js, **vendored locally** at `vendor/chart.umd.min.js`
  (was a CDN link; vendored so it works offline).
- **PWA:** `manifest.json` + `sw.js` (service worker, cache-first app shell) +
  `icons/` + `apple-touch-icon.png`. Service worker only activates over http(s),
  not `file://`. Bump `CACHE` in `sw.js` whenever a cached asset changes.
- **Storage:** browser `localStorage` under key `betterHabits.v1` (per-device).
- **Data shape:**
  ```js
  { habits: [ { id, name, log: { "YYYY-MM-DD": "<ISO timestamp>", ... } } ] }
  ```
  `log` stores the **check-off timestamp** for done days; absence = not done.
  Legacy entries may be the boolean `true` — code treats any truthy value as done,
  and `checkTime()` returns null for `true`.

## Current state (v0.3)
Working features:
- Add / edit / delete habits
- Daily check-off + date navigation (‹ ›); records check-off time per day
- Per-habit streaks (🔥) and a global best-streak stat
- Per-habit expandable 28-day history grid (click to toggle; tooltip shows time)
- Stats card: today %, best streak, last-30-days %, **avg check-in time**, 30-day chart
- Export / Import JSON backup
- Installable PWA (offline-capable) — see `DEPLOY.md` for hosting
- macOS nudge system in `nudge/` (10:15pm notification)

## Recent changes
- v0.3: timestamp check-offs + avg check-in stat; PWA (manifest/SW/icons);
  vendored Chart.js; phone install + deploy docs
- v0.2: editable names, per-habit history grid, export/import, docs, nudge system
- v0.1: initial MVP

## How to test
1. `open index.html`
2. Add a couple of habits, check them off, use ‹ › to backfill yesterday.
3. Expand a habit (▾) and click grid squares.
4. Export, then Import the file back — data should round-trip.

## Backlog / ideas (not yet built)
- Cross-device sync (data is currently per-device; only Export/Import bridges them)
- A "time of day" chart using the new check-off timestamps
- Weekly/monthly goals (e.g. "5 of 7 days") instead of daily-only
- Reorder habits (drag and drop)
- Per-habit color tags
- Notes per day
- Reminder times configurable inside the app

## Conventions
- Keep `index.html` self-contained; avoid adding build tooling unless necessary.
- Bump the version in `README.md` Changelog **and** here on every meaningful change.
- Update this file's "Current state" + "Recent changes" each session.
