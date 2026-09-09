# Short 5 Instagram retention and creative analysis

Analyzed September 2, 2026.

Reel: https://www.instagram.com/reel/DcyO3GYimT3/

Final master:
`aliases/04-final-cuts/shorts/ep05/cpp-accumulator-dependency-chain-performance.mp4`

SHA-256:
`cd659294df94d8ee3bd79af6edb762d219442bdfb5a290bc3eacf3045d854fe5`

## Executive conclusion

Short 5 succeeded because Instagram gave it a large cold-audience test and the
content continued producing useful signals after exposure. The strongest
observable creative pattern is:

1. familiar code in the first frame;
2. a simple performance question;
3. one tiny code change;
4. a delayed measured result;
5. a genuine technical question after the payoff; and
6. an immediate cut.

The retention curve also identifies a real weakness. Most loss happens during
the opening question. Retention falls from approximately 100% at the start to
roughly two-thirds by four seconds. The curve then declines much more slowly
and finishes at 43% around 0:19.

The breakout therefore does not prove that the opening is finished or optimal.
The premise, middle, payoff, and ending appear strong enough to overcome a
meaningful opening loss. The next Short should preserve the overall structure
while making the complete promise land sooner.

## Evidence used

- The final 19.77-second master, inspected at half-second intervals.
- The owned YouTube automatic captions downloaded after Studio confirmed the
  English source track.
- The learner-supplied Instagram retention and traffic-source screenshot.
- The September 2 Instagram API snapshot at approximately 12 hours and 58
  minutes.
- Authenticated inspection of the live Reel, comment panel, and profile grid.
- The Short 5 publishing package and platform copy research.

The retention curve is available only as a screenshot. Intermediate retention
values below are visual estimates rather than exported data points. The 43%
value at 0:19 and traffic-source percentages are displayed directly by
Instagram.

## Master and audio facts

- Runtime: 19.77 seconds
- Source: 2160x3840, 9:16
- Frame rate: 30 fps
- Video: H.264 High, Rec.709
- Audio: AAC stereo, 44.1 kHz
- Integrated loudness: -16.7 LUFS
- True peak: -3.0 dBFS
- Loudness range: 1.6 LU
- Instagram transcode observed in Chrome: 1080x1920, 19.78 seconds
- Spoken-word gaps above -35 dB lasted only 0.12 to 0.25 seconds. There is no
  meaningful dead air.

The audio could not be judged subjectively in this environment. Loudness,
silence, codec, and timing are objective measurements. Vocal tone, room sound,
compression character, keyboard balance, and music presence require a human
listening pass.

## Actual narration

> How much faster can you make this loop with only a single extra variable?
> Right now, every addition has to wait for the one before it. Add B, split the
> values between them, and now the processor has two independent sums to work
> on. On my machine, that gave me almost a 40% speed up. Two is faster. Four is
> even faster than two. So, what do you think is going on here? What is the CPU
> doing differently?

The narration contains approximately 79 words, or roughly 246 words per minute
across the spoken portion. It is fast, but the sentences remain short and the
burned-in captions carry the wording visually.

## Frame, narration, and retention map

