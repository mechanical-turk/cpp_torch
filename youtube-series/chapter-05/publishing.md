# Episode 5 Publishing Package

## Release target

- **YouTube publication:** Friday, August 21, 2026 — learner decision,
  moved up one day from the Monday/Wednesday/Saturday cadence's next slot
  (Saturday, August 22). This is a deliberate one-off, not a cadence
  change; `youtube-series/production/posting-cadence.md` still governs the
  standing schedule. Friday is also the standing Short B slot, which this
  week's Short 3 already partially occupies (TikTok published Thursday,
  August 20) — reconcile Short 3's remaining Instagram post against this
  release rather than running both blind.
- **X announcement:** Friday, August 21 at approximately 12:00 PM ET
- **LinkedIn announcement:** Saturday, August 22 between 9:00 and 10:30 AM
  ET (the day-after slot, mirroring the Wednesday-episode -> Thursday
  pattern; the standing grid has no Friday-episode row since Friday isn't
  normally a long-form day)
- **Episode 5 native Short:** date to be determined; no Episode-5-specific
  Short backlog exists yet. Add candidates (a strong option is the
  `[3,1]` bias vs. `[3,1]` uniform-bias vs. scalar-bias contrast used in the
  cold open, or the stride-zero reuse trick) and schedule separately from
  this episode's launch, per the standing Shorts-are-independent-productions
  rule.

The YouTube date remains provisional until the final export, thumbnail,
captions, metadata, and playback checks are complete.

## Final title

Implementing Broadcasting in C++: One Rule for Every Compatible Shape | Deep Learning, All the Way Down #5

## YouTube description

In Episode 5 of *Deep Learning, All the Way Down*, our C++ tensor stops
requiring two operands to have the exact same shape.

We implement real broadcasting: align two shapes from the right, let a
size-one axis stretch to match the other side, and give every stretched axis
a stride of zero so it reuses one value instead of needing a copy. The
manual bias-copy workaround from Episode 4 is gone, and the same rule
already covers cases a scalar-only fix never could.

Along the way, we examine:

- The align-from-the-right, size-one-stretches rule that decides whether two
  different shapes are actually compatible
- Why `broadcast_shape()` and `effective_strides()` are `static` member
  functions instead of ordinary ones
- Why a broadcast axis gets a stride of zero, and why that's the only choice
  that's correct without knowing in advance whether the axis will actually
  be stretched
- Walking every position in an N-dimensional output exactly once, the same
  way a car odometer counts
- Verifying the rule against both the easy case (a scalar bias) and a case a
  scalar-only fix couldn't handle (subtracting one per-feature offset from
  an entire batch)

The implementation remains in one C++23 file and uses only the standard
library, assertions, and exceptions.

Source code:
https://github.com/mechanical-turk/deep-learning-all-the-way-down

Watch the complete series:
https://www.youtube.com/playlist?list=PLZSg76FHvdTw

#cpp #deeplearning #machinelearning

## Thumbnail

Not yet generated. Add `thumbnail.png` to this directory before scheduling;
see the release checklist below.

## Chapter timestamps

Manual chapter timestamps are intentionally omitted from the initial
release, consistent with Episodes 3 and 4. Revisit chapters after a
transcript-assisted workflow exists.

## Pinned comment

```text
Answers to the questions at the end:

1. The flat index is a sum of coordinate[axis] * stride[axis] across every
axis. When an axis's effective stride is zero, that term is coordinate[axis]
* 0, which is 0 no matter what the coordinate actually is. So that axis
never contributes to the index, regardless of how far the output walks along
it — the same underlying element gets read every time, with no separate
check needed anywhere in the traversal.

2. A scalar is already the general rule's most extreme case: it has no axes
at all, so every axis reads as an implicit 1 and stretches against anything.
Keeping a scalar-specific copy path would mean maintaining a second way to
do exactly what the general rule already does correctly, and for free —
duplicated logic with no actual benefit, since the general path is neither
slower nor less correct.

3. Padding on the right would misalign every existing axis instead of just
the missing ones. A `[3]` shape is meant to line up against the *last* axis
of a `[2,3]` shape — the feature axis — so its three values get reused
across observations. Right-padding would instead compare that 3 against the
*first* axis of `[2,3]`, the observations axis, either rejecting a shape
pair that should have worked or silently reusing values along the wrong
dimension.

Source code:
https://github.com/mechanical-turk/deep-learning-all-the-way-down

Complete playlist:
https://www.youtube.com/playlist?list=PLZSg76FHvdTw
```

