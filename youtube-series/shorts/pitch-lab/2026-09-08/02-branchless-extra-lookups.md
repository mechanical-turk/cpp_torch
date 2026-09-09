Proposed MP4: `cpp-branchless-code-conditional-memory-lookups.mp4`

# One-script pitch: Branchless made this slower

September 8, 2026. Internal pitch, not measured results or recording approval.

## Objective and evidence

Challenge the belief that removing branches is automatically an optimization.
Show one familiar conditional, one small rewrite, the extra memory accesses it
can introduce, and a measured result. Invite competent disagreement about
compiler transformations, SIMD, predictability and active-player frequency.

Apply Short 5's tiny-edit/annotated-code/payoff pattern while shortening the
spoken hook. Its inspected opening lost roughly one-third of viewers by four
seconds. Compiler discussions were substantial, but their contribution to
distribution was not isolated. Preserve the why-question and then add a
specific continuation rather than replace discussion with a follow request.

Short 6's September 8 Instagram capture showed 44,265 views, 60 follows,
239 saves and 19 comments, with 32% native skip rate. Its topic, runtime,
audience and crop changed alongside animation and the continuation outro.
Do not claim those two treatments improved follows or caused the lower
discussion count. Its formatting issue motivates one short code view at a time.

Sources: [Short 5 media analysis](../../../analytics/reports/2026-09-02-short-05-instagram-retention-and-creative-analysis.md),
[native baseline](../../../analytics/reports/2026-09-07-native-insights-workflow-and-short05-baseline.md),
[comment observations](../../../../docs/logs/analytics-observations.md), private
native record `20260908T1426-instagram-short06`.

Refines [prior branchless candidate](../2026-09-05/19-branchless-does-extra-work.md):
replace an opaque costly score() function with a visible score-array lookup.
Same broad player setting as Short 6, but both variants use the same separated
score array; this is conditional access, not another struct-layout comparison.

## Checklist plan

| ID | Attempt / risk |
| --- | --- |
| S01 | "Branchless made this slower" challenges automatic branch removal; likely objection: unnecessary lookups are an unfair rewrite. Show that work rather than hide it. |
| S02 | First word names the disputed optimization; four-word hook completes the contradiction quickly. Some viewers will not know branchless. |
| S03 | One if block, red circle on if, "Remove the if?" callout and full opening caption at frame zero. |
| S04 | Same score array and selected IDs; only conditional versus unconditional lookup changes. |
| S05 | Show nine skipped lookups, delete if, reveal the same nine now loaded and discarded. |
| S06 | Fixed 0/1 flags, unsigned arithmetic, valid IDs and defined reads; conditional result claim. No general anti-branchless rule. |
| S07 | Same dataset, order, outputs, optimization and timing boundaries; production inspects generated code. |
| S08 | Matching totals and two timings reveal [N] with no universal speedup claim. |
| S09 | Immediately ask why keeping the branch won. |
| S10 | Increase active-player fraction next; no follow plea or artificial unresolved original promise. |
| S11 | Yellow setup, teal slower/faster, outlined synchronized captions outside code. |
| S12 | Circle if, arrows skipping grey records, markers on discarded loads, result pointer. |
| S13 | Point to if, wave past inactive players, swipe away condition, point to result, face viewer. |
| S14 | Approximately 75 words; target 25-30 seconds with time to understand the discarded loads. |
| S15 | Two- or three-line code view, ten small record markers but only one explanatory label; central phone-safe composition. |
| S16 | Plain active-player example; introduce no branch-predictor lecture. |
| S17 | One filename, one > script and separate non-runnable viewport fragments. |
| S18 | Prior round's hidden-cost critique applied; Short 5 and 6 evidence scoped by platform. |
| S19 | Candidate phrase: C++ branchless programming; supporting: conditional memory access, compiler optimization. Publishing research separate. |
| S20 | Explicit measurement, assembly, caption, gesture, safe-zone and audio handoff; no work executed by pitching. |

## Script

Timecodes are intended beats, not measured duration. Result-dependent wording
is prospective until production supplies the measurements and emitted-code
evidence. Do not force a winner if the experiment disagrees.

### 0:00-0:02 | First frame

> Branchless made this slower.

Show one viewport with if circled in red and `Remove the if?` above it.
The full opening caption is already present, with `slower` teal. Point at if.
No greeting or delayed fade-in.

```cpp
for (auto id : ids)
  if (active[id])
    sum += scores[id];
```

### 0:02-0:07 | Show the skipped work

> Only one in ten players is active. This if skips the other nine score lookups.

Ten small player markers: one colored, nine grey. Show access to active flags
for all, but only an active player's score is loaded. Wave past the grey ones.
The 10% active label stays visible. Both arrays and all records still exist.

### 0:07-0:12 | Make the edit

> Remove it, and multiply inactive scores by zero instead.

Swipe away if as this viewport replaces it:

```cpp
for (auto id : ids)
  sum += active[id] * scores[id];
```

All flags are 0 or 1. Use unsigned score and total types in the runnable code.
The visible loop is a viewport, not a complete compilable program.

### 0:12-0:17 | Show its consequence

> Now we fetch every score, even when we throw it away.