| Time | Spoken beat | Visual beat | Approximate retention | Reading |
| --- | --- | --- | ---: | --- |
| 0:00-0:01 | `How much faster...` | Existing one-accumulator loop, rough red circle, `Inefficient loop?`, face, microphone, and `HOW MUCH FASTER` caption | 100% to high 90s | The subject and a performance question are immediate. The complete one-variable promise has not landed yet. |
| 0:01-0:03.7 | `...with only a single extra variable?` | Opening code remains. Captions progress through `THIS LOOP`, `ONLY A SINGLE`, and `EXTRA VARIABLE`. The red opening annotation disappears around 0:02.5. | high 90s to roughly 70% | This is the steepest loss. The key novelty arrives over several caption beats rather than in the first second. |
| 0:03.7-0:06.5 | `Every addition has to wait...` | `a += arr[i]` remains highlighted. The creator uses a one-chain hand gesture. | roughly 70% to high 50s | The mechanism begins immediately after the question. Retention starts flattening. |
| 0:06.5-0:08.8 | `Add B...` | The second accumulator and `i += 2` appear. A red arrow points to `b`. | high 50s | The promised tiny change becomes visible at the same time it is named. |
| 0:08.8-0:11.4 | `Split the values... two independent sums` | A red circle encloses the two additions. Two-handed gestures reinforce the split. | mid 50s to low 50s | Audio, code, annotation, captions, and gesture all express the same idea. |
| 0:11.4-0:14.4 | `Almost a 40% speed up` | The benchmark table replaces the code. The two-accumulator row receives a cyan highlight and red arrow. | low 50s to high 40s | The first numerical payoff arrives about 58% into the runtime. The curve remains comparatively stable. |
| 0:14.4-0:16.9 | `Two is faster. Four is even faster...` | The four-accumulator row becomes the focus. The complete table is already visible. | high 40s to mid 40s | The final escalation is easy to read, although all three results were visible when the table first appeared. |
| 0:16.9-0:19.77 | `What is the CPU doing differently?` | The benchmark remains on screen while the creator addresses the viewer. No CTA or end card appears. | mid 40s to 43% | The adjacent question costs only a few additional points. The edit cuts immediately after the final word. |

## What the retention curve says

### Opening

The opening is the largest remaining bottleneck. The visible curve loses about
one-third of viewers during the first four seconds. The first sentence begins
at 0:00.08, so silence is not the problem. The likely friction is that the
complete proposition takes about 3.7 seconds to finish.

`only a single` is redundant. A shorter version such as `How much faster can
one variable make this loop?` would deliver the same promise sooner without
changing the premise.

The first frame combines code, a red circle, `Inefficient loop?`, the creator's
face, a microphone, and the spoken-hook caption. The compact callout gives a
viewer a fast visual entry into the problem, while selective yellow and teal
caption emphasis makes the key phrase easier to scan. The data cannot isolate
either treatment as causal, but the combined opening system is strong enough to
preserve while tightening the spoken promise.

### Middle

The curve flattens once the dependency explanation begins. From approximately
0:04 through the benchmark reveal near 0:11, the video loses viewers gradually
rather than collapsing. The edit gives each sentence a matching visual action:

- one accumulator line highlighted;
- second accumulator revealed;
- arrow pointing to `b`;
- two additions circled;
- one-hand and two-hand gestures; and
- short caption fragments synchronized with speech.

This is the strongest instructional section and should remain the model for
future Shorts.

### Payoff

The benchmark appears around 0:11.4. Retention stays comparatively stable from
that point through the end. Viewers who reached the result generally continued
through the second comparison and final question.

The table shows all three rows immediately. Highlighting controls attention,
but the last result is technically available before the narration reveals it.
A future test can stage the second and fourth accumulator rows without delaying
the first numerical payoff.

### Ending and replay

Instagram shows 43% retention at 0:19. The API separately reported 17.57
seconds average watch time on a 19.77-second master. Those values use different
platform definitions and denominators, so they must not be forced into one
funnel calculation.

Together they are consistent with substantial replay or looping among viewers
who stayed. The ending does not attempt a seamless visual loop. The replay is
more plausibly connected to dense code, a fast explanation, a benchmark worth
checking, or the unresolved hardware question.

The final question does not withhold the original lesson. The Short has already
shown that independent sums can overlap more work. The question opens the next
layer: what the CPU does with that independence. This is a useful continuation
cue without asking for a follow.

## Complete factor inventory

### Premise and topic

- The subject is a familiar C++ loop rather than an unfamiliar library or
  framework.
- The visible change is one extra accumulator. The idea is small enough to
  understand visually.
- The result is counterintuitive: more code and more state produce a faster
  benchmark.
- The result is measurable rather than rhetorical.
- The deeper explanation reaches CPU execution, which attracts C++, systems,
  performance, and computer-architecture audiences.
- The premise invites prediction before the result appears.
- The topic supports disagreement and technical scrutiny without relying on
  manufactured controversy.

### Hook

- Speech starts at 0:00.08. There is no greeting, logo animation, or context
  block.
