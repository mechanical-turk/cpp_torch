# Long-form Retention Comparison: Episodes 1-6

Captured: 2026-08-29

Scope: YouTube long-form only. This report must not be used as evidence for
Shorts structure, pacing, or distribution.

Sources: the Studio `All.csv` audience-retention exports stored under Chapters
1-6, the public video durations, the recorded automatic captions, and the
caption-derived chapter timestamps.

The exports use one-percent position buckets. The values below interpolate
between those buckets to compare episodes at matched elapsed times. They are
approximate, especially for the smaller episodes, and are best read as a strong
structural signal rather than precise point estimates.

## Matched opening retention

| Episode | Runtime | 0:00 | 0:15 | 0:30 | 0:45 | 1:00 |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 37:11 | 52.8% | 35.0% | 23.6% | 18.4% | 16.7% |
| 2 | 28:11 | 73.5% | 32.7% | 22.9% | 18.3% | 14.0% |
| 3 | 34:11 | 67.1% | 31.1% | 13.4% | 7.4% | 4.4% |
| 4 | 13:19 | 102.2% | 34.2% | 20.6% | 12.5% | 11.9% |
| 5 | 27:06 | 74.8% | 39.5% | 25.5% | 22.1% | 23.5% |
| 6 | 10:59 | 81.3% | 40.1% | 28.1% | 23.0% | 12.8% |

Episode 4's opening bucket exceeds 100%, which can happen when moments are
replayed or viewers enter and revisit the opening. It does not mean that the
video acquired more than its total audience. Episode 4 also has a small sample,
so its curve is coarse.

## Main finding

The opening cliff repeats across all six long-form episodes.

This is no longer an Episode 1 anomaly. Every episode loses a large share of
its measured audience before one minute. The shorter runtimes of Episodes 4 and
6 do not prevent the opening collapse. Shortening the complete episode is
therefore not a sufficient remedy.

The severity varies, but the structural pattern is stable:

1. The video identifies the series.
2. It explains prior state or the current concept.
3. It describes what will be implemented.
4. Only afterward does it begin doing the work promised by the title.

The first minute remains an explanation of the coming lesson rather than the
first useful piece of the lesson.

## Retrieval made the problem substantially worse

Episodes 2 and 3 put the previous episode's answers near the beginning.

| Episode | Retrieval begins | New subject begins | Retention at new subject |
|---:|---:|---:|---:|
| 2 | 0:26 | 3:04 | approximately 6.0% |
| 3 | 0:54 | 4:54 | approximately 3.2% |

Episode 3 is the clearest failure. It falls from 67.1% at the opening bucket to
about 5.6% at 0:54 and about 3.2% when the new subject begins. Retention then
rises around 5:30-6:10 as the episode approaches and begins tensor-addition
code. The export cannot distinguish seeking, chapter navigation, and replay,
but each explanation points in the same direction: viewers wanted the new
implementation and skipped the retrieval section.

Moving retrieval answers to the first comment was the correct decision. They
must never return to the beginning of a long-form episode.

## Topic-specific narration is still not enough

Episodes 4-6 removed the long retrieval block and started with the current
topic. Their openings are better focused, but they still explain for roughly
40-60 seconds before producing visible progress.

- Episode 4 explains how one prediction becomes a batch, introduces matrix
  multiplication, and previews broadcasting before switching to code.
- Episode 5 explains the scalar-bias shape mismatch and describes the two
  broadcasting questions before working through the representation.
- Episode 6 explains why predictions require targets and previews the scalar
  loss before switching to code at about 0:40.

All three still lose heavily during that explanation. A relevant explanation
is better than series administration, but a promise of useful work is not the
same as useful work.

Episode 5 is the strongest of these openings at 0:45-1:00. It begins from a
specific operation that fails even though it should work. This supports using a
concrete failure or contradiction as the entry point. The next improvement is
to demonstrate that failure immediately instead of spending a minute describing
it.

## Concrete implementation attracts navigation and replay

Several curves rise around specific implementation moments:

- Episode 1 rises around tensor construction, testing, indexing, and the
  unsigned reverse-loop failure.
- Episode 3 rises around 5:30-6:10 as tensor addition begins after the retrieval
  section.
- Episode 4 rises around 4:02 when the output element is explained as a dot
  product.
- Episode 6 rises around 3:11 near normalization of the batch loss.

Small samples prevent precise causal claims. The consistent interpretation is
that viewers navigate toward, revisit, or remain interested in concrete
technical payoffs. The response should be to move those payoffs earlier, not to
remove mathematical or systems depth.

## Cold-viewer context

The subscriber exports for Episodes 2-6 contain only non-subscribed retention
rows. The new-versus-returning exports are also small and inconsistent, but the
series is clearly being evaluated largely by viewers without a subscription
commitment. An opening cannot assume patience based on series loyalty.

Every episode must stand on its own. Prior state should be restated only when
the current operation needs it, and then in the shortest form that makes the
next step understandable.

## Decisions for future long-form episodes

1. Remove the spoken series introduction from the opening by default.
2. Never begin with retrieval questions, recap, roadmap, or setup commands.
3. Open on the current failure, contradiction, calculation, or code state.
4. Start changing, running, or deriving something inside the first 30 seconds.
5. Deliver the first observable payoff within the first minute.
6. Use an opening visual only if it makes the immediate problem faster to
   understand. Retire it as soon as it has done that job.
7. Organize the rest of the episode into repeated cycles: need, smallest useful
   step, observable result, interpretation, next need.
8. Preserve rigorous explanations, but introduce them when the implementation
   creates the need for them.

## Next controlled test

For the next three long-form episodes:

- no spoken series preamble;
- no dedicated recap or retrieval section at the beginning;
- a concrete problem or failure in the first sentence and first frame;
- meaningful work by 0:30;
- first observable result by 1:00; and
- no uninterrupted explanatory block longer than roughly two minutes without a
  calculation, code change, run, test, or visible state change.

Measure retention at 0:15, 0:30, 0:45, 1:00, and 2:00. Compare those values
against Episodes 1-6 at matched elapsed times. Do not change the long-form
technical depth at the same time. The experiment is about ordering and time to
payoff.

## Limits

- The episodes have small and unequal audiences.
- One-percent buckets represent different elapsed times for each runtime.
- `Detailed activity.csv` contains no event rows for any episode.
- Retention rises cannot distinguish seeking, chapter clicks, and replay.
- Topic, packaging, traffic source, and audience composition also vary.

The data is nevertheless consistent enough to justify a strong opening-order
experiment. It is not yet sufficient to prescribe an ideal episode runtime or
to attribute every decline to one sentence or visual.
