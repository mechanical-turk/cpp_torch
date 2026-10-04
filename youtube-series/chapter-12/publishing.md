# Episode 12 Publishing Package

## Checklist plan

Prepared September 15, 2026. YouTube long-form, with X and LinkedIn announcements.
Stage: publishing-copy preparation, not upload or public-release approval.
Follow the [publishing checklist](../production/publishing-playbook.md).

| ID | How this package will satisfy the check |
| --- | --- |
| P01 | Match the shortened script and recorded main.cpp: MNIST classification, Tensor primitives, training and test accuracy. Exclude architecture comparisons and ReLU instruction. |
| P02 | Research YouTube, X and LinkedIn vocabulary separately; distinguish indexed examples from measured search demand. |
| P03 | Put MNIST, C++, neural networks, softmax and cross-entropy in relevant public fields. |
| P04 | Use accurate broad and specific YouTube tags. Keep visible hashtags out of this package. |
| P05 | Follow previous announcements: clear technical substance, connected sentences, no canned contrasts or em dashes. |
| P06 | Include the series and episode number, with one title separator. Check platform lengths. |
| P07 | Keep only the episode's YouTube URL in main announcements. Put source and playlist links in replies. |
| P08 | Propose a useful numerical-stability first comment, not Q&A or GitHub promotion. Do not auto-post the candidate. |
| P09 | Use the script's descriptive MP4 filename; verify the actual export before upload. |
| P10 | Require an Episode 12 thumbnail and a real preview check. |
| P11 | Inspect the final export for 4K resolution, runtime, audio and readable code. |
| P12 | Check comments, playlist membership, processing and end-screen navigation. |
| P13 | Derive chapters from the uploaded video's captions, not script estimates. |
| P14 | Respect episode order and the existing long-form cadence; announce only after publication. |
| P15 | Publish the matching code checkpoint and README update when authorized. |
| P16 | Keep parser headings intact and separate public copy from internal notes. |
| P17 | Audit the actual evidence and score remaining gaps honestly. |
| P18 | Reconcile live URLs, metadata, comments, source and timeline after publication. |

## Publishing content

- Upload filename: `cpp-mnist-handwritten-digit-recognition-neural-network.mp4`
- Filename status: descriptive hard link created September 24 for the actual
  export `aliases/04-final-cuts/ep12/0915 (1).mp4`; original retained.
- Source of truth: [shortened script](script.md) and `aliases/02-screen-long-form/main.cpp`, inspected September 15.
- Recorded scope: existing 784-32-10 MLP; original MNIST data through the supplied reader; exp, log and column sums with backward rules; softmax; cross-entropy built from Tensor operations; mini-batch training; test-set accuracy.
- Current code uses 10,000 training images, batches of 64, five epochs and 2,000 separate test images. Do not describe this as training on the full MNIST dataset.
- Exclusions: model comparisons, new ReLU implementation, CNNs, CUDA, fused cross-entropy, dataset-loader walkthrough and any unconfirmed accuracy percentage.
- The script's recap still contains “Comparing network setups.” This package follows the user's edited scope and does not repeat that leftover bullet.
- Final master verified September 24: 3840x2160 at 30 fps, H.264 with stereo AAC
  at 44.1 kHz, 25:13.244, 4,872,617,330 bytes. This exceeds the 10–15-minute
  target. Sampled opening, MNIST input, backward code and recorded 88.2%
  (1764/2000) result. Full audiovisual review and custom thumbnail remain pending.
- Episode URL: https://www.youtube.com/watch?v=12MUX0SD4lc
- Studio: https://studio.youtube.com/video/12MUX0SD4lc/edit
- September 24 upload complete. API read-back verifies private visibility,
  no publication date, title, description, all 22 tags, English, Education,
  not made for kids and complete-series playlist membership. Processing is
  still underway. English automatic captions are not serving yet.
- Playlist verified via API September 24: `PLZSg76FHvdTw`, complete series.
- Public source: Episode 12 checkpoint c9918e8 is already pushed; README has the
  Episode 12 summary. Add its video URL only after public release.
- Current directive: upload private, without a schedule. [distribution.md](distribution.md)
  holds the upload identity, remaining checks and conditional distribution plan.

## Platform research records

Research date: September 15, 2026. These are vocabulary observations, not search-volume estimates or evidence that a phrase causes reach. No paid tweet-history pull was performed.

