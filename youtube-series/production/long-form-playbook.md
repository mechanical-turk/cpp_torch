# Long-Form Playbook and Checklist

Read this before planning, writing, reviewing, or publishing a long-form episode
of Deep Learning, All the Way Down. This is the authoritative long-form script
checklist. Keep its pacing and evidence separate from the Shorts playbook.

## Required script-writing workflow

Every new or rewritten long-form script must go through the following steps
in order, without requiring a separate critique request. Keep their artifacts
separate so the recording document stays easy to follow:

- `script.md`: descriptive MP4 filename, episode title, concise recording
  directions, `>` narration, exact code edits and expected on-screen output.
- `keyword-research.md`: dated SEO research and spoken-keyword map.
- `script-review.md`: checklist plan, source/scope notes, checklist audit,
  critique, score, verification references and editorial rationale. Link the
  script and keyword research here. Do not put this material in `script.md`.

1. **Keyword and SEO analysis, before drafting:** complete the research and
   spoken-keyword map below before writing narration or live-coding beats.
   Save the episode-specific record as `keyword-research.md` and link it from
   `script-review.md`. Publishing-time research does not replace this step.
2. **Checklist plan:** in `script-review.md`, explain how this draft will attempt every item L01-L16.
   Use one concise row per ID with the actual intended beat, visual, code,
   evidence, or known risk. Identify the opening promise, first useful action,
   first payoff, and the capability gained in each section. Intention is not
   proof of compliance.
3. **Script:** one canonical draft, with `>` marking only spoken narration.
   Keep code, estimated timecodes and scene directions outside narration.
   Use the episode structure below; keep review notes in `script-review.md`.
4. **Checklist audit:** in `script-review.md`, assess that exact draft against every L01-L16 item.
   Give status, a specific beat or evidence reference, awarded points, and a
   repair for each shortfall. Do not copy the plan and call it an audit.
5. **Critique:** in `script-review.md`, prioritize the biggest obstacles to viewer understanding,
   useful progress, and trust. Explain their consequences and the next repair.
   Do not invent faults or add cosmetic revisions to inflate an iteration count.
6. **Final score:** in `script-review.md`, calculate the score out of 100 and give the decision
   `advance`, `rework`, or `hold` using the rubric below.

For a requested fragment, preserve scope and recorded material. Audit the
fragment and mark unavailable whole-episode checks UNVERIFIED; label any total
a provisional partial-draft score. Do not rewrite a recorded opening or invent
the rest of an episode merely to pass checks. After revisions, rerun affected
checks and recalculate the score for the actual delivered draft.

## Source of truth

- The implementation lives at
  `/Users/keremkazan/Documents/Projects/deep-learning-all-the-way-down`, exposed
  here as `aliases/02-screen-long-form`.
- Read the current code and git history before writing live-coding beats.
- A script records intent. Final media, captions, and checked-in code establish
  what viewers actually received.
- Respect the live-build format. Do not invent finished code or final output for
  an opening when it did not exist during recording.
- Build the episode's core machine-learning implementation on camera. Routine
  dataset file parsing may be supplied in a separate, inspectable file when it
  is not the lesson. Explain its inputs, outputs and normalization in no more
  than 30 seconds, then show how its data enters the Tensor and training loop.
  Chapter 12 uses this approach for mnist_reader.hpp. Do not build a general
  Dataset/DataLoader abstraction until that abstraction is itself the topic.
  Do not hide model, loss, gradient, training or evaluation code in the helper.
  Keep support code narrow and explicitly identify it as supplied. Separate
  production regression checks may remain outside the recording, but must not
  supply hidden implementation. Never use "done off screen" to bridge missing
  lesson code.
- Keep uncommitted content ideas in `youtube-series/content-ideas.md`, separate
  from active scripts and release packages.
- Give new examples meaningful names such as `predictions` and `targets`.
  Do not carry numbered test variables such as `pred_23` into new lessons.
  Initialize a fresh example explicitly when historical test setup is irrelevant.

## Pre-script keyword and SEO analysis

Before writing any new episode script:

1. Read the preceding episode's actual ending and current code. Establish what
   this episode will deliver, and which attractive search phrases would overpromise.
2. Research YouTube search language for that specific subject. Prefer owned
   search/traffic data when available, then current search suggestions and
   comparable videos. Use official documentation or original educational sources
   to check terminology. Do not invent query volume, competition, rankings or
   keyword effectiveness from a few search results.
