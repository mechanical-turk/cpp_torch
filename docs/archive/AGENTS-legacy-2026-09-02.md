# Codex Operating Instructions

These instructions govern every Codex session in this repository.

## Purpose

This repository is the content-production operation for *Deep Learning, All
the Way Down*: a YouTube series (and its X, Instagram, TikTok, and LinkedIn
presence) teaching deep learning and modern C++ from first principles. It is
not a library. It holds the distribution ledger, analytics tooling, episode
scripts and publishing packages, visual assets, and the standing operating
rules below. The series' own demonstration code lives outside this
repository.

The north star is a durably growing, high-quality series: rigorous technical
substance, delivered so people actually watch, distributed without diluting
that substance for reach.

## Mandatory copy and SEO playbook

Before writing, revising, approving, or publishing any audience-facing copy,
read `youtube-series/production/platform-copy-playbook.md` and apply its full
release gate. This includes titles, descriptions, captions, comments, social
posts, profile copy, alt text, tags, hashtags, upload filenames, and every
`publishing.md` package.

Do not reduce SEO to adding keywords after the copy is written. Conduct and
record current platform-specific keyword research first, select the language
from that evidence, then write and audit the copy. Copy is not final when any
selected platform lacks its own keyword and hashtag research record. Never
reuse another platform's research record as a substitute.

## Reference implementation

- The series' own demonstration code — the actual `Tensor` class viewers
  watch get built live — lives outside this repository, at
  `/Users/keremkazan/Documents/Projects/deep-learning-all-the-way-down`. Its
  `main.cpp` is a running checkpoint: each commit captures the code exactly
  as an episode leaves it (for example, `022c750` is "chapter 04 - matmul").
  Read this file before writing or revising any chapter's live-coding beats;
  do not assume a prior chapter's script was followed verbatim on camera.
- This checkpoint file is a working scratchpad, not camera-ready prose: it
  keeps scratch test-numbered variable names (`matmul_23`, `weights_`,
  `scalar_16`, and similar) and inline test assertions from whatever state
  testing left them in. A chapter's script may rename these on screen as
  part of its own live-coding beats, but the beat must start from what the
  file actually contains, not from a cleaner name an earlier script merely
  planned to use.
- Treat that repository's git history as the authoritative timeline of what
  code state existed after each recorded episode.

## GitHub is a primary distribution channel

Treat the public source repository as part of every release, not merely as a
place to store demonstration code. Its current state must present the same care,
accuracy, and professionalism as the videos and platform copy.

The repository currently lives at
`/Users/keremkazan/Documents/Projects/deep-learning-all-the-way-down` and is
available inside this workspace through `aliases/02-screen-long-form`.

- Every public long-form episode must have a corresponding checkpoint commit on
  `main`. The commit must preserve the code state reached by the episode rather
  than a cleaner state imagined by its script.
- The public README must remain synchronized with the latest public episode. It
  must identify the current checkpoint, describe only capabilities present in
  the checked-in code, link every published episode to its exact checkpoint,
  provide verified build and run commands, and state the next major milestone
  without presenting speculative work as complete.
- Compare the README, git history, published titles, live video URLs, final
  captions when relevant, and actual source code. Scripts describe intent but
  do not override recorded or checked-in evidence.
- Compile and run every current public entry point after a release-facing code
  or README update. Never publish build instructions that have not been tested.
- Confirm that the release commit is pushed to `origin/main`, the working tree
  contains no accidental binaries or secrets, and generated executables remain
  ignored.
- Keep discoverability accurate. The README should naturally name the actual
  C++ and deep-learning concepts implemented so far, but must not claim a
  production framework, a PyTorch replacement, completed GPU support, or any
  other future capability.
- Write public GitHub copy in simple, direct English. Prefer active voice and
  concrete technical terms. Remove corporate language, AI-style cadence,
  filler, and vague claims. Use accurate C++, machine learning, deep learning,
  and systems keywords where they help readers find and understand the work,
  but never stuff keywords or make the prose unnatural.
- When a new episode changes the repository layout, update the layout, build
  commands, current-capabilities section, checkpoint table, and next milestone
  together. Do not append only a new video link while leaving the rest stale.
- Record meaningful GitHub release maintenance in the distribution ledger,
  including the checkpoint commit and README synchronization. Treat stale
  source code or a stale README as a release defect.

Start every session by reading `docs/distribution-timeline.md` for the
current release/production state before recommending any release,
announcement, or distribution action.

## Evidence rule: recorded content overrides production scripts

Never treat a production script as definitive evidence of what appeared or was
said in a published video. The learner does not always follow scripts one to
one during recording or editing. Scripts establish the intended structure only.
For claims about actual wording, timing, visual order, code shown, benchmark
reveal, CTA, runtime, or any other viewer-visible element, inspect the final
media master, the live platform post, or captions/transcript derived from the
recorded video. Prefer the live platform rendering when evaluating what viewers
received. If none of those sources is available, label the detail as planned or
unknown and do not use it as observed evidence in a performance conclusion.

## Primary directive: release and distribution ledger

Codex must keep the production, release, and distribution history of *Deep
Learning, All the Way Down* continuously organized in
`docs/distribution-timeline.md`. This is a primary operational responsibility,
not an optional session-handoff task.

The standing weekly cadence across all channels (long-form, Shorts, native X,
native LinkedIn, episode announcements, personal posts) is maintained at
`youtube-series/production/posting-cadence.md`. Consult it before proposing a
one-off schedule; update it, not a fresh ad-hoc plan, when the cadence itself
needs to change.

Before recommending, scheduling, or evaluating YouTube Posts or the subscriber
Community, read
`youtube-series/production/youtube-community-growth-research-2026-08-29.md`.
Keep the two features distinct: public Posts are the channel's reach,
participation, and audience-research surface; the subscriber Community is a
moderated discussion space. Do not turn Posts into a duplicate upload
announcement feed, invent a universal posting frequency, or claim that post
engagement causes video distribution. Run the documented eight-post experiment
before adopting standing Community-post rules, record each post and its metrics,
and compare like formats and topics only.

- Consult the ledger before recommending a release date, announcement, repost,
  community submission, Short, or other distribution action.
- Record every meaningful event as soon as it becomes known: recording and edit
  milestones, upload and scheduling, YouTube publication, X and LinkedIn posts,
  Reddit submissions, community shares, Shorts, and useful analytics snapshots.
- For each event, preserve the episode, platform, Eastern Time timestamp, URL
  when available, status, and the next dependent action.
- Distinguish exact timestamps from approximate or inferred ones. Never invent
  a missing time, URL, publication, or result; mark it as unknown and reconcile
  it when evidence becomes available.
- Track planned actions separately from completed events. Reschedule or cancel
  stale plans explicitly rather than silently deleting them.
- Use the ledger to prevent simultaneous over-promotion, coordinate spacing
  across platforms, and compare distribution actions with subsequent traffic
  without claiming causation from correlation.
- The current target cadence is three long-form episodes per week, normally
  Monday, Wednesday, and Saturday at 11:00 AM Eastern Time. Treat dates as
  provisional until the edit and release package pass their quality gates; do
  not silently replace this cadence with a weekly schedule.
- Distribution planning must include an organic personal-presence layer, not
  only episode announcements. On most active days, plan one or two concise X
  posts that reveal genuine personality, emotion, humor, curiosity, struggle,
  or behind-the-scenes process. A third post is appropriate only when there is
  a real observation worth sharing; never manufacture filler to satisfy a
  quota.
- Keep personal posts native and self-contained. Do not attach a YouTube link,
  GitHub link, hashtag block, or promotional call to action unless the post
  genuinely requires it. Their purpose is to help people know the person doing
  the work, not to disguise advertisements as personal thoughts.
- Maintain variety across personal posts: production observations, learning
  surprises, technical opinions, honest difficulties, small victories, and
  occasional humor. Avoid repetitive self-deprecation, engagement bait, and
  commentary that diminishes the perceived quality of the series.
- Record published personal posts in `docs/distribution-timeline.md` with their
  exact timestamp and URL when available. Keep unposted drafts separate from
  completed events.
- Reconcile the ledger at every meaningful stopping point in video production
  or distribution work, even when the learner does not request an update.

## Command: `engine-check`

When the learner says `engine-check` or `run engine check`, perform a complete
mechanical operations audit for the series. This is a standing command and must
continue to work after sessions are wiped.

Before forming or sharing any engine-check opinion, run the default dashboard
refresh with `make analytics-sync` and inspect the resulting snapshots. The
default refresh must collect only X account and follower metrics, never tweet
metadata. Pull tweet-level X analytics only when the learner explicitly asks
for tweet or X-post performance data, using `make x-post-analytics-sync`.

Begin by reading `docs/distribution-timeline.md`,
`youtube-series/production/posting-cadence.md`, every active episode or Short's
`publishing.md`, and the latest relevant analytics report. Then reconcile what
we said we would do against what is recorded as complete and, where authorized
tooling exists, against the current platform state.

At minimum, check every active release for:

- whether every selected platform's publishing package passes
  `youtube-series/production/platform-copy-playbook.md`, including a complete
  platform-specific keyword and hashtag research record. Treat missing research
  as an incomplete release package rather than improvising tags or approving
  vague SEO language;

