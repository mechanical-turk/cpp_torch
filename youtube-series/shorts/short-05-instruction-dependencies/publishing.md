# Short 5 Publishing Package

## Release plan

- **YouTube:** published Tuesday, September 1, 2026 at **7:15:06 PM ET**:
  https://www.youtube.com/watch?v=_f01HV9lzj8
- **First comment:** published shortly afterward:
  https://www.youtube.com/watch?v=_f01HV9lzj8&lc=Ugx09naGMien_KsSX4J4AaABAg
- **Instagram:** published Wednesday, September 2 at **8:26:42 AM ET** after
  the browser composer exposed no scheduling control:
  https://www.instagram.com/reel/DcyO3GYimT3/
- **TikTok:** published Thursday, September 3 at **8:34:30 AM ET**:
  https://www.tiktok.com/@mechaturka/video/7681286402046381342
- X native publication remains outstanding.
- Instagram was published first because it is currently the strongest proven
  native discovery surface. Use the gap before TikTok to verify the Reel and
  respond to early comments rather than releasing both at once.
- Do not create a standalone LinkedIn post for this Short.
- Do not submit this Short to Reddit or Hacker News. It is a compact performance
  lesson, not a new project milestone.
- Add Episode 4 as the YouTube related video because its matrix-multiplication
  kernel is the closest long-form application of an accumulator loop:
  https://www.youtube.com/watch?v=ZC6F284rRGo

This release used the standing Tuesday Short slot. Friday remains the next
standing Short slot rather than a required duplicate release.

## Release gate

- Uploaded filename: `cpp-accumulator-dependency-chain-performance.mp4`.
- Verified master: `2160 x 3840`, H.264, 30 fps, AAC stereo, Rec.709,
  19.77 seconds, `-16.7 LUFS` integrated loudness, `-3.0 dBFS` true peak.
- Verify the exported file with `ffprobe` and watch it from beginning to end
  with headphones.
- Confirm the opening challenge and `Inefficient loop?` are readable on the
  first frame before platform controls appear.
- Confirm every code line is readable on a phone-sized preview.
- Confirm the spoken and displayed results agree exactly:
  `5.826 s`, `4.212 s`, `3.619 s`, `1.38x`, and `1.61x`.
- Keep the benchmark footer visible long enough to inspect without making it
  compete with the main result.
- Confirm captions do not obscure the code, result table, benchmark footer, or
  final question.
- Listen for distracting pumping in the keyboard ducking. The taps should remain
  audible under narration without competing with the voice.
- Confirm the Instagram cover crop inside the live publishing preview.

## YouTube

## Final title

```text
Can One Extra Variable Make This C++ Loop Faster?
```

## YouTube description

```text
How much faster can you make a C++ loop with one extra accumulator?

In this controlled benchmark, one accumulator took 5.826 seconds. Splitting the same sum across two independent accumulators took 4.212 seconds. Four accumulators reached 3.619 seconds.

The build disables SIMD vectorization and loop unrolling, and each version performs the same four loads and four scalar additions per source-loop iteration. The exact result depends on the processor, compiler, and workload. The interesting change is the dependency graph: one running total makes additions wait on one another, while independent totals expose work the CPU may be able to overlap.

Watch the matrix-multiplication episode:
https://www.youtube.com/watch?v=ZC6F284rRGo

Complete series:
https://www.youtube.com/playlist?list=PLZSg76FHvdTw
```

## Thumbnail

- A custom YouTube thumbnail is present. Record its local source path when it is
  recovered.
- Lead with `ONE EXTRA VARIABLE` and the one-versus-two-accumulator contrast.
- Keep the wording and essential code inside the central safe area.
- Do not crowd the thumbnail with all three benchmark rows.

## Pinned comment

Post only after inspecting every existing channel-authored comment. Do not post
a duplicate.

```text
The controlled build uses:
-O3 -fno-vectorize -fno-slp-vectorize -fno-unroll-loops

Every version processes four inputs per source-loop iteration. That removes SIMD and different loop counts from the comparison; the changing structure is one, two, or four independent accumulator chains.

What do you expect to become the bottleneck as we keep adding accumulators?
```

After posting, remind the learner once to pin it and provide the direct comment
URL. Do not inspect pin status or repeat the reminder later.

## Suggested tags

```text
C++, cpp, C++ performance, instruction level parallelism, instruction dependency,
dependency chain, accumulator, CPU performance, scalar reduction, loop optimization,
compiler optimization, benchmarking, computer architecture
```

## Research record

- **Research date:** September 1, 2026.
- YouTube's official help says the title, thumbnail, and description matter more
  for discovery than tags, which are mainly useful for misspellings. The title
  therefore carries the natural challenge and `C++ loop`; `cpp` is retained as
  the useful naming variant:
  https://support.google.com/youtube/answer/146402?hl=en
