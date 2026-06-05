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

By default each device keeps its own habit log. To link them, set up sync below.

---

## 11. Reminders (gentle nudges)
The **Reminders** card lets you set little nudges with your own message — a
compassion prompt ("Be kind to yourself"), a posture check, a water reminder,
whatever you like.

**Add one:** tap **＋ Add reminder**, type the message, then choose either:
- **Repeat every…** — fires on an interval (e.g. every `30` minutes, or every `2`
  hours), or
- **At a time…** — fires once a day at a clock time (e.g. `15:00`).

Tap **Save**. When a reminder is due, a **banner slides in at the top** and a
**soft chime** plays.

**Managing reminders:**
- **Tap** a reminder to turn it **on/off** (the switch slides green when on).
- **Press and hold** a reminder to **edit** it — like rearranging apps on an
  iPhone. Change the message, timing, or delete it.
- Tap the **×** to delete.

**System notifications (optional):** at the bottom of the Reminders card, tap
**Enable notifications** to also get a real OS notification when a reminder is
due *and the app isn't the window you're looking at*. While you're actively in
the app you just get the in-app banner + chime (no double alert); when it's in
the background, you get a system notification you can click to jump back in.

Good to know:
- Reminders fire **while the app is open** (foreground or background). A web app
  can't reliably alert you when it's **fully closed** — especially on iPhone — so
  for a closed-app nudge, leave it open in the background, or use a time-of-day
  reminder for around when you'll be using it.
- System notifications work best on **desktop**. On **iPhone** they require the
  app to be **installed to your Home Screen** (see §10) and permission granted.
- **Time-of-day** notifications **stay on screen until you dismiss them** (so you
  don't miss the one daily nudge); **interval** notifications auto-dismiss, since
  they keep coming and would otherwise pile up.
- The **first tap anywhere** in the app unlocks sound (a browser rule), so the
  chime works from then on.
- Reminders **sync across your devices** if you've set the same sync code.
  (The notification permission itself is per-device — enable it on each.)

---

## 12. Counters (tap buttons)
The **Counters** card has **three square buttons** you can make your own — handy
for tallying anything through the day: glasses of water, pushups, deep breaths,
times you stepped away from a screen.

**Use one:** just **tap** the button — the big number counts up by one each press.

**Customize it:** **press and hold** a button (iPhone-style) to open its editor,
where you can:
- **Label** it — your text shows on the button (e.g. *Water*).
- **Color** it — pick from the swatches.
- See **Recent days** — the last 7 days of tallies, today highlighted.
- **Reset count** — set today back to 0 (past days are kept).

Good to know:
- **Resets daily** — each button starts at 0 every morning, so the number is
  always "today so far."
- **Every day is tracked** — your daily totals are saved as history (that's the
  "Recent days" strip), so nothing is lost when it resets.
- Counters **sync across your devices** on the same sync code.

---

## 13. Syncing across your devices
The **⇅ Sync** button (footer) keeps your phone and laptop in sync.

1. On the first device, tap **⇅ Sync** and type a **sync code** — any secret
   phrase you'll remember (e.g. `purple-otter-3712`). The button turns green
   (**⇅ Synced ✓**).
2. On every other device, tap **⇅ Sync** and enter the **exact same code**.
3. That's it. Check off a habit on your phone and it shows up on your laptop
   within a few seconds (it syncs while the app is open, and instantly when you
   switch back to it).

How it behaves:
- **Edits merge intelligently** — a check-off on either device counts, and
  deleting a habit or unchecking a day syncs too. You won't lose data if both
  devices were edited.
- **It still works offline** — changes upload next time you're connected.
- **Turn it off** anytime: tap **⇅ Sync** and leave the code blank.
- **Sharing the app?** Give a tester a *different* code and they get the same
  app with completely separate data.

> Your sync code is the only thing protecting your data, so pick something not
> trivially guessable. Habit names + checkmarks aren't sensitive, so a simple
> memorable phrase is fine.

---

## 14. Shutting your Mac down from the app
The **Wind-down · this Mac** card lets you power this Mac off from the app — both
a **⏻ Shut down now** button and a **nightly auto-shutdown** time.

A browser can't turn off a computer by itself, so this uses a tiny **desktop
helper** that runs in the background on your Mac. One-time setup:

1. In Terminal, run:
   ```bash
   bash "/Users/jamesades/Documents/Claude/Projects/Better_habits/helper/install.sh"
   ```
   It prints a **pairing token** and starts the helper.
2. Open the app **on that Mac**. The **Wind-down · this Mac** card appears.
3. Click **Connect helper** and paste the token.
4. Now you can:
   - **⏻ Shut down now** — graceful shutdown (apps can prompt to save first).
   - **Auto shut-down at [time] → Save** — e.g. set `22:30` for a nightly 10:30 PM
     shutdown. **Turn off** removes it.

Notes:
- The card only appears on the **Mac the helper is installed on** — your phone
  can't shut the laptop down (different machine).
- It's safe: the helper only listens on your own machine, requires the secret
  token, and rejects other websites.
- Tip: on that Mac you can also just open **http://localhost:7421** to get the
  app with the controls already wired up. Full details in `helper/README.md`.

---

## The nightly wind-down system (macOS)
Separate from the app, there are two nudges that help with late-night screens:
1. A **10:15pm notification** ("wind down — screens off soon") — see `nudge/README.md`.
2. A **10:30pm automatic shutdown** — run `sudo pmset repeat shutdown MTWRFSU 22:30:00`.

Together: you get warned, then the computer turns itself off.
