# Chapter 14 publishing package

Operational state, the upload record and the proposed release sequence live in
[distribution.md](distribution.md). This file is the only home for public copy
and the checklist audit. Script and keyword record: [script.md](script.md),
[keyword-research.md](keyword-research.md), [script-review.md](script-review.md).

## Checklist plan

October 22, 2026. YouTube long-form upload preparation, plus X and LinkedIn
announcement drafts. No upload, schedule, comment, announcement or push is
authorized by this package. Reddit and Shorts are deferred (see Distribution).

- Format and release: YouTube long-form, Episode 14.
- Selected platforms: YouTube (upload preparation), X and LinkedIn (drafts that
  cannot be final until the YouTube URL exists). Deferred: Reddit, Shorts,
  Instagram, TikTok.
- Stage: draft / upload preparation.
- Source-of-truth artifact: `/Users/keremkazan/Movies/CapCut/ep14/cpp-residual-connections-gradient-debugging.mp4`.

| ID | This release's specific approach | Platforms / applicability | Evidence to inspect or known risk |
| --- | --- | --- | --- |
| P01 | Compare every claim with sampled frames of the final export and the committed code, not with the script. Use only numbers visible in the video. | YouTube, X, LinkedIn | No captions yet, so spoken wording is unverified. The script changed after recording. |
| P02 | Reuse the October 4 keyword file for YouTube, add dated checks today, and record what is unavailable. | YouTube, X, LinkedIn | No owned query data, autocomplete or search volume. X and LinkedIn evidence is terminology only. |
| P03 | Lead the title and first description line with residual connections in C++; place MNIST, vanishing gradients and cross-entropy where the video shows them. | YouTube, X, LinkedIn | Spoken coverage of each term waits for captions. |
| P04 | Backend tags for language, audience, concepts and dataset; no visible hashtags anywhere. | YouTube, X, LinkedIn | No hashtag evidence collected, so none are used. |
| P05 | Plain active English; run a lint for em dashes and banned cadence. | all fields | Audit below. |
| P06 | One separator, exact series suffix, subject first. | YouTube, X, LinkedIn | Title length checked below. |
| P07 | Known playlist and repository links in the description; one YouTube URL per announcement. | YouTube, X, LinkedIn | The watch URL does not exist yet. Composer previews are uninspected. |
| P08 | A first-comment candidate tied to the learning-rate choice shown in the video. Not posted. | YouTube | Check existing author comments before any posting. |
| P09 | Verify the on-disk file and its descriptive name. | YouTube | Done below. |
| P10 | No thumbnail exists. Follow the visual and thumbnail research guidelines; invent nothing. | YouTube | Missing asset. |
| P11 | Probe the file, hash it, measure audio, sample frames across the runtime. | YouTube | Sampled review only, not a full playback review. |
| P12 | Specify private, unscheduled settings and playlist; check the end tail. | YouTube | Nothing applied; end tail defect found below. |
| P13 | Derive chapters from downloaded captions after upload; never from the script. | YouTube | No captions yet. Runtime is 52:24, so chapters matter. |
| P14 | Read the timeline and cadence; propose Eastern Time windows with dependencies and deferrals. | all | Plan only. |
| P15 | Match the recorded code to the demo repository commit and the README. | YouTube | Commit exists locally and is not pushed. |
| P16 | Parser-compatible YouTube fields; mark X and LinkedIn copy as drafts until the URL exists. | all | Chapter block pending. |
| P17 | Score actual evidence only; keep unknowns unknown. | all | Below. |
| P18 | List the post-publication checks and who acts. | all | Below. |

## Publishing content

- Exact upload filename: `cpp-residual-connections-gradient-debugging.mp4`
- Master: `/Users/keremkazan/Movies/CapCut/ep14/cpp-residual-connections-gradient-debugging.mp4`
  (alias `aliases/04-final-cuts/ep14/`). It is the export itself, one link, not a
  renamed hard link. Proposed and on-disk names match.
- Identity: 6,254,404,700 bytes, modified October 21, 2026 19:09.
  SHA-256 `385b1922f1fdd3821eb25ff20fb2b2b2baaf5fb36631c496431fd1ab6cce89fc`.
- Measured October 22: H.264, 3840x2160, 30 fps, yuv420p; one AAC stereo audio
  stream at 48 kHz; duration 3143.967 s (52:23.967). Whole-file audio mean
  volume -20.2 dB, peak -3.9 dB (no clipping). Last 14 seconds: mean -20.0 dB,
  peak -4.4 dB.
