"""Repository-only integrity and authored-ledger accounting, never a prose scorer.
No CLI candidate input, writes, subprocesses, historical imports or native execution.
Semantic expectations remain subject to separate agent and human adjudication.
"""
import base64
import copy
import hashlib
import json
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
BASE = 'benchmark/writing/'
PINS_SHA256 = 'f6476328df20b0c55492b7b5a4a2e4139e8ee010d3315e9f61e846ea2b9e3f10'
REVIEW_SHA256 = '23369a95a2c6a847dbe0bf09c9e19dc04c36b7a75269f03018dcbb6e282076a6'
OUTCOMES = ['correct','incorrect','partial','missing','unverified','unsupported','error','unexecuted']
DIMS = ['correctness','grounding']
CASE_IDS = ['C1-0125-N%02d-v1' % n for n in range(1,9)]
CACHE = {}
JSON_CACHE = {}
RESOLVED = set()


def need(condition, code):
    if not condition:
        raise ValueError(code)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def canonical(value):
    return json.dumps(value,sort_keys=True,separators=(',',':')).encode('utf-8')


def read(path):
    p = Path(path)
    need(not p.is_absolute() and '..' not in p.parts, 'unsafe-path')
    full = ROOT / p
    need(full.resolve().is_relative_to(ROOT), 'unsafe-path')
    need(all(not (ROOT.joinpath(*p.parts[:i])).is_symlink() for i in range(1,len(p.parts)+1)), 'symlink')
    if path not in CACHE:
        CACHE[path] = full.read_bytes()
    return CACHE[path]


def load(path):
    if path not in JSON_CACHE:
        JSON_CACHE[path] = json.loads(read(path).decode('utf-8'))
    return JSON_CACHE[path]


def pointer(value, locator):
    need(locator.startswith('/'), 'bad-pointer')
    for part in locator[1:].split('/'):
        part = part.replace('~1','/').replace('~0','~')
        value = value[int(part)] if isinstance(value,list) else value[part]
    return value


def resolve(ref, pinmap):
    path, loc = ref['path'], ref['locator']
    need(path in pinmap and ref.get('sha256')==pinmap[path]['sha256'], 'source-pin')
    b = read(path)
    key = canonical(ref)
    if key in RESOLVED:
        return
    if loc == 'whole-file':
        value = b
    elif re.fullmatch(r'L[1-9][0-9]*',loc):
        lines = b.decode('utf-8').splitlines()
        need(int(loc[1:])<=len(lines), 'line-locator')
        value = lines[int(loc[1:])-1]
    else:
        value = pointer(load(path),loc)
    if ref.get('encoding') == 'base64':
        value = base64.b64decode(value,validate=True)
    if 'content_sha256' in ref:
        need(isinstance(value,bytes) and sha(value)==ref['content_sha256'], 'content-pin')
    if 'content_locator' in ref:
        need(isinstance(value,bytes), 'content-locator')
        content = ref['content_locator']
        if 'line' in content:
            lines = value.decode('utf-8').splitlines()
            need(1<=content['line']<=len(lines), 'content-line')
        if 'start' in content:
            need(content['start']==0 and content['length']==len(value), 'content-range')
        if 'xpath' in content:
            nodes = ET.fromstring(value).findall(content['xpath'])
            need(len(nodes)==1, 'xml-locator')
            line = lines[content['line']-1]
            need(('Name="'+nodes[0].attrib['Name']+'"') in line and ('>'+nodes[0].text+'<') in line, 'xml-line-correspondence')
    RESOLVED.add(key)


def references(value, pinmap):
    if isinstance(value,dict):
        if {'path','locator','sha256'} <= value.keys():
            resolve(value,pinmap)
        for v in value.values():
            references(v,pinmap)
    elif isinstance(value,list):
        for v in value:
            references(v,pinmap)