- YouTube publication or scheduling status, final title, description, tags,
  thumbnail, playlist membership, and the intended publication time. Every
  long-form episode must belong to the main series playlist, and every Short
  must belong to the dedicated Shorts playlist. Add missing membership through
  the channel tooling during the check rather than returning it as a learner
  task;
- whether the required first comment was posted and whether its retrieval
  answers reproduce the episode's exact closing questions. Immediately after
  posting a new answer comment, give the learner one direct reminder to pin it
  and include the comment's public URL. Record that the reminder was delivered
  in the distribution timeline. Do not inspect pin status or repeat the reminder
  during later engine checks;
- the end screen on every long-form episode. It must contain both a Subscribe
  element and a playlist element linking to the complete series playlist. Use
  authenticated YouTube Studio browser automation to inspect and add missing
  elements when available. The Data API cannot read or edit end screens, so if
  Studio access is unavailable, report this as a specific manual blocker rather
  than silently treating it as complete;
- other Studio-only items, including related-video assignment, cards, reviewed
  captions, and audience settings when they were part of the release package;
- a missing related-video assignment is a routine channel correction, not a
  learner task. When authenticated Studio control is available, select the
  related video specified by the release package and save it immediately. Only
  report a blocker after attempting the Studio change and confirming that the
  authenticated browser control is unavailable or the platform rejects it;
- whether every public long-form description contains valid YouTube chapters
  derived from the recorded video's captions. The first chapter must begin at
  `0:00`, there must be at least three chapters, timestamps must increase, and
  every chapter must last at least ten seconds. Generate and apply a missing
  chapter list through the local YouTube tooling rather than assigning it to the
  learner;
- whether every public YouTube description is clean plain text. YouTube does
  not render Markdown styling, so literal emphasis asterisks, backticks, fenced
  code blocks, underscore emphasis, and Markdown links must never appear in the
  platform-ready copy. Normalize presentation Markdown through the local
  YouTube tooling while preserving ordinary C++ operators, formulas, bare URLs,
  Unicode bullets, hashtags, and the live chapter block;
- whether each long-form episode received its X announcement at the planned
  interval and the standard playlist-and-GitHub navigation reply;
- whether the corresponding LinkedIn announcement was published approximately
  one to two days later, unless the package explicitly chose another timing;
- whether each Short was published on every platform selected in its package,
  including YouTube, X, Instagram, and TikTok, with its first comment or
  platform-equivalent follow-up when planned;
- whether planned Reddit, Telegram, Hacker News, community, newsletter, blog,
  or other distribution actions were completed, deliberately deferred, or
  explicitly cancelled rather than silently forgotten;
- whether the standing weekly Reddit review occurred, whether a fresh project
  milestone supports a useful community-specific post, whether substantive
  replies on recent posts have been answered, and whether the required 24-hour,
  48-hour, 72-hour, and seven-day Reddit checkpoints were recorded. Reddit is a
  core distribution channel and must never disappear from the engine check
  merely because no new post was scheduled;
- whether scheduled 24-hour, 72-hour, and other decision-relevant analytics
  checkpoints were captured, and whether audience counts and data freshness
  are current;
- whether recording, editing, thumbnail, upload, release-gate, and next-episode
  dependencies needed for the standing cadence are complete or at risk; and
- whether the final media master satisfies the resolution standard. Episode 6
  is the final exception and must be `2560 x 1440`. Every master produced after
  Episode 6 must be 4K: `3840 x 2160` for `16:9` long-form and `2160 x 3840`
  for `9:16` Shorts and other vertical video. Verify the local export with
  `ffprobe` before upload. For YouTube, also hold publication until the intended
  `1440p` or `2160p` quality is actually available on the watch page. Other
  platforms may transcode the upload, so verify the submitted master rather
  than treating the platform's playback resolution as the source artifact;
- whether every file selected for upload has a descriptive, keyword-rich
  filename tied to the content itself. Reject internal-only names such as
  `short-05.mp4`, `episode-07-final.mov`, or `Timeline 01.mp4`. Use concise
  lowercase kebab-case terms that identify the language, central concept, and
  content type, such as `cpp-cache-locality-row-column-scan-short.mp4` or
  `cpp-autograd-chain-rule-computation-graph-episode-07.mp4`. Keep filenames
  accurate and readable; never stuff unrelated keywords or claim that the
  filename alone improves platform distribution;
- whether the public long-form GitHub repository is synchronized with every
  published episode. Compare the live episode list with `git log`, confirm each
  episode has the correct checkpoint commit on `main`, verify local `HEAD` is
  pushed to `origin/main`, and ensure the README's current checkpoint,
  capabilities, file layout, build commands, episode links, commit links, and
  next milestone match the actual code and published content. Compile and run
  every current public entry point, inspect the working tree for accidental
  binaries or secrets, and update a stale README directly during the engine
  check rather than returning it as a learner task;
- whether any planned action is stale, overdue, duplicated, contradicted by
  live state, or missing its timestamp or URL.

Use the available APIs and local tools to verify and perform routine authorized,
non-destructive operations directly. Isolate genuinely manual actions instead
of assigning API-capable work to the learner. Never infer completion from a
plan: mark an item `unknown` until the ledger or live evidence confirms it.

Before posting any comment or reply, retrieve and inspect every existing
account-authored comment on that item. Treat a comment as present when it
already fulfills the intended function, even if wording, whitespace, or link
order differs from `publishing.md`. Exact-string comparison is not sufficient
evidence that a comment is missing. Never create a second account-authored
comment automatically; if an existing comment is incomplete, report the
difference and request an explicit edit or replacement decision.

After every external write, report exactly what was created or changed and
include a direct public link to the resulting post, comment, video, playlist,
or other platform object. An object ID or generic video URL is not an adequate
substitute when a direct comment or post URL can be constructed.

After reconciling, update `docs/distribution-timeline.md` with newly verified
events, current statuses, explicit deferrals or cancellations, and the next
dependent actions. Return a compact engine-check report organized as:

1. `Missing or overdue now`
2. `Manual verification required`
3. `Upcoming next`
4. `Confirmed complete`

Lead with action, omit internal tooling details, and do not bury a missed
release obligation inside general strategy commentary.

## Command: `situation check`

When the learner says `situation check`, `situation-check`, or `run situation
check`, perform a focused content-performance analysis. This is a standing
command and must continue to work after sessions are wiped. It is distinct from
`engine-check`: a situation check explains what the newest performance data may
mean for the next content; it does not default to a complete operations audit.

Before forming or sharing an opinion, run `make analytics-sync` and inspect the
resulting snapshots, `docs/distribution-timeline.md`, the latest relevant dated
analytics reports, and the publishing packages and scripts for the newest
content being compared. Every situation check must refresh and inspect all
dashboard data available for every configured platform, even when the learner
asks for special attention on only one platform. This includes YouTube content
analytics and subscriber count, Instagram Reel analytics and follower count,
TikTok video analytics and follower count, available LinkedIn analytics and
audience data including explicitly labeled manual observations, and any future
platform represented in the dashboard. Identify unavailable, stale, delayed, or
manually supplied platform data rather than silently omitting it.

X is the one content-level exception: the default refresh must collect and
inspect the current X account profile and follower count, but it must not fetch
tweet metadata or tweet-level performance. Run `make x-post-analytics-sync` only
when the learner explicitly requests tweet or X-post performance analysis.

Publishing packages and scripts may identify variables worth checking, but a
situation check must verify those variables against the recorded master, live
post, or recorded captions before describing them as observed changes. When
verification is unavailable, distinguish the planned variable from the actual
content and exclude it from causal claims.

Prioritize the latest one to three releases on each active platform, while using
older content only as an appropriate baseline. Compare like with like whenever
possible:

- use matched publication ages such as 1 hour, 24 hours, 72 hours, or seven days;
- keep platform definitions separate rather than equating YouTube views,
  Instagram plays, TikTok views, X video views, impressions, and reach;
- separate reach, opening conversion, consumption, engagement, conversion, and
  audience growth;
- use public counters only as public counters, and identify processing lag or
  missing Studio-only fields rather than treating them as zero;
- compare Shorts with Shorts and long-form episodes with long-form episodes
  unless the cross-format relationship is the question being tested; and
- account for sample size, content age, and distribution stage before declaring
  an outlier or trend.

For every apparent improvement or decline, identify the concrete variables that
changed, including the topic, intellectual payoff, opening sentence, first
frame, visual structure, progressive disclosure, runtime, pacing, code density,
CTA, cover, title, publication timing, platform, and distribution action. Use
current tag or hashtag research only when assessing those variables. Never infer
that tags, hashtags, timing, or another coincident change caused performance
merely because it was present on a successful post.

State conclusions at three evidence levels:

1. **Observed:** the directly measured difference.
2. **Plausible explanation:** the best-supported reason the changed creative or
   distribution variable may have contributed.
3. **Next test:** the smallest controlled change that can strengthen or reject
   that explanation in the next piece of content.

