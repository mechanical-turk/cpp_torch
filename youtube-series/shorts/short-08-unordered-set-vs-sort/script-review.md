# Short 08 script review

September 16, 2026. Sequential writer/critic review, not independent reviewers.
The discarded script under `../trash/` remains unchanged.

## Objective and evidence

Challenge selecting the fastest implementation from Big O alone, using the
ordinary reserved `std::unordered_set`, not a deliberately broken hash table.
Strengthen the agreed direction, expose the large speed difference before the change,
and invite discussion of memory behavior without claiming to have isolated it.

Short 05's [creative analysis](../../analytics/reports/2026-09-02-short-05-instagram-retention-and-creative-analysis.md)
and [native follow-up](../../analytics/reports/2026-09-07-native-insights-workflow-and-short05-baseline.md)
identify opening loss and a shallower middle/end. Apply the compact curiosity
callout, synchronized highlights, gestures and a worthwhile closing question.
Their individual causal effects are unknown. The early numerical escalation
and concrete continuation are current creator directions, not proven retention
or follow-conversion improvements. Latest September 15 operational report has
no newer native curve comparison that resolves those uncertainties.

## Checklist plan

| ID | Intended treatment and risk |
| --- | --- |
| S01 | Challenge complexity-based selection; informed objection: use a flat table. |
| S02 | Directly challenge choosing by Big O; visible code establishes the performance subject. |
| S03 | Code, expected O(n), caption, callout and red circle at frame zero. |
| S04 | Count distinct values with two implementations, no complexity lecture. |
| S05 | 9.68x before sorting, then input task and insertion loop. |
| S06 | Name standard container; qualify result; memory is a discussion lead, not isolated causality. |
| S07 | Same shuffled input and distinct count; include reserve and input copy. |
| S08 | Reveal sorting with paired seconds, resolving the early speedup. |
| S09 | Diagnose time spent first; ask why worse complexity wins after reveal. |
| S10 | Specific flat-table continuation; existing research supports a next demonstration. |
| S11 | Yellow/teal emphasis, no stacked competing captions. |
| S12 | Circle complexity, insertion, sorting, result and memory indirection in sequence. |
| S13 | Point, trace, compare and address viewer across all stages. |
| S14 | Approximately 30-second spoken sequence, no dead holds; timed read still needed. |
| S15 | Five-line and four-line body viewports, one at a time. |
| S16 | Simple direct hook, questions and active narration. |
| S17 | Filename first; recording directions only in script, review here. |
| S18 | Read ledger, discarded draft, Short 07, Short 05 evidence and open experiments. |
| S19 | C++ unordered_set vs sort as primary phrase; platform metadata research deferred. |
| S20 | Explicit unresolved final media gates and audio settings. |

## Benchmark handoff

Latest standard-table headline source, not the older 7.52x run:
`aliases/01-screen-short-form/deduplication/results/short-headline/`.
Files: `short-headline-summary.csv`, `short-headline-raw.csv`,
`short-headline-metadata.txt`.

- 100,000,000 shuffled uint32_t inputs, 99,000,000 distinct, 1% duplicates.
- Seven measured pairs, discarded warmup, alternating execution order.
- Sort median 2608.428625 ms; standard hash median 25248.86446 ms.
- Ratio of medians 9.679722196. Show 9.68x and say almost ten times.
- Display 2.61 s and 25.25 s; spoken 2.6 and 25 are coarser approximations
  of the same measurements, not a different experiment.
- Input creation and correctness checks excluded; reservation, allocation,
  sorting's copy, computation and destruction included.
- Apple LLVM 21, libc++ 210106; seed 2026091601. Source uses reserve(n).
- Metadata does not embed exact compiler flags for this run. The current
  normal benchmark Makefile uses C++23/O3/DNDEBUG; recover the actual build
  command before printing flags as a verified property of the recorded run.
  Do not silently substitute the native/LTO flags from another experiment.

The original 100M run measured 7.52x, so 9.68x is not a hardware constant.
Keep the run and conditions recoverable; do not select one fastest sample.
No new benchmark was run for this script.

Important counterevidence: the newer `phase-diagram` results and `custom.cpp`
already demonstrate a specialized hash table beating sorting at 100M/1%.
The Abseil sweep also wins smaller sizes. The next-test line introduces the
next on-camera comparison; do not pretend the research has not occurred or
that its outcome is unknown. Do not claim hashing universally loses, that Big
O is mathematically false, or that hardware alone explains the full gap.
The phase-diagram README's winner-count prose is internally inconsistent;
use its CSV for any precise follow-up claims instead of repeating that prose.

