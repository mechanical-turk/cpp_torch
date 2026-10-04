# Episode 10: pre-script keyword and SEO analysis

Prepared September 14, 2026, before drafting `script.md`. Platform: YouTube
long-form. Audience: programmers learning how neural-network operations and
autograd work in C++.

## Scope from Episode 9 and the current code

Episode 9 ends by promising a nonlinear activation and a model that can learn a
curve. The current Tensor supports broadcast arithmetic, matrix multiplication,
reductions, reverse-mode autograd, and a complete linear-regression training
loop. It does not support activation functions.

Episode 10 will add three elementwise activation operations to Tensor:

- ReLU
- sigmoid
- tanh

Each operation will preserve the Tensor shape, record its input node, and add a
backward rule. The final example will replace the existing linear prediction
with `tanh(inputs.matmul(weights) + bias)` and learn values sampled from
`y = tanh(2x + 1)`.

The episode will not introduce a module base class, multilayer perceptron,
MNIST, softmax, cross-entropy loss, or general neural-network parameter
management. Those belong to later episodes.

## YouTube search language

Sources checked September 14, 2026:

- [Activation Functions in Deep Learning: Sigmoid, Tanh and ReLU](https://www.youtube.com/watch?v=7LcUkgzx3AY)
  uses `activation functions`, `deep learning`, `sigmoid`, `tanh`, and `ReLU`
  directly in the title. The video is broad and much longer than our intended
  implementation-focused episode.
- [Activation Functions in Neural Networks: Sigmoid, ReLU, tanh, softmax](https://www.youtube.com/watch?v=9vB5nzrL4hY)
  uses the same three function names and `neural networks` in the title.
- [PyTorch ReLU documentation](https://docs.pytorch.org/docs/stable/generated/torch.nn.ReLU)
  defines ReLU as the elementwise function `max(0, x)` and confirms that it
  preserves the input shape.
- [PyTorch Sigmoid documentation](https://docs.pytorch.org/docs/stable/generated/torch.nn.modules.activation.Sigmoid.html)
  defines sigmoid as the elementwise function `1 / (1 + exp(-x))` and confirms
  that it preserves the input shape.
- [PyTorch nonlinear activation documentation](https://docs.pytorch.org/docs/stable/nn.functional)
  groups ReLU, sigmoid, and tanh under `non-linear activation functions` and
  gives the tanh formula.
- Owned long-form evidence:
  [Episodes 1-6 retention comparison](../analytics/reports/2026-08-29-long-form-retention-comparison-episodes-01-06.md)
  supports a cold opening, useful code inside 30 seconds, and an observable
  result near the first minute. It does not establish keyword demand.

Searches for C++-specific activation-function videos did not return a useful
current comparable result. This supports including C++ prominently for audience
qualification, but it does not prove a ranking opportunity. Search volume,
competition, autocomplete, and owned query-level demand remain unavailable.

## Selected language

Primary phrase: **ReLU, sigmoid and tanh in C++**.

Supporting terms:

- activation functions
- nonlinear activation
- neural networks
- autograd
- backpropagation
- local derivative
- gradient
- elementwise operation
- nonlinear regression

Working title:

`Building ReLU, Sigmoid and Tanh in C++ | Deep Learning, All the Way Down #10`

Rejected or deferred:

- `activation functions explained`: too broad for an implementation episode.
- `neural network from scratch`: Episode 10 does not build a multilayer network.
- `MLP in C++`: module composition belongs to the next episode.
- `MNIST in C++`: no image data or classifier appears here.
- `softmax`: it is not elementwise and needs separate treatment with the
  classification loss.
- `vanishing gradients`: sigmoid and tanh can motivate the idea, but a full
  analysis would interrupt the implementation and overstate this episode's
  scope.
- `from scratch` as a claim about transcendental math: the Tensor operations
  and backward rules are ours, while sigmoid and tanh use the C++ standard
  library's exponential and hyperbolic tangent functions.

No hashtags are selected at scripting time. Publishing metadata requires its
own platform-specific audit.

## Spoken-keyword map

| Term | Planned spoken use | Why it belongs there |
| --- | --- | --- |
| linear layer, nonlinear activation | Opening: stacked linear layers collapse into one equivalent linear layer, so the model needs a nonlinear operation between them | Establish the need without a theory detour |
| ReLU | First implementation: preserve positive values and replace the rest with zero | Name the first concrete operation as its code appears |
| activation function, elementwise operation | Shared forward helper: transform every value while preserving shape | Connect standard terminology to the Tensor implementation |
| autograd, backward rule | ReLU backward: multiply the incoming gradient by the local derivative | State the actual capability being added |
| sigmoid | Second implementation: map each real input between zero and one | Explain its observable behavior beside the formula |
| tanh | Third implementation: map inputs between negative one and one | Explain the function beside `std::tanh` |
| local derivative, gradient | Backward cases: ReLU uses the input; sigmoid and tanh reuse their computed outputs | Preserve the causal reason for the lambda arguments |
| nonlinear regression | Final example: apply tanh to the affine prediction and fit an S-shaped target | Deliver the promised curve without claiming a multilayer network |
| neural-network modules, multilayer perceptron | Ending only: these operations will become composable modules next | Set up the next capability after completing this lesson |

The script should use these terms once where they help. It should not repeat the
three activation names as a keyword roll call or pause the cold opening to
define every term.