Look especially for actionable statements such as: this post is outperforming
the relevant baseline; this new hook, first-frame treatment, structure, or payoff
is a plausible contributor; preserve that element in the next content while
holding the other major variables as constant as practical. Also identify
underperformance and say what should not be carried forward. Do not manufacture
an explanation when the data cannot distinguish among multiple changed
variables.

After the analysis:

- translate the strongest evidence into specific instructions for the next
  episode or Short, not generic advice;
- propose one or two controlled experiments and name the variable each tests;
- create or update a dated report under `youtube-series/analytics/reports/` when
  the checkpoint is decision-relevant;
- add only durable, sufficiently supported lessons to this file, with their
  evidence and limits;
- record the analytics checkpoint and next dependent experiment in
  `docs/distribution-timeline.md`; and
- do not publish, edit live metadata, or perform another external write unless
  the learner separately authorizes that action.

Return a compact situation-check report organized as:

1. `What is outperforming or underperforming`
2. `What probably changed the result`
3. `What to carry into the next content`
4. `Next controlled experiments`
5. `Limits and missing data`

Lead with the strongest new signal and make the recommended creative change
immediately actionable.

## Automatic post-publication checks

Whenever the learner reports or Codex discovers that new content has been
published, immediately run the relevant platform's post-publication checks.
Do not wait for an `engine-check` request. Use the live public post, authenticated
platform view, and available analytics or account APIs to verify what viewers
actually received rather than assuming the upload form produced the intended
result.

For every newly published item, verify as applicable:

- the post is public on the intended account and opens from its public URL;
- the correct media plays from beginning to end with working audio;
- the title or caption, hashtags, cover, first frame, and platform crop render
  correctly on the live post and profile surface;
- comments and other intended interaction settings are enabled;
- no accidental audience, privacy, age, copyright, audio, or recommendation
  restriction is visible;
- required playlist, related-content, first-comment, navigation, or other
  platform-specific release metadata is present; and
- the exact publication time, public URL, observed defects, and any corrective
  action are recorded in `docs/distribution-timeline.md`.

For Instagram Reels specifically, inspect both the live Reel and its profile
grid tile. Confirm video playback, audio, caption, hashtags, comments, and the
actual cover crop. The live Instagram rendering is authoritative. A locally
valid cover ratio or nominal safe area never overrides an observed crop. If a
defect can still be corrected safely, fix it or present the exact correction.
If publication makes the defect irreversible, record it as a lesson and apply
the corrected rule to every subsequent release package.

## Primary directive: preserve distribution lessons

Codex must preserve important lessons derived from platform analytics so they
continue shaping future publishing decisions after sessions are wiped. Record
the detailed evidence in dated analytics reports and keep the durable operating
principles here. Do not merely collect metrics; interpret what part of the
distribution funnel they describe and turn the strongest findings into future
experiments.

- Analyze **reach and conversion separately**. Similar impressions do not imply
  similar performance. Ask what happened after the impression: engagements,
  link clicks, profile visits, watch behavior, and subscriptions.
- Episode announcements should lead with the intellectual payoff,
  transformation, paradox, or newly unlocked capability. Do not lead with an
  implementation inventory that is meaningful only after someone already cares.
  Technical details support the promise; they are not automatically the promise.
- Never open an X announcement with `episode N is out`, `new episode`, or other
  release-administration language. The first line must stand on its own as an
  interesting technical observation, contradiction, result, or question. Name
  the episode only after the reader has a reason to care.
- Every X and LinkedIn episode announcement must name the complete series when
  it identifies the episode. Write `Episode N of Deep Learning, All the Way
  Down`, never only `Episode N`. This applies even when the series name already
  appears in the linked video's title, thumbnail, or preview card.
- The initial X comparison established the first concrete example. The Episode
  1 and Episode 2 announcements received essentially identical reach (798 and
  800 impressions), but Episode 1 generated 102 engagements, 20 link clicks,
  and 15 profile clicks versus Episode 2's 19, four, and four. The current
  interpretation is that Episode 1 framed an ambitious journey and concrete
  starting point, while Episode 2 primarily listed features. Therefore Episode
  3 should lead with the capability it unlocks, such as completing a machine
  learning prediction, and only then name the tensor operations involved.
- Treat the opening twenty seconds as part of the lesson's payoff, not as
  administrative space. Episode 1's detailed Studio export, captured on
  2026-08-29, supersedes the earlier API bucket interpretation: it reports
  52.78% absolute retention at position 0, 26.39% near 0:22, and 18.40% near
  0:45. The audience at 0:22 is therefore half the size of the first bucket,
  before the episode-specific tensor lesson begins. A displayed
  destination is only a promise, not a payoff. Future long-form openings must
  resolve or demonstrate one concrete new fact, preferably through an
  observable result or failure, while keeping the series identity to one
  clause. Compress retrieval to the prerequisites needed now and expose the
  first new problem inside the opening minute.
- This retention finding applies to YouTube long-form only. Do not use Episode
  1's long-form retention curve to justify Shorts hooks, pacing, structure, or
  distribution decisions. Analyze each format against its own audience data.
- Episode 1 establishes a serious long-form opening failure, not a general
  rejection of technical depth. Half of the opening audience was gone by about
  0:22 and roughly two-thirds was gone by about 0:45, before the tensor lesson
  had properly begun. Treat a spoken series introduction, roadmap, recap,
  housekeeping, or prolonged visual preface at the start as a known retention
  risk until later long-form evidence contradicts it.
- The Studio exports for Episodes 2-6 confirm that the opening cliff is a
  repeated long-form series problem. Approximate matched retention at 0:30 was
  23.6%, 22.9%, 13.4%, 20.6%, 25.5%, and 28.1% for Episodes 1-6 respectively.
  Every episode lost heavily before one minute, including the 13:19 and 10:59
  episodes. Do not treat shorter total runtime as the solution to poor opening
  conversion.
- Episodes 2 and 3 prove that answering the previous episode's questions near
  the beginning is especially damaging. Their new subjects did not begin until
  3:04 and 4:54, with approximate retention of 6.0% and 3.2% at those moments.
  Retrieval answers belong in the first comment and must never return to the
  beginning of a long-form episode.
- Episodes 4-6 show that removing retrieval is necessary but insufficient. A
  focused 40-60 second explanation of the current topic still postpones the
  work viewers clicked to see. Open by demonstrating or acting on the problem,
  not by describing the sequence of work that will eventually solve it.
- Episode 5 provides the strongest early direction among Episodes 4-6: it begins
  with a specific scalar-bias operation that fails. Preserve the concrete
  failure, but demonstrate it immediately instead of narrating it for a minute.
- The complete Episodes 1-6 comparison is recorded in
  `youtube-series/analytics/reports/2026-08-29-long-form-retention-comparison-episodes-01-06.md`.
- The first minute of a long-form episode is part of the lesson, not a trailer
  for the lesson. It must establish the specific problem and make visible
  progress on it. Do not ask viewers to wait through the series premise before
  receiving episode-specific value.
- Default to a cold open for long-form episodes. Remove greeting, series
  framing, recap, roadmap, and other opening talk unless a few words are needed
  to understand the code already on screen. Start meaningful coding as soon as
  possible.
- Keep long-form coding information-dense. Explain each important line in one
  short, precise beat as it becomes relevant, then continue building. Avoid
  pausing for broad theory, repeated summaries, or implementation details that
  have no immediate payoff.
- Minimize live testing. Add a test, assertion, or diagnostic only when it
  proves a meaningful contract, exposes a failure, or makes a new concept
  observable. Do not spend recording time testing arithmetic or behavior the
  viewer can already see is correct.
- Treat the first seconds of every long-form episode as an attention-and-trust
  contract. Demonstrate immediately that the video understands the viewer's
  reason for clicking and will respect their time. Do not test patience before
  earning trust.
- Do not open long-form episodes with a spoken series introduction by default.
  Identify the series through the title, packaging, a brief lower-third, or one
  natural clause only after the episode's value is clear.
- A long-form opening visual is useful only when it shortens the explanation.
  Keep it to roughly 10-20 seconds, narrate it immediately, and replace it with
  code, a calculation, a failure, or another observable step as soon as it has
  done its job. Never use a silent title card, decorative visual, extended
  diagram tour, or visual roadmap as a substitute for progress.
- Aim to reach the first concrete calculation, code change, program output, or
  visible failure within the first 30 seconds and the first observable payoff
  within the first minute. This is a long-form orientation target,
  not a demand for Shorts pacing or superficial treatment.
- Sustain attention through repeated learning cycles across the episode:
  immediate question or need -> smallest meaningful concept or code change ->
  observable result -> interpretation -> next question. Prefer a new payoff
  every few minutes over one large payoff delayed until the end.
- Introduce definitions, edge cases, prerequisite review, and implementation
  detail when the current step needs them. Preserve rigor, but do not front-load
  it before the viewer understands the problem it solves.
- When reviewing a long-form script, explicitly audit the first 15, 30, and 60
  seconds, the time to first observable progress, and every later stretch of
  uninterrupted exposition. When retention data arrives, compare long-form
  videos at matched elapsed times and annotate local rises against the actual
  transcript before changing the playbook.
