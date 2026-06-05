# Desktop helper — shut down your Mac from the app

A browser tab can't power off a computer (sandbox). This tiny helper bridges
that: it runs in the background on your Mac, and the app talks to it over
`http://localhost:7421` to **shut down now** or **schedule a nightly shutdown**.

No `sudo`, no extra dependencies — it uses the `python3` already on macOS.

## Install (one time)
```bash
bash "/Users/jamesades/Documents/Claude/Projects/Better_habits/helper/install.sh"
```
This registers a launch agent (auto-starts at login, restarts if it crashes) and
prints your **pairing token**. Then in the app:

1. Open the **Wind-down · this Mac** card (it appears once the helper is running).
2. Click **Connect helper** and paste the token.
3. Use **⏻ Shut down now**, or set a time and **Save** for a nightly auto-shutdown.

> On this Mac you can also open **http://localhost:7421** directly — the helper
> serves the full app with shutdown controls already wired up (no token paste,
> and no browser "mixed content" hassle). Enter your sync code there to see your
> habits.

## How it stays safe
Shutting a machine down is destructive, so the helper has three guards:
- **Local only** — binds to `127.0.0.1`, unreachable from other devices.
- **Token** — `/shutdown` and `/schedule` require the secret pairing token.
- **Origin/CORS** — only the Better Habits app's origins may call it from a
  browser; unknown sites are rejected at the CORS preflight.

The shutdown itself is **graceful** (`System Events → shut down`, like choosing
Shut Down from the Apple menu), so apps can prompt you to save first.

## Manage it
```bash
# see what it's doing
cat /tmp/betterhabits-helper.out
launchctl list | grep betterhabits

# the nightly auto-shutdown agent (created when you set a time in the app)
launchctl list | grep autoshutdown
cat ~/Library/LaunchAgents/com.betterhabits.autoshutdown.plist

# stop / remove the helper
launchctl unload ~/Library/LaunchAgents/com.betterhabits.helper.plist
rm ~/Library/LaunchAgents/com.betterhabits.helper.plist
# and the auto-shutdown, if set:
launchctl unload ~/Library/LaunchAgents/com.betterhabits.autoshutdown.plist 2>/dev/null
rm -f ~/Library/LaunchAgents/com.betterhabits.autoshutdown.plist
```

## Endpoints (for reference)
| Method | Path | Auth | Does |
|--------|------|------|------|
| GET  | `/status`     | none  | liveness + current schedule |
| POST | `/shutdown`   | token | graceful shutdown now (`?dry=1` = token check only) |
| POST | `/schedule`   | token | set nightly shutdown `{hour, minute}` |
| POST | `/unschedule` | token | turn the nightly shutdown off |
