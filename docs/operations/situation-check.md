# Situation Check

This is the procedure for `situation check`, `situation-check`, and
`run situation check`. It explains current performance and the next content
test. It is not a full operations audit.

## Collect evidence

1. Run `make analytics-sync`.
2. Inspect all configured platforms, the distribution timeline, recent reports,
   and the final media or captions for the content being compared.
3. Default X collection includes account and follower data only. Fetch X post
   analytics only after an explicit request.
4. Mark unavailable, stale, delayed, or manually supplied data. Never convert
   unknown values to zero.
5. Follow [Native performance analysis](native-performance-analysis.md): capture
   native insights, import curves and engagement to the dashboard, and align
   them with final-media beats before drawing creative conclusions.

## Compare correctly

- Compare like formats at matched ages when possible.
- Keep each platform's view, play, reach, and impression definitions separate.
- Separate reach, opening conversion, consumption, engagement, conversion, and
  audience growth.
- Treat scripts as plans. Verify viewer-visible variables from final media,
  captions, or the live post.
- Account for sample size and distribution stage.

For every result, state:

1. **Observed:** the measured difference.
2. **Plausible explanation:** the best-supported interpretation.
3. **Next test:** the smallest controlled change that can test it.

Inspect topic, promise, opening sentence, first frame, visual sequence, runtime,
pacing, code density, CTA, packaging, timing, platform, and distribution. Do not
credit a coincident variable with causation.

## Finish

- Turn the strongest evidence into one or two specific creative experiments.
- Write a dated report under `youtube-series/analytics/reports/` when the result
  changes a decision.
- Append the checkpoint to `docs/logs/analytics-observations.md`.
- Promote a lesson into a playbook only when it is durable and supported.
- Record the checkpoint and next action in the distribution timeline.
- Do not edit live metadata or publish anything without separate authorization.

## Report format

1. `What is outperforming or underperforming`
2. `What probably changed the result`
3. `What to carry into the next content`
4. `Next controlled experiments`
5. `Limits and missing data`
