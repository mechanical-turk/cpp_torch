Proposed MP4: `cpp-false-sharing-cache-line-padding-short.mp4`

# Short 07: Empty space

Revision: September 7, 2026 focused critique. Explain whole-line write access,
name padding, and make the next test understandable without "local counters."

Status: animation-led script draft; spoken pacing remains to review. Benchmark
verification is a separate production task, not a script-score requirement.
At initial drafting, neither benchmark nor animation had been created. The
[September 7 benchmark handoff](benchmark-results.md) now supplies measured
values; animation and recording remain separate. `[N]` stays clearly marked
until the result is incorporated into the recording and visual assets.

## Checklist plan

| Check | This draft's approach and known risk |
| --- | --- |
| S01 | Challenge compact-memory intuition with "Wasting memory made these threads faster." Invite the informed objection that accumulating privately would avoid repeated sharing. |
| S02 | Put "Wasting memory" first and complete the contradiction in one short sentence; the first frame must supply the performance context. |
| S03 | Start with the two active cores, shared tray, caption, "Too close?" editorial callout, and a red boundary marker already visible. No intro transition. |
| S04 | Explain the rule before its consequence: writing either counter needs write access to the whole line, so the cores interfere. |
| S05 | Identify each core's counter as it presses; identify the shared line as its rim switches color; move b as the relocation is spoken. |
| S06 | Explain different counters sharing a cache line accurately; mark result-dependent wording and placeholders. Motion is schematic, not a trace. |
| S07 | Specify equal work and changed counter placement, then hand timing/ratio placeholders to the benchmark owner. Verification is outside script scoring. |
| S08 | Reveal before/after time placeholders together with the corresponding spoken ratio placeholder. Do not copy Short 06's numbers. |
| S09 | Follow the result immediately with "Why is that handoff so expensive?" Invite discussion of the measured cost after explaining the basic mechanism. |
| S10 | Ask "What if we only shared the final totals?" and name that next test. Describe the proposed behavior instead of introducing "local counters." |
| S11 | Editorial captions use selective yellow/teal emphasis and outlines, separate from the clay scene. |
| S12 | Opening red boundary marker, switching rim, boundary-crossing arrow, then a result pointer direct attention through the entire short. |
| S13 | Point to the pair, alternate two fingers with updates, separate hands with b's move, then indicate the result and address the viewer. |
| S14 | Target 25-30 seconds with a complete ownership explanation. No word cap. Time the read after replacing [N]; cut repetition, not the mechanism or ending. |
| S15 | Two equal-sized counters, two identical fixed-size trays, large physical labels, no code wall. Verify phone-size readability and the actual composite safe areas. |
| S16 | Plain short sentences. No machine specifications, generic follow request, canned contrast, or unnecessary jargon beyond the labeled cache line. |
| S17 | One canonical >-marked script below, with filename above and non-spoken directions kept separate. |
| S18 | Apply Short 05's immediate visual promise and compact ending; develop the deferred false-sharing pitch with the creator's boundary-crossing animation. |
| S19 | Candidate primary phrase: C++ false sharing. Supporting language: cache line padding, multithreading performance. Platform keyword research remains a publishing task. |
| S20 | Keep proof, duration, animation, audio, and platform preview gates open. This request does not authorize running benchmarks, rendering, or publishing. |

## Canonical script

Timing windows are editing targets, not measured narration. Let the motion and
the explanation work together. Do not accelerate the read to preserve an old
animation duration; extend useful action/holds to fit the new narration.

### 0:00-0:02 | Crowded opening

> Wasting memory made these threads faster.

Frame zero: Core 0 and Core 1 sit above their own counters a and b inside one
navy tray labeled `cache line`. Short worker-colored update pulses are already
active. Gold consistently identifies Core 0/a; cobalt identifies Core 1/b.
Counters have identical geometry, distinct worker-colored accents, and deep
recessed labels. Point toward the pair immediately.

