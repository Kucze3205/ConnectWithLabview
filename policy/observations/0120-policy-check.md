# Policy check 0120 — Policymaker #579

## Scope and sources

Considered iterations 0117–0119 through `.session/history/manifest.json`, records `0117.json`–`0119.json`, task bodies and these trusted report snapshots:

- #571: `f035672c631525dcddcdf1aeaafcfa6158d491f17e25d12b150308910d3f95a4`.
- #574: `fa460b56e1ed12cfbf249f2d80f0bff1e10e7932465fd3b8762e22fe8677e366`.
- #577: `23ba3ba7e812b65fe039ee83c7ca4606535a778ad6d8b3880370fc2272a1c36a`.

Reports are under `.session/history/sessions/<issue>/<snapshot>.md`. Runtime evidence: `origin/loop-runtime` resolved to `bbe678242c51d43c09950c8f5b0000f49cc7eccb`; inspected `sessions/574.json`, first candidates for #571/#577 and availability only from `pool.json`. Pool's last modifying commit was `91e70e939c454756a625b0c9b039c219fa534ee1`, 2026-11-14T00:53:43Z. Use these pins for historical checks; current provider state can differ.

Checkout: `e9949d9aeebcf2a19f1dbe6cc3448ad50586fd7c`, tree `e5322deb85a9a7f73f4f6216e45fb282bfcb2080`. Read current 0119 proposal Markdown/pre-edit findings and selected JSON sections, preserved 0118 findings, role skills, parameters, evaluation and operating-parameters contracts. No checker, historical audit or probe ran in this session. This is a policy check, not semantic approval of the key.

## Results of #569's three changes

1. Cold-order rule: #574 actual runtime actions 3–8 read the limited request/preconditions/locator/license and derive from original bytes. Action 9 saves the cold expectation. First key access is action 11. Report and preserved review say P1 satisfied for #574 only. This supports retaining the orchestrator rule; no exposed continuation becomes cold.
2. Reviewer Finish rule: #574 has one Finish, action 33, status done, accepted with status done. No rejected Finish appears in its 34-action history. Retain the rule. This is one observation, not proof of a general failure-rate change.
3. Other-family preference: records show all work in #571, #574 and #577 used codex/gpt-6.1-sol. #574's full candidate history has no family switch. The configured Claude-first author route did not predict the actual author family. The separate review session found F3/F4, but the intended family difference was absent.

Decision: change only `routing.tasks.reviewer` to Claude Sonnet, Codex, Copilot. Prefer another family for the next review of Codex-authored work when available; preserve fallback. Check actual next-review candidates against actual author evidence. Do not change routing for evaluator verification, other roles, cadence or session limits. No guaranteed family difference or quota saving follows.

## Availability and resource limits

Records 0117/0118/0119 each report zero limit hits, zero parked seconds and no failed sessions. Iteration verdicts are accepted/none/accepted; the middle verdict is a completed review with findings. Input/output tokens are 2465736/26946, 2825508/25481 and 3507193/31007. These totals include shaper and task sessions, not Policymaker usage. They do not measure subscription quota or compare models fairly.

Pinned pool provider observations: Claude quota, attempts 4, observed 2026-11-14T00:35:38Z, retry_after 01:15:38Z; Codex available, observed 2026-11-13T23:17:31Z, latest model observation 2026-11-14T00:53:26Z; Copilot quota, retry_after 02:16:05Z. Older model-level available entries do not override later provider quota observations. Retry times do not prove recovery. The reviewer change can therefore still fall back to Codex. Do not wait for another family or request new spending.

## WP1 handoff and measured continuity

The shaper ordered F1/F2 correction #571, cold review #574, then focused F3/F4 disposition and exact preservation #577. This follows the previous policy handoff. Both reviews are preserved; preservation-only iterations or replay are unnecessary.

Measured current SHA256 and sizes:

| Path under benchmark/writing/ | Bytes | SHA256 |
|---|---:|---|
| wp1-key-0119.json | 327961 | 2afdca4bfc6feaa9464348bed7709b0657ea1ccbbe5d6b0a33b549c78f41c142 |
| wp1-key-0119.md | 13447 | 5f18384ed27e6b995426704f40316e69ee09a52084767304c15738f6e78980ac |
| check_wp1_key_0119.py | 37052 | 28ee70435c6a4fea7a79d942e7d90e9e3174ec31d64d741f93447000bc093d99 |
| wp1-key-0119-verification.json | 102981 | bd6054c90b5264bb9e7909937dfabae39bd919665f869a8424d1346aaa5e6cfd |
| wp1-key-review-0118.json | 569049 | 410b0ebf7d3135521d10bd32d3b1102769caa848f5e5c7278d8e9a29eefd9a55 |
| wp1-cold-expectation-0118.json | 5036 | 7ca817b22c430ece354287b0e42cd3deb106afaeee9a0d3d6c9d7dfd4dad141c |
| wp1-source-interpretation-0118.json | 2257 | b18eb04d01455a3d4b539a67042a83c4efc5d627f73ccd309ba6f1e7f48ea46b |
| wp1-review-audit-0118.py | 31314 | 8fc53c741b4d6628228e0abae53fbf3c64200c3f318d6ac903c8bbf73b13e833 |
| wp1-key-review-0116.json | 135476 | 2f127a7dad8e9719f6e026e1a1fce5aa1b0509f8503d5994771e0234c83a373e |

Actual JSON comparison: 429 source-obligation records in each 0117/0119 package; exactly seven change and 422 are equal. Changed IDs match F3's preserved findings: `/common/artifact_fidelity_rule` and `/tasks/4/requirements_mapping/W{1,2,3,4,5,8}/review`. Equality does not re-establish semantic correctness.

Actual 0119 JSON keeps F3 corrected-proposed-awaiting-separate-check and F4 blocked-for-missing-evidence. `WP1-original-output-grounding.established_key_use.status` is blocked. Missing content includes complete pre/post workspace/dependency inventories, immutable-original/license evidence and complete preservation-map relations. #577 reports 85 rejecting controls and three assessment checks passing with that block intact; this session did not rerun them.

Next execution step stays with the shaper: separate pinned semantic recheck of F3 and the F4 blocked prescriptions, using preserved #574 derivation and unchanged continuity. Do not repeat cold derivation or completed F1/F2 probes. A later complete-map example needs a new identity, concrete evidence and separate review before releasing F4. This recheck cannot make an incomplete key ready.

Native keys, validity/build/behavior/save-version results, withheld allocation, executed isolation, matched comparisons, independent method acceptance and complete artifact/version coverage remain absent or unverified. Tool quality is unmeasured. No Goal gate or owner method acceptance exists. #532 remains pending; no duplicate request or waiting task is justified. Orders are empty because no evaluator defect or separate audit question requires a task.
