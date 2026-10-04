# Episode 8 Reddit contribution

Prepared September 10, 2026. Draft only; nothing submitted or scheduled.

## Objective and placement

Return to r/learnmachinelearning with the tensor-autograd milestone that our
first post left open. Give readers a small, useful explanation of broadcast
gradients, show the implementation's actual boundary, and invite concrete
testing advice. The video is a walkthrough of the work, not the opening pitch.

- Subreddit: r/learnmachinelearning.
- Format: text post with Project flair, which is present on the original post
  and in the retrieved community feed. Verify the current composer before submission.
- Title and body below are the canonical version.
- Links: repository first, Episode 8 second. No hashtags or separate keyword block.
- Default window: Sunday, September 13, 12:30 PM ET, following the standing
  Reddit cadence. Reserve the following two hours for replies. This is an
  operating choice, not a measured best time; the completed milestone can also
  be shared earlier if the creator has time to participate. No need to wait
  for another episode just to make this post worthwhile.

The August 30 post reached a creator-reported 21,000 views and 115 upvotes at
roughly 48 hours. YouTube subscribers rose from 46 to 59 during that window;
we cannot attribute every subscriber to Reddit. The useful pattern was a
concrete project, inspectable technical detail, and a real design question.
Source: [48-hour checkpoint](../analytics/reports/2026-09-01-reddit-48h-checkpoint.md).

## Final post

### Title

```text
Adding autograd to my C++ tensor library from scratch
```

### Body

```text
I've been building a C++ tensor library to understand how automatic differentiation works underneath frameworks like PyTorch.

In my previous post, the tensor and scalar autograd implementations were still separate. I've now connected the tensor to shared graph nodes. Each result keeps its data, gradients, operation, and input nodes alive for the backward pass.

The graph records whole tensor operations. Adding two matrices creates one result node, so we need to work out which input element receives each gradient contribution.

Broadcasting makes that interesting. If a scalar bias is added to three values, all three outputs depend on the same bias. Given incoming output gradients of [2, 3, 4], the bias needs to receive 2 + 3 + 4 = 9.

I reuse the broadcast strides from the forward pass to find the input indices. A broadcast dimension has a zero stride, so those contributions land on the same gradient entry and accumulate with +=.

The backward rules for addition, subtraction, multiplication, and division are in place. The public backward() entry point currently requires a scalar result; reduction and matrix multiplication backward are still next. Those will let me connect the tensor operations to a loss and build a linear regression training loop.

Code and episode checkpoints:
https://github.com/mechanical-turk/deep-learning-all-the-way-down

I recorded the implementation in Episode 8 of Deep Learning, All the Way Down:
https://www.youtube.com/watch?v=RXCeVnhjHCQ

If you've implemented tensor autograd, which broadcasting edge cases would you put in the gradient tests first?
```

## Technical verification and limits

