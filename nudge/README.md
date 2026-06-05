# Wind-down nudge (macOS)

A nightly notification at **10:15pm** reminding you screens go off soon.
Pairs with the 10:30pm auto-shutdown.

## Install (one time)
```bash
# 1. Make the script executable
chmod +x "/Users/jamesades/Documents/Claude/Projects/Better_habits/nudge/wind-down.sh"

# 2. Link the launch agent so macOS runs it on schedule
cp "/Users/jamesades/Documents/Claude/Projects/Better_habits/nudge/com.betterhabits.winddown.plist" ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.betterhabits.winddown.plist
```
No `sudo` needed — this is a per-user launch agent.

## Test it right now
```bash
bash "/Users/jamesades/Documents/Claude/Projects/Better_habits/nudge/wind-down.sh"
```
You should see a notification. If you don't, check
**System Settings → Notifications → Script Editor (or Terminal)** and allow alerts.

## Change the time
Edit `Hour` / `Minute` in the `.plist`, then reload:
```bash
launchctl unload ~/Library/LaunchAgents/com.betterhabits.winddown.plist
cp "/Users/jamesades/Documents/Claude/Projects/Better_habits/nudge/com.betterhabits.winddown.plist" ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.betterhabits.winddown.plist
```

## Remove it
```bash
launchctl unload ~/Library/LaunchAgents/com.betterhabits.winddown.plist
rm ~/Library/LaunchAgents/com.betterhabits.winddown.plist
```

## The companion auto-shutdown (10:30pm)
```bash
sudo pmset repeat shutdown MTWRFSU 22:30:00   # enable
pmset -g sched                                # check
sudo pmset repeat cancel                      # disable
```
