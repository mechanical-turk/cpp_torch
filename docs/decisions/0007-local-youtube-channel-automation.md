# Decision 0007 - Local YouTube Channel Automation

## Status

Accepted.

## Context

The video series now publishes three long-form episodes per week plus native
Shorts. Screenshots and manually exported CSV files do not provide a durable,
queryable analytics history and make routine metadata, playlist, thumbnail, and
comment work unnecessarily repetitive.

## Decision

Maintain a private local Python tool under `tools/youtube-channel/` using the
official YouTube Analytics API and YouTube Data API v3.

The tool authenticates through an installed-application OAuth client with:

```text
yt-analytics.readonly
youtube.readonly
youtube.force-ssl
```

Credentials and refresh tokens live outside Git. Raw snapshots remain in a
gitignored private directory. Read-only synchronization is the default.

The channel contains older unrelated uploads. A committed analytics config sets
2026-08-12 as the series boundary and supports explicit inclusions and
exclusions. Routine syncs query only series videos and defer device/geography
breakdowns to an opt-in full mode.

Mutation commands must be non-destructive, dry-run by default, and visibly diff
live state before `--apply`. A finalized `publishing.md` is the source of truth
for routine metadata, tags, thumbnail, playlist, and comment actions. Deletion
and banning capabilities are not implemented.

## Consequences

- Codex can refresh available analytics and channel metadata on demand without
  requesting screenshots or exports.
- Data API public counters can provide a fresh fallback while richer Analytics
  API rows are still processing.
- Analytics API processing delay and Studio-only panels remain limitations.
- Comment pinning, related-video assignment, cards, and end screens still need
  Studio or separately verified browser automation because the official API
  does not expose them.
- The broad `youtube.force-ssl` token must be protected even though destructive
  commands are absent from the local client.
