#!/usr/bin/env python3
"""Regression check for iteration 0161: policy/session-state.py must print at most 8 MiB (bytes) even when the history
is JSON-heavy (quotes double when a record is embedded as a JSON string) and holds Polish text (2 UTF-8 bytes per letter).
Run from the repository root: python3 policy/checks/session_state_size.py"""
import json
import os
import subprocess
import sys
import tempfile

LIMIT = 8 * 1024 * 1024
heavy = {"k%d" % i: "\"ąęłóśżź\"" * 40 for i in range(60)}           # quote- and Polish-heavy payload
records = [{"iteration": n, "tasks": [{"issue": 1000 + n, "title": "zadanie ż"}], "input_state": heavy,
            "outcome": {"sessions": [{"issue": 1000 + n, "status": "done"}]}} for n in range(1, 400)]
reports = [{"issue": 1000 + n, "source": "s", "snapshot": "x%d" % n, "body": "status: done\n" + "„łóż” \"q\" " * 4000}
           for n in range(1, 400)]
facts = {"role": "policymaker", "state": {"iterations": [{"n": 1}], "goal": {"text": "Cel ąę" * 2000}},
         "full": True, "checkout": "c", "records": records, "reports": reports, "outboxes": []}
with tempfile.TemporaryDirectory() as tmp:
    path = os.path.join(tmp, "facts.json")
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(facts, handle, ensure_ascii=False)
    out = subprocess.run([sys.executable, "-I", "policy/session-state.py", path], capture_output=True, check=True).stdout
answer = json.loads(out.decode("utf-8"))
manifest = json.loads(answer["files"]["history/manifest.json"])
print("printed bytes %d, characters %d, files %d, omitted %d" %
      (len(out), len(out.decode("utf-8")), len(answer["files"]), manifest["omitted_oldest_files"]))
assert len(out) <= LIMIT, "answer exceeds 8 MiB"
assert manifest["omitted_oldest_files"] > 0, "test input did not exercise the budget"
assert "history/records/0399.json" in answer["files"], "newest record was dropped"
assert answer["loop_state"]["history"]["records"] == len(records)
print("OK")