3. Save a dated `keyword-research.md` with sources, observed wording, candidate
   phrases, one primary phrase, a short supporting set, rejected terms and
   unavailable evidence. Existing relevant data may be used without triggering
   an unrequested analytics refresh.
4. Map the selected words to actual spoken moments: the opening promise, the
   code or calculation that introduces each concept, and the recap. Record the
   intended natural sentence or use, not just a list for the description.
   Name the concrete subject early when it helps the viewer, and pronounce
   abbreviations in useful ordinary terms, for example mean squared error
   before using MSE.
5. Write the script around the problem and code progression. Use the chosen
   terminology where the viewer needs it. Do not add a keyword roll call, repeat
   phrases for density, slow the cold open, or force unrelated topics into speech.
6. Before approving the script, audit the actual `>` narration against the map.
   Keywords present only in headings, code, production notes or future upload
   metadata do not count as recorded speech. Remove unsupported promises and
   repair unnatural phrasing. A written audit is not proof of the final transcript;
   recheck the captions after recording.

This is a recording requirement, not only a publishing requirement. Spoken
terminology should make the lesson clear and searchable; no claim is made that
repeating a term causes higher ranking. Follow the separate platform-copy
playbook when researching and writing the later public package.

## Long-form script checklist

Weights express editorial priorities, not measured contributions to retention.

### Promise and opening

- [ ] **L01 | Specific, achievable promise | 10 points.**
  Does the opening state a concrete problem and a capability we will deliver,
  rather than merely name the topic? Identify the current limitation, desired
  result, and scope boundary. Check the preceding episode's recorded promise
  against its captions and code; explain any necessary scope change. The
  title's promise must match the lesson, not a more ambitious future episode.

  **Curiosity gap:** establish one concrete question, surprising behavior, or
  unresolved engineering problem that gives viewers a reason to keep watching.
  Make clear what they already understand and what they will discover by
  following the implementation. Answer the question through visible progress
  and a real payoff. Do not hide prerequisite context, delay useful work, or
  manufacture suspense around a trivial answer. Long-form lessons should
  deliver intermediate answers rather than withhold everything until the end.

  **Unique service proposition:** identify the specific value this episode
  provides beyond naming its topic. What will viewers build, understand, or
  learn to diagnose here, and why is our implementation worth following?
  Express that value through the concrete promise and opening code or visual,
  not a sales pitch or an unsupported claim that nobody else teaches it.
  "From scratch" alone is insufficient; name the useful capability or insight
  the viewer gains by seeing the machinery built and explained.

  In the pre-script checklist plan, write down the curiosity question, its
  payoff, and the episode's distinctive viewer benefit. Audit the actual
  opening for all three, not just the planning notes. Combine them naturally
  with the quick reassurance in L02; do not stack three introductory speeches.

- [ ] **L02 | Clear cold opening | 10 points.**
  **Thumbnail-title-opening alignment:** the thumbnail, video title, and first
  five seconds must communicate the same subject and promise. Immediately
  name the title's core subject and say what we are doing in one short, natural
  sentence, so viewers know they clicked the right video. This is quick
  reassurance, not a separate introduction: do not recite the series name,
  episode number, full SEO title, or a roadmap. Begin the relevant code or
  visual action alongside that sentence, then continue directly into the work.
  Display the video's topic title in writing within the first five seconds,
  ideally from the first frame, so muted autoplay and hover-preview viewers
  can immediately tell what we are doing. Use the same topic wording as the
  published title; the series suffix and episode number need not occupy the
  overlay. Keep the text readable at preview size and visible long enough to
  read. Overlay it on the relevant code or visual without obscuring the work;
  do not insert a separate title card or delay the first useful action.
  During review, compare the thumbnail, title, first frame, and first five
  seconds of narration together. A viewer should recognize the promised
  content without waiting for context later in the intro. If packaging is not
  final yet, keep this alignment check pending and repeat it before recording
  approval and release; do not claim it passed from the script alone.

  Do the first sentence and first frame point to the same understandable need?
  Put meaningful subject and stakes before setup. Begin with relevant existing
  code, a real failure, a calculation, or a concise narrated visual. No greeting,
  series premise, roadmap, recap, previous answers, or setup commands. Supply
  only the prerequisite a new viewer needs for this action. A visual is optional
  and must explain faster than code; no silent slideshow or repeated titles.
  Ease the viewer into the subject: name the concrete object or situation
  before referring to its limitation. A cold open must establish context and
  sell the core idea together. Do not begin with "this model", "this result",
  or an unexplained failure when the viewer has not yet been shown what it is.
  Use a brief, understandable observation or example to establish the subject,
  connect it to the interesting problem, then introduce the change we will
  build. This is necessary orientation, not a series recap or a long preface.
  Review the first spoken lines as someone who has just opened this video:
  can they identify what we are discussing, why it matters, and what they will
  learn without having watched another episode?

