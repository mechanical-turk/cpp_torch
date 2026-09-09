from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "dashboard.py"
SPEC = importlib.util.spec_from_file_location("analytics_dashboard", MODULE_PATH)
assert SPEC and SPEC.loader
dashboard = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(dashboard)


class TikTokLoadingTest(unittest.TestCase):
    def test_manual_video_fills_provider_indexing_gap(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            phyllo = root / "phyllo"
            phyllo.mkdir()
            (phyllo / "latest-profiles.json").write_text(
                json.dumps(
                    [
                        {
                            "platform": "TikTok",
                            "username": "mechaturka",
                            "followers": 2,
                        }
                    ]
                )
            )
            (phyllo / "latest-content.json").write_text(
                json.dumps(
                    [
                        {
                            "platform": "TikTok",
                            "external_id": "old",
                            "content_id": "provider-old",
                            "title": "Old post",
                            "url": "https://www.tiktok.com/@mechaturka/video/old",
                            "published_at": "2026-08-20T15:00:00-04:00",
                            "views": 100,
                            "likes": 5,
                            "comments": 1,
                            "shares": 0,
                        }
                    ]
                )
            )
            (phyllo / "latest-summary.json").write_text(
                json.dumps({"collected_at": "2026-08-26T23:35:00+00:00"})
            )
            (root / "manual-tiktok.json").write_text(
                json.dumps(
                    {
                        "captured_at": "2026-08-26T18:01:00-04:00",
                        "videos": [
                            {
                                "id": "old",
                                "title": "Stale duplicate",
                                "url": "https://www.tiktok.com/@mechaturka/video/old",
                                "views": 1,
                            },
                            {
                                "id": "new",
                                "title": "New post",
                                "url": "https://www.tiktok.com/@mechaturka/video/new",
                                "published_at": "2026-08-26T17:46:23-04:00",
                                "views": 64,
                                "likes": 4,
                                "comments": 0,
                                "shares": 0,
                            },
                        ],
                    }
                )
            )
            (root / "manual-audience.json").write_text("{}")

            original_root = dashboard.PRIVATE_ROOT
            dashboard.PRIVATE_ROOT = root
            try:
                result = dashboard.load_tiktok()
            finally:
                dashboard.PRIVATE_ROOT = original_root

        self.assertEqual(result["source"], "phyllo+manual")
        self.assertEqual({item["id"] for item in result["content"]}, {"old", "new"})
        old = next(item for item in result["content"] if item["id"] == "old")
        new = next(item for item in result["content"] if item["id"] == "new")
        self.assertEqual(old["metrics"]["views"], 100)
        self.assertEqual(old["source"], "phyllo")
        self.assertEqual(new["metrics"]["views"], 64)
        self.assertEqual(new["source"], "manual")

    def test_newer_public_count_overrides_stale_phyllo_profile(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            phyllo = root / "phyllo"
            public = root / "tiktok-public"
            phyllo.mkdir()
            public.mkdir()
            (phyllo / "latest-profiles.json").write_text(
                json.dumps(
                    [
                        {
                            "platform": "TikTok",
                            "username": "mechaturka",
                            "followers": 8,
                            "updated_at": "2026-09-03T16:30:00+00:00",
                        }
                    ]
                )
            )
            (phyllo / "latest-content.json").write_text("[]")
            (phyllo / "latest-summary.json").write_text(
                json.dumps({"collected_at": "2026-09-04T15:11:00+00:00"})
            )
            (public / "latest.json").write_text(
                json.dumps(
                    {
                        "captured_at": 1788539400,
                        "account": {"follower_count": 19},
                    }
                )
            )
            (root / "manual-audience.json").write_text("{}")
            (root / "manual-tiktok.json").write_text("{}")

            original_root = dashboard.PRIVATE_ROOT
            dashboard.PRIVATE_ROOT = root
            try:
                result = dashboard.load_tiktok()
            finally:
                dashboard.PRIVATE_ROOT = original_root

        self.assertEqual(result["followers"], 19)
        self.assertIn("public-profile-audience", result["source"])


class GitHubLoadingTest(unittest.TestCase):
    def test_repository_stars_are_loaded_as_a_tracked_metric(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            github = root / "github"
            snapshots = github / "snapshots"
            snapshots.mkdir(parents=True)
            payload = {
                "captured_at": 1788534000,
                "repository": {
                    "full_name": "mechanical-turk/deep-learning-all-the-way-down",
                    "stargazers_count": 17,
                },
            }
            (github / "latest.json").write_text(json.dumps(payload))
            (snapshots / "2026-09-04T15-00-00Z.json").write_text(
                json.dumps(payload)
            )
            (root / "manual-audience.json").write_text("{}")

            original_root = dashboard.PRIVATE_ROOT
            dashboard.PRIVATE_ROOT = root
            try:
                platform = dashboard.load_github()
                history = dashboard.load_audience_history()
            finally:
                dashboard.PRIVATE_ROOT = original_root

        self.assertEqual(platform["followers"], 17)
        self.assertEqual(platform["metric_label"], "Stars")
        self.assertEqual(history["GitHub"][0]["followers"], 17)


if __name__ == "__main__":
    unittest.main()
