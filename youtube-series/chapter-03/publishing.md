# Episode 3 Publishing Package

## Release target

- **YouTube publication:** Monday, August 17, 2026 at 11:00 AM ET
- **X announcement:** Monday, August 17 at approximately 12:00 PM ET
- **LinkedIn announcement:** Tuesday, August 18 between 9:00 and 10:30 AM ET
- **Episode 3 native Short:** Friday, August 21 around noon ET

The YouTube date remains provisional until the final export, thumbnail, captions,
metadata, and playback checks are complete.

## Final title

Building a Linear Prediction from Scratch in C++ | Deep Learning, All the Way Down #3

## YouTube description

In Episode 3 of Deep Learning, All the Way Down, our C++ tensor stops being
only a container and begins participating in numerical computation.

We implement equal-shape tensor addition, subtraction, and multiplication,
separate shared traversal from the arithmetic performed at each element, make
reductions return scalar tensors, and build dot product by composing
elementwise multiplication with sum().

Finally, we use those operations to express a complete linear prediction:

prediction = weights.dot(features) + bias

Along the way, we examine:

• The precise contract behind equal-shape elementwise operations
• Why operators return new tensors without modifying their operands
• How one traversal helper can support several arithmetic operations
• Why a full reduction produces a rank-zero tensor
• How dot product combines multiplication and reduction
• The difference between forward computation and learning
• A deliberate intermediate allocation that we will benchmark and optimize later

The implementation remains in one C++23 file and uses only the standard
library, assertions, and exceptions.

Source code:
https://github.com/mechanical-turk/deep-learning-all-the-way-down

Watch the complete series:
https://www.youtube.com/playlist?list=PLZSg76FHvdTw

#cpp #deeplearning #machinelearning

## Thumbnail

Use [`thumbnail.png`](thumbnail.png).

Thumbnail text:

```text
TEACH TENSORS TO COMPUTE
```

The computation shown is the exact example used in the episode:

```text
[0.5, -1, 2] dot [4, 3, 2] + 0.5 = 3.5
```

## Chapter timestamps

Manual chapter timestamps are intentionally omitted from the initial release.
The edited video no longer matches the recording-script estimates, and manually
recovering every boundary would have lower value than completing the release and
the next episode. Revisit chapters after a transcript-assisted workflow exists.

## Pinned comment

```text
Answers to the questions at the end:

1. Equal-shape elementwise operations preserve shape because every shared
coordinate produces exactly one output coordinate.

2. A full sum reduces every axis, leaving one scalar with shape []. Constructing
that result tensor can allocate and throw, so sum() cannot remain noexcept.

3. weights.dot(features) multiplies corresponding features and weights and
reduces their contributions to one scalar. Adding the scalar bias produces the
linear prediction.

Source code:
https://github.com/mechanical-turk/deep-learning-all-the-way-down

Complete playlist:
https://www.youtube.com/playlist?list=PLZSg76FHvdTw
```

## Suggested tags

```text
C++, C++23, modern C++, tensors, tensor operations, operator overloading,
elementwise operations, tensor addition, tensor multiplication, reductions,
dot product, linear model, linear prediction, deep learning from scratch,
machine learning from scratch, numerical computing, deep learning systems,
PyTorch internals, systems programming
```

## Upload settings

- Add the video to the **Deep Learning, All the Way Down** playlist.
- Set the language to English.
- Mark the video as not made for children.
- Upload `thumbnail.png` as the custom thumbnail.
- Do not add the obsolete recording-script timestamps to the description.
- Add reviewed English captions. Do not rely on unreviewed automatic captions
  for C++ identifiers or mathematical terminology.
- Add an end screen linking to Episode 2 and the complete playlist.
- If a card is used, link Episode 2 near the opening retrieval section rather
  than interrupting the central implementation.
- Leave embedding enabled.
- Keep comments enabled.
- Schedule publication for Monday, August 17 at 11:00 AM ET only after the
  release checklist passes.

## X announcement

### Timing

Publish Monday, August 17 at approximately **4:00 PM ET**. The original noon
window passed, so publish once rather than postponing the announcement or
adding a separate teaser.

### Copy

```text
Episode 3 is out.

We take the tensor we've been building in C++ and use it to compute a complete linear prediction:

prediction = weights.dot(features) + bias

The whole thing is built from smaller tensor operations, using C++23 and only the standard library.

https://www.youtube.com/watch?v=R_NZJ_rcX7E
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

- YouTube currently advertises Episode 3 to X as a compact `player` card rather
  than the full-width `summary_large_image` card used by Episodes 1 and 2.
  Remove the compact preview in the composer and upload `thumbnail.png`
  directly so the announcement retains the established full-width visual
  treatment. Keep the direct YouTube URL in the post text.
- The uploaded image itself will not function as an embedded YouTube player;
  the visible YouTube URL remains the clickable destination.
- Remain available for technical replies during the first hour.
- Do not publish another link-only reminder on launch day.
- A later technical post should teach one idea from the episode rather than
  repeating the announcement copy.
- Continue the separate organic cadence of one or two genuine personal or
  process posts on most active days. Do not add the Episode 3 link to those
  posts merely because they occur during its release window.

## LinkedIn announcement

### Timing

Publish Tuesday, August 18 between **9:00 and 10:30 AM ET**. This gives the X
announcement its own launch-day window while reaching the professional network
before Episode 4's Wednesday target.

The public Episode 3 URL is:

```text
https://www.youtube.com/watch?v=R_NZJ_rcX7E
```

### Copy

```text
A tensor becomes useful when it can participate in larger computations without exposing or corrupting its representation.

Episode 3 of Deep Learning, All the Way Down teaches our C++ tensor to compute.

We implement:

