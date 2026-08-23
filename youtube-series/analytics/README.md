# YouTube Analytics Operations

This directory documents the private analytics workflow for *Deep Learning,
All the Way Down*. Raw channel data and OAuth credentials must never be
committed.

## Commands

Authorize the local tool once:

```sh
make youtube-auth
```

Force a new consent flow after changing scopes or moving the OAuth app from
Testing to Production:

```sh
make youtube-reauthorize
```

Refresh all available channel and per-video analytics:

```sh
make youtube-analytics-sync
```

Routine syncs collect only core reports. Device and country breakdowns are
available when needed:

```sh
make youtube-analytics-sync-full
```

Print a compact summary of the latest snapshot:

```sh
make youtube-analytics-report
```

Run the local safety tests:

```sh
make youtube-channel-test
```

## Cross-platform dashboard

Refresh the dashboard's default data first:

```sh
make analytics-sync
```

This routine refresh collects only X profile and follower metrics. It does not
request tweet-level metadata. Pull X post analytics only when explicitly
needed:

```sh
make x-post-analytics-sync
```

Open the read-only local dashboard over the latest YouTube, X, and Instagram
snapshots:

```sh
make analytics-dashboard
```

Then visit <http://127.0.0.1:8765>. The dashboard never refreshes an external
API on page load, which prevents accidental X credit usage. Run the platform
sync commands deliberately, then reload the page. TikTok and LinkedIn remain
marked unavailable until a manual follower snapshot or API collector exists.

## Private state

OAuth credentials are stored outside the repository under:

```text
~/.config/dlatwd/youtube-analytics/
```

Timestamped analytics snapshots are written under the gitignored directory:

```text
youtube-series/analytics/private/
```

[`config.json`](config.json) defines the series boundary. Uploads before
2026-08-12 are excluded from API analytics queries and reports. Explicit include
and exclude lists handle future exceptions without relying on title matching.

The tool requests read-only Analytics and account access plus YouTube's channel
management scope. Read-only synchronization is the default. Destructive channel
operations are deliberately not implemented.

## Publishing-package dry run

Compare a live video with a release package without changing YouTube:

```sh
UV_CACHE_DIR=build/uv-cache uv run --project tools/youtube-channel \
  youtube-channel package \
  --video-id VIDEO_ID \
  --package youtube-series/chapter-NN/publishing.md
```

After reviewing the complete diff, append `--apply` to update the title,
description, and tags and to post the package's pinned-comment text if the
channel has not already posted it. YouTube does not expose comment pinning in
the API, so the posted comment must still be pinned in Studio.

## Playlists and thumbnails

All mutation commands are dry runs unless `--apply` is present:

```sh
UV_CACHE_DIR=build/uv-cache uv run --project tools/youtube-channel \
  youtube-channel playlist-ensure --title "PLAYLIST" --description "DESCRIPTION"

UV_CACHE_DIR=build/uv-cache uv run --project tools/youtube-channel \
  youtube-channel playlist-add --title "PLAYLIST" --video-id VIDEO_ID

UV_CACHE_DIR=build/uv-cache uv run --project tools/youtube-channel \
  youtube-channel thumbnail --video-id VIDEO_ID --file thumbnail.png
```

Deletion and channel-ban operations are intentionally absent even though the
OAuth management scope is broad enough to permit them.
