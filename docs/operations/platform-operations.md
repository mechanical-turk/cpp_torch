# Platform Operations

## YouTube

- Use `tools/youtube-channel/` for routine metadata and available analytics.
- Analyze only videos selected by `youtube-series/analytics/config.json`.
- Keep credentials under `~/.config/dlatwd/youtube-analytics/` and raw snapshots
  in the gitignored analytics-private directory.
- A finalized `publishing.md` plus an explicit release decision authorizes its
  non-destructive metadata, thumbnail, comment, and playlist operations.
- Always inspect the dry-run diff before applying a package.
- Inspect all channel-authored comments before posting. Exact-text matching is
  not enough to detect a functional duplicate.
- Deletion, bans, destructive moderation, and other irreversible actions need a
  separate explicit request.
- The API cannot pin comments or manage every Studio feature. Perform supported
  work directly and label the exact Studio-only blocker.
- YouTube descriptions must be plain text. Preserve valid C++ operators and
  formulas while removing Markdown presentation syntax.
- After automatic captions appear, download and cache the English track beside
  the episode, derive chapters from the recording, update the description, and
  preserve the live chapter block in later metadata updates.

## X

- `tools/social-analytics/` is authorized for reading and approved replies.
- Preview `x-reply` before `--apply`; inspect the live conversation and refuse a
  duplicate account-authored reply.
- After a write, report the direct reply URL and record it in the timeline.
- Posting access does not authorize deletion, direct messages, unsolicited
  replies, or arbitrary new posts.
- Default analytics refreshes collect follower and profile data only. Tweet
  metadata requires an explicit request and `make x-post-analytics-sync`.

## Instagram

- Use `make instagram-analytics-sync` for owned profile and Reel insights.
- Keep credentials outside the repository and raw snapshots gitignored.
- Treat the integration as read-only unless the learner explicitly expands it.
- Do not put raw external URLs in Reel captions or first comments. Use the
  profile Links field or a Story sticker. A first comment should add technical
  value or invite a real response.

## TikTok

- Use `make tiktok-analytics-sync` for owned profile and video data.
- Keep credentials outside the repository and raw snapshots gitignored.
- If the API is unavailable, label manual fallback values as manual and retain
  `null` as unknown.
- Treat the integration as read-only unless the learner explicitly expands it.

## LinkedIn

- Record manually supplied follower counts and publication URLs with timestamps.
- Never present manual observations as API measurements.
