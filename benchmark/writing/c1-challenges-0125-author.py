"""Reproduce only the public, authored 0125 cases/expectations; never adjudicate prose.
Run from repository root. Refuses to replace any output. No historical code imports.
"""
import copy
import hashlib
import json
from pathlib import Path

BASE = Path('benchmark/writing')
E = 'benchmark/writing/wp1-examples-0121.json'
M = 'benchmark/writing/method.json'
K = 'benchmark/writing/wp1-key-0119.json'
O = 'benchmark/real-project-0107/original.lvproj'
L = 'benchmark/real-project-0107/LICENSE.txt'
H = lambda b: hashlib.sha256(b).hexdigest()
load = lambda p: json.loads(Path(p).read_text())
example = load(E)['examples'][0]
core = load(K)
pins = load(BASE / 'c1-challenges-0125-pins.json')
pin_by_path = {p['path']: p for p in pins['protected_files']}


def ref(path, locator, **kw):
    return dict(path=path, sha256=pin_by_path[path]['sha256'], locator=locator, **kw)


def project_ref(output, line, xpath=None):
    if output:
        r = ref(E, '/byte_objects/expected-project/base64', encoding='base64',
                content_sha256='8d984c2efd827a7b16f0f44fbaaf89adba0e031e2af743444f09f674c96e0e42')
    else:
        r = ref(O, 'whole-file', content_sha256=pin_by_path[O]['sha256'])
    r['content_locator'] = {'line': line} if line else {'start': 0, 'length': 5806}
    if xpath:
        r['content_locator']['xpath'] = xpath
    return r

xpath = "./Item[@Name='My Computer']/Item[@Name='Build Specifications']/Item[@Name='AF PPL']/Property[@Name='Bld_version.build']"
major = xpath.replace('Bld_version.build', 'Bld_version.major')
auto = xpath.replace('Bld_version.build', 'Bld_autoIncrement')
paired = lambda line, xp=None: [project_ref(False, line, xp), project_ref(True, line, xp)]
inv = lambda name: ref(E, '/examples/0/inventories/' + name)
citations = {
    'B': {'meaning': 'Selected build property, exact original and authored expected output, line 42 / byte 3347.', 'evidence': paired(42, xpath)},
    'W': {'meaning': 'Complete original and authored expected bytes; compare size and every offset.', 'evidence': paired(None)},
    'J': {'meaning': 'Major-version property at line 43 in the original and expected byte objects.', 'evidence': paired(43, major)},
    'A': {'meaning': 'autoIncrement declaration only, true in both objects.', 'evidence': paired(33, auto)},
    'R': {'meaning': 'Exact project root attributes at line 2, declaration only.', 'evidence': paired(2)},
    'I': {'meaning': 'Complete stipulated pre/post workspace inventories.', 'evidence': [inv('workspace_pre'), inv('workspace_post')]},
    'D': {'meaning': 'All 11 declared-but-absent references, zero materialized dependencies.', 'evidence': [inv('dependency_pre'), inv('dependency_post')]},
    'Z': {'meaning': 'Logical arm/immutable boundaries; no actual allocation or resolution.', 'evidence': [ref(E, '/examples/0/boundaries')]},
    'M': {'meaning': 'Complete immutable original and notice inventories before/after.', 'evidence': [inv('immutable_pre'), inv('immutable_post'), ref(E, '/examples/0/boundaries')]},
    'N': {'meaning': 'Delivered notice and its complete pinned bytes.', 'evidence': [inv('delivered'), ref(E, '/examples/0/notice_evidence'), ref(L, 'whole-file')]},
    'Q': {'meaning': 'WP1 request, preservation and exact text contract.', 'evidence': [ref(M, '/tasks/4/request'), ref(M, '/tasks/4/text_contract'), ref(M, '/tasks/4/preservation')]},
    'V': {'meaning': 'Frozen absent-execution record plus existing WP1 native/trial limits.', 'evidence': [ref(M, '/tasks/4/oracle'), ref(M, '/tasks/4/planned_results'), ref(M, '/tasks/4/reading_fidelity'), ref(E, '/claims_and_gaps'), ref(E, '/examples/0/trial_artifact_accounting')]}
}
DID, MID, LID = load(M)['tasks'][4]['answer_ids']
slots = {
    DID: ['selected_property_delta', 'exact_byte_edit'],
    MID: load(M)['tasks'][4]['semantic_ids'] + load(M)['tasks'][4]['preservation_ids'],
    LID: ['text_and_root_trials', 'native_validity', 'dependency_resolution', 'build', 'behavior', 'save_version', 'native_key', 'reading_fidelity', 'overall_writing', 'declaration_authority']
}
# Source-derived required slots are fixed before constructing the candidate prose.
# Each tuple is one atom with its exact semantic subject/property/value and source rationale.
specs = []
def add(key, text, subject, prop, value, required, slot, cites, rationale):
    specs.append(dict(key=key, text=text, subject=subject, property=prop, value=value,
                      required_id=required, slot=slot, citation_ids=cites, rationale=rationale))

