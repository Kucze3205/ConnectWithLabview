#!/usr/bin/env python3
"""The writes the loop's state depends on, against the `gh` command line and not the fake hub."""
import subprocess
import tempfile
import unittest
from unittest import mock

import fakes  # noqa: F401  (puts the engine on the path)
import common as c


def done(code=0, err=""):
    return subprocess.CompletedProcess([], code, stdout="", stderr=err)


class IssueWritesTest(unittest.TestCase):
    def setUp(self):
        for patcher in (mock.patch.object(c.time, "sleep"), mock.patch.object(c, "say"), mock.patch.object(c, "ensure_label")):
            patcher.start()
            self.addCleanup(patcher.stop)

    def issue_with(self, *labels):
        return mock.patch.object(c, "issue", return_value={"labels": [{"name": x} for x in labels]})

    def test_labels_the_issue_does_not_have_are_not_asked_for(self):
        """`gh issue edit` refuses the whole edit when one label is missing from the repository."""
        with self.issue_with("awaiting:owner", "role:benchmark"), mock.patch.object(c.subprocess, "run", return_value=done()) as run:
            c.edit_labels(150, remove=["conflict", "awaiting:owner", "awaiting:verifier"])
        self.assertEqual(run.call_args.args[0], ["gh", "issue", "edit", "150", "--remove-label", "awaiting:owner"])

    def test_nothing_to_remove_is_no_call(self):
        with self.issue_with("role:benchmark"), mock.patch.object(c.subprocess, "run") as run:
            c.edit_labels(150, remove=["conflict"])
        run.assert_not_called()

    def test_adding_a_label_does_not_read_the_issue(self):
        with mock.patch.object(c, "issue") as read, mock.patch.object(c.subprocess, "run", return_value=done()) as run:
            c.edit_labels(150, add=["awaiting:owner"])
        read.assert_not_called()
        self.assertEqual(run.call_args.args[0], ["gh", "issue", "edit", "150", "--add-label", "awaiting:owner"])

    def test_a_label_edit_that_keeps_failing_is_reported_and_does_not_stop_the_run(self):
        with self.issue_with("awaiting:owner"), mock.patch.object(c.subprocess, "run", return_value=done(1, "HTTP 502")) as run:
            c.edit_labels(150, remove=["awaiting:owner"])
        self.assertGreater(run.call_count, 1)
        self.assertIn("HTTP 502", c.say.call_args.args[0])

    def test_a_close_survives_a_passing_failure(self):
        with mock.patch.object(c.subprocess, "run", side_effect=[done(1, "HTTP 502"), done()]) as run:
            c.close_issue(150)
        self.assertEqual(run.call_count, 2)
        self.assertEqual(run.call_args.args[0], ["gh", "issue", "close", "150", "--reason", "completed"])

    def test_a_close_that_keeps_failing_stops_the_run(self):
        """An issue left open reads as work in progress: the loop would wait for it in silence."""
        with mock.patch.object(c.subprocess, "run", return_value=done(1, "HTTP 502")):
            with self.assertRaisesRegex(SystemExit, "HTTP 502"):
                c.close_issue(150)

    def test_a_dispatch_survives_a_passing_failure(self):
        """Iteration 14: one HTTP 500 on a dispatch cost the iteration and the policy of the session before it."""
        with mock.patch.object(c.subprocess, "run", side_effect=[done(1, "HTTP 500"), done()]) as run:
            self.assertTrue(c.workflow_run("tokenless.yml", key="k"))
        self.assertEqual(run.call_count, 2)
        self.assertEqual(run.call_args.args[0], ["gh", "workflow", "run", "tokenless.yml", "-f", "key=k"])

    def test_a_dispatch_that_keeps_failing_is_refused(self):
        with mock.patch.object(c.subprocess, "run", return_value=done(1, "HTTP 500")):
            self.assertFalse(c.workflow_run("tokenless.yml", key="k"))

    def test_a_dispatch_that_keeps_failing_is_not_a_launch(self):
        """A launch nobody started must not read as a commitment: the kicks that follow count, and end in an outage."""
        i = {"state": "open", "labels": [{"name": "role:worker"}, {"name": "loop:iteration 1"}]}
        with mock.patch.object(c, "guard_ok", return_value=True), mock.patch.object(c, "issue", return_value=i), \
                mock.patch.object(c, "is_unblocked", return_value=True), mock.patch.object(c, "session_runs", return_value=[]), \
                mock.patch.object(c, "workflow_run", return_value=False), mock.patch.object(c, "LAUNCHED", set()):
            self.assertFalse(c.launch(150))
            self.assertEqual(c.LAUNCHED, set())
        self.assertIn("#150", c.say.call_args.args[0])

    def test_a_command_whose_job_left_nothing_is_told_from_a_failed_command(self):
        with mock.patch.object(c, "run_tokenless", return_value=None):
            r = c.run_command("true", tempfile.mkdtemp())
        self.assertEqual(r.returncode, c.NO_RESULT)

    def tokenless(self, *download):
        run = [{"displayTitle": "tokenless #abc", "status": "completed", "databaseId": 7}]
        with mock.patch.object(c, "git"), mock.patch.object(c, "workflow_run", return_value=True),                 mock.patch.object(c, "run_list", return_value=run), mock.patch.object(c.uuid, "uuid4", return_value=mock.Mock(hex="abc")),                 mock.patch.object(c.shutil, "make_archive"), mock.patch.object(c.subprocess, "run", side_effect=download) as gh:
            return c.run_tokenless(tempfile.mkdtemp(), 1), gh

    def test_a_result_download_survives_a_passing_failure(self):
        out, gh = self.tokenless(done(1, "HTTP 502"), done())
        self.assertTrue(out)
        self.assertEqual(gh.call_count, 2)

    def test_a_result_that_cannot_be_downloaded_is_no_result(self):
        out, _ = self.tokenless(*[done(1, "HTTP 502")] * 3)
        self.assertIsNone(out)


if __name__ == "__main__":
    unittest.main()
