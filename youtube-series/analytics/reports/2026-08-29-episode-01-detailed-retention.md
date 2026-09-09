# Episode 1 Detailed Retention Analysis

Captured: 2026-08-29

Source:
`youtube-series/chapter-01/Audience retention 2026-08-12_2026-08-29 Building a Tensor from Scratch in C++ _ Deep Learning, All the Way Down #1`

Episode duration: 37:11

The export divides the video into one-percent buckets, so each point represents
approximately 22.3 seconds. The percentages also move mostly in increments of
about 0.35 percentage points, which implies a denominator near 288 views. Late
movements of a few points can therefore represent only a handful of viewers and
must be treated as directional evidence.

## Main finding

The opening is the dominant failure.

| Position | Approximate time | Absolute retention |
|---:|---:|---:|
| 0% | 0:00 | 52.78% |
| 1% | 0:22 | 26.39% |
| 2% | 0:45 | 18.40% |
| 3% | 1:07 | 15.97% |
| 7% | 2:36 | 12.85% |

The audience at 0:22 is half the size of the first bucket. By 0:45, only about
35% of the first-bucket audience remains. The video does not begin its
episode-specific tensor subject until approximately 2:37, after most measured
viewers have already left.

The spoken opening explains the series, the intended audience, PyTorch's
abstractions, and the production process. It does not yet solve a tensor
problem. This directly supports removing broad series introductions and
beginning with the episode's concrete problem or result.

## The technical depth is not the primary problem

After the opening collapse, retention does not continue falling at the same
rate. A smaller core audience remains in roughly the 8% to 16% range through
much of the first half. Several concrete sections also produce visible rises.

| Chapter or moment | Time | Nearby retention | Reading |
|---|---:|---:|---|
| Define the first tensor | 5:44 | 14.58% | Attention rises as code begins |
| Constructor and invariants | 8:03 | 12.85% | Concrete implementation attracts navigation |
| Testing with assertions | 17:30 | 10.07% | Another chapter-start rise |
| Implement tensor indexing | 27:29 | 6.94%, then 12.15% | Strongest late attention cluster |
| Unsigned reverse-loop failure | 29:17 | 8.68%, with nearby peaks | Observable C++ failure attracts seeking or replay |
| Validate coordinates | 32:20 | 6.25% | Smaller late technical audience remains |

The strongest late cluster occurs around 27:53 to 29:00, where the lesson
implements reverse indexing, exposes the unsigned-loop problem, and starts
debugging it. Retention rises from roughly 5% to 12%. The data cannot prove
whether this came from chapter clicks, seeking, or replay, but all three imply
that viewers considered this section worth finding or revisiting.

This argues for preserving the rigor while changing the order:

1. Start with the exact technical problem.
2. Reach code or an observable result immediately.
3. Introduce theory only when it explains the next line or failure.
4. Use concrete bugs, contradictions, and debugging moments as structural
   anchors.

## Cold viewers and committed viewers behave differently

The subscriber split is noisy because the inferred subscribed sample is only
about 40 views, compared with roughly 248 non-subscribed views. Still, the
direction is notable:

| Position | Subscribed | Not subscribed |
|---:|---:|---:|
| 15% | 22.5% | 13.31% |
| 22% | 22.5% | 11.29% |
| 30% | 17.5% | 8.87% |
| 47% | 30.0% | 6.85% |

The committed audience is substantially more tolerant of the long lesson once
it reaches the technical material. This is not enough data for a stable cohort
claim, but it reinforces the present diagnosis: the largest problem is earning
attention from a cold viewer before the substance begins.

## What the export cannot establish

- `Detailed activity.csv` contains no rows, so it does not identify exact
  starts, stops, or replay counts.
- Local peaks cannot distinguish chapter clicks, manual seeking, and replay.
- The segmented cohorts are small and should not drive fine-grained decisions.
- The export cannot isolate narration, visual design, topic, or chapter labels
  as the sole cause of any movement.

All reported traffic in this export is organic, so paid promotion did not
distort the curve.

## Decision

Do not reduce the project's technical depth in response to Episode 1. Remove
the administrative opening, put the first real problem in the opening seconds,
and organize the lesson around concrete implementation payoffs. The 13-second
intro removal currently being tested on Episode 7 is directionally consistent
with this evidence, though Episode 7 will need its own retention curve before
we judge the effect.