add('d1', 'In this conditional copy, AF PPL’s childless Int property Bld_version.build changes from the literal 2 to the literal 3. [B,Q]', 'My Computer/Build Specifications/AF PPL/Bld_version.build', 'exact_property_text_transition', {'type':'Int','children':0,'before':'2','after':'3'}, DID, slots[DID][0], ['B','Q'], 'Original selected childless Int text is 2; the frozen request supplies 3; decoded expected bytes realize that substitution. No numeric coercion or native semantics.')
add('d2', 'The project stays 5806 bytes long, with the sole differing ASCII byte at zero-based offset 3347 on line 42. [W,Q]', 'complete Core/AF PPL Build.lvproj comparison', 'byte_delta', {'size':5806,'differing_offsets':[3347],'line':42,'before_hex':'32','after_hex':'33'}, DID, slots[DID][1], ['W','Q'], 'Compare complete bytes against the request-defined one-byte allowance; output is authored conditional evidence only.')
add('p1', 'The original and expected-output build-property locations support that exact text transition. [B]', 'paired selected build property locations', 'support_relation', 'support exact 2-to-3 text transition', MID, slots[MID][0], ['B'], 'Resolve both hashes and the selected property; this is a true relation, separate from merely stating the delta.')
add('p2', 'Comparing the complete paired byte objects shows every other project byte identical, including the BOM, declaration, tabs, LF endings, entities, ordering, final newline and autoIncrement=true. [W,A]', 'all project bytes except offset 3347', 'identity', 'byte-identical with no metadata exception', MID, slots[MID][1], ['W','A'], 'Whole-byte complementary ranges are equal; original line 33 and corresponding output retain true. This retains all preservation duties.')
add('p3', 'The complete pre/post workspace lists contain the same two paths, Core/AF PPL Build.lvproj and LICENSE.txt, with only the project changed. [I]', 'stipulated workspace pre/post inventories', 'file_set_and_changed_paths', {'same_paths':['Core/AF PPL Build.lvproj','LICENSE.txt'],'only_changed':'Core/AF PPL Build.lvproj'}, MID, slots[MID][2], ['I'], 'Compare complete entries, kinds, sizes, hashes and raw-object references; only the project hash differs.')
add('p4', 'The unrelated workspace LICENSE.txt has identical bytes before and after. [I,N]', 'workspace LICENSE.txt', 'byte_identity', True, MID, slots[MID][2], ['I','N'], 'Both inventory entries resolve to the exact pinned 1060-byte MIT notice.')
add('p5', 'All eleven URL declarations remain listed as absent references, and neither dependency inventory contains a materialized file. [D]', 'stipulated dependency pre/post inventories', 'declared_and_materialized', {'declared':11,'status':'absent','materialized':0}, MID, slots[MID][2], ['D'], 'Enumerated declarations match original XML URLs; null byte evidence is retained, not treated as resolved dependencies.')
add('p6', 'The logical boundaries record no cross-root links and forbid use of immutable or other-arm roots for dependencies. [Z]', 'stipulated logical root boundaries', 'links_and_forbidden_roots', {'cross_root_links':[],'forbidden':['immutable','other-arm']}, MID, slots[MID][2], ['Z'], 'Boundary record is a modeled restriction, not an executed isolation or dependency check.')
add('p7', 'The corresponding root declarations are Type=Project and LVVersion=20008000 in both byte objects. [R]', 'Project root original/expected', 'attribute_identity', {'Type':'Project','LVVersion':'20008000'}, MID, slots[MID][3], ['R'], 'Exact line 2 and parsed root attributes agree; this is not native save-version authority.')
add('p8', 'The complete immutable original-project and MIT-notice inventories outside the writable root match before and after. [M]', 'immutable original and license outside writable root', 'before_after_identity', True, MID, slots[MID][4], ['M'], 'Both complete immutable entry lists have identical paths, kinds, sizes, hashes and byte references; logical boundaries establish outside-writable scope only.')
add('p9', 'The delivered LICENSE.txt contains the complete pinned MIT copyright and permission notice without a byte change. [N]', 'stipulated delivered LICENSE.txt', 'notice_identity', 'complete pinned MIT bytes', MID, slots[MID][4], ['N'], 'Delivered entry resolves to the same pinned notice; full notice includes the copyright and permission condition.')
add('l0', 'No text-correctness or root-declaration trial has been executed. [V]', 'actual WP1 text and root trial results', 'execution_status', 'unexecuted', LID, 'text_and_root_trials', ['V'], 'Conditional expected text is not an observed trial; method planned_results retains unexecuted statuses.')
for key, label, slot in [('l1','native validity','native_validity'),('l2','dependency resolution','dependency_resolution'),('l3','building','build'),('l4','runtime behavior','behavior')]:
    add(key, 'There is no executed check of '+label+'. [V]', 'actual WP1 '+label, 'execution_status', 'unexecuted', LID, slot, ['V'], 'Frozen no-execution record and WP1 planned results provide no native execution or supporting log.')
