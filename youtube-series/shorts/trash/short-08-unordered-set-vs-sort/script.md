Proposed MP4: `cpp-unordered-set-sort-distinct-count-short.mp4`

# Short 08: Big O lost

Status: first full draft. Benchmark evidence exists and is cited below;
recording, animation, and final-media checks are separate production tasks.
Premise reframed September 15, 2026: this script names `std::unordered_set`
specifically -- the container a C++ programmer reaches for by default -- and
does not make a claim about hashing as an algorithm family. See the idea
ledger for the earlier, broader-claim version that was paused for this reason.

## Checklist plan

| Check | This draft's approach and known risk |
| --- | --- |
| S01 | Challenge "better Big O always wins" with a named, ordinary container losing badly. Position: `std::unordered_set` (average O(1) insert) loses to sort-then-scan (O(n log n)) at real scale. Objection to invite: "but hashing is asymptotically faster, this must be a bad benchmark." Risk: viewers who already know about cache-unfriendly node-based hash tables may find this less surprising; mitigated by not explaining the mechanism until asked. |
| S02 | Open on `std::unordered_set`, a name the target audience recognizes instantly, immediately paired with "better Big O" and "still lost." No setup sentence before it. |
| S03 | Frame zero: the name `std::unordered_set`, an "O(1) avg" badge, and a red "STILL LOST" stamp all visible together, over a blurred field of shuffled numbers. Plan the muted phone-size check. |
| S04 | One claim only: this specific container loses to sorting for this task at this scale. No detour into hash function quality, load factor, or general hashing theory. |
| S05 | "Still lost badly" is the qualitative escalation, delivered inside the hook itself, before any code or mechanism appears. The exact ratio is held for the visible-evidence payoff later, not spent here. |
| S06 | Claim is scoped to `std::unordered_set` by name, not "hashing." Mechanism (node-based separate chaining, forced by pointer/iterator stability, causes per-element heap allocation and pointer-chasing) is real and previously verified in this investigation; it is described only if the recording narration is extended, not required to fit the 25-30s cut. No invented numbers; both cited figures are measured. |
| S07 | "Both functions count the distinct numbers in the same shuffled array" states the invariant before either implementation is shown. Evidence handoff: exact ms values and the 7.52x ratio are supplied below, not invented here. |
| S08 | Ratio ("seven and a half times faster") is spoken as the payoff after the solution appears; the precise ms values appear on screen as visible evidence at the same beat. The winner is not left ambiguous after this point. |
| S09 | Two distinct questions: "So what could beat one hash insert per number?" (diagnosis, before the solution appears) and "Why would extra comparisons beat a single direct lookup per element?" (explanation, immediately after the solution and payoff). Different kind of reasoning each time. |
| S10 | "Next, I'm testing whether a different hash table changes this," then cut. Real and specific: this investigation already has a flat-hash-table counterexample banked, unnamed here, that becomes the next Short. |
| S11 | Selective yellow/teal caption emphasis on "still lost," "hash set," "sorts," and the ratio. No duplicate held hook caption. |
| S12 | Red "STILL LOST" stamp at open; a distinct "?" callout style for the diagnosis question; a comparison arrow at the payoff; a second, differently colored "?" for the explanation question. Four distinct annotated beats. |
| S13 | Point to the container name at open; alternate gesture toward each code block as it appears; gesture between both blocks at the second question; open-handed "what's next" gesture at the close. |
| S14 | Estimated ~25-27s at a natural conversational pace on the current draft (see word-count estimate in production notes). Timed read and `ffprobe` measurement remain a recording-stage task. |
| S15 | Two snippets, 5 and 4 lines (`scenes/scene_1.cpp`, `scenes/scene_2.cpp` in the code workspace), well under the 14-17 line guidance even shown together. Short `int` element type, minimal qualifiers, one-line signatures. |
| S16 | Short active sentences, no em dashes, no "imagine"/"picture this," no machine specs spoken aloud. `std::unordered_set` and `O(1)` are technical terms the viewer can use immediately. |
| S17 | This file: filename above, one `>`-marked canonical narration below, scene directions kept separate. Runnable snippets live in `~/code/short-08-unordered-set-vs-sort/scenes/`. |
| S18 | Checked the idea ledger: this is the September 2026 sorting-vs-hashing idea, paused once for an overbroad "hashing" claim and once more after exploring matrix-multiplication and Karatsuba alternatives that produced weaker margins (best ~1.8x vs. this figure's 7.52x). This is not a repeat of the discarded lesson; it is the same idea correctly re-scoped. |
| S19 | Candidate primary phrase: "std::unordered_set vs sort." Supporting language: C++ distinct count, hash set performance, container performance. Platform-specific keyword research remains a separate publishing task. |
| S20 | Recording, animation, audio, and platform-preview checks are open. This request does not authorize recording, rendering, or publishing. The CapCut audio checklist is included below for the eventual edit. |

## Canonical script

Timing windows are editing targets estimated from a natural read of this
draft, not measured narration. A timed read at recording remains a
production task (S14).

### 0:00-0:02 | Hook

> std::unordered_set has the better Big O here. It still lost, badly.

Frame zero: `std::unordered_set` in large monospace type, an "O(1) avg" badge
beside it, both already on screen with no fade-in. A blurred field of shuffled
number tiles sits behind the text, established but not yet explained. As
"still lost" lands, a red "STILL LOST" stamp appears over the badge. Point
toward the container name on "std::unordered_set."

### 0:02-0:07 | Explain the problem

> Both functions count the distinct numbers in the same shuffled array. This one inserts every value into a hash set.

Reveal `scenes/scene_1.cpp` (`count_hash`), phone-size, syntax highlighted.
The blurred number field sharpens into individual tiles. As "inserts every
value" lands, tiles move one at a time from the array into a loose cluster of
nodes scattered at random positions, not a tidy grid, visually distinct from
the ordered array they came from. Gesture toward the code on "this one."

### 0:07-0:10 | Why does the problem occur?

> So what could beat one hash insert per number?

Code and node cluster hold, slightly dimmed. A red "?" callout appears over
the scattered nodes. This is a genuine invitation to guess; do not answer it
yet, and do not let the next beat's code appear early.

### 0:10-0:15 | Reveal the solution

> This one sorts a copy first, then scans it once for changes.

Reveal `scenes/scene_2.cpp` (`count_sort`) beside or replacing scene 1. The
same shuffled tiles slide into sorted, contiguous order as "sorts a copy"
lands, then one sweep arrow passes across the row exactly once as "scans it
once" lands. Gesture toward the newly revealed code.

### 0:15-0:18 | Payoff

> Seven and a half times faster.

Reveal `2.48s` and `18.66s` as large on-screen numbers with a comparison
arrow between them, then the `7.52x` stamp. Use the cited figures below
verbatim; do not round further or restate them differently on screen than in
`evidence/notes.md`. Point to the improved time.

### 0:18-0:23 | Why does the solution work?

> Why would extra comparisons beat a single direct lookup per element?

A second "?" callout appears, teal instead of the earlier red, over both code
blocks together. Gesture between the two snippets rather than pointing at
either alone; this question is about the comparison, not either side in
isolation.

### 0:23-0:27 | Next test and cut

> Next, I'm testing whether a different hash table changes this.

Look toward the viewer. The `std::unordered_set` badge from the open reappears
briefly with a small "?" beside it, not a name or a number. Cut immediately
on "this." No end card, no return-to-code shot, no follow request.

## Production and evidence notes

### What the visual means

- The scattered node cluster represents `std::unordered_set`'s node-based
  layout (a separately allocated node per element, positions not related to
  insertion order or value). It is a simplified 2D motion graphic, not a
  literal memory map or a claim about exact heap addresses.
- The sorted, contiguous tile row represents a `vector` after `std::sort`:
  one allocation, elements adjacent in memory. The single sweep arrow
  represents `std::unique`'s one pass, not a literal frame-by-frame trace.
- Both code snippets are simplified for phone-size display: `int` instead of
  `uint32_t`, short names, and no `reserve()` call shown. The measured
  numbers come from the real benchmark implementation in
  `~/code/deduplication/dedup.cpp` (`Number = uint32_t`, hash set uses
  `reserve(values.size())`), not from the simplified on-screen snippets.
  This does not change the shown mechanism; it removes detail that is not
  essential to the comparison being made. Both snippets were compiled and
  checked against `std::sort`/`std::unordered_set` reference behavior before
  writing this script (see `~/code/short-08-unordered-set-vs-sort/scenes/`).
- Do not depict the hash set as literally "checking" each existing tile
  during insertion, animate a visible rehash event, or suggest the sort
  comparisons happen one-at-a-time in a way that implies `std::sort` is not
  also doing real, nontrivial work. Sorting's cost is real; it is simply
  smaller than the hash set's cost at this scale, on this container.

### Cited evidence

- 100,000,000 values, 1% duplicates (99% distinct): sort + unique 2,481.27 ms,
  `std::unordered_set` with `reserve(n)` 18,662.49 ms, ratio 7.52x.
- Full measurement contract, correctness checks, and raw samples:
  `~/code/deduplication/README.md` and
  `results/full-sweep-1m-100m-{raw,summary,metadata}`.
- A fresh reconfirmation run on September 15, 2026 measured a larger ratio
  (9.68x at the same size) under confirmed heavy machine swap pressure at
  the time of the run; that run is not cited as the headline figure because
  `std::unordered_set`'s per-element heap allocations are more sensitive to
  memory pressure than sort's few large allocations, making the larger ratio
  plausibly a swap artifact rather than a more accurate measurement. Full
  detail and the decision rationale: `evidence/notes.md` in the code
  workspace. Before recording, either confirm the machine is at a normal
  swap baseline and re-run once, or accept 7.52x as final without a further
  re-run.
- This script deliberately withholds the flat-hash-table counterexample
  (Abseil's `flat_hash_set`, and a custom open-addressing set, both of which
  beat sorting at this and most other tested sizes). That evidence exists,
  is real, and is reserved for the named "next test" follow-up, not
  disclosed here. See the idea ledger for the full investigation trail.

### Technical gate before recording

- Verify the exact cited numbers against the current `results/` files before
  the numbers are locked into rendered assets; do not carry a stale figure
  forward if the `deduplication` project's results change.
- Confirm the recording machine's swap/memory state before any fresh
  headline benchmark run, and note it in the run's metadata, per the
  existing project's own evidence-recording convention.
- Both snippets must remain correct if trimmed further for the actual edit
  (verify with a quick compile-and-run against the assertions in
  `/tmp/scene_check.cpp`'s pattern, or an equivalent check, before locking
  the on-screen code).
- Single-threaded throughout, matching this investigation's established
  convention; do not introduce multithreading into this comparison.

### Editing and release handoff

- Preserve a complete, muted, phone-size frame-zero check.
- Master export target: 2160 x 3840, matching the current animation-family
  convention for this channel.
- Measure and review the final export with `ffprobe`, targeting 25-30
  seconds; this draft's estimate (~25-27s) is not a substitute for a timed
  read.
- CapCut: spoken audio +5 dB once; Enhance voice intensity 75%; confirm
  every split clip inherits the setting; listen for clipping before upload.
- Platform-specific keyword/hashtag research, public title/caption/comments,
  cover assets, and `publishing.md` remain outside this writing task.

Evidence and prior planning: [idea ledger](../../content-ideas.md) (the
"Counting distinct numbers: sorting versus hashing" entry, including the
September 15 matrix-multiplication and Karatsuba exploration that led back
to this reframed version), `~/code/deduplication/README.md` and
`optimization-notes.md`, and `evidence/notes.md` in this Short's code
workspace folder.

## Checklist audit

Script-level design judgments below do not certify unrendered media.

| Check | Status | Evidence / repair | Points |
| --- | --- | --- | ---: |
| S01 | PASS | Names `std::unordered_set` specifically, states its Big O advantage, and shows it losing anyway; the informed objection ("but it's asymptotically faster") is the exact belief being challenged. | 15/15 |
| S02 | PASS | First words are `std::unordered_set has the better Big O`; no greeting, series context, or qualification precedes it. | 15/15 |
| S03 | PARTIAL | Container name, badge, and stamp are specified for frame zero, but the blurred-array background is a production judgment call not yet tested at phone size and muted. | 5/10 |
| S04 | PASS | One claim only: this container loses to sorting at this scale for this task; no hash-quality or load-factor detour. | 4/4 |
| S05 | PASS | "Still lost, badly" escalates inside the hook, before any code, mechanism, or exact number. | 4/4 |
| S06 | PASS | Claim is scoped to the named container throughout; both cited numbers are real and sourced; no claim about hashing in general. | 10/10 |
| S07 | PASS | States the shared input and task before either implementation appears; exact figures and their source are supplied in production notes, not invented mid-script. | 5/5 |
| S08 | PASS | Ratio is spoken and exact figures appear on screen together at the payoff beat, resolving the opening promise with evidence, not left ambiguous. | 5/5 |
| S09 | PASS | "What could beat one hash insert per number?" precedes the solution; "why would extra comparisons beat a single lookup?" follows the payoff. Different reasoning each time. | 5/5 |
| S10 | PASS | Names a real, specific, already-banked next experiment (a different hash table) and cuts immediately on "this." | 5/5 |
| S11 | PASS | Named emphasis words and two distinct callout colors specified; no duplicate held caption. | 3/3 |
| S12 | PASS | Four distinct, purposeful annotation beats named (stamp, red "?", comparison arrow, teal "?"). | 3/3 |
| S13 | PASS | Distinct gesture named for each of the four beats plus the close. | 2/2 |
| S14 | PARTIAL | Word-count estimate lands at ~25-27s; a timed, natural read at recording is still required to confirm pacing, especially across the two-question ending. | 2/4 |
| S15 | PASS | 5- and 4-line snippets, compiled and checked, short types, one-line signatures, well under the line guidance. | 3/3 |
| S16 | PASS | Short active sentences; no em dashes, forced casualness, or spoken machine specs. | 2/2 |
| S17 | PASS | Filename first, one canonical narration, scene directions separate, runnable snippets in the code workspace. | 1/1 |
| S18 | PASS | Ledger checked; this draft names the prior overbroad-claim pause and the September 15 alternative-idea exploration as the applied lesson. | 2/2 |
| S19 | PASS | Accurate candidate phrase and supporting terms; platform research explicitly deferred. | 1/1 |
| S20 | PASS | Recording, animation, audio, swap-state, and preview checks are explicit and open; this request authorizes none of them. | 1/1 |

## Critique

The strongest part of this draft is that it no longer needs to hedge. Naming
`std::unordered_set` directly, instead of "hashing," means every sentence in
the script is defensible on its own terms: the container really does have
better average-case Big O, it really did lose by 7.52x on a real, verified
benchmark, and the script never claims more than that. The paused, broader
version of this idea needed a disclosure the audience would find deflating
("but actually a different hash table wins"); this version turns that same
fact into the hook for the next Short instead of a caveat inside this one.

The two-question structure is more literally compliant with S09 than the
most recent precedent (Short 07), which effectively merged its pre-solution
and post-solution questions into one beat near the end. I chose to keep them
distinct here because the diagnosis question ("what could beat one hash
insert?") is cheap to ask and genuinely puzzling before the mechanism is
shown, whereas Short 07's topic required more setup before any question
would make sense. This is a judgment call, not a settled house style; if a
recorded read makes the two questions feel like a checklist rather than two
different thoughts, collapsing them the way Short 07 did is a reasonable
fallback, at the cost of S09's literal wording.

The biggest open risk is pacing across six narration beats in ~25-27
seconds. That is on the fast side relative to Short 07's 25-30s natural read
for five beats. The fix, if the timed read runs short or rushed, is to hold
the payoff numbers a beat longer or slow the two questions, not to cut the
explanation or the second question.

The evidence handling is the other place this draft made a deliberate
choice worth flagging: today's fresh reconfirmation run measured a bigger
ratio (9.68x) than the cited 7.52x, under measurably heavy swap pressure.
Using the larger, more dramatic number would have been easy to justify in
the moment and was rejected because the swap condition makes it a weaker,
not stronger, piece of evidence. This is recorded in `evidence/notes.md` so
the reasoning survives if someone re-opens the question later.

Remaining production work: a timed read to confirm S14 and S03's phone-size
check, and the swap-state decision named in the technical gate before any
further benchmark run backs a locked number.

Two mandatory checks, S03 and S14, are PARTIAL rather than PASS. Following
Short 07's precedent, a partial mandatory item blocks advancement regardless
of total score, so this is a rework rather than an advance, even though both
gaps are production-verification tasks (a phone-size render check and a
timed read) rather than writing defects.

Score: 93/100. Decision: rework.
