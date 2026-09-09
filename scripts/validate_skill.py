#!/usr/bin/env python3
"""Structural validator for the scholarly-voice-engine Skill.

Checks:
  1. SKILL.md exists and has valid, minimal YAML frontmatter (name, description).
  2. Every references/*.md and disciplines/*.md file mentioned by relative path
     in SKILL.md actually exists on disk (catches broken progressive-loading links).
  3. Every discipline module declares the required schema keys.
  4. Eval fixtures under evals/*.jsonl are well-formed JSON, one object per line,
     and non-empty.
  5. Light dogfooding pass: scans this Skill's own reference prose for the
     anti-generic-AI patterns it tells the model to avoid, so the Skill does not
     violate its own rules (a few example-context hits are allowed and reported,
     not treated as failures).

Exit code 0 on success (no hard failures), 1 otherwise. Warnings do not affect
the exit code but are printed.

Usage:
    python scripts/validate_skill.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_TOP_LEVEL = ["SKILL.md", "README.md", "LICENSE", "CHANGELOG.md", "VERSION"]
REQUIRED_DIRS = ["references", "disciplines", "evals", "scripts", "tests"]

REQUIRED_DISCIPLINE_KEYS = [
    "discipline_family",
    "default_claim_style",
    "typical_argument_structures",
    "typical_evidence",
    "citation_behavior",
    "methods_visibility",
    "acceptable_first_person",
    "common_failure_modes",
    "recommended_voice_profiles",
    "book_writing_norms",
    "article_writing_norms",
]

EVAL_FILES = [
    "evals/discipline-cases.jsonl",
    "evals/genre-cases.jsonl",
    "evals/voice-cases.jsonl",
    "evals/anti-generic-ai-cases.jsonl",
    "evals/book-continuity-cases.jsonl",
    "evals/integrity-cases.jsonl",
    "evals/multilingual-cases.jsonl",
]

MIN_TOTAL_EVAL_CASES = 100

SIBLING_SKILLS = ("adaptive model router", "scholarly corpus builder", "journal fit engine")

# Anti-generic-AI phrases this Skill tells the model to avoid overusing.
# Flagged only outside of the files that intentionally *list* these phrases as
# examples (human-scholarly-prose.md, anti-generic-ai-cases.jsonl).
GENERIC_AI_PHRASES = [
    r"\bfurthermore\b",
    r"\bmoreover\b",
    r"\bit is important to note that\b",
    r"\bit is worth noting that\b",
    r"\bin today's rapidly changing world\b",
    r"\bin conclusion\b",
]

EXEMPT_FROM_PHRASE_SCAN = {
    "references/human-scholarly-prose.md",
    "references/multilingual-writing.md",
    "references/book-writing.md",
    "references/review-writing.md",
    "evals/anti-generic-ai-cases.jsonl",
}

errors: list[str] = []
warnings: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


def check_top_level() -> None:
    for name in REQUIRED_TOP_LEVEL:
        if not (ROOT / name).is_file():
            fail(f"missing required top-level file: {name}")
    for name in REQUIRED_DIRS:
        if not (ROOT / name).is_dir():
            fail(f"missing required directory: {name}")
    if not (ROOT / ".github" / "workflows" / "validate.yml").is_file():
        fail("missing required file: .github/workflows/validate.yml")


def parse_frontmatter(text: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        return {}
    fm: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            key, _, value = line.partition(":")
            fm[key.strip()] = value.strip()
    return fm


def check_skill_md() -> str:
    path = ROOT / "SKILL.md"
    if not path.is_file():
        fail("SKILL.md not found")
        return ""
    text = path.read_text(encoding="utf-8")
    fm = parse_frontmatter(text)
    if "name" not in fm:
        fail("SKILL.md frontmatter missing 'name'")
    elif fm["name"] != "scholarly-voice-engine":
        warn(f"SKILL.md name is '{fm['name']}', expected 'scholarly-voice-engine'")
    if "description" not in fm or not fm["description"]:
        fail("SKILL.md frontmatter missing non-empty 'description'")
    return text


def check_referenced_files_exist(skill_text: str) -> None:
    # Find relative markdown links like `references/foo.md` or `disciplines/foo.md`
    paths = set(re.findall(r"(?:references|disciplines)/[a-zA-Z0-9_\-]+\.md", skill_text))
    if not paths:
        warn("no references/ or disciplines/ paths found inside SKILL.md")
    for rel in sorted(paths):
        if not (ROOT / rel).is_file():
            fail(f"SKILL.md references missing file: {rel}")

    # Also verify every file that exists on disk is mentioned *somewhere* it can be
    # discovered from: SKILL.md, README.md's layout tree, or (for discipline files,
    # which SKILL.md deliberately does not enumerate by name -- see
    # references/disciplinary-matrix.md) the routing table. README's tree format
    # splits "folder/" and "file.md" across lines, so match on filename alone
    # against each source rather than requiring the full "folder/file.md" string.
    readme_text = (ROOT / "README.md").read_text(encoding="utf-8") if (ROOT / "README.md").is_file() else ""
    matrix_path = ROOT / "references" / "disciplinary-matrix.md"
    matrix_text = matrix_path.read_text(encoding="utf-8") if matrix_path.is_file() else ""
    discoverable_from = skill_text + "\n" + readme_text + "\n" + matrix_text
    for folder in ("references", "disciplines"):
        for f in sorted((ROOT / folder).glob("*.md")):
            rel = f"{folder}/{f.name}"
            if rel not in discoverable_from and f.name not in discoverable_from:
                warn(f"{rel} exists but is not discoverable from SKILL.md, README.md, or disciplinary-matrix.md")


def check_discipline_schema() -> None:
    disc_dir = ROOT / "disciplines"
    if not disc_dir.is_dir():
        return
    for f in sorted(disc_dir.glob("*.md")):
        text = f.read_text(encoding="utf-8")
        missing = [k for k in REQUIRED_DISCIPLINE_KEYS if f"{k}:" not in text]
        if missing:
            fail(f"disciplines/{f.name} missing schema keys: {', '.join(missing)}")


def check_eval_fixtures() -> None:
    total_cases = 0
    for rel in EVAL_FILES:
        path = ROOT / rel
        if not path.is_file():
            fail(f"missing eval fixture: {rel}")
            continue
        lines = [ln for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]
        if not lines:
            fail(f"{rel} is empty")
            continue
        for i, line in enumerate(lines, start=1):
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as e:
                fail(f"{rel}:{i} invalid JSON ({e})")
                continue
            if "id" not in obj:
                warn(f"{rel}:{i} case missing 'id' field")
            total_cases += 1
    if total_cases < MIN_TOTAL_EVAL_CASES:
        warn(f"only {total_cases} total eval cases found; target is >= {MIN_TOTAL_EVAL_CASES}")
    else:
        print(f"[ok] {total_cases} eval cases across {len(EVAL_FILES)} fixture files")


def check_version() -> None:
    version_path = ROOT / "VERSION"
    changelog_path = ROOT / "CHANGELOG.md"
    if not version_path.is_file():
        fail("VERSION file not found")
        return
    version = version_path.read_text(encoding="utf-8").strip()
    if not re.match(r"^\d+\.\d+\.\d+$", version):
        fail(f"VERSION content {version!r} is not a plain semver string")
        return
    if not changelog_path.is_file():
        return
    changelog = changelog_path.read_text(encoding="utf-8")
    m = re.search(r"^## \[(\d+\.\d+\.\d+)\]", changelog, re.MULTILINE)
    if not m:
        warn("CHANGELOG.md has no '## [x.y.z]' heading to check VERSION against")
        return
    latest = m.group(1)
    if latest != version:
        fail(f"VERSION ({version}) does not match CHANGELOG.md's latest entry ({latest})")
    else:
        print(f"[ok] VERSION ({version}) matches CHANGELOG.md's latest entry")


def check_integration_file() -> None:
    path = ROOT / "references" / "integration.md"
    if not path.is_file():
        fail("references/integration.md not found")
        return
    text = path.read_text(encoding="utf-8").lower()
    missing = [name for name in SIBLING_SKILLS if name not in text]
    if missing:
        fail(f"references/integration.md does not mention: {', '.join(missing)}")
    else:
        print("[ok] references/integration.md names all three sibling skills")


def check_dogfood_prose() -> None:
    hits = 0
    for folder in ("references", "disciplines"):
        for f in sorted((ROOT / folder).glob("*.md")):
            rel = f"{folder}/{f.name}"
            if rel in EXEMPT_FROM_PHRASE_SCAN:
                continue
            text = f.read_text(encoding="utf-8").lower()
            for pattern in GENERIC_AI_PHRASES:
                for _ in re.finditer(pattern, text):
                    hits += 1
                    warn(f"{rel}: contains generic-AI phrase matching /{pattern}/")
    if hits == 0:
        print("[ok] no generic-AI transition phrases found outside documented examples")


def check_no_invented_quotations() -> None:
    # Historical profiles must not contain quotation marks around attributed text
    # immediately following a scholar's name pattern like `Name — "..."`.
    path = ROOT / "references" / "historical-voice-profiles.md"
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8")
    suspicious = re.findall(r"[A-Z][a-z]+ (?:said|wrote|once wrote)[:,]?\s*\"", text)
    if suspicious:
        fail("historical-voice-profiles.md appears to contain invented quotations")
    else:
        print("[ok] no invented-quotation patterns found in historical-voice-profiles.md")


def main() -> int:
    check_top_level()
    skill_text = check_skill_md()
    if skill_text:
        check_referenced_files_exist(skill_text)
    check_discipline_schema()
    check_eval_fixtures()
    check_dogfood_prose()
    check_no_invented_quotations()
    check_version()
    check_integration_file()

    print()
    if warnings:
        print(f"{len(warnings)} warning(s):")
        for w in warnings:
            print(f"  - {w}")
    if errors:
        print(f"\n{len(errors)} error(s):")
        for e in errors:
            print(f"  - {e}")
        print("\nVALIDATION FAILED")
        return 1

    print("\nVALIDATION PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