add('l5', 'Native save-version preservation remains unverified. [V]', 'native original/output save-version preservation', 'status', 'unverified', LID, 'save_version', ['V'], 'No native version authority exists; identical declarations cannot supply it.')
add('l6', 'The native key is unavailable. [V]', 'WP1 native key', 'availability', 'unavailable', LID, 'native_key', ['V'], 'WP1 oracle explicitly retains unavailable native_key.')
add('l7', 'Reader fidelity has not been measured. [V]', 'reader fidelity', 'measurement_status', 'unmeasured', LID, 'reading_fidelity', ['V'], 'No frozen reader observations or executed reader trial is provided.')
add('l8', 'Overall writing remains unverified. [V]', 'overall WP1 writing', 'status', 'unverified', LID, 'overall_writing', ['V'], 'The text fixture cannot supply a full writing result with native and trial prerequisites absent.')
add('l9', 'The root version text is a declaration and supplies no proof of native save-version preservation. [R,V,Q]', 'root LVVersion=20008000', 'authority', 'declaration-only', LID, 'declaration_authority', ['R','V','Q'], 'Method preservation.root_version_authority is declaration-only; root text is not save-version evidence.')
bykey = {s['key']:s for s in specs}

conditions = {
    'id':'C1-0125-conditional-context-v1',
    'scope':example['conditions'],
    'workspace':ref(E, '/examples/0/inventories'),
    'boundaries':ref(E, '/examples/0/boundaries'),
    'trial_artifact_accounting':ref(E, '/examples/0/trial_artifact_accounting'),
    'operative_map_evidence':ref(E, '/examples/0/original_output_map'),
    'byte_objects':{n:ref(E, '/byte_objects/'+n) for n in ['original-project','expected-project','mit-notice']},
    'interpretation':'Use complete pinned conditional byte objects and all seven inventories, all 11 absent URL references and explicit logical boundaries. These are source evidence, not an automatically appended answer/map. Only relations actually asserted in prose receive answer credit. No unseen sidecars are supplied.',
    'expected_output_kind':'authored conditional expected text, never produced agent/native output',
    'execution_record':{'agent_arms':0,'native_jobs':0,'actual_workspaces_allocated':False,'text_trials':0,'dependency_resolution':'unexecuted','native_logs':None,'save_version_evidence':None,'reading_fidelity':'unmeasured'},
    'scenarios':{
        'conditional-copy':'Compare the complete original and authored expected text under the stipulated workspace; no actual delivery or trial has occurred.',
        'abstention':'The speaker is unable to supply an edited project or source map. Neither is submitted in this scenario. Existing authored expected bytes remain references only; never infer delivered artifacts.'
    },
    'citations':'Bracket tokens refer to citation_registry; each token expands to exact repository/container and content hashes plus original/expected locators. The raw prose uses this shared frozen dictionary. V also cites this frozen zero-execution record.',
    'preservation':'All existing WP1 semantic, four preservation, three answer and thirteen trial-accounting obligations remain; no scope waiver or native inference.',
    'not_isolated':'Cases and expectations are public in one repository. Paths support an ordered-reading procedure and enforce no access boundary.'
}

