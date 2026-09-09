# Short 4 Publishing Package

## Release plan

- **YouTube:** published Tuesday, August 25 at **7:27:57 PM ET**:
  https://www.youtube.com/watch?v=HGOsqhAcd3o
- **First comment:** published at approximately 7:31 PM ET:
  https://www.youtube.com/watch?v=HGOsqhAcd3o&lc=UgwDatF2FLaIlipVUCx4AaABAg
- **Instagram and TikTok:** published natively.
- **X:** native upload and navigation reply remain outstanding.
- **X:** publish the native video approximately one hour after YouTube, then
  add the navigation reply below.
- Do not create a LinkedIn post for this Short. Episode 6 already owns the next
  LinkedIn announcement obligation.
- Do not submit this Short to Reddit or Hacker News.

This is a schedule recovery, not a cadence change. The next Short returns to
the standing Friday slot.

## Release gate

- Final master: `~/Movies/CapCut/shorts ep 04.mp4`
- Verified dimensions: `2160 x 3840`
- Verified duration: `31.95 seconds`
- Video: H.264, 30 fps
- Audio: AAC stereo, 44.1 kHz
- Watch the complete exported file once with headphones.
- Confirm the opening question is legible before any platform UI appears.
- Confirm captions do not obscure the benchmark result.
- Confirm the result shown on screen agrees with the spoken numbers.
- Confirm the Instagram cover crop before publishing.

## YouTube

## Final title

```text
Big O Matters So Much Less Than You Think
```

## YouTube description

```text
These two loops have the same Big O complexity. They visit the same 16 million integers and perform the same number of additions, but their memory access patterns are completely different.

The matrix is stored row by row in one flat vector. Rows first reads neighboring integers. Columns first jumps 4,096 integers on every step.

Big O describes how the work grows. It does not describe how that work interacts with the hardware.

Complete series:
https://www.youtube.com/playlist?list=PLZSg76FHvdTw
```

### Thumbnail

Use [`thumbnail.png`](thumbnail.png). It is `2160 x 3840` and matches the
vertical master.

## Pinned comment

Post immediately after publication. Do not include a GitHub link.

```text
The exact ratio will change with the processor, compiler, matrix size, element type, and machine load.

The important comparison is the access pattern: one loop walks through adjacent values, while the other repeatedly jumps across the allocation.

Complete series:
https://www.youtube.com/playlist?list=PLZSg76FHvdTw
```

After posting it, remind the learner once to pin it and provide the direct
comment URL. Do not check pin status later.

## Suggested tags

```text
C++, C++ performance, cache locality, memory locality, cache lines, matrix
traversal, row major order, row major matrix, Big O notation, algorithmic
complexity, benchmarking, Google Benchmark, systems programming, computer
architecture, performance engineering
```

## Tag research record

- **Research date:** August 27, 2026
- **Evidence inspected:** current owned-channel YouTube Analytics and the live
  Short 4 release state. YouTube has not processed a usable Short 4 search-term
  or traffic-source sample yet, so no discovery claim can be supported.
- **Visible YouTube hashtags retained:** none. The unresearched `#cpp`,
  `#cppperformance`, and `#cachelocality` block was removed from the live
  description rather than replaced by another intuitive guess.
- **Backend metadata status:** the existing tag set predates the research rule
  and remains a legacy descriptor set, not a validated discovery strategy. Do
  not reuse or revise it without current platform research.

### Settings

- Visibility: public at the release time above.
- Audience: not made for children.
- Language: English.
- Comments: enabled.
- Embedding: enabled.
- Add to `Deep Learning, All the Way Down | Shorts`.
- Do not add to the long-form playlist.
- Set Episode 1 as the related video because it introduces flat row-major
  tensor storage.
- Upload `thumbnail.png` as the custom YouTube Shorts thumbnail.
- Review automatic captions for `Big O`, `n squared`, `4,096`, `cache`, and
  `row by row`.
- Do not add `#shorts` to the title, description, or tags.

## Instagram Reel

### Timing

Publish natively 15 to 30 minutes after the YouTube Short. Do not paste an
external URL into the caption or first comment.

### Caption

```text
Both loops visit the same 16 million integers and perform the same number of additions.

The difference is memory order. Rows first reads neighboring values. Columns first jumps 4,096 integers on every step.

Same Big O. Very different work for the hardware.

#cpp #cppperformance #cachelocality #performanceengineering #systemsprogramming
```

### First comment

```text
The ratio is machine-dependent. The memory-access pattern is the lesson.

Rows first follows the flat vector's storage order. Columns first keeps jumping across it.
```

### Settings

- Upload the original `2160 x 3840` master natively.
- Use [`cover-instagram-reel-v2.png`](cover-instagram-reel-v2.png) as the Reel
  cover. It is `1080 x 1682`, with all essential content inside the conservative
  centered `1080 x 1080` safe area.
- Share to Feed: on.
- Comments: enabled.
- Remix and use of original audio: on.
- Confirm the cover inside Instagram's profile-grid crop before publishing.
- Keep essential text away from the right-side controls and bottom caption UI.
- Profile link remains the complete YouTube series.

