"""Install smoke test for the documented roll -> scaffold sequence.

``SKILL.md`` is copied into a skills folder on installation, so the executor's
cwd is the **target project**, not this repository. The pipeline commands are
therefore relative to the skill's own directory (``$SKILL_DIR``) and
``scaffold.py --target`` points at the project's ``prototypes/`` **parent**
directory (the session lands at ``prototypes/<slug>-<seed>/``).

This test copies the installed subset of the skill to a throwaway skills dir,
runs the exact fenced ``bash`` block from ``SKILL.md`` from a clean target, and
asserts the resulting tree. A documentation drift that breaks the copy-pasteable
sequence fails here.
"""

import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "SKILL.md"

SLUG = "task-inbox"
SEED = "cafe-com-leite"
SESSION_NAME = "%s-%s" % (SLUG, SEED)

BASH_BLOCK_RE = re.compile(r"```bash[ \t]*\r?\n(.*?)```", re.DOTALL)

# The installed skill needs exactly the runtime payload: the workflow doc plus
# the scripts, templates and catalogue the scripts read.
INSTALLED_NAMES = ("SKILL.md", "scripts", "assets", "references")


def points_fixture():
    """One point with the three structural options (the default cap)."""
    return {
        "slug": SLUG,
        "points": [
            {
                "id": "d1",
                "question": "Where does the primary action live on the list screen?",
                "why": "The brief is action-first; placement decides the list layout.",
                "axis": "primary-action-placement",
                "options": [
                    {
                        "key": "a",
                        "label": "Sticky header CTA",
                        "descriptor": "One persistent action pinned in the header.",
                    },
                    {
                        "key": "b",
                        "label": "Inline row action",
                        "descriptor": "Each row carries its own primary action.",
                    },
                    {
                        "key": "c",
                        "label": "Floating primary",
                        "descriptor": "A single floating button over the list.",
                    },
                ],
                "screens": ["index", "detail"],
                "status": "pending",
                "chosen": None,
            }
        ],
    }


class SkillInstallSequenceTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.tmp = Path(tmp.name)

        self.skill = self.tmp / "skills" / "proto-lab"
        self.skill.mkdir(parents=True)
        for name in INSTALLED_NAMES:
            source = ROOT / name
            if source.is_dir():
                shutil.copytree(source, self.skill / name)
            else:
                shutil.copyfile(source, self.skill / name)

        self.project = self.tmp / "project"
        self.project.mkdir()

        # The documented block writes both inputs to $WORK before scaffolding.
        self.scratch_tmp = self.tmp / "scratch"
        self.scratch_tmp.mkdir()
        self.work = self.scratch_tmp / ("proto-lab-" + SESSION_NAME)
        self.work.mkdir()
        self.brief = "# Brief\n\nA personal coffee log for home brewing.\n"
        (self.work / "brief.md").write_text(self.brief, encoding="utf-8")
        (self.work / "points.json").write_text(
            json.dumps(points_fixture()) + "\n", encoding="utf-8"
        )

    def documented_block(self):
        self.assertTrue(SKILL.is_file(), "missing %s" % SKILL)
        text = SKILL.read_text(encoding="utf-8")
        for block in BASH_BLOCK_RE.findall(text):
            if "scripts/roll.py" in block and "scripts/scaffold.py" in block:
                return block
        self.fail("SKILL.md has no bash block running roll.py -> scaffold.py")

    def test_documented_sequence_works_from_a_clean_project(self):
        block = self.documented_block()
        script = block.replace("/path/to/proto-lab", str(self.skill))
        script = script.replace("/path/to/project", str(self.project))

        env = dict(os.environ)
        env["TMPDIR"] = str(self.scratch_tmp)
        result = subprocess.run(
            ["bash", "-euo", "pipefail", "-c", script],
            cwd=self.project,
            env=env,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

        session = self.project / "prototypes" / SESSION_NAME
        self.assertTrue(
            session.is_dir(),
            "scaffold --target must be the parent prototypes/ directory",
        )
        self.assertEqual(session.parent, self.project / "prototypes")
        self.assertEqual(
            sorted(path.name for path in session.parent.iterdir()),
            [SESSION_NAME],
        )

        files = {
            str(path.relative_to(session))
            for path in session.rglob("*")
            if path.is_file()
        }
        self.assertEqual(
            sorted(files),
            sorted(
                {
                    "index.html",
                    "direction.json",
                    "brief.md",
                    "points.json",
                    "points/d1-%s.html" % SLUG,
                    "variants/d1-a/index.html",
                    "variants/d1-b/index.html",
                    "variants/d1-c/index.html",
                }
            ),
        )
        directories = {
            str(path.relative_to(session))
            for path in session.rglob("*")
            if path.is_dir()
        }
        self.assertEqual(
            sorted(directories),
            sorted(
                {
                    "points",
                    "variants",
                    "variants/d1-a",
                    "variants/d1-b",
                    "variants/d1-c",
                }
            ),
        )

        # The captured brief survives the scaffold step (copied in after it).
        self.assertEqual(
            (session / "brief.md").read_text(encoding="utf-8"), self.brief
        )
        self.assertEqual(
            json.loads((session / "direction.json").read_text(encoding="utf-8"))["seed"],
            SEED,
        )


if __name__ == "__main__":
    unittest.main()