cases = []
expectations = []
outcomes = ['correct','incorrect','partial','missing','unverified','unsupported','error','unexecuted']

def assessment(values):
    if not values:
        return 'unverified'
    if 'incorrect' in values:
        return 'incorrect'
    if 'unverified' in values:
        return 'unverified'
    if all(x == 'correct' for x in values):
        return 'correct'
    if any(x in ['correct','partial'] for x in values):
        return 'partial'
    if 'error' in values:
        return 'error'
    if all(x == 'unsupported' for x in values):
        return 'unsupported'
    return 'missing'


def build_case(cid, feature, selected, changes=None, additions=None, scenario='conditional-copy', reword=None):
    changes = changes or {}
    atoms = []
    pieces = []
    for key in selected:
        s = copy.deepcopy(bykey[key])
        s.update(changes.get(key, {}))
        if reword and key in reword:
            s['text'] = reword[key]
        pieces.append(s)
    pieces.extend(copy.deepcopy(additions or []))
    raw = '\n'.join(p['text'] for p in pieces)+'\n'
    offset = 0
    for i, s in enumerate(pieces):
        n = len(s['text'].encode('utf-8'))
        aid = 'a%02d' % (i+1)
        is_extra = s.get('required_id') is None
        c = s.get('correctness','correct')
        g = s.get('grounding','correct')
        refs = [copy.deepcopy(r) for token in s['citation_ids'] for r in citations[token]['evidence']]
        truth_refs = [copy.deepcopy(r) for token in s.get('truth_citation_ids',s['citation_ids']) for r in citations[token]['evidence']]
        atoms.append(dict(atom_id=aid, raw_utf8_span=[offset,offset+n], raw_quote=s['text'],
                          subject=s['subject'], property=s['property'], value=s['value'],
                          conditions={'shared_context':conditions['id'],'scenario':scenario,'evidence_mode':'authored-conditional-only'},
                          required_id=s.get('required_id'), slot=s.get('slot'), extra_id=('extra-'+aid if is_extra else None),
                          original_output_evidence=refs, truth_evidence=truth_refs,
                          context_evidence=([{'locator':'/conditions/execution_record','sha256':H(json.dumps(conditions['execution_record'],sort_keys=True,separators=(',',':')).encode())}, {'locator':'/conditions/scenarios/'+scenario,'sha256':H(json.dumps(conditions['scenarios'][scenario],sort_keys=True,separators=(',',':')).encode())}] if 'V' in s['citation_ids'] else []),
                          citation_ids=s['citation_ids'], citation_support_decision=s.get('citation_support_decision','supports complete asserted content under conditional context'),
                          correctness=c, grounding=g, duplicate_of=s.get('duplicate_of'), contradicts=s.get('contradicts',[]),
                          rationale=s['rationale'], uncertainty=s.get('uncertainty','author expectation; separate semantic check and human adjudication pending')))
        offset += n+1
    key_to_aid = {s['key']:a['atom_id'] for s,a in zip(pieces,atoms)}
    for a in atoms:
        if a['duplicate_of']:
            a['duplicate_of'] = key_to_aid[a['duplicate_of']]
        a['contradicts'] = [key_to_aid[x] for x in a['contradicts']]
    # Split independent scalar assertions in conjunctions while retaining the exact
    # shared sentence span. Universal byte identity and complete-set relations
    # remain single relational atoms; their enumerated scope is not discarded.
    expanded = []
    expansion = {}
    for a, s in zip(atoms, pieces):
        components = None
        if isinstance(a['value'], dict):
            components = [(a['subject'], a['property']+'.'+k, v) for k,v in a['value'].items()]
        elif s['key'] == 'p2':
            components = [(a['subject'], 'complementary_byte_identity', True),
                          ('AF PPL/Bld_autoIncrement original/expected', 'literal_text', 'true')]
        elif s['key'] == 'p8':
            components = [('immutable original project', 'before_after_byte_identity', True),
                          ('immutable MIT notice', 'before_after_byte_identity', True),
                          ('immutable original and notice', 'outside_writable_root', True)]
        elif s['key'] == 'l0':
            components = [('actual WP1 text correctness trial', 'execution_status', 'unexecuted'),
                          ('actual WP1 root declaration trial', 'execution_status', 'unexecuted')]
        components = components or [(a['subject'],a['property'],a['value'])]
        expansion[a['atom_id']] = []
        for j,(subject,prop,value) in enumerate(components):
            b = copy.deepcopy(a)
            b['atom_id'] = a['atom_id']+'.'+str(j+1)
            b['subject'],b['property'],b['value'] = subject,prop,value
            b['assertion_group'] = a['atom_id']
            b['rationale'] += ' Atomic component: '+prop+'. The shared quoted sentence supplies the exact raw span, including conjunctive or anaphoric context.'
            expansion[a['atom_id']].append(b['atom_id'])
            expanded.append(b)
    for a in expanded:
        if a['duplicate_of']:
            target = [b for b in expanded if b['atom_id'] in expansion[a['duplicate_of']] and b['property']==a['property']]
            a['duplicate_of'] = target[0]['atom_id'] if target else expansion[a['duplicate_of']][0]
        targets = [b for old in a['contradicts'] for b in expanded if b['atom_id'] in expansion[old]]
        # The retained assertion 'output remains 2' contradicts output=3,
        # not the original=2 or the property's type/childlessness.
        if a['property'] == 'output_literal_text':
            targets = [b for b in targets if b['property'].endswith('.after')]
        a['contradicts'] = [b['atom_id'] for b in targets]
    atoms = expanded
    items = []
    for rid, required_slots in slots.items():
        aa = [a for a in atoms if a['required_id']==rid]
        present = set(a['slot'] for a in aa)
        missing = [x for x in required_slots if x not in present]
        item = {'id':rid,'atom_ids':[a['atom_id'] for a in aa], 'required_slots':required_slots,'missing_slots':missing}
        for dim in ['correctness','grounding']:
            vals = [a[dim] for a in aa]
            if not vals:
                v = 'missing'
            elif 'incorrect' in vals:
                v = 'incorrect'
            elif 'unverified' in vals:
                v = 'unverified'
            elif missing or any(x!='correct' for x in vals):
                v = 'partial'
            else:
                v = 'correct'
            item[dim] = v
        item['rationale'] = 'Apply the unchanged required-ID tests independently in each dimension; retain every missing slot. Duplicate atoms earn credit once. A cited support relation is itself tested for truth.'
        items.append(item)
    extras = [a['atom_id'] for a in atoms if a['required_id'] is None]
    whole = {dim:assessment([x[dim] for x in items]+[a[dim] for a in atoms if a['required_id'] is None]) for dim in ['correctness','grounding']}
    counts = {dim:{o:sum(x[dim]==o for x in items) for o in outcomes} for dim in ['correctness','grounding']}
    extra_counts = {dim:{o:sum(a[dim]==o for a in atoms if a['required_id'] is None) for o in outcomes} for dim in ['correctness','grounding']}
    cases.append({'id':cid,'scenario':scenario,'shared_context':conditions['id'],'raw_answer':raw,'raw_utf8_bytes':len(raw.encode('utf-8')),'raw_utf8_sha256':H(raw.encode('utf-8'))})
    expectations.append({'id':cid,'author_design_feature':feature,'raw_utf8_sha256':H(raw.encode('utf-8')),'atoms':atoms,'required_items':items,'extras':extras,
                         'duplicates':[{'atom_id':a['atom_id'],'duplicate_of':a['duplicate_of']} for a in atoms if a['duplicate_of']],
                         'contradictions':[{'atom_id':a['atom_id'],'contradicts':a['contradicts']} for a in atoms if a['contradicts']],
                         'assessment':whole,'required_counts':counts,'extra_counts':extra_counts,'required_denominator_per_dimension':3,
                         'artifact_results':'No new artifact/native result is scored; conditional byte/inventory comparisons remain preparation evidence. Abstention supplies no artifact or map.',
                         'status':'authored-expectation-pending-separate-check'})

