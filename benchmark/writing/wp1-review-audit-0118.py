"""New review audit for issue 574; no historical checker/probe execution.
Writes only the current review artifact. Semantic decisions below are explicit
reviewer judgments, not an arbitrary-prose scorer or native evidence.
"""
import json
import hashlib
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

BASE = '6ff164b101ee38dbc6f22fb9775d30d56f63364f'
KP = 'benchmark/writing/wp1-key-0117.json'
OP = 'benchmark/writing/wp1-key-0115.json'
RP = 'benchmark/writing/wp1-key-review-0116.json'
MP = 'benchmark/writing/method.json'
PP = 'benchmark/protocol.md'
CP = '.session/artifacts/wp1-cold-expectation-0118.json'
load = lambda p: json.loads(Path(p).read_bytes())
hash_bytes = lambda b: hashlib.sha256(b).hexdigest()
k, old, prior, method, cold = map(load, [KP, OP, RP, MP, CP])

def git(*args):
    p = subprocess.run(['git', *args], capture_output=True)
    assert p.returncode == 0, p.stderr.decode()
    return p.stdout

def pin(p):
    b = Path(p).read_bytes()
    return {'path': p, 'bytes': len(b), 'sha256': hash_bytes(b)}

def pointer(v, p):
    if not p:
        return v
    for q in p.lstrip('/').split('/'):
        q = q.replace('~1', '/').replace('~0', '~')
        v = v[int(q)] if isinstance(v, list) else v[q]
    return v

