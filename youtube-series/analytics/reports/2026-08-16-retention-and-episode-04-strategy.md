# YouTube Performance Diagnosis and Episode 4 Redesign

Captured: 2026-08-16, 6:26 PM ET

Primary YouTube snapshot:
`youtube-series/analytics/private/snapshots/2026-08-16T22-26-08Z.json`

This report separates public counters, processed YouTube Analytics, observed
video structure, and hypotheses. The channel is new, the samples are small, and
YouTube Analytics is still processing some of the relevant views.

## Executive diagnosis

The strongest current signal is not X performance. It is Episode 1's audience
retention curve.

- The series premise converts unusually well for the present sample: Episode 1
  produced six attributed subscribers from 96 processed views.
- The lesson structure does not retain viewers: only 18.95% of the measured
  audience remains near 45 seconds, and 13.68% remains near 67 seconds.
- Episode 1 does not begin its tensor-specific subject until about 2:10 and does
  not begin live coding until about 7:35.
- Episode 2 again places recap and retrieval before new material. Its public
  watch behavior has not processed sufficiently to locate its own exits.
- Short 1 has no processed YouTube watch data yet. Instagram has sampled the
  same vertical lesson more broadly, but average watch time is only 5.44
  seconds. Its explanation begins at about seven seconds.

The current Episode 4 draft changes the promise but preserves the same delayed
payoff. It must be replaced, not polished.

## Current YouTube state

| Content | Public state at capture | Processed Analytics |
|---|---|---|
| Episode 1 | 139 views, 13 likes, 3 comments | 96 views, 84 minutes watched, 52-second average duration, 2.37% average viewed, 2 shares, +6 subscribers |
| Episode 2 | 29 views, 1 like, 2 comments | Only 3 views, apparently from before public release; no usable retention curve |
| Episode 3 | Private and scheduled; 5 preview views | No usable audience data |
| Short 1 | 32 views, 0 likes, 1 channel-authored comment | No processed rows for engaged views, duration, percentage viewed, traffic, subscribers, or retention |

Public counters and processed Analytics are not expected to match immediately.
The counter answers how many starts YouTube currently displays. Analytics is the
slower, richer dataset used for watch behavior and attribution.

## Episode 1: premise strength, delivery weakness

### Opening retention

Episode 1 is 37:11 long. Its first five processed retention buckets are:

| Approximate time | Audience watch ratio | Relative retention | Segment impressions |
|---:|---:|---:|---:|
| 0:22 | 51.58% | 0.484 | 49 |
| 0:45 | 18.95% | 0.382 | 18 |
| 1:07 | 13.68% | 0.305 | 13 |
| 1:29 | 11.58% | 0.260 | 11 |
| 1:52 | 9.47% | 0.215 | 9 |

The drop between approximately 22 and 45 seconds is the clearest current
bottleneck. Relative retention also declines, so the collapse underperforms the
comparison baseline for similar-length videos; it is not merely the normal
effect of publishing a long lesson.

The final transcript establishes the ordering:

- approximately 0:00-2:10: broad series mission and roadmap;
- approximately 2:13: the episode-specific tensor lesson begins;
- approximately 5:46: the tensor contract is enumerated;
- approximately 7:35: live coding begins.

Most measured viewers therefore leave before the actual episode begins.

### Conversion

The same processed sample produced six subscribers from 96 views, a 6.25%
attributed conversion rate. Thirteen public likes from 139 current public views
are also encouraging for such a small channel.

This suggests two different properties:

1. The promise of rigorous, first-principles deep learning in C++ attracts the
   right people.
2. The opening makes those people wait too long for the promised substance.

The evidence does **not** argue for less mathematical or systems depth. It
argues for moving that depth into an immediate problem-solving sequence.

### Discovery and intent

| Traffic source | Views | Estimated minutes watched |
|---|---:|---:|
| Direct or unclassified | 32 | 37 |
| External | 29 | 26 |
| Playlist | 14 | 5 |
| Other YouTube page | 11 | 1 |
| YouTube search | 5 | 13 |
| Subscriber feed | 4 | 1 |
| Channel page | 1 | 0 |

The samples and rounded minutes make per-source averages noisy. Still:

- most discovery is currently pushed from outside YouTube or direct links;
- browse and suggested discovery are not yet established;
- search contributed only five views, but those five accumulated 13 minutes of
  watch time, the strongest small high-intent signal in the current table.

