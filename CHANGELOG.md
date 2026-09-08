# Changelog

All notable changes to this Skill are documented here.

## [1.0.0] — 2026-09-09

### Added

- Initial standalone release of `scholarly-voice-engine`.
- Compact `SKILL.md` with progressive-loading pointers into `references/` and
  `disciplines/`.
- Eleven cross-cutting reference modules: voice engine, disciplinary matrix, genre
  matrix, argument architectures, human scholarly prose, historical voice profiles,
  era calibration, author voice calibration, article writing, book writing,
  interdisciplinary writing.
- Eleven discipline modules covering natural sciences, mathematics/formal sciences,
  engineering/computing, medicine/health, social sciences, business/management,
  law, humanities, education, arts/design, and interdisciplinary fields — each
  extensible without modifying `SKILL.md`.
- Abstracted historical voice profiles (composite, mechanism-level; no
  characteristic-phrase mimicry or invented quotations) and explicit
  living-author safeguards.
- Monograph continuity model for book-length work (thesis, concepts, terminology,
  claims, chapter roles, recurring examples, cross-references).
- Anti-generic-AI prose rules (transition repetition, over-signposting, uniform
  paragraph symmetry, generic "gap" language, novelty inflation).
- Eval fixtures across discipline, genre, voice, and anti-generic-AI dimensions.
- `scripts/validate_skill.py` for structural validation and light dogfooding
  checks against the Skill's own prose.

### Known limitations

- English-first; non-English rhetorical-structure modules are not yet built
  (language-neutral argument architecture is documented as an interim substitute).
- Historical-profile library is illustrative, not exhaustive, and operates at the
  level of transferable mechanism rather than exhaustive biography.
- Discipline modules describe family-level norms; sub-field and individual-journal
  house styles still require user-supplied specifics.
- No automated stylometric scoring; the validator checks structure and known
  anti-patterns, not prose quality itself.