allkeys = [s['key'] for s in specs]
build_case('C1-0125-N01-v1','supported positive comparator',allkeys)
build_case('C1-0125-N02-v1','equivalent conjunction and paraphrase',allkeys,reword={
    'd1':'For the selected childless Int build field under My Computer → Build Specifications → AF PPL, the original numeral is 2 and its conditional replacement is 3. [B,Q]',
    'd2':'One ASCII substitution at offset 3347 (line 42) is the entire difference, and the two complete project byte objects each occupy 5806 bytes. [W,Q]',
    'p7':'Both roots spell their type as Project and their LVVersion as 20008000. [R]',
    'l9':'Reading 20008000 at the project root establishes a declaration only; it establishes no native save-version preservation. [R,V,Q]'})
# Delta and its support/complement relations are absent, rather than silently copied from the references.
extra_auto = dict(key='extra-auto',text='Additionally, the paired AF PPL autoIncrement declaration reads true. [A]',subject='AF PPL/Bld_autoIncrement original/expected',property='literal_text',value='true',required_id=None,slot=None,citation_ids=['A'],rationale='Original line 33 and corresponding expected line 33 support this true extra; it cannot fill the omitted build delta or missing map relations.')
build_case('C1-0125-N03-v1','omitted delta and incomplete map with true extra',[k for k in allkeys if k not in ['d1','d2','p1','p2']],additions=[extra_auto])
build_case('C1-0125-N04-v1','resolvable non-supporting citation',allkeys,changes={
    'd1':{'text':'In this conditional copy, AF PPL’s childless Int property Bld_version.build changes from the literal 2 to the literal 3. [J,Q]','citation_ids':['J','Q'],'truth_citation_ids':['B','Q'],'grounding':'incorrect','citation_support_decision':'J resolves to Bld_version.major=1 in both objects and does not support the asserted build transition; Q supplies a request, not corresponding output evidence.','rationale':'Independent B evidence makes the delta true; submitted J evidence makes grounding incorrect without changing delta truth.'},
    'p1':{'text':'The original and expected-output major-property locations substantiate that build-text transition. [J]','subject':'paired Bld_version.major locations','property':'support_relation','value':'support build 2-to-3 text transition','citation_ids':['J'],'truth_citation_ids':['B','J'],'correctness':'incorrect','grounding':'incorrect','citation_support_decision':'resolvable but non-supporting: major is 1 in both objects','rationale':'The explicitly asserted major-to-build support relation is false. This relational correctness failure is independent of the delta statement being true.'}})
