"""Credential rotation transactions use a fake secret store and synthetic values."""
import json
import io
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import MagicMock, patch

import fakes
import credential_store as store

SEED = json.dumps({"auth_mode": "chatgpt", "OPENAI_API_KEY": None,
                   "tokens": {"id_token": "fake-id", "access_token": "fake-access", "refresh_token": "fake-refresh"}})


class CredentialStoreTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name).resolve() / "private"
        self.repo, self.token = "owner/repo", "synthetic-store-authority"
        self.saved = SEED

    def writer(self, text, repository, token):
        self.assertEqual((repository, token), (self.repo, self.token))
        self.saved = text

    def test_renewed_bundle_survives_runner_replacement(self):
        store.restore(self.home, SEED)
        store.lease(self.home, self.repo, self.token, "123", self.writer)
        self.assertEqual(json.loads(self.saved), {"state": "leased", "run_id": "123"})
        refreshed = json.loads(SEED)
        refreshed["tokens"]["refresh_token"] = "rotated"
        (self.home / "auth.json").write_text(json.dumps(refreshed), encoding="utf-8")
        store.persist(self.home, self.repo, self.token, self.writer)
        next_home = Path(self.temp.name).resolve() / "next-runner"
        store.restore(next_home, self.saved)
        self.assertEqual(json.loads(store.auth_file(next_home).read_text())["tokens"]["refresh_token"], "rotated")

    def test_interruption_or_write_failure_cannot_restore_a_stale_bundle(self):
        store.restore(self.home, SEED)
        store.lease(self.home, self.repo, self.token, "123", self.writer)
        with self.assertRaises(ValueError):
            store.restore(Path(self.temp.name).resolve() / "interrupted-next", self.saved)

        def unavailable(*args):
            raise RuntimeError("synthetic write failure")

        with self.assertRaises(RuntimeError):
            store.persist(self.home, self.repo, self.token, unavailable)
        self.assertEqual(json.loads(self.saved)["state"], "leased")

    def test_invalid_credentials_never_replace_the_store(self):
        for text in ("[]", "{}", json.dumps({"auth_mode": "apikey", "OPENAI_API_KEY": "paid-key"}),
                     json.dumps({"auth_mode": "chatgpt", "tokens": {"refresh_token": ""}})):
            with self.subTest(text=text), self.assertRaises(ValueError):
                store.restore(self.home, text)
            self.assertEqual(self.saved, SEED)

    def test_restore_names_lease_empty_and_bad_format_without_the_value(self):
        cases = {"credential_leased": json.dumps({"state": "leased", "run_id": "123"}),
                 "credential_empty": "  ",
                 "credential_invalid_format": "synthetic-not-json-secret"}
        for reason, text in cases.items():
            with self.subTest(reason=reason), self.assertRaises(store.NotReady) as error:
                store.restore(self.home, text)
            self.assertEqual(error.exception.reason, reason)
            self.assertNotIn("synthetic-not-json-secret", str(error.exception))
            with patch.dict(os.environ, {"CODEX_AUTH_JSON": text}),                  patch("sys.argv", ["credential_store.py", "restore", "--home", str(self.home)]),                  patch("sys.stdout", new_callable=io.StringIO) as out:
                self.assertEqual(store.main(), 1)
            self.assertEqual(json.loads(out.getvalue())["reason"], reason)
            self.assertNotIn("synthetic-not-json-secret", out.getvalue())

    def test_restore_never_overwrites_an_existing_or_redirected_file(self):
        path = store.restore(self.home, SEED)
        with self.assertRaises(FileExistsError):
            store.restore(self.home, SEED)
        path.unlink()
        if os.name == "nt":
            self.skipTest("symlinks require Windows developer mode; checked on Linux")
        target = Path(self.temp.name) / "outside"
        target.write_text("do not change")
        path.symlink_to(target)
        with self.assertRaises((ValueError, FileExistsError)):
            store.restore(self.home, SEED)
        with self.assertRaises(ValueError):
            store.auth_file(self.home)
        self.assertEqual(target.read_text(), "do not change")

    def test_working_copy_cannot_contain_the_credential_directory(self):
        with patch.dict(os.environ, {"GITHUB_WORKSPACE": self.temp.name}):
            with self.assertRaisesRegex(ValueError, "outside the workspace"):
                store.restore(self.home, SEED)

    @unittest.skipIf(os.name == "nt", "POSIX permissions")
    def test_readable_credential_file_is_rejected(self):
        path = store.restore(self.home, SEED)
        path.chmod(0o644)
        with self.assertRaisesRegex(ValueError, "file must be private"):
            store.persist(self.home, self.repo, self.token, self.writer)

    def test_store_process_receives_no_model_or_runner_credentials(self):
        calls = []

        def run(args, **kwargs):
            calls.append((args, kwargs))
            return subprocess.CompletedProcess(args, 0, "", "")

        with patch.dict(os.environ, {"CODEX_AUTH_JSON": SEED, "GITHUB_TOKEN": "broad-runner-token",
                                    "CLAUDE_CODE_OAUTH_TOKEN": "other-provider"}):
            store.write_secret(SEED, self.repo, self.token, run)
        args, options = calls[0]
        self.assertNotIn(SEED, args)
        self.assertEqual(options["input"], SEED)
        self.assertEqual(options["env"]["GH_TOKEN"], self.token)
        self.assertNotIn("GITHUB_TOKEN", options["env"])
        self.assertNotIn("CODEX_AUTH_JSON", options["env"])
        self.assertNotIn("CLAUDE_CODE_OAUTH_TOKEN", options["env"])
        self.assertIn("--env", args)
        self.assertIn(store.ENVIRONMENT, args)

    def test_storage_errors_do_not_repeat_stderr_or_secret_values(self):
        def run(args, **kwargs):
            return subprocess.CompletedProcess(args, 1, "", SEED + self.token)

        with self.assertRaisesRegex(RuntimeError, "^secret-store write failed$"):
            store.write_secret(SEED, self.repo, self.token, run)

    def test_external_worker_cannot_rotate_the_maintenance_credential(self):
        original = json.loads(SEED)
        worker = store.worker_bundle(original)
        self.assertEqual(worker["auth_mode"], "chatgptAuthTokens")
        self.assertEqual(worker["tokens"]["refresh_token"], "")
        self.assertEqual(original["tokens"]["refresh_token"], "fake-refresh")
        self.assertEqual(worker["tokens"]["access_token"], original["tokens"]["access_token"])

    def test_execution_store_receives_only_access_tokens(self):
        store.restore(self.home, SEED)
        calls = []
        store.publish_worker(self.home, self.repo, self.token, lambda *args, **kw: calls.append((args, kw)))
        args, options = calls[0]
        value = json.loads(args[0])
        self.assertEqual(value['auth_mode'], 'chatgptAuthTokens')
        self.assertEqual(value['tokens']['refresh_token'], '')
        self.assertEqual(options, {'environment': 'provider-claude', 'secret': 'CODEX_WORKER_AUTH_JSON'})
        with self.assertRaises(ValueError):
            store.write_secret(SEED, self.repo, self.token, environment='arbitrary')

    def test_refresh_uses_account_rpc_without_model_prompt_or_store_authority(self):
        path = store.restore(self.home, SEED)
        server = MagicMock()
        server.__enter__.return_value = server
        server.stdout = io.StringIO('{"id":1,"result":{}}\n{"id":2,"result":{"account":{"type":"chatgpt"}}}\n')
        server.stdin = io.StringIO()

        def start(args, **kwargs):
            self.assertEqual(args[:3], ["codex", "app-server", "--stdio"])
            self.assertNotIn("CREDENTIAL_STORE_TOKEN", kwargs["env"])
            self.assertNotIn("GITHUB_TOKEN", kwargs["env"])
            renewed = json.loads(SEED)
            renewed["tokens"]["refresh_token"] = "renewed-by-codex"
            path.write_text(json.dumps(renewed))
            return server

        with patch.dict(os.environ, {"CREDENTIAL_STORE_TOKEN": "synthetic-writer", "GITHUB_TOKEN": "runner"}), \
             patch("credential_store.subprocess.Popen", side_effect=start):
            store.refresh(self.home, timeout=5)
        messages = [json.loads(line) for line in server.stdin.getvalue().splitlines()]
        self.assertEqual([m["method"] for m in messages], ["initialize", "initialized", "account/read"])
        self.assertEqual(messages[-1]["params"], {"refreshToken": True})

    def test_unchanged_or_rejected_refresh_is_not_accepted_as_renewal(self):
        store.restore(self.home, SEED)
        for reply in ({"result": {"account": {"type": "chatgpt"}}}, {"error": {"message": SEED}}):
            server = MagicMock()
            server.__enter__.return_value = server
            server.stdout = io.StringIO(json.dumps({"id": 1, "result": {}}) + "\n" +
                                        json.dumps(dict(reply, id=2)) + "\n")
            server.stdin = io.StringIO()
            with patch("credential_store.subprocess.Popen", return_value=server):
                with self.assertRaises(RuntimeError) as error:
                    store.refresh(self.home, timeout=5)
            self.assertNotIn(SEED, str(error.exception))


if __name__ == "__main__":
    unittest.main()