- [ ] **L03 | Useful action immediately | 8 points.**
  Does the beat after the promise start changing, running, or deriving something
  useful instead of re-explaining what we will do? Name the action and its
  estimated time. Audit 15 and 30 seconds explicitly. Thirty seconds is an
  outer review target, not permission to spend the opening talking. Cursor
  movement, imports, and ceremonial typing do not count as meaningful progress.

- [ ] **L04 | First payoff within one minute | 8 points.**
  **Time to value:** measure elapsed time from the first frame to the first
  useful thing the viewer actually receives: an insight, an explanation that
  resolves something, a meaningful code improvement, or a demonstrated result.
  A promise of future value, topic announcement, cursor movement, or unexplained
  code typing does not count. Useful action (L03) and delivered value are
  separate checks; beginning to code is not automatically the first payoff.

  Balance **context, curiosity, and time to value**. Supply only enough context
  to understand the immediate problem, establish a concrete question worth
  following, and deliver a useful piece of the answer quickly. Give additional
  context when the next step needs it instead of front-loading prerequisites.
  Keep a worthwhile larger question open while resolving smaller questions
  along the way. Do not preserve curiosity by withholding an early answer the
  viewer needs, or chase speed by leaving viewers unable to follow the code.

  In the opening plan, identify the minimum necessary context, curiosity
  question, first value delivered, and estimated timestamp. Ask of every
  introductory sentence: does the viewer need this before that first value?
  Move unnecessary setup later or remove it. During rehearsal and final-edit
  review, record the actual time to value and what made that moment useful.
  Treat one minute as an outer review target, not an allowance to fill with
  setup; aim to deliver value as soon as the subject permits.

  Name the observable first payoff and how we reach it by about 1:00. It may be
  a useful code path, worked result, or demonstrated behavior, not necessarily
  the completed feature. Do not fabricate finished output before a live build,
  add throwaway arithmetic, or relabel setup as a payoff. Script times are
  estimates until rehearsed or measured in final media.

### Progression and comprehension

- [ ] **L05 | Sections produce capabilities | 8 points.**
  For every section, state what the program or viewer can now do. Follow
  `specific obstacle -> smallest useful change -> visible consequence -> next need`.
  Avoid an inventory of constructors, helpers, and containers with no nearby
  use. Deliver intermediate payoffs throughout; do not save all value for the
  final run. A long-form episode needs more than one delayed reveal.

- [ ] **L06 | Concepts arrive when needed | 8 points.**
  Is each abstraction, helper, mathematical rule, and design choice used in the
  next few moments? Show the call site or concrete need before explaining its
  machinery. Explain as the important code appears. No separate theory primer
  unless theory is the episode's subject; no declaration-then-definition detour
  when an inline implementation is the natural next step.
  Before each substantive code edit, include a brief spoken explanation of
  what we are about to build and why we need it here. Then narrate the decisions
  while typing. An unspoken location note or a paragraph after the code does
  not satisfy this requirement; use the sequence under Spoken delivery check.
  Write the final validation logic when it is already known. Do not introduce
  a temporary whitelist merely to match unfinished code and replace it later.
  Label incomplete recording stages instead of adding disposable scaffolding.
  Put validation at its teaching need, not merely its final source position.
  First demonstrate the supported behavior; introduce an unsupported-path
  check when the viewer can see what is supported and what the failure would
  disrupt. Code that belongs early in a function need not be taught first.
  Implement each operation's forward and backward paths together before its
  first run. Do not stage a predictable failure from a deliberately missing
  implementation just to motivate writing the code we already planned.

- [ ] **L07 | Essential reasoning survives the edit | 8 points.**
  Can viewers explain why the important lines work, rather than only copy them?
  Preserve the reasoning behind ordering, accumulation, ownership, shapes, and
  other consequential choices. Use one stable example and consistent names
  when possible. Remove duplicate preface/walkthrough/summary explanations,
  not the causal link that makes a difficult step understandable.