- The hook is a question rather than a claim.
- `How much faster` promises a numerical answer.
- `this loop` binds the narration to code already on screen.
- `one extra variable` makes the change feel surprisingly small.
- The complete novelty takes approximately 3.7 seconds to land.
- The wording uses both `only` and `single`, which adds time without meaning.
- The question does not reveal the benchmark result.

### Opening frame and stickers

- The original loop is present immediately.
- A rough red hand-drawn circle identifies the relevant loop.
- A large white-and-red `Inefficient loop?` sticker adds a second curiosity
  prompt.
- The creator's face is visible from the first frame.
- The microphone is visible and reinforces the technical creator setup.
- Large yellow captions with a black outline sit above the creator.
- Cyan accent words emphasize `FASTER` and later `40%`.
- The opening contains no platform watermark or recycled-platform chrome.
- The handmade annotation style feels native to short-form video rather than
  like a polished advertisement.
- The code itself is relatively small at phone size, but the highlight and
  circle reduce the amount the viewer must parse.

### Visual structure

- The entire Short uses a stable split-screen composition.
- Code and benchmark evidence occupy the upper region.
- The creator occupies the lower region and maintains direct eye contact.
- Essential content avoids Instagram's right control rail and bottom caption
  area.
- Captions stay out of the code and benchmark regions.
- The neutral room and black code background create clear separation.
- Red arrows and circles appear only when they have a specific target.
- The visual changes from one accumulator to two at the exact spoken reveal.
- The benchmark replaces the code rather than competing with it.
- The result table is accurate and highlighted, but its text is small.
- All three benchmark rows become visible together.
- The profile-grid crop preserves the opening code and `Inefficient loop?`
  prompt. Profile supplied only 0.2% of views, so this cover did not drive the
  breakout directly.

### Presenter and delivery

- The creator looks into the camera rather than reading away from it.
- Hand gestures mirror one dependency chain and then two independent chains.
- Facial movement and gestures provide motion while the code remains stable.
- Delivery is fast and information-dense.
- The language stays concrete until `independent sums` and `processor` enter
  after the visual demonstration.
- `On my machine` correctly limits the benchmark claim.
- The narration says `almost a 40% speed up`, an understandable summary of the
  measured result.
- There is no series introduction, biography, credential statement, or request
  for attention.

### Pacing and editing

- Runtime stays below 20 seconds.
- Narration runs at approximately 246 words per minute.
- No detected pause exceeds approximately 0.26 seconds.
- Burned-in caption fragments change roughly every half second to one second.
- Visual state changes occur around 0:02.5, 0:06.5, 0:09.5, 0:11.4, and
  0:14.4.
- The first code payoff appears around one-third of the way through the video.
- The first numerical payoff appears around 58% of the way through.
- The final question occupies roughly the last three seconds.
- The video ends immediately without a hold, logo, card, fade, or dead tail.

### Captions

- Captions are burned into the master, so the lesson remains legible when muted.
- They use short, rapidly changing phrase fragments rather than full sentences.
- Yellow, black outline, and occasional cyan emphasis create high contrast.
- They reinforce the spoken pacing and guide the eye to the current concept.
- `A 40%` is visually awkward English even though the spoken sentence is clear.
- The YouTube automatic transcript recognized the narration accurately enough
  to provide reliable timing.

### Audio

- The integrated level is a reasonable -16.7 LUFS with -3.0 dBFS true peak.
- Loudness is controlled, with only 1.6 LU of measured range.
- There is effectively continuous speech and no long silence.
- Subjective voice clarity, room sound, noise reduction, compression, and any
  background music remain unverified by this analysis.

### Proof and technical credibility

- The Short shows real source code rather than an abstract animation.
- It shows exact benchmark values: 5.826, 4.212, and 3.619 seconds.
- The caption states that SIMD vectorization and loop unrolling were disabled.
- The caption states that results depend on processor, compiler, and workload.
- The first comment adds the compiler flags and controlled-work explanation.
- Several viewers challenged SIMD, unrolling, branches, optimization level,
  and odd input sizes. That discussion increased activity but also identifies
  credibility details that viewers could not verify from the video alone.
