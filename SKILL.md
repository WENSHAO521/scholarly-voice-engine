---
name: scholarly-voice-engine
description: Apply discipline-aware scholarly voice synthesis, genre-specific argument architecture, human academic prose, and author-style calibration for research articles, reviews, book chapters, monographs, and interdisciplinary academic writing across major fields (sciences, mathematics, engineering, medicine, social science, business, law, humanities, education, arts). Use when writing or rewriting academic/scholarly text, strengthening argument structure, or adapting prose to a discipline's conventions. Do not use for casual, marketing, or non-scholarly writing.
---

# Scholarly Voice Engine

Cross-disciplinary scholarly writing, voice synthesis, and human academic prose.

## What this Skill does

Produces or rewrites scholarly text — articles, reviews, book chapters, monographs,
theoretical/empirical writing — so it reads like a serious human scholar in the
target field, not generic AI academic prose. It calibrates *voice* (how claims are
made, hedged, evidenced, and connected), not just vocabulary.

## Core principle

> Learn transferable scholarly writing mechanisms from intellectual traditions and
> distinguished scholars, then synthesize them into original, discipline-appropriate
> prose. Never imitate a specific living author's style directly, and never
> compromise factual/evidentiary integrity for the sake of voice.

## Operating hierarchy

1. Identify the task (draft vs. rewrite vs. polish).
2. Identify **discipline** — see `references/disciplinary-matrix.md`, then load the
   matching file in `disciplines/`.
3. Identify **genre** (article type, review, chapter, monograph, etc.) — see
   `references/genre-matrix.md`.
4. Identify argument architecture for that discipline × genre — see
   `references/argument-architectures.md`, and `references/article-writing.md` or
   `references/book-writing.md` depending on scale (see Book vs. article routing below).
5. Identify audience/readability level (specialist → educated general reader).
6. Choose a **voice profile** — base + secondary + depth layer — from
   `references/historical-voice-profiles.md` (abstracted, composite profiles, not
   named-author imitation) and calibrate era with `references/era-calibration.md`.
7. If the user supplies their own prior writing, run
   `references/author-voice-calibration.md` and let the author's established voice
   take priority over any historical profile.
8. Apply `references/human-scholarly-prose.md` to avoid generic-AI tics and to give
   prose natural rhythm and controlled asymmetry.
9. Preserve factual/evidentiary integrity at all times (see Integrity, below) —
   this outranks every voice consideration.
10. Draft or rewrite.
11. Run the final audit in `references/human-scholarly-prose.md` §Quality Audit
    before returning the text.

Do not narrate this pipeline to the user; just apply it.

## Book vs. article routing

- Cues like "chapter," "monograph," "book," "Chapter N" → load
  `references/book-writing.md` (and maintain the monograph continuity state it
  describes). Do not also load the full article module.
- Cues like "article," "paper," "manuscript," "journal submission" → load
  `references/article-writing.md`.
- If ambiguous, ask, or infer from context (e.g., stated word count, journal name).

## Discipline modules

Load only the module(s) needed for the current task from `disciplines/`:
`natural-sciences.md`, `mathematics-formal.md`, `engineering-computing.md`,
`medicine-health.md`, `social-sciences.md`, `business-management.md`, `law.md`,
`humanities.md`, `education.md`, `arts-design.md`, `interdisciplinary.md`.
Each specifies claim style, argument structures, evidence norms, citation behavior,
first-person conventions, common failure modes, and recommended voice profiles for
that family. See `references/disciplinary-matrix.md` for the routing table and for
guidance on adding a new discipline without touching this file.

For work spanning more than one discipline, load `references/interdisciplinary-writing.md`
in addition to each home/secondary discipline module — it governs terminology
ownership and evidentiary-standard reconciliation (see §Terminology and integrity).

## Voice profiles

Voice is a multi-dimensional profile (sentence length, claim strength, qualification
density, mechanism focus, historical depth, etc.), never a single label. See
`references/voice-engine.md` for the dimension list and how to combine a
primary/secondary/depth profile into a coherent composite. Historical profiles in
`references/historical-voice-profiles.md` describe transferable *mechanisms*
(sentence architecture, argument architecture, evidence handling) abstracted from
named scholars — never characteristic phrases or quotations to copy.

**Living or contemporary scholars:** never imitate directly. Abstract only
high-level, discipline-general traits (e.g., "mechanism-centered prose,"
"comparative institutional analysis") into a composite profile. If asked to
"write exactly like [living scholar]," comply with the spirit (channel the
requested traits) but produce an original voice, not a stylistic copy.

## Author voice calibration

If the user provides their own prior writing, infer sentence/paragraph length,
first-person use, transition style, claim strength, and concept density from it
(`references/author-voice-calibration.md`). Priority order is: **user's established
voice > disciplinary convention > selected scholarly profile.** Do not copy the
user's errors; do copy their genuine stylistic choices.

## Terminology and integrity

- When a term (e.g., "institution," "resilience," "validity," "robustness") carries
  different meanings across disciplines, name which meaning is intended — see
  `references/interdisciplinary-writing.md`.
- Never fabricate citations, DOIs, page numbers, quotations, authors, or results.
  Where evidence is missing, mark `[VERIFY]` or ask the host/user to supply it.
- Never invent quotations attributed to historical or living scholars.
- Never inflate claim strength (association → causation), novelty, or contribution
  beyond what the material supports.
- When rewriting existing scholarship, never silently alter data, results, causal
  claims, sample, method, legal rule, historical fact, definitions, or theorem
  statements — voice edits are subordinate to epistemic accuracy.
- Do not "humanize" prose by degrading it: no deliberately inserted errors, typos,
  logical gaps, or bad citations. Naturalness comes from genuine intellectual
  variation, not incompetence — see `references/human-scholarly-prose.md`.

## Rewrite modes

Support: light polish, academic polish, voice calibration, deep rewrite, argument
reconstruction, book-prose rewrite, disciplinary conversion. The user's phrasing
determines intervention strength; when unclear, prefer the lighter option and say
what a deeper pass would additionally change.

## Router integration

This Skill is standalone and does not perform model routing. If an adaptive
model-routing skill is active in this environment, let it decide model, reasoning
effort, and delegation; this Skill only controls scholarly genre, argument
architecture, and prose voice.

## Reference index

| File | Loads when you need... |
|---|---|
| `references/voice-engine.md` | The voice-dimension schema and how to compose profiles |
| `references/disciplinary-matrix.md` | Routing to the right discipline module(s) |
| `references/genre-matrix.md` | The genre list and its defining features |
| `references/argument-architectures.md` | Section-by-section argument shapes per genre family |
| `references/human-scholarly-prose.md` | Anti-generic-AI prose rules, rhythm, transitions, final audit |
| `references/historical-voice-profiles.md` | Abstracted historical scholarly profiles and composite voices |
| `references/era-calibration.md` | Adjusting prose for the intellectual era being emulated |
| `references/author-voice-calibration.md` | Inferring and prioritizing the user's own voice |
| `references/article-writing.md` | Article-scale drafting/rewriting |
| `references/book-writing.md` | Book/chapter-scale drafting, monograph continuity state |
| `references/interdisciplinary-writing.md` | Combining disciplines without collision |

See `evals/` for worked test cases and `scripts/validate_skill.py` for structural
validation of this Skill's own files.
