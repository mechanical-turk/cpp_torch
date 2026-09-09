# Episode 7 Forum Distribution

## Goal

Share the project as a technical learning milestone, not as a video
announcement. Lead with the work, give readers something concrete to inspect,
and ask a narrow technical question.

## Recommended order

1. Publish the r/learnmachinelearning standalone post.
2. Add the shorter r/cpp comment to the current monthly Show and Tell thread.
3. Optionally add the compact r/MachineLearning comment to its current
   self-promotion thread.
4. Do not submit to Hacker News or Lobsters yet.

Do not paste the same body into several communities. Reply to every substantive
comment and do not ask anyone to upvote the post.

## r/learnmachinelearning

### Timing

Publish Sunday, August 30 between 12:00 and 2:00 PM ET, after the LinkedIn
announcement. Check the current community rules immediately before posting.

### Title

```text
I’m rebuilding deep learning from scratch in C++ and just reached autograd
```

### Body

```text
I started this project to understand what frameworks like PyTorch are doing underneath their abstractions, while getting better at production C++.

The project now has:

- a tensor type with checked multidimensional indexing
- reductions and elementwise operations
- broadcasting
- matrix multiplication
- mean squared error
- a scalar reverse-mode autograd engine

The autograd step was the most interesting part so far. Each Value remembers the operation and inputs that produced it. backward() builds a topological ordering, walks it in reverse, applies the local derivative at each operation, and accumulates gradients when one value reaches the loss through several paths.

This is an educational implementation, not an attempt to replace PyTorch. Next I’m going to connect autograd to tensors and use it to train a small model.

Code:
https://github.com/mechanical-turk/deep-learning-all-the-way-down

I’m documenting each milestone here:
https://www.youtube.com/playlist?list=PLZSg76FHvdTw

I’d especially value feedback on the computation-graph ownership model and what you would implement before attaching autograd to tensors.
```

## r/cpp monthly Show and Tell

### Placement

Post this as a comment in the current monthly Show and Tell thread. The project
is written in C++, but it is not yet a C++ library or tool intended for other
C++ programmers, so a standalone r/cpp submission would not match the current
guidance.

Current thread:
https://www.reddit.com/r/cpp/comments/1vhdqw8/c_show_and_tell_august_2026/

### Comment

```text
I’m rebuilding deep learning from first principles in modern C++ as a learning project.

The implementation has reached scalar reverse-mode automatic differentiation. So far it includes a tensor type, checked indexing, reductions, elementwise operations, broadcasting, matrix multiplication, mean squared error, and a computation graph with reverse topological traversal and gradient accumulation.

The current design uses small Value handles over shared graph nodes. I’d especially appreciate feedback on ownership and API design before I connect autograd to tensors.

Code:
https://github.com/mechanical-turk/deep-learning-all-the-way-down

Step-by-step video series:
https://www.youtube.com/playlist?list=PLZSg76FHvdTw
```

## r/MachineLearning self-promotion thread

### Placement

Use only the current self-promotion thread. Do not create a standalone post for
the series.

Current thread:
https://www.reddit.com/r/MachineLearning/comments/1vd5kqk/d_selfpromotion_thread/

### Comment

```text
I’m building an educational deep learning stack from scratch in C++ and documenting each milestone. It now includes tensors, broadcasting, matrix multiplication, mean squared error, and a scalar reverse-mode autograd engine with topological traversal and gradient accumulation.

Code:
https://github.com/mechanical-turk/deep-learning-all-the-way-down

Series:
https://www.youtube.com/playlist?list=PLZSg76FHvdTw
```

## Deferred communities

### Hacker News

Wait until the project can train a small neural network through a clean,
runnable demo. A future Show HN submission should let readers clone, build, and
run something useful immediately. Hacker News also prohibits generated or
AI-edited submission text, so the learner must personally write the final post.

Rules:
https://news.ycombinator.com/showhn.html
https://news.ycombinator.com/newsguidelines.html

### Lobsters

Do not use Lobsters as a one-off promotion channel. Its self-promotion guidance
expects an established pattern of participating in other discussions. Revisit
only after genuine community participation.

### r/deeplearning

Wait until tensor autograd can train a small model. At that point the project
will have a clearer deep-learning result than the current scalar-autograd
milestone.

## Post-publish record

For every forum post or comment, record:

- publication time;
- direct URL;
- community and placement;
- title used;
- replies that reveal technical confusion or future content ideas;
- a 24-hour and 72-hour checkpoint when metrics are available.
