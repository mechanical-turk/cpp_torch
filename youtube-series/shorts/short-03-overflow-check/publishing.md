# Short 3 Publishing Package

## Release target

- **TikTok:** published Thursday, August 20 at approximately 3:00 PM ET.
  learner chose to stagger platforms and start with TikTok, ahead of the
  originally planned same-batch release.
  https://www.tiktok.com/@mechaturka/video/7676185349994876190
- **YouTube Short:** uploaded, processed in HD, and scheduled for Saturday,
  August 22 at 2:00 PM ET:
  https://www.youtube.com/watch?v=3kdVmqAl-js
- **Instagram and X:** publish natively Saturday, August 22 at approximately
  2:00 PM ET. This keeps the Short clear of Episode 5's Friday YouTube and X
  launch while avoiding a long delay after the TikTok release.
- **Shorts playlist:** add to the existing **Deep Learning, All the Way Down
  | Shorts** playlist immediately after YouTube publication, after Short 2.
- **X:** publish the native video in the same Saturday batch, then add the
  standard playlist-and-source navigation reply.
- **LinkedIn:** no standalone post.
- **Reddit:** no standalone submission.

Publication remains provisional until the final export, captions,
thumbnail/cover, audio, and mobile playback checks pass on all three
platforms. Do not delay publication merely to preserve a target minute.

## Final title

```text
This Check Can Never Catch a C++ Overflow
```

## YouTube description

```text
This overflow check runs after the multiplication already happened, so it can never catch anything.

unsigned char only holds 0 through 255. 20 * 20 = 400, which wraps to 144 when it's stored back. 144 is still bigger than 20, so a check that looks for a smaller result finds nothing wrong. By the time you check, the real answer is already gone.

The fix: check whether the multiplication would overflow before you do it, not after.

Watch Episode 2, where this exact guard protects our tensor's element count:
https://www.youtube.com/watch?v=8kzL5NdxGCo

Complete series:
https://www.youtube.com/playlist?list=PLZSg76FHvdTw

Source code:
https://github.com/mechanical-turk/deep-learning-all-the-way-down

#cpp #overflow #computerscience
```

## Thumbnail

[`thumbnail.png`](thumbnail.png) is a real frame from the finished export
(the `no overflow` terminal reveal, ~13s in), with a bold "THIS CHECK LIES"
headline composited into the empty space above the terminal. Unlike Short
2's fully rendered graphic, this is a frame-plus-overlay approach. It is worth
noting as a deliberate production difference, not an inconsistency, when
comparing results.

## Chapters

No chapter markers. The Short is 23.6 seconds (measured from the final
export) and teaches one continuous idea through a live compile-and-run.

## Pinned comment

```text
The exact guard this Short is built from:
https://www.youtube.com/watch?v=8kzL5NdxGCo

Complete series:
https://www.youtube.com/playlist?list=PLZSg76FHvdTw

Source code:
https://github.com/mechanical-turk/deep-learning-all-the-way-down
```

## Suggested tags

```text
C++, unsigned char, integer overflow, integer overflow check, overflow
detection, undefined behavior, wraparound, systems programming, deep
learning from scratch, machine learning from scratch, deep learning
systems, PyTorch internals, numerical computing
```

## Upload settings

- Upload the final 1080x1920 vertical export.
- Confirm YouTube classifies it as a Short.
- Set the title and description exactly as written above.
- Set the language to English.
- Mark it as not made for children.
- Add it to the **Deep Learning, All the Way Down | Shorts** playlist,
  after Short 2.
- Do not add it to the long-form course playlist.
- Upload `thumbnail.png` as the custom thumbnail.
- Add Episode 2 as the **related video** in YouTube Studio. This is the
  episode the overflow guard is drawn from.
- Review automatic captions closely for `unsigned char`, `x < 20`, and the
  compiled terminal output (`no overflow`, `overflow`); these are exactly
  the terms automatic captioning tends to mangle.
- Keep comments and embedding enabled.

## Instagram post

### Timing

Publish natively as a Reel on **Saturday, August 22 at approximately 2:00 PM
ET**, in the same batch as YouTube and X.

### What we're watching for this time

