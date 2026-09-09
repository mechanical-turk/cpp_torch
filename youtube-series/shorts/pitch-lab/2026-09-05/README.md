# Twenty Shorts pitch-and-critique rounds

Created September 5, 2026. Internal creative development, not approved platform
copy or a release schedule. The goal is twenty different best-effort pitches,
each followed by a critical review and a lesson applied to later rounds.
No candidate is called perfect or assigned a predicted view count.
The [completion audit](completion-audit.md) records the scope checked and the
production work that remains deliberately unclaimed.

## How to read the exercise

Each numbered file preserves the writer's pitch, then the analyst's itemized
critique, decision, and learning. Later rounds name the lesson they inherit.
The running [learning log](../../../../docs/logs/short-pitch-lab-2026-09-05.md)
records the sequence. The [short-form playbook](../../../production/short-form-playbook.md)
contains the resulting editorial checks so future scripting reads them.

All scripts are prospective narration. A line describing a measurement can
only be recorded after the stated technical gate produces that result. No
benchmark, frame, audience reaction, or exported runtime was fabricated.
Every concept targets an 18-19-second edit, but elapsed runtime and visual
quality remain UNVERIFIED until the final export passes the existing upload gate.

## Shared production contract

- Every opening starts with speech, a readable visual, a short text callout,
  selective yellow/teal caption emphasis, and an annotation present on frame one.
- Each pitch specifies changing annotations and purposeful presenter movement
  through its explanation and payoff. These are plans, not evidence of execution.
- Keep each code shot within 14 preferred / 17 maximum visible lines. Use the
  current safe-area layout, not a miniature side-by-side full-file comparison.
- Finish the original promise, ask a specific adjacent question, name the next
  concrete test, and cut. Proposed continuations are not publishing commitments.
- Search phrases are candidate topic labels only. Platform search, keywords,
  hashtags, descriptions, covers, and release readiness require separate audits.

## Evidence and evaluation

Read [evidence.md](evidence.md). Each critique distinguishes owned-account
observations, creative inference, and missing technical evidence. These twenty
reviews are not twenty audience experiments. Editorial selection will consider
opening clarity, demonstration burden, credible disagreement, useful payoff,
and production cost, without invented numerical scores.

## Round index

Read in sequence to see how each critique changes the next pitch. These are
twenty distinct concepts, not twenty wording variants.

| Round | Pitch and critique | Spoken words |
| --- | --- | ---: |
| 01 | [These brackets change the answer](01-brackets-change-the-answer.md) | 49 |
| 02 | [I deleted eight bytes without deleting a field](02-delete-bytes-without-deleting-fields.md) | 50 |
| 03 | [Empty space made these threads faster](03-empty-space-faster-threads.md) | 46 |
| 04 | [This move adds work](04-move-adds-work.md) | 44 |
| 05 | [Reserving memory made this loop slower](05-reserve-inside-the-loop.md) | 49 |
| 06 | [Sorting made this loop faster](06-sorting-speeds-up-the-scan.md) | 48 |
| 07 | [This copy changes the original](07-copy-that-changes-the-original.md) | 49 |
| 08 | [This lookup keeps growing the map](08-lookup-grows-the-map.md) | 50 |
| 09 | [One missing character copies every object](09-missing-reference-copies-objects.md) | 50 |
| 10 | [These unused fields are slowing the loop](10-unused-fields-slow-the-loop.md) | 48 |
| 11 | [Replacing endl made this logger faster](11-endl-flushes-the-logger.md) | 48 |
| 12 | [This promise stops the copies](12-noexcept-removes-copies.md) | 46 |
| 13 | [This const view changes under your feet](13-const-view-changing-text.md) | 47 |
| 14 | [Negative one is greater than one here](14-negative-one-greater-than-one.md) | 44 |
| 15 | [These parallel jobs run one at a time](15-async-jobs-run-in-line.md) | 50 |
| 16 | [Copying this pointer updates a shared counter](16-shared-pointer-hidden-counter.md) | 49 |
| 17 | [Checking every number beat binary search](17-linear-scan-beats-binary-search.md) | 47 |
| 18 | [This billion-iteration loop never runs](18-benchmark-loop-never-runs.md) | 49 |
| 19 | [Removing this if made the loop slower](19-branchless-does-extra-work.md) | 47 |
| 20 | [The compiler split this loop for me](20-compiler-splits-the-sum.md) | 48 |

