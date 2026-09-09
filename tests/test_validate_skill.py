import importlib.util
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT_PATH = REPO_ROOT / "scripts" / "validate_skill.py"


def _load_validate_skill():
    spec = importlib.util.spec_from_file_location("validate_skill", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ValidateSkillIntegrationTests(unittest.TestCase):
    """Runs the real validator against the actual repository — this is the
    end-to-end check that everything documented in SKILL.md/README.md
    actually exists and is internally consistent."""

    def setUp(self):
        self.module = _load_validate_skill()

    def test_full_validation_passes_on_the_real_repo(self):
        self.module.errors.clear()
        self.module.warnings.clear()
        exit_code = self.module.main()
        self.assertEqual(
            exit_code, 0,
            msg=f"validator failed with errors: {self.module.errors}",
        )


class VersionCheckUnitTests(unittest.TestCase):
    """Exercises check_version()'s failure paths directly, without needing a
    second on-disk fixture repo (see README §Running tests)."""

    def setUp(self):
        self.module = _load_validate_skill()
        self.module.errors.clear()
        self.module.warnings.clear()

    def test_mismatched_version_is_a_failure(self):
        real_root = self.module.ROOT
        try:
            # Point at a scratch layout whose VERSION deliberately disagrees
            # with CHANGELOG.md's latest heading.
            import tempfile

            with tempfile.TemporaryDirectory() as tmp:
                tmp_path = Path(tmp)
                (tmp_path / "VERSION").write_text("9.9.9\n", encoding="utf-8")
                (tmp_path / "CHANGELOG.md").write_text(
                    "# Changelog\n\n## [1.0.0] - 2026-09-09\n\nstuff\n",
                    encoding="utf-8",
                )
                self.module.ROOT = tmp_path
                self.module.check_version()
                self.assertTrue(
                    any("does not match" in e for e in self.module.errors)
                )
        finally:
            self.module.ROOT = real_root

    def test_matching_version_passes(self):
        real_root = self.module.ROOT
        try:
            import tempfile

            with tempfile.TemporaryDirectory() as tmp:
                tmp_path = Path(tmp)
                (tmp_path / "VERSION").write_text("1.0.0\n", encoding="utf-8")
                (tmp_path / "CHANGELOG.md").write_text(
                    "# Changelog\n\n## [1.0.0] - 2026-09-09\n\nstuff\n",
                    encoding="utf-8",
                )
                self.module.ROOT = tmp_path
                self.module.check_version()
                self.assertEqual(self.module.errors, [])
        finally:
            self.module.ROOT = real_root


if __name__ == "__main__":
    unittest.main()