- [ ] **L08 | Correct, traceable code progression | 10 points.**
  Does the draft start from the actual code checkpoint and build one step at a
  time without unexplained state changes? Check the runnable milestones and
  claimed outputs. Explicitly label fragments that cannot compile yet. Preserve
  existing behavior, and clearly reject or disclose unsupported paths rather
  than silently produce incomplete results. Keep decisive conditions visible;
  do not omit the central mechanism to provoke comments. Missing proof is
  UNVERIFIED, not a promise to verify later marked PASS.
  Every requested code edit must show the exact **Before** code and exact
  **After** code at that point in the build. Verify that each Before matches
  the preceding state, including earlier edits in this episode.

- [ ] **L09 | Useful on-screen proof, complete off-screen checks | 6 points.**
  Does each live test expose a failure, establish a contract, or make new
  behavior clear? Skip obvious assertions and throwaway arithmetic. Keep full
  regression and correctness checks in the code workflow even when they stay
  off camera. Use minimal on-screen compilation commands; warning diagnostics
  deserve screen time when they are the subject. Numerical/performance claims
  need actual evidence and relevant conditions, not guessed outputs.

### Visuals and delivery

- [ ] **L10 | Narration and visual attention agree | 5 points.**
  Do scene directions identify the exact line, value, or shape being discussed
  and show its change when named? Use selective highlights, arrows, or a diagram
  to reduce searching. Preserve spatial and color meaning. Retire a visual when
  it has served its purpose. Keep code readable in 16:9; avoid competing panels,
  obligatory stickers, and full-screen text that repeats every spoken word.

- [ ] **L11 | Dense information, manageable reading | 5 points.**
  Are explanations short, connected, active, and natural to say? Remove empty
  transitions, repeated definitions, needless syntax tours, and dead setup.
  Leave enough stable screen time to read unfamiliar code. Flag exposition
  stretches approaching two minutes without useful visible progress; repair
  the teaching sequence rather than add decorative motion. Do not impose a
  Shorts speaking rate, line limit, or cut frequency on long form; see L11a
  for the separate standing runtime target. Review the complete spoken track
  for natural cadence, rhythm and sentence structure, not just word count.
  A string of short textbook statements can still sound robotic. Explain the
  visible code as you would to someone sitting beside you; connect reasons and
  consequences naturally. Do not add filler, fake informality or exaggerated
  enthusiasm to simulate a human voice.
  Audit the spoken track without headings, code, or production notes. The
  listener must still understand what prompted each edit and why we moved to
  the next function. Check both section boundaries and sentence-to-sentence
  continuity; grammatical sentences alone do not establish a coherent lesson.

- [ ] **L11a | Target runtime | included in L11's 5 points.**
  Target a final edited runtime of 10 to 15 minutes. Episode 7 at 23:39
  established that this series' episodes run too long relative to that target,
  reading as intimidating and reducing the odds a viewer starts or finishes.
  Estimate runtime from the script draft (spoken word count plus code/visual
  holds) and flag a projected final cut outside 10-15 minutes before recording,
  not after editing. Repair a script that runs over by cutting scope (fewer
  sections, a narrower promise) rather than by speeding up delivery or trimming
  necessary reasoning that L07 requires to survive the edit. A finished edit
  outside the target range is a named risk to record here and revisit in the
  episode's `publishing.md`, not an automatic FAIL of L11 by itself, since
  going over may reflect a scope decision made before this rule existed.

### Completion and handoff

- [ ] **L12 | Complete lesson and meaningful continuation | 4 points.**
  Does the episode demonstrate the promised capability and explain the main
  result before moving on? Use genuine prediction or tradeoff questions when
  they help thinking, then answer what this lesson owes. End with a concrete
  next capability arising from the completed work, without a fabricated release
  promise, compulsory controversy, or withholding today's answer for a sequel.

- [ ] **L13 | Tight, readable ending | 4 points.**
  Does the ending follow the required structure below: itemized recap, concise
  on-screen follow-up list, standard sign-off, and planned clean end-screen
  tail? Keep these useful and brief. Starting with Episode 8, omit the closing
  Q&A, retrieval questions, answer key and automatic answer-comment obligation.