Complexity references: [unordered containers](https://eel.is/c++draft/unord.req)
and [sort](https://eel.is/c++draft/sort). Expected O(n) labels the full insertion
loop, not an O(1) badge misleadingly compared against a whole sort.

## Checklist audit

| ID | Status | Specific evidence or remaining repair | Points |
| --- | --- | --- | ---: |
| S01 | PASS | Worse algorithm wins; named standard container leaves a real flat-table objection. | 15 |
| S02 | PASS | "Stop choosing algorithms" starts the position immediately; Big O and the speed question are visible from frame zero. | 15 |
| S03 | PASS | Exact simultaneous code/caption/callout/circle design. Actual render unverified. | 10 |
| S04 | PASS | One distinct-count task and one implementation change. | 4 |
| S05 | PASS | Test-scoped almost-ten-times result precedes any sorting name or code. | 4 |
| S06 | PASS | "In this test", named table, expected complexity and non-causal memory prompt. | 10 |
| S07 | PASS | Reserve, copy, same input and output stated in directions and handoff. | 5 |
| S08 | PASS | Both paired times appear with the complete replacement. | 5 |
| S09 | PASS | "Where's the time going?" before reveal; complexity question immediately after. | 5 |
| S10 | PASS | Flat hash table is a concrete next demonstration; research already exists. | 5 |
| S11 | PASS | Selective outlined captions; opening text replaced, not stacked. | 3 |
| S12 | PASS | Five named attention targets, not an opening-only sticker. | 3 |
| S13 | PASS | Gestures specified across problem, replacement, memory and closing. | 2 |
| S14 | PARTIAL | Dense explanation with 30-second target; actual read and question pacing not measured. | 2 |
| S15 | PASS | 5/4-line body shots; Number preserves uint32_t benchmark type. | 3 |
| S16 | PASS | Short spoken sentences, no em dash or manufactured conversational setup. | 2 |
| S17 | PASS | Filename and > narration in script; review and keyword record separate. | 1 |
| S18 | PASS | Evidence and prior draft repairs recorded above; no causal performance forecast. | 2 |
| S19 | PASS | Accurate primary phrase and explicit boundary on platform SEO approval. | 1 |
| S20 | PASS | Open export/audio/preview checks explicitly retained below. | 1 |

## Critique and final decision

The revised order fixes the discarded draft's late numerical escalation.
The full-loop O(n) label also fixes comparing a single hash insertion against
an entire sort. Both are existing S05-S08 rules, not new playbook additions.

First-pass criticism: "I made this" spends the first words on the presenter,
and "worse algorithm" needs clarification. Applied repair: "Stop choosing
algorithms by Big O alone." It makes the position explicit without asserting
that asymptotic analysis is false. The canonical script now contains that repair.

Biggest remaining weakness is spoken pacing: the second question needs room
to sound genuinely curious rather than a checklist requirement. A natural
timed read remains necessary; no generated word-count estimate proves delivery.

The two questions are distinct but could feel scripted if delivered with long
dramatic pauses. Ask them over the continuing visual; do not wait for an answer.
The memory hint offers a useful reasoning direction without pretending this
timing experiment isolates cache misses. The standard container's semantics,
allocator, hash/capacity choices and duplicate rate remain informed discussion
topics, not mistakes to hide. Public copy should disclose the flat-table
counterexample and point to the complete results.

Score: 98/100. Decision: rework.

This is a usable recording draft, not a claim that every mandatory editorial
check passes. Resolve the timed read before locking it.

## Production handoff

- Final frame-zero phone-size inspection: UNVERIFIED.
- Recurring annotations and presenter movement in final export: UNVERIFIED.
- Timed read and ffprobe duration, target 25-30 seconds: UNVERIFIED.
- Three-platform interface/safe-area inspection: UNVERIFIED.
- CapCut +5 dB once, Enhance voice 75%, all split clips; settings confirmation
  and listening review for clipping/artifacts: UNVERIFIED.
- Exact run build provenance, finished overlays and paired timing labels:
  confirm in the publishing package before release.
- No image, animation, recording, upload, publishing package or release date
  was created or approved. Embedded snippets are viewport directions only;
  camera-ready scene files can be prepared separately in the code workspace.


## September 16 — Clay animation rewrite: checklist plan

This visual-only revision preserves every spoken line. It supersedes earlier
visual directions and their audit after the rewrite below; benchmark provenance
above remains applicable. Scope: script and animation pitch, not rendering.

| ID | Planned treatment / risk |
| --- | --- |
| S01 | Preserve Big O challenge; separate node layout and compact array make the informed objection visible. |
| S02 | Preserve exact hook; code and active hash structure present immediately. |
| S03 | Complete first frame; editorial caption/callout/circle stay outside the clean Blender asset. |
| S04 | One distinct-count example; five illustrative values, no collision or allocator lecture. |
| S05 | Early 9.68× precedes replacement; timed code and model changes on spoken cues. |
| S06 | Separate sorting from unique; no invented cache-miss trace or universal hashing claim. |
| S07 | Preserve reserve and copied input; same illustrative multiset and supplied run. |
| S08 | Full timings and ratio follow visible replacement. |
| S09 | Preserve both questions exactly, motion continues underneath. |
| S10 | Flat-table preview only when named; no new result or return to code. |
| S11 | Captions in final edit only, no baked banners or duplicate hook. |
| S12 | Complexity, insert, sort/unique and memory path receive sequential attention. |
| S13 | Specify pointing, gathering and comparison gestures below animation. |
| S14 | Existing 30-second target; sort/unique needs a timed read before locking. |
| S15 | Shorter viewport identifiers; linked tile masters; native safe-zone proof pending. |
| S16 | Spoken language unchanged. |
| S17 | Canonical script retains filename and > narration; reviews remain here. |
| S18 | Apply Short 05 opening evidence, current experiment caveats and Short 07 approved native look. |
| S19 | Preserve filename and existing subject; no new public copy or keyword claims. |
| S20 | Seven numbered clips planned; render, final audio and interface gates remain unverified. |


### Visual rewrite audit

This audit applies to the rewritten canonical script, not the superseded
caption-led staging above. Sequential self-review, not independent reviewers.

| ID | Status | Evidence / repair | Points |
| --- | --- | --- | ---: |
| S01 | PASS | Unchanged complexity challenge; separate-node and contiguous-layout comparison preserves a flat-table objection. | 15 |
| S02 | PASS | Exact hook retained; active hash model and code at frame zero. | 15 |
| S03 | PASS | Scene 01 specifies code, complexity, clay, presenter and separate editorial hook/callout/circle. Actual composite pending. | 10 |
| S04 | PASS | One five-value teaching example and one distinct-count task; no extra algorithm lecture. | 4 |
| S05 | PASS | Scene 02 teases ratio without sorting; copy, sort and unique synchronize with replacement reveal. | 4 |
| S06 | PASS | Duplicate attempts leave count unchanged; copied source preserved; unique keeps allocation and marks logical end. | 10 |
| S07 | PASS | reserve and input copy retained; benchmark handoff unchanged; toy duplicate fraction explicitly illustrative. | 5 |
| S08 | PASS | Scene 05 resolves tease with paired times, method labels and ratio from supplied medians. | 5 |
| S09 | PASS | Both exact questions preserved, directly before and after replacement/payoff. | 5 |
| S10 | PASS | Scene 07 names next test and cuts; new table has no timing, old measurement stays labeled. | 5 |
| S11 | PASS | Caption treatment remains in final edit; clean native assets contain no baked editorial overlays. | 3 |
| S12 | PASS | Complexity circle, insert underline, staged copy/sort/unique emphasis, result arrow and path tracing. | 3 |
| S13 | PASS | Point upward, follow a link, gather hands, compare times, trace memory and face viewer. | 2 |
| S14 | PARTIAL | Complete 30-second target; natural read plus five-second reorder/unique beat still needs rehearsal. Retiming is explicit. | 2 |
| S15 | PASS | Five/four code rows, shortened local name and targeted using declarations, repeated tile masters and exact template workflow. | 3 |
| S16 | PASS | Spoken words mechanically identical to incoming script. | 2 |
| S17 | PASS | Original filename retained; only narration uses >; review remains separate. | 1 |
| S18 | PASS | Current report, native follow-up, open experiments, idea ledger and approved clay reference consulted. | 2 |
| S19 | PASS | Existing C++ unordered_set vs sort subject and filename preserved; no new public-copy claims. | 1 |
| S20 | PASS | Seven clean scene files, direct assets location, proof/audio/duration/interface gates explicitly planned. | 1 |

### Critique and applied repairs

The first visual proposal risked turning the hash nodes directly into a sorted
row. That loses duplicated input before sort even begins. The canonical version
keeps the original five-value tray and visibly copies it when the code does.
Hash nodes withdraw as a separate assembly, not as the source of the new array.

A second risk was making unique look like deleting storage. The sample now
sorts to 1,2,3,3,4, so unique has an observable compaction: 4 moves left, the
logical end precedes the fifth slot, and the allocated tray stays intact.
The tail's numeral is hidden; the illustration does not assert its value.
These are different actions from sorting's earlier reorder.

The proposed ending could misattribute 25.25 s to the newly compacted hash
diagram. The canonical script keeps method labels with the measured times
and gives the flat-table preview its own label and no timing. That motion is
an editorial preview, not a measured in-place conversion. Existing flat-table
research is acknowledged in the earlier benchmark handoff; it is not unknown.

The biggest remaining weakness is pacing and visual load during the replacement.
Copy, reorder, unique and the code transition require distinct readable beats.
Keep five tiles, one active attention target, stacked comparison lanes and a
fixed camera. A native still and a simple motion preview must establish whether
this composition fits; no exact pixel clearance is claimed from prose. Rehearse
the unchanged narration before locking scene durations. This visual-only task
does not authorize changing the spoken script to rescue the timing.

Score: 98/100. Decision: rework.

S14 remains partial under the mandatory rubric. The pitch is ready for creator
review; that is separate from a locked recording or rendered-media approval.
The score is not an audience-performance prediction.

### Evidence, semantics and production handoff

- The September 15 engine report contains newer aggregate Short 07 metrics,
  but no native curve comparison establishing that clay caused retention gains.
  Apply the Short 05 lesson as a design hypothesis: complete first frame,
  immediate progress, synchronized emphasis and meaningful final question.
  The September 7 native follow-up explicitly cautions against causal transfer.
- Short 07's final-v9 package, sculpted still and builder define the actual
  look. Reuse geometry/material/light sources; the proposal is new choreography.
  This episode has no threads or cache-line ownership transfer.
- Read the short-headline summary CSV and metadata for the existing 100M/1%
  result. They match 25248.86446 ms, 2608.428625 ms and ratio 9.679722196.
  No benchmark ran. Exact-run compiler flag provenance remains unresolved as
  already documented; animation must not print invented build flags.
- C++ semantics checked against [unique](https://eel.is/c++draft/alg.unique)
  and [unordered containers](https://eel.is/c++draft/unord.req): unique returns
  a new logical end; duplicate set insertions do not add another equivalent key.
  Clay routes/reorders are schematic, not an implementation or hardware trace.
- Viewport-only edit: sorted becomes s; std::sort/std::unique become unqualified
  calls with targeted using declarations off camera. Same copy, operations and
  returned distance. Runtime source was not changed; viewport files remain to
  prepare if requested. Use unlit native glyphs and test longest-line bounds.
- Proposed native exports: 01-big-o-opening, 02-speedup-tease,
  03-hash-insertions, 04-sort-and-compact, 05-benchmark-result,
  06-memory-layout, 07-flat-table-tease, each .mp4. Nominal durations are
  3/2/7/5/3/7/3 seconds; actual frame ranges await spoken rehearsal.
- Native 2160×2300 / 24 fps, seven independent silent clips; 1080×1150 previews.
  Place at (0,0) in 2160×3840 master. All render products go directly under
  this episode's assets/blender-clay-scenes/ when rendering is authorized.
- Current task produced written directions only. Native stills, motion,
  safe-zone/phone proofs, all-frame crossings, export duration, audio listening,
  CapCut settings and three-platform interface checks remain UNVERIFIED.
  Retain the four final-export gates from the earlier production handoff.


## September 16 — Creator correction, keyframes v2: checklist plan

Supersedes the preceding visual treatment. Spoken words and benchmark remain
locked. The creator revoked the video batch and requested seven native review
stills before any motion render.

| ID | Plan for this revision |
| --- | --- |
| S01 | Keep the Big O challenge and memory-layout question. |
| S02 | Keep the exact hook; begin with code and an active insertion. |
| S03 | Remove native complexity/callout text; preserve a complete first frame. |
| S04 | One five-value example, 3,1,3,2,1, with two redundant occurrences. |
| S05 | Tease ratio, then hash insertion, sort, unique and result in order. |
| S06 | Show unique's retained prefix and unchanged allocation; no invented tail values. |
| S07 | Use direct v iterators; disclose prepared working copy off camera without changing measured scope. |
| S08 | Retain paired measured seconds and 9.68×. |
| S09 | Preserve both audience questions. |
| S10 | Flat-table preview remains unmeasured; immediate cut. |
| S11 | Keep speech captions separate from native renders. |
| S12 | Use insert/sort/unique emphasis, matching duplicate colors and result arrow. |
| S13 | Retain code, path, array and result gestures. |
| S14 | Rehearse unchanged speech before locking motion; stills cannot verify pacing. |
| S15 | Native glyph bounds, phone review and actual template proofs for seven poses. |
| S16 | Preserve every spoken line verbatim. |
| S17 | Replace canonical visual directions, retain filename; audit stays here. |
| S18 | Apply prior evidence cautiously and actual Short 07 clay materials. |
| S19 | Existing subject/filename; no new public copy. |
| S20 | Stop v1; seven review PNGs only, remote GPU evidence, no video approval. |


### Revision 3 plan amendment — remove labels, expose indirection

Creator rejected every floating method label, including labels under results.
This overrides v2's S03/S08/S10/S12/S15 treatments: keep code, benchmark figures,
units/speedup and physical numerals only. S06/S07: a contiguous bucket-pointer
rail leads to separately placed nodes; each lookup follows a pointer before
checking the stored key. Contrasting adjacent values illustrates locality,
not a measured number of misses or a claim sorting does fewer instructions.
S20: exactly seven stills, no motion batch. Other plan rows remain applicable.


### Revision 3 script audit (supersedes previous visual scores)

| ID | Status | Evidence / next check | Points |
| --- | --- | --- | ---: |
| S01 | PASS | Exact Big O challenge retained; node indirection versus contiguous values invites a substantive objection. | 15 |
| S02 | PASS | Hook unchanged; opening already has code and an insertion in progress. | 15 |
| S03 | PASS | Code, five colored values and active hash route complete frame zero; removed extra labels per explicit creator direction. | 10 |
| S04 | PASS | One five-value example and one distinct-count task. | 4 |
| S05 | PASS | Ratio tease, bucket/key check, sort, unique, measured payoff in that order. | 4 |
| S06 | PASS | Unique keeps allocation; tail unspecified; routes schematic; no fabricated collisions, misses or rehashing. | 10 |
| S07 | PASS | reserve visible; prepared v keeps real benchmark copy within unchanged timed scope; same supplied medians. | 5 |
| S08 | PASS | 25.25 s -> 2.61 s and 9.68×; no method labels cluttering figures. | 5 |
| S09 | PASS | Both original audience questions preserved verbatim. | 5 |
| S10 | PASS | Next table introduced by speech and slot layout; old benchmark clears to avoid attributing it to the new test. | 5 |
| S11 | PASS | Narration captions remain an editing layer, absent from native renders. | 3 |
| S12 | PASS | insert/sort emphasis, active pointer pulse, matching-key press and result arrow provide meaningful attention cues. | 3 |
| S13 | PASS | Code, path, array, result and next-table gestures remain in directions. | 2 |
| S14 | PARTIAL | Spoken read and sorting/unique pacing still need rehearsal; no duration locked from stills. | 2 |
| S15 | PASS | Direct v code; consistent value palette; all seven pose glyph bounds pass; final rendered review remains separate from script fit. | 3 |
| S16 | PASS | Spoken lines mechanically preserved through both visual edits. | 2 |
| S17 | PASS | Canonical script contains only recording content; audit here; filename unchanged. | 1 |
| S18 | PASS | Prior audience evidence remains qualified; actual Short 07 native clay reused; indirection explanation checked against primary reference below. | 2 |
| S19 | PASS | Existing subject and upload filename retained; no new public claims or copy. | 1 |
| S20 | PASS | Seven stills only; video remains stopped, template/motion/platform/audio checks distinguished. | 1 |

Critique: the strongest addition is separating bucket selection, dependent
pointer travel and key comparison instead of using arbitrary slow motion to
make hashing look bad. The array must still visibly reorder before unique's
linear pass. A static scene cannot establish weighted timing or causality:
those remain review requirements for the next motion stage. The narration is
unchanged, so its natural read must determine how long these beats need.

Removing method labels creates a risk when the next unmeasured table appears.
The repair is to retire the previous timings before that new layout enters,
not restore unwanted floating words. Do not claim that fewer comparisons, a
fixed number of cache misses, or locality alone caused the measured ratio.
[Abseil's indirection discussion](https://abseil.io/fast/83) supports the general
pointer-dependency rationale, not a causal profile of this benchmark.

Score: 98/100. Decision: rework.

S14 is still partial. Creator review of the seven stills and a natural spoken
read precede motion. This score evaluates script directions, not final video,
measured retention or publication readiness.


### Physical-occupancy correction during authorized animation

Creator identified overlapping boxes in a motion preview. Corrected S06/S12/S15:
new insertion creates one stored shell, duplicate queries form in a vacant
comparison position and squash away, and the final lower-tray move waits for
the upper nodes to clear. Opening descent waits for horizontal clearance.
Zero value-shell intersections across all 456 poses after expanding the audit
beyond sorting. Native corrected-pose preflight remains separate. Spoken lines
and measurements are unchanged. S20: full batch not started before this repair.
Prior script score remains 98/100 (rework: S14 natural-read timing is still an
editing dependency), not a claim about rendered motion or publication readiness.


### 2026-09-16 — Tiny-preview bucket redesign: affected-check plan

Creator rejected the rope-based hash model, weak input selection and cyan end
divider. This revision changes visuals only; the spoken lines remain locked.

| Check | Planned repair |
| --- | --- |
| S03 | Occupied bucket wells and one clearly outlined duplicate input at opening. |
| S05 | Source selection, bucket selection, landing or duplicate comparison in order. |
| S06 | Schematic bucket ownership, no claimed hash function, capacity, measured addresses or pointer trace; preserve allocation/tail semantics. |
| S12 | White outline on the actual active input and processed array value. |
| S13 | Point to selected input, then its bucket; trace contiguous retained values later. |
| S15 | Remove ropes and purposeless divider; keep actual clay and code, audit box clearance. |
| S20 | Seven 216×230 motion previews only; creator feedback precedes resolution expansion. |

Affected-check audit after the visual rewrite: S03/S05/S06/S12/S13/S15/S20
retain their planned script points (10/4/10/3/2/3/1). Opening, source-order
insertions, duplicate rejection, selection highlights, gestures, unchanged
allocation semantics and tiny-only delivery are explicit in script.md. Spoken
lines were compared mechanically and are unchanged. Other checks retain the
previous audit; S14 remains 2/4 pending the natural spoken read.

Critique: three destination wells simplify away the pointer mechanism; this
version must not claim to visualize literal pointer traffic or prove the cause
of the benchmark. Its success depends on whether viewers read the selection,
landing and duplicate rejection immediately. Creator motion review is pending.
The 10% previews cannot settle final code sharpness. Script score remains
98/100, rework for the existing S14 timing dependency; this is not motion or
publication approval.


### Source-only contour correction

S12/S15 visual repair: replace padded selection frames with a thin contour
projected from the sculpted source shell. Remove every destination highlight,
including the later stored-key highlight. Only input/working-array sources
may be selected, at most one at a time. Spoken lines, timing and other visual
semantics remain unchanged; prior script score and S14 dependency unchanged.
Motion remains a 10% preview for creator review.


### 2026-09-16 — Static storyboard conversion

Scope: creator replaced animation with a slideshow. Spoken lines remain
mechanically identical. Affected-check plan: S03 establishes input/output in
one image; S05 shows both states of every transformation; S06 separates
logical examples from benchmark/memory claims; S12 uses simple operation
arrows; S13 gestures identify the compared states; S15 aligns projected rows
and separates sort from unique; S20 delivers only tiny Blender PNGs.

Audit: all those visual directions are now explicit in script.md. No frame
requires an unseen transfer or animated disappearance. The duplicate example
shows insert(3) leaving {3,1} unchanged. Sort preserves five values; unique
shows three retained values without shrinking allocation. Benchmark unchanged.
Other prior checks remain unchanged; S14 natural-read timing is unresolved.
Prior script score remains 98/100, rework for S14. This is not approval of
rendered comprehension, full-resolution legibility or publication.

Critique: a static memory-layout diagram is schematic and cannot isolate the
cause of the speedup. A 216×230 composition proof is too small to establish
final code readability. Creator storyboard review precedes larger rendering.
