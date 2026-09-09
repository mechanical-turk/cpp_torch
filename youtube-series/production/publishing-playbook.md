# Publishing Package Checklist

Read this before creating, rewriting, reviewing, or approving a `publishing.md`
for any format or platform. Use the [template](publishing-template.md).
This document owns the package workflow and scoring. The linked playbooks own
the underlying copy, media, and operations rules; read the applicable sources.

## Required workflow

Every new or rewritten package must contain the following, in this order.
This is mandatory without a separate critique request.

1. **Checklist plan:** the first section after the document title. Explain how
   this release will attempt every P01-P18 item before writing its copy. Give
   the intended wording, evidence, verification, or action and known risk.
   Name the format, selected platforms, review date, and preparation stage here.
   Include an applicability reason for conditional items. A promise to comply
   is not a plan, and a plan is not a completed check.
2. **Publishing content:** the actual release package, including the exact
   upload filename near the start, assets, settings, research records, and
   separately labeled, copy-ready platform fields. Keep internal instructions
   outside public-copy blocks. Give one canonical version of each field.
3. **Checklist audit:** assess that exact package against every P01-P18 item.
   State PASS, PARTIAL, FAIL, UNVERIFIED, or justified N/A; cite the field or
   inspected evidence, award points, and name the fix for every shortfall.
   Evaluate each selected platform separately where the rule is platform-specific.
   Do not paste the intentions from the opening table as evidence of a pass.
4. **Critique:** identify the most important remaining weaknesses, explain their
   effect on discovery, trust, usability, or release safety, and propose a
   concrete repair. Prioritize inaccurate claims, weak search choices, generic
   copy, wrong links, and failed media checks over cosmetic edits. Do not pad
   the critique or dilute a correct, strong position just to sound cautious.
5. **Final score:** calculate the checklist score out of 100, name the assessed
   stage and platforms, and give the decision and unresolved blockers.

Use this order in both the saved file and a full publishing-package response.
For a brief handoff, link the file and summarize its decision rather than
repeating all its tables. The checklist belongs inside `publishing.md`, not
only in a chat message or detached review file.

Apply this to the next package created or rewritten. Do not bulk-rewrite old
publication records. For a small correction, preserve unrelated copy and
records, update any existing affected audit rows, and recalculate the score.
If the creator requests only one platform, explicitly scope the package to it;
do not generate or publish the other platforms just to fill the checklist.

## Checklist

Weights total 100 before explicitly inapplicable items are excluded. They are
editorial priorities, not measured ranking factors. SEO is a required audit,
not an optional final polish or a synonym for adding hashtags.

### Content, search, and language

- [ ] **P01 | Content truth and scope | 10 points.**
  Identify the release, format, audience, selected platforms, final artifact,
  and exact demonstrated subject. Compare the copy with final media/captions
  and relevant code or results, not just the script. Support numerical claims
  and technical explanations; distinguish measured results from hypotheses.
  Do not generalize one benchmark or claim unfinished work. List unavailable
  evidence and the exact claims it prevents us from approving.
  Source: [copy playbook, content truth](platform-copy-playbook.md).

- [ ] **P02 | Independent platform SEO research | 15 points.**
  For every selected platform, record date, sources checked, owned-account
  evidence, candidate phrases, primary phrase, supporting terms, retained and
  rejected hashtags, reasons, and unavailable evidence. Use current relevant
  platform evidence; do not recycle one platform's research as another's.
  Cite actual sources and observations, never invented search volume or an
  unsupported claim that a choice is optimal. Unavailable autocomplete is not
  automatically a failure if other credible evidence supports the decision;
  no research record or no usable evidence is UNVERIFIED.
  Source: [copy playbook, research template](platform-copy-playbook.md).

- [ ] **P03 | Accurate keywords in the actual copy | 10 points.**
  Map the chosen primary and supporting terms to the title, opening line,
  description/caption, and other relevant fields on each platform. Put the
  strongest accurate subject phrase near the beginning naturally. Name the
  language and central concept when useful. Verify that the content fulfills
  each term; avoid stuffing and unrelated popular topics. Evaluate the
  published wording, not merely the existence of a keyword list.
  Source: [copy playbook, search language](platform-copy-playbook.md).

