# Changelog

All notable changes to this Skill are documented here.

## [1.1.0] — 2026-09-09

Closes the other compatibility gap v1.0.1/v1.0.2 documented rather than
faked: `JOURNAL_STYLE_CONTEXT_V1` was declared as "not yet reconciled" in
`references/integration.md` because journal-fit-engine did not yet emit it
and this Skill had no consumer for it. journal-fit-engine v0.3.0 now emits
it (`jfe.style_context`); this release adds the consumer.

### Added

- `scripts/voice/journal_context.py` — `from_journal_style_context_v1()`
  validates an incoming envelope (protocol, required fields, dict-typed
  buckets, freshness enum) and raises `JournalContextError` rather than
  coercing a malformed one; `apply_journal_style_context()` folds it into
  an existing voice-precedence layer set. `official_requirements` is
  returned as `hard_requirements`, verbatim, never confidence-gated and
  never merged into the precedence-resolved layers — it sits above
  author/discipline/journal/historical precedence entirely
  (`journal-style-adaptation.md`). `observed_patterns` is fed into
  `profile_merge.resolve_voice_precedence()` as the existing "journal"
  layer, reusing that function's tested confidence-gating rather than
  building a second precedence mechanism; confidence is set from
  `freshness` (`current`→high, `aging`→moderate, `stale` or **absent**
  →low — a missing freshness is never silently treated as current). Every
  evidence gap (no official_requirements, no observed_patterns, stale or
  absent freshness) produces a `limitations` entry that is preserved
  through to the caller, never summarized away.
- 18 new tests, including explicit regressions for: a stale/absent
  freshness yielding to a lower-precedence layer instead of winning on
  weak evidence; the author layer still beating a "journal" layer of any
  freshness; and `official_requirements`/`observed_patterns` never
  leaking into each other's output path after a full
  validate→apply round trip.
- `references/integration.md`'s `JOURNAL_STYLE_CONTEXT_V1` compatibility
  entry updated from "not yet reconciled" to reconciled, describing the
  two-path handling above.
- `references/journal-style-adaptation.md` now documents the
  `JOURNAL_STYLE_CONTEXT_V1` handoff as the primary path, with the older
  compact/full adaptation-target shapes kept as a secondary path for a
  caller that has already derived writing-level adjustments itself.

### Unchanged (by design)

- The existing `journal_context`/`validate_journal_target()` compact/full
  adaptation-target consumption path (`scripts/voice/profile_schema.py`)
  is untouched — the two input shapes are not mutually exclusive.

## [1.0.2] — 2026-09-09

Closes one of the two compatibility gaps v1.0.1 documented rather than
faked.

### Added

- `scripts/voice/continuity.py`'s `ContinuityLedger` now has
  `to_dict()`/`from_dict()`, serializing to and restoring from a
  `CONTINUITY_STATE_V1` envelope. Previously in-memory only, so it could
  not actually be "passed between chapter-drafting sessions" as that
  protocol's own description requires -- now it can. A restored ledger
  still enforces the same concept-redefinition/claim-contradiction checks
  as the original (verified by a round-trip test that a restored ledger
  still raises `ContinuityConflict`). `voice_contract`/`evidence_ledger`/
  `chapter_ledger`/`terminology`/`open_questions` round-trip opaquely --
  stored and returned unchanged, not yet validated or acted on.
- 6 new tests covering the round trip, conflict-detection survival, and
  malformed-input rejection.

### Still open

- `JOURNAL_STYLE_CONTEXT_V1` vs. this Skill's `journal_context` shape
  mismatch (see references/integration.md) remains unresolved --
  `journal-fit-engine` v0.2.0 still doesn't emit either that protocol or
  an adaptation-target shape in code (its own fit logic covers evidence
  lookup and one fit dimension so far, not adaptation-target output).

## [1.0.1] — 2026-09-09

Compatibility audit against `scholarly-agent-suite`'s protocol schemas and
sibling-Skill outputs, per the Suite's cross-repo alignment pass. No change
to the v1.0 discipline/genre/argument content itself.

### Fixed

- `profile_schema.py`'s `CONFIDENCE_LEVELS` used `medium`; both
  `scholarly-corpus-builder`'s actual profile output and the Suite's
  `SCHOLARLY_PROFILE_V1` schema use `moderate`. A real corpus-builder
  profile would have failed this Skill's own confidence validation.
  Corrected the vocabulary in `profile_schema.py` and
  `references/corpus-profile-integration.md`.
- Added the missing `.github/workflows/validate.yml` CI (this repository
  previously had none) running the validator, unit tests, and a packaging
  dry run on every push/PR.

### Added

- `scripts/voice/profile_schema.py`: `from_voice_request_v1()` and
  `to_voice_output_v1()` — an optional, additive translation layer between
  this Skill's own conceptual `VOICE_REQUEST`/`VOICE_OUTPUT` contract and
  the Suite's narrower `VOICE_REQUEST_V1`/`VOICE_OUTPUT_V1` orchestration
  envelopes. This Skill has no hard dependency on the Suite or either
  protocol.
- `audit` added to `OUTPUT_MODES`: a read-only quality-audit pass over
  `input_text`, distinct from the audit step every other mode already runs
  before returning text. Needed because `VOICE_REQUEST_V1`'s `task` enum
  includes `audit` and no existing mode covered "check but don't rewrite."
- 15 new tests covering the confidence-vocabulary fix and both protocol
  adapters (`tests/test_profile_schema.py`).
- `references/integration.md` §Optional scholarly-agent-suite protocol
  compatibility: records the audited state per protocol, including two
  gaps left deliberately open rather than papered over —
  `JOURNAL_STYLE_CONTEXT_V1` (this Skill's `journal_context` expects
  `journal-fit-engine`'s adaptation-target shape, not that protocol's
  official/observed-evidence shape; reconciling this needs a decision made
  alongside `journal-fit-engine`'s still-pending fit-logic implementation)
  and `CONTINUITY_STATE_V1` (`ContinuityLedger` has no serialization yet,
  so it cannot be saved/restored across chapter-drafting sessions as that
  protocol requires).

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
