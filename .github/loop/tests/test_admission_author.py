import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import executor_boundary  # noqa: E402


class AdmissionAuthorTest(unittest.TestCase):
    """The admitted session commit carries engine.yml `author`; without one it stays `executor`."""

    def admit(self, author):
        root = Path(tempfile.mkdtemp())
        work, trusted = root / "work", root / "trusted"
        for d in (work, trusted):
            executor_boundary.git(str(root), "init", "-q", str(d))
        (work / "a.txt").write_text("base")
        executor_boundary.git(str(work), "add", "a.txt")
        executor_boundary.git(str(work), "commit", "-q", "-m", "base")
        executor_boundary.git(str(trusted), "fetch", "-q", str(work), "HEAD")
        executor_boundary.record(str(work), str(trusted))
        meta = json.loads((trusted / "executor-baseline.json").read_text(encoding="utf-8"))
        (work / "a.txt").write_text("changed")
        sha = executor_boundary.import_candidate(str(work), meta, str(trusted), "refs/heads/task/1", author=author)
        return executor_boundary.git(str(trusted), "log", "-1", "--format=%an <%ae>|%cn", sha).decode().strip()

    def test_configured_author(self):
        self.assertEqual(self.admit({"name": "Owner", "email": "owner@example.test"}),
                         "Owner <owner@example.test>|Owner")

    def test_empty_author_keeps_executor(self):
        self.assertEqual(self.admit({"name": "", "email": ""}), "executor <executor@localhost>|executor")
        self.assertEqual(self.admit(None), "executor <executor@localhost>|executor")


if __name__ == "__main__":
    unittest.main()
