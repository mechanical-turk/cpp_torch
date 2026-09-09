from __future__ import annotations

import tempfile
import unittest
from argparse import Namespace
from contextlib import redirect_stdout
from io import StringIO
from types import SimpleNamespace
from unittest.mock import MagicMock, patch
from pathlib import Path

from youtube_channel import (
    analytics_start_date,
    command_package,
    description_with_chapters,
    desired_video_snippet,
    publishing_package,
    plain_youtube_description,
    report_rows,
    select_caption_track,
    series_videos,
    validate_chapters,
)


class PublishingPackageTest(unittest.TestCase):
    def test_comment_is_optional(self) -> None:
        document = "## Final title\nTitle\n\n## YouTube description\nDescription\n\n## Suggested tags\nC++\n"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "publishing.md"
            path.write_text(document, encoding="utf-8")
            self.assertEqual(publishing_package(path)["pinned_comment"], "")

    def test_no_comment_package_skips_comment_actions(self) -> None:
        package = {"title": "Title", "description": "Description", "tags": ["C++"], "pinned_comment": ""}
        video = {"snippet": {"title": "Title", "description": "Description", "categoryId": "28"}}
        for apply in (False, True):
            with self.subTest(apply=apply), \
                patch("youtube_channel.publishing_package", return_value=package), \
                patch("youtube_channel.authorize"), \
                patch("youtube_channel.build_services", return_value=SimpleNamespace(youtube=MagicMock())), \
                patch("youtube_channel.channel_details", return_value={"id": "channel"}), \
                patch("youtube_channel.owned_video", return_value=video), \
                patch("youtube_channel.execute") as execute, \
                patch("youtube_channel.channel_comment_exists") as inspect_comment, \
                patch("youtube_channel.post_comment") as post_comment, \
                redirect_stdout(StringIO()) as output:
                self.assertEqual(command_package(Namespace(package="unused.md", video_id="video", apply=apply)), 0)
                inspect_comment.assert_not_called()
                post_comment.assert_not_called()
                self.assertEqual(execute.call_count, int(apply))
                self.assertIn("comment actions skipped", output.getvalue())
                self.assertNotIn("pin this comment", output.getvalue())
                self.assertNotIn("Post and pin", output.getvalue())

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

    def test_preserves_code_fence_inside_plain_description(self) -> None:
        document = """\
# Publishing

## Final title

Episode title

## YouTube description

The calculation is:

```text
prediction = weights.dot(features) + bias
```

Source code: https://example.com

## Pinned comment

```text
Comment body.
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

        self.assertIn("prediction = weights.dot(features) + bias", package["description"])
        self.assertIn("Source code: https://example.com", package["description"])


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

    def test_preserves_live_chapters_during_package_updates(self) -> None:
        current = {
            "title": "Old",
            "description": (
                "Old description\n\nChapters:\n"
                "0:00 Intro\n1:00 Code\n2:00 Review"
            ),
            "tags": [],
            "categoryId": "28",
        }
        package = {
            "title": "New",
            "description": "New description",
            "tags": [],
        }

        desired = desired_video_snippet(current, package)

        self.assertEqual(
            desired["description"],
            "New description\n\nChapters:\n0:00 Intro\n1:00 Code\n2:00 Review",
        )

    def test_normalizes_package_description_before_update(self) -> None:
        current = {
            "title": "Old",
            "description": "Old",
            "tags": [],
            "categoryId": "28",
        }
        package = {
            "title": "New",
            "description": "In *the series*, call `sum()`.\n\n- One result",
            "tags": [],
        }

        desired = desired_video_snippet(current, package)

        self.assertEqual(
            desired["description"],
            "In the series, call sum().\n\n• One result",
        )


class VideoChapterTest(unittest.TestCase):
    def test_validates_and_normalizes_chapters(self) -> None:
        document = "0:00 Intro\n2:37 Tensors\n5:44 Recap\n"

        self.assertEqual(validate_chapters(document), document.rstrip())

    def test_rejects_short_or_nonzero_first_chapter(self) -> None:
        with self.assertRaises(ValueError):
            validate_chapters("0:01 Intro\n0:20 Tensors\n0:40 Recap")
        with self.assertRaises(ValueError):
            validate_chapters("0:00 Intro\n0:09 Tensors\n0:40 Recap")

    def test_rejects_chapter_titles_that_are_too_long_for_the_player(self) -> None:
        with self.assertRaises(ValueError):
            validate_chapters(
                "0:00 Introduction\n"
                "0:20 Compute the broadcast output shape\n"
                "0:40 Recap"
            )

    def test_requires_recap_as_the_final_chapter(self) -> None:
        with self.assertRaises(ValueError):
            validate_chapters("0:00 Introduction\n0:20 Code\n0:40 Review")

    def test_replaces_an_existing_chapter_block(self) -> None:
        current = "Description\n\nChapters:\n0:00 Old\n1:00 Old section"
        chapters = "0:00 Intro\n2:00 New section\n4:00 Recap"

        self.assertEqual(
            description_with_chapters(current, chapters),
            "Description\n\nChapters:\n" + chapters,
        )


class CaptionTrackTest(unittest.TestCase):
    def test_prefers_serving_automatic_track_in_requested_language(self) -> None:
        tracks = [
            {
                "id": "manual",
                "snippet": {
                    "language": "en",
                    "status": "serving",
                    "trackKind": "standard",
                },
            },
            {
                "id": "automatic",
                "snippet": {
                    "language": "en",
                    "status": "serving",
                    "trackKind": "asr",
                },
            },
        ]

        self.assertEqual(select_caption_track(tracks, language="en")["id"], "automatic")


class PlainYouTubeDescriptionTest(unittest.TestCase):
    def test_removes_presentation_markdown_without_changing_code_operators(self) -> None:
        description = """\
In *Deep Learning*, call `sum()`.

```text
prediction = left * right + bias
```

* First item
- Second item

complexity = rows * inner * columns * batches
"""

        self.assertEqual(
            plain_youtube_description(description),
            "In Deep Learning, call sum().\n\n"
            "prediction = left * right + bias\n\n"
            "• First item\n"
            "• Second item\n\n"
            "complexity = rows * inner * columns * batches",
        )


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
