#!/usr/bin/env python3
"""Web UI: upload PDF, remove red answers, download result."""

from __future__ import annotations

import io
import os
import tempfile
from pathlib import Path

from flask import Flask, jsonify, render_template, request, send_file
from werkzeug.utils import secure_filename

from remove_red_pdf import process_pdf

app = Flask(__name__)
_max_mb = int(os.environ.get("MAX_UPLOAD_MB", "50"))
app.config["MAX_CONTENT_LENGTH"] = _max_mb * 1024 * 1024


def safe_download_stem(original_filename: str) -> str:
    name = secure_filename(original_filename)
    if not name or name == "_":
        name = "document.pdf"
    stem = Path(name).stem
    if not stem:
        stem = "document"
    return stem


@app.errorhandler(413)
def too_large(_exc):
    return jsonify({"error": "File is too large (max 50 MB)."}), 413


@app.get("/health")
def health():
    return jsonify({"ok": True})


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/api/process")
def api_process():
    upload = request.files.get("file")
    if upload is None or upload.filename == "":
        return jsonify({"error": "No file uploaded."}), 400

    filename = upload.filename or ""
    if not filename.lower().endswith(".pdf"):
        return jsonify({"error": "Only PDF files are supported."}), 400

    stem = safe_download_stem(filename)
    download_name = f"{stem}_no_red.pdf"

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        input_path = tmp_path / "input.pdf"
        output_path = tmp_path / "output.pdf"
        upload.save(input_path)

        try:
            removed = process_pdf(input_path, output_path)
        except Exception as exc:  # noqa: BLE001 — return message to client
            return jsonify({"error": f"Could not process PDF: {exc}"}), 400

        if not output_path.is_file():
            return jsonify({"error": "Processing produced no output."}), 500

        pdf_bytes = output_path.read_bytes()

    buffer = io.BytesIO(pdf_bytes)
    buffer.seek(0)

    response = send_file(
        buffer,
        mimetype="application/pdf",
        as_attachment=True,
        download_name=download_name,
    )
    response.headers["X-Red-Regions-Removed"] = str(removed)
    return response


def main() -> None:
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "5000"))
    debug = os.environ.get("FLASK_DEBUG", "").lower() in ("1", "true", "yes")
    app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":
    main()