Counts cover the draft narration only. Code tokens can take longer to speak
than their word count suggests. None of these counts verifies runtime.

## Selection after the twenty rounds

This is an editorial shortlist, not a forecast of views or followers.

1. **Best new performance experiment: [10, unused fields](10-unused-fields-slow-the-loop.md).**
   A visible target, a consequential claim, and a real tradeoff when the access
   pattern changes. First action: build the fair layout comparison and inspect
   the code. Drop the speed claim if measurement does not support it.
2. **Best response to an actual audience objection: [20, compiler splits the sum](20-compiler-splits-the-sum.md).**
   Directly addresses the compiler discussion, with an inexpensive assembly
   check. Main risk: familiar to commenters and visually too similar to Short 5.
3. **Best compact behavioral surprise: [15, serialized async jobs](15-async-jobs-run-in-line.md).**
   The timeline makes the claim concrete before source-level explanation.
   Main risk: concurrency introduces a new topic and extra lifetime concepts.
4. **Fastest layout fallback: [02, field order](02-delete-bytes-without-deleting-fields.md).**
   Easy to verify and visualize. Main risk: the eight-byte saving can seem
   insignificant without a useful repeated-object context.
5. **Fastest code-edit fallback: [09, range-loop copies](09-missing-reference-copies-objects.md).**
   Familiar code and a one-character edit. Main risk: copied objects are already
   familiar to many C++ viewers, and instrumentation can affect optimization.

Round 17 remains a deferred benchmark candidate. Rounds 03 and 19 need stronger
measurement work. The remaining ideas are reserves or require the concept
repair named in their critiques. No episode number or release date is assigned.

## What changed in the playbook

Every round added its lesson before the next pitch. The final editorial pass
consolidated those twenty additions into ten checks, avoiding a second ledger
inside the playbook. The original lessons remain intact in the round files and
append-only log.

| Playbook check | Lessons preserved |
| --- | --- |
| Concrete opening and meaningful stakes | P01, P02, P15 |
| Prerequisite burden and novelty | P12, P13 |
| Substantive disagreement | P05, P07, P11 |
| Evidence matches the headline | P03, P04 |
| Fair task and cost boundaries | P06, P08, P10 |
| Instrumentation, generated code, and repairs | P09, P18, P19 |
| Honest reveal and current payoff | P14, P16 |
| Production readiness | P17 |
| Audience relevance beyond existing threads | P20 |
| Critique-to-test discipline | Synthesis of the twenty reviews, not a new measured lesson |

## What to measure after selection

- Review the final first frame silently at phone size, then the first three
  seconds with sound. A draft layout does not pass the upload gate.
- Use the same edit treatment where practical. Record differences in topic,
  hook, length, annotations and presentation rather than attributing every
  change in results to a single creative choice.
- Compare Instagram at matched ages: early retention, completion, shares,
  saves, audience comments and thread depth, profile visits, and follows.
  Use reached accounts for per-person rates where available, not plays as if
  they were unique people. Separate creator replies from audience participation.
- Use YouTube's own Shorts-feed exposure, stayed-to-watch and engaged viewing
  metrics separately. Low distribution is not by itself proof of a poor hook.
- Read what viewers argue about. Competent tradeoff discussion is more useful
  evidence for this strategy than a pile of corrections about a broken test.
- A result can reject the premise. Do not keep tuning the benchmark until the
  prewritten winner appears.
