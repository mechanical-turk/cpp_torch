# Episode 4 Publishing Package

## Release target

- **YouTube publication:** Wednesday, August 19, 2026 at 11:00 AM ET
- **X announcement:** Wednesday, August 19 at approximately 12:00 PM ET
- **LinkedIn announcement:** Thursday, August 20 between 9:00 and 10:30 AM ET
- **Episode 4 native Short:** date to be determined; draw from the backlog in
  `youtube-series/shorts/episodes-01-04-ideas.md` rather than clipping this
  episode

The YouTube date remains provisional until the final export, thumbnail,
captions, metadata, and playback checks are complete.

## Final title

Building Matrix Multiplication in C++ | Deep Learning, All the Way Down #4

## YouTube description

In Episode 4 of Deep Learning, All the Way Down, our C++ tensor stops
predicting one observation at a time and starts predicting a whole batch at
once.

We implement matrix multiplication as a reference kernel, batch a linear
prediction across multiple observations in a single matmul() call, then
expose the one piece that still isn't clean: making the bias line up requires
copying it, and that copy is wasteful.

Along the way, we examine:

• Why dot() correctly rejects two rank-two tensors
• How [m,k] @ [k,n] = [m,n] determines the shape of a matrix product
• Why the two inner dimensions must agree, and why that shared dimension
  disappears from the output
• Replacing checked, general-purpose indexing with direct row-major math once
  the loop bounds already guarantee it's safe
• Why copying one repeated bias value into a full column is correct but
  wasteful, and why that waste is exactly the problem broadcasting exists to
  solve

The implementation remains in one C++23 file and uses only the standard
library, assertions, and exceptions.

Source code:
https://github.com/mechanical-turk/deep-learning-all-the-way-down

Watch the complete series:
https://www.youtube.com/playlist?list=PLZSg76FHvdTw

#cpp #deeplearning #machinelearning

## Thumbnail

Use [`thumbnail.png`](thumbnail.png).

## Chapter timestamps

Manual chapter timestamps are intentionally omitted from the initial release,
consistent with Episode 3. Revisit chapters after a transcript-assisted
workflow exists.

## Pinned comment

```text
Answers to the questions at the end:

1. k must match because it is the length of the dot product computed at every
output coordinate: each output value sums k paired terms, one from a left-matrix
row and one from a right-matrix column. It disappears from the output shape
because it is consumed by that sum, not carried forward as its own axis.

2. The copy costs one full extra allocation and a linear pass to fill it, purely
to satisfy equal-shape addition, even though every value being written is
identical. A smarter version would describe the reuse instead of materializing
it: read the same bias value for every row without ever allocating the extra
copies. That's broadcasting, and it's the subject of Episode 5.

3. The row-major formulas `row * left_cols + index` and `index * right_cols +
column` assume both operands are stored contiguously in that exact layout. A
transposed view swaps which axis moves fastest without moving any data, so the
same formulas would read the wrong elements. Once views exist, `matmul()` needs
to read through each operand's actual strides instead of assuming one fixed
layout.

Source code:
https://github.com/mechanical-turk/deep-learning-all-the-way-down

Complete playlist:
https://www.youtube.com/playlist?list=PLZSg76FHvdTw
```

## Suggested tags

```text
C++, C++23, modern C++, tensors, matrix multiplication, matmul, linear algebra,
batch prediction, linear layer, dense layer, deep learning from scratch,
machine learning from scratch, numerical computing, deep learning systems,
PyTorch internals, systems programming, broadcasting, row-major storage
```

## Upload settings

- Add the video to the **Deep Learning, All the Way Down** playlist.
- Set the language to English.
- Mark the video as not made for children.
- Upload `thumbnail.png` as the custom thumbnail.
- Add reviewed English captions. Do not rely on unreviewed automatic captions
  for C++ identifiers or mathematical terminology.
- Add an end screen linking to Episode 3 and the complete playlist.
- Leave embedding enabled.
- Keep comments enabled.
- Schedule publication for Wednesday, August 19 at 11:00 AM ET only after the
  release checklist passes.

## X announcement

### Timing

Publish Wednesday, August 19 at approximately **12:00 PM ET**, roughly one
hour after the YouTube release.

### Copy

```text
Episode 4 is out.

Our C++ tensor stops predicting one observation at a time. We implement matrix multiplication and batch a linear prediction across many observations in one call.

Then we hit the next real problem: making the bias line up means copying it, and that copy is wasteful.

https://www.youtube.com/watch?v=ZC6F284rRGo
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

- Check whether YouTube is still serving X a compact `player` card instead of
  the full-width `summary_large_image` card seen on Episodes 1 and 2. If so,
  repeat the Episode 3 workaround: remove the auto-generated preview in the
  composer and upload `thumbnail.png` directly, keeping the visible YouTube
  URL as the clickable destination.
- Remain available for technical replies during the first hour.
- Do not publish another link-only reminder on launch day.
- A later technical post should teach one idea from the episode (a good
  candidate is the wasted-bias-copy cost) rather than repeating the
  announcement copy.
- Continue the separate organic cadence of one or two genuine personal or
  process posts on most active days; do not attach the Episode 4 link to those
  posts merely because they occur during its release window.

## LinkedIn announcement

### Timing

Publish Thursday, August 20 between **9:00 and 10:30 AM ET**. This gives the X
announcement its own launch-day window and keeps LinkedIn's weekly slot
focused on this episode rather than doubling up with a separate native post
the same week.

### Copy

```text
A batch is not just a loop around a single prediction.

