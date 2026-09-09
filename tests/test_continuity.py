import unittest

from scripts.voice.continuity import ContinuityConflict, ContinuityLedger


class ConceptLedgerTests(unittest.TestCase):
    def setUp(self):
        self.ledger = ContinuityLedger()

    def test_same_definition_repeated_is_fine(self):
        self.ledger.add_concept("resilience", "capacity to absorb shock", chapter=2)
        self.ledger.add_concept("resilience", "capacity to absorb shock", chapter=6)
        self.assertEqual(self.ledger.concepts["resilience"].chapter, 6)

    def test_silent_redefinition_raises(self):
        self.ledger.add_concept("resilience", "capacity to absorb shock", chapter=2)
        with self.assertRaises(ContinuityConflict):
            self.ledger.add_concept("resilience", "tendency to return to equilibrium", chapter=6)

    def test_explicit_refinement_is_allowed(self):
        self.ledger.add_concept("resilience", "capacity to absorb shock", chapter=2)
        self.ledger.add_concept(
            "resilience", "capacity to absorb shock without losing core function",
            chapter=6, refinement=True,
        )
        self.assertIn("without losing core function", self.ledger.concepts["resilience"].definition)


class ClaimLedgerTests(unittest.TestCase):
    def setUp(self):
        self.ledger = ContinuityLedger()

    def test_consistent_claim_repeated_is_fine(self):
        self.ledger.add_claim("mechanism_x_operative", "supported", chapter=3)
        self.ledger.add_claim("mechanism_x_operative", "supported", chapter=7)
        self.assertEqual(self.ledger.claims["mechanism_x_operative"].chapter, 7)

    def test_silent_contradiction_raises(self):
        self.ledger.add_claim("mechanism_x_operative", "supported", chapter=3)
        with self.assertRaises(ContinuityConflict):
            self.ledger.add_claim("mechanism_x_operative", "rejected", chapter=7)

    def test_explicit_refinement_of_a_claim_is_allowed(self):
        self.ledger.add_claim("mechanism_x_operative", "supported", chapter=3)
        self.ledger.add_claim(
            "mechanism_x_operative", "supported only under low state capacity",
            chapter=7, refinement=True,
        )
        self.assertEqual(
            self.ledger.claims["mechanism_x_operative"].stance,
            "supported only under low state capacity",
        )


class TerminologyAuditTests(unittest.TestCase):
    def test_variant_terms_flagged(self):
        ledger = ContinuityLedger()
        variants = ledger.check_term_variants("resilience", ["resilience", "Resilience", "robustness"])
        self.assertEqual(variants, ["Resilience", "robustness"])

    def test_no_variants_returns_empty(self):
        ledger = ContinuityLedger()
        self.assertEqual(ledger.check_term_variants("resilience", ["resilience", "resilience"]), [])


if __name__ == "__main__":
    unittest.main()
