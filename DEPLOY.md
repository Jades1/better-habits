# Deploying Better Habits (and installing on your phone)

The app works by just opening `index.html`. But to **install it on your phone**
and get **offline support**, it needs to be served over **HTTPS**. This guide
covers a quick local test and then real hosting.

---

## 1. Test the PWA locally (on your Mac)
Service workers run on `localhost`, so you can verify offline/install behavior
before hosting:
```bash
cd ~/Documents/Claude/Projects/Better_habits
python3 -m http.server 8000
```
Open <http://localhost:8000> in Chrome → the install icon appears in the address
bar. (This won't install on your *phone* — phones need real HTTPS, below.)

---

## 2. Host it on the web — recommended: GitHub Pages (free, HTTPS)
One-time GitHub login (interactive — run it yourself in the terminal):
```bash
gh auth login
```
Then, from the project folder:
```bash
cd ~/Documents/Claude/Projects/Better_habits
gh repo create better-habits --public --source=. --remote=origin --push
gh api -X POST repos/:owner/better-habits/pages -f "source[branch]=main" -f "source[path]=/" || \
  echo "If that errored, enable Pages in the repo: Settings → Pages → Branch: main → /(root)"
```
Your site will be live in ~1 minute at:
```
https://<your-github-username>.github.io/better-habits/
```
> Free GitHub Pages requires a **public** repo. If you'd rather keep it private,
> use Cloudflare Pages or Netlify (below), which host private projects for free.

### Updating the live site later
```bash
git add -A && git commit -m "update" && git push
```
After deploying changes, **bump `CACHE` in `sw.js`** so phones pick up the new
version instead of the cached one.

---

## 3. Alternatives (no GitHub, still free + HTTPS)
- **Netlify Drop** — go to <https://app.netlify.com/drop> and drag the project
  folder into the page. Instant HTTPS URL, no account needed to start.
- **Cloudflare Pages** / **Vercel** — connect a repo or upload; both free, both
  support private projects.

---

## 4. Install on your phone
Once you have an HTTPS URL:

**iPhone (must use Safari):**
1. Open the URL in **Safari**.
2. **Share** → **Add to Home Screen** → **Add**.
3. Open it from the 🌱 icon — runs full-screen, works offline.

**Android (Chrome):**
1. Open the URL in Chrome.
2. **⋮ menu** → **Install app**.

> Data is stored per-device. Your phone and laptop track habits **separately** —
> use **Export/Import** in the app footer to move data between them. (Real-time
> cross-device sync is on the backlog in `HANDOFF.md`.)
