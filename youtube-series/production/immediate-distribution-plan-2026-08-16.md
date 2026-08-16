# Immediate Production and Distribution Plan

Created Sunday, 2026-08-16 at approximately 2:30 PM ET. This schedule covers
the launch of Episode 3, production of Episodes 4 and 5, and the first native
cross-platform Short cycle. Exact completed timestamps belong in
`docs/distribution-timeline.md`.

## Operating priorities

1. Keep the Monday-Wednesday-Saturday long-form cadence viable.
2. Improve openings and time-to-first-payoff without redesigning the series
   from incomplete retention data.
3. Give each release one X announcement and one later LinkedIn announcement.
4. Record Shorts natively; do not extract them from long-form recordings.
5. Use Reddit and Hacker News as communities, not syndication endpoints.
6. Protect at least 70% of available project time for scripting, implementation,
   recording, and editing rather than distribution.

## Sunday, August 16

### 2:30-3:00 PM: finish Short 1 launch

- [x] Publish Short 1.
- [x] Post and pin its channel comment.
- [ ] Confirm Episode 2 is selected as its related long-form video.
- [ ] Confirm it belongs to the dedicated Shorts playlist.
- [ ] Reply to any substantive early comment.

### 3:00-3:45 PM: prepare native distribution

- [ ] Export the clean 1080x1920 file without YouTube UI or watermark.
- [ ] Prepare native X caption and accessibility text.
- [ ] Prepare a distinct LinkedIn-native caption; do not paste the X copy.

### Around 4:00 PM: native X Short

- [ ] Upload the video directly to X.
- [ ] Keep the main post self-contained; put Episode 2, the playlist, and source
  code in one reply.
- [ ] Be available for replies for approximately 30 minutes.

Suggested main copy:

```text
An empty tensor shape does not describe an empty tensor.

Why [] contains one value while [0] contains none:
```

Navigation reply:

```text
Full tensor lesson:
https://www.youtube.com/watch?v=8kzL5NdxGCo

Complete series:
https://www.youtube.com/playlist?list=PLZSg76FHvdTw

Source code:
https://github.com/mechanical-turk/deep-learning-all-the-way-down
```

### 4:30-8:00 PM: Episode 4 critical path

- [ ] Finalize Episode 4's learning promise and dependency chain.
- [ ] Write and validate its complete single-file reference implementation.
- [ ] Draft the full recording script using the established episode structure.
- [ ] Stop before recording if the code or conceptual sequence remains unstable.

### Personal X presence

- [ ] Publish at most one genuine process post in the evening, separated from
  the native Short by at least two hours.

Candidate:

```text
there’s something deeply humbling about speaking to a camera by yourself for hours on end
```

## Monday, August 17: Episode 3 launch

### 9:30-10:15 AM: release gate

- [ ] Capture Episode 2's approximately 48-hour analytics before Episode 3
  changes channel traffic.
- [ ] Verify Episode 3 visibility, final description, chapters, captions,
  thumbnail, playlist, end screen, and comments.

### 11:00 AM: YouTube

- [ ] Confirm Episode 3 publishes successfully.
- [ ] Post and pin its prepared comment.
- [ ] Verify the public video from a signed-out or private browser window.

### Around 12:00 PM: X announcement

- [ ] Publish the prepared Episode 3 announcement with its direct YouTube URL.
- [ ] Add the standard playlist and GitHub navigation reply.
- [ ] Respond to substantive replies without posting another launch link.

### 1:30-5:30 PM: Episode 4 recording

- [ ] Complete a final read-through and compile/run check.
- [ ] Record Episode 4 long-form.
- [ ] Back up the recording and begin the edit immediately.

### Personal X presence

- [ ] Optional evening post only if a real recording or learning observation
  emerges. Do not attach the episode link.

## Tuesday, August 18

### 9:00-10:30 AM: LinkedIn Episode 3

- [ ] Publish the prepared Episode 3 LinkedIn post.
- [ ] Link directly to YouTube and answer technical comments.

### Main work block: Episode 4 post-production

- [ ] Finish edit, captions, thumbnail, chapters, description, and end screen.
- [ ] Run the complete upload QA checklist.
- [ ] Schedule Episode 4 for Wednesday at 11:00 AM only if it passes.

### Short and personal content

- [ ] Outline one native Short teaching a single Episode 3 idea.
- [ ] Publish one concise personal X post if there is a genuine observation.
- [ ] Do not publish another promotional link post.

## Wednesday, August 19: Episode 4 launch

### 10:00 AM

