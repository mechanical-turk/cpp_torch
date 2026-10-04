# Chapter 13 publishing package

## Checklist plan

October 3, 2026. YouTube long-form private preparation and public GitHub code
checkpoint only. No public release, schedule or social announcements authorized.

| Check | Plan |
| --- | --- |
| P01 | Use the final export and recorded main.cpp, not the obsolete momentum draft. |
| P02 | Recheck YouTube search language and learning-rate terminology; disclose unavailable query data. |
| P03 | Lead with deeper neural networks in C++; include MNIST and learning rate decay naturally. |
| P04 | Include broad C++/machine learning tags and specific implemented concepts; no visible hashtags. |
| P05 | Plain active English, no hype, em dashes or canned contrasts. |
| P06 | One separator and the exact series/episode suffix. |
| P07 | Use the verified series playlist and public code repository; record the returned upload URL. |
| P08 | Prepare a useful training-experiment comment, but do not post while private. |
| P09 | Upload a descriptive hard link to the exact final export. |
| P10 | Locate an approved thumbnail; do not invent approval or reuse another episode's image. |
| P11 | Probe resolution and duration, sample final frames, record hash and review limits. |
| P12 | Explicit private visibility, no publishAt, English, Education, not made for kids; add series playlist. |
| P13 | Wait for actual captions to derive chapters, never use script estimates. |
| P14 | Defer all social distribution and public scheduling until creator approval. |
| P15 | Test and push recorded source plus activation plots; update README without unrelated WIP changes. |
| P16 | Validate parser fields and inspect the upload dry run. |
| P17 | Score actual evidence, leaving public-release checks pending. |
| P18 | Record direct URLs and remaining public-release work in the timeline. |

## Upload artifact and state

Filename: `cpp-deeper-neural-network-sequence-learning-rate-decay.mp4`

Source: `/Users/keremkazan/Movies/CapCut/ep13/out.mp4`

Upload: `/Users/keremkazan/Movies/CapCut/ep13/cpp-deeper-neural-network-sequence-learning-rate-decay.mp4`

The descriptive name is a hard link, preserving the original export.
3840x2160, 30 fps, H.264 video, AAC mono at 48 kHz.
Duration: 31:20.344. Size: 5,209,074,542 bytes.
This exceeds our 10-15 minute editorial target; no edit was requested.

SHA-256: `fa59bfa7dd996a0a391bd71faab4b3b9b098d74de13bed7b3f18eea52f5dea6a`.
Replacement requested October 3 after the creator rejected the previous edit.
Sampled replacement frames at 00:30 and 30:00 show the MLP and final ReLU
Sequence. The final model shown matches the previously committed model.
This is a sampled visual review, not a full audio or native-playback review.

Replacement uploaded: https://www.youtube.com/watch?v=yonurmbDkbM

Studio: https://studio.youtube.com/video/yonurmbDkbM/edit

API read-back confirms private visibility, no schedule, exact title and
description, and all 21 tags. Added the replacement to the complete-series
playlist. YouTube processing remains in progress.

Superseded upload: https://www.youtube.com/watch?v=ASoqjGVOUKc
Do not distribute that URL. No deletion was performed by the agent.
No thumbnail was found in
the chapter directory or final-export directory. Chapters, 2160p playback,
end screens, comment settings and full audio review remain pending.

## Research and scope

Platform: YouTube. Research date: October 3, 2026.

The September 30 keyword file describes momentum, which the final script no
longer implements. Do not use its momentum title or numerical results here.
Recorded source instead has Layer, Sequence, Tanh and ReLU layers, MNIST,
and multiplicative learning rate decay. The final source trains ten epochs
with an initial rate of 0.5 and decay factor 0.9. Avoid accuracy claims until
the recorded result and code run are reconciled. The final-code verification
run reached 91.95% (1839/2000), with final training loss 0.120646. No numerical
accuracy claim is included in the upload copy.

GitHub source checkpoint:
https://github.com/mechanical-turk/deep-learning-all-the-way-down/commit/dc29a21f43e32992f81958d94d3a506eb5d1ca36

README and main branch verified at:
https://github.com/mechanical-turk/deep-learning-all-the-way-down/commit/2c8078579fa26b62cc17e3554953ebf1a80d53fb

Both entry points compiled and ran successfully. Source and activation plots
were pushed from a separate worktree, preserving the recording checkout and
its unrelated local WIP commit. README also links the now-public Chapter 12.

Sources checked:

- Owned-channel API: Chapter 12 is public and uses "Training a Neural Network
  on MNIST in C++". No Chapter 13 duplicate exists in the latest uploads.
