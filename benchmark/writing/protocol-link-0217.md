# Write-task coverage map (protocol-link-0217)

Measurement only. Nothing was repaired. No LabVIEW behaviour, native result or benchmark readiness is claimed (readiness stays false). Checkers ran as `python3 -I -B <file>` from the repository root.

## Checker runs

| File | Exit | Output tail |
|---|---|---|
| benchmark/writing/verify_method.py | 1 | `writing method verification failed: historical-pin-drift:benchmark/writing/input-pins.json` |
| benchmark/writing/check_c1_challenges_0125.py | 1 | `{"status": "failed", "error": "protected-pin-manifest", "benchmark_ready": false}` |
| benchmark/writing/check_c1_f1_0129.py | 1 | `FAIL: sha256 mismatch: benchmark/preparation.json` |
| benchmark/writing/check_human_c1_0130.py | 1 | `ValueError: protected input changed: benchmark/preparation.json` |
| benchmark/writing/check_wp1_examples_0121.py | 1 | `"errors": ["unchanged-file-pin:benchmark/preparation.json", "unchanged-file-pin:benchmark/writing/input-pins.json"]` |
| benchmark/writing/check_wp1_key_0115.py | 1 | JSON report ending `"status": "failed"`, `"trial_readiness": "pending"` (303 lines; cause not in the tail) |
| benchmark/writing/check_wp1_key_0117.py | 1 | JSON report ending `"status": "failed"`, `"trial_readiness": "pending"` (777 lines; cause not in the tail) |
| benchmark/writing/check_wp1_key_0119.py | 1 | `"package_errors": ["input-blob","input-hash","review-scoped-pin:benchmark/preparation.json","review-scoped-pin:benchmark/writing/input-pins.json"]`, `"status": "failed"`. The 85 of 85 counterexamples rejected as expected; only the package pins failed. |
| benchmark/writing/check_wp1_key_0123.py | 1 | `{"status": "failed", "cause": "ValueError: pinned bytes differ: ['benchmark/preparation.json']"}` |
| benchmark/writing/reviews-0128/check_integrity_0128.py | 1 | `Integrity verification failed: c1-artifact-manifest-0126.json: repository bytes differ` |

Result: 0 of 10 pass. Every failure I could read is pin or hash drift. `benchmark/preparation.json` and `input-pins.json` changed after these packages were pinned. README.md:60 says the frozen #544 checker intentionally stops matching current inputs. A drift failure does not show the method content is wrong, and a pass would not have shown it right. Causes of the 0115 and 0117 failures were not inspected. None needed `LABVIEW_ENVIRONMENT`. Nothing was repaired.

## Protocol map

`protocol.md` headings: tasks :7, oracle :45, split :65, baseline :77, challenges :92. Citations below point to the section or line range I saw. I did not check exact line numbers beyond the README line ranges in the task.

| Protocol section | Writing artifact that extends it |
|---|---|
| tasks (protocol.md:7) | benchmark/writing/README.md:11-18 (WC1, WM1, WM2, WB1 contracts); README.md:50 onward (WP1 text case); benchmark/writing/method.json. The protocol's own task table (protocol.md:7-43) has no write row. |
| oracle (protocol.md:45) | Partial. WP1 has text keys, `benchmark/writing/wp1-key-0123.json` (latest of 0115, 0117, 0119, 0123), and C1 files (`c1-challenges-0125-*`). README.md:20 says native references, connector maps and save versions are unavailable for WC1, WM1, WM2 and WB1. No native key exists. |
| split (protocol.md:65) | Only the README.md section "Paired writing comparison": public originals stay in development lineage groups, and restricted writing cases are not allocated. No writing split file or isolation test exists. Closest artifact: `benchmark/writing/input-pins.json`, which is pins only. Treat the split as absent apart from that statement. |
| baseline (protocol.md:77) | README.md:24-30 (paired comparison design); `benchmark/baseline/runner-contract.md` is reused. Design only: zero runs and no frozen writing addendum file. |
| challenges (protocol.md:92) | `benchmark/writing/verify_method.py` with `controls.json` (44 synthetic rejections plus the WP1 `project_text` controls, README.md:32-44, :54); `c1-challenges-0125.md` and its `-cases`/`-expectations` JSON files. All executed runs here failed on pin drift. |

## Write contracts

Independent key means a key derived independently of any candidate output. Glob of `benchmark/writing/` shows no key file named for WC1, WM1, WM2 or WB1.

| Task | Independent key? | What blocks it |
|---|---|---|
| WC1 (README.md:15) | Partial and in-method only: arithmetic vectors (x+1 on I32) derive from the request (README.md:20). I found no key file, only the synthetic `controls.json`. | Native capability: the native reference, connector map, documentation pins and a separate check are unavailable. |
| WM1 (README.md:16) | No. Inversion semantics are specified in the contract, but no key file exists. | Owner material and native capability: the DD-E1 original computation, native locators, save version and controlled results are unavailable. |
| WM2 (README.md:17) | No. | Native capability and owner material: confirmed consumers, propagation save set and save versions are unavailable. |
| WB1 (README.md:18) | No. Arithmetic and API obligations are stated, but no key file exists. | Owner material and native capability: matching source and build originals, the toolchain and native evidence are absent. Binary patching is excluded. |
| WP1 text case (README.md:50 section; project-text-writing-0109.md:3,9-11,29) | Yes for the text edit only: `wp1-key-0123.json` and `.md` (with 0115/0117/0119 predecessors). The key covers the one-byte `2`→`3` edit at byte 3347 and nothing native. Its checker now fails on pin drift (see above), and the semantic F4 and C1 items stay open. | Nothing blocks the text key. Native load, build, behaviour and save version stay `unexecuted` or `unverified` and need native capability. |

## Recommendation

Next task, needing no LabVIEW, owner material or product code: **re-pin and reconcile the writing evidence package against the current `benchmark/preparation.json` and `benchmark/writing/input-pins.json`.** First, a benchmark session classifies each of the 10 failures, using the full output of the 0115 and 0117 runs. For each, it records whether the cause is only pin drift, or content drift as well. It writes `benchmark/writing/pin-drift-0218.md`: a table of file, pinned hash, current hash and the commit or issue that changed it. It does not repair any checker. Whether to refresh frozen pins stays an owner or Policymaker decision. Re-pinning is not done here.

Expected gain: the next reviewer learns whether any writing checker can pass on the current tree. At present none does, so the "write extension passes its own checks" claim is unsupported. A drift classification stops the whole-method review from relying on stale `verification.json` files.

Verification command: `python3 -c "import pathlib; t=pathlib.Path('benchmark/writing/pin-drift-0218.md').read_text(); assert t.count('check_')>=10; assert not list(pathlib.Path('benchmark').rglob('__pycache__')); print('OK')"`.

Remaining write gaps beyond this need native capability or the owner: native keys for WC1, WM1, WM2 and WB1; their original sources and builds; a restricted split; executed paired runs.