- [ ] **L14 | Recording-ready format and voice | 2 points.**
  Is the descriptive MP4 filename at the top, with one canonical `>`-marked
  narration and separate code/scene directions? Follow the script voice rules
  below. Preserve already recorded sections unless the requested change needs
  them altered, and make any resulting continuity issue explicit.

- [ ] **L15 | Accurate subject and SEO handoff | 2 points.**
  Was the dated keyword and SEO analysis completed before script drafting, with
  sources and an explicit spoken-keyword map? Check the exact narration for
  the selected terms at useful moments, not just headings or descriptions.
  Keep title, promise and implemented scope aligned, and reject keyword stuffing
  or unnatural delivery. Missing pre-script research requires rework regardless
  of the total score. Follow the copy/SEO playbook for later public fields;
  script research does not approve the publishing package.

- [ ] **L16 | Evidence limits and honest review | 2 points.**
  Cite the relevant long-form evidence and name any technique borrowed from
  Shorts as a transfer hypothesis. Separate observation from explanation and
  creator direction. State remaining code, rehearsal, asset, and final-media
  checks. Do not claim rendered legibility or measured pacing from prose alone,
  predict reach from this score, or start unrequested publishing/analytics work.

## Script format and voice

- Put the final descriptive `.mp4` filename near the top.
- Mark spoken narration with `>` and keep one canonical narration.
- Write for speech. Use direct, connected sentences that sound natural aloud.
- Follow the voice rules in `platform-copy-playbook.md`, including the ban on em
  dashes, canned contrasts, corporate copy, and manufactured informality.
- Do not say `last episode` or `last time` unless continuity is indispensable.

### Spoken delivery check

- Use this sequence for each substantive coding section:
  **explain the immediate need and intended change -> write while narrating
  the decisions -> interpret the result when it adds something new**.
  The preview should normally take one or two connected sentences. Give the
  viewer enough to anticipate the code without explaining the whole function
  twice. During typing, explain how we carry out the promised change, using
  the line currently on screen. Do not save the explanation until after a
  large code block or read a completed function as an abstract summary.
- Keep the reasoning in the `>` narration. Headings, location labels and
  director notes can orient the presenter but cannot supply a missing spoken
  transition. A routine include or simple rename may share the preview of the
  substantive change it belongs to; it does not need a separate speech.
- Check each transition by asking: what did the viewer just learn, what does
  that make us want to do, and does the next spoken sentence express that
  connection? Resolve missing reasoning before polishing wording. Do not
  paste "so", "now", or "that's why" onto an unrelated new topic.
- When switching subjects, carry the viewer from the visible result to a
  concrete reason for considering the next subject, then name the next action.
  A property comparison alone is not a transition: explain why the difference
  matters here before introducing another function or concept. For alternatives,
  explain the different need without pretending the previous solution failed.
  Read the last spoken passage and the next section's opening together; revise
  them until the change of subject makes sense without the section heading.
- Verbal sections must sound natural and human throughout: vocabulary, cadence,
  rhythm, transitions and sentence structure. Technical accuracy does not excuse
  narration that reads like API documentation or an abstract summary.
- Review narration separately from production notes. Ask whether the presenter
  could say it naturally while pointing to the current line. Replace abstract
  subject pairs and repeated sentence templates with a connected explanation.
- Use contractions where natural; retain precise technical terms when needed.
  Neither choppy fragments nor forced casual language satisfies this check.
- Preserve the causal explanation. Do not shorten a sentence until the viewer
  can no longer understand why the code exists.
- Explain decisions and consequences, not a spoken transcription of operands,
  coefficients or index expressions. Leave readable arithmetic on screen unless
  working through it answers the viewer's immediate question.
- Tie each section to the need left by the previous one. Explain what we can
  do now, what is still missing, and why the next edit addresses it. Use "so",
  "but", "because" and "and that's why" where they express the actual connection;
  adding connectors to unrelated bullet sentences does not fix the progression.
- Narrate the actual editing decision, not just the architecture. If a field
  moved, say why we're returning to its constructor; if a helper gained an
  argument, lead into fixing its callers. Put this guidance before or during
  the edit, not only in headings or an explanation after a large code block.
  Review the last spoken line of one segment together with the first of the
  next: the listener must not have to infer an unstated design decision.
- Keep those bridges short. Do not give every segment the same "now we have X,
  but need Y" template, or add a mini-recap before every edit.
  Once the reason is clear, state the next action plainly. Use "Let's initialize
  the gradients to zero", not an appended explanation such as "ready for
  backward to add its contributions". Do not confuse natural transitions with
  re-explaining the purpose of every line.
