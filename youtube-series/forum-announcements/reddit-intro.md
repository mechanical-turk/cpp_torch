# Reddit introduction

## Decision

This recommendation comes from the live subreddit rules, current comparable posts, and the code that is public today. It replaces the earlier generic series title.

- **Subreddit:** `r/learnmachinelearning`
- **Format:** Rich-text post with the `Project` flair
- **Publish:** Sunday, August 30, 2026 at **12:30 PM ET**
- **Availability:** Stay active in the thread until at least 2:30 PM, then check it again that evening and over the next two days
- **Visual:** Upload the computation-graph image listed below inside the post
- **Links:** GitHub first, YouTube playlist second, both near the end
- **Repeat promotion:** Do not promote the series again in `r/learnmachinelearning` for at least one week. Any later post in another community must use new copy and follow that community's rules

The time is an operating window, not a claim about a universal best hour. It leaves space after the morning LinkedIn post and gives us two uninterrupted hours to answer comments.

## Final post

### Title

```text
I built tensor operations and scalar autograd from scratch in C++
```

### Body

```text
I started this project because I wanted to see what sits beneath PyTorch tensor operations and loss.backward().

The tensor currently supports flat storage, multidimensional indexing, elementwise operations, reductions, broadcasting, rank-two matrix multiplication, and mean squared error.

On my last update (#7), I added a separate scalar reverse-mode autograd engine. Arithmetic operators build a computation graph during the forward pass. backward() creates a topological order, walks it in reverse, applies each operation's local derivative, and accumulates gradients when a value reaches the loss through more than one path.

The example builds this expression:

Value prediction = w1*x1 + w2*x2 + w3*x3 + bias;
Value residual = prediction - target;
Value loss = residual * residual;
loss.backward();

For weights [0.5, -1.0, 2.0], inputs [4.0, 3.0, 2.0], bias 0.5, and target 2.5, the forward pass produces prediction 3.5 and loss 1. The backward pass recovers:

- dL/db = 2
- dL/dw = [8, 6, 4]

Scalar autograd still lives separately from the tensor implementation. The next step is connecting graph identity, ownership, and gradients to tensors before building a training loop.

Code and Git checkpoints:
https://github.com/mechanical-turk/deep-learning-all-the-way-down

Videos:
https://www.youtube.com/playlist?list=PLZSg76FHvdTw

For the tensor integration, would you keep autograd metadata inside each Tensor handle, or have tensors point to separate shared graph nodes? I would appreciate design feedback before I commit to that boundary.
```

## Visual

Upload [autograd-full-model-opening-v4.png](../chapter-07/assets/autograd-full-model-opening-v4.png) after the paragraph that explains reverse-mode automatic differentiation.

**Caption:**

```text
The scalar computation graph and the parameter gradients recovered by backward().
```

**Alt text:**

```text
A scalar computation graph for a linear prediction and squared loss, with gradients flowing backward to three weights and one bias.
```

Do not use the YouTube thumbnail. The computation graph is technical evidence and gives Reddit readers something they can inspect before opening either link.

## Search and keyword audit

The title carries the primary search terms without stuffing them:

- `C++`
- `tensor operations`
- `scalar autograd`
- `from scratch`

The body naturally adds:

- `deep learning`
- `PyTorch`
- `loss.backward()`
- `broadcasting`
- `matrix multiplication`
- `mean squared error`
- `reverse-mode automatic differentiation`
- `computation graph`
- `topological order`
- `gradient accumulation`
- `training loop`

Do not add hashtags. Do not repeat the keywords in a separate keyword block. Reddit search can understand the title and body, while readers should encounter ordinary technical writing.

## Why this version

The title covers the full public checkpoint instead of announcing only Episode 7. It names the tensor work from the first six episodes and the scalar autograd milestone from the seventh. The body states clearly that tensor autograd has not been implemented yet and ends with one concrete design question.

Current examples in `r/learnmachinelearning` suggest that a concrete implementation and visible proof work better than a broad product inventory. A focused [C++ neural-network build](https://www.reddit.com/r/learnmachinelearning/comments/1fg48vc/i_built_a_neural_network_from_scratch_in_c_with_a/) attracted substantial discussion, while a broad [framework feature list](https://www.reddit.com/r/learnmachinelearning/comments/1u6le3h/i_built_an_ml_library_from_scratch_in_c_that/) received little attention. The final post therefore shows one working expression, reports its recovered gradients, and asks one answerable architecture question.

The community's [live rules](https://www.reddit.com/r/learnmachinelearning/about/rules.json) allow members to share work and achievements but limit repeated promotion. Reddit's [publisher guidance](https://redditinc.com/hubfs/Reddit%20Inc/Content/%5B2025%5D%20Reddit%20Pros%20playbook%20for%20publishers.pdf) also emphasizes community context and continued participation after publishing.

## Submission checklist

Before submitting:

- Recheck the live `r/learnmachinelearning` rules
- Confirm that we have not posted related material there during the previous seven days
- Choose `Project` flair, or the closest project-oriented flair available
- Use a rich-text post rather than a bare link post
- Upload the computation-graph visual in the body
- Confirm that GitHub appears before YouTube
- Open both links in a private window
- Turn on reply notifications
- Proofread the rendered post on desktop and mobile

After submitting:

- Record the Reddit URL and exact publication time in the distribution timeline
- Answer substantive comments during the first two hours
- Return later that day and for the next 48 hours
- Do not ask friends to vote on the post
- Record views, score, comments, link clicks if available, and the technical themes people discuss after 24 and 72 hours
- Use the discussion to improve the tensor-autograd episode rather than adding another promotional reply

## Communities not used for this post

- **`r/cpp`:** Personal projects belong in its Show and Tell thread, and its current rules prohibit AI-written or AI-polished submissions. Do not submit this copy there.
- **`r/MachineLearning`:** Its current rules prohibit strategic marketing and SEO-oriented posts. This announcement is not appropriate there.
- **`r/deeplearning`:** Hold it for a separately written technical post after tensor autograd or the first training loop. Do not cross-post this body.