def no_promotion(value):
    if isinstance(value,dict):
        for k,v in value.items():
            if k in ['benchmark_ready','withheld','model_unseen','F4_released','full_trial_release','readiness_pass']:
                need(v is False, 'readiness-promotion')
            no_promotion(v)
    elif isinstance(value,list):
        for v in value:
            no_promotion(v)


def whole(values):
    if not values:
        return 'unverified'
    if 'incorrect' in values:
        return 'incorrect'
    if 'unverified' in values:
        return 'unverified'
    if all(x=='correct' for x in values):
        return 'correct'
    if any(x in ['correct','partial'] for x in values):
        return 'partial'
    if 'error' in values:
        return 'error'
    if all(x=='unsupported' for x in values):
        return 'unsupported'
    return 'missing'


def required_result(atoms, missing, dim):
    values = [a[dim] for a in atoms]
    if not values:
        return 'missing'
    if 'incorrect' in values:
        return 'incorrect'
    if 'unverified' in values:
        return 'unverified'
    if missing or any(x!='correct' for x in values):
        return 'partial'
    return 'correct'


def validate(cases, exp, pinmap, slots, core):
    no_promotion(cases)
    no_promotion(exp)
    need(cases.get('benchmark_ready') is False and exp.get('benchmark_ready') is False, 'readiness-promotion')
    need(cases.get('withheld') is False and cases.get('model_unseen') is False, 'public-scope')
    need([c['id'] for c in cases['cases']]==CASE_IDS and [e['id'] for e in exp['cases']]==CASE_IDS, 'case-inventory')
    need(exp.get('required_slot_inventory')==slots, 'required-slot-inventory')
    need(exp.get('inherited_denominators')==core['claim_adjudication']['required_denominators'], 'denominators')
    need(exp.get('pending')==dict(independent_agent_check=True,human_execution=True,owner_acceptance=True,native_checks=True,trials=True), 'pending-prerequisites')
    need(cases['conditions']['execution_record']==dict(agent_arms=0,native_jobs=0,actual_workspaces_allocated=False,text_trials=0,dependency_resolution='unexecuted',native_logs=None,save_version_evidence=None,reading_fidelity='unmeasured'), 'execution-overclaim')
    need(cases['author_exposure']['exposed'] is True and cases['author_exposure']['human'] is False and cases['author_exposure']['independent_checker'] is False, 'author-exposure')
    need(cases['conditions']['expected_output_kind']=='authored conditional expected text, never produced agent/native output', 'output-authority')
    for field,locator in [('workspace','/examples/0/inventories'),('boundaries','/examples/0/boundaries'),('trial_artifact_accounting','/examples/0/trial_artifact_accounting'),('operative_map_evidence','/examples/0/original_output_map')]:
        r = cases['conditions'][field]
        need(r['path']==BASE+'wp1-examples-0121.json' and r['locator']==locator, 'conditional-source-scope')
    references(cases,pinmap)
    references(exp,pinmap)
    total_atoms = 0
    for c,e in zip(cases['cases'],exp['cases']):
        raw = c['raw_answer'].encode('utf-8')
        need(len(raw)==c['raw_utf8_bytes'] and sha(raw)==c['raw_utf8_sha256']==e['raw_utf8_sha256'], 'raw-answer-hash')
        need(c['shared_context']==cases['conditions']['id'] and c['scenario'] in cases['conditions']['scenarios'], 'case-context')
        need([i['id'] for i in e['required_items']]==list(slots), 'required-slot-accounting')
        need(e['required_denominator_per_dimension']==3, 'denominators')
        atoms = e['atoms']
        total_atoms += len(atoms)
        ids = [a['atom_id'] for a in atoms]
        need(len(ids)==len(set(ids)) and bool(ids), 'atom-inventory')
        byid = {a['atom_id']:a for a in atoms}
        covered = set()
        for a in atoms:
            need(all(k in a for k in ['subject','property','value','conditions','original_output_evidence','truth_evidence','citation_support_decision','rationale','uncertainty','correctness','grounding']), 'atom-fields')
            need(all(a[d] in OUTCOMES for d in DIMS), 'separate-dimensions')
            start,end = a['raw_utf8_span']
            need(0<=start<end<=len(raw) and raw[start:end].decode('utf-8')==a['raw_quote'], 'raw-atom-span')
            covered.update(range(start,end))
            need(a['conditions']==dict(shared_context=c['shared_context'],scenario=c['scenario'],evidence_mode='authored-conditional-only'), 'atom-conditions')
            tokens = [t for group in re.findall(r'\[([A-Z,]+)\]',a['raw_quote']) for t in group.split(',')]
            need(tokens==a['citation_ids'] and all(t in cases['citation_registry'] for t in tokens), 'citation-accounting')
            supplied = [r for t in tokens for r in cases['citation_registry'][t]['evidence']]
            need(supplied==a['original_output_evidence'], 'submitted-evidence-accounting')
            need(a['citation_support_decision'] and a['rationale'] and a['uncertainty'], 'rationale-accounting')
            for r in a['context_evidence']:
                need(sha(canonical(pointer(cases,r['locator'])))==r['sha256'], 'context-pin')
            need(bool(a['context_evidence'])==('V' in tokens), 'context-accounting')
            rid = a['required_id']
            need((rid in slots and a['slot'] in slots[rid] and a['extra_id'] is None) or (rid is None and a['slot'] is None and bool(a['extra_id'])), 'atom-mapping')
            if a['duplicate_of']:
                need(a['duplicate_of'] in byid, 'duplicate-reference')
                b = byid[a['duplicate_of']]
                need(b['required_id']==rid and b['property']==a['property'] and b['value']==a['value'] and b['raw_utf8_span'][0]<start, 'duplicate-accounting')
            for target in a['contradicts']:
                need(target in byid and byid[target]['required_id']==rid and target!=a['atom_id'], 'contradiction-reference')
                need(a['correctness']=='incorrect' and a['grounding']=='incorrect', 'contradiction-accounting')
        need(all(i in covered or raw[i:i+1]==b'\n' for i in range(len(raw))), 'unaccounted-raw-content')
        extras = [a for a in atoms if a['required_id'] is None]
        need(e['extras']==[a['atom_id'] for a in extras], 'extra-accounting')
        need(e['duplicates']==[dict(atom_id=a['atom_id'],duplicate_of=a['duplicate_of']) for a in atoms if a['duplicate_of']], 'duplicate-accounting')
        need(e['contradictions']==[dict(atom_id=a['atom_id'],contradicts=a['contradicts']) for a in atoms if a['contradicts']], 'contradiction-accounting')
        for item in e['required_items']:
            rid = item['id']
            aa = [a for a in atoms if a['required_id']==rid]
            missing = [s for s in slots[rid] if s not in {a['slot'] for a in aa}]
            need(item['required_slots']==slots[rid] and item['missing_slots']==missing and item['atom_ids']==[a['atom_id'] for a in aa], 'required-slot-accounting')
            need(all(item.get(d)==required_result(aa,missing,d) for d in DIMS), 'required-dimension-accounting')
        need(set(e['assessment'])==set(DIMS), 'separate-dimensions')
        for d in DIMS:
            need(e['assessment'][d]==whole([i[d] for i in e['required_items']]+[a[d] for a in extras]), 'whole-dimension-accounting')
            need(e['required_counts'][d]=={o:sum(i[d]==o for i in e['required_items']) for o in OUTCOMES}, 'required-counts')
            need(e['extra_counts'][d]=={o:sum(a[d]==o for a in extras) for o in OUTCOMES}, 'extra-counts')
    # Frozen discrimination checks on these authored records, not narrative scoring.
    wrong = exp['cases'][3]['required_items'][0]
    need((wrong['correctness'],wrong['grounding'])==('correct','incorrect'), 'merged-dimensions')
    need(exp['cases'][6]['assessment']==dict(correctness='unverified',grounding='partial'), 'merged-dimensions')
    need(exp['cases'][0]['assessment']==exp['cases'][1]['assessment']==exp['cases'][4]['assessment']==dict(correctness='correct',grounding='correct'), 'fixed-positive-accounting')
    need(exp['cases'][2]['required_items'][0]['correctness']=='missing' and exp['cases'][2]['extras'], 'omission-extra-accounting')
    need(exp['cases'][5]['contradictions'] and exp['cases'][5]['assessment']==dict(correctness='incorrect',grounding='incorrect'), 'fixed-contradiction-accounting')
    need(all(i['correctness']=='missing' for i in exp['cases'][7]['required_items'][:2]), 'abstention-accounting')
    return total_atoms