Future packaging should therefore lead with a concrete capability while
retaining precise searchable terms such as matrix multiplication and
broadcasting.

### A late failure-oriented spike

Near 79% of the video, around 29:23, audience watch ratio rises to 20% after
being much lower immediately beforehand. The transcript at that moment shows a
real `bus error`, followed by the unsigned-underflow explanation.

The sample is small and the spike may include seeking or replaying, so it does
not prove a causal rule. It is nevertheless consistent with a useful Episode 4
experiment: show an observable failure, explain it, and fix it, instead of
opening with a trailer for a result delivered much later.

## Episode 2: weaker demand, insufficient consumption data

Episode 2 has 29 public views after about 31 hours. Episode 1 had roughly 91
views at a broadly comparable checkpoint in the learner's earlier Studio
capture. Episode 2 therefore has a weaker public trajectory, but the launches
were not controlled:

- Episode 1 had series-launch novelty, friend support, Telegram, LinkedIn, and
  broader external distribution.
- Episode 2 received a narrower rollout.
- The titles, topics, and thumbnails also changed.

The API currently reports three processed Episode 2 views on August 14, before
its public release on August 15. Its reported 39-second average duration and
2.36% average viewed must not be treated as public audience behavior. Its
retention request succeeds but contains no rows.

The final transcript still reveals a structural risk:

- approximately 0:00-0:26: opening, recap, and feature inventory;
- approximately 0:26-3:04: five retrieval answers;
- approximately 3:04: first new subject;
- approximately 5:09: implementation begins.

This does not prove where Episode 2 viewers left. It does show that the episode
repeats the ordering exposed by Episode 1: administrative framing and retrieval
arrive before the first new payoff.

Episode 2's packaging also describes an inventory: scalars, mutations, and
reductions. That requires a cold viewer to care about continuing an existing
implementation. The weaker X conversion provides separate support for testing
capability-led packaging, but it does not diagnose YouTube consumption.

## Short 1: what is known and unknown

### YouTube

At 6:26 PM ET, approximately four hours and 26 minutes after publication, the
Short displayed:

- 32 public views;
- zero likes;
- one comment, written by the channel;
- no processed YouTube Analytics rows.

The counter reached 32 by 4:23 PM and remained there through 6:26 PM. At least
five views existed before public release from review traffic. YouTube has not
yet supplied engaged views, average duration, percentage viewed, swipe
behavior, traffic sources, subscriber conversion, or retention.

We therefore know that YouTube recorded 32 starts or replays. We do not know
how many viewers chose to continue watching. It is too early to diagnose the
YouTube hook. Capture 24-hour and 72-hour checkpoints.

### Instagram comparison

The same vertical lesson was published on Instagram at 5:07 PM ET. At about
6:29 PM it had:

- 118 plays;
- 109 accounts reached;
- 5.44 seconds average watch time;
- 598.1 seconds total watch time;
- zero likes, comments, saves, or shares.

Platform view definitions differ, so 118 Instagram plays must not be compared
directly with 32 YouTube views. The useful signal is internal to Instagram: it
found an initial cold sample, but consumption and response were shallow.
Against the uploaded video's 34-second runtime, 5.44 seconds is approximately
16% average consumption.

The Short's mechanism begins at about seven seconds. The average Instagram
viewer did not reach it. Plausible, testable causes include:

- the complete three-column answer is visible from the first frame, leaving
  little information to reveal;
- spoken phrases such as "shape empty brackets" are cognitively awkward;
- `[1]` adds a third concept to a lesson whose central contrast is `[]` versus
  `[0]`;
- the lesson is long relative to the size of the idea;
- the CTA occupies a substantial share of the ending.

These are hypotheses, not conclusions. Short 2 should test progressive visual
disclosure, a 20-25 second target, natural wording, and no CTA or a CTA under two
seconds.

### X native-video checkpoint at 8:54 PM ET

The X upload received 1,112 impressions and 355 organic video views in its
first 4 hours and 47 minutes. That is meaningful distribution for an account
with 224 followers, although impressions and views are not unique people.

Playback telemetry reported 727 starts, 131 reaching 25%, 49 reaching 50%, 30
reaching 75%, and 18 reaching 100%. Measured against starts, those survival
rates are 18.0%, 6.7%, 4.1%, and 2.5%. Starts are playback events rather than
qualified or unique views, so they can exceed the reported view count.

