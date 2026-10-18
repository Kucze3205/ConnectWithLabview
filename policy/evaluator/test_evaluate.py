"""Integrity and false-positive checks, not LabVIEW benchmark cases."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from evaluate import MANIFEST, MILESTONES, compare, inventory


class BootstrapTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.base, self.candidate = self.root / "base", self.root / "candidate"
        self.base.mkdir()
        self.candidate.mkdir()

    def write_manifest(self, refs=None):
        target = self.candidate / MANIFEST
        target.parent.mkdir(exist_ok=True)
        target.write_text(json.dumps({"schema_version": 1, "milestones": {
            name: refs or [] for name in MILESTONES}}), encoding="utf-8")

    def test_missing_benchmark_is_not_a_pass(self):
        result = compare(self.candidate, self.base)
        self.assertEqual(result["verdict"], "inconclusive")
        self.assertFalse(result["improved"])
        self.assertIsNone(result["candidate"]["tool_quality"])
        self.assertFalse(result["candidate"]["benchmark_executed"])

    def test_empty_manifest_does_not_establish_readiness(self):
        self.write_manifest()
        result = inventory(self.candidate)
        self.assertEqual(result["manifest"], "indexed")
        self.assertEqual(result["missing"], list(MILESTONES))
        self.assertFalse(result["benchmark_ready"])

    def test_even_all_references_do_not_prove_quality_or_substance(self):
        (self.candidate / "claim.txt").write_bytes(b"Everything works")
        self.write_manifest([{"path": "claim.txt", "sha256": hashlib.sha256(b"Everything works").hexdigest()}])
        result = compare(self.candidate, self.base)
        self.assertEqual(result["candidate"]["missing"], [])
        self.assertEqual(result["verdict"], "inconclusive")
        self.assertFalse(result["candidate"]["benchmark_ready"])
        self.assertFalse(result["improved"])

    def test_tampered_or_missing_evidence_is_rejected(self):
        self.write_manifest([{"path": "missing.txt", "sha256": "0" * 64}])
        self.assertEqual(compare(self.candidate, self.base)["verdict"], "rejected")
        (self.candidate / "missing.txt").write_bytes(b"different")
        self.assertEqual(compare(self.candidate, self.base)["verdict"], "rejected")

    def test_external_evidence_is_not_read(self):
        for path in ("../secret", "/secret", "C:/secret", "..\\secret"):
            with self.subTest(path=path):
                self.write_manifest([{"path": path, "sha256": "0" * 64}])
                self.assertTrue(inventory(self.candidate)["errors"])

    def test_corrupt_manifest_is_not_missing(self):
        self.write_manifest()
        (self.candidate / MANIFEST).write_bytes(b"{")
        self.assertTrue(inventory(self.candidate)["errors"])

    def test_candidate_python_is_never_executed(self):
        (self.candidate / "evaluate.py").write_text("raise RuntimeError('candidate executed')", encoding="utf-8")
        self.assertEqual(compare(self.candidate, self.base)["verdict"], "inconclusive")

    def test_baseline_and_candidate_are_both_reported(self):
        self.write_manifest()
        result = compare(self.candidate, self.base)
        self.assertEqual(result["baseline"]["manifest"], "missing")
        self.assertEqual(result["candidate"]["manifest"], "indexed")


if __name__ == "__main__":
    unittest.main()