- Sampled frames reviewed (1280 px wide) at 0:20, 14:00, 22:00, 30:00, 38:00,
  46:00, 48:00, 49:05, 49:50, 51:00, 52:00, 52:18 and 52:22.5. They show: the Chapter 13
  ReLU network at the start; the sixteen-layer Sequence trace with value counts
  (14:00); the plain network's signal and gradient report, gradient 4.7e-03 at
  the output and 1.2e-05 at layer 7 (22:00); the cross-entropy loss formula as a code
  comment (30:00) and its table, probability 0.1 giving loss 2.30 and 2e-23
  giving 52.27 (38:00); the first residual run ending at `Epoch 10 loss: 2.44455` and
  `Test accuracy: 58.85% (1177/2000)` (46:00); the residual report at 48:00 with
  `Epoch 1 loss: 1.28227`; and the final run `Epoch 20 loss: 0.0116095`,
  `Test accuracy: 92.85% (1857/2000)` (49:05), with `EPOCHS = 20`,
  `INITIAL_LEARNING_RATE = 0.08` and `DECAY_RATE = 0.95` on screen.
- Constants of the first residual run (rate 0.5, 10 epochs, decay 0.9) are not on
  screen in the sampled frames. They come from reproducing its exact printed
  losses and 58.85% from the earlier committed code.
- Script versus recording: the recorded video does not follow the current
  script. The script ends at rate 0.1 and 10 epochs (91.05%); the video ends at
  0.08, 20 epochs and 92.85%. Copy below follows the video. The script's
  verification run does not describe the video.
- Not reviewed: full playback, narration, keyboard audio presence (one mixed
  stereo stream), caption accuracy, YouTube 2160p playback.
- Live URLs: none known. No upload is recorded in the timeline.

## Platform research records

### YouTube research

- Research date: October 22, 2026, plus the October 4 record in
  [keyword-research.md](keyword-research.md).
- Sources checked: the October 4 sources (Aman.ai, AI Summer and DeepAI on
  residual and skip connections; He et al. 2015; Neptune and MathWorks on
  per-layer gradient norms); a general web search for a C++ from-scratch
  residual connections video; a web search for per-layer gradient debugging
  with skip connections.
- Owned-account evidence: none pulled for this episode. The latest long-form
  retention report covers Episodes 1 to 6 only.
- Candidate search phrases: residual connections in C++, debugging gradients,
  vanishing gradient, deeper neural network in C++, neural network in C++, skip
  connections, cross entropy loss.
- Primary phrase: residual connections in C++.
- Supporting terms and where they appear: debugging, gradients and layers in the
  title; vanishing gradients, MNIST and cross-entropy in the first paragraphs and
  topic list; skip connections and cross entropy loss as backend tags only.
- Observations: no C++ from-scratch residual connections video turned up in the
  general search. Written and lecture material uses both "residual connections"
  and "skip connections", and describes per-layer gradient norms as the standard
  diagnostic. This is language and novelty evidence, not demand.
- Hashtags retained: none. Rejected: all, because no evidence of their use was
  collected and descriptions normally carry none.
- Backend tags: language and audience terms; the implemented concepts; the
  dataset; the loss. Rejected: ResNet, ImageNet, batch normalization, layer
  normalization, momentum, Adam and optimizer, none of which the video builds.
- Unavailable: YouTube autocomplete, search volume, owned search-term data.

### X research

- Date: October 23, 2026. Sources: a web search restricted to x.com and
  twitter.com, which returned no relevant posts; the Chapter 13 announcement
  structure; the YouTube search language above; the episode captions.
- Primary phrase: C++ neural network. Supporting: vanishing gradient, residual
  connections, cross-entropy loss, learning rate, MNIST, tanh. Each is spoken in
  the video. Hashtags: none retained or tested.
- Unavailable: X search results, fresh owned tweet metrics, composer preview.

### LinkedIn research

- Date: October 23, 2026. Sources: web searches for LinkedIn posts on residual
  connections and vanishing gradients, which returned tutorials and papers plus
  two LinkedIn Advice pages on debugging and fixing vanishing gradients (language
  evidence only, not post performance); the Chapter 13 announcement structure;
  the episode captions.
- Primary phrase: neural network from scratch in C++. Supporting: vanishing
  gradient, residual connections, debugging gradients, cross-entropy loss,
  learning rate, MNIST. Hashtags: none.
- Unavailable: LinkedIn post examples, owned analytics, composer preview.

## Final title

```text
Residual Connections and Debugging Gradients in C++ | Deep Learning, All the Way Down #14
```

## YouTube description

Chapters derived from the uploaded video's English captions on October 23,
2026. See `chapters.txt` and `chapters-review.md`.

