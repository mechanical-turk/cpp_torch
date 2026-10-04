# Short 08 Publishing Package

## Checklist plan

September 16, 2026. Preparation for YouTube Shorts, Instagram Reels, TikTok
and native X video. No publication or scheduling authorized by this document.
LinkedIn and Reddit deferred. Latest creator direction: talking head with code
overlays, no animation requirement. Final export outranks the older storyboard.

| ID | Specific plan |
| --- | --- |
| P01 | Match the export, two code snippets and seven-run standard-container benchmark; disclose missing transcript/audio review. |
| P02 | Research each destination separately; record weak search coverage instead of inventing demand. |
| P03 | Lead with C++, unordered_set, sorting and Big O in useful sentences. |
| P04 | Separate YouTube backend tags from restrained, platform-supported hashtags. |
| P05 | Direct technical result, plain English and useful paragraph breaks. |
| P06 | Standalone Short title; no long-form episode branding. |
| P07 | Native uploads, link-free main copy; no unverified benchmark repository URL. |
| P08 | Prepare substantive first comments with controls and flat-table nuance. |
| P09 | Name the located export and descriptive upload basename; rename remains pending. |
| P10 | Select real cover frames per platform; Instagram technical cover keeps existing no-face direction. |
| P11 | Measure export and inspect sampled frames; do not certify full playback from a contact sheet. |
| P12 | Specify audience, comments, playlist and relevant related Short; verify saved state later. |
| P13 | Check technical subtitles against final speech; no chapters for this Short. |
| P14 | Offer next standing Friday slot with same-day native distribution, not a claim about best posting time. |
| P15 | No public source URL supplied, so no implied published benchmark. |
| P16 | Preserve parser headings; isolate paste-ready fields. |
| P17 | Score this preparation stage honestly, with media checks pending. |
| P18 | Inspect live posts, report direct URLs, then append actual events to timeline. |

## Publishing content

- Upload filename, all four platforms: `cpp-unordered-set-vs-sort-big-o-performance-short.mp4`.
- Located source: `aliases/04-final-cuts/shorts/ep08/0916.mp4`.
- Source SHA-256: `74c788c6561dd9695b1800ce874457036b07a6f0748c03183db1e016e8ecca54`.
- Measured: 2160 x 3840, 30 fps, H.264 video, AAC audio, 36.566667 seconds.
- Descriptive filename is proposed; no rename or duplicate created.
- Sampled frames confirm talking head, captions, complexity labels and two code
  overlays. Full speech transcription and audio listening have not been completed.
- Sampled hash overlay uses `vector<int>` / `unordered_set<int>` while sorting
  uses `Number`. Benchmark uses uint32_t on both sides. Confirm the on-screen
  types before upload; do not describe these differing overlays as literal
  identical benchmark source. The measured comparisons themselves use the same type.
- Latest seven-run medians for 100M integers, 1% duplicates: standard hash set
  25248.86446 ms; sorting 2608.428625 ms; ratio 9.679722196.
- Evidence: `aliases/01-screen-short-form/deduplication/results/short-headline/`.
  Allocation, reserve, sorting's input copy and destruction are timed. Same
  shuffled input; both return 99M distinct values. The older 7.52x is a different run.
- Exact build flags are not embedded in this run's metadata. Do not claim a
  particular flag set in public copy until the build command is recovered.
- No live Short 08 URL established. Existing Blender assets are not required
  by the current creator direction and are not approved covers.

## Platform research records

Research date for all records: September 16, 2026. Search wording evidence is
not search-volume or ranking evidence. No paid tweet data was pulled.

### YouTube

