# Episode 5 Publishing Package

## Release status

- **Final master:** `~/Movies/CapCut/Deep Learning All The Way Down Ep 05.mov`
- **Verified media:** 1920x1080, 30 fps, H.264 video, stereo AAC audio,
  27:05 runtime
- **End-screen tail check:** current export keeps the retrieval questions on
  screen through the final seconds. Add approximately five seconds of clean
  question-free video and re-export before publication.
- **Thumbnail:** [`thumbnail.png`](thumbnail.png), verified at 1280x720
- **YouTube publication:** Friday, August 21, 2026, as soon as the private
  upload finishes HD processing and passes the playback checks below
- **X announcement:** 45-75 minutes after the actual YouTube publication time
- **LinkedIn announcement:** Saturday, August 22 between 9:00 and 10:30 AM ET
- **Short 3:** do not publish its remaining YouTube and Instagram versions in
  the same launch window; reschedule them after Episode 5 has room to breathe

This is a deliberate Friday exception. It does not change the standing
Monday-Wednesday-Saturday cadence.

## Final title

```text
Implementing Tensor Broadcasting in C++ | Deep Learning, All the Way Down #5
```

This is 76 characters and fits YouTube's 100-character title limit while
preserving the technical search term, series name, and episode number.

## YouTube description

```text
One bias should be reusable across an entire batch without first being copied into a larger tensor.

In Episode 5 of Deep Learning, All the Way Down, we implement general tensor broadcasting in C++.

We align shapes from the right, allow size-one axes to stretch, and assign a stride of zero wherever an operand needs to reuse the same value. That removes the manual bias-copy workaround from Episode 4 and also supports operations such as subtracting one per-feature offset from every observation in a batch.

Along the way, we cover:

• the shape-compatibility rule behind broadcasting
• row-major strides for N-dimensional tensors
• why broadcast axes use a stride of zero
• converting output coordinates into operand indices
• walking every coordinate in an N-dimensional output
• sharing one broadcasting implementation across addition, subtraction, and multiplication

The complete implementation remains in one C++23 file and uses only the standard library, assertions, and exceptions.

Source code:
https://github.com/mechanical-turk/deep-learning-all-the-way-down

Complete series:
https://www.youtube.com/playlist?list=PLZSg76FHvdTw

#cpp #deeplearning #machinelearning
```

## Thumbnail

Upload [`thumbnail.png`](thumbnail.png).

The visual promise is one scalar being reused across every element of the
right-hand tensor without an expanded copy. The arrows run from that scalar
to all three elements it participates in. The arithmetic is correct:

```text
       [2.5]     [3.0]
0.5 + [-1.0] =  [-0.5]
       [3.0]     [3.5]
```

## Suggested tags

```text
C++, C++23, modern C++, tensors, broadcasting, tensor broadcasting, numpy broadcasting, tensor shapes, strides, stride zero, multidimensional arrays, deep learning from scratch, machine learning from scratch, numerical computing, deep learning systems, PyTorch internals, systems programming, row-major storage
```

## Chapter timestamps

Manual chapters are omitted from the initial release. Add them only after the
final recording has been transcribed and the timestamps can be verified.

## Pinned comment

Post this immediately after the video becomes public, then pin it in YouTube
Studio:

```text
Answers to the questions at the end:

1. The flat index is the sum of coordinate[axis] * stride[axis] across every axis. If an effective stride is zero, that axis always contributes zero to the index, regardless of its coordinate. Every position along that output axis therefore reads the same underlying value.

2. A scalar is already handled by the general rule. It has no axes, so every output axis is treated as a missing size-one axis with an effective stride of zero. Keeping the copied scalar path would duplicate behavior without providing a different result.

3. A shape [3] must align with the final axis of [2,3], because both describe the feature dimension. Padding on the right would compare 3 against the leading size 2 instead, rejecting a valid operation or aligning values along the wrong axis.

Source code:
https://github.com/mechanical-turk/deep-learning-all-the-way-down

Complete playlist:
https://www.youtube.com/playlist?list=PLZSg76FHvdTw
```

These answers correspond exactly to the three questions at the end of
[`script.md`](script.md).

## YouTube upload settings

- Visibility during upload: **Private**
- Playlist: **Deep Learning, All the Way Down | From First Principles in C++**
- Category: **Education**
- Language: **English**
- Audience: **No, it is not made for kids**
- Comments: **On**
- Embedding: **On**
- Thumbnail: [`thumbnail.png`](thumbnail.png)
- End screen: **Subscribe** element plus the **complete series playlist**
- Captions: review the automatic English captions, especially
  `broadcast_shape`, `effective_strides`, `stride_offset`, `size_t`, and
  `row-major`

