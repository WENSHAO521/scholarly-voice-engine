#!/usr/bin/env python3
"""Package this Skill's runtime files into a distributable zip.

Bundles SKILL.md, README.md, LICENSE, CHANGELOG.md, VERSION, agents/,
assets/, references/, disciplines/, and scripts/ into
dist/scholarly-voice-engine-<version>.zip. Excludes tests/ and evals/ —
those are development-only, not needed by a host loading this Skill.

Usage:
    python scripts/package_runtime.py
"""
from __future__ import annotations

import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACKAGE_NAME = "scholarly-voice-engine"

RUNTIME_FILES = ["SKILL.md", "README.md", "LICENSE", "CHANGELOG.md", "VERSION"]
RUNTIME_DIRS = ["agents", "assets", "references", "disciplines", "scripts"]

# Never ship bytecode caches even though scripts/ is included for
# scripts/voice/*.py.
EXCLUDE_SUFFIXES = {".pyc"}
EXCLUDE_DIR_NAMES = {"__pycache__"}


def read_version() -> str:
    version_file = ROOT / "VERSION"
    if not version_file.is_file():
        print("error: VERSION file not found", file=sys.stderr)
        sys.exit(1)
    return version_file.read_text(encoding="utf-8").strip()


def iter_runtime_paths():
    for name in RUNTIME_FILES:
        path = ROOT / name
        if path.is_file():
            yield path, path.relative_to(ROOT)
    for dirname in RUNTIME_DIRS:
        base = ROOT / dirname
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*")):
            if path.is_dir():
                continue
            if path.suffix in EXCLUDE_SUFFIXES:
                continue
            if EXCLUDE_DIR_NAMES & set(path.relative_to(ROOT).parts):
                continue
            yield path, path.relative_to(ROOT)


def main() -> int:
    version = read_version()
    dist_dir = ROOT / "dist"
    dist_dir.mkdir(exist_ok=True)
    out_path = dist_dir / f"{PACKAGE_NAME}-{version}.zip"

    count = 0
    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for abs_path, rel_path in iter_runtime_paths():
            arcname = str(Path(PACKAGE_NAME) / rel_path)
            zf.write(abs_path, arcname)
            count += 1

    print(f"wrote {out_path} ({count} files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
