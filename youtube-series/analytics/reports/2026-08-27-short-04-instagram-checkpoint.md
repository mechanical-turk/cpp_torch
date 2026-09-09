# Short 4 Instagram checkpoint: August 27, 2026

## Observation

The August 27 9:42 AM ET refresh captured Short 4 approximately 20 hours and
58 minutes after its Instagram publication. The closest available checkpoints
for Shorts 2 and 3 are approximately 23 hours and 17 minutes and 25 hours and
48 minutes after publication, respectively:

| Short | Age | Plays | Reach | Avg. watch | Avg. runtime watched | Interaction rate | Save rate | Share rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Short 2: unsigned loop | 23.3h | 10,399 | 7,320 | 15.65s | 58.9% | 0.82% | 0.14% | 0.09% |
| Short 3: overflow check | 25.8h | 3,323 | 2,335 | 15.72s | 66.4% | 1.50% | 0.45% | 0.06% |
| Short 4: cache locality | 21.0h | 19,104 | 13,817 | 18.08s | 55.7% | 1.33% | 0.26% | 0.15% |

At comparable ages, Short 4 produced 1.84 times Short 2's plays, 1.89 times its
reach, and three times its interactions. It produced approximately 5.7 times
Short 3's plays and 5.9 times its reach. Its current interaction breakdown is
165 likes, nine comments, 50 saves, and 28 shares. The Instagram account grew
from 26 to 32 followers between the August 26 8:43 PM and August 27 8:35 AM
refreshes. That account-level change overlaps Short 4's distribution window but
cannot be attributed entirely to one Reel.

Short 4 did not win every stage of the funnel. Its 18.08-second average watch
is the highest in absolute seconds, but its 32.46-second runtime makes that only
55.7% of the Reel. Shorts 2 and 3 averaged approximately 58.9% and 66.4% of
their shorter runtimes at the comparison checkpoints. Short 4's interaction
rate per account reached is stronger than Short 2's but slightly lower than
Short 3's. Its share rate is the strongest of the three.

User-supplied Instagram Insights screenshots at approximately 9:50-9:51 AM ET
added fields that are not available in the API snapshot:

- 19,161 views and 13,818 viewers;
- 18-second average watch time;
- 10 follows attributed by Instagram to the Reel;
- 35.7% skip rate, labeled `Typical` by Instagram;
- 0.2% share rate, labeled `Higher`;
- 1.2% like rate, 0.4% save rate, and 0.1% comment rate, each labeled `Lower`;
- 0.0% repost rate, labeled `Higher`; and
- 84.8% of views from the Reels tab, 13.8% from Explore, 0.3% from the
  profile, and 0.3% from Feed.

The screenshots' retention graph shows its sharpest decline near the opening
and then a more gradual decline through the 32-second endpoint, but it does not
display exact per-second values. No exact points should be inferred from the
curve image.

## Profile-visit funnel

The learner later supplied 49 profile visits attributed to the Reel. Against
13,818 unique viewers, that is a 0.355% viewer-to-profile-visit rate, or 3.55
profile visits per 1,000 viewers. The reported 10 follows divided by 49 visits
is 20.4%, but this should not be treated as a proven sequential conversion rate.
Instagram reports profile visits and follows as separate actions attributable
to a Reel, and a viewer can follow from the Reel surface without first opening
the profile. Preserve both raw counts and use `10 / 49` only as a directional
profile-conversion proxy.

There is no rigorous universal public benchmark for organic Reel-to-profile
visits. The strongest large-sample 2026 Reel study found during research covers
140,000 Reels and publishes reach, engagement, skip, repost, length, and posting
frequency, but not profile visits. Public practitioner thresholds vary widely:
some flag less than 1% as weak, some use 2% for posts with an explicit profile
CTA, and others call 3-5% high. These sources do not disclose a comparable
organic-Reel dataset, account maturity, audience source mix, or consistent
attribution window, so they are directional heuristics rather than defensible
percentiles. Short 4's 0.355% is below all of those heuristics and deserves a
controlled test, but it cannot honestly be assigned a public percentile.

Flick's public account-level benchmark defines conversion as new followers
divided by profile visitors and reports a January 2025 average of 13.49% across
4,078 accounts, with the preceding five months near 18%. This is not a
Reel-level cohort and therefore is not directly comparable, but it supports the
learner's view that the downstream profile conversion is not the clearest leak.

Research sources:

- Socialinsider 2026 Reel study and methodology:
  https://www.socialinsider.io/blog/instagram-reels-statistics/
- Flick public Instagram conversion benchmark:
  https://www.flick.social/learn/instagram-analytics-benchmarks/insights/conversion-rate/3-months
- CreatorIQ metric definitions distinguishing profile visits and follows:
  https://21030792.fs1.hubspotusercontent-na1.net/hubfs/21030792/CreatorIQ_Metrics%20Guide.pdf
