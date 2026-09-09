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

Start every session by reading `docs/distribution-timeline.md` for the
current release/production state before recommending any release,
announcement, or distribution action.

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

- YouTube publication or scheduling status, final title, description, tags,
  thumbnail, playlist membership, and the intended publication time. Every
  long-form episode must belong to the main series playlist, and every Short
  must belong to the dedicated Shorts playlist. Add missing membership through
  the channel tooling during the check rather than returning it as a learner
  task;
- whether the required first comment was posted and whether its retrieval
  answers reproduce the episode's exact closing questions;
- the end screen on every long-form episode. It must contain both a Subscribe
  element and a playlist element linking to the complete series playlist. Use
  authenticated YouTube Studio browser automation to inspect and add missing
  elements when available. The Data API cannot read or edit end screens, so if
  Studio access is unavailable, report this as a specific manual blocker rather
  than silently treating it as complete;
- other Studio-only items, including related-video assignment, cards, reviewed
  captions, and audience settings when they were part of the release package;
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
- whether scheduled 24-hour, 72-hour, and other decision-relevant analytics
  checkpoints were captured, and whether audience counts and data freshness
  are current;
- whether recording, editing, thumbnail, upload, release-gate, and next-episode
  dependencies needed for the standing cadence are complete or at risk; and
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
- The initial X comparison established the first concrete example. The Episode
  1 and Episode 2 announcements received essentially identical reach (798 and
  800 impressions), but Episode 1 generated 102 engagements, 20 link clicks,
  and 15 profile clicks versus Episode 2's 19, four, and four. The current
  interpretation is that Episode 1 framed an ambitious journey and concrete
  starting point, while Episode 2 primarily listed features. Therefore Episode
  3 should lead with the capability it unlocks, such as completing a machine
  learning prediction, and only then name the tensor operations involved.
- Treat the opening twenty seconds as part of the lesson's payoff, not as
  administrative space. Episode 1's first processed retention curve measured
  51.58% audience watch ratio near 0:22 and only 18.95% near 0:45; its relative
  retention also declined sharply against videos of similar length. A displayed
  destination is only a promise, not a payoff. Future long-form openings must
  resolve or demonstrate one concrete new fact, preferably through an
  observable result or failure, while keeping the series identity to one
  clause. Compress retrieval to the prerequisites needed now and expose the
  first new problem inside the opening minute.
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
  keep the CTA to at most two seconds. Recheck at 24 and 72 hours before
  declaring a conclusion.
- The second Short provides the first strong follow-up experiment. On Instagram,
  the 27-second unsigned-loop failure reached 9,757 accounts, averaged 15.87
  seconds, and generated 111 interactions, versus 1,026 reach, 7.68 seconds,
  and nine interactions for the 34-second tensor-shape Short. YouTube's
  processed comparison also favors the second Short on average percentage
  viewed (66.76% versus 59.61%) and subscriber conversion (one versus zero).
  Treat this as evidence to repeat a concrete failure, immediately visible
  code, one causal mechanism, and a 20-30 second runtime for the next two
  experiments, not as proof that unsigned loops or any single topic always win.
- Episode 3's processed retention extends the long-form opening diagnosis:
  audience watch ratio fell from 53.1% near the first 1% of the video to 18.8%
  near 2%, 9.4% near 3%, and 3.1% near 4%. Future episodes must expose the real
  contradiction or completed calculation within the first twenty seconds and
  begin meaningful code around thirty seconds when the subject permits it.
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
  the intended comment through the API when authorized, then record pinning,
  related-video assignment, end screens, cards, and other unsupported actions as
  manual or separately verified browser steps.
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

- Never use an em dash in any audience-facing copy. This prohibition applies
  to scripts, narration, titles, descriptions, comments, social posts,
  captions, visual text, and publishing packages. Rewrite the sentence with a
  period, comma, colon, semicolon, or parentheses instead. Treat this as an
  absolute series voice rule, not a stylistic preference.
- Never use `#shorts` in a description, caption, social post, or metadata tag.
  The format is already known to the platform, and the generic label adds no
  useful subject information. Use a small set of topic-specific hashtags and
  metadata tags that identify the language, technical concept, and intended
  audience instead.

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
- Keep early chapter compilation commands minimal, using only the selected C++
  language standard unless a flag is itself being taught. Introduce warning
  groups such as `-Wall`, `-Wextra`, and `-Wpedantic` later as part of an
  explicit transition into production-grade diagnostics and tooling.
- Use this mandatory chapter skeleton:
  1. an opening that begins with "Welcome back to Deep Learning, All the Way
     Down, where we..." and concisely frames the series;
  2. a self-contained statement of the current problem and why it matters;
  3. a direct statement of what the current episode will accomplish;
  4. the chapter's cohesive concept-to-code-to-verification sequence; and
  5. a closing review, a concise next-chapter hook, and retrieval questions as
     the final spoken content.
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
- Respect the live-build format. Do not open by showing finished code, final
  output, or a successful end state that does not exist yet. The learner builds
  the implementation while recording. Begin from the code or understanding
  already available, surface the real limitation or failure, and let the viewer
  experience the result when it is actually produced.
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
  thumbnail and cover references, tags,
  an X announcement, a LinkedIn announcement, a Reddit decision and draft when
  appropriate, a separately produced Shorts plan, and a release check for the
  five-second end-screen tail plus the Subscribe and complete-series-playlist
  elements.
