# PDF Answer Remover

Upload a worksheet PDF; red answer text is removed so students see questions only.

**Deploy:** See [`DEPLOY-NO-CARD.md`](DEPLOY-NO-CARD.md) for hosts that **do not require a credit card**.  
Render’s free tier often asks for a card for verification — optional one-click (may require card):  
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/bobbyum-cmyk/pdf-answer-remover)

## Local run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python web_app.py
```

Open http://127.0.0.1:5000

See `DEPLOY.md` for details.
