#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Convert all .m files (MATLAB) under a folder (including subfolders) to .txt
while preserving the directory structure.

Default behavior:
- Input:  <input_root>
- Output: <input_root>_txt/
- For each file: relative/path/file.m -> relative/path/file.txt

Notes:
- Uses binary copy to preserve exact content and avoid encoding issues.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def convert_m_to_txt(input_root: Path, output_root: Path, overwrite: bool, dry_run: bool) -> int:
    if not input_root.exists() or not input_root.is_dir():
        raise FileNotFoundError(f"Input folder not found or not a directory: {input_root}")

    input_root = input_root.resolve()
    output_root = output_root.resolve()

    m_files = sorted(input_root.rglob("*.m"))
    total = len(m_files)

    if total == 0:
        print(f"No .m files found under: {input_root}")
        return 0

    converted = 0
    skipped = 0
    errors = 0

    print(f"Input : {input_root}")
    print(f"Output: {output_root}")
    print(f"Found : {total} .m file(s)\n")

    for src in m_files:
        try:
            rel = src.relative_to(input_root)
            dst = (output_root / rel).with_suffix(".txt")

            # Ensure destination directory exists
            if not dry_run:
                dst.parent.mkdir(parents=True, exist_ok=True)

            if dst.exists() and not overwrite:
                skipped += 1
                print(f"[SKIP] exists: {dst}")
                continue

            if dry_run:
                print(f"[DRY ] {src} -> {dst}")
            else:
                # Binary copy to preserve content exactly
                data = src.read_bytes()
                dst.write_bytes(data)
                print(f"[OK  ] {src} -> {dst}")

            converted += 1

        except Exception as e:
            errors += 1
            print(f"[ERR ] {src} ({e})", file=sys.stderr)

    print("\nSummary")
    print(f"  Converted: {converted}")
    print(f"  Skipped  : {skipped}")
    print(f"  Errors   : {errors}")

    return 0 if errors == 0 else 2


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Recursively convert .m files to .txt while preserving folder structure."
    )
    p.add_argument(
        "input_root",
        type=Path,
        help="Input folder containing .m files (MATLAB scripts/functions).",
    )
    p.add_argument(
        "-o",
        "--output-root",
        type=Path,
        default=None,
        help="Output folder root. Default: <input_root>_txt",
    )
    p.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing .txt files.",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without writing files.",
    )
    return p


def main() -> int:
    parser = build_arg_parser()
    args = parser.parse_args()

    input_root: Path = args.input_root
    output_root: Path = args.output_root or Path(f"{input_root}_txt")

    return convert_m_to_txt(
        input_root=input_root,
        output_root=output_root,
        overwrite=args.overwrite,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    raise SystemExit(main())
