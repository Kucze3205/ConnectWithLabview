import copy
import unittest

import fakes
from runtime_store import Store


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