Editorial layer only: `Too close?` sits above the trays inside the safe region;
a red bracket/arrow targets their shared boundary. Place the synchronized spoken
caption near the presenter, without covering the face or gesture. Emphasize
`Wasting memory` in yellow and `faster` in teal; do not add a second held copy of
the hook. The Blender scene contains no caption or title card.

### 0:02-0:06 | Separate counters, shared boundary

> These cores update different counters, but both counters share one cache line.

Each counter gives a small press and numeral change as its worker pulses.
Alternate two fingers toward a and b, then trace the single tray boundary.
The opening red marker clears once the shared boundary is established.

### 0:06-0:13 | Explain the interference

> To change either counter, a core needs write access to the whole line. So the cores keep making each other wait.

The whole tray rim takes the active worker's color, then switches when the other
core gains write ownership. Trace the entire rim on "the whole line," then
coordinate a clear color switch with "making each other wait." Use a small hesitation to suggest
interference, not exact lockstep serialization or a handoff on every increment.
Counters stay stationary. Alternate an open hand between the workers while the
rim highlight makes the whole-line cost visible. This beat teaches the cause;
it is not filler before the move.

### 0:13-0:19 | Make room

> Add padding so b starts on another cache line. That stops the back-and-forth.

b lifts and moves across an explicit cache-line boundary into a second tray.
Both trays keep exactly the same size; a does not move and neither counter
changes size. Show recessed unused slots between the counter positions so the
additional memory is tangible. Briefly trace b's crossing with a red editorial
arrow. Separate your hands with the motion. Land b on "another cache line";
let both rim colors settle on "stops the back-and-forth." The recessed unused
slots make the spoken padding visible, rather than suggesting distance alone
is the fix.

Preserve a's gold and b's cobalt identities throughout. A small clay compression
settles b on landing. Each tray now retains its worker's rim color and the
counters update in independent rhythms. Do not animate a dramatic speed jump
that purports to reproduce an unmeasured ratio.

### 0:19-0:22 | Measured payoff

> Same updates, 5.5 times faster in this test.

Reveal `244.52 ms` in coral, one clean ivory arrow, and `44.19 ms`
in mint. Both values appear as one readable comparison above the settled
trays. Align their optical centers and keep the units smaller. Use actual
matched measurements with defensible rounding. Point to the improved time;
place a brief editorial pointer beside it without covering digits.

The animation has already revealed the direction of improvement. This beat
reveals its measured size; do not pretend the winner remains a mystery.

### 0:22-0:30 | Discussion and continuation

> Why is that handoff so expensive? What if we only shared the final totals? I'm testing that next.

Ask the first question immediately after the result line. The basic cause has
already been taught; this question concerns the size of the measured overhead,
not a pretend mystery about why spacing could matter at all. Look toward the
viewer, then gesture toward the counters' final values on "final totals." Hold the
timings and the settled scene throughout. Cut on `next`, with no end card,
return-to-code shot, or silent tail. The next test is proposed, not performed
or scheduled; confirm that commitment before recording.

## Production and evidence notes

### What the visual means

- The subject is false sharing between independently updated counters. Sharing
  a cache line, not simply physical closeness, is the relevant condition.
- Trays represent cache-line-sized address regions. They are not literal
  containers inside one shared physical cache. The rim color is a simplified
  indication of write ownership/activity, not a complete coherence protocol.
- b's relocation represents comparing two layouts, not moving live storage
  while worker threads access it. Configure each layout before its timed run.
- The two equal-size trays retain fixed boundaries. Do not stretch one cache
  line until it becomes two, introduce a lock, resize counters, or change work.
- The pulse rate, hesitation, presses, and independent rhythm are conceptual
  animation, not measured processor activity or a guarantee of perfect parallelism.
- Use the selected Retro Sunset background, sculpted matte surfaces, crisp warm
  studio key, cool edges, and deep recessed labels. Worker gold/cobalt colors
  identify ownership; timing coral/mint colors compare performance.
- Follow the animations playbook's pending whole-foreground downward placement
  correction when adapting the native scene. Verify the complete composite in
  real platform previews; source dimensions alone cannot prove safe placement.

