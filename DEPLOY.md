# Deploy on the internet (free containers)

This app is packaged as a **Docker** image. The easiest free option that runs the full upload/process flow (not static-only) is **Render**.

## Recommended: [Render](https://render.com) (free tier — **card often required**)

> As of 2026, Render frequently asks for a credit card on signup even for the Free plan (verification; you are not charged unless you upgrade). For **no card**, use [`DEPLOY-NO-CARD.md`](DEPLOY-NO-CARD.md) (JustRunMy.App, Enzonic, or Cloudflare Tunnel).

**What you get:** public HTTPS URL, Docker deploy, **750 instance-hours/month**, 512 MB RAM.

**Catch:** the service **sleeps after ~15 minutes** with no traffic; the first visit after sleep may take **~1 minute** to wake. Fine for a personal/school tool.

### Steps

1. Push this folder to a **GitHub** repository (private or public).
2. Sign up at [render.com](https://render.com).
3. **New → Blueprint** (or **New → Web Service**).
4. Connect GitHub and select the repo.
5. If using **Web Service** manually:
   - **Environment:** Docker
   - **Plan:** Free
   - **Region:** Singapore (or closest to you)
   - **Health check path:** `/health`
6. Deploy. Render sets `PORT` automatically; the Dockerfile uses it.
7. Open the URL Render gives you (e.g. `https://pdf-answer-remover.onrender.com`).

Optional: **New → Blueprint** and point at `render.yaml` in the repo for one-click setup.

### Local Docker test (before deploy)

```bash
docker build -t pdf-answer-remover .
docker run --rm -p 8080:10000 -e PORT=10000 pdf-answer-remover
```

Open http://127.0.0.1:8080

---

## Other free-ish options (2026)

| Platform | Docker | Card required? | Notes |
|----------|--------|----------------|--------|
| **Render** | Yes | No | Best match for this app; sleeps when idle |
| **Railway** | Yes | No for trial | ~$5 trial, then very small monthly credit |
| **Google Cloud Run** | Yes | Yes | Pay-per-use; small traffic often stays in free quota |
| **Fly.io** | Yes | Yes | No meaningful always-free tier anymore |
| **Koyeb** | Yes | Yes ($ hold) | 1 free service, scale-to-zero |

For a classroom tool with occasional use, **Render free** is usually enough. If you need **always-on** with no cold start, you need a paid plan (~$7/month on Render) or Cloud Run with minimum instances (paid).

---

## Environment variables

| Variable | Default | Meaning |
|----------|---------|---------|
| `PORT` | `5000` / `10000` in Docker | Set by the host (Render injects this) |
| `MAX_UPLOAD_MB` | `50` | Max upload size per PDF |

---

## Security note

Files are processed in memory/temp storage and are not saved intentionally. Do not upload confidential documents to a public free tier unless you accept shared-cloud risk.
