# Reddit Launch Plan

## Primary post: r/cpp August Show and Tell

- **Venue:** [C++ Show and Tell, August 2026](https://www.reddit.com/r/cpp/comments/1vhdqw8/c_show_and_tell_august_2026/)
- **Format:** Comment in the recurring thread, not a standalone submission
- **Timing:** Sunday, August 23 around 10:30 AM ET, or the next time Kerem can
  remain available to answer technical comments for at least two hours
- **Primary link:** GitHub repository
- **Secondary link:** YouTube playlist
- **Goal:** Obtain concrete C++ design feedback and introduce the project
  without treating the subreddit as an announcement feed

### Pre-publication blocker

Update the public repository README before posting. It currently describes the
code as it existed after Episode 2, while the implementation has progressed
through broadcasting, matrix multiplication, and a linear prediction. Reddit
readers should not land on stale documentation.

### Draft comment

I started this because I wanted to understand what PyTorch is doing under the
hood, and I wanted a project substantial enough to push me past
LeetCode-style C++.

I'm building a small deep-learning stack from scratch in C++23. It is still one
`main.cpp` file and uses only the standard library. So far the tensor supports
flat row-major storage, scalar and empty tensors, checked indexing, elementwise
operations, reductions, dot products, rank-two matrix multiplication, and
broadcasting. Next come loss functions, autograd, and an actual training loop.

Repository:
https://github.com/mechanical-turk/deep-learning-all-the-way-down

I'm also recording the implementation as a video series:
https://www.youtube.com/playlist?list=PLZSg76FHvdTw

This is an educational project, not an attempt to ship a production tensor
library. I'd be especially interested in where the current representation or
API is likely to become painful once I add views and automatic differentiation.

## Secondary communities

### r/learnmachinelearning

Wait until the project can train its first model. At that point, write a
standalone, result-led post explaining what was learned from implementing the
forward pass, autograd, and optimization. Do not cross-post the r/cpp text.

### r/MachineLearning

Use only the current self-promotion thread unless a later result qualifies as a
substantive technical discussion. The current thread explicitly accepts
personal projects, blogs, and tutorials, but requires pricing or payment terms
to be disclosed and prohibits shortened or auto-subscribe links. When used,
state that the repository and series are free and open source.

Wait until autograd or the first trained model provides a stronger technical
milestone. The current tensor implementation is less differentiated for this
audience than it is for r/cpp.

### Hacker News

Wait for a concrete milestone such as the first trained neural network, a
measured matrix-multiplication result, or a working autograd engine. Submit the
technical artifact or write-up, not a generic series announcement.

### Communities to avoid for this post

- r/cpp as a standalone submission, because personal projects are currently
  being removed and redirected to Show and Tell.
- r/cpp_questions, because this is not a focused C++ question.
- broad programming and side-project communities, because they offer weaker
  audience fit than the current r/cpp thread.

## Participation rules

- Post to one community first rather than copying the same text everywhere.
- Disclose that it is Kerem's project.
- Lead with the implementation and learning problem, not subscriber growth or
  the episode schedule.
- Ask for specific feedback rather than generic engagement.
- Reply substantively to every serious technical response.
- Do not ask for upvotes or coordinate voting.
- Record the final timestamp and direct comment URL in the distribution ledger.
