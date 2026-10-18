import json
import os
from unittest.mock import patch

import yaml

import fakes
from fakes import common as c, loop
import test_session
from test_session import SessionCase, read


class RoutedSessionTest(SessionCase):
    work = test_session.StageTest.work

    def setUp(self):
        super().setUp()
        owner = {'providers': {'codex': {'models': ['approved-model']}},
                 'backoff': {'initial_seconds': 60, 'max_seconds': 300}}
        cfg = c.load_yaml('engine.yml')
        cfg['provider_pool'] = owner
        self.w.write(self.w.loop, 'engine.yml', yaml.safe_dump(cfg))
        params = c.load_yaml('policy/params.yml')
        params['routing'] = {'tasks': {key: [{'provider': 'codex', 'model': 'approved-model'}]
                                      for key in ('default', 'policymaker', 'review')}}
        self.w.write(self.w.loop, 'policy/params.yml', yaml.safe_dump(params))

    def test_role_and_policymaker_route_and_freeze_model_policy_in_trusted_stage(self):
        for role, labels, task in (('worker', ['route:review'], 'review'), ('policymaker', [], 'policymaker')):
            n = self.issue(role, labels=labels)
            loop.resolve(n)
            options = self.outputs()
            self.assertEqual((options['execution'], options['routing_task']), ('routed', task))
            work, trusted = self.work(), os.path.join(self.w.tmp, 'trusted-' + str(n))
            loop.stage(n, work, trusted)
            staged = json.loads(read(os.path.join(trusted, 'runtime.json')))
            self.assertEqual(staged['fingerprint'], options['profile_digest'])
            self.assertEqual(staged['task'], task)
            self.assertTrue(os.path.isfile(os.path.join(trusted, 'runtime_entry.py')))

    def test_invalid_route_is_refused_before_execution(self):
        n = self.issue(labels=['route:nonexistent'])
        with self.assertRaisesRegex(ValueError, 'no explicit routing'):
            loop.resolve(n)

    def test_watchdog_does_not_make_claude_auth_a_global_dependency(self):
        with patch.object(c, 'probe', side_effect=AssertionError('Claude probe must not run')), \
             patch.object(loop, 'drive', return_value=0) as drive:
            self.assertEqual(loop.watch(), 0)
        drive.assert_called_once()
        self.assertEqual(loop.main(['loop.py', 'probe']), 0)

    def test_durable_wait_does_not_exhaust_the_legacy_three_attempts(self):
        n = self.issue()
        self.hub.issues[n]['created_at'] = '2020-01-01T00:00:00Z'
        self.assertTrue(loop.park(n, c.issue(n), {'attempts': '100'}, {}, 'waiting', None, durable=True))
        self.assertEqual(self.hub.report(n)['status'], 'paused')
        self.assertEqual(self.hub.issues[n]['state'], 'open')
