"""A small, heuristic continuity ledger for long-form (book/monograph) work,
operationalizing references/continuity-ledger.md's concept and claim
ledgers. Not NLP — it catches exact-key redefinition and direct stance
contradiction, which is most of what actually goes wrong across chapters
drafted in separate passes.
"""
from __future__ import annotations

from dataclasses import dataclass


class ContinuityConflict(Exception):
    """Raised when a concept is redefined or a claim is contradicted without
    being explicitly marked as a refinement."""


@dataclass
class ConceptEntry:
    definition: str
    chapter: int


@dataclass
class ClaimEntry:
    stance: str
    chapter: int


class ContinuityLedger:
    def __init__(self) -> None:
        self.concepts: dict[str, ConceptEntry] = {}
        self.claims: dict[str, ClaimEntry] = {}

    def add_concept(self, term: str, definition: str, chapter: int, *, refinement: bool = False) -> None:
        """Record a concept's definition. Raises ContinuityConflict if the
        term was previously defined differently and this isn't marked as a
        deliberate refinement (see continuity-ledger.md §Concept ledger).
        """
        existing = self.concepts.get(term)
        if existing is not None and existing.definition != definition and not refinement:
            raise ContinuityConflict(
                f"term {term!r} redefined in chapter {chapter} "
                f"(chapter {existing.chapter} defined it as {existing.definition!r}, "
                f"chapter {chapter} defines it as {definition!r})"
            )
        self.concepts[term] = ConceptEntry(definition, chapter)

    def add_claim(self, claim_key: str, stance: str, chapter: int, *, refinement: bool = False) -> None:
        """Record a claim's stance (e.g. "supported", "rejected", or any
        short label meaningful to the caller). Raises ContinuityConflict on
        a direct contradiction not marked as a refinement (see
        continuity-ledger.md §Claim ledger).
        """
        existing = self.claims.get(claim_key)
        if existing is not None and existing.stance != stance and not refinement:
            raise ContinuityConflict(
                f"claim {claim_key!r} contradicted in chapter {chapter} "
                f"(chapter {existing.chapter} stated {existing.stance!r}, "
                f"chapter {chapter} states {stance!r})"
            )
        self.claims[claim_key] = ClaimEntry(stance, chapter)

    def check_term_variants(self, canonical: str, seen_terms: list[str]) -> list[str]:
        """Return any terms in seen_terms that are not the canonical term
        registered for a concept — a lightweight terminology-drift check
        (continuity-ledger.md §Terminology audit). Case-sensitive by design:
        capitalization drift is itself a flagged pattern.
        """
        return [t for t in seen_terms if t != canonical]
