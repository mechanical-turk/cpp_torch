Proposed MP4: `cpp-async-future-destructor-blocking-short.mp4`

# This semicolon blocks your thread

## What this pitch is trying to accomplish

Make a familiar punctuation mark carry a surprising, consequential C++ claim.
Challenge the assumption that launching two asynchronous jobs means they can
overlap. Show an actual serialization trap, fix it with two retained futures,
and invite discussion about why destruction waits. This is a concurrency topic
expansion, not another cache-layout or accumulator lesson.

Apply the [Short 5 analysis](../../../analytics/reports/2026-09-02-short-05-instagram-retention-and-creative-analysis.md):
its complete opening promise took about 3.7 seconds, while the small code
change, synchronized annotations and technical question supported an engaging
demonstration. Those elements co-occurred; their causal effects are unknown.
The September 8 native Short 6 record still shows a 32% skip rate, so a successful
middle does not mean our opening is solved. Its continuation outro is a useful
test, not proven to cause follows. No long-form evidence informs this pitch.

Revision of the [September 5 internal async candidate](../2026-09-05/15-async-jobs-run-in-line.md):
replace the generic parallel-jobs opening with one visible semicolon, drop the
19-second compression, and add the missing immediate why-question. Keep the
real execution trace, explicit launch policy and small-job thread-pool follow-up.
These are sequential editorial reviews, not independent reviewers.

## Checklist plan

| ID | Specific attempt and risk |
| --- | --- |
| S01 | A semicolon blocks the caller despite explicit async launch. Expected objection: keep the futures; waiting protects lifetimes. The claim concerns this code, not every semicolon. |
| S02 | Open with “This semicolon blocks your thread.” The circled semicolon makes the subject visible before its name is finished. |
| S03 | Frame zero: two async calls, red circle on the first semicolon, caption with SEMICOLON yellow and BLOCKS teal, compact “ASYNC?” callout, presenter already pointing. |
| S04 | One lifetime trap and one repair. Future/destructor vocabulary is a real comprehension risk; show its meaning rather than adding a definition passage. |
| S05 | Immediately show job B waiting for A, explain the discarded return object at that exact statement, then retain it. |
| S06 | Explicit launch::async stays visible. Restrict the claim to the returned futures shown; no guarantee of simultaneous execution on physical cores. |
| S07 | Same independent jobs and completed outputs; discarded versus retained futures. Production supplies actual start/end events. |
| S08 | Reveal the second trace with actual overlapping job intervals; the claim promises overlap, not a fabricated speedup. |
| S09 | Immediately ask why discarding a result makes the caller wait. This asks about the design behind the demonstrated behavior. |
| S10 | Ask whether a thread pool handles small jobs better, identify it as the proposed next test, cut immediately. |
| S11 | Short synchronized caption phrases, yellow/teal emphasis only on semicolon, blocks, waits and overlap. |
| S12 | Circle statement end, point to the discarded future, highlight retained names, bracket the overlap. |
| S13 | Point at opening; sequential hand beats for A/B; hold two fingers for retained handles; spread hands at overlap; address camera for questions. |
| S14 | Budget 27-30 seconds for a complete cause, repair and observed outcome. Timed creator read remains a production check. |
| S15 | Two source lines before, four after. Only one timeline pair visible at once; code setup off camera. |
| S16 | Concrete verbs: launch, finish, discard, keep, wait. No greeting, machine specs, hype or jargon preface. |
| S17 | Filename above; one canonical narration below. Scene fragments are not a complete benchmark. |
| S18 | Applies Short 5 opening lesson and Short 6 evidence limits; revives an unproduced concurrency candidate rather than repeating published loop lessons. |
| S19 | Primary candidate: C++ std::async. Supporting: future destructor, blocking, asynchronous tasks, concurrency. Platform search/hashtag research belongs to publishing. |
| S20 | Explicit trace, safe-zone, duration, annotations, presenter and audio checks below. No release or benchmark execution authorized. |

