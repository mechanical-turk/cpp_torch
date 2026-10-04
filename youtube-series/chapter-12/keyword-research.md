# Chapter 12 keyword research

Prepared September 14, 2026, before script drafting.

## Scope and source

Start from the actual recorded Chapter 11 main.cpp, including its Linear,
Tanh, MLP, parameter lists, generalized gradient_step and tensor autograd.
The ending promises MNIST, mini-batches, classification loss and accuracy.
Build a 784-32-10 MLP, mean softmax cross-entropy with backward, an original IDX
binary batch reader, training and held-out digit accuracy. No CNN, GPU, image drawing
app, generic data-loader framework or optimizer class.

## Evidence

- [Author's C++ MNIST recipe](https://www.ea.com/seed/amp/news/machine-learning-game-devs-part-3): C++ and recognizing handwritten digits, with training/test sets. Its result is not our result.
- [MNIST C++ video](https://www.youtube.com/watch?v=oCElhUzadaA): title uses MNIST, neural network and C++; its CNN is outside our scope. Search-index observation, not demand measurement.
- [PyTorch CrossEntropyLoss](https://docs.pytorch.org/docs/2.11/generated/torch.nn.CrossEntropyLoss.html): unnormalized logits, class-index targets, mean reduction and log-softmax/NLL formulation.
- [Torchvision MNIST source](https://docs.pytorch.org/vision/stable/_modules/torchvision/datasets/mnist.html): source archive URLs/checksums and separate train/test data. Used to verify dataset provenance, not as an implementation dependency.

Original dataset page did not load. No current autocomplete, query volume,
owned topic-specific search queries or ranking estimates available.

## Selection and spoken map

Primary: MNIST digit recognition in C++.
Supporting: neural network from scratch, handwritten digits, mini-batch,
logits, softmax, cross-entropy, backpropagation, test accuracy.

| Term | Natural recording use |
| --- | --- |
| handwritten digit / MNIST / C++ | Anchor the opening in a real image and the recognition task. |
| mini-batch | Reader returns a small group of images, one row per image. |
| logits | Ten raw output scores, one per digit, before explaining the loss. |
| softmax / cross-entropy | Turn relative scores into probabilities and penalize a low probability for the correct digit. |
| backpropagation | Feed the loss gradient into our existing network graph. |
| test accuracy | Count predictions on images excluded from weight updates. |

Reject: CUDA, CNN, PyTorch replacement, production framework, guaranteed
accuracy, training on all 60,000 images when the lesson uses a subset.

## Evidence-led structure

The long-form-only [retention comparison](../analytics/reports/2026-08-29-long-form-retention-comparison-episodes-01-06.md)
supports early concrete work and no series preamble. Introduce the image row
and network dimensions immediately. Preserve the entire learning path on
screen for the ML implementation. The supplied reader gets a maximum 30-second
contract overview; original binary-format parsing is outside this lesson.
Do not import Shorts controversy, deliberate omissions or a compulsory question.

## September 15 model-comparison context

The separate experiments use validation accuracy, validation cross-entropy,
generalization gap, hidden-layer width/depth and learning rate. These terms
describe research outside the current lesson; do not add a tuning lecture to
the narration or claim the 32-unit Tanh baseline is best-known.

[TensorFlow's beginner MNIST example](https://www.tensorflow.org/tutorials/quickstart/beginner)
uses a 128-unit ReLU layer with dropout and Adam. Its different data budget and
training recipe prevent treating it as a controlled comparison to our baseline.
[Keras training guidance](https://keras.io/guides/training_with_built_in_methods/)
supports separate validation data for model development. Neither establishes
the best architecture for our custom Tensor implementation.

## Three-setup comparison handoff

The requested closing comparison now brings hidden-layer width/depth, ReLU,
Tanh and validation accuracy into the narration. Use the already measured
shuffled 32-unit Tanh, shuffled 128-unit ReLU and shuffled 128/64-unit ReLU
runs at epoch 15, seed 42. This holds the data order policy and budget fixed.
Say "in this comparison", not "each larger model is always better". Keep the
five-epoch lesson's test score separate from the comparison's validation scores.

## Opening revision: main.cpp first

Keep MNIST, handwritten digits and C++ neural network in the opening promise.
The creator's latest direction replaces the image-led opening and 30-second
reader overview with main.cpp and a roughly ten-second helper acknowledgment.
Download/setup instructions live only in preparation documentation. Explain
784 inputs at the first image-to-network call, not in a parser preface.

## Final loss-section direction

Use exp, sum_columns and log as reusable operations. Introduce softmax through
the concrete need for positive scores that sum to one; show exp results first,
then complete probabilities, then use log to compose cross-entropy externally.
Explain one-hot targets at the selection step. The current script has no
native cross-entropy operation, label metadata or derivative cache. Stability
refinements are deferred beyond the first pass. Earlier alternative proposals
remain historical in script-review.md, not instructions for this version.