Do not make the video public until:

- [ ] Re-export with an approximately five-second clean end-screen tail after
      the retrieval questions.
- [ ] HD processing is complete.
- [ ] YouTube reports no copyright or processing restriction.
- [ ] The opening, a middle coding section, and the ending play correctly.
- [ ] Audio is present and synchronized.
- [ ] Code is legible at ordinary desktop and mobile playback size.
- [ ] The final question finishes before an approximately five-second clean
      end-screen tail; no question text is covered by YouTube UI.
- [ ] The title, description, thumbnail, tags, playlist, audience setting, and
      comments have been rechecked on the uploaded video.
- [ ] The end screen contains both Subscribe and the complete series playlist,
      positioned only over the dedicated tail.

Once those checks pass, publish immediately rather than waiting for another
arbitrary clock time. Record the actual public URL and timestamp in
`docs/distribution-timeline.md`.

## X announcement

### Timing

Publish at approximately **12:15 PM ET on Friday, August 21**, about one hour
after the video became publicly playable.

### Main post

```text
episode 5 is out.

our C++ tensor used to reject this:

[2, 3] + [3]

now it broadcasts the smaller tensor across both rows, without copying it first.

everything underneath that operation is built from scratch with C++23 and the standard library.

https://www.youtube.com/watch?v=70mVVGNc0Ik
```

### Navigation reply

```text
Complete playlist:
https://www.youtube.com/playlist?list=PLZSg76FHvdTw

Source code:
https://github.com/mechanical-turk/deep-learning-all-the-way-down
```

### X checks

- Inspect the video's live `twitter:card` metadata before posting.
- If YouTube serves the compact `player` card, remove that preview and attach
  [`thumbnail.png`](thumbnail.png) directly while retaining the visible video
  URL.
- Publish the navigation reply immediately afterward.
- Remain available for substantive replies during the first hour.

## LinkedIn announcement

### Timing

Publish Saturday, August 22 between 9:00 and 10:30 AM ET.

### Copy

```text
Adding one bias to every row of a batch should not require copying that bias into a larger tensor first.

In Episode 5, we implement tensor broadcasting from scratch in C++.

To make that work, we align the operand shapes from the right, decide whether their dimensions are compatible, and compute how each operand should move while we traverse the output.

If an operand needs to reuse the same value along an axis, we give that axis a stride of zero. Its physical index stays in place as the output coordinate advances, so there is no need to allocate an expanded copy.

With that in place, the same elementwise implementation can broadcast addition, subtraction, and multiplication.

The code remains in one C++23 file using only the standard library.

Watch Episode 5:
https://www.youtube.com/watch?v=70mVVGNc0Ik

Source code:
https://github.com/mechanical-turk/deep-learning-all-the-way-down
```

## Reddit decision

Do not create a standalone Episode 5 Reddit submission. The pending Reddit
work remains a series-level r/cpp Show and Tell contribution centered on the
code and the learning project rather than an episode announcement.

## Native Short plan

Do not extract a Short from this recording. Script a separate native Short
around one of these ideas:

1. Why a broadcast axis has stride zero.
2. Why `[3]` aligns with `[2,3]` from the right.

Publish it in a later Short slot, independently of this launch.

## Immediate launch sequence

1. Upload the final master as private.
2. Apply the title, description, tags, thumbnail, playlist, language, category,
   audience setting, comments, and embedding settings above.
3. Wait for HD processing and run the playback checks.
4. Add reviewed captions and place Subscribe plus the complete series playlist
   over only the final five-second tail.
5. Make the video public.
6. Replace every episode URL placeholder in this file with the public URL.
7. Post the first comment above through the channel tooling and report its
   direct comment URL; pinning remains a manual Studio action.
8. Record the publication in `docs/distribution-timeline.md`.
9. Publish the X announcement 45-75 minutes later, followed immediately by
   its navigation reply.
10. Publish the LinkedIn announcement Saturday morning.

## Analytics checkpoints

Capture Episode 5 at approximately:

- **24 hours:** reach, consumption, engagement, subscribers, traffic sources,
  and the opening retention curve when processed
- **72 hours:** the same metrics, compared with Episodes 3 and 4 at equivalent
  ages
- **Seven days:** stable cross-episode comparison

Record every distribution event occurring between snapshots. Treat resulting
changes as associations to investigate rather than proof of causation.
