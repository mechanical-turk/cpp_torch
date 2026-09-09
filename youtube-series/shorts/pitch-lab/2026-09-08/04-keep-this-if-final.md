Proposed MP4: `cpp-if-statement-branchless-lookup-performance.mp4`

# Final pitch: Keep this if

September 8, 2026. Focused revision of
[03](03-keep-this-if.md). Earlier drafts and their scores remain unchanged.
This revision addresses its missing optimization motive.

## What this is trying to accomplish

Make a cold C++ viewer question a familiar optimization: replacing a conditional
with arithmetic to avoid branching. Lead with a concrete instruction and its
performance consequence, then show the work the rewrite can introduce.

The intended reaction is "But branches are expensive" or "The compiler can
handle this." Those are useful starting points for discussing skipped loads,
predictability and compiler transformations. We do not claim all branches are
good or that this is the best possible branchless implementation.

Applied lessons:

- Short 5's inspected opening lost roughly one-third of viewers in its first
  four seconds. Keep its code/change/result structure but replace an opening
  technical label with "Keep this if. It's faster."
- Its compiler threads show real participation, not proof that controversy
  caused distribution. Keep the explanation technically defensible when
  viewers inspect the complete experiment.
- Short 6's September 8 Instagram checkpoint: 44,265 views, 60 follows,
  239 saves, 19 comments and 32% native skip rate. Animation, topic, audience,
  duration and crop changed together. Preserve both questions in the ending;
  do not treat its continuation or animation as proven conversion levers.
- Short 6's formatting problems motivate one code view at a time and only two
  representative player paths, replacing revision 02's ten small markers.
- Revision 03 showed the edit without its motive. State the attempt to make
  the loop faster as the code changes, then expose the extra reads. No
  prerequisite lecture or pretend ignorance of the cost.
- The prior lab's branchless idea hid the cost in score(). Use the actual
  array lookup. Both variants retain Short 6-style separated arrays, so the
  new lesson is which accesses happen, not where fields are stored.

Evidence: [Short 5 media review](../../../analytics/reports/2026-09-02-short-05-instagram-retention-and-creative-analysis.md),
[native baseline](../../../analytics/reports/2026-09-07-native-insights-workflow-and-short05-baseline.md),
[comment observations](../../../../docs/logs/analytics-observations.md),
[prior branchless critique](../2026-09-05/19-branchless-does-extra-work.md),
private native record `20260908T1426-instagram-short06`.
No new analytics or browser session was requested or run.

## Checklist plan

| ID | Specific attempt |
| --- | --- |
| S01 | "Keep this if. It's faster." opposes automatic branch removal; compare a plausible conditional-to-arithmetic rewrite rather than a broken loop. |
| S02 | "Keep this if" is an immediate action aimed at visible code; the next two words supply the stakes. No definition before the promise. |
| S03 | Three-line code, circled if, "DELETE IT?" callout, complete opening caption and face all present at frame zero. |
| S04 | Same separated arrays and IDs; conditional versus unconditional score access is the only lesson. |
| S05 | State "I tried removing the check to make the loop faster" at the edit, then show how multiplying by zero still reads the scores. |
| S06 | Valid IDs, 0/1 flags, unsigned totals, exact output equivalence and prospective result claims. Keep the 10% active condition visible from the start. |
| S07 | Same inputs/order/output/build/timing scope, hand off [A]/[B]/[N] and generated-code checks to production. |
| S08 | Show the measured size of the gain and equal totals. The hook already discloses the winner; do not pretend otherwise. |
| S09 | Ask "Why did the shorter version lose?" immediately after the measured payoff. |
| S10 | Ask about everyone being active, name that next test, then cut. Confirm this proposed experiment before recording. |
| S11 | Full opening caption, then synchronized fragments with selective yellow/teal emphasis and dark outlines. |
| S12 | Circle if, mark skipped path, highlight extra read/zero, point at timing winner. |
| S13 | Point, wave past inactive path, swipe away if, indicate extra work and result, then face viewer. |
| S14 | 69 spoken words before result substitution; target 25-30 seconds with a complete mechanism and both ending questions. Time the real read later. |
| S15 | One three-line snippet and at most two short paths, not ten miniature players or two whole files. Keep essential elements centrally placed. |
| S16 | Connected plain sentences; branchless, cache protocol and machine specifications absent from narration. |
| S17 | Filename first, one >-marked script, viewport fragments and edit directions separate. |
| S18 | Apply two earlier critique repairs and recorded Short 5/6 lessons without causal overclaiming. |
| S19 | Candidate primary: C++ if statement performance. Supporting: branchless programming, conditional lookups. Publishing research stays separate. |
| S20 | Explicit conditional measurements, final-frame/audio/crop review and no unauthorized benchmark, release or schedule. |

## Script

Timing is a design estimate. The hook, load illustration and result wording are
prospective until the production owner supplies evidence for this comparison.
No hypothetical ratio may appear in a published video.

### 0:00-0:02 | The position

> Keep this if. It's faster.

