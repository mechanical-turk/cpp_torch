# Short 06 Publishing Package

Current upload filename: `cpp-data-layout-structure-of-arrays-performance.mp4`

Prepared September 5, 2026, Eastern Time. Use this exact basename on YouTube,
Instagram, TikTok, and X when uploading the same master.

## Post-publication status: September 6

- The fixed export is published on
  [YouTube](https://www.youtube.com/shorts/SPWFaXBs8tE) and
  [TikTok](https://www.tiktok.com/@mechaturka/video/7682503962943114526).
- YouTube publication: **3:15:06 PM ET**. TikTok's exact timestamp remains
  unverified. Both URLs and account identities were checked directly.
- The actual fixed file is
  [cpp-data-layout-structure-of-arrays-performance.mp4](../../../aliases/04-final-cuts/shorts/ep06/cpp-data-layout-structure-of-arrays-performance.mp4).
  YouTube's uploaded filename, byte size, and dimensions match it.
- YouTube 4K processing and Shorts playlist membership are confirmed. The
  creator selected Short 4 as the related video; this relevant choice was
  preserved instead of overwriting it with the planned Episode 1 below.
- Added the missing 16 YouTube backend tags, saved Newest comment sorting,
  and posted the prepared
  [first comment](https://www.youtube.com/watch?v=SPWFaXBs8tE&lc=UgzcpXEZx-K4LxHxZwF4AaABAg)
  after duplicate inspection. The one-time pin reminder was delivered.
- Preserved the live YouTube title, including the creator's appended
  `#cpp #coding #programming` hashtags. Description and TikTok caption match
  the prepared copy. Downloaded and reviewed YouTube's English ASR text.
- TikTok's first comment is **not posted**: Chrome is signed out, and the
  creator was asked to sign in. The Phyllo content feed has not indexed this
  upload yet, despite its verified public availability.
- The fixed export is 2160x3840 at 30 fps, **14.366667 s**. The exact first
  frame still lacks the spoken subtitle, so the strict first-frame gate is
  not passed. Live crop checks and subjective audio review remain unverified;
  measured audio peaks at 0.0 dBFS and needs a listening check.
- Full evidence, hash, completed actions, and remaining checks:
  [September 6 post-publication audit](post-publication-2026-09-06.md).

The September 5 preparation and old-export observations below are historical.
References there to `0905.mp4`, the proposed `-short-06` filename, and no
publication do not describe the current rollout. The old source is no longer
present under that filename; this task did not rename or replace media.

## Preparation status: September 5

- Recording and editing: completed, reported by the creator.
- Reviewed export: [0905.mp4](../../../aliases/04-final-cuts/shorts/ep06/0905.mp4).
  Rename the upload copy to the descriptive filename above. The source was
  not renamed or modified during this review.
- Export verified: **2160 x 3840, 30 fps, 14.366667 seconds**, H.264 High,
  Rec.709, AAC stereo at 44.1 kHz.
- Platform copy and platform-specific research records: prepared below.
- Upload approval: **held**. The spoken opening caption starts on frame 1,
  not frame 0. Extend it backward by one frame, then verify the new export.
  The large `PERFORMANCE TRAP` callout and red annotations already appear on
  frame 0. This is a strict first-frame gate issue, not a request to rerecord.
- Audio listening and actual platform crop/cover previews remain unverified.
- No upload, publication, first comment, or schedule was created by this task.

## YouTube Shorts

### Title

```text
This C++ Struct Is a Performance Trap
```

### Description

Copy only the plain text inside this block. No visible hashtag block or
Markdown styling belongs in the YouTube description.

```text
C++ data layout made these score lookups 12.5x faster: 4.36 ms to 0.35 ms in this benchmark.

Each player stores a score beside 15 historical scores, but this loop only needs the current scores. Moving from an array of structs to a structure of arrays puts the scores together while keeping every history stored separately.

The benchmark uses 1,048,576 ordered player IDs from 4,194,304 players. Both versions use the same IDs, values, lookup order, and result. The build uses normal -O3 optimization; both compiled lookup loops are scalar. No vectorization-disabling flags were used.

The times measure the lookup batch after the layouts are built, not allocation or conversion. The size of the gain depends on the workload, compiler, and hardware.

What changes when the loop needs the histories too?

Build a tensor with flat storage in C++ in Episode 1 of Deep Learning, All the Way Down:
https://www.youtube.com/watch?v=DmU2b64tWfA
```

### Metadata tags

These are backend tags, not text to paste into the description.

```text
C++, cpp, C++ performance, C++ structs, data layout, memory layout, array of structs, array of structures, structure of arrays, struct of arrays, AoS, SoA, data oriented design, loop optimization, CPU performance, C++ benchmark
```

### First comment

```text
The histories are real stored values, not padding. Both layouts keep them.

The 12.5x result measures score-only lookups with ordered IDs. Normal -O3, no vectorization-disabling flags, and scalar loads in both compiled loops.

Which access pattern would make you keep the fields together?
```

Before posting, inspect all existing channel-authored comments and avoid a
duplicate. After posting, return its direct URL and remind the creator to pin
it once. Do not add a GitHub link or repeatedly check pin status.

### Settings and navigation

- Upload filename: `cpp-data-layout-structure-of-arrays-performance-short-06.mp4`.
- Upload privately first; confirm 2160p playback before public release.
- English; Science & Technology; not made for children.
- Comments and embedding enabled. Set the default comment sort to Newest first
  where available; this does not override moderation or reveal held comments.
- Add to `Deep Learning, All the Way Down | Shorts`, not the long-form playlist.
- Set Episode 1 as the related video:
  https://www.youtube.com/watch?v=DmU2b64tWfA
- Rationale: its flat tensor storage and indexing provide a concrete long-form
  continuation. It does not teach this exact benchmark or prove the speedup.
- Do not leave a missing related-video assignment as a reminder-only task when
  authorized Studio control is available. Add it and verify the saved state.
- Select a readable opening frame using the available Shorts cover controls.
  No separate YouTube cover asset has been prepared or verified for this release.
- Review automatic captions against the export, especially `struct`, `scores`,
  `histories`, and `twelve times faster`. No chapter block for this short clip.

## Instagram Reel

### Caption

```text
This C++ struct slows down a loop that never reads most of its fields.

Moving the scores into their own array cut the lookup batch from 4.36 ms to 0.35 ms. Every player history stays stored. This is a structure-of-arrays layout.

Measured with about 1.05 million ordered IDs from 4.19 million players, using normal -O3. Both compiled loops are scalar. Timing covers the lookups, not building or converting the layouts. Results depend on the workload and hardware.

Would you keep the fields together when the loop needs the histories too?

#cpp #coding #programming #cpu #softwareengineering
```

### First comment

```text
The histories are real data, not padding. The loop skips them in both versions, and both layouts retain them.

The next test reads the scores and histories for the same player IDs. Would you expect the split layout to keep its lead?
```

Inspect existing author comments before posting. No external URL in the caption
or first comment. Return the direct comment URL after any publication.

### Cover and settings

- Upload filename: `cpp-data-layout-structure-of-arrays-performance-short-06.mp4`.
- Upload the reviewed 4K master natively. Keep comments enabled and check the
  intended sharing/remix controls in the actual composer.
- Cover: **not prepared or approved**. The opening video frame contains the
  creator's face; do not silently reuse it as the standalone Instagram cover.
- For a separate `cover-instagram-reel.png`, follow the repo's `1080 x 1682`
  template, with all essential technical content inside the centered square
  at approximately y=301 through y=1380. No face unless specifically requested.
- Inspect the real Reel, feed, and profile-grid previews. Dimensions alone do
  not pass the crop check. The actual video uses code above the presenter,
  unlike the earlier script's planned layout.
- No scheduling action is recorded. Do not assume the browser composer offers
  scheduling; it did not for Short 5.

### Accessibility description

Use where the upload interface supports an appropriate accessibility field;
availability for this Reel has not been verified.

```text
A C++ player struct stores scores beside histories. An animation separates the scores into one array and preserves the histories in another. The score-only benchmark changes from 4.36 milliseconds to 0.35 milliseconds. A presenter uses arrows, circles, and highlighted captions to explain the change.
```

## TikTok

### Caption

```text
C++ data layout: these score lookups ran 12.5x faster after separating the fields. The scores move into one array; every history stays stored.

About 1.05M ordered IDs from 4.19M players, normal -O3, both compiled loops scalar. Query time only, excluding layout construction. What changes when we need the histories too?

#cpp #coding #programming #computerscience #softwareengineering
```

### First comment

```text
The two layouts use the same player IDs and return the same total. The measured loop reads only scores. Would the result change if it needed each player's full history too?
```

### Cover and settings

- Upload filename: `cpp-data-layout-structure-of-arrays-performance-short-06.mp4`.
- Use the same reviewed master with original audio, no external caption URL,
  and comments enabled. Check the intended Duet and Stitch settings.
- Select a frame with `PERFORMANCE TRAP` and the player records visible.
  Inspect the actual profile-grid crop and right/bottom interface overlays.
- Cover and platform rendering: unverified. No schedule or post exists yet.

## X native video

### Main post

```text
This C++ loop never reads the histories, but their placement costs time.

Separating the scores cut this batch from 4.36 ms to 0.35 ms. Every history stays stored.

~1.05M ordered IDs, ~4.19M players, normal -O3. What changes when we need both?
```

Upload filename: `cpp-data-layout-structure-of-arrays-performance-short-06.mp4`.
Attach the video natively. No hashtags or external URLs in the main post.
Verify the opening poster in X's composer rather than assuming a custom image
can be attached as its cover.

### Technical reply

```text
Both compiled lookup loops are scalar, without vectorization-disabling flags. The timing excludes allocation and layout conversion. This is the ordered-ID result, not a claim that every access pattern improves by 12.5x.
```

### Optional series navigation reply

```text
I also build tensors and autograd in C++ in Deep Learning, All the Way Down. Episode 1 starts with flat storage and indexing:
https://www.youtube.com/watch?v=DmU2b64tWfA
```

This is a native standalone Short, not an Episode 6 announcement. Do not imply
that the series repository hosts this benchmark. Only the YouTube episode URL
appears in the navigation reply, so a GitHub preview cannot replace it.
Inspect existing replies first; return direct URLs for any replies actually
posted. Nothing in this package has been posted.

## Keyword and hashtag audit

Research date for every record: **September 5, 2026 ET**.

Research used the final export's visible captions and code, the benchmark,
owned-platform records, and current web searches. Live autocomplete and query
volumes were not obtained. Failed or irrelevant search results were not used
as evidence. These are relevance decisions, not claims of optimal search volume
or guaranteed distribution.

### YouTube research record

- Sources checked: owned [Short 5 package](../short-05-instruction-dependencies/publishing.md),
  including its separately recorded YouTube Search contribution;
  [CppCon's Data-Oriented Design and C++ video](https://www.youtube.com/watch?v=rX0ItVEVjHc);
  [YouTube's tag guidance](https://support.google.com/youtube/answer/146402?hl=en-EN);
  [YouTube's description guidance](https://support.google.com/youtube/answer/12948449?hl=en-GB);
  and [CERN's structure-of-arrays documentation](https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideStructureOfArrays).
- Owned-account evidence: earlier C++ performance Shorts received search
  traffic. The available record does not expose the exact viewer queries for
  this new topic; do not invent them.
- Candidate phrases: `C++ structs`, `C++ performance`, `C++ data layout`,
  `array of structs vs structure of arrays`, `memory layout`.
- Primary subject: `C++ struct` plus its performance consequence in the title;
  `C++ data layout` leads the description.
- Supporting terms: the exact AoS/SoA technique and common spelling variants,
  memory layout, loop optimization, CPU performance, benchmarking.
- `C++` and `cpp` remain standalone metadata tags as language identifiers.
  The two expanded structure names and `AoS`/`SoA` identify the demonstrated
  comparison. `data oriented design` names the established topic family, not
  a promise to teach a complete design methodology in fourteen seconds.
- Hashtags retained: none, following the YouTube description rule.
- Rejected: CUDA, GPU programming, deep learning and machine learning as tags
  for this clip, disabling SIMD, padding optimization, and generic viral tags.
  The clip does not demonstrate those topics. The series link is navigation,
  not a reason to add unrelated tags.
- Unavailable: authenticated search suggestions, current query-volume estimates,
  and title-testing results. Conference terminology supports audience vocabulary,
  not a forecast that this title will outperform alternatives.

### Instagram research record

- Sources checked: Instagram-specific caption and hashtag records in the
  [Short 5 package](../short-05-instruction-dependencies/publishing.md) and
  [Short 5 final-media report](../../analytics/reports/2026-09-02-short-05-instagram-retention-and-creative-analysis.md).
  An Instagram-domain search for C++/programming/memory returned no useful
  results; no live-search popularity claim is made.
- Owned-account evidence: the published Short 5 Reel used `#cpp`, `#coding`,
  `#programming`, `#cpu`, and `#softwareengineering`. The report preserves
  over 100,000 plays at its checkpoint. Co-occurrence does not establish that
  those tags caused the reach.
- Candidate phrases: `C++ struct`, `C++ loop`, `C++ performance`,
  `structure of arrays`, `data layout`.
- Primary phrase: `C++ struct`, directly tied to the visible opening.
- Supporting terms: loop, scores, player histories, structure of arrays, lookup
  benchmark, compiler optimization. They explain the actual clip.
- Hashtags retained: `#cpp` for the language; `#coding` and `#programming` for
  the demonstrated code change; `#cpu` for the execution-performance audience;
  `#softwareengineering` for the storage-design tradeoff. Each has documented
  use on this Instagram account.
- Hashtags rejected: `#cppperformance`, `#dataorienteddesign`, `#soa`, `#aos`,
  `#viral`, and `#fyp`. No useful Instagram-specific evidence was obtained for
  the specialist compounds, and the generic virality labels add no subject.
- Unavailable: live Instagram autocomplete and hashtag/query volumes.

### TikTok research record

- Sources checked: TikTok-specific records for Shorts 3 and 4 in the
  [Short 5 package](../short-05-instruction-dependencies/publishing.md), plus
  the recorded native Short 5 rollout. TikTok web access was robots-blocked;
  irrelevant shop results were discarded.
- Owned-account evidence: the preserved Short 4 TikTok record used `#cpp`,
  `#coding`, `#programming`, `#computerscience`, and `#softwareengineering`
  among its tags. This is separate TikTok evidence, not Instagram reach used
  to validate TikTok tags. No new TikTok analytics pull occurred.
- Candidate phrases: `C++ data layout`, `C++ performance`, `C++ structs`,
  `structure of arrays`, `loop optimization`.
- Primary phrase: `C++ data layout`, placed first.
- Supporting terms: scores, fields, lookups, ordered IDs, optimization.
- Hashtags retained: `#cpp` identifies the language; `#coding` and
  `#programming` identify the demonstration; `#computerscience` identifies
  the data-representation topic; `#softwareengineering` identifies the design
  tradeoff. All have owned TikTok usage rather than borrowed Instagram evidence.
- Hashtags rejected: `#cppperformance`, `#soa`, `#aos`, `#viral`, and `#fyp`.
  No verified topic-specific TikTok evidence supports adding them.
- Unavailable: live TikTok search suggestions, Creator Search Insights, and
  current keyword/hashtag volumes.

### X research record

- Sources checked: the owned [Short 5 X copy record](../short-05-instruction-dependencies/publishing.md),
  the current benchmark, and the CppCon/CERN terminology sources above.
  An X-domain search for structure of arrays returned no useful result.
- Owned-account evidence: existing native performance copy uses `C++ loop`
  and compiler terminology. That establishes vocabulary already used, not
  measured discovery effectiveness. No tweet analytics were requested or pulled.
- Candidate phrases: `C++ loop`, `C++ performance`, `data layout`,
  `structure of arrays`.
- Primary phrase: `C++ loop`, followed immediately by the unread-field problem.
- Supporting terms: scores, histories, ordered IDs, -O3, lookup timing.
- Hashtags retained: none. Preserve room for the actual result and scope.
- Hashtags rejected: generic coding blocks and unverified specialist compounds.
- Unavailable: X autocomplete, query volume, and a matched post-performance test.

## Short upload gate

Reviewed file: `aliases/04-final-cuts/shorts/ep06/0905.mp4`.
SHA-256: `9d9cbe87feb14fc6b8825f2285b650aee8123e671c3400b8e908866af7b83321`.
Review date: September 5, 2026 ET.

Evidence: [first decoded frame at phone size](assets/final-review-2026-09-05/first-frame-phone.png),
[first ten consecutive frames](assets/final-review-2026-09-05/opening-first-ten-frames.jpg),
and four quarter-second contact sheets:
[0-3.75 s](assets/final-review-2026-09-05/contact-01.jpg),
[4-7.75 s](assets/final-review-2026-09-05/contact-02.jpg),
[8-11.75 s](assets/final-review-2026-09-05/contact-03.jpg),
[12 s to ending](assets/final-review-2026-09-05/contact-04.jpg).
Black unused tiles in the final sheet are contact-sheet padding, not evidence
of black frames in the video.

| Required check | Result | Observed evidence and action |
| --- | --- | --- |
| All hook elements on the first frame | FAIL | The code, red circle/arrow, face, and readable `PERFORMANCE TRAP` callout exist at frame 0. The yellow `THIS PATTERN` subtitle first appears at frame 1, about 0.033 s. Extend that caption to frame 0 and recheck. |
| Recurring targeted annotations | PASS | Opening circle/arrow at 0-1.75 s; lookup arrow around 2.25-3 s; score arrows around 3.5-4.5 s; retained-history arrow around 7-7.75 s; result circle around 9.25-10 s. |
| Complete export below 20 seconds | PASS | ffprobe format duration is 14.366667 seconds, including the tail. |
| Presenter movement throughout | PASS | Pointing during 0-1.75 s; hands brought together around 2-3 s; spreading hands around 3.25-4.5 s; pulling/packing gestures around 4.75-6.5 s; retained-data gestures around 7-8 s; result gesture around 9.25-10 s; head and hand movement through the closing questions. |

Overall four-check gate: **not passed until the first-frame fix is reviewed**.
Do not turn a planned fix into a recorded pass. Re-exporting changes the hash;
repeat the review against the actual upload file.

### Other final-media observations

- Burned-in text reads `THIS PATTERN DESTROYS PERFORMANCE`, not the discarded
  related-data hook. The close adds `WHY DO YOU THINK THAT'S HAPPENING` before
  asking about histories and saying what will be tested next. Copy follows
  these final visuals, not the old nineteen-second script timing.
- The code/animation occupies the upper region and the presenter the lower
  region. Do not mark the old planned webcam-above composition as observed.
- The displayed result is `4.36 ms`, `0.35 ms`, and `12.5x faster`, appearing
  around 8.25 s. The numbers remain visible during the next-test question.
  The score-plus-history test has no measured result in this package.
- Conditions are absent from the on-screen result. The description, captions,
  and first comments above therefore state the score-only, ordered-ID workload
  and timing boundary explicitly. Do not publish a stripped-down universal
  speedup claim. A compact `Score-only lookup` label during the result and
  removal of the old result during the next question would clarify the edit.
- Readable headline, score values, and captions at the inspected phone scale;
  detailed code is small. Platform overlays and cover crops require actual
  composer previews, which have not been inspected.
- Audio decodes and is non-silent; sample peak was -3.9 dBFS. This is not a
  subjective listening or synchronization pass. Listen to the complete upload
  copy with headphones before release.

## Distribution and post-publication work

- Publication window: **not selected or scheduled**. The standing Short days
  are Tuesday and Friday; the next standing slot after preparation is Tuesday,
  September 8. An earlier release is a creator-approved cadence exception,
  not an action performed by this package.
- Prepare native YouTube, Instagram, TikTok, and X uploads from the same master.
  No standalone LinkedIn, Reddit, or Hacker News announcement is planned for
  this compact lesson.
- This is a standalone C++ performance Short within the wider content project.
  It is not long-form Episode 6. Preserve the series name when providing the
  optional long-form navigation, without padding the Short's title with it.
- Immediately after each publication, run the repo's
  [post-publication check](../../../docs/operations/post-publication-check.md).
  Verify the actual account, media, audio, privacy/restrictions, caption,
  comments, cover crop, and platform-specific metadata.
- Record the exact publication time and direct video/post/comment URLs in the
  distribution timeline. Post first comments only after duplicate checks.
- On YouTube, verify Shorts playlist membership, Episode 1 related video,
  2160p playback, and captions. No manual playlist sorting is required.
- On Instagram and TikTok, inspect both playback and the profile-grid tile.
  Never infer their crop from the exported aspect ratio alone.
- Capture matched-age 24-hour, 72-hour, and seven-day results. Keep reach,
  retention, discussion, saves/shares, and follow conversion separate by
  platform. Twitter/X post-level data still requires an explicit request.
