# Native insights workflow and Short 5 baseline

September 7, 2026. Instagram Short 5 only. This does not establish performance
on YouTube, TikTok, or long-form content.

## Evidence now available

Captured Instagram iOS through iPhone Mirroring. The private dashboard record
`20260907T1404-instagram-short05` contains four original screenshots: Overview,
Engagement, native rate diagnostics, and retention / traffic sources. Capture
session: 13:57–14:04 UTC. This is a lifetime snapshot roughly five days after
publication, not a matched-age comparison with an earlier post.

The dashboard displays extracted engagement and conversion metrics, a sampled
retention curve, source links and creative-beat annotations. Curve points are
visual estimates from a small native screenshot, not exported data. The stated
±4 percentage-point reading tolerance is approximate, not a statistical
confidence interval. Intermediate points also have uncertain time alignment.

Beat annotations reuse the actual recording inspection in the
[September 2 report](2026-09-02-short-05-instagram-retention-and-creative-analysis.md).
They do not claim a new frame-by-frame inspection today.

## What this baseline can tell us

The opening still loses viewers fastest, while the subsequent curve is
shallower. The recording ends with the CPU question and cuts; it does not
contain a concrete next-test promise. It is therefore a question-only baseline,
not evidence that the proposed continuation outro improved follow conversion.

Keep comments, shares, saves, end retention and absolute reach alongside follows
when testing that addition. More follows per view is not an unqualified win if
distribution or useful discussion deteriorates.

The recording's annotations, captions and hand movement differ from the planned
clay animation. Their co-occurrence with retention cannot establish whether that
animation will help. Align future animation starts/ends with the curve and
compare repeated, similar posts before promoting a conclusion.

## What remains unknown

- No exact retention export or end tooltip was obtained. Average watch time is
  not completion and can reflect replay behavior.
- Native diagnostic rate definitions/denominators were not inspected. Preserve
  them separately from calculated view-based rates.
- Aggregate follows do not reveal which viewers heard the outro. Profile visits
  are not a required step before following.
- Screens were captured over seven minutes, not atomically; Audience tab
  breakdowns were not captured in this implementation pass.
- No animation or next-test outro treatment/control comparison exists here.

## Workflow change

[Native performance analysis](../../../docs/operations/native-performance-analysis.md)
is now required by AGENTS.md for future content-performance requests. The local
dashboard has a validated append-only importer, source screenshots, curve and
metric provenance, estimates labeled separately, capture history, timed creative
events and qualitative notes. Capture remains an agent-operated native UI task,
not an unattended phone scraper or part of the default API-only sync command.

Before the next script, read this evidence and open experiments, state the
specific creative change being tested, and preserve the engagement guardrails.
