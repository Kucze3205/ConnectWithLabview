import errno
from datetime import datetime, timedelta, timezone
import json
import unittest

from provider_adapter import Failure
from role_runtime import Runtime
from runtime_store import Store
from test_runtime_store import Backend
from test_role_runtime import Broker
from test_tool_broker import action

PROMPT = "SECRET-PROMPT-TEXT"


class ProviderUnknownTest(unittest.TestCase):
    def setUp(self):
        self.backend, self.store = Backend(), None
        self.store = Store(self.backend)
        self.owner = {'providers': {p: {'models': ['allowed']} for p in ('claude', 'codex')},
                      'backoff': {'initial_seconds': 300, 'max_seconds': 21600}}
        candidates = [{'provider': p, 'model': 'allowed'} for p in self.owner['providers']]
        self.policy = {'tasks': {'build': candidates[:1]}}
        self.credentials = {p: 'synthetic-' + p for p in self.owner['providers']}
        self.now = datetime(2026, 10, 22, 12, tzinfo=timezone.utc)

    def runtime(self, request, probe=None):
        return Runtime(self.owner, self.policy, 'build', self.store, 'sessions/11.json', Broker(),
                       lambda _: {'head': 'h'}, self.credentials, PROMPT, 'fingerprint',
                       model_request=request, clock=lambda: self.now, probe=probe)

    def record(self):
        return self.store.read('pool.json')['availability']['providers']['claude']

    def local_failures(self, error, runs=3):
        calls, results = [], []
        def request(*args, **kwargs):
            calls.append(1)
            raise error
        for _ in range(runs):
            results.append(self.runtime(request).run(10, 30))
            if results[-1]['status'] == 'crashed' or len(results) == runs:
                break
            self.now += timedelta(seconds=301)
        return results, calls

    def test_e2big_is_recorded_without_content_and_does_not_grow_the_cooldown(self):
        results, calls = self.local_failures(OSError(errno.E2BIG, PROMPT + ' Argument list too long'), runs=1)
        self.assertEqual(results[0]['status'], 'paused')
        record = self.record()
        self.assertEqual(record['error'], {'type': 'OSError', 'errno': errno.E2BIG})
        self.assertEqual(record['retry_after'], (self.now + timedelta(seconds=300)).isoformat().replace('+00:00', 'Z'))
        self.assertEqual(results[0]['reasons'][0]['error'], {'type': 'OSError', 'errno': errno.E2BIG})
        self.assertNotIn(PROMPT, json.dumps(self.backend.files, default=str))

    def test_local_errors_wait_a_fixed_short_time_then_crash_the_session(self):
        results, calls = self.local_failures(OSError(errno.E2BIG, PROMPT))
        self.assertEqual([r['status'] for r in results], ['paused', 'paused', 'crashed'])
        self.assertEqual(results[-1]['reason'], 'local_error:OSError:E2BIG')
        self.assertEqual(len(calls), 3)
        self.assertEqual(self.record()['retry_after'], (self.now + timedelta(seconds=300)).isoformat().replace('+00:00', 'Z'))
        self.assertNotIn(PROMPT, json.dumps(self.backend.files, default=str) + json.dumps(results, default=str))

    def test_a_success_between_local_errors_resets_the_count(self):
        self.local_failures(TypeError('bad'), runs=2)
        self.now += timedelta(seconds=301)
        self.assertEqual(self.runtime(lambda *a, **kw: action('Write', path='f', text='x')).run(1, 30)['status'], 'partial')
        self.assertNotIn('local_errors', self.store.read('sessions/11.json'))

    def test_provider_failures_keep_exponential_cooldown(self):
        def request(*args, **kwargs):
            raise Failure({'status': 'quota', 'scope': 'provider'})
        self.runtime(request).run(3, 30)
        self.assertEqual(self.record()['retry_after'], (self.now + timedelta(seconds=300)).isoformat().replace('+00:00', 'Z'))
        self.now += timedelta(seconds=301)
        self.runtime(request).run(3, 30)
        self.assertEqual(self.record()['attempts'], 2)
        self.assertEqual(self.record()['retry_after'], (self.now + timedelta(seconds=600)).isoformat().replace('+00:00', 'Z'))
        self.assertNotIn('error', self.record())

    def test_a_successful_probe_shortens_a_long_cooldown(self):
        fail = lambda *a, **kw: (_ for _ in ()).throw(Failure({'status': 'quota', 'scope': 'provider'}))
        for _ in range(3):                    # 5, 10 and 20 minutes
            self.runtime(fail).run(3, 30)
            self.now += timedelta(seconds=21 * 60 * 60 // 1000 * 0) + timedelta(seconds=1300)
        self.runtime(fail).run(3, 30)
        self.assertGreater((datetime.fromisoformat(self.record()['retry_after'].replace('Z', '+00:00')) - self.now).seconds, 1800)
        probes = []
        def probe(provider, credential, timeout):
            probes.append((provider, credential))
            return {'status': 'available'}
        result = self.runtime(lambda *a, **kw: action('Finish', status='done'), probe=probe).run(3, 30)
        self.assertEqual(result['status'], 'done')
        self.assertEqual(probes, [('claude', 'synthetic-claude')])

    def test_a_failed_probe_keeps_the_cooldown_and_probes_once(self):
        self.runtime(lambda *a, **kw: (_ for _ in ()).throw(Failure({'status': 'quota', 'scope': 'provider'})), None).run(1, 30)
        runtime = self.runtime(None)
        state = self.store.read('pool.json')
        state['availability']['providers']['claude']['retry_after'] = (self.now + timedelta(hours=2)).isoformat().replace('+00:00', 'Z')
        self.store.update('pool.json', lambda _: state)
        probes = []
        runtime.probe = lambda provider, credential, timeout: probes.append(provider) or {'status': 'quota'}
        result = runtime.run(5, 30)
        self.assertEqual((result['status'], len(probes)), ('paused', 1))
        self.assertEqual(self.record()['status'], 'quota')


if __name__ == '__main__':
    unittest.main()
