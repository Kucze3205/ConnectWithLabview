import json
from contextlib import contextmanager
from pathlib import Path
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

    def test_copilot_legacy_handshake_and_catalog_use_explicit_empty_ping(self):
        rpc = FakeRPC()
        with patch.object(adapter, 'RPC', return_value=rpc), patch.object(adapter, 'sandbox', side_effect=lambda c, _: c):
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
        with patch.object(adapter, 'RPC', side_effect=start), patch.object(adapter, 'sandbox', side_effect=lambda c, _: c):
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
