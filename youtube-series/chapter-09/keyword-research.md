# Episode 9: pre-script keyword and SEO analysis

Prepared September 10, 2026, before drafting script.md. Platform: YouTube
long-form. Audience: programmers learning deep learning implementation in C++.

## Scope from the recorded promise and code

Episode 8's ending promises sum and matrix-multiplication backward, gradient
tests, and a linear regression loop that learns from data. Checkpoint
`7021cfe0eb1704a31e9f429c9684d5ff66af78bd` already has tensor storage, broadcast
arithmetic, MSE forward, graph traversal and arithmetic backward rules. It lacks
sum and matmul backward. Reuse that code instead of rebuilding a tensor or
autograd engine. The September 13 draft uses one batched model throughout:
`inputs.matmul(weights) + bias`. It writes the full training loop first, then
implements the two backward rules required to make that loop run. There is no
row-wise model, scalar-weight vector, differentiable indexing detour, or second
forward API. The final example fits ten synthetic points to `y = 2x + 1`.
Target 7-9 minutes.

## Sources and observed language

- [PyTorch Tutorial 05: Gradient Descent with Autograd and Backpropagation](https://www.youtube.com/watch?v=E-I2DNVzQLg):
  current indexed title explicitly combines gradient descent, autograd and
  backpropagation; its description names linear regression from scratch.
- [Linear Regression Gradient Descent From Scratch in Python](https://www.youtube.com/watch?v=pCCUnoes1Po):
  current indexed title groups linear regression, gradient descent and from
  scratch. Language is Python, so it supports subject wording, not C++ demand.
- [Dive into Deep Learning: Linear Regression](https://classic.d2l.ai/chapter_linear-networks/linear-regression.html):
  establishes linear regression, squared loss, parameters and gradient descent
  as the standard terms. This episode uses full-batch gradient descent. Do not
  claim that it demonstrates stochastic or mini-batch training.
- [PyTorch automatic differentiation tutorial](https://docs.pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html):
  uses a linear prediction, weights, bias, a loss and autograd. Useful terminology
  reference; this episode does not use PyTorch or claim to reproduce its full API.
- [PyTorch autograd-engine overview](https://pytorch.org/blog/overview-of-pytorch-autograd-engine/):
  explains operation graphs and local backward computations without materializing
  a whole Jacobian. Reference only; no Jacobian lecture is needed in this episode.
- Owned evidence: [Episodes 1-6 long-form retention report](../analytics/reports/2026-08-29-long-form-retention-comparison-episodes-01-06.md)
  supports immediate implementation and early payoff. It does not establish
  search demand. Episode 8's [captions](../chapter-08/captions/automatic-en.srt),
  [script ending](../chapter-08/script.md) and public source establish continuity.

YouTube-domain and broader primary-source searches ran September 10. No new
analytics pull, paid keyword tool or live autocomplete measurement was performed.
Owned query-level search demand, search volume, competition and rank opportunity
are unavailable. These are relevant established phrases, not proven best keywords.

## Selection

Primary phrase: **linear regression from scratch in C++**.

Supporting terms: gradient descent, autograd, backpropagation, mean squared
error (MSE), matrix multiplication, gradients, weights and bias, learning rate,
broadcasting and full-batch gradient descent.

Working title: `Training Linear Regression from Scratch in C++ | Deep Learning, All the Way Down #9`.

Rejected or deferred: PyTorch tutorial (we do not use it), neural-network
training (the model is linear regression), CUDA/GPU acceleration, stochastic
or mini-batch training (the episode uses one full batch), optimizers from scratch (no
optimizer abstraction), automatic differentiation from scratch as the primary
promise (much of it already exists), production-ready tensor library and
performance benchmarking (not demonstrated).

No hashtags are selected at scripting time. Upload metadata gets its own audit.

## Spoken-keyword map before drafting

September 13 revision: retain the cited subject research and primary phrase.
Use ten points following `y = 2x + 1` so the implementation stays focused on
autograd, matrix multiplication and gradient descent. No fresh search or demand
measurement is claimed for this editorial change.

| Concept | Intended spoken use | Timing purpose |
| --- | --- | --- |
| Linear regression, C++, autograd | Opening: train linear regression in C++ using our own autograd | Establish the deliverable before implementation; no keyword inventory |
| Backpropagation | Connect mean squared error back to the weight and bias | Give the missing rules an immediate purpose |
| Full-batch gradient descent | Clear gradients, calculate every prediction, build one loss, call backward and update once per step | Show the final training structure before implementing its missing backward rules |
| Mean squared error / MSE | Build one loss from all ten squared errors | Motivate the short sum backward rule |
| Matrix multiplication | Define the model as the whole input matrix times one weight column | Keep the real model representation from the opening through the final run |
| Gradient accumulation | Explain += while showing contributions to reused matrix entries | Preserve the chain-rule reasoning beside the code |
| Backward correctness | Train a complete batch after implementing sum and matmul backward; keep finite-difference checks in the verification suite | Prove the integrated path on screen without turning the episode into a numerical-gradient detour |
| Weights and bias | Start both at zero and recover two and one | Make the result immediately readable |
| Gradient descent, learning rate | Explain subtracting a scaled gradient as the update loop is written | First parameter update |
| Broadcasting | Explain why the one bias receives all row contributions | Inspect bias gradient, not a standalone recap |
| Loss / training loop | Rebuild the batch graph after every parameter update | Keep forward values and backward history aligned with the current weights |

Keep the primary phrase in the opening as natural speech. Do not force the
entire phrase into every section or recap. The final script audit must cite
where these words occur in the actual spoken blocks.

## September 13 compact batch revision

Retain the researched subject and search-language selection. The creator
removed the row-wise teaching path before drafting the replacement script.
Start with one `linear_forward()` that accepts an input matrix, a weight matrix
and a scalar bias. Write the full-batch training lifecycle before adding sum and
matmul backward so each derivative rule supports code already on screen. The
final example uses ten observations, one feature and one output. This is an
editorial and implementation-order revision, not new evidence about keyword
demand.