- Episode 1's detailed retention curve also shows a smaller but comparatively
  stable technical audience after the opening collapse, with local attention
  increases around tensor construction, tests, indexing, and the unsigned
  reverse-loop failure. Treat this as evidence to move concrete code and
  failure-driven explanation earlier, not to remove depth. The full analysis is
  recorded in
  `youtube-series/analytics/reports/2026-08-29-episode-01-detailed-retention.md`.
- Episode 2's final transcript placed its first new subject at approximately
  3:04 and implementation at approximately 5:09. Episode 2 does not yet have a
  usable retention curve, so this timing is a structural risk and the basis for
  an Episode 4 experiment, not proof of where its viewers left. Use the repeated
  sequence need -> derivation -> code -> observable result instead of a long
  setup followed by a feature inventory.
- Episode 1 did not begin its episode-specific tensor subject until roughly
  2:10 and did not begin live coding until roughly 7:35. Episode 4 therefore
  tests a materially different order: begin changing code within the first few
  minutes, produce an intermediate working result around minute six, deliver
  the main promised computation before hardening, and move exhaustive edge
  cases after the central payoff. Preserve rigor by attaching each derivation
  to the failure it removes, not by postponing code until all theory is stated.
- Episode 1's current processed sample combines weak consumption with strong
  idea conversion: 52 seconds average view duration and 2.37% average viewed,
  but six subscribers from 96 processed views. Treat this as evidence that the
  premise and rigor may be attractive while the delivery order is weak. Do not
  respond by diluting the technical depth; move the technical substance
  forward.
- The first Short's YouTube watch metrics were still unprocessed at its initial
  checkpoint. On Instagram, the same lesson reached 109 accounts but averaged
  5.44 seconds of watch time and received no interactions. Future Short
  experiments should reveal the answer progressively, avoid showing the entire
  comparison in the first frame, use natural spoken notation, keep one central
  contrast, target approximately 20-25 seconds when the idea permits it, and
  finish with a natural open technical door rather than a social CTA. Recheck
  at 24 and 72 hours before declaring a conclusion.
- The second Short provides the first strong follow-up experiment. On Instagram,
  the 27-second unsigned-loop failure reached 9,757 accounts, averaged 15.87
  seconds, and generated 111 interactions, versus 1,026 reach, 7.68 seconds,
  and nine interactions for the 34-second tensor-shape Short. YouTube's
  processed comparison also favors the second Short on average percentage
  viewed (66.76% versus 59.61%) and subscriber conversion (one versus zero).
  Treat this as evidence to repeat a concrete failure, immediately visible
  code, one causal mechanism, and a 20-30 second runtime for the next two
  experiments, not as proof that unsigned loops or any single topic always win.
- Short 4 provides the second five-figure Instagram discovery event. At its
  August 27 checkpoint, approximately 19 hours and 50 minutes after publication,
  the cache-locality Short had 18,100 plays, 13,010 reach, an 18.04-second average
  watch time, and 246 interactions. It had already exceeded Short 2's current
  lifetime plays and reach and produced approximately twice its interactions.
  Treat this as stronger evidence that concrete C++ surprises with an immediately
  legible comparison and measurable payoff can earn repeat cold distribution.
  Do not attribute the result to hashtags, posting time, cache locality, or any
  single creative variable because several changed together. Preserve the
  structure and vary one opening element in the next experiment.
  A matched-age comparison strengthens the reach result but narrows the lesson:
  at approximately 21 hours it had 13,817 reach, 19,104 plays, and 255
  interactions, versus Short 2's 7,320 reach, 10,399 plays, and 85 interactions
  near 23 hours. Short 4 averaged only 55.7% of its 32.46-second runtime,
  however, below Short 2's 58.9% and Short 3's 66.4% at their closest
  checkpoints. Its gain therefore reflects wider cold distribution with solid
  response, not superior completion. User-supplied Instagram Insights then
  showed a 35.7% skip rate labeled `Typical`, a 0.2% share rate labeled `Higher`,
  lower like, save, and comment rates, and 10 Reel-attributed follows. Reels tab
  and Explore supplied 98.6% of views. The supported lesson is algorithmic cold
  discovery with above-typical sharing and real follow conversion, not an
  exceptional skip rate or broad engagement-rate win. Preserve a concrete,
  quantified result that is easy to pass along and verify its actual placement
  in the final media. The initially planned next test was to reveal the exact
  measurement within five seconds and shorten the runtime to 20-25 seconds.
  The same Reel produced only 49 profile visits from 13,818 unique viewers, a
  0.355% visit rate or 3.55 visits per 1,000 viewers. Public sources do not
  provide a rigorous comparable organic-Reel benchmark; published practitioner
  thresholds are methodologically weak and must not be presented as established
  norms. The Reel's complete standalone payoff and lack of a specific
  continuation are plausible contributors to the profile-intent gap. Because
  the learner prioritizes this leak, test a one-sentence open technical door
  next while preserving Short 4's verified live opening structure and pacing
  as closely as practical. The ending must expose a genuine adjacent technical
  question without mentioning the account, profile, following, or future
  content. Defer the five-second
  result and shorter-runtime experiment until afterward. Measure profile visits
  per 1,000 viewers and protect skip, watch, and share performance. Do not
  assume Reel-attributed follows are a subset of profile visits, because
  Instagram reports them as
  separate attributed actions and viewers may follow from the Reel surface.
- Episode 3's processed retention extends the long-form opening diagnosis:
  audience watch ratio fell from 53.1% near the first 1% of the video to 18.8%
  near 2%, 9.4% near 3%, and 3.1% near 4%. Future episodes must expose the real
  contradiction or completed calculation within the first twenty seconds and
  begin meaningful code around thirty seconds when the subject permits it.
- YouTube Studio's August 23 Short-funnel checkpoint shows 2.4K Shorts views,
  1.1K engaged views, 45.8% stayed to watch, and 54.2% swiped away. The
  overflow Short reached 1.4K views with 80.0% average percentage viewed, but
  average percentage viewed is conditional evidence about viewers who stayed;
  it does not describe everyone who was shown the Short. Treat stayed-to-watch
  as the first opening metric, then inspect engaged views, interactions,
  rewatches, and subscriber conversion. A two-hour slowdown is an initial-test
  result, not proof of permanent removal from circulation. Keep testing
  concrete-failure Shorts in the 20-30 second range, changing one opening
  variable at a time. The per-video comparison is more diagnostic: the shape,
  unsigned-loop, and overflow Shorts stayed rates were 55.0%, 53.5%, and
  40.6%, respectively. The overflow Short had the best average percentage
  viewed among engaged viewers but no subscriber conversion, while the
  unsigned-loop Short converted one subscriber. Optimize the opening for
  stayed-to-watch before optimizing the middle for average percentage viewed.
- For the current phase, Short production must prioritize the hook and value
  proposition above everything else. The first spoken sentence and first frame
  must make the problem, surprise, or payoff immediately legible to a cold
  viewer. Do not spend the opening on greetings, series context, setup, or
  terminology. The central value proposition must arrive before background,
  derivation, or implementation detail. Judge the opening first by
  stayed-to-watch rate, then optimize the rest of the Short for completion,
  interaction, and subscriber conversion.
- Treat navigation replies as infrastructure for high-intent readers, not as a
  reach mechanism. Low impressions do not make them useless when they provide
  direct paths to the playlist and repository.
- Continue native technical and personal posts between releases, but do not
  declare a winning format from one or two posts.
- State the limits of every conclusion. Separate observed facts from plausible
  explanations, and use small samples to design the next comparison rather than
  claiming universal causation.
- Before writing any new episode announcement, consult the latest dated report
  under `youtube-series/analytics/reports/` and explicitly apply or test the
  relevant lessons.
- Before posting a YouTube link on X, inspect the video's live
  `twitter:card` metadata. YouTube may emit either `summary_large_image` or
  `player` on a per-video basis even when the custom thumbnail is the same
  1280x720 format. X renders `player` as the compact thumbnail-and-text card;
  changing between `youtube.com/watch` and `youtu.be`, or adding ordinary share
  parameters, does not change YouTube's canonical card type. A separately
  attached native image is not an equivalent fix because clicking it opens the
  image rather than the episode. The durable solution is a branded preview URL
  under our control that serves `summary_large_image` metadata to unfurlers and
  routes human visitors to the YouTube episode. Until that infrastructure is in
  place, consciously choose between YouTube's compact clickable player card
  and a native-image post; do not describe the latter as preserving normal
  card click-through behavior.
- Keep the ledger focused on the learner's observable timeline and next actions:
  recordings, edits, scheduling, releases, social announcements, community
  posts, Shorts, and decision-relevant analytics checkpoints. Update it as soon
  as the learner supplies a timestamp, URL, completion, cancellation, or changed
  plan. Do not clutter it with internal tooling, OAuth/API work, asset creation,
  script preparation, or routine document maintenance unless that work creates
  a concrete learner action or blocker.
- Perform routine authorized YouTube channel operations directly whenever the
  local channel tooling and granted API scopes support them, including playlist
  assignment, metadata reconciliation, comment posting, and analytics capture.
  Do not turn API-capable operational checks into learner TODOs. Clearly isolate
  the rare Studio-only action when YouTube exposes no corresponding API field.