## Script

### 0-3 seconds: the trap

Current layout: 2160x3840 master, webcam in the top 2160x1488 region; code and
trace in the lower region. Keep essential material central, clear of platform
controls. The complete opening caption, “ASYNC?” callout and red circle are
visible on frame zero. Do not fade them in. Point to the first semicolon.

```cpp
async(launch::async, job_a);
async(launch::async, job_b);
```

> This semicolon blocks your thread.

### 3-9 seconds: show the consequence

Show the recorded A interval, then B beginning after A ends. Keep the code
above the trace. Sequential hand beats match the two jobs. Do not imply that
these lanes represent hardware cores.

> These calls launch two jobs, but the first must finish before we even launch the second.

### 9-14 seconds: connect the wait to the code

A small `future` return-object label appears beside the first call, then
disappears at the circled semicolon. Point to that boundary; do not introduce
a separate diagram or replay the whole trace.

> We're discarding the future, so its destructor waits right here.

### 14-20 seconds: retain the results

Highlight `auto a` and `auto b` as the existing calls gain names. Then reveal
the two get calls. Both launches remain above both waits. Use two fingers to
mark the retained handles.

```cpp
auto a = async(launch::async, job_a);
auto b = async(launch::async, job_b);
a.get();
b.get();
```

> Keep both futures, then wait after launching both jobs.

### 20-23 seconds: complete the payoff

Replace the old trace with the recorded retained-future trace. Bracket the
actual overlapping region and spread both hands. Use visible start/end events,
not a schematic presented as measured execution. Retain this frame to the cut.

> Now they overlap.

### 23-30 seconds: discussion and continuation

Look at the camera, then use a small pinching gesture on “small jobs.” No
additional explanatory sentence between the payoff and the first question.

> Why should discarding a result make you wait?
>
> Would a thread pool handle small jobs better? That's what I'm testing next.

Cut immediately. The continuation is a proposed experiment, not an approved
release schedule or an already measured answer.

## Production and correctness handoff

