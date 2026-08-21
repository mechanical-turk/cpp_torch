from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from youtube_channel import (
    analytics_start_date,
    desired_video_snippet,
    publishing_package,
    report_rows,
    series_videos,
)


class PublishingPackageTest(unittest.TestCase):
    def test_reads_fenced_platform_ready_sections(self) -> None:
        document = """\
# Publishing

## Final title

```text
Tensor Shapes: [] Is Not [0]
```

## YouTube description

```text
Description body.
```

## Pinned comment

```text
Full lesson: https://example.com
```

## Suggested tags

```text
C++, tensors, deep learning
```
"""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "publishing.md"
            path.write_text(document, encoding="utf-8")
            package = publishing_package(path)

        self.assertEqual(package["title"], "Tensor Shapes: [] Is Not [0]")
        self.assertEqual(package["description"], "Description body.")
        self.assertEqual(package["pinned_comment"], "Full lesson: https://example.com")
        self.assertEqual(package["tags"], ["C++", "tensors", "deep learning"])

    def test_supports_legacy_plain_title_and_description(self) -> None:
        document = """\
# Publishing

## Recommended title

Legacy title

## Description

Legacy description.

## Pinned comment

```text
Comment
```

## Suggested tags

```text
one, two
```
"""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "publishing.md"
            path.write_text(document, encoding="utf-8")
            package = publishing_package(path)

        self.assertEqual(package["title"], "Legacy title")
        self.assertEqual(package["description"], "Legacy description.")

    def test_uses_platform_block_when_section_contains_notes(self) -> None:
        document = """\
# Publishing

## Final title

```text
Episode title
```

Internal title note.

## YouTube description

```text
Description body.
```

## Pinned comment

Post this immediately, then pin it:

```text
Comment body.
```

Internal comment note.

## Suggested tags

```text
one, two
```
"""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "publishing.md"
            path.write_text(document, encoding="utf-8")
            package = publishing_package(path)

        self.assertEqual(package["title"], "Episode title")
        self.assertEqual(package["pinned_comment"], "Comment body.")


class VideoSnippetTest(unittest.TestCase):
    def test_preserves_fields_required_by_videos_update(self) -> None:
        current = {
            "title": "Old",
            "description": "Old",
            "tags": ["old"],
            "categoryId": "28",
            "defaultLanguage": "en",
            "defaultAudioLanguage": "en-US",
        }
        package = {
            "title": "New",
            "description": "New description",
            "tags": ["C++", "tensors"],
        }

        desired = desired_video_snippet(current, package)

        self.assertEqual(desired["title"], "New")
        self.assertEqual(desired["description"], "New description")
        self.assertEqual(desired["tags"], ["C++", "tensors"])
        self.assertEqual(desired["categoryId"], "28")
        self.assertEqual(desired["defaultLanguage"], "en")
        self.assertEqual(desired["defaultAudioLanguage"], "en-US")


class SeriesBoundaryTest(unittest.TestCase):
    def test_excludes_uploads_before_series_launch(self) -> None:
        old = {
            "id": "old",
            "snippet": {"publishedAt": "2020-01-01T00:00:00Z"},
        }
        current = {
            "id": "current",
            "snippet": {"publishedAt": "2026-08-12T00:00:00Z"},
        }

        self.assertEqual(series_videos([old, current]), [current])

    def test_analytics_query_includes_the_full_local_publication_day(self) -> None:
        video = {
            "id": "current",
            "snippet": {"publishedAt": "2026-08-13T00:45:18Z"},
        }

        self.assertEqual(analytics_start_date(video), "2026-08-12")


class AnalyticsReportTest(unittest.TestCase):
    def test_maps_report_headers_to_every_row(self) -> None:
        report = {
            "status": "ok",
            "response": {
                "columnHeaders": [
                    {"name": "elapsedVideoTimeRatio"},
                    {"name": "audienceWatchRatio"},
                ],
                "rows": [[0.01, 0.5], [0.02, 0.25]],
            },
        }

        self.assertEqual(
            report_rows(report),
            [
                {
                    "elapsedVideoTimeRatio": 0.01,
                    "audienceWatchRatio": 0.5,
                },
                {
                    "elapsedVideoTimeRatio": 0.02,
                    "audienceWatchRatio": 0.25,
                },
            ],
        )


if __name__ == "__main__":
    unittest.main()