Short 2's Instagram numbers are the strongest baseline the series has:
10,399 views and 7,320 reach within a day, 85 interactions including 15
saves and 9 shares, off a 6-follower account. This is clear evidence the
front-loaded, declarative-hook structure ("This X can never Y," stated
before it's explained) travels well here. This Short reuses that exact
hook shape. It's also structurally different from Short 2 in one respect:
it's a live compile-and-run rather than a pure visual reveal, and it's
somewhat longer (23.6s vs. Short 2's ~22s). Treat the 24-hour average watch
time and completion rate as the direct test of whether the hook template
generalizes to a live-coding format, not just a short, pure-reveal one.

### Cover image

Use `thumbnail.png` as the Reel cover, same asset as the YouTube thumbnail
and TikTok cover.

### Caption

```text
This overflow check can never catch anything.

unsigned char only holds 0-255. 20 * 20 = 400, which wraps to 144, and 144 is still bigger than 20. The check that's supposed to catch the overflow finds nothing wrong, because by the time it runs, the real answer is already gone.

Full series in bio.
```

### Hashtags

```text
#cpp #coding #programming #computerscience
```

Same four-tag set as Short 2, placed at the end of the caption. No
evidence yet that a larger tag block changes reach at this account size.

### First comment

Post and pin immediately after publishing:

```text
The exact guard this is built from:
https://www.youtube.com/watch?v=8kzL5NdxGCo

Complete series:
https://www.youtube.com/playlist?list=PLZSg76FHvdTw
```

### Settings

- Audio: original recorded narration only.
- Allow remix/use-audio: on.
- Share to Feed: on, in addition to Reels.
- Share to Stories: off by default.
- Alt text: write manually. For example, "C++ code demonstrating that
  checking for integer overflow after multiplying an unsigned char fails,
  because the wrapped result can still look larger than the original
  value."
- Comments: enabled.

### Instagram strategy

- Native upload only, never a cross-post of the YouTube or TikTok file.
- Link only through the bio and the pinned first comment.
- At 24 hours, compare average watch time and completion rate directly
  against Short 2's own checkpoints, not just raw view count. Short 2 is
  now the series' best-performing baseline, so this is the first real test
  of whether that result repeats.

## TikTok post

### Timing

Published natively on **Thursday, August 20 at approximately 3:00 PM ET**:
https://www.tiktok.com/@mechaturka/video/7676185349994876190

### Safe area

Reuse the universal 9:16 export/safe-area setup confirmed working for
Short 2. Keep the code, the wrapped value, and the fix clear of the
right-edge and bottom UI regions. No platform-specific re-crop needed
unless a new UI element is found to intrude.

### Caption

```text
This overflow check can never catch anything (and it looks completely fine)

unsigned char wraps at 255. 20 * 20 wraps to 144. It is still bigger than 20, so the check says nothing's wrong. Full series in bio.
```

### Hashtags

```text
#cpp #coding #programming #softwareengineering #computerscience #stem
```

### Cover frame

Use `thumbnail.png`, same asset as YouTube and Instagram.

### Settings

- Sound: original audio only.
- Comments: enabled. Pin the creator's own first comment with the same
  navigation links used in the Instagram pinned comment.
- Duet and Stitch: allow both.
- Link: rely on the bio link and the pinned comment; the description link
  will not render as clickable at this account's current size.

### TikTok strategy

- Second TikTok data point for the account. Compare directly against
  Short 2's TikTok checkpoints once available, not against X or Instagram
  history from before TikTok joined the rotation.
- Capture 24- and 72-hour checkpoints and record them in
  `docs/distribution-timeline.md`.

## X post

### Timing

Publish the video natively on **Saturday, August 22 at approximately 2:00 PM
ET**, alongside the YouTube Short and Instagram Reel.

### Main post

```text
this overflow check can never catch an overflow.

20 * 20 is 400, but an unsigned char stores 144. since 144 is still greater than 20, the check says nothing went wrong.

the bug is checking after the multiplication.
```

### Navigation reply

```text
The full tensor lesson where we build the correct guard:
https://www.youtube.com/watch?v=8kzL5NdxGCo

Complete playlist:
https://www.youtube.com/playlist?list=PLZSg76FHvdTw

Source code:
https://github.com/mechanical-turk/deep-learning-all-the-way-down
```

Upload the original 1080x1920 master directly to X. Do not link to the
YouTube Short in the main post.

## LinkedIn decision

Do not create a standalone LinkedIn announcement for this Short, consistent
with Short 2: LinkedIn's one weekly native slot is reserved per the
standing cadence, and a sub-40-second bug explainer is a weaker fit for
that slot than a technical write-up or full-episode repost.

## Reddit decision

Do not submit this Short to Reddit. It is not a series-level milestone and
would read as an announcement-feed post rather than a genuine community
contribution.

## Post-publication checks

Record snapshots in `docs/distribution-timeline.md` at approximately:

- **1 hour:** views and obvious caption, cover, or playback problems on
  YouTube, Instagram, and TikTok.
- **24 hours:** views, likes, average percentage viewed, viewed versus
  swiped away, traffic sources, and subscriber/follower conversion on each
  platform. Compare Instagram's average watch time and TikTok's numbers
  directly against Short 2's own checkpoints.
- **72 hours:** the same metrics, plus an updated TikTok-vs-Instagram
  comparison now that TikTok has two data points.

Treat this as the third data point in the Shorts format experiment. It is the
first real test of whether Short 2's declarative-hook, front-loaded
structure generalizes to a longer, live-coded format, or whether it was
partly specific to Short 2's shorter runtime.

## Source assets

- Recording script: [`script.md`](script.md)
- Final export: `~/Movies/CapCut/shorts ep 03.mov`
- Custom thumbnail and cover: [`thumbnail.png`](thumbnail.png)
