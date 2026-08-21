# Cross-platform content analysis: August 20, 2026

Snapshot captured at approximately 6:50 PM ET. YouTube, X, and Instagram were
refreshed directly before this analysis. LinkedIn's latest manual count is 759
at 12:52 PM ET; TikTok's stored count is stale and should not be treated as a
current zero after Short 3 was published there.

## Executive finding

The clearest current signal is not simply that short-form works. A short,
concrete program failure with an immediate explanation is materially
outperforming a more abstract tensor-semantics lesson. The comparison is still
only two Shorts and contains topic, timing, and platform-distribution
confounds, so it establishes the next format experiment rather than a permanent
rule.

Long-form continues to convert a small number of viewers into subscribers, but
the opening minute remains the primary bottleneck. Episode 3's processed
retention confirms that the earlier episodes' opening collapse was not isolated.

## Audience snapshot

| Platform | Current audience | Earlier baseline | Change |
|---|---:|---:|---:|
| YouTube | 22 subscribers | 16 on Aug 17 | +6 |
| X | 226 followers | 224 on Aug 17 | +2 |
| Instagram | 8 followers | 0 on Aug 17 | +8 |
| LinkedIn | 759 followers | 755 on Aug 17 | +4 |
| TikTok | unavailable in current dashboard | 0 before first post | unknown |

Audience change is temporally associated with the releases but cannot be
assigned to individual posts unless the platform reports that conversion.

## Short-form comparison

### Instagram

| Metric | Tensor shapes Short | Unsigned-loop Short |
|---|---:|---:|
| Runtime | 34 seconds | 27 seconds |
| Views | 1,147 | 13,965 |
| Accounts reached | 1,026 | 9,757 |
| Average watch | 7.68 seconds | 15.87 seconds |
| Approx. average percentage watched | 22.6% | 58.8% |
| Views per reached account | 1.12 | 1.43 |
| Interactions | 9 | 111 |
| Likes / comments / saves / shares | 6 / 0 / 1 / 2 | 71 / 11 / 18 / 11 |

The second Reel reached 9.5 times as many accounts, held attention for 2.1
times as long, generated more replaying, and produced 12.3 times as many total
interactions. Its saves and comments show that the reach was not purely empty
autoplay traffic.

Plausible contributors are the concrete contradiction in the title and first
sentence, immediately visible code, a single causal mechanism, a shorter
runtime, and a payoff that does not require prior tensor knowledge. The data
does not isolate which contributor caused the improvement.

### YouTube Shorts

| Metric | Tensor shapes Short | Unsigned-loop Short |
|---|---:|---:|
| Public view counter | 99 | 868 |
| Processed views | 97 | 167 |
| Engaged views | 53 | 75 |
| Average view duration | 20 seconds | 18 seconds |
| Average percentage viewed | 59.61% | 66.76% |
| Subscribers gained | 0 | 1 |

The public counter and processed Analytics use different definitions and are
also affected by processing delay, so they should not be combined. The
comparable processed metrics still favor Short 2 on percentage viewed and
subscriber conversion. Its retention curve shows replay behavior above 100%
near the opening and approximately one third of the engaged audience at the
end. The API still does not expose Studio's exact stayed-to-watch versus
swiped-away card.

### X

The only native Short with complete X video telemetry remains the tensor-shape
Short: 1,227 impressions, 799 playback starts, 148 plays through 25%, 54
through 50%, 35 through 75%, and 19 completions. It achieved reach but lost
most playback before the explanation. Short 2 has not been captured as a native
X-video comparison, so no format conclusion can be transferred to X yet.

## Long-form

| Episode | Processed views | Average duration | Average viewed | Subscribers gained |
|---|---:|---:|---:|---:|
| 1 | 165 | 68 seconds | 3.08% | 7 |
| 2 | 75 | 47 seconds | 2.82% | 0 |
| 3 | 32 | 30 seconds | 1.48% | 1 |
| 4 | 3 | 270 seconds | 33.91% | 0 |

Episode 4 has only three processed views and cannot yet be evaluated. Its 22
public views are not evidence for or against the revised structure.

Episode 3's retention is the decision-relevant update. Audience watch ratio is
53.1% around the first 1% of the video, 18.8% around 2%, 9.4% around 3%, and
3.1% around 4%. For a roughly 34-minute video, that corresponds to a collapse
inside approximately the first 80 seconds. Together with Episodes 1 and 2,
this supports changing the lesson order, not weakening the technical depth.

Long-form conversion remains encouraging despite weak consumption. Episodes 1
and 3 have generated eight reported subscribers from 197 processed views. The
series premise appears capable of converting the right viewer; too few viewers
currently reach the substance.

## X distribution

Episode announcement reach has fallen from 944 and 872 impressions for the
first two launches to 113 and 129 for Episodes 3 and 4. Episode 3 still earned
an 11.5% engagement rate and Episode 4 approximately 7.0%, but neither produced
a reported link click. This sample cannot distinguish audience fatigue, link
post suppression, launch novelty, or timing.

The personal post about the series becoming real produced 13 profile visits
from 265 impressions, a 4.9% profile-visit rate. Personal/process posts remain
useful as a relationship layer even when they do not directly drive YouTube
clicks.

## Decisions

1. Continue long-form, but judge the next episodes primarily on first-minute
   retention. Put a real contradiction, failure, or completed calculation in
   the first 20 seconds and begin changing code by roughly 30 seconds.
2. Chapter 6 should use its real `{1.0, -1.0}` residuals to demonstrate
   cancellation immediately. Do not wait for a separate hypothetical example
   before exposing why plain summation fails.
3. Run the next two Shorts as controlled repetitions of Short 2's structure:
   one concrete failure or surprising result, visible code immediately, one
   mechanism, 20-30 seconds, and no long CTA.
4. Publish every Short natively on YouTube, Instagram, X, and TikTok so the same
   creative receives a true cross-platform comparison. Record exact URLs and
   timestamps.
5. Do not add more distribution channels this week. The highest-value work is
   producing the next strong Short and improving the next long-form opening.
6. Recheck Episode 4 after enough processed views exist. Do not change its title
   or thumbnail based on the present three-view Analytics sample.
7. Keep personal X posts, but stop expecting episode-link announcements alone
   to grow reach. Technical native posts and genuine process observations serve
   different funnel stages.

## Next checkpoints

- Capture Short 2's Instagram and YouTube metrics again at approximately 72
  hours.
- Capture TikTok Short 3's first manual 24-hour metrics, including followers,
  views, average watch time, completion, likes, comments, saves, and shares.
- Re-evaluate Episode 4 when its processed Analytics sample is large enough to
  produce a retention curve; until then, treat its strong average duration as
  anecdotal.
