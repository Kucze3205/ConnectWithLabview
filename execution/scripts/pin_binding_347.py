"""Record review #347 of manifest binding and add its two controls (findings 1 and 2).

Idempotent and hash-gated. Changes only benchmark/scripts/run_record.py,
benchmark/baseline/README.md, benchmark/preparation-status.json and
benchmark/preparation.json. Synthetic bytes only; no populated manifest, no runner.
Run from the repository root: python3 -I -B execution/scripts/pin_binding_347.py
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
    CHECKER: "48404c939c7cf97219759a64f309d3ac76db39085fb61d1a632d05a82bb9e63d",
    README: "9008a808827d0d4e0436af2fddfad7f1344fbce31b25254a517cec57011ab50e",
    STATUS: "e225d24c37a16151f7451b5610d838df7aa2d13f242ee6ebf59d0d4f30ff6479",
}
MARKER = "'uppercase hash of the right bytes'"

LOOP_OLD = '''    changed = manifest_bytes[:-2] + b'X' + manifest_bytes[-1:]
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
LOOP_NEW = '''    changed = manifest_bytes[:-2] + b'X' + manifest_bytes[-1:]
    validate(wrong, manifest)
    # Review #347 finding 1: case normalization and text input must also fail.
    upper = deepcopy(bound)
    upper['fields']['manifest_sha256']['value'] = upper['fields']['manifest_sha256']['value'].upper()
    for name, candidate, data, reason in (
            ('wrong content with well-formed hash', wrong, manifest_bytes, BINDING_REASON),
            ('one changed manifest byte', bound, changed, BINDING_REASON),
            ('uppercase hash of the right bytes', upper, manifest_bytes, BINDING_REASON),
            ('text instead of bytes', bound, manifest_bytes.decode(), 'manifest bytes required')):
        try:
            bind_manifest(candidate, data)
        except ValueError as exc:
            require(str(exc) == reason, name + ': failed for unexpected reason: ' + str(exc))
            binding.append({'control': name, 'result': 'rejected', 'reason': str(exc)})
        else:
            raise ValueError(name + ': mismatched manifest accepted')
'''

README_OLD = "This binding is not yet independently reviewed."
README_NEW = ("Review #347 accepted this binding over synthetic bytes; the check also rejects an uppercase hash "
              "and text input instead of bytes.")
STATUS_OLD = "and awaits independent review"
STATUS_NEW = ("and was accepted by review #347 (claude-sonnet-5-5, same model family as the Policymaker author), "
              "with uppercase-hash and text-input controls added")


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
        checker = replace_once(checker, LOOP_OLD, LOOP_NEW, "checker controls")
        (ROOT / CHECKER).write_bytes(checker.encode())
        print("run_record.py: controls added")
    elif MARKER in checker:
        print("run_record.py: unchanged")
    else:
        fail("run_record.py is neither the reviewed nor the updated bytes")

    readme = read(README).decode()
    if sha(read(README)) == OLD[README]:
        readme = replace_once(readme, README_OLD, README_NEW, "README sentence")
        (ROOT / README).write_bytes(readme.encode())
        print("README: sentence replaced")
    elif README_NEW in readme:
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
