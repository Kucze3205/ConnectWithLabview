import copy
import subprocess
import unittest
from unittest import mock

import fakes
from runtime_store import APIError, GitHubBackend, RETRY_PAUSES_S, Store


class Backend:
    def __init__(self):
        self.files, self.revisions = {}, {}
        self.before_write = None

    def read(self, key):
        return copy.deepcopy(self.files.get(key, {})), self.revisions.get(key)

    def write(self, key, value, expected):
        if self.before_write:
            callback, self.before_write = self.before_write, None
            callback()
        if expected != self.revisions.get(key):
            return False
        self.files[key] = copy.deepcopy(value)
        self.revisions[key] = (self.revisions.get(key) or 0) + 1
        return True


class GitHubBackendRetryTest(unittest.TestCase):
    def run_api(self, *outcomes):
        """Each outcome is an HTTP status, 0 for no response, or None for success. Returns (result or error, calls)."""
        replies = [subprocess.CompletedProcess([], 0, '{"ok": true}', "") if x is None else
                   subprocess.CompletedProcess([], 1, "", "gh: failed (HTTP %s)" % x if x else "connection reset")
                   for x in outcomes]
        with mock.patch("runtime_store.subprocess.run", side_effect=replies) as run, mock.patch("runtime_store.time.sleep") as sleep:
            try:
                result = GitHubBackend("o/r").api("GET", "contents/pool.json")
            except APIError as error:
                result = error
        self.assertEqual(sleep.call_count, run.call_count - 1)
        return result, run.call_count

    def test_a_passing_server_error_is_retried(self):
        self.assertEqual(self.run_api(500, None), ({"ok": True}, 2))

    def test_a_lost_connection_is_retried(self):
        self.assertEqual(self.run_api(0, None), ({"ok": True}, 2))

    def test_a_server_error_that_stays_is_raised_after_every_attempt(self):
        result, calls = self.run_api(*[502] * (len(RETRY_PAUSES_S) + 1))
        self.assertEqual((result.status, calls), (502, len(RETRY_PAUSES_S) + 1))

    def test_a_client_error_is_an_answer_and_is_not_retried(self):
        result, calls = self.run_api(404)
        self.assertEqual((result.status, calls), (404, 1))


class StoreTest(unittest.TestCase):
    def test_competing_provider_observation_is_preserved_after_retry(self):
        backend = Backend()
        first, second = Store(backend), Store(backend)
        backend.before_write = lambda: second.update("pool.json", lambda state: dict(state, copilot="quota"))
        first.update("pool.json", lambda state: dict(state, codex="available"))
        self.assertEqual(first.read("pool.json"), {"copilot": "quota", "codex": "available"})

    def test_session_checkpoints_do_not_share_a_revision_or_overwrite_inputs(self):
        backend = Backend()
        store = Store(backend)
        value = {"history": [{"action": "first"}]}
        store.update("sessions/11.json", lambda _: value)
        value["history"].clear()
        store.update("sessions/12.json", lambda _: {"history": []})
        self.assertEqual(store.read("sessions/11.json"), {"history": [{"action": "first"}]})

    def test_state_paths_cannot_escape_engine_namespace(self):
        for key in ("../engine.yml", "sessions/../../pool.json", "/pool.json", "pool.json?ref=main"):
            with self.subTest(key=key), self.assertRaises(ValueError):
                Store(Backend()).read(key)


if __name__ == "__main__":
    unittest.main()