- Track audience size on every platform alongside content performance. Every
  analytics refresh must preserve the available YouTube subscriber count, X
  follower count, Instagram follower count, and any future TikTok or LinkedIn
  follower counts. Never overwrite history with only the latest value; retain
  timestamped observations so absolute change and growth rate can be compared
  with releases and distribution events. Mark unavailable or manually supplied
  counts explicitly rather than treating them as zero.
- Maintain a local, read-only cross-platform dashboard as the primary human
  view of analytics. It must distinguish platform-specific definitions instead
  of collapsing unlike views into a misleading universal score; show data
  freshness and unavailable metrics; separate reach, consumption, engagement,
  conversion, and audience growth; and keep raw private snapshots gitignored.
- Routine dashboard and engine-check refreshes must use `make analytics-sync`.
  On X, this collects only the current follower count and profile metadata.
  Tweet-level metadata consumes API credits and must never be part of a default
  refresh; collect it only after an explicit learner request with
  `make x-post-analytics-sync`.

## YouTube channel operations

- Use the local tool under `tools/youtube-channel/` as the canonical routine
  source for YouTube channel metadata and available analytics. Refresh it before
  analytics-based release or distribution recommendations when the current data
  could materially change the decision.
- Analyze only videos selected by `youtube-series/analytics/config.json`. The
  channel contains historical uploads unrelated to the current series; never
  mix their performance into series baselines, growth conclusions, or release
  decisions.
- OAuth client credentials and refresh tokens must remain outside the repository
  under `~/.config/dlatwd/youtube-analytics/`. Raw analytics snapshots remain
  private under the gitignored `youtube-series/analytics/private/` directory.
- A finalized `publishing.md` and an explicit learner decision to release its
  associated video authorize Codex to perform the package's routine,
  non-destructive YouTube operations: update metadata and tags, upload its
  thumbnail, post its pinned-comment text, create or update the named playlist,
  and add or reorder the video as specified.
- Always run and inspect the package dry-run diff before applying changes. Never
  assume prose written for internal planning is exact platform-ready metadata.
- A package dry run's `already posted` check is only an exact-text check. Before
  posting, independently inspect all channel-authored comments and do not add a
  duplicate when an existing comment already serves the package's purpose.
- Never implement or execute deletion, channel banning, destructive comment
  moderation, or other irreversible YouTube actions under this standing
  authorization. Those require a separate explicit learner request.
- The YouTube API cannot pin comments or manage every Studio-only feature. Post
  the intended comment through the API when authorized, then remind the learner
  once, immediately, to pin it manually. Record that the reminder was delivered
  so no later engine check repeats it. Track related-video assignment, end
  screens, cards, and other unsupported actions as manual or separately verified
  browser steps.
- Write every platform-ready YouTube description as plain text. YouTube does
  not render Markdown emphasis, inline code, fenced code blocks, or Markdown
  links. Use ordinary unadorned prose, bare code and formulas, Unicode `•`
  bullets, and bare URLs. Markdown may still structure the internal
  `publishing.md` document around the exact description block, but none of its
  presentation syntax may leak into the description itself. Before applying a
  publishing package, normalize the description with the local channel tool and
  inspect its dry-run diff. Preserve legitimate operators such as `*` in C++ or
  mathematical expressions.
- After a long-form video's automatic captions become available, download and
  preserve its English caption track beside the episode script. Use the caption
  timestamps as the authority for what happened in the recording and the script
  headings as the authority for the intended conceptual structure. Derive a
  concise `youtube-chapters.txt`, inspect the metadata dry-run, and add the
  validated chapter block to the live description. Cache caption downloads and
  do not repeatedly fetch an unchanged track because caption API requests carry
  substantial quota cost. If automatic captions are not yet available, record
  the chapter task as pending and retry it during the next engine check. Any
  later metadata or publishing-package update must preserve the live chapter
  block unless the learner explicitly replaces it. Name the `00:00` chapter
  `Introduction` consistently across episodes. Format every sub-hour timestamp
  as zero-padded `MM:SS`, including `00:00`, so the description presents a
  visually consistent timestamp column. Keep every chapter title short enough
  to remain fully visible in YouTube's narrow player chapter label: at most 28
  characters and at most five words. YouTube truncation is based on proportional
  visual width and available device space rather than a published hard character
  limit, so these are conservative house limits, not a platform guarantee. Put
  the defining action or noun first, remove filler such as `the`, and inspect
  the real player after publication.
  Name the final chapter `Recap`. Do not use `Review and next steps`, `Closing`,
  or another variant for the last chapter label.

## X account operations

- The local X integration under `tools/social-analytics/` is authorized with
  `tweet.read`, `tweet.write`, `users.read`, and `offline.access`. Use its
  `x-reply` command for account-authored navigation replies rather than asking
  the learner to post them manually when the reply is already authorized by a
  finalized publishing package or an explicit request.
- Always preview an X reply without `--apply` first. Before applying it, the
  command must retrieve the account's live conversation state and refuse to
  create another account-authored reply when one already exists. After a
  successful write, report the direct public reply URL and record it in the
  distribution timeline.
- X posting access does not authorize deletion, direct messages, unsolicited
  replies, or arbitrary new posts. Those require a separate explicit learner
  request even when the app technically has broader permissions.

## Instagram analytics operations

- Use `make instagram-analytics-sync` as the canonical routine source for the
  owned `@mechaturka` Instagram profile and Reel insights. Refresh it before an
  Instagram distribution decision when current performance could change the
  recommendation.
- Instagram credentials must remain outside the repository under
  `~/.config/dlatwd/instagram-analytics/`. Raw snapshots remain private under
  the gitignored `youtube-series/analytics/private/instagram/` directory.
- The current Instagram Login integration is read-only in practice. Do not add
  publishing, messaging, comment-management, or Facebook Page permissions
  unless the learner explicitly authorizes a new capability.
- Do not place raw external URLs in Instagram Reel captions or first comments.
  They are generally not clickable, add friction, and can resemble repetitive
  promotional spam without providing a useful navigation path. Use the
  profile's Links field or a Story link sticker for external navigation. An
  Instagram first comment should add technical value, answer a likely question,
  or invite a genuine response; when navigation is relevant, use a short
  `full series in bio` reference instead of pasting URLs.

## TikTok analytics operations

- Use `make tiktok-analytics-sync` as the canonical routine source for the
  owned `@mechaturka` TikTok profile and video stats, once authorized (see
  `tools/analytics-dashboard/README.md` for the one-time setup). Refresh it
  before a TikTok distribution decision when current performance could
  change the recommendation.
- TikTok credentials (client key, client secret, and OAuth token) must
  remain outside the repository under `~/.config/dlatwd/tiktok-analytics/`.
  Raw snapshots remain private under the gitignored
  `youtube-series/analytics/private/tiktok/` directory.
- Until TikTok is authorized, or if authorization lapses, the analytics
  dashboard and any TikTok reporting fall back to the hand-maintained
  `youtube-series/analytics/private/manual-tiktok.json`. Treat that
  fallback's numbers as `unknown` rather than zero when they are `null`,
  and do not silently report them as current API data.
- The TikTok integration is read-only in practice. Do not add posting,
  comment-management, or additional scopes beyond `user.info.basic` and
  `video.list` unless the learner explicitly authorizes a new capability.

## Video-series scripting

When planning or writing a chapter for *Deep Learning, All the Way Down*:

- Treat discoverability as a primary requirement for every piece of
  audience-facing platform copy. Titles, descriptions, captions, comments,
  profile text, alt text, and publishing packages must lead with accurate,
  subject-specific search terms that describe the actual content. Optimize for
  platform search and SEO before ornamental phrasing, but never stuff keywords,
  repeat synonyms mechanically, or weaken technical accuracy. The important
  language, concept, operation, performance topic, and intended discipline
  should appear naturally near the beginning whenever relevant.
- Before finalizing audience-facing copy on any platform, conduct current,
  platform-specific keyword research. Inspect the owned account's available
  search and traffic-source analytics, live platform search or autocomplete,
  current comparable content, and broader search-demand evidence when useful.
  Research the natural-language terms in titles, captions, and posts separately
  for YouTube, X, Instagram, TikTok, LinkedIn, and any future platform; never
  assume one platform's audience uses the same vocabulary as another's.
- Every publishing package must include a keyword-research record for each
  selected platform, not only a tag or hashtag record. Record the research date,
  tools and APIs consulted, candidate phrases tested, observed evidence, the
  search intent each retained phrase serves, and why the final wording uses it.
  Identify unavailable evidence explicitly. Copy is not final when this record
  is missing.
- Optimize for qualified discoverability and accurate audience matching, not
  raw keyword density. Place the strongest supported subject phrase naturally
  near the beginning, add only terms the content genuinely fulfills, and judge
  results through search impressions, search terms, discovery sources, and
  downstream viewing or engagement when the platform exposes them. Never claim
  that keywords guarantee or independently maximize recommendation reach.
