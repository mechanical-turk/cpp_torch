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
- Never implement or execute deletion, channel banning, destructive comment
  moderation, or other irreversible YouTube actions under this standing
  authorization. Those require a separate explicit learner request.
- The YouTube API cannot pin comments or manage every Studio-only feature. Post
  the intended comment through the API when authorized, then record pinning,
  related-video assignment, end screens, cards, and other unsupported actions as
  manual or separately verified browser steps.

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

## Video-series scripting

When planning or writing a chapter for *Deep Learning, All the Way Down*:

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
  not between them. End on the questions so viewers leave with an active task.
- Keep closing retrieval to at most five questions and prefer approximately
  three. Select the questions that retrieve the chapter's central dependency
  chain rather than attempting exhaustive coverage.
- Optimize the long-form chapter only for a natural, coherent 16:9 lesson. Do
  not constrain its composition, narration, or structure to make excerpts work
  as vertical Shorts.
- Plan, script, and record Shorts separately as native standalone lessons. A
  Short may teach an idea also covered by the long-form episode, but it must not
  be treated as an extraction target inside the chapter script.
- Every episode must have a `publishing.md` package before release. It must
  include the final title, YouTube description, pinned comment, chapter markers
  or an explicit note that they remain provisional, thumbnail reference, tags,
  an X announcement, a LinkedIn announcement, a Reddit decision and draft when
  appropriate, and a separately produced Shorts plan.
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

- Follow `youtube-series/production/visual-asset-guidelines.md` for generated
  diagrams and OBS overlays.
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