Episode 4 of Deep Learning, All the Way Down turns our C++ tensor from "predict one observation" into "predict a whole batch," by implementing matrix multiplication as a reference kernel.

We cover:

• why a vector dot product correctly rejects two matrices
• how [m,k] @ [k,n] = [m,n] determines the shape of a matrix product, and why the shared inner dimension disappears from the output
• replacing general-purpose checked indexing with direct row-major math once the loop bounds already guarantee it's safe
• why making the bias line up requires copying it today, and why that copy is wasteful

The implementation remains one C++23 file using only the standard library, assertions, and exceptions, so every allocation and tradeoff stays visible.

Watch Episode 4:
https://www.youtube.com/watch?v=ZC6F284rRGo

Source code:
https://github.com/mechanical-turk/deep-learning-all-the-way-down

I would especially value feedback on where the line should sit between readable indexing and performance-motivated indexing.
```

### LinkedIn strategy

- Link directly to YouTube, not through the X announcement.
- Use clean paragraphs and preserve the compact bullet list.
- Respond substantively to technical questions.
- Do not mention early view counts or ask for generic engagement.

## Reddit decision

Do **not** create a standalone Episode 4 Reddit submission. Continue treating
Reddit as a series-level, community-participation channel rather than an
announcement feed, per the existing r/cpp contribution already planned for the
series and the r/MachineLearning gate (deferred until autograd or a trained
model exists).

## Native Short

No Short is scripted specifically for Episode 4 yet. Draw the next Short from
the ranked backlog in `youtube-series/shorts/episodes-01-04-ideas.md` — the
strongest existing candidate sourced from this episode's material is "PyTorch
Calls This Linear, but Mathematically It Is Affine," which uses the bias term
this episode just introduced. Treat Short selection and scheduling as a
separate production task from this episode's launch, per the standing
Shorts-are-independent-productions rule.

## Exact release checklist

### Before scheduling

- [x] Complete the script rewrite (matmul-only scope, 15-minute-max target).
- [x] Fix the weights/bias shapes so the live-coded example matches the
      single-output model established by the opening visuals.
- [x] Rebuild `observation-to-prediction.png` and `observations-to-predictions.png`
      to match the corrected model, including the bias fix and bracket-orientation
      fix.
- [x] Generate `thumbnail.png`.
- [ ] Record Episode 4 long-form.
- [ ] Complete the rough cut; mark missing explanations, incorrect statements,
      dead air, and pickups.
- [ ] Confirm the final on-screen computation matches `predictions = {3.5, 0.0}`.
- [ ] Complete the fine cut and audio pass; export the final master.
- [ ] Watch the exported file from beginning to end without editing.
- [ ] Check code legibility at ordinary YouTube playback size.
- [ ] Check for clipped audio, abrupt edits, frozen frames, and cursor mistakes.
- [ ] Upload the video as private or unlisted.
- [ ] Add the final title, description, thumbnail, tags, playlist, captions,
      and end screen.
- [ ] Wait for HD processing and YouTube's checks to complete.
- [ ] Verify playback on desktop and mobile.
- [x] Replace every `[EPISODE_4_URL]` placeholder in this file after YouTube
      assigns the URL. (Video ID `ZC6F284rRGo`.)
- [ ] Schedule Wednesday publication only if every required check passes.

### Wednesday launch

- [ ] Capture Episode 3's approximately 48-hour analytics before this release
      changes channel traffic.
- [ ] At 10:45 AM, verify Episode 4 is still scheduled for 11:00 AM and that
      thumbnail, description, captions, playlist, and end screen are present.
- [ ] At 11:00 AM, confirm Episode 4 is publicly playable.
- [ ] Add the pinned comment (API can post; pinning remains a manual Studio
      action).
- [ ] Test every public link in the description and pinned comment.
- [ ] Record the publication time and URL in `docs/distribution-timeline.md`.
- [ ] At approximately 12:00 PM, publish the X announcement and its navigation
      reply.
- [ ] Record the X URL and exact time in the distribution ledger.
- [ ] Respond to substantive comments; do not publish another launch post.

### Thursday and later

- [ ] Thursday morning: publish the LinkedIn announcement and record its URL.
- [ ] Capture Episode 4 analytics at approximately 24 hours, 48 hours, and
      seven days after publication.
- [ ] Begin Episode 5's script; nothing exists for it yet.
- [ ] Select and schedule the next native Short from the backlog.

## Analytics snapshots

At approximately 24 hours, 48 hours, and seven days, record:

- Views
- Watch time and average view duration
- Average percentage viewed and the opening audience-retention curve
- Impressions and impressions click-through rate
- Subscribers gained
- Traffic-source distribution

Annotate which distribution events occurred between snapshots. Treat changes as
associations to investigate, not proof that a particular post caused them. This
episode is the live test of the pacing/hook restructuring — compare its opening
retention curve directly against Episodes 1-3 before drawing conclusions.
