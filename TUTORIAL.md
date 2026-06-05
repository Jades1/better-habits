# Better Habits — Tutorial

A walkthrough of every feature. Open `index.html` in any browser to follow along.

---

## 1. Adding a habit
At the bottom of the **Daily Check-in** card, type a habit into the text box
(e.g. *"Screens off by 10:30"*) and press **Enter** or click **Add**.

Tips for good habits:
- Make them **specific and binary** — something you can clearly mark done/not-done.
- Phrase as the action you *want* ("Screens off by 10:30"), not the one you're avoiding.

## 2. Checking off a habit
Tap the **square box** to the left of a habit to mark it done for the selected day.
- Done habits turn **green with a ✓** and the name gets struck through.
- The **time you checked it off** is recorded and shown as `✓ 10:14 PM` on the row.
- Tap again to undo.

## 3. Streaks 🔥
When you complete a habit on consecutive days, a **🔥 streak counter** appears
showing how many days in a row you've kept it. Miss a day and it resets to 0.

## 4. Moving between days
Use the **‹ › arrows** at the top of the Daily Check-in card to move to a
different day. This lets you **backfill** a day you forgot, or review the past.
You can't go past today.

## 5. Editing a habit's name
Click the **pencil ✎** button on a habit to rename it. Your history is kept.

## 6. Per-habit history grid
Click the **▾ arrow** on a habit to expand a **28-day grid**. Each square is a day:
filled = done, empty = missed. Click any square to toggle that day directly —
a fast way to backfill a week at once. **Hover a square** to see the date and the
time you checked it off that day.

## 7. Stats
The **Stats** card shows:
- **Today done** — % of your habits completed today.
- **Best streak** — your longest run across all habits.
- **Last 30 days** — overall completion rate.
- **Avg check-in** — the average time of day you check off habits. Watch this to
  see whether you're doing things earlier over time.
- A **30-day bar chart** of daily completion %.

## 8. Backing up your data (important!)
Your data is stored in the browser, so use the footer buttons:
- **Export** — downloads a `.json` backup file. Do this occasionally.
- **Import** — restores from a backup file (replaces current data).

## 9. Deleting a habit
Click the **×** on a habit and confirm. This removes the habit *and* its history,
so export a backup first if you might want it later.

---

## 10. Installing on your phone
The app is a **PWA** (progressive web app), so it can live on your home screen
and work offline once hosted over HTTPS. See `DEPLOY.md` for hosting the site, then:

**On iPhone (Safari):**
1. Open the hosted URL in **Safari** (must be Safari, not Chrome, for install).
2. Tap the **Share** button → **Add to Home Screen** → **Add**.
3. Launch it from the home-screen icon 🌱 — it opens full-screen like a native app.

**On Android (Chrome):**
1. Open the URL in Chrome.
2. Tap the **⋮ menu** → **Install app** (or **Add to Home screen**).

Your data is stored per-device in the browser, so your phone and laptop keep
**separate** habit logs. Use **Export/Import** to move data between them.

---

## The nightly wind-down system (macOS)
Separate from the app, there are two nudges that help with late-night screens:
1. A **10:15pm notification** ("wind down — screens off soon") — see `nudge/README.md`.
2. A **10:30pm automatic shutdown** — run `sudo pmset repeat shutdown MTWRFSU 22:30:00`.

Together: you get warned, then the computer turns itself off.