The shape of the funnel matters more than the raw view count. The largest loss
occurred before the first quarter, which is approximately the first eight
seconds of the 33.5-second upload. Once a viewer reached halfway, the remaining
decline was materially gentler: 30 of 49 halfway plays reached 75%, and 18 of
those 30 completed. Combined with Instagram's 5.44-second average watch time,
this is now a cross-platform reason to test a faster opening. It is not yet
proof that any single phrase, visual, or duration caused the exits.

The post produced 11 engagements, three profile clicks, five likes, one reply,
and one bookmark. Native video therefore expanded reach, but it did not yet
convert that reach into strong interaction or profile exploration. Short 2
should preserve native distribution while testing progressive disclosure, a
20-25 second runtime, and delivery of the first explanatory result inside the
opening five seconds.

## X: useful, but not the main content diagnosis

The existing bounded X comparison remains valuable:

| Announcement | Impressions | Engagements | Link clicks | Profile clicks |
|---|---:|---:|---:|---:|
| Episode 1 | 798 | 102 | 20 | 15 |
| Episode 2 | 800 | 19 | 4 | 4 |

Reach was essentially identical while post-impression conversion differed.
That supports capability-led announcement copy. It does not explain where
YouTube viewers leave, and it should never have been used as a substitute for
video-consumption analysis.

## Why the first Episode 4 draft failed the evidence

The draft placed the final expression at 0:00, but a displayed destination is a
promise, not a payoff. Its actual sequence was:

- 1:20: first new failure;
- 3:30: first mathematics;
- 8:15: first code;
- 16:00: first matrix-multiplication result;
- 18:30: broadcasting failure;
- 38:15: the opening expression finally works;
- 40:00: ending.

It also inserted a 2.5-minute overflow-safe element-counting review before the
central operation. In other words, it changed the words in the opening while
preserving the same lecture-first structure.

That is not a credible response to an audience collapse concentrated before 45
seconds.

## Episode 4: the new experiment

The episode will remain rigorous and will still combine rank-two matrix
multiplication with general elementwise broadcasting. The order changes.

### Governing computation

```cpp
const Tensor predictions =
    inputs.matmul(weights) + bias;
```

The batch already exists in `inputs`. The episode does not "turn one prediction
into a batch." It applies one rank-two linear transformation to a batch of
input rows and produces one output vector per row.

### Pacing contract

1. Teach one complete new fact in the first 15 seconds: each matrix output cell
   is the dot product already implemented.
2. Show the current rank error in the opening minute.
3. Begin changing code around minute two, not minute eight.
4. Produce a working matrix result around minute six.
5. Produce the complete numerical prediction early with an intentionally
   expanded bias matrix, then make its waste motivate broadcasting.
6. Make the real `inputs.matmul(weights) + bias` expression work around minute
   18, before hardening and edge cases.
7. Alternate failure -> derivation -> code -> result throughout.
8. Target roughly 25-29 minutes. Do not pad toward 40.

### Replacement arc

| Time | Observable progress |
|---:|---|
| 0:00-0:18 | Current rank failure, one row-column dot product, and final numerical destination |
| 0:18-0:55 | Concise recap, roadmap, and the three exact Episode 3 retrieval answers |
| 0:55-2:15 | Derive one output cell and the `[m,k] @ [k,n] -> [m,n]` contract |
| 2:15-6:30 | Implement the rank-two reference kernel while explaining each loop where it enters |
| 6:30-8:15 | Run matmul; explicitly expand the bias; obtain the full predictions early |
| 8:15-10:30 | Expose the repeated allocation and derive right alignment plus zero-stride reuse |
| 10:30-17:30 | Generalize the existing elementwise traversal to broadcasting |
| 17:30 | Run the exact final expression |
| 17:30-22:30 | Verify scalar, size-one, empty, incompatible, and empty-inner cases |
| 22:30-25:30 | Explain the contiguous-layout limitation, review, preview stored views, and end with three questions |

The overflow-safe element-count helper remains useful, but it is not a new
subject. Moving Episode 2's existing rule into a helper should take one short
explanation at the point of allocation.

## Packaging experiment

Working title:

```text
Building a Linear Layer in C++: Matmul & Broadcasting | Deep Learning, All the Way Down #4
```

