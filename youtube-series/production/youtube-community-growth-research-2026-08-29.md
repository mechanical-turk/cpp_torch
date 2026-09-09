# YouTube Posts and Communities growth research

Research date: August 29, 2026

## Conclusion

Use YouTube Posts now. They can put polls, quizzes, images, text, and videos on
the channel, Home, and Subscriptions surfaces. Image posts can also appear in
the Shorts feed. Their best role for this channel is not announcing every
upload. They should turn technical ideas into low-friction participation,
collect topic evidence, and give interested viewers a reason to return between
videos.

Run an eight-post experiment over four weeks. Publish two posts per week and
keep them separate from the long-form and Short production quotas. Most posts
should ask or answer one concrete C++ or machine-learning question. At most one
of the eight should be a direct video-link post.

The newer subscriber Community is a separate feature. Enable it only as a
moderated 30-day experiment, not as a growth assumption. Public Posts remain
the main reach tool. The subscriber Community is for deeper conversation among
people who already chose to subscribe.

## Two features that share similar names

### Public Posts

The Posts tab lets a creator publish text, images, GIFs, polls, quizzes, music,
and videos. Posts can appear:

- on the channel's Posts tab and Home shelf;
- in viewers' Home and Subscriptions feeds;
- in some subscriber notifications; and
- in the Shorts feed when the post is an image post.

These distribution surfaces make Posts useful for reach beyond the current
subscriber list. YouTube says Posts can provide more reach and engagement, but
it does not promise distribution or publish a formula for earning it.

### Subscriber Community

Communities are opt-in discussion spaces where subscribers can create posts as
well as respond to the creator. Community-only posts do not appear in the
normal Posts tab, although YouTube says they can still be recommended on Home,
Subscriptions, and Watch surfaces.

YouTube reported in November 2025 that channels in an internal Communities
experiment saw higher post impressions and likes on average. YouTube did not
publish the effect size, sample, or experimental design. Treat this as a reason
to test the feature, not evidence that enabling it will grow the channel.

## What the evidence supports

### 1. Posts can reach outside the subscriber base

Current YouTube documentation says Posts can appear on Home and other feeds,
not only on the channel page. This makes them a discovery surface, although the
creator cannot control who receives each post.

### 2. Posts should complement uploads

YouTube repeatedly recommends a regular schedule that complements video
uploads. Its examples include polls about the next video, previews, quizzes,
behind-the-scenes images, and follow-up questions.

The useful principle is not maximum frequency. It is continuity: a viewer can
interact with the same subject before or after watching the video.

### 3. A video-link post can duplicate an existing impression

YouTube explicitly says a post about a video already shown in a viewer's Home
or Subscriptions feed might not appear again. The platform does this to avoid
showing the same video repeatedly.

Do not make an immediate "new episode is live" video post the default. Let the
upload occupy the release slot. Use a later post only when it adds a question,
result, diagram, correction, or other standalone value.

### 4. Low-friction formats are useful, but votes are not market research

Polls and quizzes require one tap and are well suited to technical questions.
They can reveal which subjects attract the people YouTube chose to show the
post to. They do not represent the entire subscriber base, and they do not
prove that the winning answer will become a successful video.

Use poll results as idea evidence, not as a production order.

### 5. Creator interaction can deepen participation

YouTube recommends replying to and hearting comments on Posts. Research on
creator hearts in video comments also found that early positive creator
feedback can encourage more commenting. That research concerns video comments,
not Posts, so it supports the general interaction principle rather than a
specific Posts growth claim.

### 6. There is no defensible universal posting frequency

YouTube documents a per-day safety limit but does not publish the number. It
does not prescribe a daily or weekly growth frequency. Third-party advice
varies widely and usually lacks controlled evidence.

For this channel, two posts per week is an operational starting point. It is a
testable choice that protects production time, not a platform rule.

## Role in this channel's growth system

The content system already has clear jobs:

- Shorts introduce one sharp technical idea to new viewers.
- Long-form episodes build trust and depth.
- GitHub proves that the implementation exists and remains usable.
- YouTube Posts create participation and continuity between those releases.
- The subscriber Community, if enabled, gives recurring viewers a place to
  discuss the work with one another.

Posts should not become another announcement feed. A good post must do at least
one of these jobs:

1. make a technical question easy to answer;
2. reveal a useful result;
3. ask viewers to choose between real production options;
4. show a meaningful piece of the work in progress; or
5. resurface an older lesson because it answers the current question.

## Four-week experiment

Publish eight public Posts across four weeks. Keep the main video and Short
cadence unchanged.

### Post 1: prediction poll

Use the instruction-dependency idea before recording it:

> These loops add the same values. Which version do you expect to run fastest?

Offer 1, 2, 4, and 16 accumulators. Do not reveal the result in the post.

### Post 2: result and explanation

Show a compact benchmark image. State the machine and compiler configuration.
Explain in one sentence that independent accumulation chains expose more
instruction-level parallelism. Ask where the performance stops improving.

Do not attach a video link unless the matching Short or episode adds a
substantial explanation that the post cannot contain.

### Post 3: C++ quiz

Show a short unsigned reverse loop and ask what happens at zero. Use the quiz
explanation field to state the answer after the viewer responds.