```text
Build residual connections in C++ and debug vanishing gradients layer by layer in a sixteen-layer neural network trained on MNIST handwritten digits.

In Episode 14 of Deep Learning, All the Way Down, we stack sixteen hidden layers and write a report that prints the size of every layer's output and gradient. The report shows the gradient shrinking on its way back to the early layers. Then we add a Residual layer that adds its input to the output of the layer it wraps, and train the new network.

We also look at what the loss measures. Cross-entropy loss is the negative log of the probability the network gives the correct digit, so guessing among ten digits costs 2.30 and a confident wrong answer costs far more. We finish by lowering the starting learning rate and training for 20 epochs, which reaches 92.85% accuracy on 2,000 test images.

Topics covered:
- A name for every Layer, and a Sequence that is itself a Layer
- A traced forward pass that keeps each layer's output
- A per-layer report of signal and gradient size
- Vanishing gradients in a deep plain network
- A Residual layer: the input plus the wrapped layer's output
- Cross-entropy loss as the negative log probability of the correct digit
- Choosing the learning rate, learning rate decay and number of epochs

Complete series:
https://www.youtube.com/playlist?list=PLZSg76FHvdTw

Source code:
https://github.com/mechanical-turk/deep-learning-all-the-way-down

Chapters:
00:00 Introduction
00:33 Simplify layer construction
02:05 Build reusable hidden layers
04:10 Stack sixteen hidden layers
05:15 When deeper networks stall
07:34 Name layers for debugging
09:39 Trace the forward pass
11:22 Print the layer report
14:04 Measure signal with RMS
17:33 Trace gradients in training
19:32 Spot vanishing gradients
20:55 Residual connections
22:58 Implement the Residual layer
25:30 Wrap the hidden layers
26:25 Compare residual gradients
28:35 Cross-entropy loss
31:55 Map probabilities to loss
34:48 Why loss can exceed 2.30
38:40 Tanh saturation and collapse
41:02 Learning rate decay recovery
42:07 Loss versus accuracy
45:12 Lower the learning rate
48:50 Train for twenty epochs
49:45 Recap
```

## Suggested tags

```text
C++, cpp, C++23, machine learning, deep learning, neural networks, neural network from scratch, neural network in C++, deep learning in C++, residual connections, skip connections, vanishing gradient, vanishing gradients, debugging neural networks, MNIST, handwritten digit recognition, cross entropy loss, learning rate, gradient descent, backpropagation, tanh, Deep Learning All the Way Down
```

## First-comment candidate

Proposed, not approved, not posted. Check existing author comments before any
posting. No GitHub link.

```text
At a starting learning rate of 0.5, the sixteen-layer residual network ended at 58.85% test accuracy. Lowering the starting rate to 0.08, slowing the decay to 0.95 and training for 20 epochs took it to 92.85%. Residual connections keep the gradient from shrinking, but the learning rate that works changed. If you kept tuning, would you lower the rate further, scale each residual branch down, or add an optimizer such as momentum?
```

## X announcement

Rewritten October 23, 2026 to cover the whole episode. Final copy. Not posted. Post
only after the video is public (scheduled October 23, 2026, 11:00 AM ET) and the
link opens while logged out. Inspect the account for an existing Episode 14 post
first. This is a long post (about 1,000 characters), which needs X's longer post
limit; the account's limit is unverified. Check the composer before posting.

```text
We stacked sixteen layers in a C++ neural network and it stopped learning. The loss sat at 2.30, which is what guessing among ten MNIST digits costs, and test accuracy was 11.7%.

To find out why, we wrote a debugging report that prints the signal and gradient size of every layer. The gradient at the first layer was about 15,000 times smaller than at the output. That is the vanishing gradient problem.

A residual connection adds a layer's input to its output, so the gradient gets a path that never shrinks. Accuracy rose to 58.85%, but the first epoch's loss was 52, far worse than guessing. Cross-entropy loss has no upper limit, and the network was confidently wrong: large updates saturated tanh and it predicted one digit for every image.

A lower learning rate and 20 epochs reached 92.85% on 2,000 test images.

Episode 14 of Deep Learning, All the Way Down covers residual connections, gradient debugging, cross-entropy loss and learning rate in C++.

https://www.youtube.com/watch?v=YZnfcbwwOdI
```

## LinkedIn announcement

Rewritten October 23, 2026 to cover the whole episode. Final copy. Not posted.
Post the next weekday after the X announcement, with the URL below. Inspect the
account for an existing Episode 14 post first, and inspect the composer preview.

