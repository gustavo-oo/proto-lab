"""Version and changelog checks for the proto-lab skill.

``VERSION`` is the machine-readable release marker and ``CHANGELOG.md`` is the
human-readable source of the "what changed" story between releases. These
assertions pin the shape both consumers depend on: a single semver line and a
Keep a Changelog document whose newest heading matches the shipped version.
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

SEMVER = re.compile(r"^\d+\.\d+\.\d+$")

EXPECTED_VERSION = "0.5.0"
EXPECTED_CHANGELOG_HEADING = "## [0.5.0] - 2026-10-28"


class VersionTest(unittest.TestCase):
    def test_version_is_semver_on_a_single_line(self):
        version_path = REPO_ROOT / "VERSION"
        self.assertTrue(
            version_path.is_file(),
            "missing file: VERSION",
        )

        version_text = version_path.read_text(encoding="utf-8")
        self.assertNotIn(
            "\n",
            version_text,
            "VERSION must be a single line with no trailing newline",
        )
        self.assertRegex(version_text, SEMVER)
        self.assertEqual(version_text, EXPECTED_VERSION)

    def test_changelog_follows_keep_a_changelog(self):
        changelog_path = REPO_ROOT / "CHANGELOG.md"
        self.assertTrue(
            changelog_path.is_file(),
            "missing file: CHANGELOG.md",
        )

        changelog_text = changelog_path.read_text(encoding="utf-8")
        self.assertIn("Keep a Changelog", changelog_text)
        self.assertIn(EXPECTED_CHANGELOG_HEADING, changelog_text)
        self.assertIn("### Added", changelog_text)
        self.assertIn("### Changed", changelog_text)

        # 0.5.0 adds fit mode, so the current release carries its own
        # ### Added and ### Changed sections rather than inheriting older
        # headings.
        current = changelog_text.split(EXPECTED_CHANGELOG_HEADING, 1)[1]
        current = current.split("\n## ", 1)[0]
        for section in ("### Added", "### Changed"):
            self.assertIn(
                section,
                current,
                "%s must carry a %s section"
                % (EXPECTED_CHANGELOG_HEADING, section),
            )

    def test_version_matches_changelog_heading(self):
        version_text = (REPO_ROOT / "VERSION").read_text(encoding="utf-8")
        changelog_text = (REPO_ROOT / "CHANGELOG.md").read_text(encoding="utf-8")

        self.assertIn(
            "## [%s]" % version_text,
            changelog_text,
            "CHANGELOG.md must have a heading for the version in VERSION",
        )


if __name__ == "__main__":
    unittest.main()