### Post 4: production decision

Ask a real choice that can change upcoming work, such as which implementation
should be benchmarked next. Do not ask viewers to choose between topics that
will be produced regardless of the result.

### Post 5: autograd graph question

Use one clean computation-graph image and ask where gradient contributions
must add instead of overwrite. This connects directly to Episode 7 without
reposting the episode.

### Post 6: behind the scenes

Show a real intermediate artifact: a failed benchmark, surprising assembly,
or a code design that was later removed. State what changed. Avoid generic
desk, camera, or editing updates unless they contain a useful production lesson.

### Post 7: catalog resurfacing

Choose one older episode because it resolves the week's question. Lead with
the technical point. Include the video only after the post explains why it is
relevant.

### Post 8: audience research

Ask which unresolved systems question viewers most want tested next. Use four
specific, comparably scoped options. Compare the result with actual video and
Short performance before committing the next production slot.

## Timing

YouTube's Audience report includes "When your viewers are on YouTube" for the
previous 28 days. Use it when the channel has enough data. Schedule a post
roughly 30 to 60 minutes before the strongest relevant block, then keep the
timing stable long enough to compare posts.

If the report is unavailable or sparse, alternate two fixed Eastern Time slots
for the first eight posts, such as noon and 7:00 PM. Do not infer an ideal time
from one post.

Avoid publishing a Post close to a new upload. Start with these gaps:

- question or poll: 18 to 24 hours before the related release;
- follow-up or result: 24 to 48 hours after release; and
- unrelated post: on a non-release day.

These gaps are experiment controls, not YouTube rules.

## Writing and visual rules

- Give each post one idea and one action.
- Put the concrete technical question in the first sentence.
- Keep the answer choices mutually exclusive and easy to scan.
- Make image posts square when practical; YouTube recommends 1:1 in the feed.
- Make every post useful without requiring a click.
- Use natural C++, machine learning, and systems terms. Do not keyword-stuff.
- Avoid generic engagement bait, unrelated polls, and fake production choices.
- Do not use a link as the hook.
- Reply when a viewer contributes a real question, correction, or observation.

## Measurement

YouTube documents these Posts metrics:

- impressions;
- likes;
- poll votes; and
- top posts by likes or votes.

Record each post's format, topic, publication time, impressions, likes, votes,
comments, and whether it included a video. Calculate interactions per
impression for comparison, but do not treat it as an official YouTube metric.

Review after all eight posts. Compare like with like:

- poll against poll;
- quiz against quiz;
- image explanation against image explanation; and
- topic against similar topic.

Then inspect channel-level returning, casual, and regular viewer reports.
YouTube says these segments do not directly determine reach. They are useful
for understanding whether viewers continue returning. Because this channel is
young, the regular-viewer segment needs months to become meaningful.

YouTube does not document a clean Post-to-video click-through metric in Posts
analytics. Do not claim that a post caused later video views from timing alone.
Treat changes in video traffic sources and viewing patterns as directional.

## Subscriber Community setup

If the Community feature is available, test it for 30 days with:

- Basic moderation;
- a one-day minimum subscription period before viewers can post;
- one pinned welcome post;
- no expectation of daily viewer-created activity; and
- a weekly moderation check.

Suggested channel guidelines:

1. Questions and corrections are welcome.
2. Challenge ideas, not people.
3. Keep posts relevant to C++, machine learning, or systems.

Use public Posts for reach. Use Community-only posts for conversations that
specifically benefit current subscribers. If the space remains empty, do not
manufacture activity. Keep the public Posts experiment and revisit Communities
after recurring commenters emerge.

## Claims this research does not support

- Posting every day makes YouTube recommend the channel.
- Polls automatically increase video distribution.
- Post engagement is a ranking signal for unrelated videos.
- Community activity converts to subscribers at a known rate.
- One winning poll predicts a winning video.
- There is one best posting time or frequency for every channel.

## Sources

Primary YouTube sources:

- Learn about Posts: https://support.google.com/youtube/answer/9409631
- Create a Post: https://support.google.com/youtube/answer/7124474
- Posts tips: https://support.google.com/youtube/answer/11912631
- Posts performance analytics: https://support.google.com/youtube/answer/12340301
- Understand YouTube audiences: https://support.google.com/youtube/answer/9314416
- New, casual, and regular viewers: https://support.google.com/youtube/answer/10246996
- Start a Community: https://support.google.com/youtube/answer/15739414
- Moderate a Community: https://support.google.com/youtube/answer/15739725
- Set channel guidelines: https://support.google.com/youtube/answer/11895180
- Communities product announcement and experiment note:
  https://support.google.com/youtube/thread/321825573/
- YouTube Community Playbook:
  https://services.google.com/fh/files/misc/community_repost_playbook.pdf
- YouTube creator-community guidance:
  https://blog.youtube/creator-and-artist-stories/community-on-youtube/

Supporting research:

- Creator Hearts: Investigating the Impact Positive Signals from YouTube
  Creators in Shaping Comment Section Behavior:
  https://arxiv.org/abs/2404.03612

Third-party frequency and growth claims were reviewed but excluded from the
operating recommendations when they lacked disclosed samples, methods, or
controls.