```text
A deeper neural network is not automatically a better one. A sixteen-layer network written from scratch in C++ trained to a loss of 2.30 and stayed there, which is what random guessing among ten MNIST digits costs. Test accuracy was 11.7%.

Episode 14 of Deep Learning, All the Way Down finds out why and fixes it:

- Layers get names, and a Sequence becomes a Layer itself, so a hidden layer is one Linear and one tanh built by a single helper.
- A traced forward pass keeps every layer's output, and a report prints the signal and gradient size of each layer. Size is measured with root mean square, because an ordinary average lets positive and negative values cancel.
- The report shows the signal halving at every layer. The gradient at the first layer is about 15,000 times smaller than at the output, which is the vanishing gradient problem, now measured instead of assumed.
- A Residual layer adds its input to the output of the layer it wraps. Addition sends the gradient down both sides at full size, so the gradient no longer vanishes. The first layer stays unwrapped because 784 inputs and 32 outputs cannot be added.
- Accuracy rises to 58.85%, but the first epoch's loss is 52, much worse than guessing. Cross-entropy loss is the negative log of the probability given to the correct digit and has no upper limit. The network was confidently wrong: a large learning rate saturated tanh, and it predicted one digit for nearly every image.
- A loss near 2.44 alongside 58.85% accuracy shows that loss and accuracy measure different things.
- Starting the learning rate at 0.08 instead of 0.5, with slower decay, and training for 20 epochs reaches 92.85% on a 2,000-image test subset, with diminishing returns after that.

Next: more training data and momentum, and hopefully the Adam optimizer.

https://www.youtube.com/watch?v=YZnfcbwwOdI
```

## X navigation reply / LinkedIn comment

Keep these links out of the main announcements. Inspect the preview and check for
an existing author reply or comment first.

```text
Source code:
https://github.com/mechanical-turk/deep-learning-all-the-way-down

Complete series:
https://www.youtube.com/playlist?list=PLZSg76FHvdTw
```

## Settings and release checks

- Intended settings: private, no schedule at first; English; category Education;
  not made for kids; add to the complete-series playlist
  (`PLZSg76FHvdTw`). Nothing applied.
- End screen: the file ends in continuous speech. The 52:22.5 frame shows the
  sign-off still being spoken, and silence detection finds no pause after about
  3139.9 s. There is no clean tail for the Subscribe and playlist end screen.
  Decision needed: append about five clean seconds, or accept an end screen over
  speech.
- Captions and chapters: none yet. After upload, download the English captions,
  derive chapters from actual transitions, begin `00:00 Introduction`, end
  `Recap`, and split sections longer than five minutes. Correct ASR errors such
  as MNIST and tanh.
- Resolution and playback: 2160p processing, code legibility and audio in the
  YouTube encode are uninspected.
- Copy readiness: YouTube title, tags and first-comment candidate are ready;
  the description waits for chapters. X and LinkedIn wait for the URL and a
  composer preview.
- Upload readiness: the file is probed and identified; thumbnail missing.
  Creator approval is required.
- Public-release readiness: not ready (thumbnail, chapters, end tail,
  processing, push).

## Short upload gate

N/A. This is a 16:9 long-form release.

## Distribution and follow-through

- Timeline and cadence consulted: [distribution timeline](../../docs/distribution-timeline.md),
  [posting cadence](../production/posting-cadence.md).
- Proposed sequence, windows and dependencies: [distribution.md](distribution.md).
- Reddit: explicit defer. Planning needs the Reddit research notes, the strategy
  document and current subreddit rules, which this package did not read.
- Separate Shorts: explicit defer. Any concept goes through the short-form
  playbook and critique check first. Nothing is scripted.
- Public source: the recorded code matches the local demo repository commit
  `47db7ed`, which is not pushed; see distribution.md.
- Post-publication: run the post-publication check, update the README video link,
  inspect for duplicate author comments before any authorized comment, report
  direct URLs, and append the timeline.
- Responsible person: the creator approves every external action.

## Checklist audit

