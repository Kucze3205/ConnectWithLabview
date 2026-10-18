import json
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