### Alt text

```text
A vertical C++ lesson comparing row-first and column-first traversal of the same flat row-major matrix, followed by benchmark results showing the effect of memory access order.
```

## TikTok

### Publication

Published on August 26, 2026 at 5:46:23 PM ET:

https://www.tiktok.com/@mechaturka/video/7678459926871575838

### Timing

Publish natively after Instagram in the same evening rollout.

### Caption

```text
C++ matrix traversal can have the same Big O complexity and very different runtime performance.

With row-major storage, scanning rows reads adjacent values. Scanning columns jumps across the allocation and has much poorer cache locality.

#cpp #cppperformance #cachelocality #computerarchitecture #performanceengineering
```

### Settings

- Upload the original `2160 x 3840` master natively.
- Original audio: on.
- Comments: enabled.
- Duet and Stitch: enabled.
- Select a cover frame where the comparison remains readable in the profile
  grid.
- Confirm that TikTok's right-side controls do not cover either result.

### Post-upload audit

- Public and indexable on `@mechaturka`.
- Live transcode: `720 x 1280`, H.264, 30 fps, with AAC stereo audio.
- Runtime: 32.34 seconds.
- Original sound is present and attributed to `mechaturka`.
- Comments are enabled; no warning or restriction is reported.
- The result table and comparison remain outside the critical right-side control
  rail. Some nonessential code reaches that rail.
- The selected cover is readable and contains the intended `41x THE TIME`
  result hook.
- The live body copy matches the intended topic, but the uploaded hashtag set
  differs from this package. TikTok received `#cpp #coding #programming
  #computerscience #software #softwareengineering` rather than the five
  technical hashtags above.
- Initial public checkpoint at 6:01 PM ET: 64 views, four likes, zero comments,
  zero shares, and zero saves.

## X

### Timing

Publish the video natively approximately one hour after YouTube. Do not place
an external link in the main post.

### Main post

```text
C++ performance changed by 41x due to cache locality, despite identical Big O. Both loops did 16 million additions on the same row-major matrix. On my machine: rows 1.7 ms, columns 71.1 ms. Big O matters, but software runs on hardware after all.
```

### X keyword research record

- **Research date:** August 27, 2026.
- **Tools and evidence:** Current web search, recent C++ performance material,
  and university material on cache-aware matrix traversal. Live X search and
  autocomplete were unavailable, and the default analytics refresh deliberately
  excluded tweet-level metadata, so no X query-volume claim is made.
- **Candidate phrases:** `C++ performance`, `cache locality`, `memory access
  pattern`, `row-major matrix`, `row-major traversal`, `cache misses`, and `Big
  O`.
- **Observed language:** Current technical sources consistently use `cache
  locality` for the mechanism and `row-major` for contiguous matrix traversal.
  `C++ performance` accurately supplies the broader discipline. `Big O` names
  the conceptual contrast already fulfilled by the video.
- **Retained phrases:** `C++ performance`, `cache locality`, `Big O`, and
  `row-major matrix`. They cover the discipline, mechanism, conceptual contrast,
  and concrete data layout without repeating synonyms.
- **Hashtags retained:** None. The research supports natural-language subject
  terms but provides no evidence that an X hashtag would improve qualified
  discovery for this post.
- **Sources:** UCL Research Computing,
  https://github-pages.ucl.ac.uk/research-computing-with-cpp/07performance/sec02Memory.html;
  Cornell CS 3410,
  https://www.cs.cornell.edu/courses/cs3410/2024fa/assignments/cacheblock/instructions.html;
  CppLearn's July 2026 cache-locality explanation,
  https://cpplearn.com/article/cache-locality.

### Navigation reply

Keep the YouTube URL first so its preview wins over GitHub.

```text
Deep Learning, All the Way Down:
https://www.youtube.com/playlist?list=PLZSg76FHvdTw

Source code:
https://github.com/mechanical-turk/deep-learning-all-the-way-down
```

## Post-publication checks

### One hour

- Verify playback, captions, cover, comments, playlist membership, and related
  video.
- Record public views and obvious distribution or rendering problems.

### 24 hours

- YouTube: views, engaged views, stayed to watch, average view duration,
  average percentage viewed, likes, comments, and subscribers.
- Instagram: views, reach, average watch time, interactions, shares, saves, and
  followers.
- TikTok: views, average watch time, completion, interactions, shares, saves,
  and followers.
- X: pull post-level analytics only when explicitly requested.

The main experiment is the first-second question hook. Compare stayed-to-watch
against Short 3 before interpreting completion among viewers who stayed.

### 72 hours

Repeat the same checkpoint and compare Short 4 with Shorts 2 and 3. Keep the
opening question as the tested variable; do not infer a universal posting-time
rule from this delayed Tuesday release.

## Source assets

- Script: [`script.md`](script.md)
- Opening visual: [`assets/opening-question.png`](assets/opening-question.png)
- Result visual: [`assets/hook-comparison.png`](assets/hook-comparison.png)
- Thumbnail: [`thumbnail.png`](thumbnail.png)
- Master: `~/Movies/CapCut/shorts ep 04.mp4`