### Technical gate before recording

Build nothing implicitly from this script request. When the experiment is
authorized, require:

- Two workers updating distinct, correctly initialized atomic counters, with
  identical increment counts, memory ordering, output checks, and normal
  optimized build settings in both layouts. Never race on one counter.
- Verify actual counter addresses, alignment, and target cache-line boundaries:
  packed counters share a line and separated counters do not. Do not assume
  64-byte padding guarantees this on every target.
- Exclude thread creation/allocation from the timed comparison or report a
  consistently scoped end-to-end measurement. Synchronize starts without
  placing timing/control data in the counters' measured cache lines.
- Repeated interleaved runs and a stable effect. Verify distinct-core execution
  where possible and document scheduler/placement limitations where not.
- Inspect generated code and use available coherence diagnostics to support
  attribution. Timing alone does not prove every illustrated mechanism.
- Store the actual benchmark source, commands, outputs, and evidence references
  before replacing [N] and both timing placeholders. If the gain is absent or
  unstable, revise the premise rather than tune away compiler optimizations.

The follow-up would compare private accumulation with publication of final
totals only. That changes intermediate visibility; it is not automatically an
equivalent substitute for counters whose progress other code must observe.
Leave that tradeoff for discussion without claiming local counters always win.

Technical reference: [Linux kernel false-sharing documentation](https://docs.kernel.org/kernel-hacking/false-sharing.html).
It supports the mechanism. Our measured comparison is recorded separately in
[benchmark-results.md](benchmark-results.md).

### Editing and release handoff

- Preserve a complete frame-zero hook; check it muted at phone size and with
  sound through the first three seconds.
- Use purposeful markers and presenter movement throughout, as specified above.
- Master: 2160 x 3840. For the clay source, follow the current animation-family
  dimensions and foreground-placement correction in the linked playbook.
- Measure and review the final complete export, targeting 25-30 seconds with
  natural, dense delivery. No arbitrary word cap or under-20-second rule. The
  scene can hold its result through speech; do not pad a complete lesson.
- CapCut: spoken audio +5 dB once; Enhance voice intensity 75%; confirm every
  split clip. Listen for clipping and processing artifacts before upload.
- Verify actual platform safe areas, captions, physical label legibility, exact
  timings, and the endpoint. No animation or export is approved by this draft.
- Platform-specific keyword/hashtag research, public title/caption/comments,
  covers, and publishing.md remain outside this writing task. The filename and
  search terms above are descriptive candidates, not SEO clearance.

Evidence and prior planning:
[Short 05 retention/creative analysis](../../analytics/reports/2026-09-02-short-05-instagram-retention-and-creative-analysis.md),
[prior false-sharing critique](../pitch-lab/2026-09-05/03-empty-space-faster-threads.md),
[idea ledger](../../content-ideas.md),
[Short 06 script](../short-06-data-layout/script.md), and the creator's animation
brief in this conversation. The first-frame treatment co-occurred with Short
05's Instagram success; it is not an isolated causal finding. This is distinct
from Short 06's score-only layout experiment, and it does not fulfill that
script's proposed score-plus-history follow-up.

## Checklist audit

Script-level design judgments below do not certify the unrendered media.

| Check | Status | Evidence / repair | Points |
| --- | --- | --- | ---: |
| S01 | PASS | "Wasting memory" challenges compactness; local/private accumulation supplies a substantive objection rather than a fake bug. | 15/15 |
| S02 | PASS | "Wasting memory" carries the contradiction immediately; "these threads" identifies what gets faster instead of the vague "this." | 15/15 |
| S03 | PASS | Opening names each layer, placement, frame-zero timing, marker target, and phone-size check. Render remains unverified. | 10/10 |
| S04 | PASS | Whole-line write-access rule, interference, then padding; one mechanism and one change. | 4/4 |
| S05 | PASS | Presses match "update"; rim trace matches "whole line"; b crosses and lands on "another cache line." | 4/4 |
| S06 | PASS | Explanation distinguishes counters from shared-line ownership; result-dependent wording is explicitly provisional with no invented number. | 10/10 |
| S07 | PASS | "Same updates" specifies the invariant, padding specifies the change, and "in this test" scopes the placeholder ratio. Verification stays with production. | 5/5 |
| S08 | PASS | Before/after times and spoken ratio resolve the opening promise together. Marked placeholders are valid at this stage. | 5/5 |
| S09 | PASS | The next spoken words after the result are "Why is that handoff so expensive?" It asks about cost, without withholding the mechanism. | 5/5 |
| S10 | PASS | "Only shared the final totals" describes a concrete next change without new jargon; cut on "next." | 5/5 |
| S11 | PASS | Separate editorial captions, yellow/teal key words, outline, and no competing held hook. | 3/3 |
| S12 | PASS | Boundary marker, rim activity, crossing arrow, and timing pointer each have a distinct beat. | 3/3 |
| S13 | PASS | Pair-pointing, alternating fingers, separating hands, result-pointing, and viewer-facing ending specified. | 2/2 |
| S14 | PARTIAL | 25-30-second beat plan teaches the access rule and change. Natural read and gesture timing remain to review, especially the two-question ending. | 2/4 |
| S15 | PASS | Fixed-size duplicate trays and counters, visible boundary, few large labels, no miniature code. Actual composite is unverified. | 3/3 |
| S16 | PASS | Direct short narration without specifications or preface; technical term immediately labels the visible tray. | 2/2 |
| S17 | PASS | Filename first, one canonical spoken draft, separate timecodes and directions. | 1/1 |
| S18 | PASS | References prior deferral, adjacent Short 06, and Short 05 Instagram evidence without inventing causal proof. | 2/2 |
| S19 | PASS | Accurate candidate subject and supporting terms with explicit platform-research boundary; no invented hashtag package. | 1/1 |
| S20 | PASS | Open evidence/render/timing/audio/preview gates and scoped next tasks are explicit. | 1/1 |

## Critique

The strongest part remains the tangible edit across a visible boundary. The
revision now names its implementation, padding, as the empty slots appear.
"These threads" makes the opening less vague. The payoff establishes both the
unchanged work and the scope of the speed claim in one sentence.

Benchmark verification remains a separate production dependency. The script
clearly marks the result-dependent opening and numerical placeholders; this is
not a writing defect or a deduction from the script score.

The earlier draft's "taking ownership" assumed the rule it needed to teach.
The new sentence supplies it: changing either counter requires write access to
the whole line. The following sentence ties that rule to the visible waiting.
It explains enough to learn from without a cache-coherence protocol lecture.

The ending now proposes observable behavior, sharing only final totals, rather
than naming "local counters" and assuming viewers understand the alternative.
It still asks about the cost of the just-shown handoff before introducing that
next test, and holds the completed result throughout.

Second-pass risk: the two closing questions carry different jobs and need to
sound different. Deliver the first with curiosity about the cost, then gesture
at the totals when proposing the next experiment. Do not make the ending a
rapid list of questions. The 25-30-second plan allows roughly eight seconds for
that ending, but a natural recorded read remains to verify. Shorten dead holds
before compressing the explanation or racing the final words.

The animation must not imply that the entire core stops doing all work, that a
software lock protects the tray, or that every increment forces a handoff.
Counter presses and the switching rim illustrate interference in these writes;
the core blocks themselves do not freeze. Production semantics already specify
schematic timing rather than measured processor activity.

See [focused critique record](critique-2026-09-07.md) for the prior weaknesses,
applied repairs, and second review. No new audience result is claimed.

Score: 98/100. Decision: rework.

This supersedes the 85.5/100 hold under the earlier responsibility assignment.
S06-S08 now assess writing and evidence handoff, not the benchmark owner's work.
S14 remains partial pending spoken pacing review; do not confuse that delivery
check with benchmark timing verification. The score is editorial, not a reach
forecast, and does not certify the unbuilt animation or approve release.