- All audience-facing copy must be free of AI slop, corporate language, and
  manufactured hype. Reject slogan-like fragments, symmetrical contrast
  templates, canned transitions, rhetorical filler, fake intimacy, vague value
  claims, and punctuation used to manufacture drama. Use concrete nouns,
  precise technical verbs, natural sentence lengths, professional
  capitalization, restrained punctuation, and a cadence that a technically
  serious person would actually use aloud. SEO requirements never excuse
  robotic repetition or unnatural prose. Treat this as a release-blocking rule.
- Never use an em dash in any audience-facing copy. This prohibition applies
  to scripts, narration, titles, descriptions, comments, social posts,
  captions, visual text, and publishing packages. Rewrite the sentence with a
  period, comma, colon, semicolon, or parentheses instead. Treat this as an
  absolute series voice rule, not a stylistic preference.
- Do not use conspicuously polished Unicode or typographic symbols in public
  copy when a normal person would naturally type the ordinary keyboard form.
  Use `41x`, not `41×`. Prefer familiar human typing over typography that makes
  the copy look generated or overproduced. Preserve symbols only when they are
  part of code, a formula, a proper name, technically necessary notation, or a
  platform-required normalization; never trade correctness for informality.
- Never use `#shorts` in a description, caption, social post, or metadata tag.
  The format is already known to the platform, and the generic label adds no
  useful subject information.
- Never select YouTube metadata tags or visible platform hashtags from intuition,
  linguistic neatness, or imagined SEO value. Before choosing either, conduct
  current, platform-specific research using available tools and APIs. At minimum,
  inspect the channel's own search and traffic-source analytics, live platform
  search results or autocomplete where available, and comparable current content.
  Use broader search-demand evidence such as Google Trends when it materially
  helps distinguish candidate wording. Platform behavior and search language can
  change, so old assumptions are not sufficient evidence.
- Keep YouTube metadata tags and visible hashtags conceptually separate. Metadata
  tags are backend descriptors; hashtags are viewer-facing links and should not be
  used as a substitute for a strong title and natural description. YouTube
  descriptions should normally contain no hashtags unless research demonstrates
  a specific discovery or navigation benefit for the exact term. Fewer researched
  terms are preferable to a decorative block.
- Reject invented or extremely low-signal compound hashtags merely because they
  describe the topic precisely. Terms such as `#cppperformance`, `#cachelocality`,
  and `#systemsprogramming` receive no presumption of value and must not be used
  without current evidence that real viewers search, follow, or engage with them
  on the target platform. Generic terms receive no presumption either. Relevance
  alone is necessary but not sufficient; demonstrated audience language and
  platform behavior must support the choice.
- Every `publishing.md` must include a short tag-research record for each platform:
  research date, tools or APIs consulted, candidate queries or terms tested,
  observed evidence, and the reason each retained tag or hashtag survived. Record
  unavailable evidence explicitly. Do not finalize or apply a tag set when this
  research is missing, and do not copy one platform's set to another without
  separate evidence.
- After publication, evaluate tags and hashtags through the part of the funnel they
  can plausibly affect: search terms, search impressions or reach, discovery source,
  and qualified downstream viewing or engagement. Do not credit them for unrelated
  recommendation traffic, and use the result to improve the next release's research.

- Maintain uncommitted video, Short, post, and content concepts in
  `youtube-series/content-ideas.md`. Keep this idea backlog separate from active
  scripts, publishing packages, and the distribution timeline. Preserve the
  learner's proposed wording unless a later ideation session explicitly
  develops alternatives.
- Every long-form episode title must include the exact series name
  `Deep Learning, All the Way Down` and its episode number in the form `#N`.
  Capability-led title experiments may change the leading promise, but must not
  remove this canonical series suffix. Use exactly one vertical bar in the
  title, reserved for separating the episode-specific title from the series
  suffix. Separate an episode title from its technical subtitle with a colon.
- Every episode and Short script must list the exact final `.mp4` upload
  filename near the top of the document. Use the same descriptive,
  keyword-rich filename required by the upload checks, and update the script if
  the final export name changes.
- Keep early chapter compilation commands minimal, using only the selected C++
  language standard unless a flag is itself being taught. Introduce warning
  groups such as `-Wall`, `-Wextra`, and `-Wpedantic` later as part of an
  explicit transition into production-grade diagnostics and tooling.
- Use this mandatory long-form chapter skeleton:
  1. begin immediately with the current problem, contradiction, failure, or
     question;
  2. use one concise visual only when it makes that problem easier to grasp;
  3. begin changing, calculating, deriving, running, or testing immediately;
  4. mention `Deep Learning, All the Way Down` briefly only after the viewer
     understands the episode's value; and
  5. end with an itemized recap, a concise next-chapter hook, and retrieval
     questions as the final spoken content.
- A long-form episode may begin with a dedicated visual aid when the visual
  immediately clarifies the episode's problem. Do not require a visual when a
  concrete result, failure, or code example communicates the problem faster.
  When used, keep it brief and do not spend visual space
  repeating the episode title or series title. Use the full canvas for one clear
  diagram, relationship, question, or contradiction that directly supports the
  introduction. Write the narration around what the viewer can see and reveal or
  reference the visual in the same order it is explained. This is not a silent
  title card and must not be decorative. Begin speaking immediately. Do not show
  finished code or disclose a result that the episode intends to derive live;
  use unknowns, a failure, or the current limitation when needed. Every script
  must specify this opening visual before its opening narration.
- An opening visual must include the upstream context required by the episode's
  promise. Do not begin at a derived result when the episode is about tracing
  through the inputs that produced it. For autograd material, show the path from
  model inputs and parameters through the prediction and loss before asking for
  parameter gradients; isolate smaller subgraphs later during the explanation.
- In computation diagrams, values and operations must use visibly different
  shapes. Edges must terminate at the entities they actually describe; never
  let a backward parameter edge appear to terminate at an operation node.
- Make every opening understandable to a viewer entering the series through
  that episode. Do not say "last episode," "last time," or otherwise lead with
  continuity unless a prior result is indispensable to understanding the
  current problem. Restate required prior ideas directly instead of narrating
  the publication sequence.
- Write narration for speech, not for an essay. Prefer connected, conversational
  sentences that sound natural when spoken aloud. Avoid artificial symmetry,
  clipped instructional fragments, slogan-like contrasts, repeated rhetorical
  templates, tidy three-beat cadences, and phrases whose primary effect is to
  sound polished. Read every opening aloud in substance before treating it as
  final; if a capable person would not naturally say it to another person, rewrite
  it.
- Always remember that a viewer is on the other side and their patience is
  limited. Use fewer words, shorter sentences, and simple vocabulary. Move to
  the next useful idea quickly. Avoid word salads, repeated explanations, and
  long preambles. Give only the context needed to understand what is currently
  on screen.
- If an idea has no immediate payoff within the next few moments, do not
  introduce it yet. Delay constructors, helpers, abstractions, terminology, and
  side concepts until the first place they are needed. Show the problem, add
  the idea, and use it immediately.
- Avoid the abrupt AI-style transition `X. That is Y.` in narration and social
  copy, especially constructions such as `That is the problem we solve...`
  immediately after stating a fact. Connect the ideas in one natural sentence,
  explain the relationship directly, or soften the transition with wording such
  as `This is the problem...` when a new sentence reads better. Do not ban the
  word `that`; avoid the conspicuous rhetorical template.
- Avoid the canned contrast pattern `it is not X, it is Y` and close variants
  such as `this is not about X; this is about Y`. State the intended point
  directly. Use a contrast only when the distinction itself carries necessary
  technical meaning, and write it as ordinary prose rather than a slogan.
- Keep social copy professional without making it stiff. Use normal
  capitalization and punctuation. Do not force lowercase as a shortcut to
  sounding casual or approachable.
- Do not manufacture informality with openings such as `say`, `imagine`,
  `picture this`, or similar conversational stage directions. State the actual
  situation directly.
- Prefer one complete explanatory sentence over several dramatic fragments.
  Use paragraph breaks only when the idea genuinely changes, not to create an
  artificial cadence.
- Use the approved Episode 6 announcement as a voice reference: establish the
  concrete technical problem in plain language, explain the surprising result
  without theatrics, and then state what the episode builds and why it matters.
  The desired tone is clear, technically serious, and natural rather than
  promotional, overly polished, or deliberately casual.
- Respect the live-build format. Do not open by showing finished code, final
  output, or a successful end state that does not exist yet. The learner builds
  the implementation while recording. Begin from the code or understanding
  already available, surface the real limitation or failure, and let the viewer
  experience the result when it is actually produced.
- Do not live-code throwaway arithmetic or assertions that merely reproduce a
  result already established by the opening. Every coding beat must introduce,
  exercise, or verify a new capability. Prefer assertions that test the behavior
  implemented during the episode, such as graph construction or recovered
  gradients, over assertions that confirm arithmetic chosen by construction.
- In implementation-led episodes, do not delay the code with a separate
  from-scratch mathematics primer. Introduce each mathematical rule when the
  corresponding implementation needs it, using only enough explanation to make
  that code understandable. Reserve extended derivations for episodes whose
  explicit subject is the mathematics itself.
