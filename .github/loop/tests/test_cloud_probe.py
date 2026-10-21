"""Probes must not confuse echoed prompts or burst 429s with usable capacity."""
import json
from datetime import datetime, timezone
import os
from pathlib import Path
import tempfile
from unittest.mock import patch
import unittest

import fakes  # adds the trusted engine module path
from cloud_probe import classify, classify_result, probe


class ClassifyTest(unittest.TestCase):
    def test_real_answers_for_each_wire_format(self):
        self.assertEqual(classify("claude", json.dumps({"type": "result", "result": "CLAUDE_READY", "is_error": False}), 0), "available")
        self.assertEqual(classify("codex", json.dumps({"type": "item.completed", "item": {"type": "agent_message", "text": "CODEX_READY"}}), 0), "available")
        self.assertEqual(classify("copilot", "COPILOT_READY\n", 0), "available")

    def test_echoed_prompt_and_error_are_not_success(self):
        self.assertEqual(classify("codex", json.dumps({"type": "user", "text": "Reply CODEX_READY"}), 0), "unknown")
        self.assertEqual(classify("claude", json.dumps({"type": "result", "result": "CLAUDE_READY", "is_error": True}), 0), "unknown")
        self.assertEqual(classify("copilot", "COPILOT_READY", 1), "unknown")

    def test_transient_throttle_is_not_subscription_exhaustion(self):
        self.assertEqual(classify("claude", "HTTP 429: too many requests", 1), "throttled")
        self.assertEqual(classify("claude", "usage_limit_reached: hit your weekly limit", 1), "quota")
        self.assertEqual(classify("copilot", "authentication failed", 1), "auth_failure")

    def test_model_entitlement_is_distinct_from_bad_credentials(self):
        result = classify_result("codex", "HTTP 403: You do not have access to model example", 1)
        self.assertEqual(result, {"status": "entitlement_failure", "reason": "model_access_denied", "scope": "model"})
        self.assertEqual(classify("codex", "HTTP 401: unauthorized", 1), "auth_failure")
        self.assertEqual(classify_result("copilot", "HTTP 403 forbidden", 1)["reason"], "access_denied_unspecified")
        self.assertEqual(classify("copilot", "HTTP 403 forbidden", 1), "unknown")

    def test_transient_failure_does_not_claim_a_subscription_limit(self):
        for output, status in (("getaddrinfo ENOTFOUND", "network_failure"),
                               ("connection reset", "network_failure"),
                               ("HTTP 503 service unavailable", "service_failure"),
                               ("HTTP 529 overloaded", "service_failure"),
                               ("HTTP 429 rate limit", "throttled")):
            with self.subTest(output=output):
                result = classify_result("claude", output, 1)
                self.assertEqual(result["status"], status)
                self.assertNotIn("retry_after", result)

    def test_model_and_provider_subscription_limits_have_separate_scopes(self):
        self.assertEqual(classify_result("codex", "usage_limit_reached", 1)["scope"], "provider")
        self.assertEqual(classify_result("codex", "model_quota_exceeded", 1)["scope"], "model")

    def test_only_future_numeric_provider_reset_is_preserved(self):
        now = datetime(2026, 10, 18, tzinfo=timezone.utc)
        future = int(now.timestamp()) + 600
        for stamp in (future, future * 1000):
            output = json.dumps({"type": "turn.failed", "error": {"message": "usage_limit_reached", "resets_at": stamp}})
            result = classify_result("codex", output, 1, now)
            self.assertEqual(result["retry_after"], "2026-10-18T00:10:00+00:00")
            self.assertEqual(result["reset_source"], "provider_timestamp")
        for stamp in (int(now.timestamp()) - 1, -1, 10**30, True, "tomorrow"):
            output = json.dumps({"message": "usage_limit_reached", "resetsAt": stamp})
            self.assertNotIn("retry_after", classify_result("claude", output, 1, now))
        # A burst throttle timestamp is not a subscription reset.
        self.assertNotIn("retry_after", classify_result("claude", json.dumps({"message": "HTTP 429", "resetsAt": future}), 1, now))

    def test_summaries_do_not_repeat_untrusted_output_or_credentials(self):
        sentinel = "SYNTHETIC_CREDENTIAL_DO_NOT_PUBLISH"
        result = classify_result("codex", "invalid token " + sentinel, 1)
        self.assertEqual(result["status"], "auth_failure")
        self.assertNotIn(sentinel, json.dumps(result))

    def test_missing_secret_fails_before_starting_cli(self):
        with patch.dict(os.environ, {}, clear=True), patch("cloud_probe.subprocess.Popen") as process:
            result = probe("codex", 5)
        self.assertEqual(result["reason"], "missing_secret")
        self.assertEqual(result["status"], "auth_failure")
        process.assert_not_called()

    def test_corrupt_or_paid_api_bundle_is_not_used_as_subscription_auth(self):
        for text in ("broken-json", "[]", '{"OPENAI_API_KEY":"synthetic-api-key"}'):
            with patch.dict(os.environ, {"CODEX_AUTH_JSON": text}), patch("cloud_probe.subprocess.Popen") as process:
                result = probe("codex", 5)
            self.assertEqual(result["status"], "auth_failure")
            self.assertEqual(result["reason"], "invalid_credential_bundle")
            process.assert_not_called()

    def test_codex_probe_keeps_refresh_file_but_never_receives_store_authority(self):
        import credential_store
        seed = json.dumps({"auth_mode": "chatgpt", "tokens": {
            "id_token": "synthetic-id", "access_token": "synthetic-access", "refresh_token": "synthetic-refresh"}})
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory).resolve() / "credential-home"
            credential_store.restore(home, seed)
            with patch.dict(os.environ, {"GITHUB_TOKEN": "runner-token", "CREDENTIAL_STORE_TOKEN": "store-writer",
                                         "CLAUDE_CODE_OAUTH_TOKEN": "other-provider", "CODEX_AUTH_JSON": "stale-seed"}), \
                 patch("cloud_probe.subprocess.Popen") as process, \
                 patch("cloud_probe.sandbox", side_effect=lambda command, root: command):
                snapshot = {}

                def start(*args, **kwargs):
                    snapshot["auth"] = json.loads(Path(kwargs["env"]["CODEX_HOME"], "auth.json").read_text())
                    return process.return_value

                process.side_effect = start
                child = process.return_value.__enter__.return_value
                child.returncode = 0
                child.communicate.return_value = (json.dumps({"type": "item.completed", "item": {
                    "type": "agent_message", "text": "CODEX_READY"}}), None)
                result = probe("codex", 5, home)
            self.assertEqual(result["status"], "available")
            env = process.call_args.kwargs["env"]
            self.assertNotEqual(env["CODEX_HOME"], str(home))
            self.assertEqual(snapshot["auth"]["auth_mode"], "chatgptAuthTokens")
            self.assertEqual(snapshot["auth"]["tokens"]["refresh_token"], "")
            for secret in ("GITHUB_TOKEN", "CREDENTIAL_STORE_TOKEN", "CODEX_AUTH_JSON", "CLAUDE_CODE_OAUTH_TOKEN"):
                self.assertNotIn(secret, env)
            self.assertTrue(credential_store.auth_file(home).exists())