- [YouTube educational example](https://www.youtube.com/watch?v=N-qNAJbP74Y)
  uses "Neural Network" and "Learning Rate" together. This is language evidence,
  not proof of search volume or likely performance.
- [PyTorch StepLR documentation](https://docs.pytorch.org/docs/stable/generated/torch.optim.lr_scheduler.StepLR.html)
  confirms the terminology for multiplying the learning rate after epochs.

Candidates: deeper neural networks in C++, neural network layers in C++,
MNIST in C++, learning rate decay. Primary: deeper neural networks in C++.
Supporting: learning rate decay, MNIST, gradient descent, ReLU, tanh, C++23,
sequential layers. No current owned search-query report or autocomplete data
was pulled, and no keyword demand or ranking claim is made.

Backend tags cover the language, broader audience, implemented architecture,
dataset, activations and training technique. Reject momentum, residual
connections, CUDA and GoogleTest because this upload does not implement them.
Visible hashtags: none, following the YouTube description convention.

## Final title

```text
Deeper Neural Networks and Learning Rate Decay in C++ | Deep Learning, All the Way Down #13
```

## YouTube description

```text
Build deeper neural networks in C++ and experiment with learning rate decay on MNIST handwritten digits.

In Episode 13 of Deep Learning, All the Way Down, we turn our fixed neural network into a Sequence of layers. A shared Layer interface lets us stack Linear layers with tanh or ReLU and collect their trainable parameters for gradient descent.

We then change the network's depth, compare training behavior, and adjust the learning rate. We add decay to reduce the step size over successive epochs and examine what happens to the loss and test accuracy.

Topics covered:
- A Layer base class with forward and parameters
- A Sequence container that owns layers with std::unique_ptr
- Deeper multilayer perceptrons for MNIST classification
- Tanh and ReLU activation layers
- Gradient descent, learning rate experiments and decay

Complete series:
https://www.youtube.com/playlist?list=PLZSg76FHvdTw

Source code:
https://github.com/mechanical-turk/deep-learning-all-the-way-down
```

## Suggested tags

```text
C++, cpp, C++23, machine learning, deep learning, neural networks, neural network from scratch, neural network in C++, deep learning in C++, MNIST, handwritten digit recognition, multilayer perceptron, MLP, learning rate, learning rate decay, gradient descent, ReLU, tanh, sequential neural network, backpropagation, Deep Learning All the Way Down
```

## First-comment candidate

Prepared, not posted. Check existing author comments before any future posting.

```text
When comparing network depth, keep the training budget in mind. A deeper model may need different learning rates or more epochs before the comparison is useful. Here we experiment with the learning rate instead of assuming more layers will improve accuracy. Which would you test next: initialization, residual connections, or momentum?
```

## Private preparation and release handoff

Use private visibility with no schedule, category Education, English audio
and metadata, and not made for kids. Add to the complete-series playlist.
Do not post comments, X/LinkedIn announcements or Reddit updates in this task.
Social copy, timing and any separate Short require the later public-release
decision. No public announcement should point to a private video.

Before release: supply the approved thumbnail, verify 2160p playback and
code legibility, download serving captions and derive chapters, inspect
comments and Subscribe/playlist end screens. Chapters must start with
Introduction and end with Recap; use actual transitions, not draft timings.
After public release, run the post-publication procedure, update README's
video link, inspect any authorized comment for duplicates, and log URLs.

## Checklist audit

| Check | Status | Points | Evidence / remaining work |
| --- | --- | ---: | --- |
| P01 | PASS | 10/10 | Source plus sampled final frames match the copy; no unsupported numeric claim. |
| P02 | PASS | 15/15 | Dated YouTube research above; unavailable query data disclosed. |
| P03 | PASS | 10/10 | Subject leads title and description; implemented keywords only. |
| P04 | PASS | 8/8 | Language, audience and specific tags justified; no visible hashtags. |
| P05 | PASS | 10/10 | Natural public fields, no banned punctuation or boilerplate. |
| P06 | PASS | 5/5 | Exact series suffix, one separator, title below 100 characters. |
| P07 | PASS | 5/5 | Known playlist and public source links; no social preview in scope. |
| P08 | PASS | 5/5 | Content-specific candidate, explicitly unposted. |
| P09 | PASS | 4/4 | Descriptive hard link created for the actual export. |
| P10 | UNVERIFIED | 0/4 | Approved thumbnail and Studio preview absent. |
| P11 | PARTIAL | 3/6 | Measured 4K master; playback/audio review incomplete. |
| P12 | PARTIAL | 1.5/3 | Replacement private/unscheduled metadata verified and playlist insertion succeeded; processing and Studio checks pending. |
| P13 | UNVERIFIED | 0/4 | Captions and recording-derived chapters pending. |
| P14 | PASS | 3/3 | Private-only scope; all social release work explicitly deferred. |
| P15 | PASS | 2/2 | Both entry points passed; source, plots and README pushed and remote hash verified. |
| P16 | PASS | 2/2 | Parser-compatible fields; private unscheduled dry run inspected, 21 tags. |
| P17 | PASS | 2/2 | Evidence limits and arithmetic explicit. |
| P18 | PASS | 2/2 | Private and eventual public handoffs distinguished. |

## Critique

The old keyword draft describes a different lesson. This package avoids its
momentum and accuracy claims. The final runtime is long; record that risk
without pretending a private upload solves pacing. Thumbnail, captions and
native playback checks remain necessary before public release.

## Final score

Score: 87.5/100 (87.5/100 earned). Decision: hold public release.
The user explicitly authorized private preparation; this score does not
authorize scheduling or publication.