- Official Clang documentation confirms the benchmark's vectorization and loop-
  unrolling controls. These flags belong in the first comment and methodological
  copy, not in the title:
  https://clang.llvm.org/docs/ClangCommandLineReference.html
  https://clang.llvm.org/docs/genindex.html
- Arm's processor documentation uses data dependencies to explain why some
  instructions must remain ordered while independent work may execute in
  parallel. `instruction dependency`, `dependency chain`, and `instruction
  level parallelism` are therefore accurate subject terms:
  https://developer.arm.com/community/arm-research/b/articles/posts/eliminating-memory-barriers-with-ede
- Visible YouTube hashtags retained: none. No current evidence supports adding
  a hashtag block to this description.

## YouTube settings

- Visibility: public since September 1, 2026 at 7:15:06 PM ET.
- Audience: not made for children.
- Language: English.
- Category: Science & Technology.
- Comments: enabled.
- Embedding: enabled.
- Add to `Deep Learning, All the Way Down | Shorts`.
- Do not add to the long-form playlist.
- Set Episode 4 as the related video in YouTube Studio.
- Upload `thumbnail-youtube-shorts.png` as the custom thumbnail.
- Review automatic captions for `accumulator`, `SIMD`, `loop unrolling`, the
  three runtimes, and both speedup ratios.
- Do not add chapters to a 20-to-25-second Short.

## Instagram Reel

### Timing

Published Wednesday, September 2 at 8:26:42 AM ET. The browser composer did not
offer scheduling, so the planned 11:30 AM slot was replaced by immediate manual
publication. Do not place an external URL in the caption or first comment.

### Caption

```text
One extra accumulator made this C++ loop faster.

1 accumulator: 5.826 s
2 accumulators: 4.212 s
4 accumulators: 3.619 s

SIMD vectorization and loop unrolling were disabled. Splitting one dependency chain across independent sums gave the CPU more work it could overlap. Exact results depend on the processor, compiler, and workload.

#cpp #coding #programming #cpu #softwareengineering
```

### Instagram keyword and hashtag research record

- **Research date:** September 2, 2026.
- **Sources checked:** owned Instagram Reel results for Shorts 2, 3, and 4;
  the exact code, narration, and benchmark results in this Short.
- **Owned-account evidence:** Short 4 reached 17,642 accounts and used `#cpp`,
  `#software`, `#cache`, `#cpu`, `#code`, and `#programming`. Shorts 2 and 3
  also used `#cpp`, `#coding`, `#programming`, and `#computerscience`. These
  results show that the terms occur in content Instagram has distributed for
  this account, but they do not prove that hashtags caused the reach.
- **Candidate search phrases:** `C++ loop`, `C++ performance`, `CPU
  performance`, `instruction dependency`, `independent accumulators`, and
  `compiler optimization`.
- **Primary phrase:** `C++ loop`.
- **Supporting terms:** `accumulator`, `dependency chain`, `CPU`, `SIMD
  vectorization`, and `loop unrolling`.
- **Hashtags retained:** `#cpp`, `#coding`, `#programming`, `#cpu`, and
  `#softwareengineering`. They match the subject and have prior owned-account
  use.
- **Hashtags rejected:** `#cppperformance`, `#computerarchitecture`,
  `#compileroptimization`, and `#benchmarking`. No current platform or
  owned-account evidence supports these compounds for this release.
- **Unavailable evidence:** live Instagram search volume and autocomplete were
  not available. No claim about hashtag volume or causation is made.

### First comment

```text
One accumulator makes each addition wait for the previous one. Splitting the sum across independent accumulators gives the processor more work it may overlap.

Where do you expect that benefit to stop?
```

Status: not yet posted as of the 8:30 AM ET API read-back. Instagram publishing
and comment operations remain manual with the current read-only integration.
At the 9:24 PM checkpoint, the Reel had 85 total comments, but the current sync
does not identify comment authors. The account-authored first-comment status is
therefore unknown until manually inspected.

### Cover

- Produce `cover-instagram-reel.png` at `1080 x 1682`.
- Use `ONE EXTRA VARIABLE` as the primary line and `FASTER?` as the payoff cue.
- Keep all essential content inside the conservative centered `1080 x 1080`
  profile-grid safe area.
- Verify the actual crop in Instagram before publishing; the local dimensions
  alone are not sufficient evidence.

### Settings

- Upload the original `2160 x 3840` master natively.
- Share to Feed: on.
- Comments: enabled.
- Remix and use of original audio: on.
- Keep essential code and results away from the right-side controls and bottom
  caption UI.
- Profile link remains the complete YouTube series.

### Alt text

