# Episode 11 Publishing Package

## Checklist plan

Prepared September 14, 2026. YouTube long-form with X and LinkedIn announcements.
Stage: copy preparation, not upload approval.

| ID | Release-specific approach |
| --- | --- |
| P01 | Match recorded main.cpp: Linear/Tanh, parameter collection, 2-4-1 MLP and XOR. Inspect final media when available. |
| P02 | Record separate platform evidence and unavailable X research. |
| P03 | Lead with C++ neural networks, supported by MLP, XOR and autograd. |
| P04 | Include relevant broad and specific backend tags; no visible hashtags. |
| P05 | Connected technical sentences, no canned contrasts or em dashes. |
| P06 | One title pipe, series name and #11; identity in both announcements. |
| P07 | YouTube-only main announcement URL; other links in replies. Verify destinations. |
| P08 | Useful generalization comment, not Q&A or GitHub promotion. |
| P09 | Descriptive filename; verify actual export. |
| P10 | Dedicated Chapter 11 thumbnail and real preview check pending. |
| P11 | Inspect final 4K media, audio, captions, duration and code. |
| P12 | Verify comments, playlist, end screen and 2160p processing. |
| P13 | Caption-derived chapters, not estimated script timings. |
| P14 | Release after Chapter 10; conditional cadence, separate Shorts and forum decisions. |
| P15 | Checkpoint actual code and minimal README update when authorized. |
| P16 | Parser-safe headings and separate public fields. |
| P17 | Score evidence, not intentions. |
| P18 | On publication, reconcile URLs, metadata, captions, source and timeline. |

## Publishing content

- Upload filename: `cpp-neural-network-modules-mlp-xor-from-scratch.mp4`
- Export: `aliases/04-final-cuts/ep11/0915.mp4`, 3840x2160, 22:04.025, 4,313,097,171 bytes. A hard link with the descriptive upload filename preserves the original file without duplicating media storage.
- Episode URL: https://www.youtube.com/watch?v=Jiqc8jW1skM (private upload initiated September 20, 2026; not scheduled or published).
- Studio: https://studio.youtube.com/video/Jiqc8jW1skM/edit
- Thumbnail: no dedicated Chapter 11 asset found; creator final adjustment pending.
- September 20 setup: title, description, 22 tags, series playlist, English, Newest comments and playlist/Subscribe end screen saved in Chrome. Private selected; Save clicked. Last observed upload progress: 89%. Completion verification timed out, so upload/processing completion remains unverified. End-screen timing is currently 21:44-22:04; review during final adjustments. Captions and chapters remain pending.
- Source: current `aliases/02-screen-long-form/main.cpp`, public HEAD 1535f54 plus local Chapter 11 edits. Chapter 11 is not yet committed/pushed.
- Actual code differs from the script: Linear::parameters is const, random_weights omits the draft's guards, and the generalized gradient_step also serves older regression examples. Copy does not claim those guards or a second update overload.
- Demonstration: four XOR pairs, Linear(2,4), Tanh, Linear(4,1), MSE, 5,000 steps, learning rate 0.1, seed 42. These are all training examples, not a held-out test.
- Final video/runtime unverified. No MNIST, classification-loss or GPU implementation claimed.

## Platform research records

September 14, 2026. Vocabulary observations do not establish demand or conversion.

### YouTube

