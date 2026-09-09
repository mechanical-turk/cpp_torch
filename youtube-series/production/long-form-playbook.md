# Long-Form Playbook and Checklist

Read this before planning, writing, reviewing, or publishing a long-form episode
of Deep Learning, All the Way Down. This is the authoritative long-form script
checklist. Keep its pacing and evidence separate from the Shorts playbook.

## Required script-writing workflow

Every new or rewritten long-form script must contain these sections in order,
without requiring a separate critique request. Put the descriptive proposed
MP4 filename above them.

1. **Checklist plan:** explain how this draft will attempt every item L01-L16.
   Use one concise row per ID with the actual intended beat, visual, code,
   evidence, or known risk. Identify the opening promise, first useful action,
   first payoff, and the capability gained in each section. Intention is not
   proof of compliance.
2. **Script:** one canonical draft, with `>` marking only spoken narration.
   Keep code, estimated timecodes, scene directions, and review notes outside
   narration. Use the episode structure below.
3. **Checklist audit:** assess that exact draft against every L01-L16 item.
   Give status, a specific beat or evidence reference, awarded points, and a
   repair for each shortfall. Do not copy the plan and call it an audit.
4. **Critique:** prioritize the biggest obstacles to viewer understanding,
   useful progress, and trust. Explain their consequences and the next repair.
   Do not invent faults or add cosmetic revisions to inflate an iteration count.
5. **Final score:** calculate the score out of 100 and give the decision
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
- Keep uncommitted content ideas in `youtube-series/content-ideas.md`, separate
  from active scripts and release packages.
- Give new examples meaningful names such as `predictions` and `targets`.
  Do not carry numbered test variables such as `pred_23` into new lessons.
  Initialize a fresh example explicitly when historical test setup is irrelevant.

## Long-form script checklist

Weights express editorial priorities, not measured contributions to retention.

### Promise and opening

- [ ] **L01 | Specific, achievable promise | 10 points.**
  Does the opening state a concrete problem and a capability we will deliver,
  rather than merely name the topic? Identify the current limitation, desired
  result, and scope boundary. Check the preceding episode's recorded promise
  against its captions and code; explain any necessary scope change. The
  title's promise must match the lesson, not a more ambitious future episode.

- [ ] **L02 | Clear cold opening | 10 points.**
  Do the first sentence and first frame point to the same understandable need?
  Put meaningful subject and stakes before setup. Begin with relevant existing
  code, a real failure, a calculation, or a concise narrated visual. No greeting,
  series premise, roadmap, recap, previous answers, or setup commands. Supply
  only the prerequisite a new viewer needs for this action. A visual is optional
  and must explain faster than code; no silent slideshow or repeated titles.

- [ ] **L03 | Useful action immediately | 8 points.**
  Does the beat after the promise start changing, running, or deriving something
  useful instead of re-explaining what we will do? Name the action and its
  estimated time. Audit 15 and 30 seconds explicitly. Thirty seconds is an
  outer review target, not permission to spend the opening talking. Cursor
  movement, imports, and ceremonial typing do not count as meaningful progress.

- [ ] **L04 | First payoff within one minute | 8 points.**
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
  Write the final validation logic when it is already known. Do not introduce
  a temporary whitelist merely to match unfinished code and replace it later.
  Label incomplete recording stages instead of adding disposable scaffolding.
  Put validation at its teaching need, not merely its final source position.
  First demonstrate the supported behavior; introduce an unsupported-path
  check when the viewer can see what is supported and what the failure would
  disrupt. Code that belongs early in a function need not be taught first.

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
  Identify the primary subject phrase and accurate supporting search terms.
  Keep the title, promise, and actual implemented scope aligned. Follow the
  copy/SEO playbook for public filenames, titles, and other copy; candidate
  keywords alone are not SEO approval. Route the later publishing package to
  its own checklist rather than treating a script score as publishing approval.

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

**Mandatory checks: L01-L08, L12, and L13.** A misleading promise, delayed
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
outside read-aloud narration.

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
