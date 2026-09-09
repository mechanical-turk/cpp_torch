# Analytics and Evidence

## Evidence hierarchy

For viewer-visible claims, prefer:

1. the live platform rendering;
2. the final media master;
3. captions or a transcript derived from the recording;
4. checked-in code for code-state claims; and
5. the production script only as planned intent.

If stronger evidence is unavailable, label the detail planned or unknown. Never
use a script as proof of wording, timing, visual order, code shown, runtime, or
CTA in a performance conclusion.

## Analysis rules

For content performance requests, follow
[Native performance analysis](native-performance-analysis.md). Capture native
screenshots, extract retention and engagement with provenance, surface them on
the local dashboard, and align findings with the final video's creative beats.

- Keep platforms and formats separate.
- Separate reach, opening conversion, consumption, engagement, conversion, and
  audience growth.
- Compare matched ages and like formats when possible.
- Distinguish observed facts, plausible explanations, and next tests.
- Never infer causation from a coincident title, hashtag, time, topic, or visual.
- Preserve missing and stale values as such.
- Compare each source record's own capture or update time when several sources
  report the same metric. A pipeline refresh time must not make an older
  provider value appear current. For TikTok followers, prefer the newer of the
  public profile observation and the Phyllo profile record while retaining
  Phyllo for indexed content metrics.
- Track timestamped YouTube subscribers; X, Instagram, TikTok, and LinkedIn
  followers; and stars on the public long-form GitHub repository. Never
  overwrite history with the newest count.
- The local dashboard is the primary human view. It must preserve platform
  definitions, freshness, and unavailable data rather than creating a universal
  view score.

## Where evidence belongs

- Raw private snapshots: gitignored platform analytics directories.
- Decision-changing analysis: dated files in
  `youtube-series/analytics/reports/`.
- Chronological observations: append to
  `docs/logs/analytics-observations.md`.
- Active controlled tests: append to `docs/logs/content-experiments.md`.
- Durable supported rules: promote a short version into the relevant playbook
  and cite the report or log entry.

Do not place raw metrics, one-off hypotheses, or dated experiment bookkeeping in
`AGENTS.md`.
