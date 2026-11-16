# Chapter 15 distribution

Procedure: [distribution operations](../../docs/operations/distribution.md).
Ledger: [distribution timeline](../../docs/distribution-timeline.md) (append-only;
log completed events there). Standing schedule:
[posting cadence](../production/posting-cadence.md).

## Current instruction

November 16, 2026: the private YouTube upload (November 14) is the only external
publication recorded. No public release, scheduling, announcement, comment,
Reddit post or Short has been authorized yet; each needs the creator's explicit
approval. This file records plans and facts, and no completed external event.

Canonical title, description, tags, chapters, first-comment candidate:
[publishing.md](publishing.md), including the X announcement, LinkedIn
announcement and navigation reply (drafted November 16, not posted). Do not
maintain duplicate copy here.

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

## Before public release

- Thumbnail: none confirmed. Follow the visual asset and thumbnail research
  guidelines; do not reuse another episode's image. Check it at small size.
- End screen: Subscribe and complete-series playlist. Four source-tail clips
  were held for up to two frames, so confirm the tail is clean enough for an
  end screen or place it over speech by creator decision.
- Captions: the YouTube automatic English track was used for chapters only.
  Review it for ASR errors (Adam, MNIST, ReLU, `std::sqrt`) before release.
- Chapters: the recording has no batch-size comparison, so the chapter list and
  description must not mention one.
- Claims: the description says only what was recorded. The script's batch-64
  section was not recorded; the later experiments show batch-64 momentum versus
  SGD flips with epoch budget (2 epochs worse, 3 or more tied). Do not make a
  batch-size claim in any social copy.
- Inspect 2160p playback and audio in the YouTube encode.

## Public source

- The demo repository `origin/main` is at `ffba324` ("Add momentum and Adam
  optimizers for Episode 15 (work in progress); link Episode 14 in README"),
  pushed November 16. It is a work-in-progress commit, not a checkpoint of the
  recorded final state: its `main.cpp` runs momentum at rate 0.1, batch 64, five
  epochs (94.25%, 1885 of 2000 in one run), which is not a run shown in the video.
- README marks Episode 15 as work in progress with no code link and links the
  Episode 14 checkpoint `47db7ed`.
- At release: decide which commit is the Episode 15 checkpoint (the recorded
  final source is in `verification/episode-15-final.cpp`), commit it, push, add
  its hash and the public YouTube URL to the Episode 15 README row and summary,
  add a work-in-progress row for Episode 16, confirm `origin/main` matches, and
  compile and run the entry point.

## Proposed sequence (a plan, not events)

Today is Monday, November 16, 2026. The standing cadence publishes long-form at
11:00 AM ET on Monday, Wednesday and Saturday, announces on X about an hour
later, and announces on LinkedIn the next weekday at 9:00 to 10:30 AM ET. This
proposal makes no claim that timing causes a result.

| Step | Proposed window (ET) | Depends on |
| --- | --- | --- |
| Thumbnail, end screen, caption review, 2160p and settings checks | Before release | Creator decisions above |
| Episode 15 code checkpoint and README | Immediately before release | Approval; verified URL |
| Public release | Earliest Wednesday, November 18, 11:00 AM; otherwise Saturday, November 21, 11:00 AM | Every item above, creator approval |
| X announcement and navigation reply | Release day, about 12:00 PM | Public URL; composer preview |
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