- Before an on-screen test run, establish what we expect, why this change puts
  it in question, and what the result will let us do next. After a large
  refactor, distinguish preserved behavior from intentional behavior changes.
  "Let's check it" alone does not explain the test's place in the lesson.
- Put action cues immediately before the action. After "let's run it", run it;
  finish the explanation and write any remaining test code before that cue.
- Do not interrupt a connected coding sequence with a caveat about a feature
  we have not used yet. Keep the restriction in recording notes and introduce
  it on camera when it affects the example. Routine verification checkpoints
  can stay off camera when they add no new behavior for the viewer to see.
- Explain reused code from what is on screen in this episode. Do not substitute
  "we already did this for scalars" or similar references for the explanation.
  A viewer who missed the earlier implementation still needs to understand
  the next edit, without a recap of that entire episode.
- A text review is not an actual spoken rehearsal. State that distinction and
  retain pacing/voice risk when delivery has not been tested by the presenter.

### Literal code edits

For an explicitly approved **commit-review episode**, replace literal
Before/After blocks with small verified commits in a separate workspace.
Each script segment must name its real commit hash, files, exact diff command,
and the few hunks to explain. Show declarations and definitions in the same
checkpoint, including caller/build changes needed to keep it runnable. Explain
the need before showing the diff and the consequence while reviewing it.
Do not read every moved line aloud. Keep replay commands and full verification
in a separate checkpoint guide. Never apply checkpoints to the recording
checkout until requested, and check its current state before cherry-picking:
partially recorded work may already contain a migration. This exception also
applies to L08 and the live-build requirement when the creator chooses this
format; it does not authorize hidden implementation in normal coding episodes.

- For every edit, show **Before** and **After** in code fences. A location label
  can help navigation but must never substitute for the code itself.
- For additions, include unchanged surrounding code in both blocks so the
  insertion point is visible. For deletions, show what remains afterward.
- Show includes, signatures, storage changes, all affected callers and every
  mechanical replacement explicitly. Do not say "do the same for the other
  operators", "move these fields", or "update the accessors" and leave the
  actual edits for the presenter to infer.
- Use the smallest exact region with enough context to locate it. No ellipses
  or invented placeholder comments inside replacement code. Label unchanged
  reference code separately; it does not require a fake edit pair.
- Sequence pairs against the evolving source, not repeatedly against the
  episode's initial checkpoint. Clearly mark when a multi-edit change is not
  ready to compile. Avoid duplicate canonical implementations.
- Keep Before blocks in the recording guide, not obligatorily on the video.
  They reduce recording friction; they are not extra narration or a reason to
  re-explain unchanged code.

## Required structure

1. Cold problem or observable need.
2. Optional concise visual that immediately helps.
3. Code, calculation, failure, or experiment.
4. Brief series identification only when natural.
5. Progress through small implementation and payoff cycles.
6. Itemized recap.
7. A concise next-episode list, normally three concrete items.
8. Standard sign-off: `That brings us to the end of this episode. Thanks for
   watching, and I will see you next time.`
9. Approximately five clean seconds for Subscribe and complete-series playlist
    end-screen elements.

Do not add end-of-episode Q&A or retrieval questions to new long-form scripts.
No answer key, automatic answer comment or associated pin reminder is required.
Preserve historical videos and comments; do not delete them retroactively.
Questions that help explain a concept during the lesson remain allowed. This
change does not remove the Shorts discussion/next-experiment ending.

### First comment: extend the lesson

- For each new long-form publishing package, prepare one useful first-comment
  candidate tied to a specific choice or limitation in the recorded episode.
  This is separate from the video ending; do not restore closing Q&A or an
  answer key.
- Prefer a real engineering tradeoff, a small extension, or a practical
  consequence that the description does not already explain. State our own
  reasoning briefly, then ask one concrete question when it invites useful
  alternatives. A question is not compulsory if a correction or useful detail
  is more valuable.
- Make it understandable without remembering a timestamp or answering a quiz.
  Avoid generic engagement requests, repeated episode summaries, manufactured
  controversy, and promises to implement unapproved features.
- Use accurate C++ and deep-learning terms naturally. Apply the copy/SEO
  playbook to the comment as well as the announcement. No GitHub promotion or
  external-link dump in this comment.