## Suggested tags

```text
C++, C++23, modern C++, tensors, broadcasting, numpy broadcasting, tensor
shapes, strides, stride tricks, deep learning from scratch, machine learning
from scratch, numerical computing, deep learning systems, PyTorch internals,
systems programming, row-major storage, N-dimensional arrays
```

## Upload settings

- Add the video to the **Deep Learning, All the Way Down** playlist.
- Set the language to English.
- Mark the video as not made for children.
- Upload `thumbnail.png` as the custom thumbnail.
- Add reviewed English captions. Do not rely on unreviewed automatic
  captions for C++ identifiers or mathematical terminology.
- Add an end screen linking to Episode 4 and the complete playlist.
- Leave embedding enabled.
- Keep comments enabled.
- Schedule publication for Friday, August 21 (target time still to be
  set — not necessarily 11:00 AM ET, since this is off the standing
  cadence) only after the release checklist passes.

## X announcement

### Timing

Publish Friday, August 21 at approximately **12:00 PM ET**, roughly one
hour after the YouTube release.

### Copy

```text
Episode 5 is out.

Our C++ tensor no longer needs both operands to have the exact same shape. We implement real broadcasting: align from the right, stretch size-one axes, and give every stretched axis a stride of zero so it reuses a value instead of needing a copy.

The manual bias-copy hack from Episode 4 is gone. And the same rule already handles cases a scalar-only fix never could, like subtracting one per-feature offset from an entire batch.

https://www.youtube.com/watch?v=[EPISODE_5_URL]
```

### Series navigation reply

Immediately reply beneath the announcement with:

```text
Complete playlist:
https://www.youtube.com/playlist?list=PLZSg76FHvdTw

Source code:
https://github.com/mechanical-turk/deep-learning-all-the-way-down
```

### X strategy

- Confirm YouTube is serving X the full-width `summary_large_image` card
  before posting; if it's still serving a compact `player` card, repeat the
  Episode 3/4 workaround (remove the auto-generated preview, upload
  `thumbnail.png` directly, keep the visible YouTube URL as the clickable
  destination).
- Remain available for technical replies during the first hour.
- Do not publish another link-only reminder on launch day.
- A later technical post should teach one idea from the episode rather than
  repeat the announcement copy — the stride-zero reuse trick is the
  strongest candidate.
- Continue the separate organic cadence of one or two genuine personal or
  process posts on most active days; do not attach the Episode 5 link to
  those posts merely because they occur during its release window.

## LinkedIn announcement

### Timing

Publish Saturday, August 22 between **9:00 and 10:30 AM ET** — the
day-after slot, since Friday isn't a standing long-form day and the grid
has no dedicated Friday-episode LinkedIn row.

### Copy

```text
A shape check that only accepts identical shapes is the special case, not the rule.

Episode 5 of Deep Learning, All the Way Down implements real broadcasting in our from-scratch C++ tensor: two shapes align from the right, a size-one axis stretches to match the other side, and any stretched axis gets a stride of zero so it reuses one value instead of needing a copy.

We cover:

• the align-from-the-right, size-one-stretches rule that decides shape compatibility
• why the new helper functions are static member functions instead of ordinary ones
• why a stride of zero is the only choice that's correct before the function knows whether an axis will actually be stretched
• walking every position in an N-dimensional output exactly once, the same way a car odometer counts
• verifying the rule against the easy case (a scalar bias) and a case a scalar-only fix never could handle (a per-feature offset subtracted from an entire batch)

The implementation remains one C++23 file using only the standard library, assertions, and exceptions, so every allocation and tradeoff stays visible.

Watch Episode 5:
https://www.youtube.com/watch?v=[EPISODE_5_URL]

Source code:
https://github.com/mechanical-turk/deep-learning-all-the-way-down

I would especially value feedback on the effective_strides design: is committing to a stride before knowing whether an axis will be stretched the right tradeoff, or would you structure that differently?
```

