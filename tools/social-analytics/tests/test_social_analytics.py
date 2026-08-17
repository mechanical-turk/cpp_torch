from __future__ import annotations

import base64
import hashlib
import unittest

from social_analytics import X_COLLECTION_START, base64url, pkce_pair


class PkceTest(unittest.TestCase):
    def test_base64url_omits_padding(self) -> None:
        self.assertEqual(base64url(b"test"), "dGVzdA")

    def test_challenge_matches_verifier_hash(self) -> None:
        verifier, challenge = pkce_pair()
        expected = base64.urlsafe_b64encode(
            hashlib.sha256(verifier.encode("ascii")).digest()
        ).rstrip(b"=").decode("ascii")

        self.assertEqual(challenge, expected)
        self.assertGreaterEqual(len(verifier), 43)


class CollectionBoundaryTest(unittest.TestCase):
    def test_x_collection_never_precedes_series_boundary(self) -> None:
        self.assertEqual(X_COLLECTION_START, "2026-08-13T13:10:00Z")


if __name__ == "__main__":
    unittest.main()
