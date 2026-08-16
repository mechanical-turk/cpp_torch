# Episode 2 Publishing Package

## Recommended title

Completing Our Tensor in C++: Scalars, Mutations & Reductions | Deep Learning, All the Way Down #2

## Description

In Episode 2 of *Deep Learning, All the Way Down*, we complete the foundational
tensor data structure we began in Episode 1.

We give scalar and empty tensors precise semantics, make shape and indexing
arithmetic overflow-safe, add checked mutation without exposing the underlying
storage, and implement `sum()` as our first reduction.

Along the way, we examine several C++ ideas that matter when numerical code must
remain correct at its boundaries:

- The difference between shape `[]`, `[1]`, and `[0]`
- Why a zero-dimensional tensor contains one scalar value
- How unsigned integer overflow can violate representation invariants
- Const and mutable member-function overloads
- Returning references without surrendering ownership of storage
- Why the sum of an empty tensor is zero

The entire implementation remains in one C++23 file, using only the standard
library, ordinary assertions, and exceptions.

Source code:
https://github.com/mechanical-turk/deep-learning-all-the-way-down

Watch the complete series:
https://www.youtube.com/playlist?list=PLZSg76FHvdTw

#cpp #deeplearning #machinelearning

## Chapter timestamps

These are based on the script. Replace them with timestamps from the final edit
before publishing.

```text
00:00 Completing the tensor foundation
00:45 Questions from Episode 1
02:30 Scalars, singleton vectors, and empty tensors
08:30 Overflow-safe tensor arithmetic
16:00 Checked dimension queries
19:00 Safe element mutation
26:30 Our first reduction: sum
32:30 What we built
34:30 What comes next
```

## Pinned comment

```text
Thanks for watching!

Source code:
https://github.com/mechanical-turk/deep-learning-all-the-way-down

Watch the complete series:
https://www.youtube.com/playlist?list=PLZSg76FHvdTw
```

## X announcement

### Timing

Publish between **12:00 and 12:15 PM ET on launch day**, approximately one hour
after the YouTube release.

This delay gives the public video page time to settle while keeping the post
inside the launch window. Do not publish an earlier teaser or repeat the same
link several times that day.

### Copy

```text
Episode 2 of Deep Learning, All the Way Down is live.

We extend our C++ tensor with scalar and empty shapes, checked mutation, overflow-safe indexing, and our first reduction.

Built from first principles with C++23 and only the standard library.

https://www.youtube.com/watch?v=8kzL5NdxGCo
```

### Strategy

- Let the YouTube URL generate its native preview.
- If X fails to produce the preview, attach the episode thumbnail.
- Stay available to answer substantive replies.
- Do not coordinate likes or ask friends for generic engagement.
- Judge the post by qualified conversations and video watch time, not raw
  impressions alone.

### Series navigation reply

Immediately reply beneath the Episode 2 announcement with:

```text
Complete playlist:
https://www.youtube.com/playlist?list=PLZSg76FHvdTw

Source code:
https://github.com/mechanical-turk/deep-learning-all-the-way-down
```

Use the same reply beneath the Episode 1 announcement and every future episode
announcement. The main tweet points to the specific episode; this reply provides
the durable series and source-code destinations.

## LinkedIn announcement

### Timing

Publish **Monday between 9:00 and 10:30 AM ET**, two days after the Saturday
release. This staggers distribution and places the professional-network post in
a weekday window.

### Copy

```text
Deep learning frameworks make sophisticated systems remarkably easy to build. I am working backward through those abstractions to understand the machinery underneath.

Episode 2 of Deep Learning, All the Way Down extends our tensor implementation in modern C++.

We cover:

• scalar and empty tensor semantics
• overflow-safe shape and indexing arithmetic
• checked mutation without exposing storage
• sum as our first tensor reduction

The implementation remains deliberately small: one C++23 file, the standard library, ordinary assertions, and exceptions. The goal is to make every representation and correctness decision visible before introducing more powerful abstractions.

Watch Episode 2:
https://www.youtube.com/watch?v=8kzL5NdxGCo

Source code:
https://github.com/mechanical-turk/deep-learning-all-the-way-down

I would especially value feedback on the technical depth and pacing.
```

### Strategy

- Use the YouTube link directly rather than linking through X.
- Do not post it on the same day as the X announcement.
- Respond to technical comments with substantive answers.
- Avoid asking for generic engagement or presenting early view counts as proof
  of success.

## Suggested tags

```text
C++, C++23, modern C++, tensors, tensor implementation, deep learning from
scratch, machine learning from scratch, deep learning systems, numerical
computing, scalar tensor, empty tensor, reductions, const correctness,
integer overflow, systems programming, PyTorch internals
```

## Thumbnail

Use [`thumbnail.png`](thumbnail.png).

The thumbnail text is intentionally shorter than the video title. The title
states the specific material; the thumbnail communicates the episode's broader
progression without repeating the same words.