- [ ] **P04 | Hashtags and backend tags | 8 points.**
  Audit visible hashtags separately from YouTube metadata tags. Explain each
  retained term or coherent group, including relevant standalone topics and
  specific phrases; do not omit useful broad identifiers merely because a
  compound contains them. Do not add broad terms the video fails to fulfill.
  Research hashtag use separately per platform; reject decorative or invented
  compounds without evidence. No `#shorts`. YouTube descriptions normally
  contain no hashtags. An intentional, reasoned choice of no hashtags can pass.
  Source: [copy playbook, tags](platform-copy-playbook.md).

- [ ] **P05 | Natural, professional language | 10 points.**
  Audit every public field, including first comments, replies, alt text, and
  announcements. Use simple active English, useful opening words, natural
  cadence, professional capitalization, and clear paragraph breaks. Remove
  filler, corporate phrasing, forced lowercase, fake intimacy, canned
  contrasts, abrupt setup/relabel transitions, and em dashes. Do not open
  announcements with `Episode N is out` or add the banned one-C++23-file
  boilerplate. SEO does not excuse awkward language.
  Source: [copy playbook, voice and platform rules](platform-copy-playbook.md).

### Platform fields and audience interaction

- [ ] **P06 | Titles, identity, and platform fit | 5 points.**
  Supply the fields each selected platform actually supports. Long-form
  YouTube titles lead with the subject, use exactly one `|`, and end with
  `Deep Learning, All the Way Down #N`; use a colon for another separation.
  X and LinkedIn episode announcements name the episode and series after the
  technical opening. Standalone Shorts need an accurate concrete title, not
  a false series-episode claim. Instagram and TikTok captions identify the
  topic immediately; keep TikTok compact. Check current field limits and
  account/interface support rather than assuming every destination is identical.
  Sources: [copy](platform-copy-playbook.md), [long-form](long-form-playbook.md).

- [ ] **P07 | Correct links and previews | 5 points.**
  Verify known destination URLs and replace placeholders as soon as URLs
  exist. X and LinkedIn episode announcements get exactly one previewable
  external URL, the YouTube episode; secondary navigation belongs in the
  appropriate author reply/comment. No external URL in Instagram Reel captions
  or first comments, or TikTok captions. Reddit uses its separate community
  rules and GitHub-first ordering. Inspect the actual composer preview before
  posting; link ordering alone cannot prove how a card renders. Record a
  legitimate link-free choice explicitly.
  Sources: [copy](platform-copy-playbook.md),
  [distribution](../../docs/operations/distribution.md).

- [ ] **P08 | Useful first comments and replies | 5 points.**
  Include specifically planned first-comment and required navigation-reply
  copy. New long-form episodes have no closing Q&A, required answer key,
  automatic answer comment or associated pin reminder. Prepare a useful
  content-specific candidate using the long-form playbook's first-comment
  section; distinguish a prepared candidate from an authorized or posted
  comment. Short
  comments support the actual demonstration and invite meaningful discussion
  without adding unsupported claims or generic engagement demands. Preserve
  a genuine next-experiment promise without inventing its result or date.
  No GitHub link in YouTube pinned comments. Include duplicate inspection
  before posting and direct comment/reply URL reporting afterward. Do not
  invent a comment obligation merely to fill this field. Never repeat pin
  checks. Do not claim these actions happened from a prepared draft.
  Sources: [long-form](long-form-playbook.md), [short-form](short-form-playbook.md),
  [platform operations](../../docs/operations/platform-operations.md),
  [engine check](../../docs/operations/engine-check.md).

### Files, presentation, and upload readiness

- [ ] **P09 | Real upload filename and file identity | 4 points.**
  State the exact descriptive, lowercase kebab-case upload filename for each
  platform, with the language/domain and central concept, without stuffing.
  Keep the same basename for an identical master. Verify the actual file,
  not only the proposed name. If it still has an internal export name, state
  the required upload-copy action and keep that verification pending. Link
  the source file without confusing a rename plan with a completed rename.
  Source: [visual guidelines, filenames](visual-asset-guidelines.md).

- [ ] **P10 | Thumbnails, covers, and real crops | 4 points.**
  Name each asset and its platform/surface, verify the actual dimensions and
  small-screen legibility, and inspect the applicable composer/grid previews.
  Use the current visual guidelines and, for long-form YouTube thumbnails,
  thumbnail research. Preserve branding without blindly resizing one cover
  for every platform. Instagram requires its own technical cover treatment,
  conservative central safe area, and real grid-crop verification. Do not
  substitute a local crop simulation for the destination preview or assume
  custom cover controls exist. Missing previews remain UNVERIFIED.
  Sources: [visual guidelines](visual-asset-guidelines.md),
  [YouTube thumbnail research](youtube-thumbnail-research.md) when applicable.

