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
    reminders: [ { id, message, type:"interval"|"time", intervalMin, time:"HH:MM",
                   enabled, created, updatedTs } ],   // gentle nudges (v0.6)
    counters: [ { id:"c1".."c3", label, color, history:{ "YYYY-MM-DD": count },
                  updatedTs } ],                       // 3 daily tap counters (v0.7)
    tombstones: {
      habits:    { "<habitId>": <deletion ms> },          // deleted habits
      logs:      { "<habitId>|YYYY-MM-DD": <uncheck ms> }, // un-checked days
      reminders: { "<reminderId>": <deletion ms> }         // deleted reminders
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

## Current state (v0.7)
Working features:
- Add / edit / delete habits
- Daily check-off + date navigation (‹ ›); records check-off time per day
- Per-habit streaks (🔥) and a global best-streak stat
- Per-habit expandable 28-day history grid (click to toggle; tooltip shows time)
- Stats card: today %, best streak, last-30-days %, **avg check-in time**, 30-day chart
- **Cross-device sync** via a private sync code (see "Cross-device sync" above)
- **Reminders** — interval or time-of-day nudges with custom messages; in-app
  banner + WebAudio chime + optional system notifications; tap to toggle,
  press-and-hold to edit; synced (v0.6)
- **Counters** — three customizable tap buttons (color + label); tally resets
  daily and each day's total is tracked; tap to count, press-and-hold to edit /
  view last 7 days; synced (v0.7)
- **Shut down this Mac from the app** + nightly auto-shutdown (see "Wind-down" below)
- Export / Import JSON backup
- Installable PWA (offline-capable) — see `DEPLOY.md` for hosting
- macOS nudge system in `nudge/` (10:15pm notification)

## Reminders (v0.6)
- **Model:** `state.reminders[]` (see data shape). Two kinds: `type:"interval"`
  (fires every `intervalMin`) and `type:"time"` (fires daily at `time` "HH:MM").
  `updatedTs` resolves edit conflicts; deletes are tombstoned in
  `tombstones.reminders`. Merged in `mergeState()` like habits (union by id,
  later `updatedTs` wins the whole object, tombstone drops it); ordered by
  `created`→`id` in `orderReminders()` and included in `canon()`.
- **Firing is device-local, NOT synced:** runtime lives in localStorage key
  `betterHabits.reminderRuntime` ({id → {nextFire} | {lastDate}}), so one device
  chiming doesn't suppress another and constantly-changing timestamps don't cause
  sync ping-pong. `reminderTick()` runs every 15s (+ on focus/visibility): interval
  reminders fire when `now ≥ nextFire` then re-arm `now + interval` (no burst
  catch-up); time reminders fire once/day only within 5 min after the target
  (avoids a stale fire when you open the app hours later).
- **Alert:** in-app banner (`#reminderToast`, auto-hides after 12s) + a soft
  two-note WebAudio chime (no audio asset). Audio is unlocked on first
  `pointerdown` (browser gesture requirement, esp. iOS).
- **System notifications (optional layer):** `systemNotify()` raises an OS
  notification via `serviceWorker.ready.showNotification()` (falls back to
  `new Notification`). Fired from `fireReminder()` **only when**
  `document.visibilityState !== "visible"` (foreground already has banner+chime,
  so no double alert). Permission is opt-in via the `#notifyRow` "Enable
  notifications" button (`renderNotifyRow()` reflects granted/denied/default/
  unsupported); permission is per-device, not synced. `sw.js` has a
  `notificationclick` handler that focuses an existing window or opens one.
  Time-of-day reminders are sticky (`requireInteraction:true` + unique tag so
  they aren't replaced); interval ones auto-dismiss (shared tag, would pile up).
  Known limitation (documented for the user): nothing fires when the app is
  *fully closed* (no Web Push backend); background desktop tabs still tick
  (throttled ~1/min) and notify. On iOS, notifications need the PWA installed
  to the Home Screen + permission.
- **UI:** `#remindersCard`; rows render in `renderReminders()` (called from
  `render()` so sync updates redraw them). **Tap** a row = toggle enabled;
  **press & hold** (550ms, movement >10px cancels) = open the editor modal
  (`#remEditOverlay`). `×` deletes. Editor handles new + edit, interval-vs-time
  segmented control, minutes/hours unit.

## Counters (v0.7)
- **Model:** `state.counters[]` is a **fixed set of three** buttons with stable
  ids `c1`–`c3` (no add/delete — `normalizeCounters()` always coerces to exactly
  three, in order, and migrates the brief earlier `count`/`countDate` shape into
  `history`). Each has `label`, `color`, `updatedTs`, and `history` =
  `{ "YYYY-MM-DD": presses }`.
- **Daily reset + tracking:** the number shown is `counterToday(c)` =
  `history[today]` (so it reads 0 on a new day). `bumpCounter()` does
  `history[today]++` — every day's total persists as history. If the app is left
  open across midnight, `reminderTick()` (15s) notices `today !== counterDay` and
  re-renders so the tallies reset on screen.
- **Merge:** in `mergeState()`, per counter id the `history` maps **union with
  per-day max** (a tally survives across devices), while `label`/`color` take the
  later `updatedTs`; `updatedTs` = max. Commutative + idempotent (verified).
  Included in `canon()`. No tombstones (fixed set). Caveat: because history is
  max-union, "Reset today" can be undone by another device still holding a higher
  count for today — fine for single-user use.
- **UI:** `#countersCard` → `#counterRow` (three `.counter` `<button>`s, colored
  background, count + label superimposed; empty label shows "Hold to set").
  **Tap** = +1 (updates just that button's number, no full re-render/chart redraw
  via `save()` + direct DOM write); **press & hold** (550ms, >10px cancels) opens
  `#counterEditOverlay` to set label, pick a color from `COUNTER_COLORS` swatches,
  see the **last 7 days** (`renderCounterHistory()`), and **Reset today**.

## Wind-down: shut down the Mac from the app (v0.5)
- **Why a helper:** a browser tab can't power off a computer (sandbox), so the
  "Wind-down · this Mac" card talks to a tiny local helper over `http://127.0.0.1:7421`.
- **Helper:** `helper/habits-helper.py` (Python stdlib only). Endpoints:
  `GET /status`, `POST /shutdown` (`?dry=1` = token check), `POST /schedule`
  `{hour,minute}`, `POST /unschedule`. Shutdown is graceful (`osascript` →
  System Events), so **no sudo**. Scheduling writes a per-user launch agent
  `com.betterhabits.autoshutdown` (also sudo-free). The helper ALSO serves the
  app's static files, so `http://localhost:7421` gives the full app + controls.
- **Security (3 layers):** binds to `127.0.0.1` only; `/shutdown`+`/schedule`
  require the `X-Habits-Token` secret (in `~/.better-habits-helper-token`);
  CORS allowlist + Origin check (custom header forces a preflight we reject for
  unknown origins). Verified: wrong token → 401, `evil.com` preflight blocked.
- **Install location matters:** installed to `~/Library/Application Support/BetterHabits`,
  NOT `~/Documents` — macOS TCC blocks launchd processes from reading `~/Documents`
  ("Operation not permitted"). `helper/install.sh` copies the helper + web assets
  there and loads `helper/com.betterhabits.helper.plist` (RunAtLoad + KeepAlive).
  Re-run `install.sh` after changing the app to refresh the local served copy.
- **App side (index.html):** `HELPER_URL` = same-origin when served on :7421, else
  `http://127.0.0.1:7421`. Card auto-shows only when the helper is reachable (so
  phones don't see a dead card). Token paired via a `prompt()`, stored under
  `betterHabits.helper` (device-local, NOT synced). Token is verified with a
  `/shutdown?dry=1` call. Mixed-content note: an HTTPS page (github.io) calling
  `http://127.0.0.1` works in Chrome (localhost is "potentially trustworthy"); if
  a browser blocks it, open `http://localhost:7421` (served by the helper) instead.

## Recent changes
- v0.7: Counters (3 customizable tap buttons, daily reset + per-day history, synced)
- v0.6: Reminders (interval / time-of-day nudges, in-app banner + chime, synced)
- v0.5: shut-down-from-app via local helper (`helper/`), Wind-down card
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

## Conventions
- Keep `index.html` self-contained; avoid adding build tooling unless necessary.
- Bump the version in `README.md` Changelog **and** here on every meaningful change.
- Update this file's "Current state" + "Recent changes" each session.
