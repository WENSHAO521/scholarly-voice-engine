import unittest

from scripts.voice import profile_schema as ps


class ClaimTypeTests(unittest.TestCase):
    def test_valid_claim_type(self):
        self.assertEqual(ps.validate_claim_type("mechanistic"), [])

    def test_invalid_claim_type(self):
        errors = ps.validate_claim_type("proven")
        self.assertEqual(len(errors), 1)
        self.assertIn("proven", errors[0])

    def test_none_is_valid(self):
        self.assertEqual(ps.validate_claim_type(None), [])


class ConfidenceTests(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(ps.validate_confidence("high"), [])

    def test_invalid_percentage_rejected(self):
        errors = ps.validate_confidence("73%")
        self.assertEqual(len(errors), 1)


class AuthorProfileTests(unittest.TestCase):
    def test_minimal_valid_profile(self):
        profile = {"profile_type": "author", "source_count": 14}
        self.assertEqual(ps.validate_author_profile(profile), [])

    def test_unknown_field_flagged(self):
        profile = {"profile_type": "author", "made_up_field": True}
        errors = ps.validate_author_profile(profile)
        self.assertTrue(any("made_up_field" in e for e in errors))

    def test_wrong_profile_type_flagged(self):
        profile = {"profile_type": "journal"}
        errors = ps.validate_author_profile(profile)
        self.assertTrue(any("profile_type" in e for e in errors))

    def test_do_not_preserve_must_be_list(self):
        profile = {"profile_type": "author", "do_not_preserve": "citation errors"}
        errors = ps.validate_author_profile(profile)
        self.assertTrue(any("do_not_preserve" in e for e in errors))


class JournalTargetTests(unittest.TestCase):
    def test_compact_shape_valid(self):
        target = {"contribution_position": "earlier", "mechanism_visibility": "higher"}
        self.assertEqual(ps.validate_journal_target(target), [])

    def test_full_shape_valid(self):
        target = {"genre": "empirical_social_science", "theory_density": "medium_high"}
        self.assertEqual(ps.validate_journal_target(target), [])

    def test_unknown_field_flagged(self):
        target = {"contribution_position": "earlier", "acceptance_probability": "93%"}
        errors = ps.validate_journal_target(target)
        self.assertTrue(any("acceptance_probability" in e for e in errors))


class VoiceRequestOutputTests(unittest.TestCase):
    def test_default_request_is_valid(self):
        self.assertEqual(ps.VoiceRequest().validate(), [])

    def test_invalid_editing_mode_flagged(self):
        req = ps.VoiceRequest(editing_mode="full_rewrite")
        errors = req.validate()
        self.assertTrue(any("editing_mode" in e for e in errors))

    def test_request_validates_nested_author_profile(self):
        req = ps.VoiceRequest(author_profile={"profile_type": "journal"})
        errors = req.validate()
        self.assertTrue(any("profile_type" in e for e in errors))

    def test_default_output_is_valid(self):
        self.assertEqual(ps.VoiceOutput(mode="draft").validate(), [])

    def test_invalid_integrity_status_flagged(self):
        out = ps.VoiceOutput(mode="draft", integrity_status="LOOKS_FINE")
        errors = out.validate()
        self.assertTrue(any("integrity_status" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
