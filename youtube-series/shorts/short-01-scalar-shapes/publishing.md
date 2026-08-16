# Short 1 Publishing Package

## Release target

- **YouTube Short:** Sunday, August 16, 2026 at approximately 2:00 PM ET
- **Shorts playlist:** create when Short 1 becomes public
- **X post:** Sunday, August 16 at approximately 4:00 PM ET
- **LinkedIn:** no standalone post
- **Reddit:** no standalone submission

Publication remains provisional until the final export, captions, thumbnail,
audio, and mobile playback checks pass.

## Final title

```text
Tensor Shapes: [ ] Is Not [0]
```

## YouTube description

```text
Why does tensor shape [ ] contain one value, while shape [0] contains none?

Rank counts axes. Element count multiplies their sizes, starting from one. An empty shape has no dimensions to change that starting value, so it represents one scalar. Shape [0] has one axis of length zero, so it contains no values.

Watch the complete tensor lesson:
https://www.youtube.com/watch?v=8kzL5NdxGCo

Complete series:
https://www.youtube.com/playlist?list=PLZSg76FHvdTw

Source code:
https://github.com/mechanical-turk/deep-learning-all-the-way-down

#cpp #deeplearning #shorts
```

## Thumbnail

Upload [`thumbnail.png`](thumbnail.png) as the custom thumbnail.

The thumbnail is 1080x1920 and uses the established series branding:

```text
[] != [0]
1 VALUE
0 VALUES
C++
```

## Chapters

No chapter markers. The Short is approximately 41 seconds and teaches one
continuous idea.

## Pinned comment

```text
Full tensor lesson:
https://www.youtube.com/watch?v=8kzL5NdxGCo

Source code:
https://github.com/mechanical-turk/deep-learning-all-the-way-down
```

## Suggested tags

```text
C++, C++23, tensors, tensor shape, scalar tensor, rank zero tensor,
empty tensor, tensor rank, tensor element count, deep learning from scratch,
machine learning from scratch, deep learning systems, PyTorch internals,
numerical computing
```

## Upload settings

- Upload the final 1080x1920 vertical export.
- Confirm YouTube classifies it as a Short.
- Set the title and description exactly as written above.
- Set the language to English.
- Mark it as not made for children.
- Add it to the dedicated **Deep Learning, All the Way Down | Shorts** playlist.
- Do not add it to the long-form course playlist; preserve that playlist as the
  ordered episode sequence.
- Add Episode 2 as the **related video** in YouTube Studio.
- Upload `thumbnail.png` as the custom thumbnail.
- Review the automatic captions, especially `[]`, `[0]`, `rank`, `scalar`, and
  `C++`.
- Keep comments and embedding enabled.
- Publish it at approximately 2:00 PM ET on Sunday, August 16, or as soon
  afterward as final QA passes. Do not delay it merely to preserve the target
  minute.

## Final quality gate

- The opening contrast is understandable without prior context.
- The arrow begins on the scalar, moves to the empty vector, and disappears
  before the explanation.
- `[]`, `[1]`, and `[0]` remain readable on a phone at normal brightness.
- The narration does not repeat the same claim unnecessarily.
- The final distinction is explicit: no axes is not an axis of length zero.
- Captions do not cover the comparison labels or arrow target.
- Speech is clear and evenly leveled; there is no clipping or distracting room
  noise.
- The custom thumbnail displays correctly without unintended cropping.
- Episode 2 appears as the related-video link in the Shorts player.
- The Short appears in the dedicated Shorts playlist, not the long-form course
  playlist.

## Shorts playlist

Create this public playlist when Short 1 is published.

### Title

```text
Deep Learning, All the Way Down | Shorts
```

### Description

```text
Short, self-contained lessons on C++, tensors, autograd, machine learning systems, GPU programming, and deep learning from first principles.
```

Add every native Short to this playlist in publication order. Keep the main
**Deep Learning, All the Way Down** playlist reserved for full episodes. The
playlist organizes the Short library; the related-video link remains the
primary path from each Short to its corresponding long-form lesson.

## X post

### Timing

Publish at approximately **4:00 PM ET**, one hour after the Short. This gives
the YouTube release a clean initial window and avoids a simultaneous link dump.

Upload the final Short video directly to X rather than linking to the YouTube
Short.

### Copy

```text
A tensor with shape [] contains one value.

A tensor with shape [0] contains none.

The distinction comes down to axes, multiplication, and the identity value we start from when counting elements.
```

### Series navigation reply

Reply beneath the post with:

```text
Full tensor lesson:
https://www.youtube.com/watch?v=8kzL5NdxGCo

Complete series:
https://www.youtube.com/playlist?list=PLZSg76FHvdTw

Source code:
https://github.com/mechanical-turk/deep-learning-all-the-way-down
```

### X strategy

- Upload the video natively to X.
- Keep the post self-contained so the idea remains useful without the click.
- Put the full Episode 2, playlist, and source links in the navigation reply.
- Remain available for replies during the first hour.
- Do not publish a second announcement for this Short.
- Reuse the idea later only if the new post adds a different technical insight.

## LinkedIn decision

Do not create a standalone LinkedIn announcement for this Short. Episode 3's
LinkedIn post is already planned for Tuesday morning, and another promotional
post would add little. The Short can be mentioned later in a substantive roundup
or a post about tensor shape semantics.

## Reddit decision

Do not submit this Short to Reddit. The planned series-level r/cpp Show and Tell
contribution is the appropriate Reddit action. A standalone 41-second lesson
would add little context and risk making the account look like an announcement
feed.

## Post-publication checks

Record snapshots in `docs/distribution-timeline.md` at approximately:

- **1 hour:** views and obvious caption or playback problems;
- **24 hours:** views, likes, subscribers, average percentage viewed, viewed
  versus swiped away, and traffic sources;
- **7 days:** the same metrics for comparison with later Shorts.

Treat the first Short as a baseline, not a verdict. Do not change the series
strategy from one low-sample result.

## Source assets

- Recording script: [`script.md`](script.md)
- Thumbnail: [`thumbnail.png`](thumbnail.png)
- Comparison visual:
  [`assets/tensor-shape-comparison.png`](assets/tensor-shape-comparison.png)
- Attention arrow:
  [`../../assets/attention-arrow-southeast.png`](../../assets/attention-arrow-southeast.png)
