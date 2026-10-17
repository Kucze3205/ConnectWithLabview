"""Probes must not confuse echoed prompts or burst 429s with usable capacity."""
import json
import unittest

import fakes  # adds the trusted engine module path
from cloud_probe import classify


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
        self.assertEqual(classify("claude", "HTTP 429: too many requests", 1), "unknown")
        self.assertEqual(classify("claude", "usage_limit_reached: hit your weekly limit", 1), "quota")
        self.assertEqual(classify("copilot", "authentication failed", 1), "auth_failure")
