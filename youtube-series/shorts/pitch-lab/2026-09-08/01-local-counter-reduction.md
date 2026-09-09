Proposed MP4: `cpp-atomic-counter-contention-local-reduction.mp4`

# Proposed Short 8: Stop sharing this counter

One focused script pitch, as requested. Not a twenty-concept search, an
approved recording, or an authorized benchmark. September 8, 2026.

## What this attempts

Make an ordinary thread-safe counter look worth questioning. The position is
that a final-only count should not require every worker to update one shared
atomic after every item. Invite the informed objection: live progress and
coordination can require information before the workers finish.

Continue Short 7's proposed final-totals test, but make this understandable to
a first-time viewer. Short 7 is currently a recording task, not a published
success. This demonstration uses one shared counter (true sharing); Short 7
uses different counters on one cache line (false sharing). Do not conflate them
or present these measurements as a direct rerun of Short 7's padded baseline.

Evidence informing the design:

- Short 4 Instagram's September 7 native capture: approximately 71% retention
  at 3 seconds and 28% near 32 seconds. These are screenshot estimates. Preserve
  its legible before/after comparison; 30 seconds is room for substance, not
  evidence that more seconds improve results.
- Short 5's inspected recording lost roughly one-third of viewers by four
  seconds, then flattened. Preserve code, synchronized annotations, selective
  captions and gestures, but put the action in the first two spoken words.
  Its compiler discussion generated substantive replies, including a thread
  observed with 286 likes and ten replies. That is evidence of participation,
  not proof that controversy caused distribution.
- Short 6 Instagram September 8 capture: 44,265 views, 60 follows, 239 saves
  and 19 comments. Native skip rate was 32%, similar to Short 5's 32.2% in its
  later native capture. Animation and the next-test outro are not proven causes
  of conversion. Preserve the why-question as well as the continuation.
- Short 6's published formatting issue and missing opening subtitle in the
  corrected export mean safe-zone/first-frame checks remain essential.

Sources: [Short 5 media analysis](../../../analytics/reports/2026-09-02-short-05-instagram-retention-and-creative-analysis.md),
[native baseline](../../../analytics/reports/2026-09-07-native-insights-workflow-and-short05-baseline.md),
[comment observations](../../../../docs/logs/analytics-observations.md),
[Short 6 post-publication audit](../../short-06-data-layout/post-publication-2026-09-06.md).
Private native records: `20260907T1628-instagram-short04` and
`20260908T1426-instagram-short06`, under analytics/private/native-insights.
These observations are not matched-age experiments. No fresh data pull or
browser session was run for this pitch.

## Checklist plan

| ID | Specific attempt |
| --- | --- |
| S01 | Challenge the shared atomic counter with "Stop sharing this counter." Expected objection: live progress. Risk: experienced programmers know reductions. |
| S02 | "Stop sharing" supplies the action immediately; the circled counter supplies the target before narration names it. |
| S03 | Frame zero: two workers point to one atomic total, red circle around it, "Slower together?" callout, full opening subtitle and presenter visible. |
| S04 | Only change the frequency/location of count updates, not the item-processing task. |
| S05 | Show workers updating the total immediately, split the count when naming the change, merge after completion. |
| S06 | State final-only output before changing the implementation. Never replace shared atomic increments with racing ordinary increments. |
| S07 | Same items, predicate, worker count, final answer and timed boundaries. Relaxed atomics in baseline; normal optimization in both. |
| S08 | Reveal [BEFORE_MS] and [AFTER_MS] together with [N] and the matching final counts. No invented ratio. |
| S09 | Immediately ask why the counter costs so much. |
| S10 | Follow with live-progress question and proposed next test; cut. Confirm continuation before recording. |
| S11 | Yellow for action/setup, teal for counter/faster; outlined captions outside essential code. |
| S12 | Circle shared update, arrows to local counts, then merge arrow and result pointer. |
| S13 | Point to shared target, separate hands for independent counts, bring hands together for final merge, face viewer for questions. |
| S14 | Target 25-30 seconds with a complete update/merge explanation, no empty reveal delay. Time the actual read later. |
| S15 | Two workers, one active code snippet per shot, four lines maximum; central safe area. |
| S16 | Direct verbs and familiar counting example; no memory-model lecture or machine name. |
| S17 | One filename and canonical >-marked narration; viewport examples are not runnable programs. |
| S18 | Follow the planned Short 7 totals question; distinguish this from padding and Short 5 instruction dependencies. |
| S19 | Candidate subject: C++ atomic counter contention. Supporting: thread-local counting, parallel reduction. Platform copy research remains separate. |
| S20 | No benchmark execution or publication. Production owns timings and final-media checks; audio defaults below. |