• equal-shape addition, subtraction, and multiplication
• reusable elementwise traversal
• reductions that return scalar tensors
• dot product through operation composition
• a complete linear prediction from weights, features, and bias

The implementation remains deliberately small: one C++23 file using only the standard library, assertions, and exceptions. That keeps the contracts, allocations, and tradeoffs visible before more powerful abstractions arrive.

Watch Episode 3:
https://www.youtube.com/watch?v=R_NZJ_rcX7E

Source code:
https://github.com/mechanical-turk/deep-learning-all-the-way-down

I would especially value feedback on the balance between mathematical explanation and implementation detail.
```

### LinkedIn strategy

- Link directly to YouTube, not through the X announcement.
- Use clean paragraphs and preserve the compact bullet list.
- Respond substantively to technical questions.
- Do not mention early view counts or ask for generic engagement.

## Reddit decision

Do **not** create a standalone Episode 3 Reddit submission.

The planned Reddit action is a single series-level contribution to the current
r/cpp August Show and Tell thread on Thursday, August 20. Lead with the project,
repository, technical purpose, and a specific request for C++ feedback. Include
the playlist secondarily. Posting each episode separately would become
repetitive and would treat Reddit as an announcement feed.

### r/cpp draft

```text
I'm building Deep Learning, All the Way Down, a free video and code series where I reconstruct deep-learning foundations in C++23 from first principles.

The implementation starts with only the standard library so the representation, correctness rules, allocations, and API decisions remain visible. The first three episodes build a checked tensor, establish scalar and empty-tensor semantics, add mutation and reductions, then implement elementwise arithmetic, dot product, and a forward linear prediction.

Source:
https://github.com/mechanical-turk/deep-learning-all-the-way-down

Playlist:
https://www.youtube.com/playlist?list=PLZSg76FHvdTw

I'd particularly value feedback from experienced C++ developers on the API contracts and on which production concerns should be introduced before the implementation grows more sophisticated.
```

Before posting, reread the live thread rules and revise the draft if the project
state has changed.

## Native YouTube Short

### Publication target

Friday, August 21 around **12:00 PM ET**. Record this as a separate vertical
lesson rather than extracting it from the 16:9 episode.

### Concept

**Why does a dot product return one number?**

### Short outline

```text
Hook:
You multiply two vectors element by element. Why does the dot product return
one number instead of another vector?

Demonstration:
[0.5, -1, 2] * [4, 3, 2]
= [2, -3, 4]

Then reduce:
2 - 3 + 4 = 3

Conclusion:
Elementwise multiplication produces the contributions. Summation reduces those
contributions to one scalar. Together, those two operations are the dot product.
```

### Short production requirements

- Record natively in 9:16.
- Keep the vectors and products large enough for a phone screen.
- Aim for approximately 30-45 seconds.
- Do not begin with the long-form series introduction.
- End after resolving the question; use no generic subscription appeal.
- In YouTube Studio, attach Episode 3 as the related video after the Short is
  uploaded.

## Exact release checklist

### Saturday night: active edit

- [ ] Complete the rough cut.
- [ ] Mark missing explanations, incorrect statements, dead air, and pickups.
- [ ] Confirm that the final computation produces `prediction: 3.5`.

### Sunday: finish and package

- [ ] Complete the fine cut and audio pass.
- [ ] Export the final master.
- [ ] Watch the exported file from beginning to end without editing.
- [ ] Check code legibility at ordinary YouTube playback size.
- [ ] Check for clipped audio, abrupt edits, frozen frames, and cursor mistakes.
- [x] Decide explicitly to omit manual chapters from the initial release.
- [ ] Upload the video as private or unlisted.
- [ ] Add the final title, description, thumbnail, tags, playlist, captions,
      cards if used, and end screen.
- [ ] Wait for HD processing and YouTube's checks to complete.
- [ ] Verify playback on desktop and mobile.
- [ ] Replace every `[EPISODE_3_URL]` placeholder in this file after YouTube
      assigns the URL.
- [ ] Schedule Monday publication only if every required check passes.

### Monday launch

- [ ] At 10:30 AM, capture Episode 2's approximately 48-hour analytics.
- [ ] At 10:45 AM, verify Episode 3 is still scheduled for 11:00 AM and that
      thumbnail, description, captions, playlist, and end screen are
      present.
- [ ] At 11:00 AM, confirm that Episode 3 is publicly playable.
- [x] Add the pinned comment. Posted via API (comment ID UgznctrafQ6j5khouIJ4AaABAg, 2026-08-18); still needs manual pinning in Studio (API cannot pin).
- [ ] Test every public link in the description and pinned comment.
- [ ] Record the publication time and URL in `docs/distribution-timeline.md`.
- [ ] At approximately 12:00 PM, publish the X announcement.
- [ ] Add the playlist and GitHub navigation reply.
- [ ] Record the X URL and exact time in the distribution ledger.
- [ ] Respond to substantive comments; do not publish another launch post.

### Tuesday and later

- [ ] Tuesday morning: publish the LinkedIn announcement and record its URL.
- [ ] Capture Episode 3 analytics at approximately 24 hours, 48 hours, and
      seven days after publication.
- [ ] Thursday: make the planned series-level r/cpp contribution if it remains
      appropriate under the live thread rules.
- [ ] Friday: publish the separately recorded Episode 3 Short and attach
      Episode 3 as its related video.

## Analytics snapshots

At approximately 24 hours, 48 hours, and seven days, record:

- Views
- Unique viewers when available
- Watch time
- Average view duration
- Audience-retention curve when available
- Impressions
- Impressions click-through rate
- Subscribers gained
- Traffic-source distribution
- Views and watch time attributable to external sources when available

Annotate which distribution events occurred between snapshots. Treat changes as
associations to investigate, not proof that a particular post caused them.
