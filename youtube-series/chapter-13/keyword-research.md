# Chapter 13 keyword research

Prepared September 30, 2026, before drafting. Revised the same day when the
creator reordered the episode: build a Sequence and layer classes first, stack
them, train a deeper network, then introduce momentum as the fix. The subject
changed, so the selection below replaces the earlier momentum-and-residuals one.

## Scope from the actual starting point

The recorded Chapter 12 main.cpp trains an MLP (784 inputs, 32 hidden units,
10 digit scores) on MNIST with plain gradient descent and reports 88.2% test
accuracy on a 2,000-image subset. It already has Tensor-level autograd,
Linear, Tanh, MLP, softmax, cross-entropy and a parameter-list update.

This episode adds, in order: an abstract `Layer` base class that `Linear` and
`Tanh` inherit from (`Tanh` gains an empty `parameters()`); a `Sequence`
container that owns its layers through `unique_ptr` and is filled with
`push_back`; the existing network rebuilt as a `Sequence` (which must
reproduce the old numbers exactly); an eight-hidden-layer network, written out
layer by layer, that trains badly; and momentum in a second `gradient_step`
overload, which helps but does not fully fix it. Keep residual connections,
normalization, Adam, dropout, weight initialization schemes and attention out of
this episode. Residual connections appear only in the closing next-episode
list.

## Sources and observed language

- [PyTorch C++ containers](https://docs.pytorch.org/cppdocs/api/nn/containers.html)
  and [torch.nn.Sequential](https://docs.pytorch.org/docs/2.12/generated/torch.nn.Sequential.html):
  a Sequential is a container that chains modules, passing each module's output
  to the next, and collects modules in the order given. Confirms "Sequence" and
  "layers" as standard vocabulary for what we build. PyTorch's C++ frontend also
  uses a base Module class. We do not copy its registration or shared-ownership
  machinery.
- [Cornell Computational Optimization Open Textbook: Momentum](https://optimization.cbe.cornell.edu/index.php?title=Momentum):
  momentum as a decaying accumulation of past gradients; the accumulated term
  is called velocity.
- [Machine Learning Mastery: Gradient Descent With Momentum From Scratch](https://machinelearningmastery.com/gradient-descent-with-momentum-from-scratch/):
  "from scratch" paired with momentum, and the same update rule we implement.
- [DeepAI: Vanishing Gradient Problem](https://deepai.org/machine-learning-glossary-and-terms/vanishing-gradient-problem)
  and [GeeksforGeeks: Vanishing and Exploding Gradients](https://www.geeksforgeeks.org/deep-learning/vanishing-and-exploding-gradients-problems-in-deep-learning/):
  the term, and the usual account that gradients shrink as they are multiplied
  through many layers, so early layers learn very slowly. Caution: these
  sources usually attribute it to activation slopes. Our own measurement
  (see script-review.md) shows the shrinkage at our starting weights without
  attributing it to tanh, and the narration says only what was measured.
- Searches for a hand-written C++ tutorial that builds a layer container,
  trains a deeper network and adds momentum found Python and framework
  material and no comparable video. This supports novelty only, not demand.

No search volume, YouTube autocomplete, owned query demand or ranking
difficulty was available. Do not label this an SEO opportunity score.

## Selection

Primary phrase: deeper neural network and momentum in C++.

Supporting: neural network in C++, MNIST, Sequence, layers, momentum,
velocity, vanishing gradient, gradient descent.

Working title: Deeper Neural Networks and Momentum in C++ | Deep Learning, All the Way Down #13

Reject for this episode: residual connections and skip connections (closing
list only), batch and layer normalization, Adam, dropout, ResNet, He or Xavier
initialization, type erasure (considered and set aside for this episode in
favor of a plain base class), PyTorch replacement or framework claims.

## Spoken-keyword map

| Term | Where it is spoken |
| --- | --- |
| C++ neural network, MNIST, deeper, momentum | Cold open: the first two sentences name the network, the dataset, the goal and the fix. |
| layers, base class, forward, parameters, override | Section A, as the base class and its two layers are written. |
| Layer, Sequence | Section A, where each is named and built; Section B, where the network is stacked. |
| pointer, unique_ptr, make_unique | Section A, where the list of pointers is explained; Section B, where layers are created. |
| deeper network | Section C, where hidden layers are added. |
| vanishing gradient | Section D, right after the measured explanation of why the deep network is stuck. |
| momentum, velocity, gradient descent | Section D, before and while the update is written. |
| residual connections | Closing next-episode list only. |

## Evidence-led scope

[Long-form retention comparison](../analytics/reports/2026-08-29-long-form-retention-comparison-episodes-01-06.md)
shows repeated opening losses and movement toward concrete implementation.
The episode therefore names the network, the dataset and the plan in the first
two sentences and reaches code within about 30 seconds. Each abstraction is
introduced when the next edit needs it: the Layer base class only once a network
built from a list of layers is the goal, and momentum only after a measured run shows what it
would fix. The 10-15 minute target is an editorial constraint from the
long-form playbook, not a measured optimum.