Frame zero shows the presenter and the following code, with a red circle around
if. Place `DELETE IT?` above the code and `10% active` below it, within the safe
region. Show the full opening subtitle immediately: yellow emphasis on `Keep`,
teal on `faster`. No second held copy of the spoken hook. Point at if.

```cpp
for (auto id : ids)
  if (active[id])
    sum += scores[id];
```

### 0:02-0:07 | What the check buys us

> We only need the active players' scores, so this check skips everyone else.

Below the code, show two stable paths: `Active -> Read score -> Add` and
`Inactive -> Skip`. Highlight Skip and wave past that path. These illustrate
logical execution, not physical memory traffic or a regular input ordering.

### 0:07-0:12 | The attempted optimization

> I tried removing the check to make the loop faster.

Swipe away the condition as the code changes:

```cpp
for (auto id : ids)
  sum += active[id] * scores[id];
```

Keep the active path unchanged. Replace the inactive path with
`Read score -> x0`. Circle the new score read, not the whole screen. All active
flags are 0 or 1, so active players' scores still contribute unchanged.

### 0:12-0:17 | The consequence

> Multiplying inactive scores by zero keeps the total, but we still read their scores.

Indicate the inactive path, then the identical total. Keep one representative
active/inactive pair; do not introduce cache lines, timings or another chart.
The read illustration requires emitted-code support before production approval.
It does not claim one DRAM transaction per expression or exclude prefetching.

### 0:17-0:22 | The measured payoff

> With one in ten players active, keeping the if was [N] times faster.

Replace code/paths with two large aligned timing rows:

```text
With if       [A] ms
Without if    [B] ms
```

Keep `10% active`, show equal totals and `This test: [N]x`. Point at the smaller
time. [N] is B/A. The opening already promised this direction; this reveals
the size and proof, not a supposedly unknown winner.

### 0:22-0:30 | Discussion and return reason

> Why did the shorter version lose? What if everyone's active? That's my next test.

The why-question is the very next spoken beat after the result. Look toward
the viewer, then gesture to the active-fraction label. Hold the result and cut
immediately on test. The next test changes the fraction of active players
while retaining the same score/ID workload. It is proposed, not scheduled.

## Technical and production handoff

- Both variants compute the same final total over the same IDs, score values,
  0/1 active flags and iteration order. Use unsigned score/total arithmetic
  with appropriate widths and keep all unconditional reads valid. No race,
  invalid score access or throwing conditional-only computation is permitted.
- Use a representative active-player query with a documented 10% active
  population. Do not substitute a costly black-box function, adversarial
  unreported ordering, or a fabricated data layout to make the rewrite lose.