## Script

Time ranges are editing targets, not measured playback. The hook/result are
conditional on production supplying a meaningful measured slowdown. Do not
publish a placeholder or preserve the premise against contradictory results.

### 0:00-0:02 | Opening

> Stop sharing this counter.

Frame zero: two worker lanes converge on a single box labeled `atomic total`.
Place a red circle on that box and `Slower together?` above the visual inside
the safe zone. Opening subtitle is already visible near the presenter, not
over the code. Point at the common target. Use a simple diagram and actual
code first; a new clay animation is not necessary for this test.

### 0:02-0:07 | Establish the task

> Both threads update it after every item. But we only need the final total.

Hold a compact `Final total only` label from this point through the change.
Show the repeated update highlighted in this worker-body viewport:

```cpp
for (auto item : chunk) {
  if (matches(item))
    total.fetch_add(1, relaxed);
}
```

Small stable label: `2 threads / optimized build`. `relaxed` is imported with
`using std::memory_order::relaxed;` outside the viewport. Shared total is an
unsigned atomic count. Both threads process disjoint, equal-sized chunks.
Pulses indicate shared updates, not a literal trace or serialized whole jobs.

### 0:07-0:13 | Change where the work happens

> Give each thread its own count, then add them together when the work is done.

Replace the viewport with:

```cpp
uint64_t count = 0;
for (auto item : chunk)
  count += matches(item);
return count;
```

Each worker has its own stack-local count. Two short arrows identify them;
separate your hands. Then show both worker lanes completing before their
results merge into the same total. Bring your hands together. This is a
schematic return to the caller, not a claim that std::thread returns values.
The runnable implementation must safely transfer results and join workers
before reading and merging them.

### 0:13-0:18 | Explain the benefit

> Now the threads aren't updating the same memory over and over.

Keep private updates visible and show only the final values crossing toward
the total. No cache-protocol tour, simulated speed ratio or new terminology.
Point to the removed repeated traffic rather than replaying the entire change.

### 0:18-0:22 | Payoff

> Same items, same answer, [N] times faster.

Show `[BEFORE_MS] ms` and `[AFTER_MS] ms`, both matching final counts and
`[N]x in this test`. Only two timing rows; no full benchmark console. Point to
the lower time. Do not reveal timings before this beat. Include final merging
inside the comparison's timing boundary.

### 0:22-0:30 | Discussion, continuation, cut

> Why does that counter cost so much? What if we need live progress? I'm testing that next.

The why-question is the very next spoken beat after the result. It invites
discussion of contention, atomic operations and possible compiler differences;
it does not pretend the basic sharing mechanism was unexplained. Face the
viewer, then gesture to the final-only label when asking about live progress.
Hold the result and cut immediately on `next`. The proposed follow-up compares
periodic publication with per-item publication under an explicit progress
freshness requirement; it is not a scheduled release.

## Technical and production handoff

- The contract requires an exact total only after both workers finish. No
  intermediate observer, cancellation trigger, ticket allocation or ordering
  dependency uses the count. A progress monitor would change that contract.
- Use a data-dependent predicate over real input, not a loop whose private
  count can become a constant. Same inputs and final totals, ordinary optimized
  builds, no disabled vectorization or volatile to force a desired outcome.
