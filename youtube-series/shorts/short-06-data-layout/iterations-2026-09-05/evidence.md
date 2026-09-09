# Evidence and shared production contract

This loop uses existing evidence. It does not trigger an engine check, a new
benchmark, fresh platform collection, publishing, or a release commitment.

## Evidence register

- **E1, Instagram opening and delivery:** [Short 5 final-media and retention analysis](../../../analytics/reports/2026-09-02-short-05-instagram-retention-and-creative-analysis.md).
  The complete opening promise took about 3.7 seconds. The screenshot suggests
  roughly a third of viewers left by four seconds, then the curve declined
  more gradually; 43% remained at 19 seconds. Synchronized code changes,
  annotations, emphasized captions, and gestures accompanied the stronger
  middle. These observations do not isolate the effect of any one treatment.
- **E2, discussion:** [September 4 Instagram comment review](../../../../docs/logs/analytics-observations.md#2026-09-04-short-5-disagreement-and-intentional-omissions).
  Compiler and boundary objections prompted substantive discussion in a
  qualitative sample. Preserve room for real tradeoffs without making basic
  benchmark validity unclear. This does not prove controversy caused reach.
- **E3, actual task and measurement:** [ID-lookup evidence](../../../../aliases/01-screen-short-form/data-layout/LOOKUP-RESULTS.md),
  [source](../../../../aliases/01-screen-short-form/data-layout/lookup.cpp), and
  [repeat-run data](../../../../aliases/01-screen-short-form/data-layout/results/2026-09-05/lookup-repeat.json).
  At 4,194,304 players and 1,048,576 ordered active IDs, the repeat medians were
  4.355233 ms and 0.347342 ms, a 12.54x ratio. The first run measured 12.26x.
  Other orders and sizes differ. Both compiled loops were scalar under normal
  `-O3`; vectorization was not disabled. All histories remain stored. No
  hardware-counter evidence isolates the mechanism behind the total gain.
- **E4, novelty:** [Short 4](../../short-04-memory-order/script.md) and the
  [selected layout pitch](../../pitch-lab/2026-09-05/10-unused-fields-slow-the-loop.md).
  Memory locality already appears in the roster. This Short's specific
  contradiction is an unread field affecting the loop's performance.
- **E5, direct feedback:** the learner asked whether scene 1 was slower than
  scene 2, then whether the distinction would be clear to the viewer. This is
  direct feedback on the explanation, not audience-retention data. A planned
  diagram has not yet proved that a cold viewer understands the transformation.

## Required rules

Follow the current [Short-form playbook](../../../production/short-form-playbook.md),
[copy playbook](../../../production/platform-copy-playbook.md),
[visual guidelines](../../../production/visual-asset-guidelines.md), and
[upload gate](../../../../docs/operations/short-upload-gate.md).
Use the [critique procedure](../../../../docs/operations/critique-check.md).
Existing rules cover the lessons unless a genuinely new editorial check is
needed. Do not grow AGENTS.md with round records.

## Invariants carried through every round

- Same idea: an unused history field spaces scores apart; compare the actual
  indexed lookups before and after separating the score storage.
- Preserve data, player IDs, query order, additions, and result. Show that the
  histories remain. Do not replace this with a full sequential scan or time
  only the already-selected scores after discarding the other players.
- Keep ordered IDs, dataset size, and normal optimization visible with any
  numerical claim. Timing covers lookups, not allocation or layout conversion.
- Do not claim universal speedup, measured cache-miss reduction, or a known
  winner for the unrun score-plus-history lookup follow-up.
- First-frame code/image, hook caption, curiosity text, and annotation work
  together immediately. Use selective yellow/teal emphasis and purposeful
  annotations and presenter movement through the whole Short.
- One canonical spoken script per version, with `>` for read-aloud text. Use
  simple professional English, no em dash, no canned corporate cadence, no
  introduction or spoken machine specifications.
- Keep code shots within 14 preferred / 17 maximum lines. Scripts stay here;
  camera fragments remain under the shorts code alias. Do not edit benchmark
  kernels, compiler flags, or protected workspace settings for this script loop.
- Target 18-19 seconds without stretching a shorter read. The exact final
  export must be below 20.000 seconds; this cannot be verified from word count.
- Complete the payoff, ask a genuine adjacent question, connect it to a
  concrete next test, and cut. No request to follow, like, or visit a profile.
- Candidate search language: C++ performance, data layout, hot/cold splitting,
  score lookup. Platform keywords, titles, captions, and hashtags need their
  own research before publication. They are not SEO-approved by this exercise.

All rounds are editorial hypotheses. Keep Instagram evidence separate from
YouTube, TikTok, and long-form. Final rendered-media checks remain unverified.
