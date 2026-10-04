# Reddit MNIST milestone post

Prepared September 19, 2026. Draft only. Nothing has been submitted or
scheduled.

## Decision

- Subreddit: `r/learnmachinelearning`
- Format: rich-text post with `Project` flair
- Recommended time today: 12:30 PM ET
- Availability: stay active in the thread through at least 2:30 PM ET, then
  return later today and tomorrow
- Links: GitHub first, YouTube playlist second
- Hashtags: none
- Visual: include technical evidence, not an episode thumbnail

The previous post is now 20 days old, so another project update complies with
the subreddit's current once-per-week limit. The 12:30 PM time is an operating
choice that preserves two hours for replies, not a claim about a universally
optimal Reddit posting time.

## Final post

### Title

```text
I trained an MNIST classifier with the C++ autograd engine I built from scratch
```

### Body

```text
About three weeks ago, I shared the point where my C++ tensor library and scalar autograd engine were still separate. The main question was how to connect them.

I ended up giving each Tensor a shared graph node that stores its values, gradients, operation and parents. Since then, the project has gone from calculating scalar gradients to training a neural network on MNIST.

The training step now looks like this:

const Tensor logits = model.forward(inputs);
const Tensor probabilities = softmax(logits);
Tensor loss = cross_entropy_loss(probabilities, batch.labels);
loss.backward();
gradient_step(parameters, 0.1);

Everything underneath those calls is part of the C++ implementation built during the project.

The parts that mattered most were:

- recording whole Tensor operations in the computation graph;
- accumulating broadcast gradients back into reused values;
- implementing backward rules for matrix multiplication, reductions and nonlinear activations;
- collecting parameters from reusable Linear and Tanh modules;
- building softmax and cross-entropy from Tensor operations such as exp, log, division and column sums.

I first used the training loop to recover y = 2x + 1, then trained a small multilayer perceptron on XOR. The MNIST model has 784 inputs, 32 hidden units with tanh, and 10 outputs.

I trained it for five epochs on 10,000 images using mini-batches of 64, then evaluated it on 2,000 separate test images:

Epoch 1 loss: 0.994
Epoch 2 loss: 0.427
Epoch 3 loss: 0.340
Epoch 4 loss: 0.299
Epoch 5 loss: 0.272
Test accuracy: 88.2% (1764/2000)

The implementation is educational and deliberately small. It is not trying to compete with PyTorch. Building the graph, backward rules, training loop, softmax and cross-entropy directly made the path from pixels to parameter updates much easier for me to understand.

Code and episode checkpoints:
https://github.com/mechanical-turk/deep-learning-all-the-way-down

I am also documenting the build as a video series:
https://www.youtube.com/playlist?list=PLZSg76FHvdTw

I am cleaning up the single-file implementation before adding more layers. If you have built something similar, which abstraction would you get right first: operation objects, module and parameter discovery, or optimizers?
```

## Visual

The first post received a direct comment that its computation-graph visual made
the gradient flow easier to understand. Keep a technical visual in this post.

Final asset:
[reddit-mnist-autograd-training-result-v7.png](../chapter-12/assets/reddit-mnist-autograd-training-result-v7.png)

Recommended composition:

- left: one recognizable MNIST digit and `784 inputs`;
- center: `Linear(784, 32) -> Tanh -> Linear(32, 10)`;
- right: the five measured epoch losses and `88.2% test accuracy`;
- small footer: `10,000 training images | 2,000 test images`.

Use the exact measured values from the verified Chapter 12 run. Do not use a
YouTube thumbnail or imply evaluation against the complete 10,000-image MNIST
test set.

Suggested caption:

```text
The model, training-loss progression and held-out result from the current C++ implementation.
```

Suggested alt text:

```text
A handwritten MNIST digit passes through a 784-input, 32-hidden-unit, 10-output neural network. Training loss falls from 0.994 to 0.272 over five epochs, and the model reaches 88.2 percent accuracy on 2,000 test images.
```

## Why this follows the first post

The first submission stopped at scalar reverse-mode autograd and asked whether
Tensor handles should point to separate shared graph nodes. This post begins
with the implemented answer and shows its payoff. It does not recap every
episode or advertise one new upload.

The code sample makes the final training path inspectable. The measured loss
and accuracy prove that the system trains a model, while the stated data sizes
prevent the result from sounding broader than it is.

## Reddit and keyword research

Research date: September 19, 2026.

Current subreddit rules verified in the authenticated Reddit interface:

1. Be respectful.
2. Share the same content at most once per week.
3. Do not post content involving monetary transactions or pure marketing.

The account's submitted-post page shows no project post after the August 30
submission. That post currently shows 27,000 views, 121 upvotes and seven
comments. One commenter specifically praised the computation-graph visual.

Current subreddit search results for `MNIST C++` include titles built around
`neural network from scratch`, `C++`, `MNIST classifier` and `training MNIST`.
Comparable broad framework announcements have generally received limited
discussion. The selected title therefore names one concrete result rather than
describing the project as a general framework.

Primary phrase: `MNIST classifier with a C++ autograd engine`.

Supporting terms used naturally:

- C++ tensor library
- neural network on MNIST
- autograd
- backpropagation
- multilayer perceptron
- softmax
- cross-entropy
- mini-batch training
- test accuracy

Hashtags retained: none. Hashtags, generic AI terms, CUDA and convolution are
not part of the current result and should not be added for discovery.

## Technical verification

Verified against Chapters 8 through 12, the Chapter 12 replay report and the
public repository checkpoint.

- Tensor operations use shared graph nodes and reverse topological traversal.
- Broadcasting gradients accumulate through saved effective strides.
- Sum and matrix multiplication have backward rules.
- ReLU, sigmoid and tanh have forward and backward implementations.
- The reusable MLP collects parameters from two Linear layers.
- Softmax uses exp, column sums and broadcast division.
- Cross-entropy uses one-hot targets, log, multiplication, sum and division.
- The MNIST model is `784 -> 32 -> 10` with a tanh hidden activation.
- Training uses 10,000 images, batches of 64 and five epochs.
- The measured evaluation result is 1,764 correct predictions from a separate
  2,000-image test subset, or 88.2%.

The current repository is educational and CPU-only. Do not describe it as a
production framework, a PyTorch replacement, or a state-of-the-art MNIST
model.

## Submission checklist

Before submitting:

- confirm the title and body render correctly in Reddit's rich-text editor;
- choose `Project` flair;
- add the technical visual after the measured-results paragraph;
- confirm GitHub appears before YouTube;
- open both links in a private window;
- turn on reply notifications;
- make sure the next two hours are available for discussion;
- capture the pre-post audience and traffic snapshot.

After submitting:

- record the direct Reddit URL and exact ET publication time;
- run the automatic post-publication checks;
- answer substantive comments during the first two hours;
- revisit the thread later today and over the next week;
- capture 24-hour, 48-hour, 72-hour and seven-day checkpoints;
- record views, score, comments, repository traffic, YouTube referrals and
  audience movement without claiming unsupported attribution.

## Critique

The title is more outcome-focused than the unposted tensor-autograd follow-up.
It carries the strongest search terms without reading like a keyword list. The
body preserves the successful structure of the first post: a concrete build,
inspectable code, measured output, owned links near the end and one technical
question.

The main risk is breadth. Six development stages occurred between scalar
autograd and MNIST. The post controls this by centering the working training
step and measured classifier result, then using one short list to establish how
the implementation reached them.

The technical visual contains the verified architecture, training sizes, epoch
losses and test result. Copy and visual are ready for creator review. The post
itself has not been submitted.