- The Short should not add every benchmark control to the frame. One compact
  visible control line, combined with the caption and first comment, may reduce
  repeated misunderstandings without overcrowding the lesson.
- The visible demonstration uses paired loads. The benchmark contract and even
  input-size assumption need to remain correct and recoverable in public code.

### Ending and conversion design

- The original claim is resolved before the ending.
- The ending asks one adjacent technical question.
- There is no request to follow, like, comment, save, or visit the profile.
- There is no external link in the caption or first comment.
- The ending creates an expectation of further low-level explanations without
  promising a specific next upload.
- Followers rose from 42 before publication to 114 at the API checkpoint and
  117 during the authenticated follow-up. This is account-level net growth, not
  exact Reel-attributed conversion.

### Caption and search language

- The first caption line states the result in plain language: `One extra
  accumulator made this C++ loop faster.`
- The caption contains the primary phrase `C++ loop`.
- Supporting terms include `accumulator`, `SIMD vectorization`, `loop
  unrolling`, `dependency chain`, `CPU`, `processor`, `compiler`, and
  `workload`.
- Exact benchmark values make the caption useful even without playback.
- Method limits reduce the risk of presenting one machine as universal.
- The caption is self-contained and does not push viewers off Instagram.

### Hashtags

The live set was:

- `#cpp`
- `#coding`
- `#programming`
- `#cpu`
- `#softwareengineering`

The set combines one exact language tag, two broad coding tags, one hardware
tag, and one professional-domain tag. All five describe the content. They also
appeared in earlier owned-account posts or closely related platform tests.

No available evidence attributes the breakout to hashtags. The Reel and
Explore tabs supplied 99.2% of views, but those surfaces can classify content
from many signals, including speech, captions, on-screen text, engagement, and
viewer history. Keep the current approach of a small accurate set and avoid
claiming hashtag causation.

### Publication timing and account state

- Publication: Wednesday, September 2 at 8:26:42 AM ET.
- The post was published immediately after Instagram's browser composer failed
  to expose scheduling. The earlier planned time was 11:30 AM ET.
- The account had 42 followers immediately before publication.
- The profile contained only three earlier posts.
- A small follower base could not have produced 62,114 reached accounts by
  itself.
- Publishing in the morning gave the Reel a full daytime window for its first
  distribution cycle.
- One breakout does not establish Wednesday morning as the cause. Repeat the
  same approximate window on at least two comparable Shorts before changing
  the standing cadence.

### Distribution source

Instagram reported:

- Reels tab: 85.5%
- Explore: 13.7%
- Profile: 0.2%
- Feed: 0.2%

Reels and Explore supplied 99.2% of views. This was overwhelmingly algorithmic
cold discovery rather than profile traffic or the existing follower feed.
The result shows that Instagram could classify and distribute the content to a
relevant audience despite the small account.

### Reach, consumption, and interaction

At approximately 12 hours and 58 minutes:

- 104,182 plays
- 62,114 accounts reached
- 1.68 plays per reached account
- 17.57 seconds average watch time
- 1,099 total interactions
- 600 likes
- 85 comments
- 275 saves
- 134 shares

Authenticated follow-up later showed 610 likes and 86 comments. The first
account-authored technical comment had 19 likes.

The high save, share, comment, and replay signals show that the audience did
more than passively receive a large impression test. The exact ranking weight
of each action is unknown.

### Engagement and follower funnel follow-up

A later learner-supplied Instagram Insights capture showed:

- 155 profile visits;
- 74 follows;
- 11 bio-link clicks;
- 627 likes;
- 86 comments;
- six reposts;
- 134 shares; and
- 286 saves.

Against 104,182 plays, this is approximately a 0.15% profile-visit rate and a
0.07% follow rate. Against 62,114 reached accounts, it is approximately a 0.25%
profile-visit rate and a 0.12% follow rate. Follows equal 47.7% of profile
visits, but Instagram presents these as separate post-view actions; that ratio
does not prove that every follow passed through a recorded profile visit.

The evidence points to profile intent as the main conversion constraint. Once
the Reel generated a deeper account action, follower response was strong. The
creative gave viewers clear reasons to save, share, and discuss the individual
lesson, but it offered less evidence that another specific experiment was
coming.

