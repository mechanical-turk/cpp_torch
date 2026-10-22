# Chapter 14 distribution

Procedure: [distribution operations](../../docs/operations/distribution.md).
Ledger: [distribution timeline](../../docs/distribution-timeline.md) (append-only;
log completed events there). Standing schedule:
[posting cadence](../production/posting-cadence.md).

## Current instruction

October 22, 2026: no release instruction has been given. Upload, scheduling,
announcements, comments, Reddit, Shorts and any push of the demo repository all
need the creator's explicit approval. This file records plans and facts, and
no completed external event.

Canonical title, description, tags, first-comment candidate, X and LinkedIn
copy: [publishing.md](publishing.md). Do not maintain duplicate copy here.
Package status: score 74/100, hold for public release.

## Upload record

- File: `aliases/04-final-cuts/ep14/cpp-residual-connections-gradient-debugging.mp4`
  (`/Users/keremkazan/Movies/CapCut/ep14/`). It is the export itself, not a
  hard link to another file.
- SHA-256: `385b1922f1fdd3821eb25ff20fb2b2b2baaf5fb36631c496431fd1ab6cce89fc`
- 3840x2160, 30 fps, H.264, one AAC stereo stream at 48 kHz. Duration
  52:23.967. Size 6,254,404,700 bytes. Modified October 21, 2026 19:09.
- Upload status: none recorded in the timeline or the repository. Whether the
  creator uploaded it by hand is unknown. No watch URL exists in this record.
- Reviewed: container and stream probe, whole-file audio levels, 13 sampled frames.
  Not reviewed: full playback, narration, captions, YouTube 2160p playback.

## Before public release

- Thumbnail: none exists. Follow the visual asset and thumbnail research
  guidelines; do not reuse another episode's image.
- End tail: the file ends in continuous speech, so there is no clean tail for the
  Subscribe and complete-series playlist end screen. Creator decision: append
  about five clean seconds, or place the end screen over speech.
- Captions and chapters: after upload, download the English captions, derive
  chapters from actual transitions (the runtime is 52:24, so split long
  sections), correct ASR errors such as MNIST and tanh, then complete the
  description in publishing.md.
- Settings after approval: private and unscheduled first; English; Education;
  not made for kids; add to the complete-series playlist.
- Inspect 2160p playback, code legibility and audio in the YouTube encode.

## Public source

- The recorded final run (20 epochs, starting rate 0.08, decay 0.95, 92.85%,
  1857 of 2000) matches the local demo repository commit `47db7ed`
  ("Add layer names, tracing and Residual layer for Episode 14").
- Not pushed. README currently marks Episode 14 as work in progress, with no
  checkpoint hash or video link. At release: push, add the hash and the
  YouTube URL to the Episode 14 row and summary, add a work-in-progress row for
  the next episode, confirm `origin/main` matches, and compile and run both
  entry points.

## Proposed sequence (a plan, not events)

Today is Thursday, October 22, 2026. The standing cadence publishes long-form at
11:00 AM ET on Monday, Wednesday and Saturday, announces on X about an hour
later, and announces on LinkedIn the next weekday at 9:00 to 10:30 AM ET. This
proposal makes no claim that timing causes a result.

| Step | Proposed window (ET) | Depends on |
| --- | --- | --- |
| Private upload | After creator approval | Approval; thumbnail not required to upload privately |
| Captions and chapters | After processing finishes | Upload |
| Thumbnail, end tail, 2160p and settings checks | Before release | Creator decisions above |
| Push demo repository and update README | Immediately before release | Approval; verified URL |
| Public release | Earliest Monday, October 26, 11:00 AM; otherwise Wednesday, October 28, 11:00 AM | Every item above |
| X announcement and navigation reply | Release day, about 12:00 PM | Public URL; composer preview |
| LinkedIn announcement and author comment | Next weekday, 9:00 to 10:30 AM | Public URL; at least a day after X |
| Post-publication check, comment duplicate inspection | After release | Authorization |

## Explicit deferrals

- Reddit: defer. A post needs the Reddit research and strategy notes and the
  current rules of the chosen community, and a new angle and copy.
- Shorts: defer. No concept is selected or scripted. Candidates go through the
  short-form playbook and critique check first.
- Chapter 13 announcements: whether the X and LinkedIn drafts were ever posted
  is unverified in the timeline. Confirm before scheduling, so the two
  announcements do not collide.
- Comments: the first-comment candidate stays unposted until the video is
  public and the creator approves it.

## Completed events

None recorded for Chapter 14.
