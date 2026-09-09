# Reddit Technical-Post Research

Research date: August 29, 2026

## Scope

This review focuses on project and learning posts in `r/learnmachinelearning`,
with `r/cpp` and `r/MachineLearning` used to check community fit. Memes, news,
career arguments, and general controversy were excluded even when they earned
more votes. They do not resemble the material we plan to publish.

Reddit scores are approximate and can change. These examples show patterns,
not controlled causal evidence.

## Community rules

The current `r/learnmachinelearning` rules explicitly allow members to share
their work and achievements. The same content may appear at most once per week.
The community prohibits paid-course marketing, referral links, and other
transactional promotion.

Source: [r/learnmachinelearning rules](https://www.reddit.com/r/learnmachinelearning/about/rules.json)

Reddit's own guidance recommends first-person writing, relevant context,
continued replies after publication, and language that sounds like an
individual rather than a press release. Promotional content is not inherently
spam, although each community sets its own limits.

Sources:

- [Reddit Pro playbook for publishers](https://redditinc.com/hubfs/Reddit%20Inc/Content/%5B2025%5D%20Reddit%20Pros%20playbook%20for%20publishers.pdf)
- [Reddit Help: keeping spam out of a community](https://support.reddithelp.com/hc/en-us/articles/28012014962580-How-do-I-keep-spam-out-of-my-community)

## Closest examples

### Narrow achievement with concrete evidence

The post [I implemented a Convolutional Neural Network from scratch entirely in
x86 Assembly](https://www.reddit.com/r/learnmachinelearning/comments/1pzmmb3/i_implemented_a_convolutional_neural_network_cnn/)
earned roughly 1,800 votes and 180 comments. Its title names the exact result,
language, and constraint. The body gives dataset scale, implemented operations,
SIMD details, a measured comparison, debugging experience, a GitHub link, and a
specific request for performance feedback. It also includes technical images.

Useful pattern:

1. State the achievement immediately.
2. Prove that meaningful work exists.
3. Include concrete scale or implementation details.
4. Ask for feedback connected to the implementation.

### Personal context attached to a real result

The post [I'm 15 and built a neural network from scratch in C++](https://www.reddit.com/r/learnmachinelearning/comments/1k47qt2/im_15_and_built_a_neural_network_from_scratch_in/)
earned roughly 1,800 votes and generated extensive discussion. Its personal
context made the achievement unusually surprising. The comments concentrated
on learning resources, mathematics, C++, CUDA, and possible next steps.

The transferable lesson is to explain the genuine reason for the project. We
must not imitate personal details or manufacture a dramatic story.

### A question that opened a technical discussion

The post [I'm writing a from-scratch neural network guide. What concepts do
learners struggle with most?](https://www.reddit.com/r/learnmachinelearning/comments/1qow8t6/im_writing_a_fromscratch_neural_network_guide_no/)
earned fewer votes, but its comments contain detailed discussion of autograd,
backpropagation, computation graphs, gradient flow, initialization, and the
relationship between mathematics and code. The question was easy to answer
from personal experience and closely matched the community's learning focus.

Useful pattern: ask one question that gives readers a clear way to contribute.

### Broad promotional inventory

The post [Built a High-Performance ML Framework from Scratch](https://www.reddit.com/r/learnmachinelearning/comments/1r8bt7w/built_a_highperformance_ml_framework_from_scratch/)
received only a few votes despite listing many algorithms and broad qualities.
It reads like a product overview and gives the reader little reason to discuss
one specific engineering decision.

Useful warning: more features, headings, adjectives, and claims do not create
more interest. A broad inventory can make substantial work feel generic.

### Simple implementation with an immediately legible result

The post [Coded Simple Linear Regression from Scratch](https://www.reddit.com/r/learnmachinelearning/comments/1vhud7u/coded_simple_linear_regression_from_scratch_no/)
earned more than 200 votes. The subject was basic, but the result was easy to
understand and the presentation made it immediately clear what had been built.
Several comments asked about learning resources and the next implementation.

Useful pattern: accessibility can outperform sophistication when readers can
understand the accomplishment in seconds.

## Working principles

For the first `r/learnmachinelearning` post:

- Center the scalar reverse-mode autograd milestone.
- Put `C++`, `autograd`, `reverse-mode automatic differentiation`, and
  `PyTorch` in natural, accurate language.
- Open with the reason someone would care about `loss.backward()`.
- Explain graph construction, reverse topological traversal, and gradient
  accumulation briefly.
- Insert the computation-graph visual rather than a YouTube thumbnail.
- Mention the broader tensor project only after explaining autograd.
- Put GitHub first and the video playlist second.
- Ask what tends to break when scalar autograd expands to tensor operations.
- Remain available to answer comments for at least two hours and continue
  checking for 24 to 48 hours.
- Never ask for votes, coordinate engagement, or reuse the same body in another
  subreddit.

## Proposed visual

Use:

`youtube-series/chapter-07/assets/autograd-full-model-opening-v4.png`

It shows the forward computation, the backward path, and the two parameter
gradients without resembling an advertisement.