Highlight the extra score accesses and dim their zero contributions. Keep all
players stationary and data layout identical. This represents actual emitted
loads only if production establishes them, not a source-syntax assumption.

### 0:17-0:22 | Reveal

> Same players, same total. Keeping the if was [N] times faster.

Reveal `With if: [A] ms` and `Without if: [B] ms`, matching totals and
`This test: 10% active`. Point to the winning time; no full console table.

### 0:22-0:30 | Discussion and continuation

> Why did keeping the branch win here? What happens when everyone's active? That's my next test.

The why-question follows the result with no intervening explanation. Face the
viewer, then indicate the active-fraction label. Hold the result and cut on
test. Confirm the proposed activity-rate experiment before promising it in
the recording. No schedule or measured follow-up result is implied.

## Production handoff

- Same valid IDs, active flags, score array, order and exact final total. All
  unconditional loads must be legal even for inactive IDs. No data races,
  invalid accesses, volatile, disabled vectorization or fabricated slow kernel.
- Use a plausible active-player query and record dataset size/order/locality.
  Do not cherry-pick until the desired headline appears. This is one workload,
  not a claim that branchless programming generally loses.
- Normal identical compiler optimizations. Inspect emitted branches and loads:
  removing an if in C++ does not establish machine code is branchless. LLVM's
  loop vectorizer supports if-conversion:
  [LLVM documentation](https://llvm.org/docs/Vectorizers.html#if-conversion).
  If both variants become equivalent, this demonstration does not support the
  headline. Do not suppress legitimate transformations to rescue it.
- Measurement owner supplies [A], [B], [N], repeated timings and comparison
  conditions. Include all query-loop work in the same timing boundary. Do not
  attribute the whole time difference to one hardware cause without evidence.
- 2160x3840 master; current webcam-top, code-below layout. One snippet at a
  time. Test frame zero muted at phone scale in platform safe zones, not only
  in the editor. Keep annotations and hand movements through result/ending.
- CapCut spoken track +5 dB once and Enhance voice intensity 75%, including
  split clips. Listen for clipping/processing artifacts. Final duration,
  readability, captions, audio and real-platform crops remain unverified.
- Public captions, tags, hashtags and title need separate platform research.
  No benchmark, media generation, analytics pull or publication authorized.

## Checklist audit

| ID | Status | Points | Evidence / repair |
| --- | --- | ---: | --- |
| S01 | PASS | 15/15 | Concrete anti-automatic-branch-removal stance, visible cost and a real acceptance-rate tradeoff. |
| S02 | PARTIAL | 7.5/15 | Four words deliver the contradiction, but branchless requires C++ audience knowledge. Test whether the if/callout resolves it immediately. |
| S03 | PASS | 10/10 | One visible condition, target circle, short callout and opening caption specified together. |
| S04 | PASS | 4/4 | Identical storage, only lookup execution changes. |
| S05 | PASS | 4/4 | Skip, remove, load/discard and result follow the narration. |
| S06 | PASS | 10/10 | Safe input contract, scoped result, code-generation conditions and explicit placeholders. |
| S07 | PASS | 5/5 | Same inputs/order/output/build; measurement ownership and no hidden compiler restrictions. |
| S08 | PASS | 5/5 | Two timings plus same final total resolve the promise before the next question. |
| S09 | PASS | 5/5 | Immediate question about why the branch won. |
| S10 | PASS | 5/5 | Change active fraction next, then cut; no new result claimed. |
| S11 | PASS | 3/3 | Selective captions and defined non-overlapping placement. |
| S12 | PASS | 3/3 | Targets across condition, rejected players, discarded loads and result. |
| S13 | PASS | 2/2 | Point, wave, swipe and address viewer mapped to beats. |
| S14 | PASS | 4/4 | Complete approximately 75-word explanation and result fit a plausible 25-30-second read; final pacing separate. |
| S15 | PASS | 3/3 | One short snippet and fixed small marker sequence; no side-by-side files. |
| S16 | PASS | 2/2 | Plain connected narration after the technical opening; terminology risk scored under S02. |
| S17 | PASS | 1/1 | Filename and canonical narration/viewport separation present. |
| S18 | PASS | 2/2 | Earlier hidden-kernel problem repaired; evidence not treated as causal proof. |
| S19 | PASS | 1/1 | Accurate keyword candidates, separate publishing research, no invented tags. |
| S20 | PASS | 1/1 | Full technical and final-media/audio handoff; no implied release readiness. |

## Critique

Stronger than the shared-counter pitch on disagreement: removing branches is
a familiar optimization goal and the visible result challenges it directly.
The lookup example fixes the earlier round's opaque costly score() function.

The main weakness is the opening word. Branchless is immediate for experienced
C++ viewers but may mean nothing to a cold viewer. The if and callout help,
but the opening is not yet universally clear. Refine or test that first frame
before committing recording; do not simply add a longer definition.

The fairness objection remains useful and real. Multiplying by zero visibly
does more potential work. Present this as a plausible failed rewrite, not the
best branchless implementation or proof that branches always win. The compiler
can erase the intended contrast; if it does, accept the result rather than
disable optimizations. Pending measurements themselves do not reduce scoring.

## Final score

Score: **92.5/100. Decision: rework.** S02 is mandatory and partial.
This is a concept/script judgment, not a performance or reach forecast.
