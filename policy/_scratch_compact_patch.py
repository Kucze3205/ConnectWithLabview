"""Scratch (deleted before Finish): build engine-change diffs in a temp git repo, run runtime tests, check they apply."""
import json, os, shutil, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path.cwd()
work = Path(tempfile.mkdtemp())
shutil.copytree(ROOT / ".github/loop", work / ".github/loop", ignore=shutil.ignore_patterns("__pycache__"))
shutil.copy(ROOT / "engine.yml", work / "engine.yml")


def git(*a, cwd=work):
    return subprocess.run(["git", *a], cwd=cwd, capture_output=True, text=True)


def tests():
    env = dict(os.environ, PYTHONPATH=str(work / ".github/loop"))
    t = subprocess.run([sys.executable, "-m", "unittest", "-q", "test_role_runtime"], cwd=work / ".github/loop/tests",
                       capture_output=True, text=True, env=env)
    return t.returncode, t.stderr[-2500:]


def replace(rel, old, new):
    p = work / rel
    t = p.read_text()
    assert t.count(old) == 1, (rel, old[:80], t.count(old))
    p.write_text(t.replace(old, new))


git("init", "-q"); git("add", "-A"); git("-c", "user.name=p", "-c", "user.email=p@p", "commit", "-qm", "base")
print("BASELINE TESTS", tests())

RR = ".github/loop/role_runtime.py"
TR = ".github/loop/tests/test_role_runtime.py"
replace(RR, '''def compact(history, limits):
    """Full recent turns, a brief list of earlier ones; the oldest briefs go when the byte limit is exceeded."""
    keep = max(1, int(limits["recent_turns"]))
    older, recent = [brief(e) for e in history[:-keep]], history[-keep:]
    while older and size([older, recent]) > limits["history_bytes"]:
        older.pop(0)
    while len(recent) > 1''', '''BATCH = 8  # earlier turns are briefed and cut in groups of this many, aligned to absolute turn numbers


def compact(history, limits, start=0):
    """Full recent turns, a brief list of earlier ones; the oldest briefs go when they exceed a quarter of the limit.
    `start` is the absolute number of history[0]. The split and the cut move only at multiples of BATCH, so
    `earlier_turns` stays byte-identical between consecutive requests: an append-only prefix a prompt cache can read."""
    keep = max(1, int(limits["recent_turns"]))
    split = max(0, (start + len(history) - keep) // BATCH * BATCH - start)
    older, recent = [brief(e) for e in history[:split]], history[split:]
    del older[:(-start) % BATCH]
    while older and size(older) > limits["history_bytes"] // 4:
        del older[:BATCH]
    while len(recent) > 1''')
replace(RR, '''            prompt = (self.prompt + '\\n\\nYou propose''', '''            start = max(0, state["turns"] - len(state["history"]))  # the stored history may have lost its oldest turns
            prompt = (self.prompt + '\\n\\nYou propose''')
replace(RR, '''json.dumps(compact(state["history"], self.context), ensure_ascii=False))''',
        '''json.dumps(compact(state["history"], self.context, start), ensure_ascii=False))''')
replace(TR, '''        self.assertEqual(sent['recent_turns'], history[-12:])
        self.assertNotIn('FILE-CONTENT', json.dumps(sent['earlier_turns']))
        self.assertEqual(sent['earlier_turns'][-1]['path'], 'src/387.vi')
        self.assertIn('read them again', sent['note'])
''', '''        self.assertEqual(sent['recent_turns'], history[384:])
        self.assertNotIn('FILE-CONTENT', json.dumps(sent['earlier_turns']))
        self.assertEqual(sent['earlier_turns'][-1]['path'], 'src/383.vi')
        self.assertEqual(int(sent['earlier_turns'][0]['path'][4:-3]) % 8, 0)
        self.assertIn('read them again', sent['note'])

    def test_earlier_turns_change_only_at_aligned_batch_boundaries(self):
        history = [{'action': {'tool': 'Read', 'path': 'f%d/' % n + 'p' * 150}, 'outcome': {'text': 'x' * 300}}
                   for n in range(200)]
        limits = {'history_bytes': 40_000, 'recent_turns': 5}
        view = lambda n: json.dumps(compact(history[:n], limits)['earlier_turns'])
        for n in range(16, 200):
            if (n - 5) % 8:
                self.assertEqual(view(n), view(n - 1))
        # A cut of the stored history keeps the batches aligned to absolute turn numbers.
        cut = compact(history[3:100], limits, 3)['earlier_turns']
        self.assertEqual(cut, compact(history[:100], limits)['earlier_turns'])
        self.assertLess(len(cut), 80)
        self.assertEqual(int(cut[0]['path'][1:].split('/')[0]) % 8, 0)
''')
replace(TR, '''        self.assertIn('BODY29', prompts[0])
        self.assertNotIn('BODY26', prompts[0])
''', '''        self.assertIn('BODY24', prompts[0])
        self.assertNotIn('BODY23', prompts[0])
''')
print("PATCHED TESTS", tests())
compact_diff = git("diff").stdout
git("-c", "user.name=p", "-c", "user.email=p@p", "commit", "-qam", "compact")

replace("engine.yml", '''  min_interval_minutes: null     # null: iteration after iteration''',
        '''  min_interval_minutes: 300      # one iteration per 5-hour subscription window; null: iteration after iteration''')
cadence_diff = git("diff").stdout

for name, diff in (("compact", compact_diff), ("cadence", cadence_diff)):
    p = ROOT / ("policy/_scratch_%s.diff" % name)
    p.write_text(diff)
    chk = subprocess.run(["git", "apply", "--check", str(p)], cwd=ROOT, capture_output=True, text=True)
    print("APPLY", name, chk.returncode, chk.stderr, "bytes", len(diff))

for p in sorted((ROOT / "iterations").glob("*.json")):
    r = json.loads(p.read_text())
    o = r.get("outcome", r)
    tot = {}
    for s in o.get("sessions", []):
        for key, u in (s.get("models") or {}).items():
            fam = key.split("/")[0]
            t = tot.setdefault(fam, [0, 0, 0, 0])
            for i, f in enumerate(("in", "cache_write", "cache_read", "out")):
                t[i] += u.get(f, 0) if isinstance(u, dict) else 0
    print(p.name, "sessions", len(o.get("sessions", [])), tot,
          "ALL in+cw", sum(v[0] for v in tot.values()), sum(v[1] for v in tot.values()))
    if o.get("sessions"):
        print("  sample session keys", sorted(o["sessions"][0].keys()), json.dumps(o["sessions"][0].get("tokens"))[:400])
