# WP1 key 0123 pre-edit observed evidence

Recorded before preservation or key edits. No required pin differs. HEAD identity differs from review #587; all eleven reviewed scoped file bytes agree. Exact affected ID index was inspected; historical affected ledgers are indices 0 and 2. F3 is referenced unchanged, not replayed.

```json
{
  "observed_head": "2835358a82775c58aa8860885df8ebb2958ca86f",
  "observed_tree": "f485b05892a3be123048eadae21f2c6852a56488",
  "status_before_edits": "",
  "reviewed_identity": {
    "issue": 587,
    "session_task": "review-wp1-examples-0122",
    "role": "reviewer",
    "startup_model": "claude-sonnet-5-5",
    "continued_parent_candidate": {
      "provider": "codex",
      "model": "gpt-6.1-sol"
    },
    "model_limitation": "Startup label and continued candidate differ; exact model continuity is not certified. This review has a separate session/task from author #584.",
    "startup_status": "ok",
    "issue_bytes": 8862,
    "issue_sha256": "d572e5d8f08164617143672bd56a65ccd40a81235327fc5b8f035b2821a62942",
    "role_skill_bytes": 2374,
    "role_skill_sha256": "e8d707633435302387a0509e23f1f15e12ba2db096cefbc085b7c6a9fa8c0842",
    "observed_head": "650c282024d073a59710cdb0b2cfe5463f9b4a9d",
    "observed_tree": "752cb3a6b4010e6af388a1445402679aa564830d",
    "worktree_porcelain_before_and_after_review": "",
    "author_start_head": "94374c7a708f32b9d466614aa4c566184ac9165b",
    "author_start_tree": "74af6b6a919c2df6845e38da89604e80479584d6",
    "package_merge_commit": "4a0d8b3",
    "package_revision": "wp1-examples-0121-v1",
    "baseline_to_observed_scope": "Exactly six new benchmark/writing package files; other differences are administrative session-report, iteration and journal paths. No preexisting repository source changed.",
    "merge_to_observed_diff": [
      ".github/loop/data/session-reports/584/7db0922b3dffd6b7bf6f926cc2a18e3111269421a40a55153a22bbbb6623dd07.json",
      ".github/loop/data/session-reports/586/50e3087515a3965247c84624adbeb5f5488ebba41a2d4a14eb4e6faf0a6bbcc9.json",
      "iterations/0121.json",
      "iterations/0122/tasks.json",
      "journal/working-memory.md"
    ],
    "identity_conclusion": "Observed HEAD is later than authoring/merge; git diff and all scoped pins establish the same reviewed package bytes.",
    "repository_files_written": [],
    "standards_sources": [
      ".session/role/SKILL.md",
      "docs/perpetua/evaluation.md",
      "benchmark/protocol.md",
      "benchmark/writing/method.json"
    ],
    "tracked_agents_or_contributing_files": []
  },
  "scoped_pins": [
    {
      "path": "benchmark/writing/wp1-examples-0121.json",
      "bytes": 204095,
      "sha256": "8c6f6d82e4fdc9db268827fd1cc942daebf84319336bba3e7141a7a110a8e382"
    },
    {
      "path": "benchmark/writing/wp1-examples-0121.md",
      "bytes": 7934,
      "sha256": "b450a9d0b2d5abe9c72a7f16514705b2f72a8c4d835131843f59c2b17c3e0120"
    },
    {
      "path": "benchmark/writing/check_wp1_examples_0121.py",
      "bytes": 40139,
      "sha256": "2050ffc23448503f96ea1b5a5769f47260cb67ca478c38f2967e9276d3cf46c1"
    },
    {
      "path": "benchmark/writing/wp1-examples-0121-verification.json",
      "bytes": 31841,
      "sha256": "d7a0bc9caab9e32a265f5645ecb3dbe47c5b05146078ffb63af9f7c667e0bcd3"
    },
    {
      "path": "benchmark/writing/wp1-examples-0121-pre-edit.md",
      "bytes": 130487,
      "sha256": "649b71383e6f0467d41e97db38a3cb660a75d9e631abc411295b05fa0e35fa4b"
    },
    {
      "path": "benchmark/writing/wp1-disposition-review-0120.json",
      "bytes": 38470,
      "sha256": "bd2cd46a79bfcaf56a033b631c5b29196545283a547af86c6bcb8e9150c54141"
    },
    {
      "path": "benchmark/writing/wp1-key-0119.json",
      "bytes": 327961,
      "sha256": "2afdca4bfc6feaa9464348bed7709b0657ea1ccbbe5d6b0a33b549c78f41c142"
    },
    {
      "path": "benchmark/writing/method.json",
      "bytes": 45705,
      "sha256": "276f2881c70eae311195a4cc0a802e316ca06a206a0f1d16e7f041205fd3b0ac"
    },
    {
      "path": "benchmark/protocol.md",
      "bytes": 38342,
      "sha256": "1aeb83227dc11761160ff80d24eb03a216a2531d90c1a6d10ccb25bb85c7eb2f"
    },
    {
      "path": "benchmark/real-project-0107/original.lvproj",
      "bytes": 5806,
      "sha256": "1d5e140df788ce1f91c89241bbdb1227c5e4cc6fdf6efbbd820974bbe6082dcf"
    },
    {
      "path": "benchmark/real-project-0107/LICENSE.txt",
      "bytes": 1060,
      "sha256": "529e65e6fc185d39380efd3957ef1c9acd0aac31ed288bcb9d124840861f03a2"
    }
  ],
  "discrepancies": [],
  "protected_files": [
    {
      "path": "benchmark/preparation.json",
      "bytes": 12895,
      "sha256": "b6f9721c4518e2b9d9ed1be6a962175935f82991fd2e606ee27f5f737be97f25"
    },
    {
      "path": "benchmark/protocol.md",
      "bytes": 38342,
      "sha256": "1aeb83227dc11761160ff80d24eb03a216a2531d90c1a6d10ccb25bb85c7eb2f"
    },
    {
      "path": "benchmark/real-project-0107/LICENSE.txt",
      "bytes": 1060,
      "sha256": "529e65e6fc185d39380efd3957ef1c9acd0aac31ed288bcb9d124840861f03a2"
    },
    {
      "path": "benchmark/real-project-0107/original.lvproj",
      "bytes": 5806,
      "sha256": "1d5e140df788ce1f91c89241bbdb1227c5e4cc6fdf6efbbd820974bbe6082dcf"
    },
    {
      "path": "benchmark/writing/README.md",
      "bytes": 15838,
      "sha256": "8b6dd48d3df0a99be86dd2ab85da805b5fe8a37db49f32efcee35706623facb9"
    },
    {
      "path": "benchmark/writing/check_wp1_examples_0121.py",
      "bytes": 40139,
      "sha256": "2050ffc23448503f96ea1b5a5769f47260cb67ca478c38f2967e9276d3cf46c1"
    },
    {
      "path": "benchmark/writing/check_wp1_key_0115.py",
      "bytes": 19779,
      "sha256": "e7d22309e7ccd1b8e33628b9c0c9c77b59c3b3602b15d06e1179d26478ebeeeb"
    },
    {
      "path": "benchmark/writing/check_wp1_key_0117.py",
      "bytes": 37193,
      "sha256": "f23b829059ace8a5e77b017779c60902020057809c10663b2892ea210c31925d"
    },
    {
      "path": "benchmark/writing/check_wp1_key_0119.py",
      "bytes": 37052,
      "sha256": "28ee70435c6a4fea7a79d942e7d90e9e3174ec31d64d741f93447000bc093d99"
    },
    {
      "path": "benchmark/writing/method.json",
      "bytes": 45705,
      "sha256": "276f2881c70eae311195a4cc0a802e316ca06a206a0f1d16e7f041205fd3b0ac"
    },
    {
      "path": "benchmark/writing/wp1-cold-expectation-0118.json",
      "bytes": 5036,
      "sha256": "7ca817b22c430ece354287b0e42cd3deb106afaeee9a0d3d6c9d7dfd4dad141c"
    },
    {
      "path": "benchmark/writing/wp1-disposition-review-0120.json",
      "bytes": 38470,
      "sha256": "bd2cd46a79bfcaf56a033b631c5b29196545283a547af86c6bcb8e9150c54141"
    },
    {
      "path": "benchmark/writing/wp1-examples-0121-pre-edit.md",
      "bytes": 130487,
      "sha256": "649b71383e6f0467d41e97db38a3cb660a75d9e631abc411295b05fa0e35fa4b"
    },
    {
      "path": "benchmark/writing/wp1-examples-0121-verification.json",
      "bytes": 31841,
      "sha256": "d7a0bc9caab9e32a265f5645ecb3dbe47c5b05146078ffb63af9f7c667e0bcd3"
    },
    {
      "path": "benchmark/writing/wp1-examples-0121.json",
      "bytes": 204095,
      "sha256": "8c6f6d82e4fdc9db268827fd1cc942daebf84319336bba3e7141a7a110a8e382"
    },
    {
      "path": "benchmark/writing/wp1-examples-0121.md",
      "bytes": 7934,
      "sha256": "b450a9d0b2d5abe9c72a7f16514705b2f72a8c4d835131843f59c2b17c3e0120"
    },
    {
      "path": "benchmark/writing/wp1-key-0115-verification.json",
      "bytes": 17358,
      "sha256": "bf131650bf56d136769fd720ce8e24611b4fbd04a811634fef7eb6f48c112497"
    },
    {
      "path": "benchmark/writing/wp1-key-0115.json",
      "bytes": 262592,
      "sha256": "960b72b0aabb3e0d8151ad4fd25452377d6c05e482c76601f99163b246381a24"
    },
    {
      "path": "benchmark/writing/wp1-key-0115.md",
      "bytes": 9337,
      "sha256": "eb621c81154ccd537518bc0559e9a1fe8ed87e0e09b8418616fc3a5b52f42720"
    },
    {
      "path": "benchmark/writing/wp1-key-0117-verification.json",
      "bytes": 57834,
      "sha256": "e3e7b3da3d354b61a978d6458f7e5e523ba425dcec7ecc5699a7a513e25ea27a"
    },
    {
      "path": "benchmark/writing/wp1-key-0117.json",
      "bytes": 306601,
      "sha256": "008b4078d7f50610c7eb74e7d880e20602416130398fabf7a7534ae2a6b60982"
    },
    {
      "path": "benchmark/writing/wp1-key-0117.md",
      "bytes": 11253,
      "sha256": "ba62fabd3324329447515728d38113185ee7e7702faead0f6ca7f68a5a0a97a3"
    },
    {
      "path": "benchmark/writing/wp1-key-0119-pre-edit-findings.md",
      "bytes": 3688,
      "sha256": "c393b7bbfaf7ecb593688b1bbaf1827ce70a720ae7bc5d676430800b1785b3db"
    },
    {
      "path": "benchmark/writing/wp1-key-0119-verification.json",
      "bytes": 102981,
      "sha256": "bd6054c90b5264bb9e7909937dfabae39bd919665f869a8424d1346aaa5e6cfd"
    },
    {
      "path": "benchmark/writing/wp1-key-0119.json",
      "bytes": 327961,
      "sha256": "2afdca4bfc6feaa9464348bed7709b0657ea1ccbbe5d6b0a33b549c78f41c142"
    },
    {
      "path": "benchmark/writing/wp1-key-0119.md",
      "bytes": 13447,
      "sha256": "5f18384ed27e6b995426704f40316e69ee09a52084767304c15738f6e78980ac"
    },
    {
      "path": "benchmark/writing/wp1-key-review-0116.json",
      "bytes": 135476,
      "sha256": "2f127a7dad8e9719f6e026e1a1fce5aa1b0509f8503d5994771e0234c83a373e"
    },
    {
      "path": "benchmark/writing/wp1-key-review-0118.json",
      "bytes": 569049,
      "sha256": "410b0ebf7d3135521d10bd32d3b1102769caa848f5e5c7278d8e9a29eefd9a55"
    },
    {
      "path": "benchmark/writing/wp1-review-audit-0118.py",
      "bytes": 31314,
      "sha256": "8fc53c741b4d6628228e0abae53fbf3c64200c3f318d6ac903c8bbf73b13e833"
    },
    {
      "path": "benchmark/writing/wp1-source-interpretation-0118.json",
      "bytes": 2257,
      "sha256": "b18eb04d01455a3d4b539a67042a83c4efc5d627f73ccd309ba6f1e7f48ea46b"
    },
    {
      "path": "docs/perpetua/evaluation.md",
      "bytes": 7552,
      "sha256": "d9eb079a6be4a99aa4697433ce56ac2ef0d05dff15074b24215c8947b6e6e8d8"
    },
    {
      "path": "goal/goal.md",
      "bytes": 4161,
      "sha256": "5ee530059fd3efd34280ba632f160bbf37cb4f13c5d3e09cd841966ede5929cb"
    }
  ],
  "staged_inputs": [
    {
      "path": ".session/inputs/587-wp1-examples-review-0122.json",
      "bytes": 30049,
      "sha256": "6c7735d2c53e924075c14d68c83ba2b9c844e708778cfe563943f1c55e0b960b"
    },
    {
      "path": ".session/inputs/587-wp1-examples-cold-0122.json",
      "bytes": 6414,
      "sha256": "e1676c54e3e980f488bbb4dcc9ec8bc981890a22ae5dbcce26a62b02cf8f51e7"
    }
  ],
  "F4_exact": {
    "status": "blocked-for-missing-evidence",
    "resolution_mode": "retain-source-requirements-and-block-affected-ID",
    "affected_required_ids": [
      "WP1-original-output-grounding"
    ],
    "affected_examples": [
      "C1-correct",
      "C1-unverified-extra"
    ],
    "missing_evidence": [
      "Complete frozen pre/post workspace and dependency inventories with path, kind, length, SHA256 and raw-byte references, arm boundaries and cross-root resolution checks.",
      "Complete immutable-original and MIT license before/after inventories and byte references outside writable roots, plus delivered-copy license notice evidence.",
      "Explicit original/output preservation-map relations covering every preservation ID; whole-project/property citations and honest limits alone are not a complete preservation map."
    ],
    "source_requirements": [
      {
        "path": "benchmark/writing/method.json",
        "locator": "/common/answer_rule"
      },
      {
        "path": "benchmark/writing/method.json",
        "locator": "/tasks/4/request"
      },
      {
        "path": "benchmark/writing/method.json",
        "locator": "/tasks/4/preservation"
      },
      {
        "path": "benchmark/writing/method.json",
        "locator": "/tasks/4/output_manifest_rule"
      },
      {
        "path": "benchmark/writing/method.json",
        "locator": "/tasks/4/trial_artifacts"
      },
      {
        "path": "benchmark/protocol.md",
        "locator": "L26"
      },
      {
        "path": "benchmark/protocol.md",
        "locator": "L29"
      },
      {
        "path": "benchmark/protocol.md",
        "locator": "L35"
      },
      {
        "path": "benchmark/protocol.md",
        "locator": "L36"
      },
      {
        "path": "benchmark/protocol.md",
        "locator": "L40"
      },
      {
        "path": "benchmark/protocol.md",
        "locator": "L41"
      },
      {
        "path": "benchmark/protocol.md",
        "locator": "L60"
      }
    ],
    "disposition": "Partial/partial on explicit incomplete maps; use as established map key remains blocked. No source weakening, invented inventories or historical answer modification.",
    "unchanged": "F2 relational interpretation/tests, all other case outcomes/extras/contradictions, fixed denominators and C1 remain unchanged.",
    "what_next": "Supply complete explicit evidence in a newly identified example package and obtain a separate pinned semantic recheck; author integrity success cannot release this block."
  },
  "historical_slots_exact": {
    "/claim_adjudication/prescribed_ledgers/0": {
      "id": "C1-correct",
      "conditions": "Preserved review #/c1_tests/shared_context; hypothetical inspected output except truthful abstention; no LabVIEW. Not a new execution. 0119 interpretation is limited to the explicit preserved raw answer and supplied hypothetical project inspection; complete delivery does not stipulate unseen sidecar contents. No new execution or augmented answer is asserted.",
      "raw_answer_reference": {
        "path": "benchmark/writing/wp1-key-review-0116.json",
        "locator": "/c1_tests/cases/0/answer"
      },
      "items": [
        {
          "id": "WP1-describe-text-delta",
          "correctness": "correct",
          "grounding": "correct",
          "test_reference": "required_ids[id=WP1-describe-text-delta].separate_dimension_tests"
        },
        {
          "id": "WP1-original-output-grounding",
          "correctness": "partial",
          "grounding": "partial",
          "test_reference": "required_ids[id=WP1-original-output-grounding].separate_dimension_tests",
          "established_key_use": "blocked-F4"
        },
        {
          "id": "WP1-honest-limits",
          "correctness": "correct",
          "grounding": "correct",
          "test_reference": "required_ids[id=WP1-honest-limits].separate_dimension_tests"
        }
      ],
      "extras": [],
      "duplicates": [],
      "assessment": {
        "answer_correctness": "partial",
        "source_grounding": "partial"
      },
      "rationale": "Explicit map is nonfalse but incomplete in both independently applied dimensions: no full file-set/dependency or immutable-original/license map/inventory is supplied. Preserve partial/partial map outcomes and block established-key use pending complete evidence and separate review. L41 yields partial/partial; the historical case name does not imply a complete positive map control.",
      "evidence_reservation": {
        "status": "blocked-missing-complete-preservation-map",
        "review_reference": {
          "path": "benchmark/writing/wp1-key-review-0118.json",
          "locator": "/F2/all_prescribed_ledgers/0"
        },
        "raw_answer_utf8_sha256": "ab0c07ce725e64042c6ddf716dd6cacbdcf842ec65e9babe79b6cb92c5d8c26f",
        "evidence_mode": "explicit-preserved-answer-only; hypothetical project inspection, not an observed trial",
        "unseen_sidecars_assumed": false,
        "complete_preservation_map_supplied": false,
        "missing_evidence": [
          "Complete frozen pre/post workspace and dependency inventories with path, kind, length, SHA256 and raw-byte references, arm boundaries and cross-root resolution checks.",
          "Complete immutable-original and MIT license before/after inventories and byte references outside writable roots, plus delivered-copy license notice evidence.",
          "Explicit original/output preservation-map relations covering every preservation ID; whole-project/property citations and honest limits alone are not a complete preservation map."
        ],
        "coverage": [
          {
            "required_id": "WP1-property-text",
            "evidence": "Property and whole-project original/output citations; hypothetical comparison only."
          },
          {
            "required_id": "WP1-other-project-bytes",
            "evidence": "Whole-project one-byte comparison is stipulated; no trial result."
          },
          {
            "required_id": "WP1-file-set-and-unrelated-files",
            "evidence": "Missing complete workspace/dependency inventories and corresponding map."
          },
          {
            "required_id": "WP1-root-version-declaration",
            "evidence": "Declaration exists in hypothetical whole-project content; no explicit preservation-map relation or native save-version authority supplied."
          },
          {
            "required_id": "WP1-original-and-license",
            "evidence": "Missing immutable-root before/after inventory, license-preservation map and delivered notice evidence."
          }
        ]
      }
    },
    "/claim_adjudication/prescribed_ledgers/2": {
      "id": "C1-unverified-extra",
      "conditions": "Preserved review #/c1_tests/shared_context; hypothetical inspected output except truthful abstention; no LabVIEW. Not a new execution. 0119 interpretation is limited to the explicit preserved raw answer and supplied hypothetical project inspection; complete delivery does not stipulate unseen sidecar contents. No new execution or augmented answer is asserted.",
      "raw_answer_reference": {
        "path": "benchmark/writing/wp1-key-review-0116.json",
        "locator": "/c1_tests/cases/1/answer"
      },
      "items": [
        {
          "id": "WP1-describe-text-delta",
          "correctness": "correct",
          "grounding": "correct",
          "test_reference": "required_ids[id=WP1-describe-text-delta].separate_dimension_tests"
        },
        {
          "id": "WP1-original-output-grounding",
          "correctness": "partial",
          "grounding": "partial",
          "test_reference": "required_ids[id=WP1-original-output-grounding].separate_dimension_tests",
          "established_key_use": "blocked-F4"
        },
        {
          "id": "WP1-honest-limits",
          "correctness": "correct",
          "grounding": "correct",
          "test_reference": "required_ids[id=WP1-honest-limits].separate_dimension_tests"
        }
      ],
      "extras": [
        {
          "assertion": "Startup time decreases 10 percent",
          "correctness": "unverified",
          "grounding": "missing"
        }
      ],
      "duplicates": [],
      "assessment": {
        "answer_correctness": "unverified",
        "source_grounding": "partial"
      },
      "rationale": "Explicit map is nonfalse but incomplete in both independently applied dimensions: no full file-set/dependency or immutable-original/license map/inventory is supplied. Preserve partial/partial map outcomes and block established-key use pending complete evidence and separate review. The unmeasured startup-time extra remains correctness unverified and grounding missing, so L41 yields unverified/partial.",
      "evidence_reservation": {
        "status": "blocked-missing-complete-preservation-map",
        "review_reference": {
          "path": "benchmark/writing/wp1-key-review-0118.json",
          "locator": "/F2/all_prescribed_ledgers/2"
        },
        "raw_answer_utf8_sha256": "1499c559c30623bae8d635b4eb65c00d332a49457c46cfa7f47e8606d358956d",
        "evidence_mode": "explicit-preserved-answer-only; hypothetical project inspection, not an observed trial",
        "unseen_sidecars_assumed": false,
        "complete_preservation_map_supplied": false,
        "missing_evidence": [
          "Complete frozen pre/post workspace and dependency inventories with path, kind, length, SHA256 and raw-byte references, arm boundaries and cross-root resolution checks.",
          "Complete immutable-original and MIT license before/after inventories and byte references outside writable roots, plus delivered-copy license notice evidence.",
          "Explicit original/output preservation-map relations covering every preservation ID; whole-project/property citations and honest limits alone are not a complete preservation map."
        ],
        "coverage": [
          {
            "required_id": "WP1-property-text",
            "evidence": "Property and whole-project original/output citations; hypothetical comparison only."
          },
          {
            "required_id": "WP1-other-project-bytes",
            "evidence": "Whole-project one-byte comparison is stipulated; no trial result."
          },
          {
            "required_id": "WP1-file-set-and-unrelated-files",
            "evidence": "Missing complete workspace/dependency inventories and corresponding map."
          },
          {
            "required_id": "WP1-root-version-declaration",
            "evidence": "Declaration exists in hypothetical whole-project content; no explicit preservation-map relation or native save-version authority supplied."
          },
          {
            "required_id": "WP1-original-and-license",
            "evidence": "Missing immutable-root before/after inventory, license-preservation map and delivered notice evidence."
          }
        ]
      }
    }
  },
  "affected_key_leaf": {
    "locator": "/required_ids/6",
    "value": {
      "id": "WP1-original-output-grounding",
      "dimension": "answer",
      "expected_result": {
        "source_map": "A true complete relational original/output map for required text/preservation claims; each asserted support relation names actual artifacts and supporting corresponding content. Field presence alone is insufficient.",
        "dimensions": "Correctness independently tests relational truth; grounding independently tests supplied support. A wrong-existing citation makes this relational answer ID incorrect, while true delta prose remains correct for its own ID."
      },
      "expected_rule_ids": [
        "R-citations",
        "R-mapping",
        "R-dimensions"
      ],
      "original_output_citation_rule": "C-original-output for property/root; full file inventories for preservation; requirements/protocol for unavailable authority.",
      "comparison_or_human_adjudication": "Use separate_dimension_tests for relational correctness and evidentiary grounding; no choice of competing correctness readings remains.",
      "uncertainty": "Literal evidence and requested operation are determinate; independent approval pending, no actual output allocated or inspected, all native authority unavailable.",
      "status": "proposed-awaiting-separate-check",
      "checker_agreement": "pending",
      "source_requirements": [
        {
          "path": "benchmark/writing/method.json",
          "locator": "/tasks/4"
        },
        {
          "path": "benchmark/protocol.md",
          "locator": "L60"
        },
        {
          "path": "benchmark/protocol.md",
          "locator": "L26"
        },
        {
          "path": "benchmark/protocol.md",
          "locator": "L29"
        },
        {
          "path": "benchmark/protocol.md",
          "locator": "L35"
        },
        {
          "path": "benchmark/protocol.md",
          "locator": "L36"
        },
        {
          "path": "benchmark/protocol.md",
          "locator": "L40"
        },
        {
          "path": "benchmark/protocol.md",
          "locator": "L41"
        },
        {
          "path": "benchmark/protocol.md",
          "locator": "L99"
        }
      ],
      "separate_dimension_tests": {
        "correctness": "Treat the source map itself as an asserted factual relation: required text/preservation claims identify the actual original/output artifacts and corresponding locations whose content supports those claims. Independently inspect the artifacts to test identity, correspondence, completeness and truth of every asserted support relation. Existing wrong property (major instead of build) is an incorrect relation, even when delta prose is true. Incomplete nonfalse map partial; absent map missing; inaccessible independent evidence unverified. Extras do not automatically change this ID, but an explicit false support relation for an extra does. No automatic import of another ID grounding outcome.",
        "grounding": "Independently resolve the supplied evidence for the mapping relation: both actual hashes/paths and corresponding original/output locations, plus complete inventories for whole-file/set claims. Merely existing locations are insufficient. Wrong/non-supporting relation evidence incorrect; incomplete support partial; absent claim/evidence missing; inaccessible evidence unverified. Evaluate this separately from whether the relation was independently found true."
      },
      "established_key_use": {
        "status": "blocked",
        "finding": "F4",
        "affected_examples": [
          "C1-correct",
          "C1-unverified-extra"
        ],
        "reason": "Required complete preservation-map evidence is missing; no unseen sidecar is assumed. All requirements and separate relational correctness/grounding tests are retained.",
        "missing_evidence": [
          "Complete frozen pre/post workspace and dependency inventories with path, kind, length, SHA256 and raw-byte references, arm boundaries and cross-root resolution checks.",
          "Complete immutable-original and MIT license before/after inventories and byte references outside writable roots, plus delivered-copy license notice evidence.",
          "Explicit original/output preservation-map relations covering every preservation ID; whole-project/property citations and honest limits alone are not a complete preservation map."
        ],
        "release_condition": "Supply complete explicit evidence in a newly identified example package and obtain a separate pinned semantic recheck; author integrity success cannot release this block."
      }
    }
  },
  "source_derived_requirements": {
    "common_answer_rule": "Reuse protocol required claims, extras and contradiction rules. Writing claims cite original hash/locator plus corresponding output hash/locator; creation cites requirement anchor plus new artifact locator. Correct prose cannot compensate for a missing/wrong artifact; a correct artifact cannot compensate for unsupported prose.",
    "WP1": {
      "id": "WP1-project-build-text",
      "operation": "modify",
      "family": ".lvproj",
      "stratum": "public-development-project-text-preparation",
      "source_anchors": [
        {
          "path": "benchmark/real-project-0107/original.lvproj",
          "locator": "./Item[@Name='My Computer']/Item[@Name='Build Specifications']/Item[@Name='AF PPL']/Property[@Name='Bld_version.build']",
          "kind": "pinned original XML text only; no native locator"
        },
        {
          "path": "benchmark/project-text-writing-0109.json",
          "locator": "/task",
          "kind": "reviewed request and exact byte allowance"
        }
      ],
      "originals": [
        {
          "commit": "371c631c16155d88f02be11a953e4964d7452fd8",
          "path": "Core/AF PPL Build.lvproj",
          "snapshot": "benchmark/real-project-0107/original.lvproj",
          "sha256": "1d5e140df788ce1f91c89241bbdb1227c5e4cc6fdf6efbbd820974bbe6082dcf",
          "save_version": "unavailable"
        }
      ],
      "preconditions": [
        {
          "original_sha256": "1d5e140df788ce1f91c89241bbdb1227c5e4cc6fdf6efbbd820974bbe6082dcf",
          "root_tag": "Project",
          "root_attributes": {
            "Type": "Project",
            "LVVersion": "20008000"
          },
          "match_count": 1,
          "property_attributes": {
            "Name": "Bld_version.build",
            "Type": "Int"
          },
          "text": "2",
          "property_children": 0
        },
        "Preserved original/license outside writable trees; later trial requires frozen complete workspace/dependency manifest and independent preparer/checker approval for every text, preservation and answer ID. Native/full-trial prerequisites remain pending."
      ],
      "request": "In the isolated writable Core/AF PPL Build.lvproj copy, require the pinned original hash and unique WP1 locator/precondition. Change only its exact property text from 2 to 3. Return the complete edited project, artifact manifest, original/output source map and honest validation-limits answer. Preserve every other byte and file, including root LVVersion 20008000. Stop and report any failed precondition; do not build or resolve dependencies.",
      "semantic_ids": [
        "WP1-property-text"
      ],
      "expected_semantics": {
        "kind": "exact-text-only",
        "locator": "./Item[@Name='My Computer']/Item[@Name='Build Specifications']/Item[@Name='AF PPL']/Property[@Name='Bld_version.build']",
        "delta": {
          "before": "2",
          "after": "3",
          "offset_zero_based": 3347,
          "line_one_based": 42,
          "removed_hex": "32",
          "inserted_hex": "33",
          "output_size": 5806,
          "allowed_changed_bytes": 1
        }
      },
      "preservation_ids": [
        "WP1-other-project-bytes",
        "WP1-file-set-and-unrelated-files",
        "WP1-root-version-declaration",
        "WP1-original-and-license"
      ],
      "preservation": {
        "project_rule": "exact-one-byte-substitution",
        "unrelated_files": "byte-identical",
        "file_set": "unchanged",
        "allowed_metadata_deltas": [],
        "root_version": "20008000",
        "root_version_authority": "declaration-only",
        "native_save_version": "unverified",
        "originals_outside_writable_workspace": true,
        "complete_original_and_edited_bytes_required": true,
        "license_notice_required": true,
        "details": "Retain BOM, XML declaration, LF endings, tabs, entities, final newline, all other XML values/attributes/order; hash preserved originals/license before and after. Reject serializing/resaving noise or extra changes."
      },
      "answer_ids": [
        "WP1-describe-text-delta",
        "WP1-original-output-grounding",
        "WP1-honest-limits"
      ],
      "oracle": {
        "method": "review-0108.json#/claims/3 (D4), independently checked original text; validate locator/precondition directly against preserved source; task instruction supplies exact text 3; candidate output must never establish its own expectation",
        "provenance": "Exact review-0110.json SHA256 2dc007939a4b0637716027ef6e5a874702c9be7288daf80c3f007c07f382cdaf; scoped CLEAR permits integration preparation only. Complete trial key approval remains pending.",
        "native_key": "unavailable",
        "missing": [
          "complete-independent-text-preservation-answer-key-approval",
          "native-locators",
          "native-property-semantics",
          "native-save-version-authority",
          "native-results"
        ],
        "text_key_status": "proposed-awaiting-separate-check",
        "preflight": "Before either arm: separate preparer/checker records identities/sessions, key revision, original hashes, locator, delta, every text/preservation/answer ID, method, documentation pins, evidence hashes, agreement/disagreement and uncertainty. Resolve each ID against original and requirement independently. Disagreement blocks the affected key. Native locators/version/property effects remain missing; existing full-benchmark preflight is not waived.",
        "native_recipe": "Future separately provisioned trusted job only: use frozen original/output hashes and isolated dependency copies; pin LabVIEW version/build, OS, modules/licenses/target and documentation. Inspect original/output project/property views and save-version evidence separately; record actual load/errors, resolved and missing dependencies, authorized build inputs/results, and controlled behavior under independently established fixtures with reset/error/timeout conditions. Preserve hashed logs/captures and before/after files; reject conversion, silent repairs or unexplained saves. No native outcome is currently predictable from this text-only proposal; freeze native expectations independently before any later native validation, or retain unverified/unexecuted statuses."
      },
      "native_outcome": "unexecuted: missing-runtime and missing-independent-key; root LVVersion 20008000 is a declaration only, not native save-version authority",
      "output_paths": [
        "Core/AF PPL Build.lvproj"
      ],
      "output_manifest_rule": "Freeze original file set and dependencies before exposure. Only task.output_path may differ. Preserve immutable originals outside writable roots and reject cross-arm/original dependency resolution. A manifest or patch is not a substitute for complete artifact bytes.",
      "text_contract": {
        "locator": "./Item[@Name='My Computer']/Item[@Name='Build Specifications']/Item[@Name='AF PPL']/Property[@Name='Bld_version.build']",
        "precondition": {
          "original_sha256": "1d5e140df788ce1f91c89241bbdb1227c5e4cc6fdf6efbbd820974bbe6082dcf",
          "root_tag": "Project",
          "root_attributes": {
            "Type": "Project",
            "LVVersion": "20008000"
          },
          "match_count": 1,
          "property_attributes": {
            "Name": "Bld_version.build",
            "Type": "Int"
          },
          "text": "2",
          "property_children": 0
        },
        "delta": {
          "before": "2",
          "after": "3",
          "offset_zero_based": 3347,
          "line_one_based": 42,
          "removed_hex": "32",
          "inserted_hex": "33",
          "output_size": 5806,
          "allowed_changed_bytes": 1
        }
      },
      "planned_results": {
        "text_correctness": "unexecuted",
        "root_version_declaration": "unexecuted",
        "native_validity": "unexecuted",
        "dependency_resolution": "unexecuted",
        "build": "unexecuted",
        "behavior": "unexecuted",
        "save_version": "unverified",
        "overall_writing": "unverified"
      },
      "trial_artifacts": {
        "required": [
          "complete-original-bytes",
          "complete-edited-bytes",
          "license-notice",
          "workspace-dependency-manifest",
          "output-path-size-sha256-manifest",
          "original-output-source-map",
          "missing-unexpected-paths",
          "failed-invalid-empty-raw-outputs",
          "errors-truncation-retries",
          "request-response-tool-records",
          "time-cost-budget-records",
          "per-file-save-version-evidence",
          "native-logs-or-explicit-missing-status"
        ],
        "manifest_rule": "Freeze original file set and dependencies before exposure. Only task.output_path may differ. Preserve immutable originals outside writable roots and reject cross-arm/original dependency resolution. A manifest or patch is not a substitute for complete artifact bytes."
      },
      "result_rule": "A correct text delta and unchanged root version text cannot yield an overall writing pass with missing native evidence. Report separate artifact/text, answer, grounding, reader-fidelity and native outcomes; false/unsupported extras or contradictions require independent claim adjudication.",
      "reading_fidelity": "Separate frozen reader probes/native references required for any future reading measurement; this checker supplies no reader fidelity result.",
      "lineage": {
        "visibility": "public-development-only",
        "withheld": false,
        "model_unseen": false,
        "lineage": "NI Actor Framework original and derivatives; same lineage, no new independent project",
        "restricted_evaluation_ready": false,
        "rule": "Future withheld cases/keys require separate commissioned sources, duplicate/variant adjudication, whole-lineage allocation, custodian and executed role-specific denial/allowed-access/leakage checks. Public history and evaluator paths provide no concealment. Store readiness alone does not establish case allocation/run isolation."
      },
      "comparison": {
        "method_locator": "benchmark/writing/method.json#/comparison",
        "runner": "benchmark/baseline/runner-contract.md",
        "precision": "benchmark/precision/README.md",
        "arms": [
          "no-tool",
          "tool"
        ],
        "matched_fields": [
          "requested_change_hash",
          "original_manifest_hash",
          "allowed_inputs_hash",
          "common_prompt_hash",
          "model_snapshot_and_generation",
          "total_token_budget",
          "context_budget",
          "output_token_and_artifact_byte_budget",
          "wall_time_budget",
          "ordinary_editing_capabilities",
          "native_access_policy",
          "case_key_revision",
          "repetition_count",
          "retry_policy"
        ],
        "native_access": "neither-arm; post-output-freeze identical separate trusted validation only",
        "paired_runs_executed": 0,
        "rule": "Freeze hashed writing addendum, model/settings, prompts, inputs, key revision, budgets, retry policy, repetitions and arm order before either arm; only evaluated-tool access differs. Both arms receive same XML/ordinary editing capabilities. Fresh sessions/workspaces and no cross-arm memory/cache/key/artifact access. Retain every planned/failed/missing slot, raw bytes and accounting. Four conditional development pilots is existing design only; evaluation count/quota unresolved. Inherit paired lineage uncertainty/missing-pair rules, no interval for one lineage."
      },
      "requirements_mapping": {
        "W1": {
          "contract": "task.output_path; task.request; task.delta",
          "review": "Explicit project output and text change; no explanation-only success."
        },
        "W2": {
          "contract": "source; task.locator; task.precondition; preservation",
          "review": "Original hash/XML locator are available; native locators and full eligibility remain unavailable."
        },
        "W3": {
          "contract": "task.text_ids; task.preservation_ids; task.answer_ids; task.delta",
          "review": "Fixed IDs and one-byte allowance; no unrelated-content or metadata exceptions."
        },
        "W4": {
          "contract": "preservation.root_version; planned_results.save_version",
          "review": "Declaration preserved; native save version remains unverified."
        },
        "W5": {
          "contract": "planned_results; result_rule",
          "review": "Text and native judgments remain separate; no overall pass from missing evidence."
        },
        "W6": {
          "contract": "task.operation",
          "review": "No compiled output or rebuild; WB1 source/build chain cannot be inferred."
        },
        "W7": {
          "contract": "comparison; trial_artifacts",
          "review": "Identical copies/requests/budgets, symmetric output/retry accounting and isolated arms."
        },
        "W8": {
          "contract": "checker; planned_results",
          "review": "Positive and discriminating malformed controls; behavior/native evidence unavailable."
        }
      }
    },
    "protocol_lines": {
      "26": "Gradeable answer record: `case_id`, `status`, `claims[{claim_id, answer, conditions, citations[]}]`, `limitations`. Citations contain original SHA256, repository-relative path, archive/member chain when applicable, and a native object/property locator or exact XML/key/byte location appropriate to the claim.",
      "27": "For diagrams, record owning VI, nested structure/case, object/terminal/wire identity and native view region; attach a hashed native capture and object map when identifiers are unstable. A screenshot or exported node ID alone is insufficient: the reviewer must resolve the claim back into the preserved original.",
      "28": "Before reader exposure, freeze an independently checked reference inventory per task: stable required-claim IDs, atomic facts/relations, conditions, acceptable alternatives, numerical tolerances, original/native reference locators and hashes, and disallowed inferences. Identify separately the required answer claims and required reader observations; neither inventory may be inferred from submitted answers or exports. Record inventory/key revisions and unresolved references. Development keys may be public; withheld keys, case details and revealing evidence must never enter this repository or its history.",
      "29": "Account for every required ID and every submitted factual assertion, including implicit assertions in prose and limitations. Preserve the submitted text and its mapping to reference IDs; split compound assertions into atomic claims under frozen rules. Repeated equivalent assertions earn credit once; omissions retain their required slots. An assertion and its negation are a contradiction even when one matches the key: mark the affected item incorrect and retain both assertions. Unmatched assertions enter a separate extra-claim ledger and require independent checking; true extras cannot replace omissions, and false or unverified extras cannot disappear from scoring. Freeze these mapping/adjudication rules before runs and retain scorer/checker decisions.",
      "30": "Score reading fidelity, answer correctness and source grounding separately using the following item rules; faithful extraction alone does not establish correct reasoning, and answer correctness cannot establish fidelity.",
      "31": "",
      "32": "| Dimension | Required unit and correct outcome | Other item outcomes |",
      "33": "|---|---|---|",
      "34": "| Reading fidelity | Each fixed required reader observation matches its independently checked native reference, including required types, properties and relations under declared tolerances. | Partially represented compound content is partial; a conflicting value/relation is incorrect; absent content is missing. Unsupported access, inaccessible diagrams, tool errors and unverified native references retain their explicit outcomes and never earn correct credit. |",
      "35": "| Answer correctness | Each required answer claim matches an independently established expected claim under its conditions and tolerances. | Incomplete content is partial; false claims or contradictions are incorrect; omitted claims are missing; claims without sufficient independent evidence are unverified. An unsupported-case declaration remains unsupported, not correct. |",
      "36": "| Source grounding | Each required answer claim has resolvable original-artifact citations supporting its complete asserted content and conditions. | Support for only part is partial; a wrong or non-supporting citation is incorrect; absent claims/citations are missing; inaccessible evidence is unverified. A correct answer with a wrong citation is incorrect in grounding independently of correctness. |",
      "37": "",
      "38": "Reader-observation contract: before exposure, an independent preparer freezes probe IDs, artifact/member hashes, reader entry points and arguments, observation scope, required observation IDs and native-reference alignment rules. Choose probes from the task/native inventories, independently of agent answers and reader outputs; include the types, objects, wires, properties and relationships needed by the task. Pin ordering, limits, any adaptive branches and their selection rules; record unprobed scope as missing coverage. No favorable agent-selected calls may substitute for required probes.",
      "39": "For every probe, preserve the exact request, reader/configuration revision, environment, raw response bytes or files and hashes, timestamps, exit/error records and any truncation. Preserve empty responses and failed calls. A separate alignment record maps raw-output locations to required native-reference IDs and records absent, extra, duplicate and contradictory assertions; normalization must retain raw evidence and cannot invent missing facts. Unsupported operations, missing dependencies/licenses/environment, protected/removed diagrams, empty or truncated required content, errors and unverified references never count as matching observations. A successful call or valid wrapper alone earns no fidelity credit.",
      "40": "Freeze denominators per task and dimension: all required answer IDs for correctness and grounding, and all required observation IDs for fidelity. Report counts in every item-outcome category over those fixed totals, plus separate extra-claim counts by outcome and contradiction/duplicate counts; do not enlarge denominators with submitted claims or remove unavailable items. Report all planned cases as the coverage denominator alongside attempted/executed/scored counts. Any conditional summary must also show its eligible denominator and excluded/unavailable counts; no single aggregate merges the three dimensions.",
      "41": "Apply the following case-assessment rules in order, separately for each dimension. An absent or empty required reference inventory is unverified, never vacuously correct. With an established inventory, any incorrect required item or extra assertion, including a false assertion, contradiction or non-supporting citation in grounding, makes that dimension incorrect. Otherwise, any unverified required item or extra makes it unverified. Otherwise, every required item and extra must be correct (fully supported for grounding) for a correct assessment. Of the remaining cases, any correct/partial required item or extra makes the assessment partial; otherwise any tool error makes it error; otherwise all required items unsupported makes it unsupported; all other combinations of missing/unsupported items make it missing. Keep operational limitations and their affected IDs alongside this assessment; partial, missing, unsupported, unverified and error outcomes never become full passes. These are accounting rules, not owner quality thresholds.",
      "60": "An independent checker must resolve each expected claim and citation against original/native evidence without using the reader's output to derive the answer. Record case/key revision, evidence hashes, checker identity/role and session, procedure, claim-level agreement/disagreement and unresolved uncertainty. Disagreement blocks that claim's use as an established key until adjudicated and rechecked."
    }
  },
  "review_cold_provenance": {
    "artifact": ".session/artifacts/wp1-examples-cold-0122.json",
    "saved_before_any_later_read": true,
    "package_blind": true,
    "later_read_opened_early": false,
    "source_only_derivation": "Original/license whole, method /common/answer_rule and /tasks/4, protocol source clauses; independently parsed unique property and located and replaced the literal text byte before opening package/checker/pre-edit/review/key.",
    "procedural_deviations": [
      "Inherited continuation read protocol.md whole instead of the bounded clauses.",
      "Inherited continuation recorded HEAD/tree after original/license/protocol reads, rather than before them; clean status and identities were confirmed before the cold record and all Later reads."
    ],
    "effect": "The requested startup order was not exact; no package expectation leaked through an early Later read, including the recorded model continuation. Subsequent inspection cannot be described as a new cold derivation."
  },
  "cold_provenance": {
    "blind_to_package": true,
    "opened_files": [
      ".session/issue.md",
      ".session/role/SKILL.md",
      "benchmark/real-project-0107/LICENSE.txt",
      "benchmark/real-project-0107/original.lvproj",
      "benchmark/protocol.md",
      ".session/startup.json",
      "benchmark/writing/method.json"
    ],
    "method_scope": [
      "/common/answer_rule",
      "/tasks/4"
    ],
    "deviations": [
      "Inherited continuation read protocol.md whole rather than only lines 26-41 and 60; no Later-read package files opened.",
      "HEAD/tree were first recorded after original/license/protocol reads; reobserved with clean git status before saving this cold record."
    ],
    "startup_model": "claude-sonnet-5-5",
    "continuation_candidate": "codex / gpt-6.1-sol"
  },
  "author_provenance": {
    "session": "revise-wp1-key-0123",
    "startup_model": "claude-sonnet-5-5",
    "continued_candidate": "codex/gpt-6.1-sol",
    "independent": false,
    "cold": false
  },
  "plan": "Add a source-pinned operative extension revision referencing unchanged 0119 core and 0121 evidence; propose conditional F4 clearance only for the two new IDs, pending separate review. Historical required-ID established use and both historical slots remain blocked; unchanged F3 carried by reference."
}
```