| ID | Platform outcomes / overall status | Actual field or evidence | Points | Required fix |
| --- | --- | --- | ---: | --- |
| P01 | PASS | Every number in the copy (11.7%, 2.30, 3.2e-07 versus 4.7e-03 giving about 15,000x, 52, 58.85%, 0.08, 0.95, 20 epochs, 92.85%, 2,000 images) is visible in frames (October 23 checks at 6:50, 20:40 and 48:50 added) or spoken in the captions (loss 2.44, 0.5 start, confidently wrong, tanh saturation, one digit predicted, diminishing returns). The first run's constants come from reproduction. | 10/10 | None. |
| P02 | PARTIAL | YouTube: Oct 4 file plus Oct 22 searches. X and LinkedIn: Oct 23 platform-restricted searches found no relevant posts, only LinkedIn Advice pages as language evidence. No owned or autocomplete data. | 7.5/15 | Pull owned search terms; check X and LinkedIn in the live composers. |
| P03 | PASS | Title and first line lead with residual connections in C++; MNIST, vanishing gradients and cross-entropy appear in the first paragraphs and topic list. | 10/10 | None. |
| P04 | PASS | 22 backend tags with stated reasons; no visible hashtags, no evidence for any. | 8/8 | None. |
| P05 | PASS | Lint below found no em dashes or banned cadence. | 10/10 | None. |
| P06 | PASS | One `|`, series suffix, subject first, 89 characters. X and LinkedIn name the episode and series after the technical opening. | 5/5 | None. |
| P07 | PARTIAL | Playlist and repository links are known; the YouTube URL does not exist; no composer preview. | 2.5/5 | Replace placeholders; inspect previews. |
| P08 | PASS | Candidate tied to the 0.5 versus 0.08 result; unposted; no GitHub link. | 5/5 | Duplicate check before posting. |
| P09 | PASS | The file exists at the descriptive lowercase kebab-case name. | 4/4 | None. |
| P10 | UNVERIFIED | No thumbnail in the episode directory. | 0/4 | Supply and inspect one. |
| P11 | PARTIAL | Dimensions, duration, codecs, hash, audio levels and 13 frames measured; no full playback or narration review; keyboard audio unverified. | 3/6 | Full playback review. |
| P12 | UNVERIFIED | No settings applied; no clean end tail. | 0/3 | Resolve the end tail; apply and inspect settings. |
| P13 | UNVERIFIED | No captions or chapters. | 0/4 | Download captions after upload; derive chapters. |
| P14 | PASS | Dated windows, dependencies, deferrals, Reddit and Shorts decisions in distribution.md. | 3/3 | None. |
| P15 | PARTIAL | Output matches local commit `47db7ed`; not pushed; README has no hash or video link. | 1/2 | Push; add hash and link at release. |
| P16 | PARTIAL | YouTube fields parse and the description has the chapter block; X and LinkedIn now carry the real URL, no placeholder. X copy is about 1,000 characters and needs a longer post limit that is unverified. | 1/2 | Confirm the account's X post limit in the composer. |
| P17 | PASS | Unknowns named; arithmetic shown. | 2/2 | None. |
| P18 | PASS | Follow-up plan with owner. | 2/2 | None. |

Lint run October 22: no em dashes, no `Episode N is out`, no one-C++23-file
boilerplate, no "imagine" or "picture this".

## Critique

1. **Runtime is 52:24.** That is far above the 10 to 15 minute editorial target
   and the 30 minute cap now set for long-form. It is a retention risk that copy
   cannot repair. Chapters become the main navigation aid, which makes the
   caption-derived chapter block the most valuable unfinished item. Whether to
   trim before publishing is the creator's decision; no edit was requested.
2. **The video ends without a clean tail.** The Subscribe and playlist end
   screen has nothing clean to sit on. Appending about five seconds fixes it.
3. **Nothing spoken is verified.** The copy uses only what the frames show. The
   narration, including how the gradient shrinking is explained, waits for captions.
4. **The script no longer describes the video.** It ends at 0.1, 10 epochs and
   91.05%; the video ends at 0.08, 20 epochs and 92.85%. Treat the script as a
   planning record and do not quote its verification run as evidence for the video.
5. **No thumbnail, and the public repository is behind.** The README shows
   Episode 14 as work in progress with no hash or video link, and the commit is
   local.
6. **Research is thin.** There is no owned or autocomplete data, and the X and
   LinkedIn records are terminology only. No newer long-form retention data
   exists than Episodes 1 to 6.

## Final score

- Earned points / applicable maximum: 74 / 100.
- N/A exclusions: none for scoring. The Short upload gate is not a scored item.
- Normalized package-compliance score: 74.0.
- Assessed stage and platforms: draft / upload preparation; YouTube, with X and
  LinkedIn drafts.
- Copy readiness: YouTube ready except chapters; X and LinkedIn blocked on URL.
  Upload readiness: file ready, thumbnail missing, creator approval needed.
  Public-release readiness: not ready.
- Blocking checks and next action: thumbnail, clean end tail, captions and
  chapters, push of the demo commit, then composer previews.

Score: 74/100 (74/100). Decision: hold for public release; the file can be
uploaded privately once the creator approves. This is not approval to upload,
schedule, announce or comment.
