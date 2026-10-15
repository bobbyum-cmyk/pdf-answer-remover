# Deploy without a credit card

Render (and many similar platforms) often ask for a card **even for the free tier** — for abuse prevention, not an immediate charge. If you prefer **no card at all**, use one of these.

Your code is already on GitHub:  
**https://github.com/bobbyum-cmyk/pdf-answer-remover**

---

## Option 1: JustRunMy.App (recommended, no card)

Public HTTPS URL. **There is no “deploy from GitHub” button** — JustRunMy uses **Zip upload** or **Git push to their own remote** (not GitHub).

Free baseline: small RAM (may struggle with very large PDFs — use files under ~10 MB if you hit memory limits).

### A) Zip upload (easiest)

1. Sign up / open panel: **https://justrunmy.app/panel**
2. **Add app** → choose **Zip Upload** (not Template).
3. Upload `pdf-answer-remover-deploy.zip` from this project (create it with `./scripts/make-deploy-zip.sh`).
4. After the app exists, open its settings:
   - **HTTPS / port:** map **`10000`** (must match the Dockerfile).
   - **Env (optional):** `MAX_UPLOAD_MB=30`
5. Start / deploy, wait for the build, open the public HTTPS link.

### B) Git push (updates from your Mac)

1. **Add app** → choose **Git Push**.
2. Copy the **Git URL** the panel shows (one-liner like `git remote add jrma …`).
3. On your machine:

   ```bash
   cd /Users/leungchiwai/Downloads/Transfer
   git remote add jrma '<PASTE-URL-FROM-PANEL>'
   git push jrma main
   ```

4. Set port **`10000`** in the app settings, then redeploy if needed.

GitHub is only for your backup; JustRunMy builds from **zip** or **push to jrma**, not from github.com.

If the container is **killed (OOM)** on big PDFs, try a smaller file or use Option 2 (Enzonic, 512 MB).

---

## Option 2: Enzonic (no card, 512 MB RAM)

Better for larger PDFs; Python/Flask hosting (not Docker-only).

1. Sign up: **https://enzonic.com/python** (free tier, no card).
2. Create a new **Python** app and connect GitHub repo `pdf-answer-remover` (or upload project zip without `.venv` / `*.pdf`).
3. Set start command:

   ```bash
   gunicorn web_app:app --bind 0.0.0.0:$PORT --workers 1 --threads 2 --timeout 180
   ```

4. Set env `MAX_UPLOAD_MB=50` if their panel allows it.
5. Deploy and use the URL they provide.

---

## Option 3: Cloudflare Tunnel (no card, runs on your Mac)

Your computer serves the app; Cloudflare gives a public **https://…trycloudflare.com** link (quick tunnel) or a stable URL with a free Cloudflare account.

**Quick test (URL changes each time you restart):**

```bash
cd /Users/leungchiwai/Downloads/Transfer
source .venv/bin/activate
python web_app.py &
cloudflared tunnel --url http://127.0.0.1:5000
```

Copy the `https://….trycloudflare.com` line from the terminal and share it with students. Your Mac must stay on and awake.

**Stable URL:** create a free account at **https://dash.cloudflare.com** (usually no card), then follow Cloudflare’s “Create a tunnel” docs and point it at `http://127.0.0.1:5000`.

---

## Option 4: Keep using Render anyway

Adding a card on Render’s free plan typically **does not charge** unless you upgrade to a paid instance type. Many schools use this only for verification. If you are comfortable with that, the one-click link still works:

https://render.com/deploy?repo=https://github.com/bobbyum-cmyk/pdf-answer-remover

---

## Create a zip (for “upload project” hosts)

From the project folder:

```bash
./scripts/make-deploy-zip.sh
```

Upload `pdf-answer-remover-deploy.zip` where the host asks for a zip (exclude PDFs and `.venv`).
