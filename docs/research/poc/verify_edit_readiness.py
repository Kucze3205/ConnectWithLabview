"""Offline evidence consistency checks; passing is not LabVIEW/POC success."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys
import zlib

sys.dont_write_bytecode = True
BASE = Path(__file__).resolve().parent
REQUIREMENTS = {'semantics', 'connectivity', 'encoding', 'container_rebuild', 'integrity', 'compiled_cache', 'save_version', 'owner_runtime'}
RECIPE_TEXT = {'before_meaning', 'after_meaning', 'field_type', 'connectivity', 'replacement_contract', 'rebuild', 'integrity', 'compiled_cache', 'save_version'}

class EvidenceError(ValueError):
    pass

def need(condition, message):
    if not condition:
        raise EvidenceError(message)

def nonempty(value):
    return isinstance(value, str) and bool(value.strip())

def sha(value):
    return isinstance(value, str) and re.fullmatch('[0-9a-f]{64}', value) is not None

def local(name):
    need(nonempty(name), 'empty evidence path')
    path = (BASE / name).resolve()
    need(not Path(name).is_absolute() and path.is_relative_to(BASE), 'evidence path escapes POC directory')
    need(path.is_file(), 'missing local evidence: ' + name)
    return path

def read(name):
    return json.loads(local(name).read_text())

def validate(document):
    expected = {'schema_version', 'verdict', 'summary', 'scope', 'sources', 'fixtures', 'requirements', 'blockers', 'exits', 'recipe', 'spans', 'evidence'}
    need(isinstance(document, dict) and set(document) == expected, 'invalid top-level schema')
    need(type(document['schema_version']) is int and document['schema_version'] == 1, 'schema version')
    need(document['verdict'] in ('ready', 'partial', 'unsupported'), 'verdict')
    need(nonempty(document['summary']), 'summary')
    scope = document['scope']
    need(isinstance(scope, dict) and scope.get('fixture_limit') == 12, 'fixture limit')
    need(scope.get('edited_vi') is False and scope.get('behavior_claim') is False, 'research scope violated')
    need(nonempty(scope.get('save_version_policy')), 'save-version policy')
    need(isinstance(scope.get('runtime_checks'), list) and len(scope['runtime_checks']) >= 3 and all(map(nonempty, scope['runtime_checks'])), 'owner runtime checks')
    evidence = document['evidence']
    need(isinstance(evidence, list) and evidence, 'evidence inventory')
    inventory = {}
    for item in evidence:
        need(isinstance(item, dict) and set(item) == {'path', 'sha256', 'bytes'}, 'evidence record schema')
        name = item['path']
        need(nonempty(name) and name not in inventory and sha(item['sha256']), 'duplicate evidence or invalid hash')
        raw = local(name).read_bytes()
        need(type(item['bytes']) is int and len(raw) == item['bytes'], 'size mismatch: ' + name)
        need(hashlib.sha256(raw).hexdigest() == item['sha256'], 'hash mismatch: ' + name)
        inventory[name] = item
    def refs(names):
        need(isinstance(names, list) and names and all(nonempty(n) and n in inventory for n in names), 'missing inventoried citation')
    refs(document['sources'])
    refs([document['fixtures'], 'edit-readiness.md', 'step3/constant-candidate.json', 'inspect_vi.py', 'heap-labels.json'])
    for target in re.findall(r'\]\(([^)]+)\)', local('edit-readiness.md').read_text()):
        name = target.split('#')[0]
        if name == 'edit-readiness.json':
            local(name)  # This manifest cannot contain its own hash.
        else:
            refs([name])
    for name in document['sources']:
        if not name.endswith('provenance.json'):
            continue
        provenance = read(name)
        need(isinstance(provenance, list) and provenance, 'source provenance')
        for p in provenance:
            refs([p['file']])
            item = inventory[p['file']]
            need(p['sha256'] == item['sha256'] and p['bytes'] == item['bytes'], 'provenance hash/size mismatch')
            need(nonempty(p.get('url')) and re.search(r'/[0-9a-f]{40}/', p['url']), 'unpinned source URL')
            if name.startswith('step3/'):
                need(re.fullmatch('[0-9a-f]{40}', p.get('revision', '')) is not None, 'source revision')
                need(nonempty(p.get('original_path')) and nonempty(p.get('license')), 'source path/license')
                refs([p['license_file']])
    search = read('step3/source-search.json')
    need(isinstance(search.get('files'), list) and search['files'], 'source search inventory')
    for f in search['files']:
        need(sha(f['sha256']) and isinstance(f['classes'], list) and isinstance(f['matches'], dict), 'source search record')
        if f['origin'] == 'saved':
            refs([f['path']])
            need(inventory[f['path']]['sha256'] == f['sha256'], 'searched source hash')
            lines = local(f['path']).read_text().splitlines()
            for matches in f['matches'].values():
                for match in matches:
                    need(1 <= match['line'] <= len(lines) and lines[match['line']-1] == match['text'], 'source search line mismatch')
    probe = read(document['fixtures'])
    need(nonempty(probe.get('selection_criteria')), 'fixture selection criteria')
    fixtures = probe.get('fixtures')
    need(isinstance(fixtures, list) and 0 < len(fixtures) <= scope['fixture_limit'], 'fixture count')
    paths = set()
    for f in fixtures:
        need(nonempty(f.get('path')) and f['path'] not in paths and f.get('source') in ('pylavi', 'actor-framework'), 'fixture identity')
        paths.add(f['path'])
        need(f.get('status') in ('complete', 'partial', 'failed', 'unavailable'), 'fixture status')
        if f['status'] == 'unavailable':
            need(bool(f.get('failure')), 'unavailable fixture lacks reason')
            continue
        need(sha(f.get('sha256')) and type(f.get('bytes')) is int and f['bytes'] > 0, 'fixture hash/size')
        if f['status'] in ('complete', 'partial'):
            need(sha(f.get('heap_sha256')) and f.get('heap_bytes', 0) >= 4 and f.get('entries', 0) > 0, 'heap record')
        if f['status'] != 'complete':
            need(bool(f.get('failure')), 'failure not recorded')
    requirements = document['requirements']
    need(isinstance(requirements, dict) and set(requirements) == REQUIREMENTS, 'requirement coverage')
    for key, value in requirements.items():
        need(isinstance(value, dict) and value.get('status') in ('resolved', 'unresolved', 'owner_check') and nonempty(value.get('finding')), 'requirement schema: ' + key)
        refs(value.get('evidence'))
    need(requirements['owner_runtime']['status'] == 'owner_check', 'runtime must remain owner check')
    need(isinstance(document['blockers'], list) and all(map(nonempty, document['blockers'])), 'blockers schema')
    need(isinstance(document['exits'], list) and all(map(nonempty, document['exits'])), 'exits schema')
    recipe = document['recipe']
    if document['verdict'] == 'ready':
        need(not document['blockers'], 'ready verdict retains blockers')
        need(all(v['status'] == 'resolved' for k, v in requirements.items() if k != 'owner_runtime'), 'ready verdict has unresolved requirements')
        need(isinstance(recipe, dict) and RECIPE_TEXT | {'evidence', 'patches'} == set(recipe), 'ready recipe incomplete')
        for key in RECIPE_TEXT:
            need(nonempty(recipe[key]) and re.search(r'\b(TODO|TBD|unknown|hypothetical|unresolved)\b', recipe[key], re.I) is None, 'recipe field unsupported: ' + key)
        refs(recipe['evidence'])
        need(isinstance(recipe['patches'], list) and recipe['patches'], 'ready recipe has no patches')
    else:
        need(document['blockers'] and len(document['exits']) >= 2 and recipe is None, 'negative verdict requires blockers, two exits and no executable recipe')
    spec = importlib.util.spec_from_file_location('edit_readiness_inspector', local('inspect_vi.py'))
    inspector = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(inspector)
    constant = read('step3/constant-candidate.json')
    heaps = {}
    entries = {}
    captured = [(f, f['baseline']) for f in fixtures if 'baseline' in f]
    captured.append((constant, constant))
    for fixture, capture in captured:
        need(fixture['path'] in paths, 'captured fixture not inspected')
        recorded = next(f for f in fixtures if f['path'] == fixture['path'])
        need(recorded['sha256'] == fixture['sha256'] and recorded['heap_sha256'] == capture['heap_sha256'], 'capture provenance mismatch')
        payload = bytes.fromhex(capture['payload_hex'])
        need(len(payload) == capture['resource']['payload_length'], 'captured resource length')
        stream = zlib.decompressobj()
        heap = stream.decompress(payload[4:], inspector.MAX_HEAP + 1)
        need(stream.eof and not stream.unused_data and not stream.unconsumed_tail, 'captured zlib framing')
        need(len(heap) == int.from_bytes(payload[:4], 'big') == recorded['heap_bytes'], 'captured heap length')
        need(hashlib.sha256(heap).hexdigest() == capture['heap_sha256'], 'captured heap hash')
        parsed = inspector.parse_heap(heap)
        need(parsed['status'] == 'complete' and parsed['consumed'] == len(heap) and len(parsed['entries']) == recorded['entries'], 'captured heap parse')
        inspector.annotate(parsed, inspector.load_labels())
        heaps[fixture['path']] = heap
        entries[fixture['path']] = parsed['entries']
    # Reconstruct ancestor metadata, rather than trusting stored UID/class claims.
    stack = []
    contexts = {}
    for entry in entries[constant['path']]:
        if entry['scope'] == 'close':
            stack.pop()
            continue
        contexts[entry['heap_offset']] = copy.deepcopy(stack)
        if entry['scope'] == 'open':
            stack.append({'offset': entry['heap_offset'], 'name': entry['name'], 'class_id': next((a['value'] for a in entry['attributes'] if a['id'] == -2), None), 'uid': next((a['value'] for a in entry['attributes'] if a['id'] == -3), None)})
    by_offset = {e['heap_offset']: e for e in entries[constant['path']]}
    for observation in constant['observations']:
        e = observation['entry']
        need(by_offset.get(e['heap_offset']) == e and contexts[e['heap_offset']] == observation['ancestors'], 'constant entry/context mismatch')
    def span(fixture, start, end, value, field=None):
        need(fixture in heaps and type(start) is int and type(end) is int and 4 <= start < end <= len(heaps[fixture]), 'invalid heap span')
        need(isinstance(value, str) and re.fullmatch('(?:[0-9a-f]{2})+', value) is not None, 'span hex')
        need(heaps[fixture][start:end] == bytes.fromhex(value), 'original span bytes mismatch')
        need(any(e['data_offset'] == start and e['end'] == end and (field is None or e['name'] == field) for e in entries[fixture]), 'span does not identify a complete field body')
    need(isinstance(document['spans'], list) and document['spans'], 'missing original spans')
    for s in document['spans']:
        need(set(s) == {'fixture', 'start', 'end', 'hex', 'field'}, 'span schema')
        span(s['fixture'], s['start'], s['end'], s['hex'], s['field'])
    if recipe:
        patched = []
        for patch in recipe['patches']:
            need(set(patch) == {'fixture', 'start', 'end', 'before_hex', 'after_hex'}, 'patch schema')
            span(patch['fixture'], patch['start'], patch['end'], patch['before_hex'])
            need(isinstance(patch['after_hex'], str) and re.fullmatch('(?:[0-9a-f]{2})+', patch['after_hex']) is not None and patch['after_hex'] != patch['before_hex'], 'patch lacks a byte change')
            need(not any(f == patch['fixture'] and max(a, patch['start']) < min(z, patch['end']) for f, a, z in patched), 'overlapping patches')
            patched.append((patch['fixture'], patch['start'], patch['end']))
    return {'verdict': document['verdict'], 'fixtures': len(fixtures), 'captured_heaps': len(heaps), 'spans': len(document['spans']), 'evidence_files': len(inventory)}

def main():
    document = read('edit-readiness.json')
    result = validate(document)
    failures = []
    def reject(name, mutate):
        candidate = copy.deepcopy(document)
        mutate(candidate)
        try:
            validate(candidate)
        except (EvidenceError, KeyError, TypeError, ValueError):
            failures.append(name)
            return
        raise EvidenceError('negative self-check accepted: ' + name)
    reject('ready with blockers', lambda d: d.update(verdict='ready'))
    reject('ready with unresolved requirements', lambda d: d.update(verdict='ready', blockers=[]))
    def incomplete(d):
        d.update(verdict='ready', blockers=[], recipe={})
        for k, v in d['requirements'].items():
            if k != 'owner_runtime':
                v['status'] = 'resolved'
    reject('incomplete ready recipe', incomplete)
    reject('missing citation', lambda d: d['requirements']['integrity'].update(evidence=['missing-evidence.txt']))
    reject('corrupt evidence hash', lambda d: d['evidence'][0].update(sha256='0' * 64))
    reject('wrong original span', lambda d: d['spans'][0].update(hex='00'))
    reject('fixture count limit', lambda d: d['scope'].update(fixture_limit=13))
    result.update(status='pass', negative_checks=len(failures), limitations='Evidence consistency only; not POC success or LabVIEW validity. Original VI hashes recorded, not rehashed without originals.')
    print(json.dumps(result, sort_keys=True))

if __name__ == '__main__':
    try:
        main()
    except (EvidenceError, OSError, KeyError, TypeError, ValueError, zlib.error) as exc:
        print('edit-readiness: FAIL: ' + str(exc), file=sys.stderr)
        raise SystemExit(1)
