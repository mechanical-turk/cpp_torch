# Short 2 Publishing Package

## Release target

- **YouTube Short:** Tuesday, August 18, 2026 at approximately 2:00 PM ET —
  today's designated Short A slot in the standing posting cadence.
- **Shorts playlist:** add to the existing **Deep Learning, All the Way Down
  | Shorts** playlist immediately after publication.
- **X, Instagram, and TikTok:** approximately 3:00 PM ET, one native upload
  batch, roughly an hour after the YouTube release. This is the first Short
  posted natively to TikTok — the right-edge/bottom safe-area issue that
  blocked TikTok for Short 1 is now resolved.
- **LinkedIn:** no standalone post.
- **Reddit:** no standalone submission.

Publication remains provisional until the final export, captions, thumbnail,
audio, and mobile playback checks pass on all four platforms. Do not delay
publication merely to preserve a target minute.

## Final title

```text
This C++ Loop Can Never Finish
```

## YouTube description

```text
This reverse loop looks completely normal, right up until i hits zero.

size_t is unsigned, so it can never go negative. Decrementing past zero wraps around to the largest value the type can hold, and i >= 0 stays true forever, because it always was. The exit condition can never fail.

The fix: check before you decrement, not after.

Watch Episode 1, where this exact failure shows up:
https://www.youtube.com/watch?v=DmU2b64tWfA

Complete series:
https://www.youtube.com/playlist?list=PLZSg76FHvdTw

Source code:
https://github.com/mechanical-turk/deep-learning-all-the-way-down

#cpp #deeplearning #machinelearning
```

## Thumbnail

Upload [`thumbnail.png`](thumbnail.png) as the custom YouTube thumbnail. It
uses the established series branding and reduces the lesson to one visual
sequence: the condition `i >= 0`, followed by `size_t i = 0`, `--i`, and the
wrapped value `18446744073709551615`.

## Chapters

No chapter markers. The Short is approximately 22 seconds and teaches one
continuous idea.

## Pinned comment

```text
The exact failure this Short is built from:
https://www.youtube.com/watch?v=DmU2b64tWfA

Complete series:
https://www.youtube.com/playlist?list=PLZSg76FHvdTw

Source code:
https://github.com/mechanical-turk/deep-learning-all-the-way-down
```

## Suggested tags

```text
C++, size_t, unsigned integer, integer underflow, integer overflow,
reverse loop, off-by-one, undefined behavior, loop invariant,
systems programming, deep learning from scratch, machine learning from
scratch, deep learning systems, PyTorch internals, numerical computing
```

## Upload settings

- Upload the final 1080x1920 vertical export.
- Confirm YouTube classifies it as a Short.
- Set the title and description exactly as written above.
- Set the language to English.
- Mark it as not made for children.
- Add it to the **Deep Learning, All the Way Down | Shorts** playlist, after
  Short 1.
- Do not add it to the long-form course playlist.
- Upload [`thumbnail.png`](thumbnail.png) as the custom thumbnail.
- Add Episode 1 as the **related video** in YouTube Studio — this is the
  episode the failure is drawn from.
- Review automatic captions closely for `size_t`, `i >= 0`, and the wrapped
  numeric literal; these are exactly the terms automatic captioning tends to
  mangle.
- Keep comments and embedding enabled.

## X post

### Timing

Publish natively at approximately **3:00 PM ET**, alongside the Instagram and
TikTok uploads. Upload the final video file directly; do not link to the
YouTube Short.

### Copy

```text
This loop looks completely normal.

for (std::size_t i = n - 1; i >= 0; --i)

size_t can't go negative. When i hits zero and decrements again, it wraps around to the largest value the type holds — and i >= 0 was always going to be true.
```

### Series navigation reply

```text
The exact failure this is built from:
https://www.youtube.com/watch?v=DmU2b64tWfA

Complete series:
https://www.youtube.com/playlist?list=PLZSg76FHvdTw

Source code:
https://github.com/mechanical-turk/deep-learning-all-the-way-down
```

### X strategy

- Native upload, self-contained without the click.
- Full links live only in the navigation reply, same convention as every
  prior announcement.
- Remain available for replies during the first hour; unsigned-underflow
  bugs reliably draw "well actually" replies from C++ people — treat those as
  genuine engagement, not noise.
- Do not publish a second post for this Short.

## Instagram post

### Timing

Publish natively as a Reel at approximately **3:00 PM ET**, same batch as X
and TikTok.

### The risk this Short is specifically testing on Instagram

Instagram is the one platform with a real, damning data point already:
Short 1 averaged **5.44 seconds** of watch time against its 34-second
runtime — about 16% completion, and the steepest drop-off measured on any
platform so far, worse than X's early-loss funnel. Short 1's explanation
didn't begin until roughly seven seconds in; most Instagram viewers never
got there.

This Short's entire structure is built to front-load the payoff instead: the
loop is visible and the "this can never finish" claim lands in the first
four seconds, with the wraparound reveal by second nine. Treat Instagram's
24-hour average watch time as the single most important number to check for
this release — it is the direct test of whether the restructuring actually
fixes the problem Short 1 exposed, more than the view count on any platform.

### Cover image

Use [`thumbnail.png`](thumbnail.png) as the Reel cover, same asset as the
YouTube thumbnail and TikTok cover. One consistent cover across all three
platforms.

### Caption

```text
This C++ loop can never finish.

size_t is unsigned — it can't go negative. Decrement past zero and it wraps around to the largest number the type can hold, so the loop's own exit condition can never become false.

Full series in bio.
```

Keep it short. Instagram truncates captions aggressively in-feed, and the
visual itself carries the explanation — the caption only needs to work as a
standalone summary for anyone who doesn't watch.

### Hashtags

