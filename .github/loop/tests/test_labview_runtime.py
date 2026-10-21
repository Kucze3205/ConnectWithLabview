"""Reject altered/truncated runtime fixtures before launching LabVIEW."""
import hashlib
import unittest

import fakes
from check_labview_runtime import verify_fixture


class FixtureTest(unittest.TestCase):
    def test_rejects_corruption_even_with_a_resource_header(self):
        original = b"RSRC\r\noriginal"
        expected = hashlib.sha256(original).hexdigest()
        verify_fixture(original, expected)
        with self.assertRaises(ValueError):
            verify_fixture(b"RSRC\r\nmodified", expected)

    def test_rejects_non_labview_payload_even_if_checksum_matches(self):
        payload = b"<html>Download unavailable</html>"
        with self.assertRaises(ValueError):
            verify_fixture(payload, hashlib.sha256(payload).hexdigest())