### YouTube

Sources: [episode keyword research](keyword-research.md), [author's C++ MNIST implementation video](https://www.youtube.com/watch?v=oCElhUzadaA), and [neural-network loss lesson](https://www.youtube.com/watch?v=dEXPMQXoiLc).

Observed vocabulary: MNIST, C++, handwritten digit recognition, softmax and cross-entropy. The first example implements a convolutional network; that architecture does not describe our episode and is excluded.

Primary phrase: **MNIST neural network in C++**. Supporting phrases: handwritten digit recognition, neural network from scratch, automatic differentiation, softmax, cross-entropy loss, mini-batch gradient descent. Title and opening description cover the primary subject; later paragraphs and backend tags cover implementation details.

No visible hashtags under our YouTube convention. Backend tags include both standalone language/field terms and specific recorded topics. Reject CNN, CUDA, PyTorch tutorial, ReLU comparison and accuracy-based tags. Owned topic-query data, current autocomplete and search volume are unavailable; do not claim proven demand.

### X

Indexed search found a [C/MNIST discussion](https://x.com/oprydai/status/2008443905940009081) using from-scratch ML and MNIST classification language. It concerns C, not C++, and provides only limited adjacent vocabulary evidence. Native post inspection and a strong topic-matched C++ sample remain unavailable.

Provisional primary: **C++ neural network**. Supporting terms: MNIST, softmax, cross-entropy and Tensor operations. Use our Chapter 11 announcement format for voice, not the search result's tone. No hashtags: the short announcement already names its technical subjects. Owned search/conversion evidence and composer preview remain unavailable; research is PARTIAL.

### LinkedIn

Sources: [C++ network author's post](https://www.linkedin.com/posts/gaurang-gupta-0b70062a1_cppdeveloper-fromscratchai-machinelearning-activity-7433492333918330881-kCnI) and [from-scratch neural-network project announcement](https://www.linkedin.com/posts/anmoldeepsingh04_github-anmoldeepsingh04scratchnn-a-neural-activity-7500787201497231360-mj6U).

Observed vocabulary: C++, neural network from scratch, MNIST, softmax and cross-entropy. These author posts supply relevant terminology, not implementation evidence for our code or a writing template.

Primary: **C++ neural network**. Supporting: handwritten digit recognition, MNIST, backpropagation and mini-batch training. Keep these in readable prose. No hashtags retained: incremental benefit has not been established, and the relevant subjects are already explicit. Reject broad AI/career tags and architecture tags absent from this episode. Owned topic-query data, search volume and a live composer preview remain unavailable.

## Final title

```text
Training a Neural Network on MNIST in C++ | Deep Learning, All the Way Down #12
```

## YouTube description

```text
Train a neural network on MNIST in C++ using the Tensor library and automatic differentiation engine we've built from scratch.

In Episode 12 of Deep Learning, All the Way Down, our network learns to recognize handwritten digits. Each image produces ten scores, one for each digit. We turn those scores into probabilities with softmax, then build cross-entropy loss so we can train the model to assign a higher probability to the correct answer.

We add exp, log and column sums to our Tensor library, including their backward rules. Softmax and cross-entropy then use those operations with our existing autograd engine.

The training loop uses mini-batch gradient descent on 10,000 MNIST images. After training, we measure classification accuracy on 2,000 separate test images the model hasn't trained on.

Covered in this episode:
• MNIST images as C++ Tensors
• Raw class scores and softmax probabilities
• Exp, log and column sums with backpropagation
• One-hot targets and cross-entropy loss
• Mini-batch neural network training
• Handwritten digit recognition and test accuracy

Complete series:
https://www.youtube.com/playlist?list=PLZSg76FHvdTw

Series source code:
https://github.com/mechanical-turk/deep-learning-all-the-way-down
```

Verify the inherited playlist destination and public Episode 12 source checkpoint before release. Add real chapters after caption inspection; there are no estimated timestamps to paste here.

## Suggested tags

```text
C++, cpp, machine learning, deep learning, neural networks, MNIST, handwritten digit recognition, digit classification, neural network from scratch, neural network in C++, C++ machine learning, softmax, cross entropy loss, categorical cross entropy, one hot encoding, mini batch gradient descent, backpropagation, autograd, automatic differentiation, tensor operations, MLP, deep learning from scratch
```

Broad tags identify the language and field. Specific tags describe the actual dataset, loss, operations and training method. Tags supplement the title and description; they are not a promise of search performance.

## YouTube first-comment candidate

Status: proposed, not approved or posted. No automatic Q&A comment or pin reminder.

```text
We use exp(score) directly here so we can follow how softmax works. Very large scores can make that overflow. Subtracting the largest score from every score in the same row keeps the probabilities unchanged and prevents that overflow.

There's also a reason implementations often calculate log-softmax directly: a tiny probability can round to zero before we take its log. Those are useful improvements once the basic calculation is clear.
```

This extends the recorded implementation without claiming either improvement is already implemented. Inspect for an existing equivalent comment before posting an approved version, and report its direct URL afterward. No GitHub link.

## Other selected platform copy

### X announcement

```text
Our C++ neural network can now recognize handwritten digits.

In Episode 12 of Deep Learning, All the Way Down, we build softmax and cross-entropy from Tensor operations, train on MNIST, and test the model on images it hasn't seen.

https://www.youtube.com/watch?v=12MUX0SD4lc
```

### X navigation reply

```text
Code:
https://github.com/mechanical-turk/deep-learning-all-the-way-down

Series playlist:
https://www.youtube.com/playlist?list=PLZSg76FHvdTw
```

### LinkedIn announcement

```text
Our C++ neural network can now recognize handwritten digits from MNIST.

In Episode 12 of Deep Learning, All the Way Down, we turn the network's ten output scores into probabilities with softmax and build cross-entropy loss from our own Tensor operations.

We add exp, log and column sums with their backward rules, then use the autograd engine to train on 10,000 images in mini-batches. After training, we test the model on 2,000 separate images to see how often it picks the correct digit.

https://www.youtube.com/watch?v=12MUX0SD4lc
```

### LinkedIn navigation comment

```text
The C++ code for the series:
https://github.com/mechanical-turk/deep-learning-all-the-way-down

The full YouTube playlist:
https://www.youtube.com/playlist?list=PLZSg76FHvdTw
```

Both main announcements contain only the episode URL. Inspect the YouTube preview before posting; link ordering alone cannot guarantee a card. No separate announcement image is planned, so image alt text is not applicable here.

## Settings and release checks

- YouTube language: English. Category: Education. Audience: not made for kids.
- Comments: On, Anyone; verify moderation settings separately from Newest first sorting. Sorting does not release held comments.
- Add to the complete Deep Learning, All the Way Down playlist; verify the actual playlist ID first.
- Require 3840×2160 export and available 2160p playback before public release. Dimensions, frame rate, codec, audio and readable code need inspection on the actual master.
- Thumbnail: Episode 12 asset and upload preview still required. No thumbnail has been approved in this package.
- End screen: complete-series playlist plus Subscribe on the clean tail after the sign-off, allowing roughly five seconds of padding.
- Captions: retrieve the uploaded video's generated captions, compare with the actual edit and script, then generate chapters. Start with `00:00 Introduction`; finish with `Recap`. Keep labels short and use meaningful topic boundaries, not arbitrary equal intervals.
- Candidate chapter subjects, not timestamps: MNIST inputs; Class scores; Exp; Column sums; Softmax; Log; Cross-entropy; Training; Test accuracy; Recap. Merge or split only after checking the recording. Follow the current chapter-length rules in the publishing playbook.
- Copy readiness: drafts supplied for all three platforms. Links, previews and incomplete X research prevent a complete gate pass.
- Upload/public-release readiness: UNVERIFIED. Missing media, thumbnail, live settings and caption evidence are not approvals.

## Short upload gate

N/A: this is a long-form episode. The long-form final-media and end-screen checks above still apply. No Instagram or TikTok upload, native X video, or Short derivative is planned by this package.

## Distribution and follow-through

September 24 superseding direction: PRIVATE, UNSCHEDULED. No announcement or
comment is authorized now. The older timing defaults below are conditional
release guidance only; use [distribution.md](distribution.md) for current status.

- Consulted the current distribution timeline and posting cadence. The latest recorded checks do not establish that Episodes 10 and 11 are public. Confirm order before scheduling Episode 12.
- YouTube: next suitable Monday, Wednesday or Saturday at 11:00 AM ET, after Episode 11 is live and release checks pass. This is a planning default, not a claim about an optimal algorithmic window.
- X: announce around noon ET on publication day, after confirming playback and the watch URL. Add the navigation reply after duplicate inspection.
- LinkedIn: next eligible weekday at 9:00–10:30 AM ET, at least 24 hours after the X announcement. A noon Wednesday X post would make Friday morning eligible, not Thursday morning.
- Reddit: defer to a separately researched, community-specific milestone post. Do not automatically repeat the YouTube announcement on forums.
- Public GitHub: checkpoint the actual Episode 12 code and update the top episode table and detailed README summary, including the real watch URL and current MNIST setup. Verify reader/data instructions. Do not imply the raw dataset is bundled. Commit/push only when authorized.
- After upload: retrieve the real URL, replace both announcement placeholders, inspect metadata/tag persistence, thumbnail, processing, audience, comments and playlist. Derive and apply chapters from captions when available and authorized.
- After publication: run the post-publication checks, inspect duplicates before any approved comment/reply, report direct URLs for every external action, and append verified publication events to the distribution timeline.
- User action pending: supply/confirm final export and thumbnail, approve first-comment candidate, and choose release timing after episode-order confirmation. No upload, schedule, post or source push was performed while preparing this document.

## Checklist audit

Scope: complete draft package for YouTube, X and LinkedIn, September 15, 2026. Each check takes the lowest applicable platform credit. Plans do not count as completed live checks.

| ID | Status | Points | Evidence or remaining gap |
| --- | --- | ---: | --- |
| P01 | PARTIAL | 5/10 | Copy matches shortened script and current code; final edited media uninspected. |
| P02 | PARTIAL | 7.5/15 | Separate records supplied; X has only limited adjacent indexed evidence. |
| P03 | PASS | 10/10 | Accurate primary and supporting terms appear in public fields. No unsupported architecture or accuracy claim. |
| P04 | PASS | 8/8 | Relevant broad/specific backend tags; deliberate no-hashtag choice on each platform. |
| P05 | PASS | 10/10 | Public fields reviewed for connected prose, banned wording, forced informality and em dashes. |
| P06 | PASS | 5/5 | Series and episode identity present; title and X lengths fit. |
| P07 | PARTIAL | 2.5/5 | Real private watch URL and playlist verified; social composer previews await public release. |
| P08 | PASS | 5/5 | Substantive proposed comment and navigation replies supplied, with approval, duplicate checks and direct-link reporting. |
| P09 | PASS | 4/4 | Descriptive hard link, exact master size and SHA-256 recorded in distribution.md. |
| P10 | UNVERIFIED | 0/4 | Episode 12 thumbnail and preview absent. |
| P11 | PARTIAL | 3/6 | Master metadata and sampled frames checked September 24; full audiovisual/playback review pending. |
| P12 | PARTIAL | 1.5/3 | Private unscheduled upload, metadata, audience and playlist verified. Processing, end screen and comments UI pending. |
| P13 | UNVERIFIED | 0/4 | Caption-derived timestamps unavailable; no invented chapters. |
| P14 | PASS | 3/3 | Conditional sequence respects episode order and the 24-hour announcement gap. |
| P15 | PASS | 2/2 | Public c9918e8 and README summary verified; watch link deferred while private. |
| P16 | PASS | 2/2 | Parser-safe fields, real watch URL and title/description/tag lengths verified. Do not announce while private. |
| P17 | PASS | 2/2 | All 18 checks scored with evidence and blockers. |
| P18 | PASS | 2/2 | Concrete verification and recordkeeping handoff supplied; no publication inferred. |

## Critique

The title names the real payoff and dataset. The announcements follow the earlier series format while explaining what we build, rather than listing vague benefits. The description distinguishes training from testing and avoids borrowing results from the removed comparisons.

The release package cannot pass its final gate without the actual export, thumbnail, verified destinations and caption-derived chapters. X vocabulary evidence is weaker than the YouTube and LinkedIn evidence. These are explicit gaps, not reasons to inflate the score or invent results.

## Final score

**72.5/100: 72.5 earned points / 100 applicable points × 100.**

This is a draft-package compliance score, not a prediction of views or search ranking. Public-release approval remains on hold until the outstanding checks pass.

Private upload completed under the creator's explicit instruction. This does
not clear public release: thumbnail, native settings, processing/playback and
caption-derived chapters remain pending. Distribution is not scheduled. See
distribution.md for the Studio access blocker and notification-checkbox check.