This leads with the newly unlocked capability while retaining precise search
terms. A corresponding thumbnail should communicate the transformation, such
as `BUILD A LINEAR LAYER`, rather than list implementation features.

## What to measure next

For Episode 4:

1. audience watch ratio and relative retention at the first available buckets;
2. survival through the first failure and first code edit;
3. average view duration and percentage viewed;
4. subscriber conversion;
5. search, browse, suggested, external, and playlist traffic separately.

For Short 1:

1. YouTube engaged views, average percentage viewed, retention, and subscribers
   at 24 and 72 hours;
2. Instagram average watch time, completion, interactions, and follows at the
   same checkpoints.

This redesign is an experiment derived from limited evidence. It does not
establish a universal optimal runtime or editing formula. Its purpose is to
test whether immediate resolution, visible failure, and recurring code-level
payoffs improve the weakest observed part of the current funnel.

## Overnight cross-platform synthesis: August 17, 5:32 AM ET

The latest evidence is sufficient for a small number of structural experiments,
but not for choosing a winning platform, topic family, runtime, posting hour,
thumbnail system, or long-term growth curve.

### What is now observed

- Episode 1 converted six subscribers from 96 processed views, while average
  viewing was only 52 seconds and the audience watch ratio fell below 19% near
  45 seconds. The series proposition can convert a small high-intent group, but
  the opening loses most viewers before the lesson begins.
- Episode 2 still lacks a valid post-publication processed sample. Its content
  quality and packaging cannot yet be compared causally with Episode 1.
- The X native Short reached 1,176 impressions and 371 organic video views,
  exceeding the account's 227-follower audience. Native video can earn a cold
  distribution test. Only 140 of 761 playback starts reached 25%, 51 reached
  50%, and 18 completed, so the largest behavioral loss remains early.
- The Instagram Reel increased from 118 to 192 plays, from 109 to 165 accounts
  reached, and from 5.44 to 7.32 seconds average watch time. It also produced
  one like, one share, and the account's first follower. This is a positive
  movement, but too small to identify a cause.
- The YouTube Short reached 84 public starts but still has no processed watch
  rows. YouTube has not yet confirmed or contradicted the early-retention
  pattern visible on X and Instagram.
- The latest personal X post received 123 impressions, 11 engagements, four
  likes, two replies, and four profile clicks. Personal posts currently serve
  a smaller but more interactive audience than the native Short. They should
  remain a distinct relationship layer rather than become disguised promotion.
- Audience counts moved from X 224 to 227 and Instagram 0 to 1 while YouTube
  remained at 16. These movements overlap several distribution events and must
  not be attributed to one post.

### Decisions for the next content

1. Episode 4 will test immediate teaching rather than an immediate trailer.
   Resolve one matrix-output cell in the opening seconds, surface the current
   rank failure inside the first minute, begin code around minute two, and
   produce the first working matrix result near minute six.
2. Short 2 will be a 20-25 second native lesson built around one concrete C++
   failure. The strongest candidate is the unsigned reverse-loop failure:
   show the broken loop, expose why zero is never passed, and give the correct
   loop. Reveal the answer progressively and omit the CTA or keep it under two
   seconds.
3. Episode announcements will lead with the capability or transformation, then
   name the operations. Episode 3's title has been reframed around building a
   linear prediction; its announcement should preserve that capability-led
   framing.
4. Continue native video on X and Instagram because both obtained cold reach,
   but use the next three Shorts as controlled opening experiments rather than
   declaring either platform a winner.
5. Continue concise personal X posts without links. Their job is familiarity
   and conversation, not direct episode traffic.

### What requires more publishing

The next useful sample is approximately three more long-form episodes and three
more independently recorded Shorts with deliberately varied openings. Until
then, do not infer the ideal episode length, posting time, thumbnail style,
curriculum topic, or platform allocation from the current counts. Publishing
more is necessary, but each release must test a named hypothesis so additional
volume produces information rather than merely more noise.

## Retrieval-format decision: August 17

Episode 3's own pinned comment now answers its three closing questions. Episode
4 therefore removes the spoken answer segment entirely and moves from its
series opening and brief recap directly into the current tensor failure.

Every episode will still end with approximately three questions, but its exact
answer key will appear in that same episode's first pinned comment. This
preserves retrieval practice while testing whether removing prerequisite
administration from the next opening improves early retention.
