#!/usr/bin/env python3
"""Repository-only regressions for #663 F1; no session files or real executions.

Expectations follow 0138 linkage lines 222-246 and 265-285. These public synthetic
cases were authored after reading the review; they are not blind evaluation data.
"""
from copy import deepcopy
import json
from pathlib import Path
import runpy
import subprocess
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]

def setup():
    checker = runpy.run_path(str(ROOT / 'benchmark/verify_attempt_evidence_0143.py'))
    group = runpy.run_path(str(ROOT / 'benchmark/verify_project_run_binding_0138.py'))
    data = checker['parse']((ROOT / 'benchmark/attempt-evidence-0143.json').read_text())
    for pin in data['pins']:
        raw = (ROOT / pin['path']).read_bytes()
        checker['require'](len(raw) == pin['byte_size'] and checker['sha'](raw) == pin['sha256'], pin['path'])
    original = checker['parse']((ROOT / 'benchmark/project-run-binding-0138.json').read_text())
    source = {'base': original['rehearsal']['fixture'],
              'template': checker['parse']((ROOT / 'benchmark/baseline/run-record.template.json').read_text())}
    source['manifest'] = checker['parse'](source['base']['manifest_text'])
    return checker, group, group['load_legacy_functions'](), data, source

def build_variants(checker, fixture):
    variants = []
    def changed(name, keys):
        f = deepcopy(fixture)
        tool = next(a for a in f['envelope']['attempts'] if a['arm'] == 'tool')
        fields = tool['legacy_record']['fields']
        if 'model' in keys:
            fields['model_identity']['value'] = 'synthetic:wrong-model-0145'
        if 'prompt' in keys:
            fields['common_prompt_sha256']['value'] = checker['sha'](b'SYNTHETIC wrong common prompt 0145')
        if 'input' in keys:
            fields['input_evidence']['value'][0]['sha256'] = checker['sha'](b'SYNTHETIC wrong original 0145')
        if 'tool' in keys:
            fields['tool_calls']['value'][0]['response'] = 'SYNTHETIC different tool response 0145'
        if 'error' in keys:
            fields['tool_calls']['value'][0]['error'] = 'SYNTHETIC tool error'
        variants.append((name, f))
        return f
    changed('changed attached model identity', {'model'})
    changed('changed common prompt', {'prompt'})
    changed('changed original input', {'input'})
    changed('changed tool content', {'tool'})
    combined = changed('four contradictions in one comparison', {'model', 'prompt', 'input', 'tool'})
    four = deepcopy(combined)
    for a in four['envelope']['attempts']:
        a['legacy_record']['fields']['model_identity']['value'] = 'synthetic:wrong-model-0145'
    for original in list(four['envelope']['attempts']):
        a = deepcopy(original)
        a['attempt_id'] += '-copy-0145'
        a['attempt_order'] = max(x['attempt_order'] for x in four['envelope']['attempts']) + 1
        for e in a['evidence']:
            e['attempt_id'] = a['attempt_id']
            e['object_id'] = 'synthetic://' + a['attempt_id'] + '/' + e['kind']
        event = checker['event_at'](four, a)
        event['attempt_id'] = a['attempt_id']
        event['attempt_order'] = a['attempt_order']
        raw = checker['pack'](event)
        ref = 'synthetic:payload-f1-' + str(a['attempt_order'])
        four['payloads'][ref] = {'encoding': 'hex', 'hex': raw.hex(), 'byte_size': len(raw),
                                 'sha256': checker['sha'](raw), 'utf8': raw.decode()}
        checker['entry'](a, 'attempt_event')['payload_ref'] = ref
        four['envelope']['attempts'].append(a)
    variants.append(('four contradictory records', four))
    changed('tool error remains incomplete', {'error'})
    variants.append(('unmodified consistent control', deepcopy(fixture)))
    return variants

def observe(checker, group, legacy, source, fixture):
    try:
        decision = checker['validate'](fixture, source, group, legacy)
    except (ValueError, KeyError, TypeError, UnicodeError) as exc:
        decision = str(exc)
    counts = checker['accounting'](fixture, source, legacy, decision == 'pass')
    return {'decision': decision, 'accounting': counts,
            'legacy_results': [checker['legacy_result'](fixture, a, source, legacy)
                               for a in fixture['envelope']['attempts']],
            'retained_payloads': checker['retained_payloads'](fixture)}


def main():
    checker, group, legacy, data, source = setup()
    require = checker["require"]
    variants = build_variants(checker, data["fixture"])
    plan = checker["parse"](source["base"]["plan_text"])
    comparisons = len(plan["comparisons"])
    require(comparisons > 0, "no planned comparison")
    matched = []
    for name, fixture in variants:
        result = observe(checker, group, legacy, source, fixture)
        counts = result["accounting"]
        positive = name == "unmodified consistent control"
        expected = comparisons if positive else 0
        require(counts["synthetic_complete_comparisons"] == expected,
                name + ": unexpected completion")
        if positive:
            require(result["decision"] == "pass", "consistent control rejected")
            require(all(s == "pass" for s in result["legacy_results"]),
                    "consistent attachments rejected")
        else:
            # Completion must use the strengthened attachment joins itself, even
            # if a caller supplies a nominally consistent envelope label.
            direct = checker["accounting"](fixture, source, legacy, True)
            require(direct["synthetic_complete_comparisons"] == 0,
                    name + ": completion bypassed attachment checks")
        require(counts["attempts_retained"] == len(fixture["envelope"]["attempts"]),
                name + ": attempt inventory loss")
        matched.append(name)
    saved = subprocess.run(
        [sys.executable, "-I", str(ROOT / "benchmark/verify_attempt_evidence_0143.py")],
        capture_output=True, text=True, check=False)
    require(saved.returncode == 0, "saved controls failed: " + saved.stderr.strip())
    observed = checker["parse"](saved.stdout)
    require(observed["status"] == "pass" and
            observed["controls_matched"] == len(data["controls"]) and
            [c["name"] for c in observed["observed"]] ==
            [c["name"] for c in data["controls"]], "saved control inventory")
    require(observed["retained_grouping"]["exit"] == 0, "retained grouping failed")
    print(json.dumps({"status": "pass", "f1_controls_matched": len(matched),
                      "saved_controls_matched": len(observed["observed"]),
                      "retained_grouping_controls": observed["retained_grouping"]["controls_matched"],
                      "consistent_complete_comparisons": comparisons,
                      "benchmark_ready": False}, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, KeyError, TypeError, UnicodeError, OSError, StopIteration) as exc:
        print("attempt-evidence-f1-0145: " + str(exc), file=sys.stderr)
        sys.exit(1)