- Every `publishing.md` package, including packages for native Shorts and other
  video formats, must contain a platform-ready pinned comment. Keep it concise
  outside the required retrieval answer key, make its links explicit, and
  direct viewers to the most relevant full lesson, series playlist, source code,
  or next action without repeating the entire description.
- The X and LinkedIn sections must include platform-ready copy, recommended
  publication timing relative to the YouTube release, and a concise rollout
  strategy. Adapt timing to the actual release day, audience evidence, and
  prior distribution rather than mechanically reusing one schedule.
- Reddit is a community-participation channel, not an announcement feed. Check
  each community's current rules and recurring threads, tailor the post to that
  audience, and explicitly choose not to post when another submission would be
  repetitive or extractive.
- Shorts are native, self-contained vertical lessons recorded separately from
  the long-form chapter. Each plan must name the single idea taught, its hook,
  its relation to the episode, its intended publication window, and the related
  long-form YouTube video when that feature is available.
- Every X package must include one concise series-navigation reply containing
  the complete YouTube playlist and GitHub repository. Use it beneath every
  episode announcement. The main post links the specific episode; do not create
  an expanding chain of episode-to-episode replies.

### Current content experiments from the initial analytics

These are active hypotheses for the next three long-form episodes and next
three Shorts, not permanent universal laws. Reassess them after the comparison
sample exists.

- A displayed destination or roadmap is a promise, not a payoff. The opening
  sentence should teach one complete fact or resolve one visible step while it
  introduces the episode.
- Surface the concrete failure or limitation motivating the lesson inside the
  first minute, begin meaningful code around minute two, and create recurring
  observable results rather than postponing the opening promise until the end.
- Lead titles, thumbnails, and announcements with the capability,
  transformation, paradox, or failure the audience can understand before
  watching. Operation names and implementation inventories support that value;
  they do not replace it.
- Preserve rigorous mathematics and systems reasoning, but move administrative
  framing, repeated summaries, exhaustive edge cases, and previously learned
  machinery behind the first working result.
- For the next three native Shorts, test approximately 20-25 seconds, one idea,
  progressive visual disclosure, and the first explanatory result inside three
  to five seconds. Omit the CTA or keep it under two seconds.
- Treat personal X posts as a relationship and conversation layer distinct
  from announcements. Keep them self-contained and do not judge them by native
  video's reach objective.
- Do not infer the ideal runtime, posting hour, thumbnail style, topic family,
  or winning platform from the current small sample. Publish controlled
  experiments and compare reach, consumption, engagement, conversion, and
  audience growth separately.

## Video visual assets

- For Blender and animation work, read
  `youtube-series/production/animations-playbook.md` for the selected clay style,
  reusable elements, placement rules and numbered scene export workflow.
- Follow `youtube-series/production/visual-asset-guidelines.md` for generated
  diagrams and OBS overlays.
- Treat the video master and the platform cover files as different assets. One
  `1080 x 1920` master may be reused across Shorts, Reels, and TikTok, but its
  thumbnail must not be reused blindly across platforms. Generate YouTube
  long-form thumbnails at `16:9`, YouTube Shorts thumbnails at `9:16`, and
  Instagram Reel covers at Instagram's recommended `420:654` (`1:1.55`) ratio,
  using a high-resolution equivalent such as `1080 x 1682` rather than a small
  literal `420 x 654` raster. Keep every essential element inside Instagram's
  centered `3:4` profile-grid safe area, which is `1080 x 1440` inside the
  current cover and can remove approximately 121 pixels from both the top and
  bottom. For TikTok and X, verify the selected cover or poster frame in the
  real composer. Recompose for each ratio and inspect the destination crop
  before publishing. Instagram Reel covers currently use the technical visual
  without the learner's face unless the learner explicitly changes that
  direction.
- Equivalent repeated objects must be literal duplicates with identical
  dimensions and styling, not separately generated approximations.
- Lower-screen OBS overlays default to opaque, edge-to-edge rectangles with
  sharp corners. Do not rely on transparency or underlying scene content unless
  the learner explicitly chooses that composition.
- For the current `1080 x 1920` vertical OBS layout, the webcam occupies the
  top `1080 x 744` region and the visual aid occupies the complete remaining
  `1080 x 1176` region. Lower-screen visual assets must therefore be exactly
  `1080 x 1176` unless the learner explicitly revises the layout.
- Compose visual content specifically for the full `1080 x 1176` region. Do not
  satisfy the dimension requirement by padding a shorter design with large
  empty bands; use the available height through deliberate spacing and scale.
- Visual differences must communicate real conceptual differences. Preserve a
  consistent grammar for tensor elements, vector brackets, empty states,
  typography, and alignment.
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
- A CTA is appropriate only after the lesson has fully resolved its opening.
  Use at most one concise sentence that accurately describes the continuing
  value, such as following for more C++ and deep-learning systems from first
  principles. Do not interrupt the explanation or stack multiple asks.
- Maintain one canonical spoken script. Shot instructions may refer to its
  timestamped sections but must not duplicate the narration in a second,
  potentially divergent version.