### LinkedIn strategy

- Link directly to YouTube, not through the X announcement.
- Use clean paragraphs and preserve the compact bullet list.
- Respond substantively to technical questions.
- Do not mention early view counts or ask for generic engagement.

## Reddit decision

Do **not** create a standalone Episode 5 Reddit submission. Continue
treating Reddit as a series-level, community-participation channel rather
than an announcement feed, per the existing r/cpp contribution already
planned for the series and the r/MachineLearning gate (deferred until
autograd or a trained model exists).

## Native Short

No Short is scripted specifically for Episode 5 yet. Two strong candidates
from this episode's material: the cold-open contrast between a `[2,1]`
bias, a uniform-but-still-`[2,1]` bias, and a scalar bias; or the
stride-zero reuse trick itself (why a single value can stand in for an
entire axis without being copied). Treat Short selection and scheduling as
a separate production task from this episode's launch, per the standing
Shorts-are-independent-productions rule.

## Exact release checklist

### Before scheduling

- [x] Complete the script rewrite, grounded in the actual reference
      implementation (`deep-learning-all-the-way-down`, commit `022c750`).
- [x] Rebuild `shapes-still-rejected.png` for the cold open.
- [ ] Record Episode 5 long-form.
- [ ] Complete the rough cut; mark missing explanations, incorrect
      statements, dead air, and pickups.
- [ ] Confirm the final on-screen computation matches
      `predictions.data() == {3.5, 0.0}` and
      `centered.data() == {3.0, 2.0, 1.5, 0.0, 1.0, 0.0}`.
- [ ] Complete the fine cut and audio pass; export the final master.
- [ ] Watch the exported file from beginning to end without editing.
- [ ] Check code legibility at ordinary YouTube playback size, especially
      the five new functions (`strides`, `broadcast_shape`,
      `effective_strides`, `stride_offset`, `advance_coordinate`).
- [ ] Check for clipped audio, abrupt edits, frozen frames, and cursor
      mistakes.
- [ ] Generate `thumbnail.png`.
- [ ] Upload the video as private or unlisted.
- [ ] Add the final title, description, thumbnail, tags, playlist,
      captions, and end screen.
- [ ] Wait for HD processing and YouTube's checks to complete.
- [ ] Verify playback on desktop and mobile.
- [ ] Replace every `[EPISODE_5_URL]` placeholder in this file after
      YouTube assigns the URL.
- [ ] Schedule Friday publication only if every required check passes.

### Friday launch

- [ ] Capture Episode 4's approximately 72-hour analytics before this
      release changes channel traffic.
- [ ] At 10:45 AM, verify Episode 5 is still scheduled for 11:00 AM and
      that thumbnail, description, captions, playlist, and end screen are
      present.
- [ ] At 11:00 AM, confirm Episode 5 is publicly playable.
- [ ] Add the pinned comment (API can post; pinning remains a manual Studio
      action).
- [ ] Test every public link in the description and pinned comment.
- [ ] Record the publication time and URL in `docs/distribution-timeline.md`.
- [ ] At approximately 12:00 PM, publish the X announcement and its
      navigation reply.
- [ ] Record the X URL and exact time in the distribution ledger.
- [ ] Respond to substantive comments; do not publish another launch post.

### Saturday and later

- [ ] Saturday morning: publish the LinkedIn announcement and record its URL.
- [ ] Capture Episode 5 analytics at approximately 24 hours, 48 hours, and
      seven days after publication.
- [ ] Begin Episode 6's script; nothing exists for it yet.
- [ ] Select and schedule the next native Short from the backlog.

## Analytics snapshots

At approximately 24 hours, 48 hours, and seven days, record:

- Views
- Watch time and average view duration
- Average percentage viewed and the opening audience-retention curve
- Impressions and impressions click-through rate
- Subscribers gained
- Traffic-source distribution

Annotate which distribution events occurred between snapshots. Treat
changes as associations to investigate, not proof that a particular post
caused them.
