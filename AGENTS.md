# Codex Operating Index

This repository runs the production, publishing, distribution, and analytics
operation for Deep Learning, All the Way Down. It is not the demonstration-code
repository.

## Mission

Build a durable audience around rigorous deep learning, modern C++, and systems
content. Respect the viewer's time, keep the technical work accurate, and use
evidence to improve delivery without diluting the subject.

## Universal rules

- Read the documents routed below before acting. Do not rely on remembered rules
  from an earlier session.
- Final media, live platform state, captions, and checked-in code outrank a
  production script when establishing what actually happened.
- Never invent a publication, timestamp, URL, metric, code state, or completed
  task. Mark unavailable evidence unknown.
- Preserve user changes and unrelated dirty-tree work.
- Keep `script.md` ready for recording: narration, scene directions, exact code
  edits, and the descriptive media filename only. Put checklist plans, audits,
  critique, scores, and editorial rationale in `script-review.md`; keep keyword
  research in `keyword-research.md`. Still perform every required review step.
- Perform routine authorized, non-destructive operations directly. Ask before
  expanding authority or taking destructive action.
- Before posting a comment or reply, inspect existing account-authored comments
  and never create a functional duplicate.
- After every external write, state exactly what changed, provide the direct
  public URL, and update the distribution timeline.
- Keep secrets and raw private analytics outside tracked files.
- If browser control cannot connect, ask the creator to open Chrome and the
  Codex app, then retry immediately. Do not spend repeated diagnostic cycles
  on a closed browser or app.

## Knowledge-base map

Read only the documents relevant to the task, but read every required document
in that route.

| Task or trigger | Required documents |
| --- | --- |
| Any public title, description, caption, comment, post, profile text, alt text, tag set, hashtag set, or upload filename | `youtube-series/production/platform-copy-playbook.md` |
| Create, rewrite, review, or approve a `publishing.md` | `youtube-series/production/publishing-playbook.md` and its applicable source playbooks; require checklist plan first, publishing content, checklist audit, critique, and final score |
| Long-form planning, scripting, review, or packaging | `youtube-series/production/long-form-playbook.md`; complete keyword research and L01-L16 review workflow; keep the recording script and supporting review in separate files |
| DaVinci Resolve editing, date-ordered assembly, speech cuts, dialogue cleanup, playback speed, or final video export | `youtube-series/production/edit-playbook.md`; also read the resolution and visual-asset standards it links; preserve the creator's latest manual edit |
| Short, Reel, TikTok, or vertical-video planning and scripting | `youtube-series/production/short-form-playbook.md`; complete its checklist plan, audit, critique, and score in `script-review.md`; reserve `script.md` for recording |
| Blender or animation work | `youtube-series/production/animations-playbook.md` |
| Short, Reel, or TikTok final-export review, upload approval, or release readiness | `docs/operations/short-upload-gate.md`; `youtube-series/production/platform-copy-playbook.md` |
| Thumbnail, diagram, overlay, banner, cover, crop, or export | `youtube-series/production/visual-asset-guidelines.md`; for YouTube long-form thumbnails also read `youtube-series/production/youtube-thumbnail-research.md`; for resolution read `youtube-series/production/video-resolution-standard.md` |
| Release timing, announcement, repost, or channel distribution | `docs/operations/distribution.md`, `docs/distribution-timeline.md`, `youtube-series/production/posting-cadence.md` |
| Reddit planning | `docs/operations/distribution.md`, `youtube-series/production/reddit-engagement-research-2026-08-29.md`, `youtube-series/production/reddit-distribution-strategy.md`, and current subreddit rules |
| YouTube Posts or subscriber Community | `youtube-series/production/youtube-community-growth-research-2026-08-29.md` |
| Public long-form repository or README work | `youtube-series/production/public-github-playbook.md` |
| YouTube, X, Instagram, TikTok, or LinkedIn account operations | `docs/operations/platform-operations.md` |
| Content performance analysis or analytics interpretation | `docs/operations/analytics-and-evidence.md`, `docs/operations/native-performance-analysis.md`, and the latest relevant dated report; native screenshots, extracted curves/engagement and dashboard evidence are required |
| `engine-check` | `docs/operations/engine-check.md` and every document it names |
| `situation check` | `docs/operations/situation-check.md` and every document it names |
| `critique check` | `docs/operations/critique-check.md` and the relevant creative playbooks it names |
| Newly published content | `docs/operations/post-publication-check.md` |

## Standing commands

### `engine-check`

Run the complete procedure in `docs/operations/engine-check.md`. Refresh default
dashboard data before giving an opinion. The default X refresh includes account
and follower data only. Tweet-level data requires an explicit request.

### `situation check`

Run `docs/operations/situation-check.md`. Keep formats and platforms separate,
compare matched ages where possible, and distinguish observation, explanation,
and next test.

### `critique check`

Accept `critique check`, `critique-check`, and `run critique check`. Follow
`docs/operations/critique-check.md`: pitch, critique, record the lesson, apply it,
and repeat. For an open Shorts search, default to twenty distinct concepts;
when a specific pitch is supplied, refine that pitch instead. Honor explicit
scope and round counts. Finish with one recommendation and its unresolved
proof checks. Editorial selection does not approve recording or upload.

### Automatic post-publication check

When new content is reported or discovered, immediately run
`docs/operations/post-publication-check.md`. Do not wait for a command.

## State, evidence, and records

Before the next content pitch or script, consult the latest relevant performance
report and open creative experiments. Apply their findings explicitly; do not
rely on conversation memory or mix platform and format conclusions.

- `docs/distribution-timeline.md`: append-only observable production and
  distribution ledger. Keep plans separate from completed events.
- `youtube-series/analytics/reports/`: dated, decision-relevant analysis.
- `docs/logs/analytics-observations.md`: append-only chronological analytics
  observations.
- `docs/logs/content-experiments.md`: append-only experiment plans and results.
- `youtube-series/content-ideas.md`: uncommitted content backlog.
- Active episode and Short `publishing.md` files: release-specific truth and
  platform copy.
- External demonstration repository git history: authoritative episode code
  checkpoints.

Do not put raw metrics, release bookkeeping, OAuth work, one-off hypotheses, or
dated experiment records in this file. Add them to the correct append-only log,
timeline, package, or report. Promote a conclusion into a playbook only when it
is durable, supported, and changes future work.

## Knowledge-base maintenance

- `AGENTS.md` is an index and universal-rules file. Keep it short.
- Playbooks contain current normative instructions. Each rule should have one
  authoritative home.
- Logs are append-only. Correct an old entry by appending a dated superseding
  entry, not by rewriting history.
- Reports contain detailed analysis and may be superseded by later reports.
- Publishing packages contain release-specific research, copy, assets, and
  checks. Do not promote their temporary details into global rules.
- When adding a new playbook, add one routing row here and remove duplicate
  instructions elsewhere.
- When evidence changes a rule, update the relevant playbook and append the
  supporting observation or report reference.

## Repository locations

- Content operation: this repository.
- Long-form demonstration code:
  `/Users/keremkazan/Documents/Projects/deep-learning-all-the-way-down`
- Workspace alias for long-form code: `aliases/02-screen-long-form`
- Short-form experiment code: `/Users/keremkazan/code`
- Workspace alias for short-form code: `aliases/01-screen-short-form`

Before release or distribution advice, read `docs/distribution-timeline.md` so
the recommendation reflects the current state.
