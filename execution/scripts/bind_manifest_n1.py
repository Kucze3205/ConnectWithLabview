"""Bind run records to manifest bytes (gap delta #330 N1, review #318 finding 4).

Idempotent and hash-gated. Changes only benchmark/scripts/run_record.py,
benchmark/baseline/README.md, benchmark/preparation-status.json and
benchmark/preparation.json. Synthetic bytes only; no populated manifest, no runner.
Run from the repository root: python3 -I -B execution/scripts/bind_manifest_n1.py
"""
import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
CHECKER = "benchmark/scripts/run_record.py"
README = "benchmark/baseline/README.md"
STATUS = "benchmark/preparation-status.json"
PREP = "benchmark/preparation.json"
OLD = {
    CHECKER: "bf57224fb2e29fb476b4d343770adc20126a2997f622efcd8c5ce353cd9c3300",
    README: "24c2018f7d64a4b808a8f2438aa56a876dd44c558e43b3ebc52297b96c628cf0",
    STATUS: "fbdb65ceb9169af5a906ae19f56b8140d5ebc68243ba5bf8ef55593475899eff",
}
MARKER = "def bind_manifest("

FUNC_OLD = "\n\ndef check():\n"
FUNC_NEW = '''

BINDING_REASON = 'manifest_sha256 does not match supplied manifest bytes'


def bind_manifest(record, manifest_bytes):
    """Accept a record only when manifest_sha256 is sha256 of the exact supplied bytes."""
    require(isinstance(manifest_bytes, bytes), 'manifest bytes required')
    require(record['fields']['manifest_sha256']['value'] == hashlib.sha256(manifest_bytes).hexdigest(),
            BINDING_REASON)


def check():
'''
CHECK_OLD = "    validate(no_tool, manifest)\n"
CHECK_NEW = '''    validate(no_tool, manifest)
    # Manifest-content binding (review #318 finding 4): synthetic bytes only, no populated manifest.
    manifest_bytes = b'SYNTHETIC run manifest bytes\\n'
    bound = deepcopy(record)
    bound['fields']['manifest_sha256']['value'] = hashlib.sha256(manifest_bytes).hexdigest()
    validate(bound, manifest)
    bind_manifest(bound, manifest_bytes)
    binding = [{'control': 'matching bytes', 'result': 'accepted'}]
    wrong = deepcopy(bound)
    wrong['fields']['manifest_sha256']['value'] = sha('SYNTHETIC other manifest')
    changed = manifest_bytes[:-2] + b'X' + manifest_bytes[-1:]
    for name, candidate, data in (('wrong content with well-formed hash', wrong, manifest_bytes),
                                  ('one changed manifest byte', bound, changed)):
        validate(candidate, manifest)
        try:
            bind_manifest(candidate, data)
        except ValueError as exc:
            require(str(exc) == BINDING_REASON, name + ': failed for unexpected reason: ' + str(exc))
            binding.append({'control': name, 'result': 'rejected', 'reason': str(exc)})
        else:
            raise ValueError(name + ': mismatched manifest accepted')
'''
OUT_OLD = "'no_tool_variant': 'pass', 'mutations': results,"
OUT_NEW = "'no_tool_variant': 'pass', 'mutations': results, 'manifest_binding': binding,"

README_OLD = ("Manifest-content binding stays unresolved (#318 finding 4): actual binding and a negative test "
              "are required before runner integration.\n")
README_NEW = ("Since Policymaker #344 (iteration 0057), the check also binds a record to synthetic manifest bytes "
              "(#318 finding 4): `manifest_sha256` must equal the sha256 of the exact supplied bytes, and a "
              "wrong-content hash and a one-byte change are rejected. This binding is not yet independently "
              "reviewed. No populated manifest or runner exists, so binding of real manifests stays unverified.\n")
STATUS_OLD = "manifest-content binding is unresolved (#318 finding 4)"
STATUS_NEW = ("manifest-content binding over synthetic bytes was added later (#318 finding 4, Policymaker #344) "
              "and awaits independent review; no populated manifest or runner exists")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(rel):
    return (ROOT / rel).read_bytes()


def dump(obj):
    return (json.dumps(obj, indent=2, sort_keys=True) + "\n").encode()


def fail(msg):
    print("ERROR:", msg)
    sys.exit(1)


def replace_once(text, old, new, label):
    if text.count(old) != 1:
        fail(f"{label}: anchor found {text.count(old)} times")
    return text.replace(old, new)


def main():
    checker = read(CHECKER).decode()
    if sha(read(CHECKER)) == OLD[CHECKER]:
        checker = replace_once(checker, FUNC_OLD, FUNC_NEW, "checker function")
        checker = replace_once(checker, CHECK_OLD, CHECK_NEW, "checker controls")
        checker = replace_once(checker, OUT_OLD, OUT_NEW, "checker output")
        (ROOT / CHECKER).write_bytes(checker.encode())
        print("run_record.py: binding added")
    elif MARKER in checker and OUT_NEW in checker:
        print("run_record.py: unchanged")
    else:
        fail("run_record.py is neither the reviewed nor the bound bytes")

    readme = read(README).decode()
    if sha(read(README)) == OLD[README]:
        if not readme.endswith(README_OLD):
            fail("README tail not found")
        readme = readme[: -len(README_OLD)] + README_NEW
        (ROOT / README).write_bytes(readme.encode())
        print("README: sentence replaced")
    elif readme.endswith(README_NEW):
        print("README: unchanged")
    else:
        fail("README is neither the pinned nor the updated bytes")

    status = json.loads(read(STATUS))
    if sha(read(STATUS)) == OLD[STATUS]:
        status["limitations"] = replace_once(status["limitations"], STATUS_OLD, STATUS_NEW, "status sentence")
    elif STATUS_NEW not in status["limitations"]:
        fail("status is neither the pinned nor the updated bytes")
    (ROOT / STATUS).write_bytes(dump(status))

    prep = json.loads(read(PREP))
    current = {rel: sha(read(rel)) for rel in (CHECKER, README, STATUS)}
    count, repinned = 0, set()
    for refs in prep["milestones"].values():
        for ref in refs:
            count += 1
            if ref["path"] in current:
                ref["sha256"] = current[ref["path"]]
                repinned.add(ref["path"])
    if repinned != set(current):
        fail("not pinned: " + ", ".join(sorted(set(current) - repinned)))
    (ROOT / PREP).write_bytes(dump(prep))
    print(f"references: {count}")
    for rel in (CHECKER, README, STATUS, PREP):
        print(f"{rel} {sha(read(rel))}")


if __name__ == "__main__":
    main()