- [ ] **P11 | Exact final media and Short upload gate | 6 points.**
  Record the final path, review date, file identity, measured dimensions,
  duration, and relevant codec/audio properties. Review playback, sound,
  captions, and code readability, not just metadata. Apply the resolution
  standard and its historical exceptions. For new vertical releases, include
  all four Short upload-gate results with the required hash, first-frame
  image, annotation/gesture timecodes, and precise duration. A script, cover,
  or earlier export cannot pass the final-media gate. A failed or missing
  required result holds upload approval regardless of this package's score.
  Sources: [resolution](video-resolution-standard.md),
  [Short upload gate](../../docs/operations/short-upload-gate.md).

- [ ] **P12 | Settings, navigation, and processing | 3 points.**
  Specify visibility, intended audience, language, category where supported,
  comments, and applicable sharing controls. Keep comment sorting separate
  from moderation and do not promise that sorting reveals held comments.
  Identify the correct playlist, related video, and long-form Subscribe plus
  complete-playlist end screen on the clean tail after the sign-off.
  Shorts do not need arbitrary manual playlist sorting. Keep actual
  settings/processing pending until inspected, and hold YouTube publication
  until the required playback resolution is available. A saved draft or an
  API limitation cannot establish that Studio-only settings passed.
  Sources: [engine check](../../docs/operations/engine-check.md),
  [platform operations](../../docs/operations/platform-operations.md),
  [resolution](video-resolution-standard.md).

- [ ] **P13 | Captions and long-form chapters | 4 points.**
  Check technical caption terms against the recording. For long-form, derive
  timestamps from downloaded captions and actual transitions, compare with
  the local script, and preserve the valid live chapter block in subsequent
  edits. Begin `00:00 Introduction`, end `Recap`, and follow the engine check's
  timestamp and label limits. Split long sections at genuine topic changes,
  not arbitrary intervals. Review sections longer than five minutes for
  meaningful subdivisions rather than leaving a large section unexamined.
  Recheck after trims. If captions or timing evidence do not exist yet, record
  the specific follow-up and leave chapter verification pending; never invent
  finished timestamps. Do not add artificial chapters to a brief Short.
  Sources: [platform operations](../../docs/operations/platform-operations.md),
  [engine check](../../docs/operations/engine-check.md).

### Distribution, usability, and follow-through

- [ ] **P14 | Distribution plan grounded in current state | 3 points.**
  Read the timeline and standing cadence before timing recommendations.
  Include selected platforms, sequence, proposed window in Eastern Time,
  rationale, dependencies, and explicit deferrals. Separate native Shorts
  from long-form announcements. Long-form packages include X and LinkedIn
  copy, the Reddit decision, and a separate Shorts plan. Treat Reddit as a
  strategic channel, not an automatic duplicate episode post. Do not infer
  causality from one posting time or mark a schedule saved without evidence.
  Sources: [distribution](../../docs/operations/distribution.md),
  [timeline](../../docs/distribution-timeline.md), [cadence](posting-cadence.md).

- [ ] **P15 | Public source matches the episode | 2 points.**
  For long-form, identify the recording's source checkpoint and verify the
  README, episode links, build instructions, capabilities, and public/pushed
  state against the public GitHub playbook. Record missing work rather than
  imply that a future implementation is available. For a standalone Short,
  do not imply the series repo hosts its benchmark; verify any code link
  actually offered. This item is N/A only when the scoped package has no
  applicable public-source requirement or code link.
  Source: [public GitHub playbook](public-github-playbook.md).

- [ ] **P16 | Copy-ready fields and tooling compatibility | 2 points.**
  Keep each public field separate from research, instructions, and caveats
  meant only for the creator. YouTube descriptions contain plain text, not
  Markdown styling; Markdown can organize this local package. Keep backend
  tags out of description blocks. Verify character limits, local links, exact
  URLs, and the absence of unresolved placeholders in fields called ready.
  Preserve the supported YouTube parser headings listed below and inspect a
  dry-run diff before any authorized metadata application.
  Sources: [copy](platform-copy-playbook.md),
  [platform operations](../../docs/operations/platform-operations.md).

- [ ] **P17 | Honest audit and score | 2 points.**
  Are all checklist IDs planned and audited with actual field/evidence
  references, per-platform outcomes, point arithmetic, and actionable critique?
  Distinguish draft, verified, approved, scheduled, and published. Keep unknown
  evidence unknown, explain every N/A, and do not present intended checks as
  complete. Re-audit affected items after changing the copy, links, or media.
  Source: this workflow and the scoring rules below.

