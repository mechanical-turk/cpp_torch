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
the chapter directory or final-export directory. 2160p playback,
end screens, comment settings and full audio review remain pending.

October 4 update: downloaded the replacement's English automatic captions to
`captions.en.srt`, derived 20 chapters in `chapters.txt`, and verified the exact
chapter block in the live description. The video is now public according to
API read-back. This operation updated only the description, not visibility.
Automatic captions still contain recognition errors such as MNIST rendered
as "Amnest" and tanh as "10H"; chapter labels use correct terminology.

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

Chapters:
00:00 Introduction
00:25 Define the Layer interface
02:12 Virtual destructors
03:18 Adapt Linear and Tanh
04:24 Build the Sequence container
06:49 Forward pass and ownership
08:09 Collect layer parameters
08:50 Rebuild the MNIST model
10:09 Add a hidden layer
11:06 Add a ReLU layer
12:12 Tanh and ReLU gradients
14:19 Train a deeper network
16:03 Train for more epochs
17:10 Depth versus parameter count
19:16 Vanishing gradients
21:23 Increase the learning rate
22:58 Learning rate overshoot
24:04 Add learning rate decay
25:47 Review loss and accuracy
28:29 Recap
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

## X announcement

Drafted October 7; saved October 13, 2026. Publication status is unverified.
This section preserves the copy supplied in chat; it does not record a post.

```text
Adding more layers made our C++ neural network worse at recognizing digits.

In Episode 13 of Deep Learning, All the Way Down, we build reusable layers, experiment with deeper networks on MNIST, and add learning rate decay.

https://www.youtube.com/watch?v=yonurmbDkbM
```

## LinkedIn announcement

```text
Adding more layers made our C++ neural network worse at recognizing handwritten digits from MNIST, so we started testing what was holding it back.

In Episode 13 of Deep Learning, All the Way Down, we build a shared Layer interface and a Sequence container so we can change the network’s depth and activation functions without rewriting the training loop.

We compare tanh with ReLU, try wider and deeper networks, and give the deeper model more epochs. Then we experiment with the learning rate: larger steps help it learn, but pushing too far sends the loss back up.

We finish by adding learning rate decay and reach 91.95% accuracy on our 2,000-image test subset.

https://www.youtube.com/watch?v=yonurmbDkbM
```

## X navigation reply / LinkedIn comment

Keep these links in the reply/comment, not the main announcement, so the
main post has only the YouTube URL. Inspect the preview before posting and
check for an existing author reply/comment before adding one.

```text
Source code:
https://github.com/mechanical-turk/deep-learning-all-the-way-down

Complete series:
https://www.youtube.com/playlist?list=PLZSg76FHvdTw
```

### Announcement research notes

October 7 research, recorded October 13. Primary wording on both platforms:
C++ neural network. Supporting terms: MNIST, deeper networks, learning rate
decay; LinkedIn additionally names ReLU, tanh and training loss. These refer
to the recorded lesson and existing code, not the superseded script results.

- X: compared the Chapter 12 announcement's technical opening and series-name
  structure. The platform-specific web search returned no useful X matches;
  no fresh owned tweet metrics or search-demand evidence was collected.
- LinkedIn: compared Chapter 11/12 announcement drafts and inspected indexed
  examples using neural network and learning rate decay, including
  [this learning-rate post](https://www.linkedin.com/posts/meruagoodluck_techjourney-90daysgrowthchallenge-consistency-activity-7458264924004335617-7Lv2).
  This supports terminology only, not ranking or performance predictions.
- No hashtags selected for either platform: keep the technical terms in
  readable prose, matching the earlier announcement drafts. No hashtag
  effectiveness claim is made.
- Live composer previews and actual posting status remain unverified.

## Private preparation and release handoff

Use private visibility with no schedule, category Education, English audio
and metadata, and not made for kids. Add to the complete-series playlist.
Do not post comments, X/LinkedIn announcements or Reddit updates in this task.
Social copy, timing and any separate Short require the later public-release
decision. No public announcement should point to a private video.

Before release: supply the approved thumbnail, verify 2160p playback and
code legibility, correct automatic caption terminology, inspect
comments and Subscribe/playlist end screens. Chapters must start with
Introduction and end with Recap; use actual transitions, not draft timings.
After public release, run the post-publication procedure, update README's
video link, inspect any authorized comment for duplicates, and log URLs.

## Checklist audit

The score below retains the earlier YouTube preparation scope. October 13 is
a limited persistence correction: the previously delivered X/LinkedIn drafts
and navigation copy are now saved above. It is not a fresh full-release audit.
For those drafts, P02 remains PARTIAL (limited X research), P07 remains PARTIAL
(composer previews unchecked), and P18 posting status remains unverified.

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
| P13 | PARTIAL | 2/4 | Replacement captions downloaded; 20 recorded chapters verified live. ASR terminology corrections remain. |
| P14 | PASS | 3/3 | Private-only scope; all social release work explicitly deferred. |
| P15 | PASS | 2/2 | Both entry points passed; source, plots and README pushed and remote hash verified. |
| P16 | PASS | 2/2 | Parser-compatible fields; private unscheduled dry run inspected, 21 tags. |
| P17 | PASS | 2/2 | Evidence limits and arithmetic explicit. |
| P18 | PASS | 2/2 | Private and eventual public handoffs distinguished. |

## Critique

The old keyword draft describes a different lesson. This package avoids its
momentum and accuracy claims. The final runtime is long; record that risk
without pretending an upload solves pacing. Thumbnail and native playback
checks remain unverified here; automatic caption terminology needs correction.

## Final score

Score: 89.5/100 (89.5/100 earned). Decision: full release verification incomplete.
The video is now public; the October 4 timestamp update did not change its
visibility. This score does not establish that native playback checks passed.
