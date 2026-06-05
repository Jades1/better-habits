#!/usr/bin/env python3
"""Better Habits — local desktop helper.

Lets the Better Habits web app shut down THIS Mac and manage a nightly
auto-shutdown, since a browser tab can't touch system power on its own.

Safety model (shutting down a computer is destructive, so defense in depth):
  * Binds to 127.0.0.1 only — not reachable from other machines.
  * Dangerous endpoints require a secret pairing token (X-Habits-Token header).
  * CORS allowlist + Origin check — a random website can't trigger it from your
    browser (the custom header forces a preflight we reject for unknown origins).

It also serves the app's own files, so on this Mac you can open
http://localhost:7421 and get the full app WITH working shutdown controls
(handy if your browser blocks the GitHub Pages page from reaching localhost).
"""
import http.server
import socketserver
import json
import os
import subprocess
import secrets
import plistlib
import urllib.parse

HOST = "127.0.0.1"
PORT = 7421
HOME = os.path.expanduser("~")
# Files to serve (the app). When installed it's the helper's own dir, where
# install.sh copies the web assets. Override with BH_WEB_DIR for dev.
SERVE_DIR = os.environ.get("BH_WEB_DIR") or os.path.dirname(os.path.abspath(__file__))
TOKEN_FILE = os.path.join(HOME, ".better-habits-helper-token")
AGENT_LABEL = "com.betterhabits.autoshutdown"
LAUNCH_AGENTS = os.path.join(HOME, "Library", "LaunchAgents")
AGENT_PATH = os.path.join(LAUNCH_AGENTS, AGENT_LABEL + ".plist")

ALLOWED_ORIGINS = {
    "https://jades1.github.io",
    "http://127.0.0.1:%d" % PORT,
    "http://localhost:%d" % PORT,
}

# Graceful shutdown (lets apps prompt to save) — needs no sudo.
SHUTDOWN_AS = 'tell application "System Events" to shut down'


def get_token():
    """Read the pairing token, creating a private one on first run."""
    if os.path.exists(TOKEN_FILE):
        existing = open(TOKEN_FILE).read().strip()
        if existing:
            return existing
    token = secrets.token_urlsafe(18)
    fd = os.open(TOKEN_FILE, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as f:
        f.write(token)
    return token


TOKEN = get_token()


def do_shutdown():
    subprocess.Popen(["osascript", "-e", SHUTDOWN_AS])


def set_schedule(hour, minute):
    """Install a per-user launch agent that shuts the Mac down at hour:minute daily."""
    os.makedirs(LAUNCH_AGENTS, exist_ok=True)
    plist = {
        "Label": AGENT_LABEL,
        "ProgramArguments": ["/usr/bin/osascript", "-e", SHUTDOWN_AS],
        "StartCalendarInterval": {"Hour": int(hour), "Minute": int(minute)},
        "StandardErrorPath": "/tmp/betterhabits-autoshutdown.err",
        "StandardOutPath": "/tmp/betterhabits-autoshutdown.out",
    }
    subprocess.run(["launchctl", "unload", AGENT_PATH],
                   stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    with open(AGENT_PATH, "wb") as f:
        plistlib.dump(plist, f)
    subprocess.run(["launchctl", "load", AGENT_PATH])


def clear_schedule():
    subprocess.run(["launchctl", "unload", AGENT_PATH],
                   stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    if os.path.exists(AGENT_PATH):
        os.remove(AGENT_PATH)


def get_schedule():
    if not os.path.exists(AGENT_PATH):
        return {"enabled": False}
    try:
        with open(AGENT_PATH, "rb") as f:
            p = plistlib.load(f)
        sci = p.get("StartCalendarInterval", {})
        return {"enabled": True, "hour": sci.get("Hour"), "minute": sci.get("Minute")}
    except Exception:
        return {"enabled": False}


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=SERVE_DIR, **k)

    def log_message(self, *a):
        pass  # stay quiet

    # ---- CORS / auth helpers ----
    def _cors(self):
        origin = self.headers.get("Origin")
        if origin in ALLOWED_ORIGINS:
            self.send_header("Access-Control-Allow-Origin", origin)
            self.send_header("Vary", "Origin")
            self.send_header("Access-Control-Allow-Headers", "X-Habits-Token, Content-Type")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")

    def _json(self, code, obj):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self._cors()
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _origin_ok(self):
        origin = self.headers.get("Origin")
        return origin is None or origin in ALLOWED_ORIGINS

    def _authed(self):
        return self.headers.get("X-Habits-Token") == TOKEN

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path
        if path == "/status":
            return self._json(200, {"ok": True, "app": "better-habits-helper",
                                    "schedule": get_schedule()})
        return super().do_GET()  # otherwise serve the app's static files

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        if path not in ("/shutdown", "/schedule", "/unschedule"):
            return self._json(404, {"error": "not found"})
        if not self._origin_ok():
            return self._json(403, {"error": "origin not allowed"})
        if not self._authed():
            return self._json(401, {"error": "bad token"})

        qs = urllib.parse.parse_qs(parsed.query)
        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length) if length else b""
        try:
            body = json.loads(raw) if raw else {}
        except Exception:
            body = {}

        if path == "/shutdown":
            if qs.get("dry", ["0"])[0] == "1":   # token-check / preview, no action
                return self._json(200, {"ok": True, "dry": True, "would": SHUTDOWN_AS})
            do_shutdown()
            return self._json(200, {"ok": True, "shuttingDown": True})

        if path == "/schedule":
            h, m = body.get("hour"), body.get("minute")
            if h is None or m is None:
                return self._json(400, {"error": "hour and minute required"})
            set_schedule(h, m)
            return self._json(200, {"ok": True, "schedule": get_schedule()})

        if path == "/unschedule":
            clear_schedule()
            return self._json(200, {"ok": True, "schedule": get_schedule()})


def main():
    socketserver.ThreadingTCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer((HOST, PORT), Handler) as httpd:
        print("Better Habits helper → http://%s:%d  (serving %s)" % (HOST, PORT, SERVE_DIR))
        print("Pairing token: %s" % TOKEN)
        httpd.serve_forever()


if __name__ == "__main__":
    main()