Checked the local source, public Episode 8 checkpoint
[7021cfe](https://github.com/mechanical-turk/deep-learning-all-the-way-down/blob/7021cfe/main.cpp),
the current README, and the [Episode 8 publishing record](../chapter-08/publishing.md).

- TensorNode stores shape, data, gradients, operation, parents and effective strides.
- The reverse traversal selects a local-derivative lambda for each arithmetic operation.
- backward_elementwise maps output coordinates through the two saved stride arrays.
  It uses += for both input gradients, multiplied by the incoming gradient and local derivative.
- The public backward() requires rank zero and seeds its gradient with one.
  Unsupported operations reach the default error. Sum and matmul forward history
  exist, but their backward implementations are absent at this checkpoint.
- The [2, 3, 4] example is an illustrative local backward calculation with a
  supplied upstream gradient. It is not claimed to be output printed by the
  current program or an example runnable through its scalar-only public API.
- Do not add a loss = tensor.sum(); loss.backward() example to this post until
  reduction backward actually exists. Do not claim a trained model or full tensor
  training support.
- The September 10 source-checkpoint ledger records an existing empty-tensor
  broadcasting failure. Do not claim exhaustive correctness. If the discussion
  reaches empty dimensions, acknowledge that known issue rather than pretend it
  is an unexplored suggestion. Keep this post's question about prioritizing tests honest.

## Community and keyword research

Research date: September 10, 2026. Platform: Reddit only.

Sources inspected:

- [Current subreddit rules](https://www.reddit.com/r/learnmachinelearning/about/rules.json):
  sharing work is allowed; repeated content is limited to at most once weekly;
  referral links, paid-course marketing and transactional promotion are prohibited.
- [Original live post](https://www.reddit.com/r/learnmachinelearning/comments/1w2m6o3/i_built_tensor_operations_and_scalar_autograd/):
  it explicitly left the shared-node decision open. The retrieved comments
  include interest in the gradient visual and separate shared nodes. This makes
  the new architecture a relevant follow-up without claiming the community
  unanimously chose it.
- [Submitted-post listing](https://www.reddit.com/user/mechanical_kazan/submitted/):
  the fetched listing shows the original project post and an older unrelated
  project. No newer DLATWD post appeared in that response. Recheck before posting;
  cached relative dates and incomplete listings are not exact publication evidence.
- [Current new feed](https://www.reddit.com/r/learnmachinelearning/new/): learning
  questions and project contributions are present. No trustworthy vote comparison
  or posting-time performance conclusion can be drawn from the retrieved feed.
- [Previous research](../production/reddit-engagement-research-2026-08-29.md) and
  [Reddit strategy](../production/reddit-distribution-strategy.md): preserve the
  concrete project-and-question structure rather than repeat the old feature list.

Candidate phrases: C++ tensor library, tensor autograd, autograd from scratch,
automatic differentiation, broadcasting gradients, backpropagation.

Primary search language: C++ tensor library and autograd, both in the title.
The opening naturally adds automatic differentiation and PyTorch as context,
without suggesting this is a PyTorch extension or a replacement framework.
Supporting terms in the body include graph nodes, backward pass, broadcasting,
gradient accumulation, strides, matrix multiplication and linear regression.
Future capabilities are explicitly identified as future work.

Hashtags retained: none. Rejected: every hashtag block, generic AI tags, and
unrelated CUDA/LLM terms. Reddit readers get descriptive language, not a tag list.

Unavailable evidence: Reddit query volumes, current keyword rankings, a complete
account activity history and fresh post-insights metrics. No optimal-title or
conversion prediction is claimed.

## Presentation and submission checks

The text stands alone. Do not reuse Episode 7's scalar-gradient diagram as if it
showed the tensor implementation, and do not use the Episode 8 promotional
thumbnail as technical proof. An optional new diagram could show one bias
receiving three gradient contributions, but no new asset is required or created
by this draft. The first post's visual attracted positive comments; omitting a
visual here is a presentation tradeoff, not a finding that images do not matter.

Before submitting:

- Recheck the rules and recent account activity for a new overlapping post.
- Open the repository and Episode 8 links; inspect the rendered text and flair.
- Keep GitHub before YouTube and the narrow test question last.
- Capture the default analytics snapshot immediately before publication for
  later comparison. Do not pull tweet metadata without an explicit request.
- Make sure the creator can reply during the first two hours; otherwise move
  the operating window. No automated submission or reminder has been created.

After publication:

- Run the post-publication checks and record the direct URL and exact ET time
  in the append-only distribution timeline.
- Answer substantive replies with implementation details. Do not tag previous
  commenters, message them, or paste a video promotion into unrelated threads.
- Revisit at 24, 48 and 72 hours and seven days. Record Reddit views, score,
  comment themes, available repository traffic and YouTube referral/subscriber
  changes separately. Treat attribution and timing conclusions cautiously.

## Critique

This follows through on a question the community already saw and offers an
understandable broadcast-gradient example before either link. The title describes
the new work and leaves room for its incremental scope. It avoids claiming the
library can already train a model.

The main limitation is that the public API cannot yet run a full broadcasted
vector-to-scalar loss backward pass. The draft names that limitation instead of
promising a finished autograd framework. The post is more implementation-focused
than the first broad introduction; its success should be judged partly by the
quality of technical replies, not by demanding another 21,000-view result.

Copy checks: subject and scope verified; natural keyword placement; no hashtags,
em dashes, canned contrast, invented results or release-opening boilerplate;
GitHub-first links; one specific closing question. Ready for creator review.
Live composer and final pre-submission checks remain pending. Nothing published.