Sources: [episode keyword record](keyword-research.md), [author's C++ network](https://github.com/oktonion/neural-network-from-scratch-in-cpp), and previously inspected [XOR video](https://www.youtube.com/watch?v=A9EmBsgsMlI). Today's repeat video fetch failed; the earlier observation remains recorded.

Observed terms: neural network from scratch, C++, XOR, MLP. Primary: neural network in C++. Supporting: Linear, Tanh, hidden layer, autograd and gradient descent. Candidates rejected: MNIST classifier, CUDA training, PyTorch tutorial. No visible hashtags under our YouTube convention. Backend tags are separate. Owned evidence: series format and long-form retention report; topic-specific queries, live autocomplete and preview unavailable.

### X

Checked indexed C++/XOR searches and the previously used [tensor developer post](https://x.com/BLUECOW009/status/1834829023232274847). No usable new X result; direct post returned no text. Prior Chapter 9/10 announcements support voice continuity, not demand.

Provisional primary: C++ neural network. Candidates/supporting: neural network from scratch, XOR, MLP, autograd. No hashtags, with subjects in prose. No tweet analytics requested. Fresh native wording evidence and composer preview remain unavailable, so P02 is PARTIAL.

### LinkedIn

Sources: [author's C++ network/XOR post](https://www.linkedin.com/posts/chamela-aththanayaka_cplusplus-machinelearning-neuralnetworks-activity-7450893797204328449-08zG) and [XOR/backpropagation post](https://www.linkedin.com/posts/anshul-khaire-77732922a_machinelearning-neuralnetworks-cplusplus-activity-7414689793173057536-s-hC).

Observed terms: C++, neural network from scratch, XOR, backpropagation, gradient descent. Primary: neural network in C++. Candidates/supporting: reusable layers, multilayer perceptron, hidden layer, autograd. No hashtags; no incremental hashtag benefit established. Owned search/conversion evidence, volume and preview unavailable. These posts supply vocabulary, not technical authority or a style template.

## Final title

```text
Building Our First Neural Network in C++ | Deep Learning, All the Way Down #11
```

## YouTube description

```text
We build and train a neural network from scratch in C++, using our Tensor and autograd engine to learn XOR.

In Episode 11 of Deep Learning, All the Way Down, we turn linear layers and tanh into reusable modules, connect them into a multilayer perceptron, and train the network with gradient descent.

The model takes two inputs, passes them through four hidden units, and produces one prediction. We collect the weights and biases from both layers so the training loop can reset their gradients and update every parameter. Our existing autograd engine handles backpropagation through the network.

We train on all four XOR cases and compare the predictions with their targets. The example uses mean squared error and a linear output; it demonstrates a working MLP and training loop, not performance on unseen data.

Covered in this episode:
• Reusable Linear and Tanh modules in C++
• Weight initialization
• Hidden layers and multilayer perceptrons
• Collecting model parameters
• Gradient resets and gradient descent
• Training a neural network to learn XOR

Complete series:
https://www.youtube.com/playlist?list=PLZSg76FHvdTw

Source code:
https://github.com/mechanical-turk/deep-learning-all-the-way-down
```

Inherited playlist URL needs live verification. GitHub currently contains Chapter 10;
publish the actual Chapter 11 checkpoint before announcing its code as available.

## Suggested tags

```text
C++, cpp, C plus plus, machine learning, deep learning, neural networks, neural network from scratch, neural network in C++, C++ machine learning, multilayer perceptron, MLP, XOR neural network, linear layer, hidden layer, tanh, autograd, automatic differentiation, backpropagation, gradient descent, weight initialization, tensor library, deep learning from scratch
```

Broad tags identify the language/field; specific terms describe the actual model
and implementation. No MNIST, CUDA, CNN or classification-loss tags.

Mechanical lengths: title 78 characters, tags 366 characters, X announcement
242 characters with the future URL counted as 23. The current recording source
also compiled and ran during Chapter 12 baseline verification, including its
four correct XOR predictions. This does not substitute for final-media review.

## YouTube first-comment candidate

Proposed, not posted or selected for automatic application.

```text
XOR has only four possible inputs, and we train on all four. Getting every answer right tells us the network can fit this pattern, but it doesn't test how well it handles unseen examples.

For a larger dataset, we'd keep separate test examples out of the training loop. The loss can keep improving on the training data while test accuracy stops improving.
```

No GitHub link or automatic pin task. Inspect author comments before authorized
posting and report its direct URL afterward.

## X announcement

Draft: replace URL and inspect preview.

```text
Our C++ neural network can now learn XOR.

In Episode 11 of Deep Learning, All the Way Down, we build reusable layers, connect them into an MLP, and train both layers' weights and biases using our own autograd engine.

[EPISODE_11_URL]
```

### X navigation reply

```text
Complete series:
https://www.youtube.com/playlist?list=PLZSg76FHvdTw

Source code:
https://github.com/mechanical-turk/deep-learning-all-the-way-down
```

## LinkedIn announcement

```text
Our C++ neural network can now learn XOR with a hidden layer and backpropagation through the Tensor operations we built from scratch.

In Episode 11 of Deep Learning, All the Way Down, we turn linear layers and tanh into reusable modules, then connect them into a multilayer perceptron.

The training loop collects the weights and biases from both layers, clears their gradients, and updates them with gradient descent. We finish by training on all four XOR cases and checking each prediction against its target.

[EPISODE_11_URL]
```

### LinkedIn first author comment

```text
Source code:
https://github.com/mechanical-turk/deep-learning-all-the-way-down

Complete series:
https://www.youtube.com/playlist?list=PLZSg76FHvdTw
```

## Settings and release checks

- Private while processing; eventual audience not made for kids, English, Science & Technology.
- Verify final 3840x2160 master, sound, code legibility and 2160p playback.
- Comments On/Anyone; Newest-first sorting. Moderation is a separate check.
- Complete-series playlist; Subscribe and playlist end-screen elements on the clean tail.
- Thumbnail selection, dimensions, small-screen legibility and Studio preview pending.
- Captions/chapters pending: start 00:00 Introduction, finish Recap. Derive real transitions from captions; inspect sections over five minutes. Candidate subjects include Linear, initialization, Tanh, MLP, parameters, gradient updates and XOR training. No invented timestamps.
- Vertical Short gate does not apply; long-form media review does.
- Copy drafted. Upload/public release remain unapproved.

## Distribution and follow-through

Timeline read through September 14's Chapter 10 source push. It does not confirm
Chapter 10/11 video publication. Proposed only: Saturday September 19, 11 AM ET,
if Chapter 10 has released and this episode is ready. Otherwise the next ready
standing slot. Nothing scheduled.

- X: release day around noon ET, then navigation reply once code is public.
- LinkedIn: Monday September 21, 9-10:30 AM ET if that Saturday plan holds, exceeding the minimum 24-hour gap.
- Reddit: defer standalone episode announcement. Revisit the first-network milestone with fresh community/rules research; no forum copy or post authorized here.
- Shorts: separate hardware/performance track, no automatic crop or new commitment.
- Source: checkpoint actual main.cpp and minimally update README row/summary when authorized. Preserve unrelated edits.
- On publication: run post-publication checks, replace URL, derive chapters, reconcile metadata/source and append confirmed timeline events.
- Prepared copy does not authorize posting. Inspect duplicates before authorized comments/replies; report direct URLs afterward.

## Checklist audit

| ID | Status/evidence | Points | Remaining action |
| --- | --- | ---: | --- |
| P01 | PARTIAL: actual code inspected; final video absent. | 5/10 | Final-media comparison. |
| P02 | PARTIAL: YouTube/LinkedIn evidence; X evidence unavailable. | 7.5/15 | Fresh X-native evidence. |
| P03 | PASS: accurate terms in all fields. | 10/10 | Preserve scope. |
| P04 | PASS: broad/specific tags, reasoned no hashtags. | 8/8 | Verify saved tags. |
| P05 | PASS at text review: connected technical prose. | 10/10 | Check final recording. |
| P06 | PASS: title/series/episode identity correct. | 5/5 | Live read-back. |
| P07 | PARTIAL: order correct; URL/destinations/previews pending. | 2.5/5 | Verify links. |
| P08 | PASS for preparation: useful candidate and navigation replies. | 5/5 | Await posting authority. |
| P09 | UNVERIFIED: proposed filename only. | 0/4 | Inspect export. |
| P10 | UNVERIFIED: no thumbnail. | 0/4 | Select and inspect. |
| P11 | UNVERIFIED: final media absent. | 0/6 | Review exact export. |
| P12 | PARTIAL: settings specified, not inspected. | 1.5/3 | Studio/playback checks. |
| P13 | UNVERIFIED: captions absent. | 0/4 | Derive chapters. |
| P14 | PASS for conditional plan and deferrals. | 3/3 | Confirm readiness/dates. |
| P15 | PASS: recorded code e4dffe6 and README a1ea701 pushed September 15; remote verified. | 2/2 | Preserve checkpoint. |
| P16 | PARTIAL: parser-safe, URL unresolved. | 1/2 | Replace placeholder. |
| P17 | PASS: all checks/evidence limits scored. | 2/2 | Re-audit changes. |
| P18 | PASS for concrete post-publication handoff. | 2/2 | Execute on reported publication. |

## Critique

The package describes the actual first MLP, not future MNIST work. The comment
explains the all-training-data limitation without restoring Q&A. X research,
final media, thumbnail, URL and chapters remain incomplete. Public source and
the minimal README update are now complete.
Wording evidence is not a forecast of reach.

## Final score

Earned 64.5 / applicable 100 = 64.5/100. No exclusions. YouTube, X and LinkedIn
pre-upload preparation. Copy drafted; release requires the missing evidence.

Score: 64.5/100. Decision: hold for upload/public release.

## September 22, 2026: public status and chapters verified

Verified public URL: https://www.youtube.com/watch?v=Jiqc8jW1skM

API confirms public, processed, duration 22:05, published September 21 at
15:30:07 UTC (11:30:07 AM ET). Downloaded English automatic captions and
aligned them against the actual recording and script. Added the 16 timestamps
in [chapters.txt](chapters.txt), preserving the existing description and other
metadata. Fetched the description again and verified an exact chapter match.
See [boundary review](chapters-review.md).
This supersedes earlier upload-completion/public-status and chapter uncertainty.
Native playback, end-screen rendering and other release checks were not
revalidated during this timestamp-only task.