dupe = copy.deepcopy(bykey['d1'])
dupe.update(key='d-repeat',text='Put another way, that same selected build text goes from 2 to 3. [B,Q]',value={'before':'2','after':'3'},duplicate_of='d1',rationale='Equivalent repetition of d1 earns no additional required-item credit and enlarges no denominator.')
build_case('C1-0125-N05-v1','duplicate assertions',allkeys,additions=[dupe])
neg = copy.deepcopy(bykey['d1'])
neg.update(key='d-neg',text='In that same conditional output, the selected Bld_version.build text is still 2. [B]',property='output_literal_text',value='2',citation_ids=['B'],correctness='incorrect',grounding='incorrect',contradicts=['d1'],citation_support_decision='output selected property is 3, so B refutes the assertion',rationale='Retain d1 and its incompatible output-value assertion. Contradiction makes the affected delta item incorrect in both dimensions.')
negmap = copy.deepcopy(bykey['p1'])
negmap.update(key='p-neg',text='Those same paired build locations therefore support an unchanged build text. [B]',value='support unchanged build text',correctness='incorrect',grounding='incorrect',contradicts=['p1'],citation_support_decision='paired selected locations differ from 2 to 3',rationale='This explicitly contradictory false support relation also makes the required relational map item incorrect, without erasing the correct relation.')
build_case('C1-0125-N06-v1','contradiction with matching keywords',allkeys,additions=[neg,negmap])
pred = dict(key='extra-prediction',text='At the next launch, startup will take seven percent less time.',subject='next launch of the edited project',property='startup_time_change',value='minus 7 percent',required_id=None,slot=None,citation_ids=[],truth_citation_ids=['V'],correctness='unverified',grounding='missing',citation_support_decision='no submitted citation; no runtime evidence exists',rationale='No independent startup measurement or fixture exists; the prediction is unverified, not established false. Missing grounding on the extra yields partial whole-answer grounding under L41.',uncertainty='Future runtime effect unknown; no native execution may be inferred.')
build_case('C1-0125-N07-v1','unverified extra assertion',allkeys,additions=[pred])
abst = dict(key='abstain',text='I cannot supply an edited project or an original/output map in this scenario. [V]',subject='this abstention submission',property='delivered_project_and_map',value='absent',required_id=LID,slot='text_and_root_trials',citation_ids=['V'],rationale='The frozen abstention scenario explicitly supplies neither project nor map. Truthful inability earns only honest-limits credit; all delta/map slots remain missing.')
build_case('C1-0125-N08-v1','honest abstention',[k for k in allkeys if k.startswith('l')],additions=[abst],scenario='abstention')

