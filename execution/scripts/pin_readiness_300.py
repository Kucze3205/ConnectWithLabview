#!/usr/bin/env python3
"""Land the reviewed #169 readiness case and record re-review #298 (Policymaker #300).

Hash-gated and idempotent. Writes benchmark/native/readiness-case.json from the
#292 proposal (review #297 accept), replaces two stale limitation sentences in
preparation-status.json, pins the case under the oracle milestone and re-pins
every preparation-status.json reference. Delete this script after the landing merges.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SNAPSHOT = ROOT / '.github/loop/data/session-reports/292/d44dc4373002008469d9f40f42a57d5dc46834d08b60e7d434b6ef4bb140c382.json'
BLOCK_SHA = 'bb6c4a41daaaab377b9be8bdd7d4613e1b2dcf6496aac8da77dc48ea177ffc09'
CASE = 'benchmark/native/readiness-case.json'
STATUS = 'benchmark/preparation-status.json'
PREP = 'benchmark/preparation.json'
STATUS_BEFORE = 'ed298a8588814152b869024ecc45fbe84050dee70fc4876fb173a15601365a26'
REPLACEMENTS = [
    ('the two non-blocking checker findings of #273 were fixed by #281 (not independently re-reviewed)',
     'the two non-blocking checker findings of #273 were fixed by #281 (re-review #298 confirmed the live '
     'mutation checks and exact reasons; its own revert harness was masked, so Policymaker #300 reverted '
     'each fix in a temporary copy and --check exited 1 both times)'),
    ('its one disclosure finding was fixed by the landed diagram-difference gap row, which was not re-reviewed)',
     'its one disclosure finding was fixed by the landed diagram-difference gap row, accepted by re-review #298)'),
]
APPEND = (
    ' The readiness case benchmark/native/readiness-case.json (proposal #292, review #297 accept) lists saved-property'
    ' expectations for two public pylavi VIs from pylavi/tests/test.yaml: property expectations only, not confirmed in'
    ' LabVIEW, native API mapping unknown, controlled I/O stays a gap, capability #169 is not ready and nothing native'
    ' is executed. Authors and reviewers of #292, #297 and #298 are GPT-family models (codex gpt-6.1-sol, copilot'
    ' gpt-5.6-luna); #298 ended partial on input budget after writing its verdicts.'
)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def dump(value):
    return (json.dumps(value, indent=2, sort_keys=True) + '\n').encode()


def require(ok, message):
    if not ok:
        raise SystemExit('pin_readiness_300 failed: ' + message)


def case_bytes():
    body = json.loads(SNAPSHOT.read_text(encoding='utf-8'))['report']['body']
    blocks = re.findall(r'```json\n(.*?)```', body, re.S)
    require(len(blocks) == 1, 'expected one JSON block in the #292 snapshot')
    require(sha(blocks[0].encode()) == BLOCK_SHA, 'proposal block hash differs from the reviewed block')
    data = json.loads(blocks[0])
    require(data['capability_169_ready'] is False and data['native_executed'] is False, 'proposal claims readiness')
    return dump(data)


def main():
    case = case_bytes()
    case_path = ROOT / CASE
    if case_path.exists():
        require(case_path.read_bytes() == case, CASE + ' exists with different bytes')
    else:
        case_path.write_bytes(case)

    status_path = ROOT / STATUS
    raw = status_path.read_bytes()
    status = json.loads(raw)
    text = status['limitations']
    if sha(raw) == STATUS_BEFORE:
        for old, new in REPLACEMENTS:
            require(text.count(old) == 1, 'limitation sentence not found once: ' + old[:60])
            text = text.replace(old, new)
        status['limitations'] = text + APPEND
        status_path.write_bytes(dump(status))
    else:
        require(all(new in text for _, new in REPLACEMENTS) and text.endswith(APPEND),
                STATUS + ' is neither the expected input nor the expected output')
    status_sha = sha(status_path.read_bytes())

    prep_path = ROOT / PREP
    prep = json.loads(prep_path.read_bytes())
    oracle = prep['milestones']['oracle']
    if CASE not in [entry['path'] for entry in oracle]:
        oracle.append({'path': CASE, 'sha256': sha(case)})
    for entries in prep['milestones'].values():
        for entry in entries:
            if entry['path'] == STATUS:
                entry['sha256'] = status_sha
            elif entry['path'] == CASE:
                entry['sha256'] = sha(case)
    prep_path.write_bytes(dump(prep))
    print('pinned', CASE, sha(case), 'status', status_sha, 'preparation', sha(prep_path.read_bytes()))
    return 0


if __name__ == '__main__':
    sys.exit(main())
