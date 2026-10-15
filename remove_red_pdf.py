#!/usr/bin/env python3
"""Remove red-colored text and graphics from PDF files."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pymupdf as fitz


def color_int_to_rgb(color: int) -> tuple[int, int, int]:
    return (color >> 16) & 255, (color >> 8) & 255, color & 255


def is_red_rgb(r: int, g: int, b: int) -> bool:
    """Heuristic for answer-key red (pure red and common print reds)."""
    if r < 120:
        return False
    if r < max(g, b) + 25:
        return False
    return g <= 140 and b <= 140 and (r - min(g, b)) >= 40


def is_red_color_int(color: int) -> bool:
    return is_red_rgb(*color_int_to_rgb(color))


def is_red_float_color(color: tuple[float, ...] | None) -> bool:
    if not color or len(color) < 3:
        return False
    r, g, b = color[0], color[1], color[2]
    if max(color[:3]) <= 1.01:
        r, g, b = r * 255, g * 255, b * 255
    return is_red_rgb(int(round(r)), int(round(g)), int(round(b)))


def expand_rect(rect: fitz.Rect, padding: float = 0.5) -> fitz.Rect:
    return rect + (-padding, -padding, padding, padding)


def redact_red_on_page(page: fitz.Page, fill: tuple[float, float, float]) -> int:
    count = 0

    for block in page.get_text("dict")["blocks"]:
        if block.get("type") != 0:
            continue
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                if not is_red_color_int(span.get("color", 0)):
                    continue
                rect = fitz.Rect(span["bbox"])
                if rect.is_empty or rect.is_infinite:
                    continue
                page.add_redact_annot(expand_rect(rect), fill=fill)
                count += 1

    for drawing in page.get_drawings():
        rect = drawing.get("rect")
        if rect is None:
            continue
        if is_red_float_color(drawing.get("color")) or is_red_float_color(
            drawing.get("fill")
        ):
            page.add_redact_annot(expand_rect(fitz.Rect(rect)), fill=fill)
            count += 1

    if count:
        page.apply_redactions()
    return count


def process_pdf(input_path: Path, output_path: Path) -> int:
    doc = fitz.open(input_path)
    total = 0
    fill = (1.0, 1.0, 1.0)

    for page in doc:
        total += redact_red_on_page(page, fill=fill)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(output_path, garbage=4, deflate=True)
    doc.close()
    return total


def default_output_path(input_path: Path, output_dir: Path | None) -> Path:
    stem = input_path.stem + "_no_red"
    directory = output_dir if output_dir is not None else input_path.parent
    return directory / f"{stem}{input_path.suffix}"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Remove red-colored content from PDF files (e.g. answer keys)."
    )
    parser.add_argument(
        "inputs",
        nargs="+",
        type=Path,
        help="One or more input PDF paths",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        default=None,
        help="Directory for output files (default: same folder as each input)",
    )
    parser.add_argument(
        "--suffix",
        default="_no_red",
        help="Suffix inserted before .pdf on output filenames (default: _no_red)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    exit_code = 0

    for input_path in args.inputs:
        input_path = input_path.expanduser().resolve()
        if not input_path.is_file():
            print(f"Error: not found: {input_path}", file=sys.stderr)
            exit_code = 1
            continue
        if input_path.suffix.lower() != ".pdf":
            print(f"Error: not a PDF: {input_path}", file=sys.stderr)
            exit_code = 1
            continue

        if args.output_dir is not None:
            out_dir = args.output_dir.expanduser().resolve()
            output_path = out_dir / f"{input_path.stem}{args.suffix}{input_path.suffix}"
        else:
            output_path = input_path.with_name(
                f"{input_path.stem}{args.suffix}{input_path.suffix}"
            )

        try:
            removed = process_pdf(input_path, output_path)
        except Exception as exc:  # noqa: BLE001 — CLI boundary
            print(f"Error processing {input_path}: {exc}", file=sys.stderr)
            exit_code = 1
            continue

        print(f"{input_path.name} -> {output_path} ({removed} red regions removed)")

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