- The [C++ working draft, async synchronization rules](https://eel.is/c++draft/futures.async#4)
  support the trap: releasing the last associated state can require completion
  of the explicitly asynchronous task. Here each discarded temporary ends at
  its statement boundary. This is not a claim that every future destructor
  blocks. Preserve explicit launch::async; the default policy changes the setup.
- Use two meaningful independent jobs and retain valid captured lifetimes.
  Record starts/ends with steady_clock into separate per-job storage; report
  after completion without a racy shared logger. Compare identical completed
  work and outputs. Include both get calls in the retained version's interval.
- Do not use a two-job start barrier: the discarded-future version cannot launch
  B until A finishes, so that barrier would deadlock. Do not disable compiler
  optimizations. Ordinary warnings about discarded futures are valid, not a
  reason to suppress diagnostics or pretend this is recommended usage.
- Actual overlap must be demonstrated before recording “Now they overlap.”
  Overlapping task lifetimes do not prove simultaneous physical-core execution.
  No numerical speedup is promised. Any later timing overlay requires supplied
  measurements; do not invent one to make the pitch look complete.
- Proposed next experiment: the same batch of small independent jobs through
  explicit async launches versus a fixed worker pool, with completed outputs
  and an explicit treatment of pool construction cost. Not implemented here.
- Targeted using declarations stay off camera. Put eventual camera snippets in
  the code workspace scenes directory; keep the runnable harness separate.
- Check the first decoded frame muted at phone size, all recurring annotations,
  gestures across the complete edit, and a natural timed read. Target 25-30s;
  verify exported duration with ffprobe. Do not accelerate a confusing read.
- Preview the universal master in all three real upload interfaces. A source
  canvas does not establish crop safety. Final media checks remain UNVERIFIED.
- CapCut: +5 dB once, Enhance voice intensity 75%, confirm throughout split clips,
  listen for clipping/distortion/artifacts. Record settings evidence rather than
  infer them from audio metadata. Do not approve an unheard export.
- SEO terms above are candidates, not per-platform approval. Publishing later
  needs independent search records, copy, cover, first comment, related video
  and release information. No hashtag set or publication claim is supplied here.

## Checklist audit

| ID | Status | Evidence and remaining action | Points |
| --- | --- | --- | ---: |
| S01 | PASS | Async syntax versus the circled blocking statement is a substantive surprise; lifetime-safety objection is understood. | 15 |
| S02 | PASS | Semicolon is the first named object; visible circle and BLOCKS caption establish stakes on frame zero. | 15 |
| S03 | PASS | Specific code, full opening caption, callout, sticker and pointing gesture share one target. Render still needs review. | 10 |
| S04 | PARTIAL | One repair, but future plus destructor are two terms a beginner may not know. Return-object label limits this; a cold read should decide whether “destroying it” is clearer. | 2 |
| S05 | PASS | A-before-B trace precedes explanation; discarded object maps to boundary; names appear with “Keep.” | 4 |
| S06 | PASS | Explicit policy and scoped claim; correctness handoff rules out all-futures and physical-parallelism generalizations. | 10 |
| S07 | PASS | Identical independent work, both outputs completed, actual event trace, no disabled optimization or barrier trap. | 5 |
| S08 | PASS | Changed trace resolves overlap promise before questions; no nonexistent speed ratio. | 5 |
| S09 | PASS | First line after “Now they overlap” directly questions the blocking behavior's design. | 5 |
| S10 | PASS | Small-job pool comparison is concrete and adjacent; final word leads directly to cut. | 5 |
| S11 | PASS | Selective emphasis, synchronized phrases and no competing caption block specified. | 3 |
| S12 | PASS | Semicolon, returned object, saved handles and overlap each receive a targeted annotation. | 3 |
| S13 | PASS | Point, sequential beats, two fingers, spread hands and closing gesture assigned across stages. | 2 |
| S14 | PASS | Complete mechanism and repair with a 30-second beat budget; real delivery/ffprobe checks explicitly pending. | 4 |
| S15 | PASS | Two/four source lines, stable paired trace, no setup code or core labels. | 3 |
| S16 | PASS | Active sentences, no artificial conversational setup; new terms attach to visible code. | 2 |
| S17 | PASS | Descriptive MP4 filename and one blockquoted recording draft with separate directions. | 1 |
| S18 | PASS | Existing async critique repaired; owned Shorts evidence applied with causal limits and novelty caveat. | 2 |
| S19 | PASS | Exact subject and supporting search candidates identified; platform research explicitly not approved. | 1 |
| S20 | PASS | Concrete proof, four export checks, audio settings and copy handoff; no unrequested execution. | 1 |

## Critique

The hook is stronger than the earlier “parallel jobs” wording because the
viewer has one precise object to inspect. It also earns a useful argument:
whether a destructor should wait, rather than an argument about concealed
compiler flags. The fix is visible and the result is complete.

The remaining weakness is prerequisite load. “Future” and “destructor” will
cost some non-C++ viewers. The returning/disappearing object makes them usable
in context, but that does not eliminate the cost. Keep this as a C++ audience
pitch, not a general coding promise. A cold read should test replacing “its
destructor” with “destroying it”; do not add a separate definitions passage.

Second review: the discarded return value is a real API trap, not an invented
logic error. Still, do not frame the baseline as good practice or mock the
viewer for knowing the fix. The why-question opens the design rationale after
the mechanics are explained. The concrete small-job pool test supplies a reason
to return without postponing this video's answer. Concurrency audience demand
and rendered pacing remain unknown; this score cannot forecast reach.

**Score: 98/100. Decision: advance.** All mandatory script checks pass; S04
retains a named comprehension risk. Editorial selection only, not recording
or upload approval.