- Do not use silent slideshows or show a visual before the narration gives the
  viewer a reason to inspect it. Begin speaking immediately and discuss each
  visual while it is visible. When a matched visual sequence is used, keep its
  layout stable and change only the structure needed to express the new idea.
- Treat structured educational visuals as a shared row-and-column grid. Titles,
  subtitles, column headings, column subheadings, operators, and complete visual
  objects must each align on their own common baseline or center. Render and
  inspect every final image before reporting completion.
- Keep the problem and current-episode roadmap adjacent and economical so they
  feel like one continuous transition into new substance. Do not place a
  separate pre-introduction hook before the "Welcome back" opening.
- Do not answer retrieval questions in the next video's opening. Reproduce and
  answer each episode's exact closing questions in that same episode's first
  pinned comment. The corresponding `publishing.md` must contain this answer
  key. Do not silently substitute, rewrite, or omit a question.
- Never include a GitHub or source-repository link in a YouTube pinned comment.
  The answer comment should remain focused on the retrieval answers. A playlist
  link is allowed when it provides useful series navigation, but source-code
  navigation belongs in the description and X navigation reply.
- Place closing retrieval questions after the review and next-chapter teaser,
  not between them. Follow them only with the brief standard sign-off: “That
  brings us to the end of this episode. Thanks for watching, and I will see you
  next time.”
- Every end-of-episode review must include a concise, itemized on-screen list
  of the concepts and implementations covered in that episode. The spoken
  recap should follow the same list so it can be displayed directly during
  editing without requiring a separate summary.
- Keep the entire ending tight: itemized recap, one concise next-episode
  teaser, retrieval questions, the standard sign-off, then the clean end-screen
  tail. Do not explain the lesson again, repeat the recap in prose, or add
  another closing speech.
- The next-episode teaser must also have a concise itemized on-screen list of
  the concrete subjects or capabilities planned for that episode. Keep it to
  approximately three items and make the spoken teaser match the list.
- Reserve approximately five seconds of clean video after the sign-off. Every
  retrieval question must finish and remain readable before this tail begins.
  Use the dedicated tail for the Subscribe element and complete-series-playlist
  element; never place those elements over the questions themselves. Record
  this tail explicitly in every script and verify it in the final export before
  release.
- Keep closing retrieval to at most five questions and prefer approximately
  three. Select the questions that retrieve the chapter's central dependency
  chain rather than attempting exhaustive coverage.
- Format every on-screen retrieval question for a narrow display. Insert
  deliberate line breaks at natural phrase boundaries so no line becomes
  visually cramped, while keeping each question easy to read aloud. Do not
  rely on automatic word wrapping to choose the layout during recording.
- Optimize the long-form chapter only for a natural, coherent 16:9 lesson. Do
  not constrain its composition, narration, or structure to make excerpts work
  as vertical Shorts.
- Plan, script, and record Shorts separately as native standalone lessons. A
  Short may teach an idea also covered by the long-form episode, but it must not
  be treated as an extraction target inside the chapter script.
- Every episode must have a `publishing.md` package before release. It must
  include the final title, YouTube description, pinned comment, chapter markers
  or an explicit note that they remain provisional, platform-specific
  thumbnail and cover references, the exact descriptive media filename to
  upload on each selected platform, tags,
  an X announcement, a LinkedIn announcement, a Reddit decision and draft when
  appropriate, a separately produced Shorts plan, and a release check for the
  five-second end-screen tail plus the Subscribe and complete-series-playlist
  elements.
- Every `publishing.md` package, including packages for native Shorts and other
  video formats, must contain a platform-ready pinned comment. Keep it concise
  outside the required retrieval answer key. Never place a GitHub or source-code
  link in it. When navigation is useful, direct viewers to the most relevant
  full lesson, series playlist, or next action without repeating the entire
  description.
- The X and LinkedIn sections must include platform-ready copy, recommended
  publication timing relative to the YouTube release, and a concise rollout
  strategy. Adapt timing to the actual release day, audience evidence, and
  prior distribution rather than mechanically reusing one schedule.
- Protect the YouTube episode preview on both X and LinkedIn by giving the main
  announcement exactly one externally previewable URL: the episode's YouTube
  watch URL. Do not include the GitHub repository, series playlist, or another
  eligible URL in the main post and do not rely on putting YouTube first or
  last; multiple-link preview selection is not reliable enough to treat ordering
  as a guarantee. Paste the YouTube URL, wait for its preview to render, inspect
  that preview, and only then publish. On X, disclose the playlist and GitHub
  repository in the standard navigation reply. On LinkedIn, place a GitHub or
  secondary navigation link in the first author comment when it is useful, or
  omit it. The disclosure order is therefore: episode promise and YouTube link
  in the main announcement, supporting links only after publication.
- In both sections, refer to the release as `Episode N of Deep Learning, All the
  Way Down`. Do not shorten the announcement copy to `Episode N` alone.
- Do not include `The complete implementation remains one C++23 file using only
  the standard library` or a rephrased equivalent in X or LinkedIn episode
  announcements. This recurring implementation note does not belong in social
  announcement copy.
- Reddit is a core distribution channel and a weekly operating responsibility,
  not an occasional afterthought. Review Reddit opportunities every week and
  include a Reddit decision in every meaningful project-milestone release plan.
  A weekly Reddit action may be a new standalone project post, a tailored post
  in another suitable subreddit, a contribution to a recurring community
  thread, or substantive participation without a link. Record an explicit
  defer when no useful contribution is ready.
- Reddit is still a community-participation channel, not an announcement feed.
  Core distribution does not mean repeated link drops. Check each community's
  current rules and recent submissions, use a new angle and new copy for every
  community, answer substantive comments, and do not repost the same milestone
  to the same subreddit until there is meaningful new work to show.
- Before preparing a Reddit milestone post, consult
  `youtube-series/production/reddit-engagement-research-2026-08-29.md`. Lead
  with one concrete achievement, include enough implementation detail to earn
  the community's attention, place owned links after the substance, and end
  with one question that invites experience rather than generic praise. Prefer
  a useful technical diagram or direct project evidence over a promotional
  thumbnail.
- Also consult
  `youtube-series/production/reddit-distribution-strategy.md`. The first
  r/learnmachinelearning milestone post reached 21,000 views and 115 upvotes,
  became the top post of the day, and coincided with YouTube growing from 46 to
  59 subscribers in roughly 48 hours. This is the strongest qualified external
  distribution result recorded so far. Preserve the successful structure:
  present a concrete multi-episode milestone, show inspectable technical work,
  put the GitHub repository before the YouTube series, and end with one specific
  technical question. Treat the subscriber change as a strong temporal
  association, not complete causal attribution.
- Shorts are native, self-contained vertical lessons recorded separately from
  the long-form chapter. Each plan must name the single idea taught, its hook,
  its relation to the episode, its intended publication window, and the related
  long-form YouTube video when that feature is available.
- Treat the hook as the live-or-die beat of every Short. The first frame and
  first spoken sentence must expose the strongest concrete result,
  contradiction, failure, or question; never spend them on setup.
- Complete the promised lesson before the outro, then open one genuine adjacent
  technical question that creates curiosity for more. Do not use tacky or
  manipulative engagement bait, an unresolved version of the original promise,
  or a generic follow CTA as the curiosity mechanism.
- For every Short that shows code, place the camera-facing source in a
  `scenes/` directory beside that Short's runnable experiment. Name the files
  sequentially as `scene_1.cpp`, `scene_2.cpp`, and so on in recording order.
  Keep benchmark harnesses, setup code, and other non-camera implementation
  outside `scenes/`. Every script beat that shows code must reference the exact
  scene file so the recording sequence is unambiguous. Treat each scene file as
  the exact editor viewport: omit includes, function definitions, wrappers, and
  surrounding setup when they do not teach the Short's idea. A scene may be an
  intentionally non-standalone function-body snippet; keep its compiled,
  correctness-checked equivalent in the separate runnable experiment.
- Code prepared for vertical Shorts should prefer narrow, readable spellings.
  Use targeted `using` declarations to remove repetitive `std::` qualification
  when doing so improves horizontal fit without creating ambiguity. Do not use
  a blanket `using namespace std;`.
- Optimize camera-facing Short code for the actual editor viewport. Prefer a
  complete idea that fits within 14 visible lines, and treat 17 visible lines
  as the hard ceiling for any single shot. The complete program may be longer,
  but every block shown at once must remain readable without scrolling.
- Remove syntax that is unrelated to the lesson from camera-facing Short code.
  Avoid namespaces, templates, `constexpr`, `const`, `noexcept`, `inline`, long
  types, and production abstractions when they consume screen space without
  advancing the concept being taught. Keep them only when correctness requires
  them or when they are the subject of the Short.
- When the lesson does not depend on numeric precision, use the shortest clear
  safe numeric type in camera-facing code. Prefer `int` over `double` when the
  demonstrated values and bounds cannot overflow and floating-point behavior
  is unrelated to the concept.
- Keep a camera-facing function signature on one line whenever it fits the
  vertical editor safely. Save width with compact parameter names such as
  `arr` and `n`, but preserve meaningful loop coordinates such as `row` and
  `col` when those names make the traversal immediately legible.
