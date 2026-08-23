from __future__ import annotations

import base64
import hashlib
import unittest

from social_analytics import (
    SCOPES,
    X_COLLECTION_START,
    base64url,
    command_x_audience_sync,
    parser,
    pkce_pair,
)


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


class XAuthorizationScopeTest(unittest.TestCase):
    def test_x_authorization_requests_reply_capability(self) -> None:
        self.assertIn("tweet.read", SCOPES.split())
        self.assertIn("tweet.write", SCOPES.split())
        self.assertIn("offline.access", SCOPES.split())


class XCommandTest(unittest.TestCase):
    def test_audience_sync_is_distinct_from_tweet_sync(self) -> None:
        args = parser().parse_args(["x-audience-sync"])
        self.assertIs(args.handler, command_x_audience_sync)


if __name__ == "__main__":
    unittest.main()