- [ ] Capture Episode 1's seven-day analytics baseline.
- [ ] Run Episode 4's final public-release checks.

### 11:00 AM and noon

- [ ] Publish Episode 4 on YouTube at 11:00 AM.
- [ ] Post and pin its channel comment.
- [ ] Announce it on X around noon with the standard navigation reply.

### Afternoon production block

- [ ] Record the Episode 3-derived native Short.
- [ ] Begin Episode 5's script and validated implementation.

### LinkedIn native Short

- [ ] Do not publish Short 1 here today; Episode 4 already owns the day's main
  release window.

## Thursday, August 20

### 9:00-10:00 AM: LinkedIn native Short 1

- [ ] Upload Short 1 directly to LinkedIn.
- [ ] Use a self-contained explanation; place the full lesson link at the end,
  not as the opening sentence.
- [ ] Compare native video completion and comments with the X upload later;
  do not compare raw view counts as equivalent metrics.

### Late morning: Reddit r/cpp

- [ ] Participate in the current r/cpp August Show and Tell thread.
- [ ] Lead with the evolving C++ learning project and repository.
- [ ] Describe what is implemented, what feedback is wanted, and what remains
  intentionally simple.
- [ ] Include the playlist only as secondary context. Do not submit a bare
  Episode 3 or Episode 4 link.

The current thread explicitly accepts personal C++ projects and asks for links,
making this the appropriate r/cpp venue.

### Main work block

- [ ] Record Episode 5 long-form.
- [ ] Back up the footage and begin editing.

## Friday, August 21

### Around noon: Episode 3 native Short

- [ ] Publish the independently recorded Short on YouTube.
- [ ] Add the related Episode 3 video, Shorts playlist, and pinned comment.
- [ ] Delay X and LinkedIn native reposts; give the YouTube Short its own first
  measurement window.

### Main work block

- [ ] Finish Episode 5 editing and release package.
- [ ] Schedule Episode 5 for Saturday at 11:00 AM if all gates pass.

### Reddit ML decision

- [ ] Inspect the active r/MachineLearning self-promotion thread.
- [ ] Post only if the framing is about learning ML internals and is materially
  distinct from the r/cpp contribution.
- [ ] Otherwise defer until the project has autograd or a trainable model.

## Saturday, August 22: Episode 5 launch

- [ ] Capture Episode 2's seven-day analytics around 10:00 AM.
- [ ] Publish Episode 5 at 11:00 AM.
- [ ] Post and pin its comment.
- [ ] Announce on X around noon with the standard navigation reply.
- [ ] Begin only light Episode 6 planning after launch; protect recovery time.

## Blog strategy

Do not publish a thin episode recap this week. Begin a durable technical article
after Episode 3 is public:

- [ ] Draft working title: `What a Tensor Actually Has to Guarantee`.
- [ ] Synthesize shape, rank, storage invariants, checked indexing, scalar and
  empty shapes, mutation, reduction, and operations.
- [ ] Include diagrams and compilable excerpts, but make the article useful
  without watching the videos.
- [ ] Draft Thursday or Friday in short blocks only after production work.
- [ ] Target publication Tuesday, August 25, then share it separately on X and
  LinkedIn. It should not compete with a same-day episode announcement.

## Hacker News strategy

Do not submit the current episode announcements to Hacker News. A Show HN should
offer something people can directly try and discuss, and HN asks users to become
genuine community participants before occasional self-promotion.

- [ ] Continue building the public repository and participate naturally on HN.
- [ ] Reconsider Show HN when the repository can train its first model end to
  end, or when the durable tensor article and code form a substantial standalone
  artifact.
- [ ] Use one honest submission, remain available for discussion, and avoid
  coordinating votes when that gate is reached.

## Daily maintenance

- [ ] Respond to comments once or twice daily; do not refresh continuously.
- [ ] Record exact publication timestamps and URLs in the distribution ledger.
- [ ] Capture analytics at planned 24-hour, 48-hour, and seven-day checkpoints.
- [ ] Keep one or two personal X posts on most active days, only when genuine.
- [ ] Keep GitHub's README episode index and playlist links current.
- [ ] Preserve one no-promotion block every day for actual C++ and ML learning.

## Success criteria for this week

- Episodes 3, 4, and 5 publish only if their quality gates pass.
- Two native Shorts are public on YouTube by Friday.
- Short 1 receives one native X upload and one native LinkedIn upload.
- The r/cpp contribution is contextual and feedback-seeking.
- No premature Hacker News submission or low-substance blog post is published.
- Distribution does not displace the learning and production work that creates
  the next substantial artifact.