```text
A vertical C++ performance lesson comparing one, two, and four running sums, with benchmark results showing faster execution as independent accumulator chains are introduced.
```

## TikTok

### Timing

Published Thursday, September 3 at 8:34:30 AM ET. Do not place an external URL
in the caption.

### Caption

```text
One extra accumulator made this C++ loop faster.

1 accumulator: 5.826 s
2 accumulators: 4.212 s
4 accumulators: 3.619 s

SIMD and loop unrolling were disabled. Independent sums shorten the instruction dependency chain and give the CPU more work it may execute in parallel. Exact results depend on the hardware and compiler.

#cpp #coding #programming #computerscience #softwareengineering
```

### TikTok keyword and hashtag research record

- **Research date:** September 2, 2026.
- **Sources checked:** owned TikTok results for Shorts 3 and 4; the exact code,
  narration, and benchmark results in this Short.
- **Owned-account evidence:** Short 4 received 4,010 views with `#cpp`,
  `#coding`, `#programming`, `#computerscience`, `#software`, and
  `#softwareengineering`. Short 3 received 1,155 views with the first four of
  those terms. These are observed terms from distributed posts, not proof that
  the hashtags caused distribution.
- **Candidate search phrases:** `C++ loop`, `C++ performance`, `CPU
  performance`, `instruction dependency`, `independent accumulators`, and
  `compiler optimization`.
- **Primary phrase:** `C++ loop`.
- **Supporting terms:** `accumulator`, `instruction dependency chain`, `CPU`,
  `SIMD`, and `loop unrolling`.
- **Hashtags retained:** `#cpp`, `#coding`, `#programming`,
  `#computerscience`, and `#softwareengineering`. They accurately describe the
  video and have prior owned-account use.
- **Hashtags rejected:** `#cppperformance`, `#computerarchitecture`,
  `#compiler`, and `#benchmarking`. Current owned-account evidence does not
  support them for this post.
- **Unavailable evidence:** live TikTok search volume and autocomplete were not
  available. No claim about hashtag volume or causation is made.

### Settings

- Upload the original `2160 x 3840` master natively.
- Original audio: on.
- Comments: enabled.
- Duet and Stitch: enabled.
- Select the opening challenge as the cover frame.
- Confirm the code, result table, and final question remain outside TikTok's
  right-side controls and bottom caption UI.

## X

### Timing

Publish the video natively approximately one hour after YouTube. Do not place
an external link in the main post.

### Main post

```text
How much faster can one extra variable make a C++ loop?

On my M1 Pro:
1 accumulator: 5.826 s
2 accumulators: 4.212 s
4 accumulators: 3.619 s

Same four loads and scalar additions per source-loop iteration. SIMD and loop unrolling disabled.

The dependency graph changed. What is the CPU doing differently?
```

### X keyword research record

- **Research date:** September 1, 2026.
- **Retained natural-language terms:** `C++ loop`, `accumulator`, `SIMD`, `loop
  unrolling`, and `dependency graph`. They describe what viewers see and the
  controls used without forcing specialist terminology into the hook.
- **Hashtags retained:** none. The native video and challenge carry the post;
  no current evidence supports sacrificing space to hashtags.
- **Evidence:** the same official Clang and Arm sources recorded in the YouTube
  research section. No X query-volume claim is made.

### Navigation reply

Keep the YouTube URL first so its preview wins. The GitHub link below is the
public tensor and autograd series repository; it is not a claim that the Short's
standalone benchmark lives there.

```text
Deep Learning, All the Way Down:
https://www.youtube.com/playlist?list=PLZSg76FHvdTw

Public series source:
https://github.com/mechanical-turk/deep-learning-all-the-way-down
```

## Post-publication checks

Run the automatic platform audit immediately after each native publication.
Use the live post as the authority for playback, audio, crop, caption, cover,
comments, and restrictions.

### Initial YouTube audit

- Public URL, title, corrected description, tags, category, English language,
  comments, embedding, audience setting, custom thumbnail, and processed upload
  status passed API read-back.
- The Short is in `Deep Learning, All the Way Down | Shorts`.
- The live description was corrected immediately after publication to match the
  recorded `5.826`, `4.212`, and `3.619` second results.
- An accidental line break in the `instruction dependency` tag was corrected.
- The first comment is present. A one-time pin reminder was delivered.
- Automatic captions are not serving yet and require a later read-back.
- Public `2160p` playback and Episode 4 related-video assignment remain manual
  verification items because authenticated Studio browser control was
  unavailable during the audit.

Authenticated Studio follow-up on September 2 confirmed that English source
subtitles are now available and Episode 4 is assigned as the related video.
The September 4 Studio audit confirmed that 4K processing is complete.

### September 4 cross-platform checkpoint