- Keep normal identical optimized builds. No disabled SIMD, volatile or
  suppressed legitimate transformations. Removing a source if does not prove
  an instruction-level branch disappeared: see LLVM's
  [if-conversion documentation](https://llvm.org/docs/Vectorizers.html#if-conversion).
- Production owner checks emitted loads/control flow and supplies repeated
  timings [A], [B] and ratio [N]. Same timer boundaries, include complete loop
  work; document allocation/setup policy and input size. If both compile to
  equivalent behavior, or the claimed comparison is not supported, reject or
  rewrite the result-dependent premise. Do not rescue it by weakening builds.
- We explain a cost that this rewrite introduces. A wall-time difference does
  not isolate all of its hardware causes. SIMD, speculation, cache state and
  prediction remain legitimate discussion topics; don't attribute the entire
  ratio solely to cache misses from timing alone.
- Main argument: avoiding a conditional is not worth arbitrary extra work.
  Deliberate omissions: full branch-prediction mechanism, alternative masked
  operations, detailed compiler cost models and locality sweeps. No assertion
  that this is the optimal branchless strategy or that if is always faster.
- Native vertical master: 2160x3840, current webcam-top/visual-below layout.
  Keep code, callout, paths and results centrally inside platform-safe space;
  reserve right/bottom UI areas. Actual first-frame, complete captions,
  annotations, recurring gestures and 25-30-second delivery need export review.
  Phone-size muted check and actual platform preview remain mandatory.
- Caption fragments follow the spoken clauses, with occasional yellow/teal
  emphasis, outlined text and no overlap with source, result digits or hands.
  Do not display two full source variants simultaneously.
- CapCut +5 dB once across the spoken clips; Enhance voice at 75%. Verify split
  clips, avoid double gain, and listen for clipping and processing artifacts.
  Settings confirmation and final-export quality are unverified until editing.
- Proposed filename/search language is accurate; per-platform description,
  title, hashtag and comment research remains a separate publishing task.
- Creator approval of the script would not authorize benchmark execution,
  publication or a promised schedule. No such actions occurred in this revision.

## Checklist audit

| ID | Status | Points | Evidence in this revision |
| --- | --- | ---: | --- |
| S01 | PASS | 15/15 | "Keep this if. It's faster" challenges branch removal with a specific attempted optimization; activity fraction supplies a genuine counterexample to universal advice. |
| S02 | PASS | 15/15 | First three words give an action and visible target. Faster completes the six-word hook; no unfamiliar branchless label precedes the benefit. |
| S03 | PASS | 10/10 | First-frame code, circle, DELETE IT?, full caption and presenter reinforce one question. Render verification remains separate. |
| S04 | PASS | 4/4 | Both variants use identical arrays; only skipped versus unconditional accesses change. |
| S05 | PASS | 4/4 | The 7-second beat explicitly states the attempted speed optimization, followed by the matching code change and its extra reads. |
| S06 | PASS | 10/10 | 10% active disclosed from frame zero, safe 0/1 unsigned contract, logical rather than physical traffic claims and result-dependent wording identified. |
| S07 | PASS | 5/5 | Inputs/order/output/build/timing scope and production-owned measurements are explicit; no disabled optimizations. |
| S08 | PASS | 5/5 | Two timed rows, equal totals and test-scoped ratio resolve the opening; only magnitude remains unrevealed until the payoff. |
| S09 | PASS | 5/5 | "Why did the shorter version lose?" immediately follows the measured gain. |
| S10 | PASS | 5/5 | All-active workload is a concrete one-variable next test; immediate cut and confirmation of the proposed commitment. |
| S11 | PASS | 3/3 | Selective yellow/teal outlined captions, synchronized and kept clear of code/results/gestures. |
| S12 | PASS | 3/3 | Circle, skipped path, extra-read marker and timing pointer span every substantive stage. |
| S13 | PASS | 2/2 | Point, wave, swipe, indicate reads/result, then address viewer. |
| S14 | PASS | 4/4 | 69 words before result substitution deliver the premise, motive, mechanism, measured payoff and both questions within a plausible 25-30-second design. Actual timed read/export remains required. |
| S15 | PASS | 3/3 | One short viewport, two stable paths and two large result rows replace dense comparisons. Layout execution remains a final-media check. |
| S16 | PASS | 2/2 | The new motive links naturally to the consequence; no jargon-first opening, fake setup or machine details. |
| S17 | PASS | 1/1 | Descriptive filename, one canonical >-marked script and clearly separated viewport/production notes. |
| S18 | PASS | 2/2 | Applies recorded opening/discussion lessons and two specific previous critiques; no new performance or conversion claims. |
| S19 | PASS | 1/1 | Accurate candidate search terms and separate platform publishing research; this is not metadata approval. |
| S20 | PASS | 1/1 | Production-owned proof, final first-frame/duration/crop/motion/audio gates and authority limits explicit. |

## Critique

### First review: does it repair the actual failures?

- Opening: the code supplies the target, "Keep" supplies the position, and
  "faster" supplies the stakes. We no longer require viewers to understand
  branchless before caring.
- Motivation: the rewrite is explicitly an attempt to improve speed. Viewers
  see its arithmetic at the same moment, then learn what work remains. This
  fixes revision 03's arbitrary-looking detour.
- Visual burden: two representative paths communicate the difference without
  ten tiny objects, two simultaneous files or a cache-protocol lesson.
- Ending: the original performance promise is fulfilled; the why-question
  precedes a concrete adjacent experiment. No follow request displaces debate.

### Second review: challenge the premise, not just the wording

1. **Is this an intentionally bad example?** It is a familiar conditional-to-
   arithmetic rewrite applied to a lookup whose load can be avoided. Both
   versions preserve the same meaningful result. The extra loads are openly
   shown, not concealed in a fake expensive function. This is one failed
   optimization candidate, not a claim about the best branchless algorithm.
2. **Does the spoken claim exceed its evidence?** The outcome is explicitly
   prospective until the measurement owner supplies it. The active fraction
   is visible and spoken, and the ratio belongs to this test. No speedup,
   instruction behavior or hardware attribution has been fabricated.
3. **Does the beginning spoil the ending?** It reveals the direction, which
   is intentional. The Short earns attention by showing how the rewrite loses
   and finally how much. There is no false "guess the winner" suspense.
4. **Are we pretending not to understand the result?** We explain the extra
   work and ask viewers why that cost wins over the intended optimization.
   The next test changes the frequency of skipped work. Both questions have
   legitimate technical substance.
5. **Is this just Short 6 again?** The physical arrays remain fixed. This
   time a control-flow rewrite changes which scores are accessed. That is a
   distinct lesson with a different compiler/predictability discussion.

**Biggest residual risk:** production may show that normal optimization removes
the contrast, or that the effect is uninteresting for the representative
workload. The script must follow those findings. That is a production proof
risk, not an unresolved script defect or grounds to invent a number. Expert
familiarity is also possible; this review does not predict novelty for every
viewer or claim that discussion guarantees distribution.

## Final score

Score: **100/100. Decision: advance to technical validation.**

All 20 script-design checks pass under the existing weighted rubric. This is
not a claim of perfect creative quality, proven engagement, verified timings,
measured narration duration, creator approval or upload readiness. The goal of
a pitch that passes critique is met; benchmark/production work is a separate
authorization and gate.