- Checked indexed YouTube results for C++ unordered_set benchmarks, including
  [CppNuts: std::unordered_set In C++](https://www.youtube.com/watch?v=Yevgn0yu5mI).
  The API name and C++ appear in its title; container, hashing and complexity
  vocabulary appear in its description. It is an older tutorial, not proof of
  current performance for our premise.
- Owned precedent: Short 04 uses Big O/performance framing; no causal keyword
  result or query-demand measurement available.
- Candidates: C++ unordered_set vs sort; C++ hash set performance; Big O.
  Primary: C++ unordered_set vs sort. Supporting: sorting, distinct count,
  time complexity, C++ performance. These appear in title/description/tags.
- No visible hashtags. Backend tags include standalone C++, programming,
  algorithms and data structures plus the precise implementation phrases.
- Reject unrelated ML/CUDA tags and #shorts. Autocomplete and query volumes unavailable.

### Instagram

- Independent indexed searches for C++ hash-table/performance Reels returned
  no usable comparable Reel in this session. Use owned-platform evidence:
  [Short 05](https://www.instagram.com/reel/DcyO3GYimT3/) and its
  [captured creative report](../../analytics/reports/2026-09-02-short-05-instagram-retention-and-creative-analysis.md).
- That report records C++/CPU performance copy and actual use of #cpp,
  #programming and #softwareengineering. It does not isolate hashtag effects.
- Candidates: C++ performance, hash set vs sorting, Big O. Primary: C++
  unordered_set vs sorting; support: hash set, memory access, distinct integers.
- Retain #cpp for language, #programming for subject, #softwareengineering for
  audience. Reject #cpu because this is not an isolated CPU measurement;
  reject unresearched #cppperformance, #viral, #fyp and #shorts.
- Current comparable-post coverage, native autocomplete and query volume unavailable.

### TikTok

- Independent search attempted for C++ hash-table and performance posts;
  TikTok pages blocked by robots and unrelated shop results rejected.
- Owned evidence: Short 07 package records previous TikTok use of #cpp,
  #programming and #computerscience; [owned Short 07](https://www.tiktok.com/@mechaturka/video/7684647347833326879).
  This establishes account precedent, not demonstrated hashtag lift.
- Candidates: C++ performance, Big O, sorting vs hash set. Primary: C++ hash
  set vs sorting. Supporting: unordered_set, Big O, benchmark.
- Retain #cpp, #programming and #computerscience for language, practice and
  complexity subject. Reject #fyp, #viral, #shorts and invented compounds.
- Native search suggestions, independent current comparable posts and query
  volume remain unavailable. Research is provisional rather than SEO-approved.

### X

- Independent indexed searches for unordered_set/sorting performance returned
  no relevant current post. Do not use unrelated X engineering articles as
  evidence of audience search language.
- Owned precedent: earlier native technical Shorts and the creator's existing
  technical audience; no post-level data pulled or current search-demand claim.
- Candidates: C++ unordered_set, sorting, Big O. Primary: C++ unordered_set vs
  sorting. Supporting: O(n), O(n log n), distinct integers.
- No hashtags: use scarce space for the concrete comparison. No link preview
  competes with the native upload. Native search/autocomplete unavailable;
  this platform's research remains partial.

## Final title

```text
C++: Why Sorting Beat std::unordered_set by 9.68x
```

## YouTube description

```text
C++ std::unordered_set has better expected time complexity than sorting. It still took 25.25 seconds to count distinct integers in this benchmark. std::sort followed by std::unique took 2.61 seconds.

Same 100 million shuffled integers, 1% duplicates, seven-run medians. The hash set reserves capacity first. Sorting includes the cost of copying the input. Both measurements include allocation and cleanup.

Expected O(n) versus O(n log n) doesn't settle which implementation runs faster. Memory access, allocation and the workload matter too.

This comparison uses the standard library's unordered_set, not the fastest available hash table. Flat hash tables can change the result. That's the next comparison.
```

## Suggested tags

```text
C++, cpp, programming, algorithms, data structures, Big O, time complexity, C++ performance, unordered_set, std::unordered_set, hash set, hash table, sorting, std::sort, std::unique, unordered_set vs sort, count distinct values, benchmarking, memory locality
```

## Pinned comment

```text
reserve() is included, and the sorting timer includes copying the input. Both functions count the same distinct values without changing the source array.

The choice of hash table matters. Our flat-table experiments already changed the comparison substantially, so this result applies to std::unordered_set, not hashing in general. Which implementation would you put against sorting?
```

Prepared candidate only, not posted or pinned. Inspect existing author comments
before posting, and report the direct comment URL afterward. No GitHub link.
No repeated pinning checks.

## Instagram

### Reel caption

```text
C++ unordered_set vs sorting: the better Big O lost this benchmark by 9.68x.

Both count distinct values in 100 million shuffled integers with 1% duplicates. The hash set took 25.25 seconds. Sorting and scanning took 2.61 seconds.

The hash set reserves capacity first, and sorting pays for its input copy. These are seven-run medians, including allocation and cleanup.

Where would you look first for the extra time?

#cpp #programming #softwareengineering
```

### First comment

```text
This is std::unordered_set, not a claim about every hash table. Flat tables can change the result, and we've already seen that in the follow-up experiments. Memory layout and allocation deserve a closer look before blaming Big O.
```

Accessibility description, only if the composer supports a relevant field:
presenter discussing a C++ hash-set and sorting benchmark, with code overlays,
complexity labels and spoken-word captions. Verify final visual wording first.
Do not paste this internal description into an unsupported field.

## TikTok

### Caption

```text
C++ hash set vs sorting: std::unordered_set lost by 9.68x on 100M integers with 1% duplicates. Expected O(n) vs O(n log n). Why did the worse Big O win?

#cpp #programming #computerscience
```

### First comment

```text
Seven-run medians: 25.25s vs 2.61s. reserve() is included, and sorting includes copying the input. Different hash-table implementations can change the winner; this result is specific to std::unordered_set.
```

## X

### Native video post

```text
C++ unordered_set took 25.25s to count distinct integers. Sorting took 2.61s on the same input.

100M values, 1% duplicates. Expected O(n) lost to O(n log n).

Big O alone is a poor way to pick the fastest implementation.
```

### Technical reply

```text
Seven-run medians, with reserve() included for the hash set and the input copy included for sorting. Allocation and cleanup are timed too.

This compares std::unordered_set, not hashing in general. Flat tables already changed the result in our follow-up tests.
```

Upload video natively. No YouTube backlink or navigation reply is required for
this standalone technical Short. No external URLs in Instagram/TikTok copy.

## Settings and release checks

- YouTube: initially private for checks; English; Science & Technology;
  not made for kids; comments on, intended Newest-first sorting where supported.
  Sorting does not disable moderation or reveal held comments.
- Add to the existing Shorts playlist without manual sorting. Related-video
  candidate: existing Short 04, “Big O Matters So Much Less Than You Think”.
  Resolve and verify its video ID in the channel before saving; do not guess.
- No long-form end screen or artificial chapters for this Short.
- Verify public 2160p playback before release. Other platforms may transcode
  the 4K source. Preview code overlays against each platform's interface.
- Instagram/TikTok: intended public native Reel/video, comments enabled;
  inspect actual sharing/remix controls before deciding their saved state.
- YouTube/TikTok: choose a readable code/title frame using available cover
  controls. X uses the actual poster frame/composer behavior.
- Instagram cover: separate technical cover, no face per standing cover rule;
  planned `assets/cover-instagram-reel.png`, 1080 x 1682 with all essential
  content inside the centered 1080 x 1080 region. Asset not created or approved.
  Talking head in the video does not automatically amend the no-face cover rule.
- Check captions for unordered_set, std::unique, expected linear time,
  N log N, 9.68x and the final continuation. No transcript verified yet.

## Short upload gate

Reviewed source identity and dimensions are recorded above. Sampled contact
sheet: `/tmp/short08-contact.png` (temporary diagnostic, not durable release evidence).

| Required check | Status | Evidence / next action |
| --- | --- | --- |
| Exact first-frame hook at phone size | UNVERIFIED | Five-second sampling is not an exact frame-zero review. Extract the first decoded frame and inspect without sound. |
| Annotations throughout | UNVERIFIED | Sampled complexity and code overlays exist; review complete playback for purposeful markers and legibility. |
| Dense, substantive duration | PARTIAL | 36.566667 seconds, above the 25-30-second target. Review delivery before accepting the extra time; do not automatically pad or cut essential substance. |
| Presenter movement throughout | PARTIAL | Hands/gestures visible around sampled 5s and 25s; continuous review still needed. |

Audio gate: +5 dB once and Enhance voice 75% require creator confirmation;
AAC metadata cannot prove settings. Complete audio listening remains pending.
Benchmark gate: reconcile on-screen int/Number types and recover precise build
provenance before certifying the final presentation. No disabled-optimization
claim is made. Final full-media and platform-preview approval remains on hold.

## Distribution and follow-through

- Consulted current timeline and standing cadence. No Short 08 publication recorded.
- Proposed default: Friday, September 18, 2026, YouTube at 2 PM ET after checks;
  Instagram, TikTok and X native uploads in the 2-4 PM ET window as available.
  Friday follows the standing two-Short weekly cadence. The clock time is a
  practical proposed window, not an analytics-established optimum. Nothing scheduled.
- If the creator chooses an earlier release, use the same approved master and
  record actual times; do not hold a finished upload solely to defend this window.
- LinkedIn and Reddit deferred rather than automatically duplicating the post.
- Before any first comment/reply, check existing account-authored comments for
  functional duplicates. Prepared text does not authorize posting.
- After reported publication: inspect the direct URL, account, live media,
  captions, audio, code crop, cover/profile tile, comments and restrictions.
  Verify YouTube tags, playlist and related video. Report direct post/comment
  URLs and append observed events to docs/distribution-timeline.md.
- Creator: confirm final export and audio settings. Assistant: inspect approved
  media, reconcile copy and carry out separately authorized platform actions.

## Checklist audit

| ID | Status | Evidence and required follow-up | Points |
| --- | --- | --- | ---: |
| P01 | PARTIAL | Results/code checked; final speech and int/Number overlay discrepancy pending on all platforms. | 5/10 |
| P02 | PARTIAL | YouTube vocabulary and IG owned evidence usable; TikTok/X search coverage weak and explicitly provisional. | 7.5/15 |
| P03 | PASS | Language, named implementations, Big O and benchmark task in each platform's actual copy. | 10/10 |
| P04 | PASS | YT backend broad/specific terms; no YT/X hashtags; IG/TT use separately recorded owned precedent. | 8/8 |
| P05 | PASS | All copy uses plain active English, readable paragraphs and no em dashes or canned contrast. | 10/10 |
| P06 | PASS | Short title and native platform fields; short X post and compact TikTok caption. | 5/5 |
| P07 | PASS | Deliberate link-free native posts, no card-preview dependency or unverified code URL. | 5/5 |
| P08 | PASS | Specific prepared comments/reply; duplicate check and URL reporting stipulated, no posting claimed. | 5/5 |
| P09 | PARTIAL | Real source and hash inspected, descriptive filename not yet applied. | 2/4 |
| P10 | UNVERIFIED | All platform cover/poster selections and actual crop previews pending. | 0/4 |
| P11 | PARTIAL | Dimensions/duration/hash and sampled visuals inspected; full playback/audio and gate incomplete. | 3/6 |
| P12 | PARTIAL | Intended settings documented; playlist/related ID, saved state and processing pending. | 1.5/3 |
| P13 | PARTIAL | Caption terms identified; final speech/captions not transcribed. No Short chapters required. | 2/4 |
| P14 | PASS | Dated conditional window, standing cadence, native sequence and deferrals documented. | 3/3 |
| P15 | N/A | Standalone Short with no public source URL or long-form source-release requirement. | excluded |
| P16 | PASS | Exact parser headings and isolated copy blocks; no unresolved public URL placeholders. | 2/2 |
| P17 | PASS | All 18 rows, exclusions and readiness boundaries explicit. | 2/2 |
| P18 | PASS | Concrete live checks, duplicate prevention, direct URLs and append-only ledger handoff. | 2/2 |

## Critique

The copy names the standard container and gives enough methodology to make
the result interpretable without turning every caption into a disclaimer.
Flat-table counterevidence appears in comments and the YouTube description;
we do not manufacture a universal claim about hashing.

The main unresolved issue is matching the actual recording: the edited video
is longer than planned, uses differing visible type names, and has not received
a complete speech/audio review. Fix or explain the types, then verify that the
spoken benchmark and continuation match the package before publication.

TikTok/X keyword research is limited. The copy uses accurate technical terms,
but this is not evidence of optimal search targeting. Inspect native suggestions
when preparing those uploads, rather than claiming the weak indexed results
establish demand. No extra decorative hashtags are warranted.

## Final score

- Preparation score: 73 / 98 x 100 = 74.5/100. P15 excluded with stated reason.
- Copy: drafted for all four platforms, not final-recording approved; TikTok/X
  research remains provisional.
- Upload/public release: on hold for media/audio, type consistency, covers,
  interface previews and platform settings/processing.
- This score measures package completeness, not projected engagement or reach.

Score: 74.5/100 (73/98). Decision: hold for release; publishing copy prepared.
