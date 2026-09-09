# Changelog

All notable changes to this Skill are documented here.

## [1.0.0] — 2026-09-09

### Added

- Full cross-disciplinary build-out of the v0.1.0 scaffold into a
  discipline/genre/research-design/argument-architecture pipeline (see the
  expanded "Operating hierarchy" in `SKILL.md`).
- `references/research-design-matrix.md` — claim ceilings by research design
  (RCT, cohort, DiD/RDD/IV, ML/simulation, process tracing, doctrinal, formal
  proof, etc.), independent of discipline.
- `references/claim-calibration.md` — the eight-way claim-type taxonomy (kept
  identical to `scholarly-corpus-builder`'s), the claim-strength invariant,
  and discipline-sensitive uncertainty language.
- `references/citation-integrity.md` — no-fabrication rules, the
  citation-preservation invariant, quotation discipline, and alignment with
  `scholarly-corpus-builder`'s source-verification states.
- `references/corpus-profile-integration.md` and
  `references/journal-style-adaptation.md` — consumption contracts for
  `scholarly-corpus-builder` and `journal-fit-engine` profiles, including
  voice precedence, OBSERVED/RECOMMENDED/MANDATORY separation, confidence
  gating, and standalone fallback.
- `references/review-writing.md` (narrative, systematic, scoping,
  meta-analysis, critical, and theoretical-synthesis reviews) and
  `references/commentary-writing.md` (Nature-style commentary, perspective,
  editorial, conceptual perspective).
- `references/continuity-ledger.md` — concept/claim/evidence/chapter ledgers
  and terminology-drift auditing, split out of `book-writing.md` for
  long-form work; `book-writing.md` gained chapter opening/closing variety
  guidance.
- `references/multilingual-writing.md` — language-independent vs.
  language-specific voice, architecture-level support for Chinese, German,
  French, Spanish, Japanese, and Korean, and translation-mode rules.
- `references/editing-modes.md` — `SURFACE_EDIT` / `STRUCTURAL_EDIT` /
  `ARGUMENT_RECONSTRUCTION` intensity levels and the eleven output modes.
- `references/quality-audit.md` — redundancy audit, reviewer-aware self-test,
  mechanism/theory/causal/normative/humanities-interpretation/statistical/
  formal/legal/historical integrity tests, quality states
  (`PASS`/`PASS_WITH_LIMITATIONS`/`REPAIR_REQUIRED`/`BLOCKED_BY_*`), repair
  order, and stop rule.
- `references/integration.md` — the ecosystem responsibility diagram shared
  with `scholarly-corpus-builder` and `journal-fit-engine`, and this Skill's
  own conceptual `VOICE_REQUEST`/`VOICE_OUTPUT` shape.
- Dedicated Economics subsection in `disciplines/social-sciences.md`, and
  dedicated Philosophy and History subsections in `disciplines/humanities.md`
  — kept inside their existing family files (not split into separate files)
  to stay consistent with the same 11-family grouping used by
  `journal-fit-engine`'s own `disciplines/` folder.
- Expanded `references/genre-matrix.md` (narrative/scoping review, short
  communication, Nature-style commentary essay) and
  `references/argument-architectures.md` (economics architecture; anomaly→
  competing-explanations→test→adjudication; concept→distinction→mechanism→
  boundary condition; authority→interpretive-conflict→application→
  consequence; two compact philosophical/clinical/humanistic patterns).
- `agents/openai.yaml` gained an `interface` block (`$scholarly-voice-engine`
  invocation convention) and `policy.allow_implicit_invocation`.
- `scripts/voice/` package (`profile_schema.py`, `profile_merge.py`,
  `continuity.py`, `audit.py`) and `scripts/package_runtime.py`, all stdlib
  only.
- `tests/` — `unittest` coverage for the validator and every `scripts/voice/`
  module, including deliberately negative cases (profile conflict,
  terminology contradiction, clean-text audit).
- Eval fixtures expanded from 50 to over 125 cases across discipline, genre,
  voice, anti-generic-AI, book-continuity, integrity, and multilingual
  dimensions.
- `VERSION` file.

### Changed

- `scripts/validate_skill.py` extended to check `VERSION`/CHANGELOG
  consistency, the new reference files, `references/integration.md`'s
  ecosystem coverage, and the raised eval-count floor.

### Known limitations

- English-first; the multilingual module is architecture-level, not a full
  per-language rhetorical rulebook.
- The historical-profile library remains illustrative, not exhaustive.
- Discipline modules describe family-level (and, for economics/philosophy/
  history, subfield-level) norms; individual sub-fields and journal house
  styles still require user-supplied specifics.
- `scripts/voice/continuity.py` and `audit.py` use heuristic, not NLP-based,
  detection — they catch obvious drift/contradiction and generic-AI phrasing,
  not subtle cases.
- No automated stylometric scoring; validation checks structure and known
  anti-patterns, not prose quality itself.

## [0.1.0] — 2026-09-09

### Added

- Initial internal scaffold of `scholarly-voice-engine`.
- Compact `SKILL.md` with progressive-loading pointers into `references/` and
  `disciplines/`.
- Eleven cross-cutting reference modules: voice engine, disciplinary matrix,
  genre matrix, argument architectures, human scholarly prose, historical
  voice profiles, era calibration, author voice calibration, article writing,
  book writing, interdisciplinary writing.
- Eleven discipline modules covering natural sciences, mathematics/formal
  sciences, engineering/computing, medicine/health, social sciences,
  business/management, law, humanities, education, arts/design, and
  interdisciplinary fields.
- Abstracted historical voice profiles and explicit living-author safeguards.
- Monograph continuity model for book-length work.
- Anti-generic-AI prose rules.
- Initial eval fixtures across discipline, genre, voice, and anti-generic-AI
  dimensions.
- `scripts/validate_skill.py` for structural validation and light dogfooding
  checks.
