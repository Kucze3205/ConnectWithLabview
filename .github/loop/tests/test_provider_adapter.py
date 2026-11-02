import json
from contextlib import contextmanager
import os
from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch

import fakes
import provider_adapter as adapter
from tool_broker import FIELDS


class FakeRPC:
    def __init__(self, *args, **kwargs):
        self.calls = []
        self.notifications = []

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def call(self, method, params):
        self.calls.append((method, params))
        if method == 'connect':
            return {'rpc_error': {'code': -32603, 'message': 'unknown handshake'}}
        if method == 'models.list':
            return {'models': [{'id': 'live-copilot-id'}]}
        if method == 'model/list':
            return {'data': [{'id': 'catalog-id', 'model': 'execution-id', 'isDefault': True}]}
        return {}

    def send(self, *args):
        pass


class AdapterTest(unittest.TestCase):
    def test_codex_usage_keeps_latest_total_and_rejects_native_actions(self):
        rpc = FakeRPC()
        rpc.call = lambda method, params: {'thread': {'id': 'thread'}} if method == 'thread/start' else {}
        action = {field: '' for field in FIELDS}
        action.update(tool='Finish', status='done')
        rpc.notifications = [
            {'method': 'thread/tokenUsage/updated', 'params': {'tokenUsage': {'total': {'inputTokens': 3}}}},
            {'method': 'thread/tokenUsage/updated', 'params': {'tokenUsage': {'total': {
                'inputTokens': 10, 'outputTokens': 2, 'cachedInputTokens': 4}}}},
            {'method': 'item/completed', 'params': {'item': {'type': 'agentMessage', 'text': json.dumps(action)}}},
            {'method': 'turn/completed', 'params': {'turn': {'status': 'completed'}}}]
        @contextmanager
        def isolated(*args):
            yield Path('.'), {}, rpc
        metadata = {}
        with patch.object(adapter, 'isolated', isolated):
            self.assertEqual(adapter.request('codex', 'model', 'access-only', 'task', metadata=metadata), action)
            self.assertEqual(metadata['usage'], {'in': 10, 'out': 2, 'cache_read': 4, 'cache_write': 0})
            rpc.notifications = [{'method': 'item/started', 'params': {'item': {'type': 'commandExecution'}}}]
            with self.assertRaises(adapter.Failure) as error:
                adapter.request('codex', 'model', 'access-only', 'task')
            self.assertEqual(error.exception.observation['reason'], 'native_request_denied')

    def claude_request(self, stdout=None, **kwargs):
        action = {field: '' for field in FIELDS}
        action.update(tool='Finish', status='done')
        seen = {}
        def run(command, **options):
            seen.update(command=command, **options)
            if '--append-system-prompt-file' in command:
                seen['system'] = Path(command[command.index('--append-system-prompt-file') + 1]).read_text(encoding='utf-8')
            seen['cwd'] = str(options['cwd'])
            output = stdout if stdout is not None else '\n'.join(json.dumps(event) for event in (
                {'type': 'system', 'subtype': 'init', 'tools': []},
                {'type': 'result', 'structured_output': action, 'usage': {}}))
            return subprocess.CompletedProcess(command, 0, output, '')
        with patch.object(adapter.subprocess, 'run', run):
            return adapter.request('claude', 'model', 'token', 'whole prompt', **kwargs), seen, action

    def test_claude_prompt_goes_through_stdin_so_a_long_continuation_cannot_overflow_argv(self):
        result, seen, action = self.claude_request()
        self.assertEqual(result, action)
        self.assertEqual(json.loads(seen['input'])['message']['content'], [{'type': 'text', 'text': 'whole prompt'}])
        self.assertNotIn('--append-system-prompt-file', seen['command'])
        long = 'x' * 300_000                        # one argv entry is limited to 128 KiB
        _, seen, _ = self.claude_request(layout=(long, ['y' * 300_000]))
        self.assertEqual(seen['system'], long)
        self.assertTrue(all(len(part) < 100_000 for part in seen['command']))

    def test_claude_layout_sends_stable_text_as_system_and_each_block_separately(self):
        _, seen, _ = self.claude_request(layout=('role and schema', ['intro', 'turn 1', 'turn 2 ż']))
        self.assertEqual(seen['system'], 'role and schema')
        message = json.loads(seen['input'])
        self.assertEqual((message['type'], message['message']['role']), ('user', 'user'))
        self.assertEqual([block['text'] for block in message['message']['content']], ['intro', 'turn 1', 'turn 2 ż'])
        for flag in ('--no-session-persistence', '--setting-sources', '--tools'):
            self.assertIn(flag, seen['command'])
        self.assertEqual(seen['command'][seen['command'].index('--tools') + 1], '')

    def test_claude_requests_share_a_working_directory_and_leave_nothing_in_it(self):
        # The CLI writes this path into its system prompt, in front of everything the cache should read.
        _, first, _ = self.claude_request(layout=('s', ['b']))
        self.assertEqual(os.listdir(first['cwd']), [])
        _, second, _ = self.claude_request(layout=('s', ['b']))
        self.assertEqual(first['cwd'], second['cwd'])

    def test_claude_output_without_a_result_event_is_a_failure_that_ignores_stream_events(self):
        with self.assertRaises(adapter.Failure) as error:
            self.claude_request(stdout='{"type": "system", "subtype": "init", "tools": ["token"]}\nnot json error\n')
        self.assertEqual(error.exception.observation['diagnostic_terms'], ['error', 'not'])

    def test_copilot_legacy_handshake_and_catalog_use_explicit_empty_ping(self):
        rpc = FakeRPC()
        with patch.object(adapter, 'RPC', return_value=rpc):
            result = adapter.models('copilot', 'synthetic-token')
        self.assertEqual([m for m, _ in rpc.calls], ['ping', 'models.list'])
        self.assertEqual(result['models'][0]['id'], 'live-copilot-id')

    def test_codex_login_uses_stdin_external_tokens_and_no_refresh_file(self):
        auth = json.dumps({'auth_mode': 'chatgptAuthTokens', 'tokens': {
            'account_id': 'fake-account', 'access_token': 'synthetic-access', 'refresh_token': ''}})
        rpc = FakeRPC()
        def start(command, **kwargs):
            self.assertNotIn('synthetic-access', command)
            self.assertNotIn('synthetic-access', kwargs['env'].values())
            self.assertFalse((Path(kwargs['cwd']) / 'auth.json').exists())
            return rpc
        with patch.object(adapter, 'RPC', side_effect=start):
            result = adapter.models('codex', auth)
        self.assertEqual(result['models'][0]['id'], 'execution-id')
        self.assertEqual(rpc.calls[1][1]['accessToken'], 'synthetic-access')

    def test_invalid_or_injected_actions_fail_without_echoing_provider_text(self):
        action = {field: '' for field in FIELDS}
        action['tool'] = 'Bash'
        self.assertEqual(adapter.parse_action('codex', json.dumps(action)), action)
        for text in ('synthetic-private', json.dumps(dict(action, command=['injected'])), '{}'):
            with self.assertRaises(adapter.Failure) as error:
                adapter.parse_action('codex', text)
            self.assertNotIn(text, str(error.exception))
