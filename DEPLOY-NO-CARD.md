# Deploy without a credit card

Render (and many similar platforms) often ask for a card **even for the free tier** — for abuse prevention, not an immediate charge. If you prefer **no card at all**, use one of these.

Your code is already on GitHub:  
**https://github.com/bobbyum-cmyk/pdf-answer-remover**

---

## Option 1: JustRunMy.App (recommended, no card)

Public HTTPS URL, deploys your **Dockerfile** from GitHub. Free baseline: small RAM (may struggle with very large PDFs — use files under ~10 MB if you hit memory limits).

1. Sign up: **https://justrunmy.app/** (no credit card).
2. **Create app** → deploy method **Git Push** or connect **GitHub** repo `bobbyum-cmyk/pdf-answer-remover`.
3. In app settings:
   - **Port / HTTPS:** expose **`10000`** (matches the Dockerfile).
   - **Health check path (if offered):** `/health`
   - **Environment:** `MAX_UPLOAD_MB=30` (optional, lowers memory vs 50).
4. Deploy and wait for the build to finish.
5. Open the HTTPS URL they give you and test an upload.

If the container is **killed (OOM)** on big PDFs, try a smaller file or upgrade RAM in their panel (paid) — or use Option 2.

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
