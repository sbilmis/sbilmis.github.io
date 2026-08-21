#!/usr/bin/env python3
"""Copy static pages into the generated Quarto site."""

from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEGACY = ROOT / "archive" / "legacy-site"
OUTPUT = ROOT / "_site"


def copy_directory(source: Path, name: str | None = None) -> None:
    destination = OUTPUT / (name or source.name)
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(source, destination, ignore=shutil.ignore_patterns(".DS_Store"))


def copy_legacy_directory(name: str) -> None:
    copy_directory(LEGACY / name, name)


def main() -> None:
    copy_legacy_directory("scientometrics")
    copy_directory(ROOT / "truba-assistant")
    copy_directory(ROOT / "halisaha")

    blogs_output = OUTPUT / "blogs"
    blogs_output.mkdir(parents=True, exist_ok=True)
    shutil.copy2(LEGACY / "blogs" / "index.html", blogs_output / "index.html")


if __name__ == "__main__":
    main()
