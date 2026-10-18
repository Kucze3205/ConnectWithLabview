"""Exercise real pipes/framing without any provider or credential."""
import os
import sys
import tempfile
import unittest

import fakes
from provider_rpc import RPC


SERVER = r'''
import json,sys
headers = sys.argv[1] == 'headers'
while True:
    line = sys.stdin.buffer.readline()
    if not line: break
    if headers:
        size=int(line.split(b':')[1])
        assert not sys.stdin.buffer.readline().strip()
        line=sys.stdin.buffer.read(size)
    event=json.loads(line)
    if 'id' not in event: continue
    messages=[{'method':'notification','params':{'text':'zażółć'}},
              {'id':event['id'],'result':{'ok':True,'params':event.get('params')}}]
    for message in messages:
        data=json.dumps(message,ensure_ascii=False).encode()
        frame=(b'Content-Length: %d\r\n\r\n'%len(data)+data) if headers else data+b'\n'
        sys.stdout.buffer.write(frame)
    sys.stdout.buffer.flush()
'''


class RPCTest(unittest.TestCase):
    def test_both_provider_framings_preserve_unicode_and_notifications(self):
        for framing in ('lines', 'headers'):
            with self.subTest(framing=framing), tempfile.TemporaryDirectory() as directory:
                with RPC([sys.executable, '-c', SERVER, framing], cwd=directory, env=os.environ.copy(),
                         timeout=5, framing=framing) as rpc:
                    result = rpc.call('test', {'data': 'ąę'})
                    self.assertEqual(result, {'ok': True, 'params': {'data': 'ąę'}})
                    self.assertEqual(rpc.notifications[0]['params']['text'], 'zażółć')

    def test_disconnection_is_bounded_and_does_not_echo_diagnostics(self):
        with tempfile.TemporaryDirectory() as directory:
            with RPC([sys.executable, '-c', 'import sys; sys.stderr.write("synthetic-private")'],
                     cwd=directory, env=os.environ.copy(), timeout=5) as rpc:
                with self.assertRaisesRegex(RuntimeError, '^provider RPC disconnected$'):
                    rpc.receive()
