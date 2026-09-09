from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from phyllo_analytics import (
    SUPPORTED_PLATFORMS,
    normalize_content,
    normalize_profile,
    parser,
    parse_export_file,
)


class ExportFileTest(unittest.TestCase):
    def test_parses_exports_without_interpreting_other_shell_lines(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "phyllo.sh"
            path.write_text(
                'export PHYLLO_CLIENT_ID="client"\n'
                "export PHYLLO_CLIENT_SECRET='secret'\n"
                "curl https://example.com\n",
                encoding="utf-8",
            )

            self.assertEqual(
                parse_export_file(path),
                {
                    "PHYLLO_CLIENT_ID": "client",
                    "PHYLLO_CLIENT_SECRET": "secret",
                },
            )


class NormalizationTest(unittest.TestCase):
    def test_profile_metrics_are_read_from_reputation(self) -> None:
        profile = normalize_profile(
            {
                "id": "profile",
                "platform_username": "mechaturka",
                "work_platform": {"name": "YouTube"},
                "reputation": {
                    "subscriber_count": 32,
                    "content_count": 10,
                },
            }
        )

        self.assertEqual(profile["platform"], "YouTube")
        self.assertEqual(profile["subscribers"], 32)
        self.assertEqual(profile["content_count"], 10)

    def test_content_metrics_are_read_from_engagement(self) -> None:
        content = normalize_content(
            {
                "id": "video",
                "work_platform": {"name": "TikTok"},
                "engagement": {
                    "view_count": 692,
                    "like_count": 24,
                    "comment_count": 2,
                },
            }
        )

        self.assertEqual(content["platform"], "TikTok")
        self.assertEqual(content["views"], 692)
        self.assertEqual(content["likes"], 24)
        self.assertEqual(content["comments"], 2)


class PlatformSelectionTest(unittest.TestCase):
    def test_sync_defaults_to_all_supported_platforms(self) -> None:
        args = parser().parse_args(["sync"])

        self.assertIsNone(args.platform)
        self.assertEqual(SUPPORTED_PLATFORMS, {"youtube", "tiktok", "x"})

    def test_sync_can_select_only_tiktok(self) -> None:
        args = parser().parse_args(["sync", "--platform", "tiktok"])

        self.assertEqual(args.platform, ["tiktok"])


if __name__ == "__main__":
    unittest.main()