This does not justify replacing the final technical question with a conversion
CTA. The question likely helped produce discussion, which may have supported
distribution, although its ranking effect is not measurable here. The next
outro should keep a genuinely answerable technical question and connect it to a
specific experiment the creator will test next.

### Native-platform settings and packaging

- The clean 2160x3840 master was uploaded natively.
- The filename was descriptive:
  `cpp-accumulator-dependency-chain-performance.mp4`.
- The live post contains no external URL.
- Comments are enabled.
- The publishing package calls for Share to Feed, remix, and original-audio use
  to remain enabled. Live API evidence does not independently expose every one
  of these switches, so they are planned or manually observed settings rather
  than proven causal factors.
- No collaborator, location, paid boost, or cross-account tag is recorded.
- No evidence indicates paid distribution.
- The live profile points to the complete YouTube series, but profile traffic
  supplied only 0.2% of views at the captured checkpoint.

### Factors that remain unknown

- Exact first-comment publication time
- Follower versus non-follower retention curves
- Exact replay count and Instagram's denominator for average watch time
- Geographic and time-zone distribution
- Search-query contribution, if any
- Whether Instagram used the caption, hashtags, audio transcript, visual text,
  or early engagement most heavily for audience classification
- Share destinations and save intent
- Early minute-by-minute reach velocity
- Subjective audio quality and whether music or keyboard sounds affected watch
  behavior
- Competitive conditions in the Reels feed at publication time

## What to preserve

Preserve these features for the next controlled Short:

1. one familiar code fragment;
2. one tiny change with a surprising consequence;
3. immediate speech and no setup;
4. creator face and direct eye contact;
5. one compact curiosity callout that makes the problem instantly legible;
6. large burned-in captions with selective yellow and teal keyword emphasis;
7. annotations that point to the exact changing line;
8. code reveal synchronized with narration;
9. a measured numerical payoff;
10. explicit hardware or benchmark qualification;
11. an adjacent technical question after the lesson is complete;
12. no generic CTA; and
13. a sub-20-to-24-second runtime when the idea permits it.

## What to refine

1. Deliver the complete hook within roughly 1.5 to 2.0 seconds.
2. Remove redundant hook words such as `only a single`.
3. Make the curiosity callout and emphasized captions reinforce the same hook.
   Keep both readable and give each a clear visual role.
4. Increase the result typography or stage fewer rows at a time.
5. Avoid showing the final benchmark row before its spoken reveal.
6. Replace awkward caption fragments such as `A 40%` with a complete visual
   phrase.
7. Consider one compact methodology label if it prevents the most common false
   interpretation without crowding the frame.
8. Record the exact first-comment time and Reel-specific follow/profile actions.

## Next controlled tests

### Test A: faster promise delivery

Keep the topic family, runtime, split-screen layout, face, caption style,
annotations, delayed benchmark, ending style, and approximate Instagram time.
Change only the opening sentence and simplify the first frame. Compare the
first four seconds of retention against this Reel.

### Test B: staged result reveal

On a later Short, preserve the opening structure but reveal one benchmark row
at a time. Compare retention from the first numerical result through the final
result. Do not combine this with Test A if clean attribution matters.

### Test C: timing replication

Publish two comparable Shorts between approximately 8:15 and 9:00 AM ET on a
weekday. Treat this as a replication, not a permanent timing rule. Keep the
creative structure comparable and record early velocity at 15, 30, 60, and 180
minutes.

## Data to capture next

For this Reel at 24 hours, 48 hours, 72 hours, and seven days, capture:

- plays and reach;
- the exported retention curve if Instagram offers it;
- average watch time;
- skip rate;
- follower and non-follower watch behavior;
- Reels, Explore, Feed, Profile, and search sources;
- likes, comments, saves, shares, and reposts;
- profile visits;
- Reel-attributed follows;
- total account followers;
- first-comment likes and reply activity; and
- any recommendation or policy notice.

The main lesson should remain provisional until at least two more Shorts repeat
the structure. The current result is strong enough to guide the next test, but
not strong enough to turn every co-occurring detail into a permanent rule.
