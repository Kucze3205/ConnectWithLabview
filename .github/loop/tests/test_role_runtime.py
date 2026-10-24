import copy
from datetime import datetime, timezone
import json
import unittest

import fakes
from provider_adapter import Failure
from role_runtime import Runtime, compact
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

    def test_one_megabyte_history_is_cut_to_the_limit_and_recent_actions_stay_whole(self):
        secret = 'FILE-CONTENT-' * 200
        history = [{'candidate': self.candidates[0], 'action': {'tool': 'Read', 'path': 'src/%d.vi' % n, 'text': ''},
                    'outcome': {'text': secret}} for n in range(400)]
        self.assertGreater(len(json.dumps(history)), 1_000_000)
        limits = {'history_bytes': 120_000, 'recent_turns': 12}
        sent = compact(history, limits)
        self.assertLessEqual(len(json.dumps(sent).encode()), 120_000)
        self.assertEqual(sent['recent_turns'], history[-12:])
        self.assertNotIn('FILE-CONTENT', json.dumps(sent['earlier_turns']))
        self.assertEqual(sent['earlier_turns'][-1]['path'], 'src/387.vi')
        self.assertIn('read them again', sent['note'])

    def test_request_prompt_is_compacted_and_its_size_recorded_in_usage(self):
        self.store.update('sessions/11.json', lambda _: {'fingerprint': 'f', 'turns': 30, 'history': [
            {'candidate': self.candidates[0], 'action': {'tool': 'Read', 'path': 'a%d' % n},
             'outcome': {'text': 'BODY%d' % n}} for n in range(30)]})
        prompts = []
        def request(provider, model, credential, prompt, **kwargs):
            prompts.append(prompt)
            return action('Finish', status='done')
        runtime = Runtime(self.owner, self.policy, 'build', self.store, 'sessions/11.json', self.broker,
                          lambda _: {}, self.credentials, 'Read task inputs.', 'fingerprint',
                          model_request=request, clock=self.clock, context={'recent_turns': 3})
        runtime.run(1, 30)
        self.assertIn('BODY29', prompts[0])
        self.assertNotIn('BODY26', prompts[0])
        self.assertIn('"path": "a0"', prompts[0])
        used = self.store.read('sessions/11.json')['requests']['claude/allowed']
        self.assertEqual((used['count'], used['bytes']), (1, len(prompts[0].encode())))

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

    def test_a_park_reports_the_turns_already_taken(self):
        read = action('Read', path='.session/protocol.md')
        def provider(*args, **kwargs):
            if not self.calls:
                self.calls.append(1)
                return read
            raise Failure({'status': 'quota', 'scope': 'provider'})
        self.calls = []
        result = self.runtime(provider).run(10, 30)
        self.assertEqual((result['status'], result['turns']), ('paused', 1))

    def test_interrupted_command_is_never_blindly_replayed(self):
        state = {'fingerprint': 'previous-policy-fingerprint', 'turns': 1, 'history': [],
                 'pending': action('Bash', command='python3 migration.py')}
        self.store.update('sessions/11.json', lambda _: state)
        def request(*args, **kwargs):
            self.assertIn('may have run', args[3])
            return action('Finish', status='partial')
        self.runtime(request).run(2, 30)
        self.assertEqual(self.broker.commands, 0)

    def test_the_same_interrupted_action_is_counted_instead_of_growing_the_continuation(self):
        read = action('Read', path='.session/protocol.md')
        self.store.update('sessions/11.json', lambda _: {'fingerprint': 'f', 'turns': 0, 'history': [], 'pending': read})
        for _ in range(3):
            self.runtime(lambda *args, **kwargs: action('Finish', status='partial')).run(0, 30)
            self.store.update('sessions/11.json', lambda state: dict(state, pending=read))
        history = self.store.read('sessions/11.json')['history']
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]['repeats'], 3)
        self.store.update('sessions/11.json', lambda state: dict(state, pending=action('Glob', pattern='*')))
        self.runtime(lambda *args, **kwargs: action('Finish', status='partial')).run(0, 30)
        self.assertEqual(len(self.store.read('sessions/11.json')['history']), 2)

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
