"""Provider/model routing with fixed clocks and no provider credentials."""
import copy
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import provider_pool as pool


class ProviderPoolTest(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 10, 18, 12, tzinfo=timezone.utc)
        self.owner = {
            "providers": {
                "claude": {"models": ["large", "small"]},
                "codex": {"models": ["coding"]},
                "copilot": {"models": ["review"]},
            },
            "backoff": {"initial_seconds": 60, "max_seconds": 240},
        }
        self.a = {"provider": "claude", "model": "large"}
        self.b = {"provider": "claude", "model": "small"}
        self.c = {"provider": "codex", "model": "coding"}
        self.d = {"provider": "copilot", "model": "review"}
        self.policy = {"tasks": {"build": [self.a, self.c, self.d], "verify": [self.d]}}
        self.state = {}

    def observe(self, candidate, status="available", **kwargs):
        self.state = pool.record_outcome(self.owner, self.state, **candidate, status=status, now=self.now, **kwargs)

    def select(self, task="build", now=None):
        return pool.select_candidate(self.owner, self.policy, self.state, task, now or self.now)

    def test_missing_candidate_requires_probe_and_preserves_inputs(self):
        before = copy.deepcopy((self.owner, self.policy, self.state))
        self.assertEqual(self.select(), {"action": "probe", "candidate": self.a, "scope": "model", "reasons": []})
        self.assertEqual((self.owner, self.policy, self.state), before)

    def test_explicit_task_routing_uses_only_task_candidates(self):
        self.observe(self.a)
        self.observe(self.d)
        self.assertEqual(self.select()["candidate"], self.a)
        self.assertEqual(self.select("verify")["candidate"], self.d)
        with self.assertRaises(ValueError):
            self.select("research")

    def test_owner_catalog_rejects_model_even_on_another_task(self):
        self.policy["tasks"]["verify"] = [{"provider": "copilot", "model": "unapproved"}]
        with self.assertRaisesRegex(ValueError, "owner's allowed"):
            self.select()

    def test_policy_cannot_inject_adapter_options(self):
        self.policy["tasks"]["build"][0] = dict(self.a, command="run-me")
        with self.assertRaises(ValueError):
            self.select()

    def test_model_quota_keeps_other_models_on_same_provider_available(self):
        self.policy["tasks"]["build"] = [self.a, self.b, self.c]
        self.observe(self.a, "quota")
        self.observe(self.b)
        result = self.select()
        self.assertEqual(result["action"], "run")
        self.assertEqual(result["candidate"], self.b)

    def test_provider_quota_blocks_all_its_models(self):
        self.policy["tasks"]["build"] = [self.a, self.b, self.c]
        for candidate in (self.a, self.b, self.c):
            self.observe(candidate)
        self.observe(self.a, "quota", scope="provider")
        result = self.select()
        self.assertEqual(result["action"], "run")
        self.assertEqual(result["candidate"], self.c)

    def test_all_limited_returns_earliest_viable_retry(self):
        for candidate, seconds in ((self.a, 600), (self.c, 300), (self.d, 900)):
            self.observe(candidate, "quota", retry_after=self.now + timedelta(seconds=seconds))
        result = self.select()
        self.assertEqual(result["action"], "wait")
        self.assertEqual(result["retry_after"], "2026-10-18T12:05:00Z")

    def test_candidate_needs_both_provider_and_model_cooldowns_to_expire(self):
        self.policy["tasks"]["build"] = [self.a, self.c]
        self.observe(self.a, "quota", scope="provider", retry_after=self.now + timedelta(seconds=60))
        self.observe(self.a, "quota", retry_after=self.now + timedelta(seconds=600))
        self.observe(self.c, "quota", retry_after=self.now + timedelta(seconds=300))
        self.assertEqual(self.select()["retry_after"], "2026-10-18T12:05:00Z")

    def test_known_reset_requires_probe_then_available_observation(self):
        self.policy["tasks"]["build"] = [self.a]
        self.observe(self.a, "quota")
        self.assertEqual(self.select(now=self.now + timedelta(seconds=59))["action"], "wait")
        self.assertEqual(self.select(now=self.now + timedelta(seconds=60))["action"], "probe")
        self.now += timedelta(seconds=60)
        self.observe(self.a)
        self.assertEqual(self.select()["action"], "run")

    def test_provider_reset_probe_does_not_clear_independent_model_failure(self):
        self.policy["tasks"]["build"] = [self.a]
        self.observe(self.a, "auth_failure")
        self.observe(self.a, "quota", scope="provider")
        self.now += timedelta(seconds=60)
        self.observe(self.a, scope="provider")
        self.assertEqual(self.select()["action"], "blocked")

    def test_expired_provider_quota_uses_provider_probe(self):
        self.observe(self.a)
        self.observe(self.a, "quota", scope="provider")
        result = self.select(now=self.now + timedelta(seconds=60))
        self.assertEqual((result["action"], result["scope"]), ("probe", "provider"))

    def test_auth_failure_remains_closed_beyond_quota_and_time(self):
        self.policy["tasks"]["build"] = [self.a]
        self.observe(self.a, "auth_failure", scope="provider")
        self.assertEqual(self.select(now=self.now + timedelta(days=100))["action"], "blocked")

    def test_auth_failure_falls_back_only_with_explicit_candidate(self):
        self.observe(self.a, "auth_failure")
        self.observe(self.c)
        self.assertEqual(self.select()["candidate"], self.c)
        self.policy["tasks"]["build"] = [self.a]
        self.assertEqual(self.select()["action"], "blocked")

    def test_model_entitlement_is_permanent_and_has_a_distinct_reason(self):
        self.policy['tasks']['build'] = [self.a, self.b]
        self.observe(self.a, 'entitlement_failure')
        self.observe(self.b)
        self.assertEqual(self.select()['candidate'], self.b)
        self.policy['tasks']['build'] = [self.a]
        result = self.select(now=self.now + timedelta(days=30))
        self.assertEqual(result['reason'], 'model_entitlement_required')
        self.assertEqual(result['reasons'][0]['reason'], 'entitlement_failure')

    def test_late_provider_writer_cannot_erase_newer_quota(self):
        self.observe(self.a, 'quota', scope='provider')
        previous = copy.deepcopy(self.state)
        self.state = pool.record_outcome(self.owner, self.state, **self.a, status='available',
                                         scope='provider', now=self.now - timedelta(seconds=1))
        self.assertEqual(self.state, previous)

    def test_auth_blocked_candidate_does_not_supply_meaningless_retry(self):
        self.policy["tasks"]["build"] = [self.a]
        self.observe(self.a, "auth_failure", scope="provider")
        self.observe(self.a, "quota")
        self.assertNotIn("retry_after", self.select())

    def test_unknown_reset_uses_bounded_exponential_backoff(self):
        self.policy["tasks"]["build"] = [self.a]
        for seconds in (60, 120, 240, 240, 240):
            self.observe(self.a, "quota")
            result = self.select()
            self.assertEqual(result["action"], "wait")
            self.assertEqual(pool._time(result["retry_after"]), self.now + timedelta(seconds=seconds))
            self.now += timedelta(seconds=seconds)
            self.assertEqual(self.select()["action"], "probe")

    def test_unknown_probe_result_is_cooled_down(self):
        self.policy["tasks"]["build"] = [self.a]
        self.observe(self.a, "unknown")
        self.assertEqual(self.select()["action"], "wait")
        self.assertEqual(self.select(now=self.now + timedelta(minutes=1))["action"], "probe")

    def test_wall_clock_timezone_offsets_are_normalized(self):
        self.policy["tasks"]["build"] = [self.a]
        self.observe(self.a, "quota", retry_after="2026-10-18T14:01:00+02:00")
        self.assertEqual(self.select()["retry_after"], "2026-10-18T12:01:00Z")
        self.assertEqual(self.select(now="2026-10-18T14:01:00+02:00")["action"], "probe")

    def test_output_and_state_round_trip_as_json(self):
        self.observe(self.a, "quota")
        self.assertEqual(json.loads(json.dumps(self.state)), self.state)
        result = self.select()
        self.assertEqual(json.loads(json.dumps(result)), result)

    def test_record_outcome_does_not_mutate_persisted_state(self):
        before = copy.deepcopy(self.state)
        self.observe(self.a)
        self.assertEqual(before, {})
        original = copy.deepcopy(self.state)
        pool.record_outcome(self.owner, self.state, **self.a, status="quota", now=self.now)
        self.assertEqual(self.state, original)

    def test_malformed_state_fails_closed(self):
        for malformed in (
            [], {"providers": []}, {"models": {"unknown-provider": {}}},
            {"models": {"claude": {"not-allowed": {}}}},
            {"providers": {"claude": {"status": "unexpected"}}},
            {"providers": {"claude": {"status": []}}},
            {"providers": {"claude": {"status": "quota"}}},
            {"providers": {"claude": {"status": "quota", "observed_at": "2026-10-18"}}},
            {"providers": {"claude": {"status": "quota", "observed_at": "2026-10-18T12:00:00Z", "attempts": 0}}},
            {"providers": {"claude": {"status": "quota", "observed_at": "2026-10-18T12:00:00Z", "retry_after": "2026-10-18T11:00:00Z"}}},
            {"providers": {"claude": {"status": "available", "observed_at": "2026-10-18T12:00:00Z", "retry_after": "2026-10-18T12:01:00Z"}}},
        ):
            with self.subTest(state=malformed), self.assertRaises(ValueError):
                pool.select_candidate(self.owner, self.policy, malformed, "build", self.now)

    def test_invalid_backoff_and_naive_clock_rejected(self):
        for backoff in ({"initial_seconds": 0, "max_seconds": 1}, {"initial_seconds": 2, "max_seconds": 1}, {"initial_seconds": True, "max_seconds": 1}):
            with self.subTest(backoff=backoff), self.assertRaises(ValueError):
                pool.select_candidate(dict(self.owner, backoff=backoff), self.policy, {}, "build", self.now)
        with self.assertRaises(ValueError):
            self.select(now=datetime(2026, 10, 18))

    def test_retry_timestamp_must_be_future_and_relevant(self):
        for status, retry in (("quota", self.now), ("available", self.now + timedelta(minutes=1))):
            with self.subTest(status=status), self.assertRaises(ValueError):
                self.observe(self.a, status, retry_after=retry)


if __name__ == "__main__":
    unittest.main()