- [ ] **P18 | Post-publication and recordkeeping handoff | 2 points.**
  Specify the automatic live-post checks, first-comment/reply actions, direct
  URL reporting, and append-only timeline updates still required after release.
  Name blockers and who must act. Respect authorization and platform capability;
  preparing or scoring a package does not publish, schedule, send a comment,
  trigger an engine check, or authorize destructive operations. A concrete
  follow-up plan satisfies this planning item; it never proves live actions
  completed. Reconcile live state when publication is reported or discovered.
  Sources: [post-publication check](../../docs/operations/post-publication-check.md),
  [platform operations](../../docs/operations/platform-operations.md),
  [distribution](../../docs/operations/distribution.md).

## Scoring and stage decisions

| Status | Credit | Standard |
| --- | ---: | --- |
| PASS | Full weight | The check is satisfied with cited wording or evidence for the stated stage. |
| PARTIAL | Half weight | Some requirements are met; name the remaining defect. |
| FAIL | Zero | A requirement is absent, contradicted, or fails inspection. |
| UNVERIFIED | Zero | The necessary evidence or check is unavailable. Name it. |
| N/A | Excluded | The item genuinely does not apply to the format or selected platforms. Explain why. |

Score each ID once. For platform-specific checks, show each platform's outcome
and use the lowest credit among applicable platforms as the item's credit.
Do not average away missing TikTok research with a successful YouTube audit.
A platform-specific ready decision must cite its own evidence even when other
platforms remain blocked.

Show the arithmetic: `earned points / applicable maximum x 100`. With no N/A
items, the maximum is 100. Otherwise list every exclusion and round the
normalized result to one decimal. Missing files, unsupported actions, pending
captions, uninspected previews, or lack of time are not reasons to mark N/A.
For a limited correction, label a limited-review score rather than claiming
the entire release has just passed.

The score measures package compliance, not expected SEO rank, reach, or CTR.
There is no numerical score that overrides a required gate. All applicable
checks must PASS before claiming full package compliance. Until then, use
`revise` for fixable copy/package defects or `hold` for missing proof, access,
or failed release gates. A high score with a blocker remains a blocked package.

Always state readiness separately:

- **Copy readiness, per platform:** P01-P08 and P16 must pass their applicable
  copy requirements. Unavailable preview verification still blocks posting,
  even if the text itself is approved.
- **Upload readiness:** requires actual file, media, cover/interface evidence,
  and every applicable Short upload check. Do not mark it ready from a plan.
- **Public-release readiness:** additionally requires saved settings, intended
  resolution processing, live-state checks available at that stage, and an
  explicit release decision. Post-publication tasks remain pending until done.

Identify which checks are future-stage work rather than pretending they failed
in the live platform or passed in advance. P14 and P18 assess concrete plans;
P09-P13 require actual verification where their wording calls for it.
Use a final line such as:

`Score: X/100 (earned/applicable). Decision: revise/hold/ready for [stage].`

Then identify the platform scope if it is not already explicit. A ready
recommendation is not authorization to perform the release.

## File structure and parser safety

The first H2 must be `## Checklist plan`. The content phase comes next and
can span multiple H2 sections. The last three H2 sections are
`## Checklist audit`, `## Critique`, and `## Final score`.

For a package consumed by `tools/youtube-channel/`, preserve these exact H2
headings inside the content phase:

- `## Final title`
- `## YouTube description`
- `## Suggested tags`

`## Pinned comment` is optional. Omit it when no comment is planned; the
metadata tool must skip comment inspection, posting and pin reminders in that
case. Keep this exact heading when supplying actual comment copy. Never put
"None", "N/A" or an internal instruction into a public-copy block.

The current parser searches H2 headings; nesting them under `### YouTube`
breaks extraction. Put the public value first in a plain `text` fence beneath
each supported heading. A fenced block is local packaging, not text to paste
into YouTube. Do not create multiple competing blocks under the same field.
Do not rename existing fields or tools just to add this wrapper.

## Maintenance

Keep per-release observations, audits, scores, and research in that release's
`publishing.md`, with external events in the append-only timeline. Keep this
checklist reusable. If an underlying rule changes, update its authoritative
playbook and reconcile the corresponding check instead of adding a second rule
to AGENTS.md. The template is a scaffold, never evidence that checks passed.
