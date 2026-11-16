# Chapter 15 distribution

Procedure: [distribution operations](../../docs/operations/distribution.md).
Ledger: [distribution timeline](../../docs/distribution-timeline.md) (append-only;
log completed events there). Standing schedule:
[posting cadence](../production/posting-cadence.md).

## Current instruction

November 16, 2026: the private YouTube upload (November 14) and the GitHub pushes
are the only external events recorded. No public release, scheduling,
announcement, comment, Reddit post or Short has been authorized yet; each needs
the creator's explicit approval. This file records plans and facts.

Canonical title, description, tags, chapters, first-comment candidate, X
announcement, LinkedIn announcement and navigation reply:
[publishing.md](publishing.md) (drafted November 16, none posted). Do not
maintain duplicate copy here. Package score: 77/100, hold for public release.

## Links (checked November 16, 2026)

| Link | Used in | Result |
| --- | --- | --- |
| https://www.youtube.com/watch?v=wBB9lQnpUNU | X and LinkedIn announcements | Resolves, but the video is private: it will not open logged out and has no public oEmbed. Open it logged out after release, before posting. |
| https://github.com/mechanical-turk/deep-learning-all-the-way-down | Navigation reply, README | 200 |
| https://github.com/mechanical-turk/deep-learning-all-the-way-down/commit/1d2a49a | README Episode 15 row | 200 |
| https://www.youtube.com/playlist?list=PLZSg76FHvdTw | Navigation reply, video description | Resolves to "Deep Learning, All the Way Down \| From First Principles in C++" |
| https://www.youtube.com/watch?v=YZnfcbwwOdI | README Episode 14 row | Public (oEmbed returns the Episode 14 title) |

## Upload record

- File: `/Users/keremkazan/Movies/CapCut/ep15/cpp-momentum-adam-optimizers-from-scratch.mp4`
- SHA-256: `a345b5822f265103115a64d95a3e62a95cf8f89bbbc8c36ec81fdc2e1f18d544`
- 3840x2160, 30 fps, H.264, AAC stereo 48 kHz. Duration 34:08.967 (61,469
  frames). Size 3,475,946,106 bytes.
- Video: https://www.youtube.com/watch?v=wBB9lQnpUNU
- Studio: https://studio.youtube.com/video/wBB9lQnpUNU/edit
- Status (API read-back, November 16): private, unscheduled, processing
  succeeded, English, Education, not made for kids, in the complete-series
  playlist, 22 caption-derived chapters applied.
- Reviewed: full decode, stream probe, loudness (-16.10 LUFS, -0.63 dBTP), a
  preview frame at 15:00. Not reviewed: full subjective playback, YouTube 2160p
  playback, YouTube-encoded code legibility.

## Public source (done)

- Episode 15 code checkpoint: `1d2a49a` ("Episode 15 code checkpoint: momentum
  and Adam optimizers"). Compiled with `clang++ -std=c++23 -O2` and run; epoch 5
  loss 0.0510026 and test accuracy 93.65% (1873 of 2000), the final run of the
  video.
- README commit `e3ec684` links the checkpoint in the Episode 15 row and summary.
  The Watch column for Episode 15 is empty until the video is public.
- `origin/main` of the demo repository is at `e3ec684`, pushed November 16.
- At release: add the public YouTube URL to the Episode 15 README row, push, and
  confirm `origin/main` matches. Add a work-in-progress row for Episode 16 only
  when its topic is settled.

## Before public release

- Thumbnail: none confirmed. Follow the visual asset and thumbnail research
  guidelines; do not reuse another episode's image. Check it at small size.
- End screen: Subscribe and complete-series playlist. Four source-tail clips
  were held for up to two frames, so confirm the tail is clean enough for an
  end screen or place it over speech by creator decision.
- Captions: the YouTube automatic English track was used for chapters only.
  Review it for ASR errors (Adam, MNIST, ReLU, `std::sqrt`) before release.
- Recording check: during the playback review, read SGD's accuracy and Adam's
  loss without the step count from the recording. The posts quote 91.3% and
  0.134 / 91.15% from the verified run of the same code.
- Chapters and claims: the recording has no batch-size comparison, so no
  chapter, description or post mentions one. Batch-64 comparisons flip with the
  epoch budget; make no batch-size claim in any copy.
- Inspect 2160p playback and audio in the YouTube encode.
- Before posting: inspect the X and LinkedIn composer previews, read owned-account
  analytics and live search for the research records, and check both accounts
  for an existing Episode 15 post.

## Proposed sequence (a plan, not events)

Today is Monday, November 16, 2026. The standing cadence publishes long-form at
11:00 AM ET on Monday, Wednesday and Saturday, announces on X about an hour
later, and announces on LinkedIn the next weekday at 9:00 to 10:30 AM ET. This
proposal makes no claim that timing causes a result.

| Step | Proposed window (ET) | Depends on |
| --- | --- | --- |
| Thumbnail, end screen, caption review, 2160p and settings checks | Before release | Creator decisions above |
| README Watch link | Immediately after release | Public URL |
| Public release | Earliest Wednesday, November 18, 11:00 AM; otherwise Saturday, November 21, 11:00 AM | Every item above, creator approval |
| X announcement and navigation reply | Release day, about 12:00 PM | Public URL opens logged out; composer preview |
| LinkedIn announcement and author comment | Next weekday, 9:00 to 10:30 AM | Public URL; at least a day after X |
| Post-publication check, comment duplicate inspection | After release | Authorization |

## Explicit deferrals

- Reddit: defer. A post needs the Reddit research and strategy notes, the
  current rules of the chosen community, a new angle and copy, and a specific
  question (for example, how others pick a learning rate for momentum).
- Shorts: defer. No concept is selected or scripted.
- Episode 14 announcements: whether the X and LinkedIn drafts were posted is
  unverified in the timeline. Confirm before scheduling, so announcements do
  not collide.
- Comments: the first-comment candidate in publishing.md stays unposted until
  the video is public and the creator approves it.

## Completed events

See the ledger entries dated November 14 and November 16, 2026 for the private
upload, playlist membership, chapters, and the repository pushes. No public
release or announcement is recorded.