public = {'schema':1,'revision':'c1-challenges-0125-v1','issue':597,'status':'public-development-authored-challenges','benchmark_ready':False,
          'author_exposure':{'provider':'codex','model':'gpt-6.1-sol','role':'benchmark','exposed':True,'human':False,'independent_checker':False,'startup_label':'claude-sonnet-5-5','model_continuity':'uncertified; staged startup label differs from current candidate'},
          'withheld':False,'model_unseen':False,'conditions':conditions,'citation_registry':citations,'cases':cases}
expect = {'schema':1,'revision':'c1-challenges-0125-expectations-v1','issue':597,'status':'author-expectations-pending-separate-check','benchmark_ready':False,
          'scope':'Only exact linked authored raw answers under the frozen conditional context. These expectations and bookkeeping are not executed human results, a general narrative scorer or an established/full-trial key.',
          'authority':[ref(M,'/common/answer_rule'),ref(M,'/tasks/4'),ref(K,'/required_ids/5'),ref(K,'/required_ids/6'),ref(K,'/required_ids/7'),ref(K,'/claim_adjudication'),ref('benchmark/protocol.md','L29'),ref('benchmark/protocol.md','L35'),ref('benchmark/protocol.md','L36'),ref('benchmark/protocol.md','L40'),ref('benchmark/protocol.md','L41')],
          'required_slot_inventory':slots,'inherited_denominators':core['claim_adjudication']['required_denominators'],
          'inheritance':'0119 tests remain operative unchanged. 0123 reviewed conditional evidence is reused, never revised. Historical F4 slots/general established-key/full-trial use remain blocked; C1 human adjudication remains open.',
          'accounting_rule':'Evaluate correctness and grounding independently per atom and required ID. Map correctness tests relational truth, grounding resolves submitted support. Keep omissions, duplicates, contradictions and all extras; compute whole answers separately using protocol L41. True extras cannot fill missing required slots.',
          'cases':expectations,'pending':{'independent_agent_check':True,'human_execution':True,'owner_acceptance':True,'native_checks':True,'trials':True}}
for name, obj in [('c1-challenges-0125-cases.json',public),('c1-challenges-0125-expectations.json',expect)]:
    p=BASE/name
    if p.exists():
        raise SystemExit('Refusing to overwrite '+str(p))
    p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'cases':len(cases),'expectations':len(expectations),'assessments':{e['id']:e['assessment'] for e in expectations}},indent=2))
