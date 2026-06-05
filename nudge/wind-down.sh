#!/bin/bash
# Better Habits — nightly wind-down nudge.
# Shows a macOS notification reminding you that screens are about to go off.
# Scheduled by com.betterhabits.winddown.plist (default: 10:15pm daily).

osascript -e 'display notification "Screens off in 15 minutes — time to wind down. 🌙" with title "🌱 Better Habits" sound name "Submarine"'

# Optional spoken reminder — uncomment to also hear it:
# say "Time to wind down. Screens off in fifteen minutes."
