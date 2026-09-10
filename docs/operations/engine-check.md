# Engine Check

This is the procedure for `engine-check` and `run engine check`.

## Start

1. Run `make analytics-sync` before forming an opinion.
2. The default refresh may collect X account and follower data, but never
   tweet-level metadata. Run `make x-post-analytics-sync` only when the creator
   explicitly requests X post performance.
3. Read:
   - `docs/distribution-timeline.md`
   - `youtube-series/production/posting-cadence.md`
   - active `publishing.md` packages
   - the latest relevant analytics report
4. Reconcile plans and local records against live platform state wherever the
   available API or authenticated browser supports it.

## Release audit

For every active release, check:

- New Shorts prepared from September 5, 2026 onward pass
  `docs/operations/short-upload-gate.md` against the exact final export. Read
  that procedure and verify its four recorded results and file hash before
  clearing upload readiness. A missing or failed result holds approval.
- Every selected platform has its own current keyword and hashtag research
  record and passes `youtube-series/production/platform-copy-playbook.md`.
- New or rewritten `publishing.md` packages follow
  `youtube-series/production/publishing-playbook.md`: checklist plan, content,
  item-by-item audit, critique, and final score. Verify the cited evidence and
  stage-specific blockers; a high score does not override a failed gate. Do
  not bulk-reformat historical packages or treat their old layout as a defect.
- YouTube visibility, title, plain-text description, tags, thumbnail, audience,
  comments, captions, chapters, playlist, related video, cards, and end screen.
- Every long-form video belongs to the main playlist. Every Short belongs to the
  Shorts playlist. Add missing membership directly.
- Every long-form end screen contains Subscribe and the complete-series
  playlist. This is a Studio-only check when the Data API cannot expose it.
- New long-form episodes, starting with Episode 8, have no closing Q&A or
  required answer comment. Do not flag a missing answer key/comment or issue
  an automatic pin reminder. Preserve historical comments. Only audit other
  comments explicitly planned in the release package, including a selected
  technical discussion comment from the long-form playbook. A draft candidate
  is not authorization to post. Inspect existing
  channel-authored comments before posting and report the direct URL.
- Public long-form descriptions contain valid chapters derived from recorded
  captions: `00:00 Introduction`, at least three increasing timestamps, at
  least ten seconds per chapter, titles no longer than 28 characters or five
  words, and `Recap` as the final chapter. Add missing chapters directly.
- YouTube descriptions contain no Markdown presentation syntax.
- Every long-form release received its X announcement and playlist plus GitHub
  navigation reply.
- Every planned LinkedIn announcement, normally one or two days later, was
  published or explicitly rescheduled.
- Every Short reached every platform selected in its package.
- Reddit and other planned distribution actions were completed, deferred with
  a reason, or cancelled. Review Reddit weekly, answer substantive replies, and
  capture the 24-hour, 48-hour, 72-hour, and seven-day checkpoints.
- Decision-relevant analytics checkpoints, audience counts, and public GitHub
  stars are current.
- Recording, editing, thumbnail, upload, and next-release dependencies are not
  stale or at risk.
- The final local master passes `ffprobe`. Episode 6 is the final 2560x1440
  exception. Later masters must be 3840x2160 for long-form or 2160x3840 for
  vertical video. Hold YouTube publication until intended processing is ready.
- Upload filenames are accurate, descriptive, lowercase kebab-case, and contain
  the language and central subject without keyword stuffing.
- The public long-form GitHub repository passes
  `youtube-series/production/public-github-playbook.md`.
- No action is overdue, duplicated, contradicted by live state, or missing its
  known timestamp or URL.

Perform routine authorized, non-destructive corrections directly. Isolate only
genuinely manual or blocked actions. Never infer completion from a plan.

## After an external write

Report exactly what changed and provide the direct public URL. Record the event
in `docs/distribution-timeline.md`.

## Report format

1. `Missing or overdue now`
2. `Manual verification required`
3. `Upcoming next`
4. `Confirmed complete`

Lead with the next action. Keep tooling details out of the report unless they
explain a blocker.