- Record the chosen comment and its posting status in publishing.md. Preparing
  a candidate does not authorize posting it. Before an authorized post, inspect
  existing author comments; afterward, record its direct URL. No automatic
  pin reminder or repeated pin checks.
- Evaluate whether replies discuss the actual technical choice. Do not assume
  that adding a comment increases reach, retention, or subscriber conversion.

## Packaging

- Titles use exactly one vertical bar and end with
  `Deep Learning, All the Way Down #N`.
- Every episode needs a `publishing.md` that follows the
  [publishing-package checklist](publishing-playbook.md) and copy/SEO playbook:
  checklist plan first, actual package, audit, critique, and final score.
- The package includes title, description, chapters or their provisional state,
  any specifically planned comment, media filename, thumbnails, tags, X and LinkedIn copy,
  Reddit decision, separate Shorts plan, and end-screen checks.
- The long-form lesson remains a coherent 16:9 video. Never distort it to create
  vertical clips. Record Shorts separately.

## Scoring and decision

L01-L16 total **100 points**. Use the same status meanings for every draft:

| Status | Credit | Meaning |
| --- | ---: | --- |
| PASS | Full weight | The exact draft or checked evidence convincingly satisfies the item. Cite it. |
| PARTIAL | Half weight | A concrete attempt has a named weakness and repair. |
| FAIL | Zero | The item is missing or contradicted. |
| UNVERIFIED | Zero | Required evidence or the requested portion is unavailable. Name what is needed. |

Retain half-points. Never remove items from the denominator or silently use N/A.
For fragment work, label the total provisional and do not present it as the
whole episode's score.

**Mandatory checks: L01-L08, L12, L13, and L15.** A misleading promise, delayed
useful work, broken progression, missing explanation, or incomplete lesson
cannot be averaged away by good formatting.

- **Advance:** every mandatory check passes and no other FAIL or UNVERIFIED
  remains within script scope. List partial items and separate final-media work.
- **Rework:** editorial, visual-plan, or progression problems are repairable.
- **Hold:** missing technical proof or unresolved correctness blocks an honest
  recommendation. A limited fragment does not establish whole-episode readiness.

A specific visual plan may pass its script-level check without proving the
rendered asset. Estimate pacing honestly; final timing, legibility, audio,
resolution, and end screens still require final-media checks. Code claims need
verification before editorial advancement. Neither the score nor advancement
authorizes release or predicts performance.

Finish with `Score: X/100. Decision: advance/rework/hold.` State the most
important remaining weakness before that line. The audit and critique stay
in `script-review.md`, outside the recording script.

## Evidence and transfer boundaries

- [Episodes 1-6 long-form retention comparison](../analytics/reports/2026-08-29-long-form-retention-comparison-episodes-01-06.md):
  repeated opening drops, including topic-relevant prefaces, support the
  cold-open and earlier-progress experiment. Samples are small and unequal;
  interpolated retention and replay/navigation bumps are not causal proof.
- [Short 5 media and retention analysis](../analytics/reports/2026-09-02-short-05-instagram-retention-and-creative-analysis.md):
  synchronized code changes, selective emphasis, a familiar example, and visible
  proof are candidate teaching techniques to test in long form. Instagram reach
  does not establish their effect on YouTube long-form retention.
- Borrow clarity, timely evidence, purposeful visual attention, and a real
  reason to continue. Do not import mandatory controversy, deliberate gaps in
  the core explanation, sub-20-second limits, compulsory post-reveal questions,
  constant gestures/stickers, or the Shorts ending in place of our own.
- The workflow, weights, and timing targets are editorial directions, not
  calibrated platform ranking factors. Keep outcomes and experiments in
  [the experiment log](../../docs/logs/content-experiments.md), not this rubric.

For the next long-form opening test, record time to useful action and first
payoff, then inspect retention at 0:15, 0:30, 0:45, 1:00, and 2:00 and around
section transitions. Compare like-format videos at matched elapsed times;
record traffic mix, topic, age, sample size, and any edit to the source video.
Preserve technical depth while testing ordering. If several treatments change,
describe a bundled editorial test rather than attribute gains to one detail.

Related procedures: [critique check](../../docs/operations/critique-check.md),
[analytics and evidence](../../docs/operations/analytics-and-evidence.md),
[copy and SEO](platform-copy-playbook.md), and
[publishing checklist](publishing-playbook.md).