- Practitioner profile-visit heuristic, included only as directional evidence:
  https://www.creatorscope.io/blog/how-to-analyse-your-reels-without-expensive-tools

## Interpretation

This is the second five-figure Instagram discovery event in the current series
and materially strengthens the evidence that cold distribution is repeatable.
The size of the gain came primarily from wider distribution, while downstream
response remained solid. It did not come from the strongest normalized
consumption or engagement rate.

The strongest directly supported positive signal is sharing, not an unusually
low skip rate. Instagram labels the 35.7% skip rate `Typical` while labeling the
0.2% share rate `Higher`, and it lists those factors in that order of importance
to reach. Meanwhile, the like, save, and comment rates are all labeled `Lower`.
This narrows the interpretation: the Reel achieved broad algorithmic discovery
and an above-typical share response without broadly outperforming Instagram's
other engagement-rate norms.

The source mix confirms that this was overwhelmingly discovery distribution:
98.6% of views came from the Reels tab and Explore, versus only 0.6% from the
profile and Feed. The 10 Reel-attributed follows establish content-level
conversion that the API snapshot could not expose. This is approximately 0.07%
of unique viewers. It is a gross attributed count and should not be equated with
the account's net follower change over the same period.

A concrete, quantified performance contradiction remains a plausible reason the
Reel was shareable. The Insights screenshot confirms that the Reel is represented
by a graphic showing `1.7 ms`, `71.1 ms`, and `41x slower`. It does not establish
when that graphic appeared in the live video or which creative element caused
sharing. The final live media must be inspected before treating opening wording,
first-frame treatment, or reveal order as observed variables.

The profile-visit bottleneck is consistent with a Reel that was useful to share
but did not establish a reason to investigate its source. The verified live
caption and result graphic deliver a complete standalone lesson: the two loops,
the measured difference, and the cache-locality explanation. They do not name a
specific continuation, recurring format, or additional result waiting on the
profile. A viewer can understand it, send it to a programmer, and keep scrolling
without needing anything from the account. This is a plausible explanation,
not a proven cause, because the final live video itself was unavailable for a
complete frame-by-frame inspection.

The nearly empty Reel grid cannot explain the low viewer-to-profile-visit rate;
viewers have not seen the grid before deciding whether to tap. It can affect the
next stage after a visit. The 20.4% directional follow-per-visit proxy and
Flick's lower account-level benchmark suggest that the earlier Reel-to-profile
bridge is the more useful immediate experiment.

The production script schedules the exact `1.7 ms` versus `71.1 ms` benchmark
visual for `00:21-00:27`, which begins later than the Reel's 18.08-second
average watch time. The final live Instagram edit has not been frame-checked to
confirm that the planned cue remained at exactly 21 seconds. Average watch time
also does not reveal how many individual viewers reached that cue, especially
when replays are possible. Treat the late planned reveal as a pacing risk and
test an exact measured result in the opening five seconds; do not treat it as a
measured drop-off point.

Short 4 also differs from the prior experiments in topic, opening question,
benchmark framing, duration, publication time, cover, and hashtag set. The
available evidence cannot identify which variable caused the larger test. In
particular, nothing here demonstrates that its hashtags caused reach. Its live
profile cover also has a known crop defect, so the result is not evidence that
the cover implementation was successful.

## Next-content decision

Promote **This billion-iteration loop takes zero time** as the next Short, but
make profile intent the primary experiment. Defer the separate opening-form and
shorter-runtime experiments so multiple changes do not obscure the result.

- Inspect the final Short 4 media first and preserve its actual opening form,
  reveal order, pacing, and runtime as closely as the new topic permits.
- Use a real optimized-build measurement and one optimizer mechanism.
- Completely resolve the optimizer-deletion lesson, then expose the adjacent
  technical question: `So the next question is whether the compiler ran the
  loop at all, or just computed the answer.` Cut immediately.
- Do not mention following, the profile, the account, social media, or future
  content. Do not withhold the promised technical payoff.
- Keep every essential cover element inside the centered 1080x1080 profile-grid
  safe area and inspect Instagram's real grid preview before publication.

Judge that experiment primarily by profile visits per 1,000 unique viewers,
while guarding skip rate, average watch, and share rate. The first internal
target is not a claimed industry norm: improve from 3.55 to at least 7 profile
visits per 1,000 viewers without materially weakening sharing or consumption.
Build the real benchmark from the next 10 Reels rather than relying on
unverifiable public rules of thumb. The hypothesis is that a genuine adjacent
technical question can create creator curiosity without asking for a profile
visit; the experiment must be judged by behavior, not by how clever the ending
sounds.

After this profile-intent test, run the previously proposed opening experiment:
show the exact measured result within five seconds and target 20-25 seconds.
Do not use either result to relax the evidence requirement for platform tags
and hashtags.
