# Native performance analysis

Required whenever the creator requests content performance analysis, including
informal questions about why a post worked or stalled. This supplements API
data; an API refresh alone does not complete the analysis.

## Capture and publish evidence locally

1. Identify the post, platform, format, publication time and analysis window.
   Read the latest relevant report. Never combine Shorts and long-form results.
2. Capture screenshots from the platform's own insights screens. Use Instagram
   iOS through iPhone Mirroring for phone-only data, YouTube Studio for Studio
   data, and the relevant native analytics surface elsewhere. An export is
   preferable for precise curve points, but preserve screenshots as evidence.
3. Capture overview, retention, engagement, conversion and available traffic /
   audience breakdowns. Record missing screens explicitly. For iPhone Mirroring,
   the phone must be locked and idle. Reacquire app state once after a control
   failure; if it still fails, explain the exact blocker and request help. Do
   not spend repeated cycles attempting the same broken action.
4. Save originals in the gitignored analytics/private area. Extract displayed
   counts and curve points into a timestamped native snapshot using the
   dashboard's [import format](../../tools/analytics-dashboard/README.md#native-platform-evidence).
   Every metric and curve point must link to its source screenshot. Preserve
   native labels, units, filters, time window and capture time. Use null for
   unavailable values. Label exact tooltip values, rounded counts and visually
   estimated curve points separately. Never reconstruct a curve from average
   watch time or interpolate estimates into purported exact measurements.
5. Inspect the final media and transcript. Mark the actual opening, animation
   start/end, code reveal, payoff, engagement question, continuation promise and
   cut, with video-relative times. Scripts establish intent, not actual delivery.
6. Import the snapshot into the local dashboard. Verify the record, curve,
   metrics, screenshot links and creative annotations are accessible. Preserve
   every capture; do not overwrite history or silently replace API snapshots.
   Keep audience and content summaries at the top of the dashboard. Retention,
   source screenshots and qualitative detail belong inside the selected post's
   expanded view, not above the cross-platform overview.
7. Write observed facts, plausible explanations, next test and limitations in
   the dashboard record and a dated report when decision-relevant. Append an
   observation to the log. Name missing data and incomplete capture steps in
   the handoff rather than claiming the full workflow passed.

Do not expose private screenshots on a public Site. Do not pull X post metrics
unless explicitly requested. Do not run unrelated publishing operations.

## Evaluate animations

- Align retention with each animation's exact start, explanatory action and end.
- Inspect local drop and retention into the next beat, not just overall average
  watch time. Distinguish clarification, decorative motion and delayed delivery.
- Compare similar topics, duration, opening strength, publication age, audience
  and traffic sources on the same platform. Annotate all differences.
- One flatter segment does not prove the animation helped. Use repeated matched
  tests, changing one major creative variable where practical. Log the cost in
  screen time and production effort as well as possible retention benefit.

## Evaluate the continuation outro

Test the actual spoken version of "Next, I'm testing X", not its planned script.
Preserve the thought-provoking question immediately after the payoff. Do not
trade away discussion to improve a single conversion percentage.

- Track attributed follows per 1,000 views and per 1,000 unique viewers/reached
  accounts when available, clearly naming each denominator.
- Track profile visits, bio clicks, absolute follows, end retention, comments,
  shares, saves, absolute reach and their rates alongside conversion.
- Follows / profile visits is not a measured conversion funnel: viewers can
  follow directly from the Reel. Channel follower growth is not automatically
  attributable to this post or to the outro.
- Aggregate insights do not reveal whether a follower heard the outro. Do not
  infer an outro-exposed conversion rate from final retention.
- Compare matched-age captures from several posts with and without a concrete
  next-test promise. Account for topic, cold-audience mix and concurrent Reddit
  or other distribution. State uncertainty and sample size.
- A candidate win improves audience growth while preserving discussion and
  distribution. Mixed outcomes stay mixed; record the next test, not a universal
  rule based on a single post.

## Feed the next script

Before suggesting or writing the next relevant script, read the latest native
analysis and open experiments. State what will be preserved, changed and tested,
with evidence references. Promote only supported durable lessons to the creative
playbook; keep capture metrics and experiments in their dated records.
