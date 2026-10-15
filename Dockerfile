FROM python:3.12-slim-bookworm

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HOST=0.0.0.0 \
    PORT=10000

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY remove_red_pdf.py web_app.py ./
COPY templates/ templates/

EXPOSE 10000

# One worker keeps memory predictable for large PDFs on 512 MB free tiers.
CMD gunicorn web_app:app \
    --bind 0.0.0.0:${PORT} \
    --workers 1 \
    --threads 2 \
    --timeout 180 \
    --keep-alive 5