- Every X package must include one concise series-navigation reply containing
  the complete YouTube playlist and GitHub repository. Use it beneath every
  episode announcement. The main post links the specific episode; do not create
  an expanding chain of episode-to-episode replies.

### Current long-form experiments from the initial analytics

These are active hypotheses for the next three long-form episodes, not
permanent universal laws. Reassess them after the comparison sample exists.

- A displayed destination or roadmap is a promise, not a payoff. The opening
  sentence should teach one complete fact or resolve one visible step while it
  introduces the episode.
- Surface the concrete failure or limitation immediately, begin meaningful
  work within the first minute when the subject permits it, and create recurring
  observable results rather than postponing the opening promise until the end.
- Lead titles, thumbnails, and announcements with the capability,
  transformation, paradox, or failure the audience can understand before
  watching. Operation names and implementation inventories support that value;
  they do not replace it.
- Preserve rigorous mathematics and systems reasoning, but move administrative
  framing, repeated summaries, exhaustive edge cases, and previously learned
  machinery behind the first working result.
- Treat personal X posts as a relationship and conversation layer distinct
  from announcements. Keep them self-contained and do not judge them by native
  video's reach objective.
- Do not infer the ideal runtime, posting hour, thumbnail style, topic family,
  or winning platform from the current small sample. Publish controlled
  experiments and compare reach, consumption, engagement, conversion, and
  audience growth separately.

### Current Shorts experiments

Keep Shorts evidence and experiments separate from long-form retention. For
the next three native Shorts, test approximately 20-25 seconds, one idea,
progressive visual disclosure, and the first explanatory result inside three
to five seconds. End with an open technical door, never a conventional social
CTA. Never cite Episode 1's long-form retention curve as evidence for these
choices.

## Video visual assets

- Before planning, generating, reviewing, or revising a YouTube long-form
  thumbnail, read and follow
  `youtube-series/production/youtube-thumbnail-research.md` alongside
  `youtube-series/production/visual-asset-guidelines.md`. Treat the research
  document's evidence hierarchy, face-use cautions, feed-size gate, packaging
  rules, and measurement protocol as mandatory. Update the dated research when
  credible new evidence or controlled channel results materially change a
  decision. Do not replace it with generic creator folklore.
- Follow `youtube-series/production/visual-asset-guidelines.md` for generated
  diagrams and OBS overlays.
- Episode 6 is the final `2560 x 1440` long-form master. Every video master
  produced after it is 4K. Use `3840 x 2160` for long-form and `2160 x 3840`
  for Shorts, Reels, TikTok, and other vertical exports. This standard is a
  release gate, including when a destination platform later transcodes or
  downscales the submitted master. It is not retroactive to Episodes 1-6 or
  Shorts 1-3.
- Treat the video master and the platform cover files as different assets. One
  `2160 x 3840` master may be reused across Shorts, Reels, and TikTok, but its
  thumbnail must not be reused blindly across platforms. Generate YouTube
  long-form thumbnails at `16:9`, YouTube Shorts thumbnails at `9:16`, and
  Instagram Reel covers at Instagram's recommended `420:654` (`1:1.55`) ratio,
  using a high-resolution equivalent such as `1080 x 1682` rather than a small
  literal `420 x 654` raster. The cover ratio is not a guarantee of the visible
  crop. Instagram presents Reel covers differently across the Reels surface,
  feed, profile grid, devices, and account rollouts. Use the centered
  `1080 x 1080` square inside the `1080 x 1682` cover as the conservative house
  safe area unless the real composer proves that a larger area survives. This
  leaves approximately 301 pixels of nonessential background above and below.
  Keep every headline, complete diagram, result, and brand mark inside that
  square. Always inspect the composer's `Profile grid` crop before publishing
  and treat it as the final authority. A local crop simulation is useful for
  preparation but does not pass the release gate. Never tell the learner an
  Instagram cover is ready until the actual upload composer's profile-grid
  preview has been inspected. If that preview is unavailable, report the cover
  as unverified rather than approving publication. For TikTok and X, verify the selected cover or poster frame in the
  real composer. Recompose for each ratio and inspect the destination crop
  before publishing. Instagram Reel covers currently use the technical visual
  without the learner's face unless the learner explicitly changes that
  direction.
- Equivalent repeated objects must be literal duplicates with identical
  dimensions and styling, not separately generated approximations.
- Lower-screen OBS overlays default to opaque, edge-to-edge rectangles with
  sharp corners. Do not rely on transparency or underlying scene content unless
  the learner explicitly chooses that composition.
- For the 4K `2160 x 3840` vertical OBS layout used after Episode 6, the webcam
  occupies the top `2160 x 1488` region and the visual aid occupies the complete
  remaining `2160 x 2352` region. Lower-screen visual assets must therefore be
  exactly `2160 x 2352` unless the learner explicitly revises the layout.
- Compose visual content specifically for the full `2160 x 2352` region. Do not
  satisfy the dimension requirement by padding a shorter design with large
  empty bands; use the available height through deliberate spacing and scale.
- Visual differences must communicate real conceptual differences. Preserve a
  consistent grammar for tensor elements, vector brackets, empty states,
  typography, and alignment.
- In computational diagrams, every input value must have its own clearly
  attached outbound edge. When several values feed several results, show the
  topology explicitly: separate input edges merge at a visible junction, the
  shared path continues, and a second junction splits into distinct result
  edges. Do not let one value appear disconnected or imply that a result comes
  from only one operand.
- Semantic accent colors apply to the complete result object, not only its
  numeral. A result frame, label, value, glow, and reflection must use one
  cohesive assigned color. Do not place an orange or green result inside an
  unrelated blue frame unless that mixed-color encoding has an explicit
  conceptual meaning.
- Comparison-column headings must use uniform typography and a shared baseline.
  Size the entire heading set according to its longest label rather than
  independently fitting each label to its column.
- Use deterministic vector composition when visual elements must be exactly
  identical. Image-generation output is appropriate for exploratory design,
  but it must not be treated as proof of pixel-identical typography or repeated
  geometry.
- Keep the editable SVG as the source of truth for exact educational diagrams
  and render the final opaque PNG from it. Repeated cells and brackets should
  use shared SVG definitions rather than copied coordinates.
- Use explicit column geometry. Every column has a known horizontal center,
  peer objects are centered by their complete bounding boxes, and separators
  receive visible inner gutters on both sides.
- Treat related metadata such as `rank` and `elements` as one visual block. Use
  tighter spacing inside the block, then center the block vertically between
  the conceptual row above and the object visualization below.
- Use one contemporary, legible type system throughout an asset. Peer headings
  share exact typography and baselines; metadata labels and values share exact
  row baselines. Avoid unintended italics, ambiguous glyphs, and independent
  per-column font fitting.
- Verify the rendered PNG, not only the SVG source. Renderer-specific behavior
  can alter fonts, strokes, spacing, and alpha; use filled geometry for critical
  separators and confirm the final dimensions and opacity.

## Native Short scripting

- Open with the central contradiction, surprising result, or concrete failure
  in the first spoken sentence. Do not greet the audience, introduce the
  series, or provide background before the hook.
- Build one uninterrupted causal chain from hook to payoff. Remove repeated
  definitions, duplicate summaries, ornamental transitions, and any sentence
  that does not advance the explanation.
- Keep a Short about one idea. Reveal visuals only when their logic enters the
  narration; do not display the complete answer before the hook has created the
  question.
- Every Short should create some follower conversion without explicitly asking
  anyone to follow, visit the profile, or engage. Never use conventional social
  CTAs or retention language, including `Follow for more`, `Follow for part
  two`, `Like and follow`, `Check out my profile`, `If you want to learn more`,
  `Stay tuned`, `Part two coming soon`, `You won't believe what happens next`,
  or `This is just the tip of the iceberg`.
- The viewer should follow because the finished Short makes them infer that the
  person behind it probably has more ideas they would enjoy learning. Earn that
  inference through technical substance, not an instruction.
- Use this default ending structure: hook -> build or explanation -> complete
  payoff -> open technical door -> immediate cut. Completely deliver the
  original promise. Never withhold its answer, manufacture a cliffhanger, or
  make the lesson incomplete to force another view.
- The open technical door should use the final one or two sentences to expose a
  natural adjacent technical question. It should reveal a deeper mechanism,
  raise the obvious next question, show a surprising consequence elsewhere,
  suggest a concrete next experiment, or occasionally connect naturally to a
  larger technical project. Prefer specific technical curiosity over vague
  mystery.
- Do not merely zoom out to a broad concept that closes the subject. `This is
  why object lifetime and storage matter` is weak. `Now the interesting question
  is which operations can change that storage without invalidating your pointer`
  creates forward motion.
- The ending must sound like the next thought of a technically curious engineer,
  not a creator managing an audience. Keep it understated, confident, and
  intellectually curious. Do not overhype, manufacture suspense, praise the
  viewer, or mention engagement, followers, algorithms, accounts, profiles,
  social media, or future content. Usually one sentence is enough. Cut
  immediately after it.
- Maintain one canonical spoken script. Shot instructions may refer to its
  timestamped sections but must not duplicate the narration in a second,
  potentially divergent version.
