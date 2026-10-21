import copy
from datetime import datetime, timezone
import json
import unittest

import fakes
from provider_adapter import Failure
from role_runtime import Runtime
from runtime_store import Store
from test_runtime_store import Backend
from test_tool_broker import action


class Broker:
    def __init__(self):
        self.files, self.commands = {}, 0

    def execute(self, item, timeout=60):
        if item['tool'] == 'Write':
            self.files[item['path']] = item['text']
        if item['tool'] == 'Bash':
            self.commands += 1
        return {'status': item['status']} if item['tool'] == 'Finish' else {'ok': True}


class RuntimeTest(unittest.TestCase):
    def setUp(self):
        self.backend, self.broker = Backend(), Broker()
        self.store = Store(self.backend)
        self.owner = {'providers': {p: {'models': ['allowed']} for p in ('claude', 'codex', 'copilot')},
                      'backoff': {'initial_seconds': 60, 'max_seconds': 240}}
        self.candidates = [{'provider': p, 'model': 'allowed'} for p in self.owner['providers']]
        self.policy = {'tasks': {'build': self.candidates, 'policymaker': list(reversed(self.candidates))}}
        self.credentials = {p: 'synthetic-' + p for p in self.owner['providers']}
        self.clock = lambda: datetime(2026, 10, 18, 12, tzinfo=timezone.utc)

    def runtime(self, request, task='build', checkpoint=None):
        return Runtime(self.owner, self.policy, task, self.store, 'sessions/11.json', self.broker,
                       checkpoint or (lambda _: {'head': 'durable-head'}), self.credentials,
                       'Read task inputs.', 'fingerprint', model_request=request, clock=self.clock)

    def test_quota_switch_preserves_accepted_work_and_policymaker_uses_its_policy(self):
        calls = []
        def request(provider, model, credential, prompt, **kwargs):
            calls.append(provider)
            if len(calls) == 1:
                return action('Write', path='src/result', text='accepted')
            if provider == 'claude':
                raise Failure({'status': 'quota', 'scope': 'provider'})
            self.assertIn('accepted', prompt)
            self.assertEqual(self.broker.files['src/result'], 'accepted')
            return action('Finish', status='done')
        result = self.runtime(request).run(10, 30)
        self.assertEqual(result['status'], 'done')
        self.assertEqual(calls, ['claude', 'claude', 'codex'])
        self.assertEqual(self.store.read('sessions/11.json')['head'], 'durable-head')
        calls.clear()
        result = self.runtime(lambda p, *a, **kw: (calls.append(p) or action('Finish', status='done')),
                              task='policymaker').run(2, 30)
        self.assertEqual(calls, ['copilot'])

    def test_all_unavailable_parks_without_losing_checkpoint_and_restarts_on_new_runner(self):
        def quota(*args, **kwargs):
            raise Failure({'status': 'quota', 'scope': 'provider'})
        result = self.runtime(quota).run(10, 30)
        self.assertEqual(result['status'], 'paused')
        self.assertEqual(result['retry_after'], '2026-10-18T12:01:00Z')
        # New Runtime instance, same durable backend, now beyond retry.
        self.clock = lambda: datetime(2026, 10, 18, 12, 2, tzinfo=timezone.utc)
        result = self.runtime(lambda *args, **kwargs: action('Finish', status='done')).run(2, 30)
        self.assertEqual(result['status'], 'done')

    def test_interrupted_command_is_never_blindly_replayed(self):
        state = {'fingerprint': 'previous-policy-fingerprint', 'turns': 1, 'history': [],
                 'pending': action('Bash', command='python3 migration.py')}
        self.store.update('sessions/11.json', lambda _: state)
        def request(*args, **kwargs):
            self.assertIn('may have run', args[3])
            return action('Finish', status='partial')
        self.runtime(request).run(2, 30)
        self.assertEqual(self.broker.commands, 0)

    def test_failure_to_checkpoint_stops_before_another_action(self):
        calls = []
        def checkpoint(_):
            raise RuntimeError('synthetic persistent store failure')
        def request(*args, **kwargs):
            calls.append(1)
            return action('Write', path='src/file', text='pending')
        with self.assertRaises(RuntimeError):
            self.runtime(request, checkpoint=checkpoint).run(10, 30)
        self.assertEqual(len(calls), 1)
        self.assertIn('pending', self.store.read('sessions/11.json'))

    def test_new_authentication_retries_auth_failure_but_keeps_quota(self):
        self.runtime(lambda *a, **kw: action('Finish', status='done')).availability()
        runtime = self.runtime(None)
        runtime.observe(self.candidates[0], {'status': 'auth_failure', 'scope': 'provider'}, self.clock())
        runtime.observe(self.candidates[1], {'status': 'quota', 'scope': 'provider'}, self.clock())
        self.credentials['claude'] = 'replacement-auth'
        state = self.runtime(None).availability()
        self.assertNotIn('claude', state['providers'])
        self.assertEqual(state['providers']['codex']['status'], 'quota')

    def test_revoked_authentication_and_temporary_transport_failure_fall_back(self):
        for status in ('auth_failure', 'network_failure', 'service_failure', 'throttled', 'credential_expired'):
            with self.subTest(status=status):
                self.backend.files.clear()
                self.backend.revisions.clear()
                def request(provider, *args, **kwargs):
                    if provider == 'claude':
                        raise Failure({'status': status, 'scope': 'provider'})
                    return action('Finish', status='done')
                result = self.runtime(request).run(5, 30)
                self.assertEqual(result['candidate']['provider'], 'codex')

    def test_owner_catalog_reduction_preserves_remaining_provider_quota(self):
        runtime = self.runtime(None)
        for candidate in self.candidates:
            runtime.observe(candidate, {'status': 'quota', 'scope': 'provider'}, self.clock())
        self.owner['providers'].pop('copilot')
        state = runtime.availability()
        self.assertNotIn('copilot', state['providers'])
        self.assertEqual(state['providers']['codex']['status'], 'quota')

    def test_observed_usage_survives_provider_handoff(self):
        calls = []
        def request(provider, *args, **kwargs):
            calls.append(provider)
            kwargs['metadata']['usage'] = {'in': 10, 'out': 2, 'cache_read': 3, 'cache_write': 0}
            if provider == 'claude':
                raise Failure({'status': 'quota', 'scope': 'provider'})
            return action('Finish', status='done')
        result = self.runtime(request).run(5, 30)
        self.assertEqual(result['usage']['claude/allowed']['in'], 10)
        self.assertEqual(result['usage']['codex/allowed']['out'], 2)