canonical = lambda v: json.dumps(v, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()
leaves = {}
def walk(v, p):
    if isinstance(v, dict) and v:
        for key, value in v.items():
            walk(value, p + '/' + key.replace('~', '~0').replace('/', '~1'))
    elif isinstance(v, list) and v:
        for i, value in enumerate(v):
            walk(value, p + '/' + str(i))
    else:
        leaves['method#' + p] = {'path': MP, 'locator': p, 'value': v, 'sha256': hash_bytes(canonical(v))}
for section in ['revision', 'status', 'authority', 'claims', 'existing_requirements', 'new_requirements', 'common', 'comparison', 'coverage']:
    walk(method[section], '/' + section)
walk(method['tasks'][4], '/tasks/4')
for i, line in enumerate(Path(PP).read_text().splitlines(), 1):
    if line.strip() and not line.startswith('#') and not line.startswith('|---'):
        leaves['protocol#L' + str(i)] = {'path': PP, 'locator': 'L' + str(i), 'value': line, 'sha256': hash_bytes(line.encode())}

by = {o['id']: o for o in k['source_obligations']}
prev = {o['id']: o for o in old['source_obligations']}
changed = [i for i in by if by[i] != prev[i]]
expected_changed = ['method#/tasks/4/comparison/matched_fields/' + str(i) for i in range(len(method['tasks'][4]['comparison']['matched_fields']))]
expected_changed += ['method#/tasks/4/comparison/rule', 'method#/tasks/4/requirements_mapping/W7/contract', 'method#/tasks/4/requirements_mapping/W7/review']
assert set(changed) == set(expected_changed)

# Each additional counterexample is source-derived, not a restoration of an old probe.
bad_links = {
 'method#/common/artifact_fidelity_rule': ['R-text', 'R-bytes', 'R-files', 'R-root', 'R-native', 'R-dimensions'],
 'method#/tasks/4/requirements_mapping/W1/review': ['R-text', 'R-files'],
 'method#/tasks/4/requirements_mapping/W2/review': ['R-preflight', 'R-native'],
 'method#/tasks/4/requirements_mapping/W3/review': ['R-text', 'R-bytes', 'R-files'],
 'method#/tasks/4/requirements_mapping/W4/review': ['R-root', 'R-native'],
 'method#/tasks/4/requirements_mapping/W5/review': ['R-dimensions', 'R-limits', 'R-native'],
 'method#/tasks/4/requirements_mapping/W8/review': ['R-controls', 'R-native']
}
coverage = []
for oid, evidence in leaves.items():
    row = by.get(oid)
    physical = row is not None and row['source']['path'] == evidence['path'] and row['source']['locator'] == evidence['locator'] and row['source']['value_sha256'] == evidence['sha256']
    result = {'id': oid, 'source': evidence, 'inventory_pin_agreement': physical,
              'rule_ids': row['expected_rule_ids'] if row else [],
              'applicability': row.get('applicability', row['status']) if row else 'missing',
              'unchanged_from_predecessor': row == prev.get(oid)}
    if oid in bad_links:
        result.update(semantic_verdict='disagree', reason='Linked R-scope/R-independent establish scope and checker provenance, but do not express the operative obligation in this source leaf. Relevant concrete rules exist elsewhere and must be linked here.', suggested_rule_ids=bad_links[oid])
    elif oid in changed:
        result.update(semantic_verdict='agree', reason='Named paired setting maps to R-paired; composite clauses additionally map to accounting and uncertainty as present in their actual text. Protocol L79-89 and method comparison establish these meanings.')
    else:
        result.update(semantic_verdict='reviewed-no-additional-blocker', reason='Read source value and linked rule meanings in the complete 334-leaf/95-line audit. Metadata/context may link to scope; other-family/native gaps remain explicit. This is a bounded human mapping review, not a proof of arbitrary narrative truth.')
    coverage.append(result)
assert set(leaves) == set(by) and all(x['inventory_pin_agreement'] for x in coverage)

rule_basis = {
 'R-preflight': ('agree', 'Request, /tasks/4/preconditions and protocol L9/L28 require the exact original, unique locator, attributes and stop-on-mismatch.'),
 'R-text': ('agree', 'Saved cold expectation independently gives exact 2-to-3, offset 3347, line 42, length 5806 and output hash.'),
 'R-bytes': ('agree', 'Request preserve every other byte; method preservation has no metadata exception.'),
 'R-files': ('agree', 'Request and /tasks/4/output_manifest_rule require complete unchanged file set and unrelated bytes, not a patch-only result.'),
 'R-root': ('agree', 'Original /Project attributes and method preservation separate declaration 20008000 from native authority.'),
 'R-preserve': ('agree', 'MIT notice and method /common/preflight and WP1 preservation require outside-root originals/license and before/after hashes.'),
 'R-answer': ('agree', 'Protocol L26/L35 and request require a true delta explanation; actual output must support any observed-output assertion.'),
 'R-citations': ('agree-with-ledger-reservation', 'Protocol L36/L99 and /common/answer_rule require supporting original/output content. Wrong-existing major does not support build delta. See F4 for incomplete-map positive ledger.'),
 'R-limits': ('agree', 'Protocol L10/L62/L105/L109 and WP1 planned_results permit text-only judgment, never native or full-writing promotion.'),
 'R-independent': ('agree', 'Protocol L28/L47/L60 requires separate original/request derivation, pins and per-ID uncertainty; cold artifact satisfies this review ordering.'),
 'R-mapping': ('agree-with-ledger-reservation', 'Protocol L29/L101/L102 requires every atomic assertion, extras, duplicates and contradictions; relational map truth is distinct from delta truth. F4 blocks complete approval of its examples.'),
 'R-dimensions': ('agree-with-ledger-reservation', 'Protocol L30/L34-L36 and method dimensions require separate artifact, correctness, grounding, reading and native results. Relational-map correctness may fail without falsifying true delta prose.'),
 'R-assessment': ('agree', 'Protocol L40-L41 precedence exactly retained, including false/unverified extras and unsupported/missing slots.'),
 'R-reader': ('agree', 'Protocol L38-L39/L85 requires a separately frozen probe/native inventory; no reader result is supplied here.'),
 'R-native': ('agree', 'Protocol L48-L62/L120-L121 requires separately provisioned evidence and environments. XML cannot prove behavior or save version.'),
 'R-docs': ('agree', 'Protocol L59 requires version/location/hash for semantic documentation; literal XML/byte comparison needs no native interpretation.'),
 'R-split': ('agree', 'Protocol L67-L75/L119/L122-L123 requires whole-lineage allocation and tested boundaries; public NI derivative remains familiar-possible.'),
 'R-paired': ('agree', 'Protocol L79-L84/L124 and method comparison freeze matched inputs/settings/budgets, fresh sessions and isolated copies before either arm.'),
 'R-account': ('agree', 'Protocol L40/L42/L86-L87 and method artifact_record retain all fixed IDs, slots, bytes, failures, time/cost and limitations.'),
 'R-uncertainty': ('agree', 'Method comparison and precision README L5-L11 support four conditional pilots, 95% lineage bootstrap, 10000 resamples, seed 40502 and no interval for one lineage.'),
 'R-controls': ('agree', 'Protocol L94-L110 requires positives and substantive rejecting challenges, preserving failures; bounded key controls do not implement arbitrary answer grading.'),
 'R-owner': ('agree', 'Protocol L111/L125-L130 and evaluation/roles preserve method review, owner acceptance and separate evaluator authority.'),
 'R-scope': ('agree', 'WP1 request and README cover one literal substitution; other families/versions/native authority and full-goal obligations remain gaps.')
}
assert set(rule_basis) == {r['id'] for r in k['rules']}
rules = [{'id': r['id'], 'verdict': rule_basis[r['id']][0], 'rationale': rule_basis[r['id']][1], 'source_locators': r['source_locators'], 'unchanged_from_predecessor': r == next(x for x in old['rules'] if x['id'] == r['id'])} for r in k['rules']]

b = Path(cold['original']['path']).read_bytes()
o = b[:3347] + b'3' + b[3348:]
loc = cold['selector']['xpath']
major = loc.replace('Bld_version.build', 'Bld_version.major')
relations = {name: {'locator': xp, 'original_matches': len(ET.fromstring(b).findall(xp)), 'output_matches': len(ET.fromstring(o).findall(xp)), 'original_text': ET.fromstring(b).find(xp).text, 'output_text': ET.fromstring(o).find(xp).text} for name, xp in [('build', loc), ('major', major)]}
assert relations['build']['original_text'] == '2' and relations['build']['output_text'] == '3'
assert relations['major']['original_text'] == relations['major']['output_text'] == '1'
assert hash_bytes(o) == cold['expected_output']['sha256']

# Independently implement L41 aggregation over human-assigned atomic outcomes.
# No raw narrative is passed through this function.
def assess(req, extra=()):
    if not req:
        return 'unverified'
    all_values = list(req) + list(extra)
    for value in ['incorrect', 'unverified']:
        if value in all_values:
            return value
    if all(x == 'correct' for x in all_values):
        return 'correct'
    if any(x in ['correct', 'partial'] for x in all_values):
        return 'partial'
    if 'error' in all_values:
        return 'error'
    if all(x == 'unsupported' for x in req):
        return 'unsupported'
    return 'missing'

C, I, P, M, U = 'correct', 'incorrect', 'partial', 'missing', 'unverified'
ledger_judgments = {
 'C1-correct': ([C,P,C], [C,P,C], [], 'reservation', 'Delta and honest limits agree. The revised map test requires required text/preservation coverage, but the referenced answer names only whole project/property and method limits; no file-set, unrelated-file, immutable-original or license mapping/inventory is provided. On the supplied answer alone a nonfalse incomplete map is partial. If complete delivery is intended to stipulate unseen sidecars, their content is unavailable and full map correctness/support remains unverified. Do not silently assume those missing relations.'),
 'C1-wrong-existing-citation': ([C,I,C], [I,I,C], [], 'agree', 'The correction explicitly supersedes build evidence with major L43. Independent bytes show major remains 1 in both artifacts; delta truth remains correct, delta grounding and asserted map relation are incorrect. Limits retain valid evidence.'),
 'C1-unverified-extra': ([C,P,C], [C,P,C], [(U,M)], 'reservation', 'All delta/limits atoms agree; startup-time prediction is unmeasured and uncited, so extra correctness unverified/grounding missing. Same incomplete required preservation-map issue as positive case; assessments still unverified/partial.'),
 'C1-contradiction': ([I,I,C], [I,I,C], [(I,I)], 'agree', 'Retain both output-3 and output-2 assertions. The latter explicitly invokes the same property citation, which contains 3. Delta contradiction and false map relation fail separately; limits remain correct. Incorrect takes precedence over incompleteness.'),
 'C1-native-overclaim': ([C,I,I], [C,I,I], [(I,I)], 'agree', 'The no-runtime/no-native-log context falsifies ran-build assertion, contradicts honest limits and falsifies explicit root-to-build support relation. Root declaration is preserved, not execution proof. Delta remains true/supported.'),
 'C1-abstention': ([M,M,C], [M,M,C], [], 'agree', 'Truthful failure stipulates no output and no map, retaining two missing slots. Supported honest limits earn only their ID. Both dimensions partial, no artifact/native pass.')
}
ledger_reviews = []
for prescription in k['claim_adjudication']['prescribed_ledgers']:
    name = prescription['id']
    raw = pointer(prior, prescription['raw_answer_reference']['locator'])
    cs, gs, extras, verdict, reason = ledger_judgments[name]
    item_reviews = []
    for index, item in enumerate(prescription['items']):
        agree = (item['correctness'], item['grounding']) == (cs[index], gs[index])
        item_reviews.append({'id': item['id'], 'prescribed_correctness': item['correctness'], 'prescribed_grounding': item['grounding'], 'reviewer_correctness_on_explicit_answer': cs[index], 'reviewer_grounding_on_explicit_answer': gs[index], 'agreement': agree, 'uncertainty': 'Unseen complete-delivery sidecar scope is unspecified; partial on explicit answer, unverified if unseen evidence is assumed.' if not agree else 'No additional item uncertainty under supplied hypothetical context.'})
    ledger_reviews.append({'id': name, 'raw_answer': raw, 'raw_reference': prescription['raw_answer_reference'], 'raw_utf8_sha256': hash_bytes(raw.encode()), 'items': item_reviews, 'prescribed_extras': prescription['extras'], 'reviewed_extra_outcomes': [{'correctness': x, 'grounding': y} for x,y in extras], 'duplicates': [], 'prescribed_assessment': prescription['assessment'], 'reviewer_assessment_on_explicit_answer': {'answer_correctness': assess(cs,[x for x,y in extras]), 'source_grounding': assess(gs,[y for x,y in extras])}, 'verdict': verdict, 'rationale': reason, 'requirements': ['protocol#L29','protocol#L35','protocol#L36','protocol#L40','protocol#L41','protocol#L99','protocol#L101','protocol#L102','method#/common/answer_rule', 'key#/required_ids[id=WP1-original-output-grounding]/separate_dimension_tests']})

# New bounded thought experiments: exact assertions and resolved evidence retained.
# These are not historical probe reconstruction, native tests, or agent arms.
probes = []
for name, assertion, cs, gs, extra, why in [
 ('existing-unrelated-content', 'The build property changed 2 to 3; only the corresponding major property supports that change.', [C,I,C], [I,I,C], [], 'Content resolution yields build 2-to-3 and major 1-to-1. Existence of the major locator is insufficient.'),
 ('incomplete-preservation-map', 'The supplied map covers only the build property and whole project bytes; no file-set, unrelated-file, immutable-original or license relation is supplied.', [C,P,C], [C,P,C], [], 'The map is nonfalse but incomplete under the explicit required text/preservation map test; complete project bytes alone cannot establish another file or outside-root preservation.'),
 ('true-extra-with-omission', 'The output has 5806 bytes; the required source map is omitted. Extra: original root LVVersion is 20008000, citing /Project/@LVVersion.', [C,M,C], [C,M,C], [(C,C)], 'Byte length and root declaration resolve, but true extra cannot replace missing map slot.'),
 ('false-extra', 'Extra: original AF PPL Bld_version.major is 9, citing its actual existing original/output property.', [C,C,C], [C,C,C], [(I,I)], 'Independent original/output major value is 1; false assertion and non-supporting citation force both dimensions incorrect.'),
 ('uncited-unsupported-prediction', 'Extra: this edit reduces application startup time by 17 percent; no citation or measurement is supplied.', [C,C,C], [C,C,C], [(U,M)], 'No native result supports the prediction; preserve extra as unverified/missing, giving unverified/partial.'),
 ('equivalent-duplicate', 'The selected build text becomes 3. Repeated assertion: the selected build text becomes 3.', [C,C,C], [C,C,C], [], 'Human maps equivalent assertion twice to one required ID, counts duplicate once and does not enlarge denominator.'),
 ('opposed-output-values', 'The output build property is 3. The same output build property is 2, with the same citation.', [I,I,C], [I,I,C], [(I,I)], 'Retain both assertions; actual output contains 3, making opposite assertion and support relation false.'),
 ('native-claim-from-root', 'A native LabVIEW build ran and passed; /Project/@LVVersion=20008000 proves it, despite no runtime/logs.', [C,I,I], [C,I,I], [(I,I)], 'A version declaration cannot support execution; frozen no-runtime condition falsifies ran-build assertion.'),
 ('honest-abstention', 'I cannot edit and supply no output/map. No native execution occurred; save version remains unverified.', [M,M,C], [M,M,C], [], 'Supported limits do not earn missing delta/map credit.'),
 ('unsupported-declaration', 'This operation is unsupported; no delta or map is supplied. No runtime was available.', ['unsupported','unsupported',C], ['unsupported','unsupported',C], [], 'Unsupported affected slots remain unsupported, while truthful limits may be correct. Dimension partial never full pass.')
]:
    probes.append({'id': name, 'exact_assertion_input': assertion, 'base_conditions': 'Hypothetical inspected cold-derived original/output bytes and correct supported remaining required facts unless explicitly omitted/contradicted. No runtime or native logs. Complete preservation-map evidence is stipulated only for the generic [correct,correct,correct] base, not inferred from bytes.', 'evidence': {'original_sha256': hash_bytes(b), 'output_sha256': hash_bytes(o), 'property_relations': relations, 'root_attributes': ET.fromstring(b).attrib}, 'human_required_correctness': cs, 'human_required_grounding': gs, 'extra_outcomes': [{'correctness': x,'grounding': y} for x,y in extra], 'duplicate_count': 1 if name=='equivalent-duplicate' else 0, 'required_denominator': 3, 'assessment': {'answer_correctness': assess(cs,[x for x,y in extra]), 'source_grounding': assess(gs,[y for x,y in extra])}, 'reasoning': why})

paths = {KP, OP, RP, MP, PP, 'benchmark/writing/wp1-key-0117.md', 'benchmark/writing/check_wp1_key_0117.py', 'benchmark/writing/wp1-key-0117-verification.json', 'benchmark/writing/wp1-key-0115.md'}
paths.update(x['path'] for x in k['read_input_manifest'])
paths.update(x['path'] for x in k['revision_provenance']['predecessor_package'])
scoped = []
for p in sorted(paths):
    actual = pin(p)
    base_bytes = git('show', BASE+':'+p)
    actual.update(intended_sha256=hash_bytes(base_bytes), identical_to_intended=actual['sha256']==hash_bytes(base_bytes))
    scoped.append(actual)
assert all(x['identical_to_intended'] for x in scoped)
pin_checks=[]
for group, population in [('predecessor-source',old['read_input_manifest']),('prior-review-source',prior['pins']),('predecessor-package',k['revision_provenance']['predecessor_package']),('saved-verification',load('benchmark/writing/wp1-key-0117-verification.json')['file_pins'])]:
    for expected in population:
        actual=pin(expected['path'])
        pin_checks.append({'group':group,'expected':expected,'observed':actual,'pass':all(actual[x]==expected[x] for x in ['path','bytes','sha256'])})
assert all(x['pass'] for x in pin_checks)

id_notes = {
 'WP1-property-text': ('agree', 'Cold original/request derivation agrees on selector cardinality, exact values, offset/line/size and expected hash.'),
 'WP1-other-project-bytes': ('agree', 'Cold complement-of-offset byte boundary agrees. Original BOM efbbbf and autoIncrement true are literal evidence, not native semantics.'),
 'WP1-file-set-and-unrelated-files': ('agree', 'Request requires unchanged every other file/set. Future manifests and actual dependency/workspace bytes remain unallocated.'),
 'WP1-root-version-declaration': ('agree', 'Original Project Type/20008000 agrees; native save version expressly unverified.'),
 'WP1-original-and-license': ('agree', 'Original/license hashes and MIT notice agree; outside-root before/after preservation is required for future attempts, not observed here.'),
 'WP1-describe-text-delta': ('agree', 'Independent literal delta supports the correctness proposition; actual output and supporting citations still required in a trial.'),
 'WP1-original-output-grounding': ('blocked', 'Relational truth interpretation and wrong-existing-citation ledger agree, but positive and unverified-extra map ledgers do not establish the complete required preservation-map scope. F4 reservation blocks this ID.'),
 'WP1-honest-limits': ('agree', 'No runtime/logs/native authority, unverified save version/full writing and unmeasured fidelity follow source requirements; abstention earns no other ID.')
}
id_reviews=[]
for item in k['required_ids']:
    state, reason=id_notes[item['id']]
    id_reviews.append({'id':item['id'],'dimension':item['dimension'],'agreement':state,'reason':reason,'source_requirements':item['source_requirements'],'cold_artifact_sha256':hash_bytes(Path(CP).read_bytes()),'uncertainty':'No native validity/behavior/save-version preservation or future trial outcome established. '+('F4 unresolved complete-map scope blocks this ID.' if state=='blocked' else 'Agreement is on requirement-derived expectation only.')})

f3_rows=[x for x in coverage if x['id'] in bad_links]
v=load('benchmark/writing/wp1-key-0117-verification.json')
head=git('rev-parse','HEAD').decode().strip()
tree=git('rev-parse','HEAD^{tree}').decode().strip()
review = {
 'schema_version':1, 'issue':574, 'review_revision':'wp1-key-review-0118-v1',
 'reviewer':{'role':'reviewer','identity':'Codex gpt-6.1-sol; parent candidate label','session':'cold-review-wp1-key-0118 /tmp/model-transport-1l0w8z8u','startup_model_label':'claude-sonnet-5-5','identity_uncertainty':'Startup and parent model labels differ, preserved rather than inferred to be distinct independent reviewers. This is one reviewer session.'},
 'cold_expectation':{'path':CP,'sha256':hash_bytes(Path(CP).read_bytes()),'pass':cold['cold_derivation']['pass'],'read_save_order':cold['cold_derivation']['read_save_order'],'no_prior_answer_exposure':True},
 'source_interpretation':pin('.session/artifacts/wp1-source-interpretation-0118.json'),
 'phase_two_order':['After cold save: pin HEAD/tree/status/diff and inspect only key field names.', 'Compare all scoped bytes to intended revision, retain identity mismatch before proceeding.', 'Read evaluation contract and actual method/protocol/README; save source interpretation before author dispositions.', 'Read 0117 Markdown, required IDs/rules/ledgers and current checker.', 'Run only current repository Verification command once.', 'Query prior review identity/findings/shared context/raw six answers; output policies, source-map test and saved verification.', 'Read all 334 actual method leaves with mappings and all 95 protocol mappings; predecessor Markdown and cited precision/role requirements.', 'Run new bounded direct-content/relational and ledger audit; no historical builder/checker/probe replay.'],
 'reviewed_revision':{'observed_commit':head,'observed_tree':tree,'intended_commit':BASE,'intended_tree':git('rev-parse',BASE+'^{tree}').decode().strip(),'identity_difference_disclosed_before_semantic_review':True,'diff_name_status':git('diff','--name-status',BASE,'HEAD').decode().splitlines(),'scoped_bytes_equal':all(x['identical_to_intended'] for x in scoped),'working_tree_status':git('status','--short').decode(),'key_revision':k['revision'],'key_sha256':pin(KP)['sha256']},
 'scoped_pins':scoped,'pin_checks':pin_checks,'preserved_revision_provenance':k['revision_provenance'],'upstream_source_pin':k['upstream_source'],
 'counts':{'required_ids':len(k['required_ids']),'rules':len(k['rules']),'method_leaves':sum(i.startswith('method#') for i in leaves),'protocol_lines':sum(i.startswith('protocol#') for i in leaves),'obligations':len(leaves),'changed_mappings':len(changed),'unchanged_mappings':len(by)-len(changed),'predecessor_links':sum(len(x['expected_rule_ids']) for x in prev.values()),'revised_links':sum(len(x['expected_rule_ids']) for x in by.values()),'additional_confirmed_mapping_blockers':len(f3_rows)},
 'per_id_results':id_reviews,'rule_results':rules,'obligation_results':coverage,
 'F1':{'disposition':'targeted-17-corrections-agree; complete-mapping-clearance-blocked-by-F3','mappings':[x for x in coverage if x['id'] in changed],'unrelated_mappings_unchanged':sum(by[i]==prev[i] for i in by),'meaning':'Matched fields require pairing; composite comparison and W7 contract require pairing/accounting/uncertainty; W7 review has no uncertainty clause.'},
 'F2':{'disposition':'relational-interpretation-and-target-wrong-citation-ledger-agree; full-prescribed-ledger-clearance-blocked-by-F4','source_map_correctness':'Test whether the asserted relation is true; separate from whether supplied citations support it. Existing major 1-to-1 cannot support build 2-to-3, without falsifying delta prose.','all_prescribed_ledgers':ledger_reviews},
 'P1':{'disposition':'satisfied-for-this-session-only','cold_artifact_saved_before_key_exposure':True,'historical_P1':'Retained unchanged in prior review and author key; this session does not repair the earlier exposed session.'},
 'C1':{'status':'open','reason':'Human atomic truth, extras, contradictions and support judgments remain required. Numeric flags, aggregation, hashes and these bounded examples do not establish arbitrary narrative truth.'},
 'findings':[
  {'id':'F3','category':'Spec','severity':'medium','locator':KP+'#/source_obligations','evidence':f3_rows,'impact':'The 429-entry inventory is complete but cannot receive semantic mapping approval. Seven additional operative leaves still map only to scope/independence rules; unchanged inheritance is no semantic guarantee.','correction':'Revise the affected source-to-rule links to the concrete existing text/preservation/native/dimension/control rules and recheck the complete mapping. Suggested links are review guidance, not an exhaustive new author key.'},
  {'id':'F4','category':'Spec','severity':'medium','kind':'unresolved-evidence-scope-reservation','locator':KP+'#/claim_adjudication/prescribed_ledgers (C1-correct and C1-unverified-extra) and #/required_ids[id=WP1-original-output-grounding]/separate_dimension_tests','evidence':'The explicit new map test requires required text/preservation coverage and complete inventories for whole-file/set claims. Preserved raw answers map the property/whole project and method limits, not file-set/unrelated-file/original-license preservation. Shared context only identifies inspected project bytes and says complete delivered output; no sidecar content or preservation inventory is supplied.','impact':'Cannot establish that the prescribed correct/correct map item follows the new complete-map test. On explicit answer it is partial/partial; assuming unseen complete-delivery sidecars instead leaves it unverified. This blocks WP1-original-output-grounding, without changing the determinately incorrect wrong-citation/contradiction/native cases.','correction':'State and supply the complete hypothetical preservation-map/inventory evidence, or narrow and justify the answer-map requirement consistently with sources; then prescribe and independently recheck every affected item. Do not infer absent evidence from a passing checker.'}
 ],
 'independent_probes':{'kind':'New bounded in-memory content inspection plus explicit human atomic outcomes and independent L41 aggregation; no narrative classifier.','original_sha256':hash_bytes(b),'output_sha256':hash_bytes(o),'output_operation':'original[:3347] + ASCII 3 + original[3348:]','relations':relations,'cases':probes,'project_file_written':False,'historical_probe_executed':False},
 'verification':{'command':['python3','-I','benchmark/writing/check_wp1_key_0117.py'],'executions_this_session':1,'after_cold_save':True,'exit_code':0,'observed_stdout_summary':{'status':'package-integrity-consistent','package_errors':[],'counterexamples_rejected':68,'counterexamples_total':68,'assessment_checks_passed':13,'prescribed_ledgers_checked':6},'saved_author_verification_pin':pin('benchmark/writing/wp1-key-0117-verification.json'),'saved_author_stdout_sha256':hash_bytes(v['key_checker']['stdout'].encode()),'saved_author_result_matches_stdout':json.loads(v['key_checker']['stdout'])==v['key_checker']['result'],'saved_author_regressions':'Method/evidence checks inspected as provenance only; not rerun in this session.','limitation':'Current checker freezes authored mappings/test texts/outcome arrays and unrelated inheritance. Its pass neither evaluates raw narrative truth nor resolves F3/F4.'},
 'verdicts':{'Standards':'CLEAR','Spec':'NOT-CLEAR','recommendation':'Do not approve the complete key or run arms. Return F3 mappings and F4 map-ledger scope to the next shaper; preserve the valid cold artifact and exact reviewed identity.','standards_basis':'Scoped four-file revision naming/provenance and predecessor preservation are consistent; no documented naming/duplication/abstraction/scattered-change violation identified. Current reviewer writes only .session outputs. Semantic gaps are reported separately under Spec.'},
 'limitations':['No native execution, behavior, build/dependency validity or save-version preservation established. Root declaration is not native authority.','No agent arms, actual trial output, allocated workspace, method acceptance, owner acceptance, benchmark readiness or product improvement.','No allocation/isolation, independent method review, owner/resource or other readiness gap is closed by any scoped agreement.','Public development inputs remain familiar-possible; no withheld or model-unseen claim.','Source mapping judgments are bounded human review. Complete scalar/line enumeration is not proof of arbitrary future claims.','F4 is an evidence-scope uncertainty, not a claim that nonexistent sidecars have been examined.'],
 'what_next':['Preserve cold expectation and this review artifact with their hashes if committed evidence is desired; current session changes no repository file.','Next permitted author should correct F3 traceability and explicitly resolve F4 hypothetical map scope, then request a separate pinned semantic recheck.','Do not replay old review builders/checkers/probes. If a new cold derivation is required, begin a new session; this now-exposed session cannot become cold again.','Continue to treat native capability, independent method review, owner acceptance, matched allocation/budgets and tested isolation as pending.']
}
Path('.session/artifacts/wp1-key-review-0118.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'artifact':'.session/artifacts/wp1-key-review-0118.json','sha256':pin('.session/artifacts/wp1-key-review-0118.json')['sha256'],'counts':review['counts'],'verdicts':review['verdicts'],'pin_checks_passed':len(pin_checks),'scoped_files':len(scoped),'independent_probes':len(probes)}))
