"""Repository bootstrap checks for the proto-lab skill.

These assertions guard the skeleton every consumer of the repository relies
on: the skill directories, the MIT license and the ignore rules. If any of
them disappears, the repository is no longer installable as a skill.
"""

import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

EXPECTED_DIRECTORIES = (
    "references",
    "scripts",
    "assets",
    "examples",
    "tests",
)

EXPECTED_FILES = (
    "LICENSE",
    ".gitignore",
)


class RepoBootstrapTest(unittest.TestCase):
    def test_repository_skeleton_is_present(self):
        missing_directories = sorted(
            name for name in EXPECTED_DIRECTORIES if not (REPO_ROOT / name).is_dir()
        )
        self.assertEqual(
            missing_directories,
            [],
            "missing directories: %s" % ", ".join(missing_directories),
        )

        missing_files = sorted(
            name for name in EXPECTED_FILES if not (REPO_ROOT / name).is_file()
        )
        self.assertEqual(
            missing_files,
            [],
            "missing files: %s" % ", ".join(missing_files),
        )

        license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
        self.assertIn("MIT License", license_text)
        self.assertIn("Copyright (c) 2026 Gustavo", license_text)


if __name__ == "__main__":
    unittest.main()
