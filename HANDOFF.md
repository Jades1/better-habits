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
- **Storage:** browser `localStorage` under key `betterHabits.v1`. With sync on,
  the same data also lives in one Supabase row (see "Cross-device sync" below);
  localStorage stays the offline cache + source for the UI.
- **Data shape:**
  ```js
  {
    habits: [ { id, name, created, nameTs, log: { "YYYY-MM-DD": "<ISO ts>", ... } } ],
    tombstones: {
      habits: { "<habitId>": <deletion ms> },        // deleted habits
      logs:   { "<habitId>|YYYY-MM-DD": <uncheck ms> } // un-checked days
    }
  }
  ```
  `log` stores the **check-off timestamp** for done days; absence = not done.
  Legacy entries may be the boolean `true` — code treats any truthy value as done,
  and `checkTime()` returns null for `true`. `created` gives a stable cross-device
  sort order; `nameTs` resolves rename conflicts. `normalize()` upgrades old data.

## Cross-device sync (v0.4)
- **Backend:** a single Supabase table `sync_state(code text pk, data jsonb,
  updated_at)`, RLS policy allows anon full access (the **sync code** is the
  secret). `SB_URL`/`SB_KEY` (anon key — safe to ship) are constants in `index.html`.
- **Transport:** plain `fetch` to Supabase REST (no SDK, keeps the single-file
  build). Near-live via 8s polling **while the tab is visible** + pull on
  focus/visibility. Realtime is enabled on the table but unused for now.
- **Merge:** `mergeState(a,b)` is commutative + idempotent → no ping-pong.
  Check-offs union (earliest real timestamp wins over legacy `true`); habit
  deletes and per-day unchecks are timestamped tombstones (uncheck loses to a
  later re-check); latest `nameTs` wins for renames. `canon()` (deterministic,
  key-sorted, habits ordered by `created`→`id`) is used to detect real changes
  and decide when to push. `reconcile()` adopts merged state, then pushes back
  only if the remote is missing data we hold.
- **UI:** footer "⇅ Sync" button → `prompt()` for the code (blank = off);
  per-device code stored under `betterHabits.syncCode`. Different codes = fully
  separate data (handy for sharing the app with a tester).

## Current state (v0.4)
Working features:
- Add / edit / delete habits
- Daily check-off + date navigation (‹ ›); records check-off time per day
- Per-habit streaks (🔥) and a global best-streak stat
- Per-habit expandable 28-day history grid (click to toggle; tooltip shows time)
- Stats card: today %, best streak, last-30-days %, **avg check-in time**, 30-day chart
- **Cross-device sync** via a private sync code (see "Cross-device sync" above)
- Export / Import JSON backup
- Installable PWA (offline-capable) — see `DEPLOY.md` for hosting
- macOS nudge system in `nudge/` (10:15pm notification)

## Recent changes
- v0.4: cross-device sync (Supabase REST + merge/tombstones), footer sync button
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