- Baseline uses relaxed atomic updates so this is not merely a demonstration
  of unnecessarily strong ordering. Relaxed operations remain indivisible:
  [C++ draft](https://eel.is/c++draft/atomics.order).
- Production checks optimized code and timing boundaries, supplies repeated
  wall-time results and ratio, includes result transfer/merge in timing, and
  documents allocation/worker-start policy consistently. If optimized local
  counting also vectorizes, report that rather than attributing the entire
  difference exclusively to cache coherence or pretending SIMD was isolated.
- Join before final read/merge. Thread completion synchronizes with successful
  join: [C++ draft](https://eel.is/c++draft/thread.thread.member).
- Do not claim padding fixes this example: workers intentionally update the
  same counter. To fulfil Short 7's exact experimental continuation as well,
  the benchmark owner should include its padded separate-counter baseline;
  do not reuse its measured ratio for this different comparison.
- 2160x3840 universal master, webcam top and visual/code region below per current
  visual guidelines. Check all essential elements within actual platform UI
  safe areas, including the first decoded frame at phone size while muted.
- Captions: opening "Stop sharing" yellow, "counter" teal. Later emphasize
  "final total", "own count", and the measured gain. Avoid coloring every word.
- CapCut +5 dB once across the spoken track, Enhance voice at 75%; verify split
  clips and listen for clipping or processing artifacts. Actual settings,
  captions, gestures, duration and platform crops remain unverified.
- No title/hashtag package, recording schedule, benchmark or analytics pull is
  authorized by this editorial pitch. Keyword candidates are not SEO approval.

## Checklist audit

| ID | Status | Points | Evidence / remaining repair |
| --- | --- | ---: | --- |
| S01 | PARTIAL | 7.5/15 | Strong directive challenges shared counting, but experienced viewers may identify a standard reduction immediately. The practical progress-versus-throughput tradeoff must earn interest beyond novelty. |
| S02 | PASS | 15/15 | "Stop sharing" arrives first; five-word hook has no prerequisite lecture. |
| S03 | PASS | 10/10 | Shared target, circle, short callout and opening caption explicitly present at frame zero. This scores design, not a rendered frame. |
| S04 | PASS | 4/4 | Count updates and final merge are the only demonstrated change. |
| S05 | PASS | 4/4 | Existing updates, split, completed workers and merge follow the spoken actions. |
| S06 | PASS | 10/10 | Final-only contract explicit, race-free result handling, conditional measurements and no universal claim. |
| S07 | PASS | 5/5 | Input/output/worker/build/timing contract and result-owner handoff specified. |
| S08 | PASS | 5/5 | Matching totals plus two measured timings answer the original performance promise. |
| S09 | PASS | 5/5 | Immediate "Why does that counter cost so much?" |
| S10 | PASS | 5/5 | Live progress supplies a genuine next experiment, followed by immediate cut. Commitment remains proposed. |
| S11 | PASS | 3/3 | Selective yellow/teal captions, outline and placement specified. |
| S12 | PASS | 3/3 | Shared circle, split arrows, merge arrow and result pointer span the lesson. |
| S13 | PASS | 2/2 | Target, split, merge and audience-address gestures specified. |
| S14 | PASS | 4/4 | Complete roughly 70-word explanation fits a plausible 25-30-second design; no word cap or dead hold. Final read must confirm pacing. |
| S15 | PASS | 3/3 | One four-line viewport at a time, two worker lanes, two timing rows and central-safe composition. |
| S16 | PASS | 2/2 | Plain counting language, short connected sentences and no machine-name detour. |
| S17 | PASS | 1/1 | One canonical quoted script and descriptive filename; non-runnable fragments labeled. |
| S18 | PASS | 2/2 | Recent records, prior pitch and planned Short 7 examined; causal limits and different sharing mechanisms explicit. |
| S19 | PASS | 1/1 | Accurate candidate search language and separate per-platform publishing research path. |
| S20 | PASS | 1/1 | Explicit production/media/audio/commitment checks; no implied execution or release approval. |

## Critique

The biggest weakness is premise novelty, not length. An experienced C++ viewer
can predict local reduction immediately. The counter is concrete and the
comparison is legible, but that alone does not make it as surprising as Short
5's extra-variable result. A large real effect and recognizable practical
workload would help, but a missing timing is not the reason for this deduction.

The revision already avoids two weaker choices: it does not claim atomics are
universally bad, and it states final-only output before the optimization so
the expected live-progress objection is a real tradeoff rather than a gotcha.
The next editorial repair is to ground the counter in a recognizable task
where developers plausibly keep a shared total, without adding prerequisite
setup. Do not manufacture a bad implementation just to make the comparison win.

This follows through on the counter experiment more convincingly than it opens
a completely new topic. Avoid promising a third counter video unless we want
that sequence; confirm the live-progress continuation before recording.

## Final score

Score: **92.5/100. Decision: rework.** S01 is mandatory and only partial.
The draft is complete, but the premise needs a stronger practical reason to
care before recording. This is an editorial score, not a forecast of views,
and pending benchmark measurements do not reduce it.
