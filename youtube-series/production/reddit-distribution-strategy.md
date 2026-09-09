# Reddit distribution strategy

## Why Reddit is now a core channel

The first standalone Reddit post was published in r/learnmachinelearning on
August 30, 2026. Within roughly 48 hours, it reached:

- 21,000 views;
- 115 upvotes;
- top post of the day; and
- a period in which the YouTube channel grew from 46 to 59 subscribers.

Episode 7 also moved from 122 to 445 public YouTube views during that window.
The timing strongly suggests that Reddit contributed to the growth, although
delayed platform attribution means we cannot assign every view or subscriber
to Reddit.

One successful post is not enough to establish a stable conversion rate. It is
enough to establish Reddit as the strongest qualified external distribution
channel tested so far and justify a deliberate weekly operating process.

Detailed checkpoint:
`../analytics/reports/2026-09-01-reddit-48h-checkpoint.md`

## What worked

The post did not announce one episode. It presented a concrete seven-episode
project milestone:

- tensor operations;
- broadcasting and matrix multiplication;
- mean squared error;
- scalar reverse-mode autograd; and
- the next engineering decision.

It included enough implementation detail for readers to judge the work, linked
the public GitHub repository before the YouTube playlist, and ended with one
specific architecture question. The subreddit matched the learning project and
the post used ordinary technical language rather than promotional copy.

## Weekly process

Every week:

1. Review the latest project milestone and unresolved technical question.
2. Identify one subreddit or recurring thread where that work is relevant.
3. Read its live rules and recent posts before drafting.
4. Choose one useful angle for that community.
5. Publish on Sunday between 12:00 and 2:00 PM ET when a qualified post is
   ready, or record an explicit defer.
6. Answer substantive replies during the first two hours and revisit the thread
   over the next week.
7. Capture 24-hour, 48-hour, 72-hour, and seven-day checkpoints.
8. Compare views, discussion quality, repository traffic, YouTube referral
   traffic, and subscriber movement against the pre-post snapshot.

## Submission rules

- Do not use Reddit as an episode announcement feed.
- Do not paste the same post into several communities.
- Do not force weekly self-promotion when there is no new milestone.
- Do not post to a subreddit without checking its current rules.
- Do not ask for upvotes or coordinate voting.
- Lead with the work, not the creator or content schedule.
- Include concrete code, measurements, diagrams, or results when they help the
  reader evaluate the claim.
- Put owned links after the technical substance.
- Prefer GitHub before YouTube for project posts.
- End with one narrow question that can produce useful technical discussion.
- Treat comments as research for the implementation and future content.

## Community map

- **r/learnmachinelearning:** major learning milestones, implementation
  retrospectives, and questions about the next conceptual boundary.
- **r/cpp:** use the current Show and Tell thread unless the live rules clearly
  support a standalone post. Focus on C++ ownership, APIs, performance, and
  tooling.
- **r/deeplearning:** revisit after tensor autograd or a complete training loop
  produces a clear deep-learning result.
- **r/MachineLearning:** use only placements permitted by its current rules.
  Do not disguise promotion as a research post.
- **Other technical subreddits:** add them only after checking topic fit,
  promotion rules, and recent community norms.

## Current experiment

The next Reddit contribution should not repeat the tensor-and-scalar-autograd
milestone in r/learnmachinelearning. Wait for meaningful new work, such as
tensor autograd, a complete training loop, or a trained model. In the meantime,
participate in relevant discussions and consider a separately written r/cpp
Show and Tell contribution focused on the C++ design.
