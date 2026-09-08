# Scholarly Voice Engine

**Scholarly Voice Engine is a cross-disciplinary Agent Skill for producing
discipline-aware, genre-aware, intellectually structured academic prose.** It
synthesizes transferable scholarly writing patterns from historical intellectual
traditions, modern disciplinary conventions, and an author's own established voice
to support journal articles, reviews, book chapters, monographs, and
interdisciplinary scholarship.

The final output aims to be:

- discipline-appropriate
- intellectually structured
- evidence-aware
- stylistically human
- conceptually precise
- original in voice

rather than simply formal-sounding, verbose, citation-heavy, or "AI-polished."

## Why this exists

Generic AI academic prose tends to collapse "scholarly voice" into formal
vocabulary + long sentences + many citations. Real scholarly voice is about *how
an argument moves*: what claims are made and how strongly, how evidence sits next
to claims, how counterarguments are handled, how concepts are defined and kept
stable, and how paragraphs and sections accumulate intellectual force. This Skill
models scholarly writing at that level, separately for each discipline and genre,
rather than applying one universal "academic style."

## What it is not

- Not a celebrity-imitation engine. Historical figures are modeled as **abstracted,
  transferable mechanisms** (sentence architecture, argument architecture, evidence
  handling), never as characteristic phrases or quotations to copy.
- Not a direct-imitation tool for living scholars. Requests to "write exactly like
  [living author]" are honored only at the level of abstracted high-level traits,
  synthesized into an original voice.
- Not a model router. It assumes something else (the host, or an adaptive routing
  skill) decides model/reasoning/execution policy; this Skill only governs
  scholarly genre, argument architecture, and prose voice.
- Not an AI-detector-evasion tool. The goal is prose that is genuinely well
  constructed, not prose engineered to fool a classifier.

## Repository layout

```text
scholarly-voice-engine/
├── SKILL.md                          # entry point — compact, progressive loading
├── README.md
├── LICENSE
├── CHANGELOG.md
├── agents/
│   └── openai.yaml                   # optional cross-runtime agent descriptor
├── references/
│   ├── voice-engine.md               # voice-dimension schema, composite profiles
│   ├── disciplinary-matrix.md        # discipline routing table
│   ├── genre-matrix.md               # supported genres and their features
│   ├── argument-architectures.md     # section-shape per discipline family
│   ├── human-scholarly-prose.md      # anti-generic-AI rules, rhythm, final audit
│   ├── historical-voice-profiles.md  # abstracted historical scholarly profiles
│   ├── era-calibration.md            # intellectual-era prose calibration
│   ├── author-voice-calibration.md   # inferring/prioritizing the user's own voice
│   ├── article-writing.md            # article-scale architectures
│   ├── book-writing.md               # book/chapter-scale architectures, continuity
│   └── interdisciplinary-writing.md  # combining disciplines without collision
├── disciplines/
│   ├── natural-sciences.md
│   ├── mathematics-formal.md
│   ├── engineering-computing.md
│   ├── medicine-health.md
│   ├── social-sciences.md
│   ├── business-management.md
│   ├── law.md
│   ├── humanities.md
│   ├── education.md
│   ├── arts-design.md
│   └── interdisciplinary.md
├── evals/
│   ├── discipline-cases.jsonl
│   ├── genre-cases.jsonl
│   ├── voice-cases.jsonl
│   └── anti-generic-ai-cases.jsonl
└── scripts/
    └── validate_skill.py
```

## Adding a new discipline

1. Add a row to the routing table in `references/disciplinary-matrix.md`.
2. Add `disciplines/<new-discipline>.md` following the schema at the top of any
   existing discipline file (`discipline_family`, `default_claim_style`,
   `typical_argument_structures`, `typical_evidence`, `citation_behavior`,
   `methods_visibility`, `acceptable_first_person`, `common_failure_modes`,
   `recommended_voice_profiles`, `book_writing_norms`, `article_writing_norms`).
3. Do not edit `SKILL.md` — it loads discipline files by convention, not by an
   enumerated list that needs updating.
4. Add at least 2–3 eval cases to `evals/discipline-cases.jsonl`.

## Integrity guarantees

- No fabricated citations, quotations, data, or results — ever.
- No deliberately inserted errors to seem "more human."
- No claim-strength inflation (e.g., association reworded as causation).
- No novelty/contribution inflation.
- No direct stylistic imitation of living authors.
- Voice edits never silently change data, results, causal claims, legal rules,
  historical facts, or formal definitions/theorems.

## Validating this Skill

```bash
python scripts/validate_skill.py
```

Checks frontmatter validity, that every reference/discipline file referenced from
`SKILL.md` exists, that eval fixtures are well-formed JSONL, and flags common
anti-generic-AI violations inside the Skill's own prose (dogfooding).

## Known limitations

See `CHANGELOG.md` and the "Remaining limitations" note reported alongside this
Skill's build summary — in short: v1 is English-first (language-neutral argument
architecture is documented, but non-English rhetorical-structure modules are not
yet built), the historical-profile library is illustrative rather than exhaustive,
and discipline modules describe norms at the family level rather than every
sub-field or journal's house style.