```text
#cpp #coding #programming #computerscience
```

Place these at the end of the caption, not as a separate first comment.
Four is deliberately restrictive: Instagram's own guidance favors a small
number of specific, genuinely relevant tags over a large generic block, and
the account has no evidence yet that hashtag volume changes reach here.

### First comment

Instagram Reels support pinning up to three comments. Post and pin this one
immediately after publishing:

```text
The exact failure this is built from:
https://www.youtube.com/watch?v=DmU2b64tWfA

Complete series:
https://www.youtube.com/playlist?list=PLZSg76FHvdTw
```

Keep the GitHub link in the bio rather than duplicating it here; the pinned
comment is for the single most relevant link, not every link.

### Settings

- Audio: keep the original recorded narration. Do not swap in trending
  audio — the spoken explanation is the content, and detached audio would
  make the video unusable.
- Allow remix/use-audio: on. Low cost, and it is the only path to any
  reach beyond the account's own followers at this size.
- Share to Feed: on, in addition to appearing in Reels — do not limit
  distribution to the Reels tab alone.
- Share to Stories: off by default; this is a standalone lesson, not a
  moment worth a separate Stories callout unless it clearly outperforms
  Short 1 after 24 hours.
- Alt text: write it manually rather than accepting Instagram's
  auto-generated description. Something like: "A C++ for-loop using
  std::size_t that appears to count down but can never exit, because an
  unsigned integer can never become negative."
- Comments: enabled.

### Instagram strategy

- Native upload only; never a repost of the YouTube or X file via a
  cross-posting tool, per the standing native-only rule.
- Link only through the bio and the pinned first comment, consistent with
  Short 1's approach — Instagram Reels captions do not render links as
  clickable at this account's size regardless.
- At the 24-hour checkpoint, compare average watch time, completion rate,
  reach, and accounts-reached directly against Short 1's own checkpoints
  (4.73s at ~20 minutes, 5.44s at ~75 minutes, 7.32s by the next morning) —
  same platform, same measurement, the cleanest apples-to-apples comparison
  available across the whole Shorts experiment so far.
- If average watch time is still well under 10 seconds at 24 hours, that is
  evidence the front-loaded restructuring did not fix Instagram's specific
  problem, and the next Short should test cutting straight to the wraparound
  reveal with no setup at all, rather than assuming duration alone is the
  fix.

## TikTok post

### Timing

Publish natively at approximately **3:00 PM ET**, same batch as X and
Instagram. This is the first Short in the series posted to TikTok.

### Safe area

Confirmed resolved: the 9:16 master now keeps the loop code, the wrapped
value, and the fix within TikTok's actual safe area (clear of the right-edge
profile/share column and the bottom caption/interaction bar), verified
against the same universal export used for YouTube Shorts and Instagram — no
TikTok-specific re-crop needed. If a future review finds new UI intruding
into that region, fix the master, not this one video.

### Caption

```text
This C++ loop can never finish (and it's not a typo)

size_t can't go negative, so the exit condition can never fail. Full series in bio.
```

### Hashtags

```text
#cpp #coding #programming #softwareengineering #computerscience #stem
```

Keep the hashtag set small and genuinely descriptive. Do not add
high-volume/unrelated tags purely to chase reach; that misrepresents the
content and draws the wrong audience.

### Cover frame

Use [`thumbnail.png`](thumbnail.png) as the cover wherever the platform allows
a separate cover image. Otherwise choose the closest frame from the export,
with `18446744073709551615` centered and unobstructed.

### Settings

- Sound: original audio only. Do not attach trending audio; the spoken
  narration is the content.
- Comments: enabled. Pin the creator's own first comment with the same
  navigation links used in the X reply — TikTok allows pinning a comment
  directly, unlike the YouTube API.
- Duet and Stitch: allow both. A technical short like this benefits from
  reaction/response content more than it risks misrepresentation.
- Link: TikTok will not make the description link clickable at this account's
  current size; rely on the bio link and the pinned comment instead.

### TikTok strategy

- This is a new-platform baseline test, not a proven format yet. Capture 24-
  and 72-hour checkpoints the same way Short 1 was measured on X and
  Instagram, and record them in `docs/distribution-timeline.md`.
- Do not treat first-Short-on-a-new-platform numbers as representative of
  TikTok's ceiling for this content; the account has zero prior TikTok
  history and zero followers.
- If this Short performs meaningfully differently on TikTok than on X or
  Instagram, that comparison — not raw view count — is the useful signal.

## LinkedIn decision

Do not create a standalone LinkedIn announcement for this Short. LinkedIn's
one weekly native slot (Thursday) is reserved per the standing cadence, and a
41-second bug explainer is a weaker fit for that audience than a technical
write-up or a full-episode repost.

## Reddit decision

Do not submit this Short to Reddit. It is not a series-level milestone and
would read as an announcement-feed post rather than a genuine community
contribution.

## Post-publication checks

Record snapshots in `docs/distribution-timeline.md` at approximately:

- **1 hour:** views and obvious caption, cover, or playback problems on all
  four platforms, including whether the TikTok safe-area fix actually held.
- **24 hours:** views, likes, average percentage viewed, viewed versus
  swiped away, traffic sources, and subscriber/follower conversion on each
  platform. Compare Instagram's average watch time directly against Short 1's
  5.44-second baseline.
- **72 hours:** the same metrics, plus a first TikTok-vs-X-vs-Instagram
  comparison now that TikTok has one full data point.

Treat this as the second data point in the Shorts format experiment, not a
verdict. Two Shorts is still not enough to declare a winning duration,
platform, or disclosure style.

## Source assets

- Recording script: [`script.md`](script.md)
- Custom thumbnail and cover: [`thumbnail.png`](thumbnail.png)