def main():
    need(len(sys.argv)==1, 'no-arbitrary-input-supported')
    pins_path = BASE+'c1-challenges-0125-pins.json'
    need(sha(read(pins_path))==PINS_SHA256, 'protected-pin-manifest')
    pins = load(pins_path)
    pinmap = {p['path']:p for p in pins['protected_files']}
    need(len(pinmap)==len(pins['protected_files'])==125, 'protected-inventory')
    for p in pins['protected_files']:
        b = read(p['path'])
        need(len(b)==p['bytes'] and sha(b)==p['sha256'], 'protected-file-changed:'+p['path'])
    review_path = BASE+'wp1-key-review-0124.json'
    need(len(read(review_path))==126735 and sha(read(review_path))==REVIEW_SHA256, 'preserved-review')
    review = load(review_path)
    identity = review['reviewed_revision']['key_identity']
    need(identity==pinmap[identity['path']], 'review-scoped-key-pin')
    need(review['standards_assessment']['verdict']==review['spec_assessment']['verdict']=='CLEAR' and review['recommendation']['benchmark_ready'] is False, 'review-scope')
    method = load(BASE+'method.json')['tasks'][4]
    core = load(BASE+'wp1-key-0119.json')
    did,mid,lid = method['answer_ids']
    slots = {did:['selected_property_delta','exact_byte_edit'], mid:method['semantic_ids']+method['preservation_ids'], lid:['text_and_root_trials','native_validity','dependency_resolution','build','behavior','save_version','native_key','reading_fidelity','overall_writing','declaration_authority']}
    source = load(BASE+'wp1-examples-0121.json')
    x = source['examples'][0]
    original = read('benchmark/real-project-0107/original.lvproj')
    expected = base64.b64decode(source['byte_objects']['expected-project']['base64'],validate=True)
    need(expected==original[:3347]+b'3'+original[3348:] and original[3347:3348]==b'2' and len(original)==len(expected)==5806, 'conditional-text-bytes')
    need(set(x['inventories'])=={'workspace_pre','workspace_post','dependency_pre','dependency_post','immutable_pre','immutable_post','delivered'}, 'source-inventories')
    for name,inventory in x['inventories'].items():
        entries = inventory['entries']
        need(inventory['entries_sha256']==sha(canonical(entries)) and inventory['file_count']==len(entries), 'inventory-pin')
        for ent in entries:
            obj = source['byte_objects'][ent['byte_object']]
            raw = expected if ent['byte_object']=='expected-project' else read(obj['path'])
            need(len(raw)==ent['size'] and sha(raw)==ent['sha256'], 'inventory-byte-support')
    declared = [n.attrib['URL'] for n in ET.fromstring(original).iter() if 'URL' in n.attrib]
    for name in ['dependency_pre','dependency_post']:
        inv = x['inventories'][name]
        need(not inv['entries'] and [r['path'] for r in inv['declared_references']]==declared and len(declared)==11, 'dependency-accounting')
        need(all(r['status']=='unavailable' and r['raw_byte_reference'] is None and r['sha256'] is None and r['size'] is None for r in inv['declared_references']), 'invented-dependency-evidence')
    need([r['id'] for r in x['trial_artifact_accounting']]==method['trial_artifacts']['required'] and len(x['trial_artifact_accounting'])==13, 'trial-inventory')
    need(all(r['status']=='unavailable' and r['evidence'] is None for r in x['trial_artifact_accounting'][7:]), 'invented-trial-evidence')
    cases = load(BASE+'c1-challenges-0125-cases.json')
    exp = load(BASE+'c1-challenges-0125-expectations.json')
    atom_count = validate(cases,exp,pinmap,slots,core)
    template = load(BASE+'c1-challenges-0125-record-template.json')
    need(template['recording_state']=='unexecuted-blank-template' and template['human_result'] is None and template['independent_agent_result'] is None and not template['case_records'], 'nonblank-template')
    need([r['id'] for r in template['case_record_template']['required_items']]==list(slots), 'template-required-slots')
    no_promotion(template)
    # In-memory rejection checks use copies; no files are changed and no historical code runs.
    checks = []
    def reject(name, code, mutate):
        c,e = copy.deepcopy(cases),copy.deepcopy(exp)
        mutate(c,e)
        try:
            validate(c,e,pinmap,slots,core)
        except ValueError as err:
            need(str(err)==code, 'wrong-rejection:'+name+':'+str(err))
            checks.append(dict(name=name,rejected=True,reason=code))
        else:
            raise ValueError('accepted-rejecting-control:'+name)
    reject('corrupted-raw-UTF8-bytes','raw-answer-hash',lambda c,e:c['cases'][0].__setitem__('raw_answer',c['cases'][0]['raw_answer'].replace('\n','\r\n',1)))
    reject('wrong-source-pin','source-pin',lambda c,e:c['citation_registry']['B']['evidence'][0].__setitem__('sha256','0'*64))
    reject('missing-required-item','required-slot-accounting',lambda c,e:e['cases'][0]['required_items'].pop())
    reject('missing-required-inventory-slot','required-slot-inventory',lambda c,e:e['required_slot_inventory'][mid].pop())
    reject('unreported-missing-slot','required-slot-accounting',lambda c,e:e['cases'][2]['required_items'][0].__setitem__('missing_slots',[]))
    reject('merged-whole-dimensions','separate-dimensions',lambda c,e:e['cases'][0].__setitem__('assessment',{'combined':'correct'}))
    reject('copied-correctness-into-grounding','required-dimension-accounting',lambda c,e:e['cases'][3]['required_items'][0].__setitem__('grounding','correct'))
    reject('unsupported-readiness-promotion','readiness-promotion',lambda c,e:c.__setitem__('benchmark_ready',True))
    reject('invented-native-execution','execution-overclaim',lambda c,e:c['conditions']['execution_record'].__setitem__('native_jobs',1))
    reject('dropped-unverified-extra','extra-accounting',lambda c,e:e['cases'][6].__setitem__('extras',[]))
    reject('dropped-contradiction','contradiction-accounting',lambda c,e:e['cases'][5].__setitem__('contradictions',[]))
    reject('dropped-duplicate','duplicate-accounting',lambda c,e:e['cases'][4].__setitem__('duplicates',[]))
    print(json.dumps(dict(status='ok',scope='repository integrity and authored expectation accounting only; no arbitrary prose scoring or human result',benchmark_ready=False,protected_files=len(pinmap),preserved_review_sha256=REVIEW_SHA256,cases=len(cases['cases']),atoms=atom_count,answer_denominators=dict(correctness=3,grounding=3),resolved_unique_references=len(RESOLVED),rejection_checks=checks,package_errors=[],checker_sha256=sha(read(BASE+'check_c1_challenges_0125.py'))),sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (ValueError,KeyError,TypeError,IndexError,OSError,ET.ParseError) as error:
        print(json.dumps({'status':'failed','error':str(error),'benchmark_ready':False}),file=sys.stderr)
        raise SystemExit(1)
