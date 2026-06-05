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
- **Single file:** `index.html` contains all HTML, CSS, and JS. No build step,
  no framework, no server.
- **Only dependency:** Chart.js via CDN (for the stats chart).
- **Storage:** browser `localStorage` under key `betterHabits.v1`.
- **Data shape:**
  ```js
  { habits: [ { id, name, log: { "YYYY-MM-DD": true, ... } } ] }
  ```
  `log` only stores done days; absence = not done.

## Current state (v0.2)
Working features:
- Add / edit / delete habits
- Daily check-off + date navigation (‹ ›)
- Per-habit streaks (🔥) and a global best-streak stat
- Per-habit expandable 28-day history grid (click to toggle any day)
- Stats card: today %, best streak, last-30-days %, 30-day bar chart
- Export / Import JSON backup
- macOS nudge system in `nudge/` (10:15pm notification)

## Recent changes
- v0.2: editable names, per-habit history grid, export/import, docs, nudge system
- v0.1: initial MVP

## How to test
1. `open index.html`
2. Add a couple of habits, check them off, use ‹ › to backfill yesterday.
3. Expand a habit (▾) and click grid squares.
4. Export, then Import the file back — data should round-trip.

## Backlog / ideas (not yet built)
- Phone access (host the file, or wrap as a PWA with offline support)
- Weekly/monthly goals (e.g. "5 of 7 days") instead of daily-only
- Reorder habits (drag and drop)
- Per-habit color tags
- Notes per day
- Reminder times configurable inside the app

## Conventions
- Keep `index.html` self-contained; avoid adding build tooling unless necessary.
- Bump the version in `README.md` Changelog **and** here on every meaningful change.
- Update this file's "Current state" + "Recent changes" each session.