- Instagram: 156,478 plays, 90,998 accounts reached, 18.35 seconds average watch
  time, and 1,775 interactions. The account reached 154 followers.
- TikTok: the latest Phyllo index reports 796 views, 21 likes, one comment, and
  one share. The account reached eight followers. Treat this as the latest
  indexed reading rather than a guaranteed live count.
- YouTube: 152 public views, four likes, and one comment. Its small processed
  Analytics row remains insufficient for a final distribution diagnosis.

### Instagram breakout checkpoint

- Published September 2 at 8:26:42 AM ET:
  https://www.instagram.com/reel/DcyO3GYimT3/
- At 9:24 PM ET, approximately 13 hours after publication: 104,182 plays,
  62,114 reach, 17.57 seconds average watch time, 1,099 interactions, 600 likes,
  85 comments, 275 saves, and 134 shares.
- Instagram followers rose from 42 before publication to 114. Treat this as an
  account-level change because the API does not attribute every follow to the
  Reel.
- The live caption matches the approved Instagram copy.
- Authenticated Chrome inspection confirmed that the Reel plays normally, the
  audio control is present, the approved caption is live, and the profile-grid
  crop keeps the code and hook readable.
- The account-authored first comment is present and matches the content. At the
  browser check it had 19 likes.
- Report:
  `youtube-series/analytics/reports/2026-09-02-short-05-instagram-breakout.md`.
- Frame-by-frame retention and creative analysis:
  `youtube-series/analytics/reports/2026-09-02-short-05-instagram-retention-and-creative-analysis.md`.

### YouTube 24-hour checkpoint

- At one day and two hours, Studio showed 116 views, 46 engaged views, 75.4%
  stayed to watch, 30 seconds overall average view duration, and 153.4% average
  percentage viewed on the channel dashboard.
- YouTube Search supplied 54.3% of views and the Shorts feed supplied only
  25.0%. Studio estimated 13 unique viewers and no subscriber change.
- The audience-retention card separately showed 38 seconds average view
  duration and 67.9% stayed to watch. These cards are still processing and use
  different scopes, so do not collapse them into one value.
- Viewers who stayed replayed the Short heavily, but YouTube still supplied a
  very small cold-feed test. This strengthens the distribution and
  audience-matching diagnosis rather than a creative-rejection diagnosis.

### One hour

- YouTube: verify public playback, audio, captions, thumbnail, Shorts playlist,
  comments, and Episode 4 related-video assignment.
- Instagram: inspect the live Reel and profile-grid tile; verify audio, caption,
  hashtags, comments, and the actual cover crop.
- TikTok: verify playback, original audio, caption, cover, comments, and UI-safe
  placement.
- X: verify the native video and navigation reply are public and render
  correctly.
- Record exact publication times, public URLs, and any corrective action in the
  distribution timeline.

### 24 hours

- YouTube: views, engaged views, stayed to watch, average view duration,
  average percentage viewed, likes, comments, and subscribers.
- Instagram: views, reach, average watch time, interactions, shares, saves,
  profile visits, and followers.
- TikTok: views, average watch time, completion, interactions, shares, saves,
  profile views, and followers.
- X: pull post-level analytics only when explicitly requested.

The main experiment is the genuine adjacent technical question at the end.
The lesson resolves first; then the final line invites viewers to think about
what the CPU is doing differently. Compare profile intent and substantive
comments with Short 4 while treating topic, runtime, and reach as confounds.

### 72 hours and seven days

- Repeat the cross-platform checkpoint using matched publication ages.
- Compare opening conversion and consumption separately from profile intent and
  comments.
- Do not attribute a result solely to the ending when the topic, opening, and
  runtime also differ.
- Decide whether this open-door ending should be retained for the next Short.

## Source assets

- Script: [`script.md`](script.md)
- Owned automatic captions: [`captions/en.vtt`](captions/en.vtt)
- One-accumulator scene:
  `/Users/keremkazan/code/short-05-instruction-dependencies/scenes/scene_1.cpp`
- Two-accumulator scene:
  `/Users/keremkazan/code/short-05-instruction-dependencies/scenes/scene_2.cpp`
- Controlled benchmark:
  `/Users/keremkazan/code/short-05-instruction-dependencies/benchmark.cpp`
- YouTube thumbnail: custom thumbnail present; local source path not recorded
- Instagram cover: `cover-instagram-reel.png` (not yet produced)
- Final master:
  `/Users/keremkazan/Movies/CapCut/shorts/ep05/cpp-accumulator-dependency-chain-performance.mp4`
- Verified master: `2160 x 3840`, H.264, 30 fps, AAC stereo, 19.77 seconds,
  Rec.709, integrated loudness `-16.7 LUFS`, true peak `-3.0 dBFS`.
