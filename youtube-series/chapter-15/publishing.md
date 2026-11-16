# Episode 15 — YouTube private upload

## Checklist plan

YouTube long-form, X and LinkedIn announcements, reviewed November 14 and 16, 2026. Stage: final export uploaded privately, unscheduled; X and LinkedIn copy drafted and not posted. Reddit and Shorts are deferred. No public date is set.

| Item | Planned evidence or action |
|---|---|
| P01 | Describe only recorded C++ momentum, Adam and SGD experiments; avoid benchmark winner claims. Final timeline inspected; full caption review pending. |
| P02 | Use November 14 YouTube Data API searches and chapter keyword research; do not invent traffic estimates. |
| P03 | Put momentum, Adam and C++ in the title and from-scratch implementation in the opening. |
| P04 | Use relevant backend tags; omit visible hashtags. |
| P05 | Plain English, no em dashes, no promotional filler. |
| P06 | Subject first; one separator; series identity ends in #15. |
| P07 | Link the owned complete-series playlist, verified by playlists.list. |
| P08 | Prepare a specific optimizer comparison comment; do not post without instructions. |
| P09 | Verify cpp-momentum-adam-optimizers-from-scratch.mp4 after rendering. |
| P10 | Custom thumbnail and small-screen review remain pending before public release. |
| P11 | Verify native 3840×2160, 30 fps, 61,469 frames, stereo voice plus keyboard; final-file playback pending. |
| P12 | Private, unscheduled, English, Education, not made for kids. Processing, playlist membership and end screen pending. |
| P13 | Derive chapters from final captions after upload; never reuse pre-cut timestamps. |
| P14 | YouTube private upload plus X and LinkedIn announcement drafts. Reddit and Shorts deferred; release timing is in distribution.md as a plan only. |
| P15 | Code checkpoint `1d2a49a` pushed November 16 and verified by compiling and running it; the README links it. |
| P16 | Use supported parser headings and plain-text fields; inspect upload dry run. |
| P17 | Score the private-upload preparation stage, keeping public-release gaps visible. |
| P18 | Record the returned video URL and verified privacy in the ledger; public release requires resolution, captions and navigation checks. |

## Media and release status

Filename: `cpp-momentum-adam-optimizers-from-scratch.mp4`

Local path: `/Users/keremkazan/Movies/CapCut/ep15/cpp-momentum-adam-optimizers-from-scratch.mp4`

Source: the creator's finished Resolve timeline, saved as `ep15-final-2026-11-14.xml` with a matching DRP backup in the episode's `.episode-edit` directory. The XML contains 61,469 frames, 34:08.967, 4K/30, existing 107% picture retiming and aligned cleaned voice plus preserved keyboard audio. Direct XML rendering cannot reproduce unrepresented Resolve grades, Fusion or Fairlight bus effects. Export completed and passed full decoding, 4K/30, exact frame count, matching stereo AAC duration and no-clipping checks. A preview at 15:00 shows readable code. Full subjective playback remains pending. Uploaded: https://www.youtube.com/watch?v=wBB9lQnpUNU

Studio: https://studio.youtube.com/video/wBB9lQnpUNU/edit

API read-back verified private, unscheduled, not made for kids and the exact title. As of November 16, API processing has succeeded; 2160p playback is unverified. Complete-series playlist membership was also verified.

File identity: 3,475,946,106 bytes; SHA-256 `a345b5822f265103115a64d95a3e62a95cf8f89bbbc8c36ec81fdc2e1f18d544`.

## Final title

```text
Momentum and Adam Optimizers in C++ | Deep Learning, All the Way Down #15
```

## YouTube description

```text
Build momentum and Adam optimizers from scratch in C++, then compare them with stochastic gradient descent on an MNIST neural network.

We add optimizer state to the training loop and explore how learning-rate choices affect training loss and test accuracy.

Episode 15 of Deep Learning, All the Way Down.

Watch the series from the beginning:
https://www.youtube.com/playlist?list=PLZSg76FHvdTw

Chapters:
00:00 Introduction
00:22 Smaller MNIST network
01:01 Training configuration
02:59 How momentum works
03:58 Implementing momentum
06:44 Momentum in training
08:26 Tracing SGD gradients
10:11 First momentum run
11:21 Signals and gradients
12:40 Lowering the learning rate
13:58 Why velocity builds up
14:58 Learning-rate search
18:01 How Adam works
20:19 Adam's second moment
21:45 Scaling the update
22:41 Avoiding division by zero
23:25 First Adam run
25:14 Zero-initialization bias
27:15 Why bias correction works
28:20 Coding bias correction
29:57 Comparing Adam and momentum
31:03 Recap
```

## Suggested tags

```text
C++, momentum optimizer, Adam optimizer, optimizer from scratch, stochastic gradient descent, SGD, MNIST, neural networks, deep learning, Deep Learning All the Way Down
```

## First-comment candidate — not posted

```text
An optimizer comparison depends on the learning rate as well as the update rule. The MNIST runs here are individual experiments, not evidence that one optimizer always wins. A useful next comparison would tune each optimizer separately and repeat the runs with different random seeds.
```

This is a prepared candidate only. No comment, pin or reminder is authorized by this package. Inspect existing author comments before any later authorized post.

## Search evidence and wording

Research date: November 14, 2026. YouTube Data API searches for “Adam optimizer from scratch” and “momentum Adam C++” were inspected. Relevant results include [Adam Optimizer from Scratch in Python](https://www.youtube.com/watch?v=M4HQHmBrAmI), [ADAM optimizer from scratch](https://www.youtube.com/watch?v=YisebsYZK7c), and [Adding Momentum algorithm](https://www.youtube.com/watch?v=amWI5EOPUfg). Their titles support recognizable subject language, not search-volume or ranking claims. Local evidence: `work/ep15/youtube-search-2026-11-14.json` in the editing workspace; also see `keyword-research.md`.

Primary phrase: momentum and Adam optimizers in C++. Supporting terms: from scratch, SGD, MNIST, training loss, test accuracy. The title carries the primary phrase; the first description paragraph carries implementation, SGD and MNIST. Backend tags group the actual language, optimizer names and subject. No visible hashtags: the title and prose identify the lesson clearly. Reject #shorts, AdamW, Nesterov, schedulers and claims of an overall winner because this release does not establish them.

Owned channel identity and recent uploads were checked through the API; no existing Episode 15 upload was present in the recent history. Owned search-query analytics and autocomplete evidence were unavailable. No quantitative demand claim is made.

## X announcement

Draft, November 16, 2026. Not posted. Post only after the video is public and the
link opens while logged out. Inspect the account for an existing Episode 15 post
first. This is a long post (about 1,100 characters); check the composer's limit
and preview before posting. Numbers are the recorded single runs (one network,
one random seed, five epochs, batch 250), taken from the verified run output.

```text
Plain gradient descent forgets each step as soon as it takes it. Momentum remembers. In a C++ neural network on MNIST, giving every weight a velocity cut the training loss from 0.162 to 0.077 after five epochs, and test accuracy went from 91.3% to 93.75%. The learning rate had to drop from 1.0 to 0.316 first, because velocity makes each step up to ten times longer.

Adam also tracks the average squared gradient, so each weight's step is scaled by that weight's own recent gradient size. Its averages start at zero, which made the first steps about three times too large, and our Adam finished behind momentum. Dividing by one minus beta to the power of the step count fixed it: loss 0.051, accuracy 93.65%.

These are single runs on one network, so they show how the optimizers work, not which one wins.

Episode 15 of Deep Learning, All the Way Down builds momentum and Adam from scratch in C++.

https://www.youtube.com/watch?v=wBB9lQnpUNU
```

## LinkedIn announcement

Draft, November 16, 2026. Not posted. Post the next weekday after the X
announcement, with the URL below. Inspect the account for an existing Episode 15
post first, and inspect the composer preview.

```text
A faster optimizer is mostly bookkeeping: what each weight remembers from earlier steps. Episode 15 of Deep Learning, All the Way Down adds that memory to a C++ neural network trained on MNIST.

- Plain gradient descent chooses every step from the current gradient and forgets it. Momentum keeps a velocity per weight: multiply the old velocity by 0.9, add the new gradient. A steady gradient makes the velocity approach ten times the gradient, so the same learning rate moves much further.
- That is why the rate had to change. Reading the loss and gradient traces showed momentum at rate 1.0 taking steps too large (loss 0.50, accuracy 82.1%). A search over rates spaced four per decade picked 0.316: loss 0.077 and 93.75%, against 0.162 and 91.3% for plain gradient descent at its own rate of 1.0.
- Adam keeps two running averages per weight: the gradient (first moment) and the squared gradient (second moment). Dividing the first by the square root of the second makes every step close to the learning rate in size, whatever the raw gradient looks like.
- Both averages start at zero, so early on they are far too small and the first steps come out about three times too large. We ran it that way first: loss 0.134 and 91.15%, worse than momentum. Dividing each average by one minus beta to the power of the step count removes the bias.
- With the correction, Adam reached a loss of 0.051 and 93.65%. Momentum's best was 93.75%. A lower loss with slightly lower accuracy points toward overfitting the 10,000 training images, which the next episode takes on with more data.

These are single runs of one network with one random seed, not a ranking of optimizers.

https://www.youtube.com/watch?v=wBB9lQnpUNU
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

## X and LinkedIn research records

```text
Platform: X
Research date: November 16, 2026
Sources checked: the Episode 14 announcement copy and its structure in this repository; the platform copy playbook X rules; the recorded run output and captions for every number.
Owned-account evidence: unavailable. No X post analytics or search-term data were read for this package.
Candidate search phrases: momentum and Adam optimizers in C++; Adam optimizer from scratch; momentum SGD MNIST.
Primary phrase: momentum and Adam from scratch in C++
Supporting terms: velocity, learning rate, MNIST
Hashtags retained: none
Hashtags rejected: all. No evidence that hashtags help an episode post in this account's niche, and the previous episodes used none.
Reasoning and evidence: the opening states the contrast (forgetting versus remembering) and the measured result, then names the episode and series.
Unavailable evidence: live X search and autocomplete, owned-account analytics.

Platform: LinkedIn
Research date: November 16, 2026
Sources checked: Episode 14 LinkedIn copy; the playbook LinkedIn rules; recorded run output.
Owned-account evidence: unavailable.
Candidate search phrases: optimizer from scratch; Adam optimizer bias correction; momentum optimizer C++.
Primary phrase: momentum and Adam optimizers
Supporting terms: bias correction, learning rate, neural network from scratch in C++
Hashtags retained: none
Hashtags rejected: all, for the same reason as X.
Reasoning and evidence: leads with the technical idea (an optimizer is bookkeeping of what each weight remembers), as the playbook requires.
Unavailable evidence: LinkedIn search data, owned-account analytics.
```

Claim check for both posts. Every number comes from the verified run of the same code and seed (`verification/dump.txt`, `verification/last-run.txt`): 0.162 and 91.3% (plain gradient descent, rate 1.0), 0.50 and 82.1% (momentum, rate 1.0), 0.077 and 93.75% (momentum, 0.316), 0.134 and 91.15% (Adam without the step count), 0.051 and 93.65% (Adam with it). The three-times-too-large first step is the verified factor 1/(1 - 0.9) over sqrt(1/(1 - 0.999)), about 3.16. The recording speaks 0.162, 0.077, 0.05, 93.65% and 93.75%; the other figures were not read from the recorded frames. The final code checkpoint reproduces 0.0510026 and 93.65%.

## Settings and follow-through

Private, unscheduled; English audio and metadata; Education (27); not made for kids; embedding enabled. The complete-series playlist ID was verified from the owned account, and Episode 15 membership is verified. Comment moderation, end screen and 2160p playback are unverified. Custom thumbnail remains pending. On November 16, downloaded the serving English captions and added 22 transcript-derived chapters. Boundary evidence, technical-term corrections in labels and script deviations are recorded in chapters-review.md. The raw automatic caption track itself was not edited. The public source checkpoint is `1d2a49a` in the demo repository (pushed November 16; compile and run verified).

No public date is set. X and LinkedIn announcements are drafted above and not posted; Reddit and Shorts are deferred. After upload, record the direct URL and actual privacy/processing status. Publication requires a separate release decision and the automatic post-publication check. A private upload does not establish public readiness.

## Checklist audit

| Item | Status | Points | Evidence or remaining repair |
|---|---|---:|---|
| P01 | PARTIAL | 5/10 | Social numbers checked against the verified run and the captions (see claim check). Full subjective final playback pending; Adam's 0.134 and SGD's 91.3% were not read from recorded frames. |
| P02 | PARTIAL | 7.5/15 | YouTube research complete. X and LinkedIn records exist but have no owned-account or live-search evidence. Repair: read account analytics and live search before posting. |
| P03 | PASS | 10/10 | Accurate subject in title and opening; supporting terms in description. |
| P04 | PASS | 8/8 | Relevant backend tags; reasoned omission of visible hashtags on YouTube, X and LinkedIn. |
| P05 | PASS | 10/10 | All copy, both announcements and the candidate comment use plain, specific English with no em dashes. |
| P06 | PASS | 5/5 | One separator, correct identity, title under 100 characters. X and LinkedIn name Episode 15 and the series after the technical opening. |
| P07 | PARTIAL | 3/5 | November 16 checks: playlist resolves to the series playlist; GitHub repository and checkpoint `1d2a49a` return 200; each announcement has one YouTube URL and the navigation reply holds GitHub and playlist. The video URL is private and will not open logged out; composer previews not inspected. |
| P08 | PASS | 5/5 | First-comment candidate and the X/LinkedIn navigation reply prepared; none posted. |
| P09 | PASS | 4/4 | Completed file, exact path, size and SHA-256 recorded above. |
| P10 | UNVERIFIED | 0/4 | Thumbnail and destination preview pending. |
| P11 | PARTIAL | 3/6 | Approved timeline known; final-file technical checks passed; full subjective playback remains pending. |
| P12 | PARTIAL | 1.5/3 | Concrete upload settings; processing, navigation and Studio-only checks pending. |
| P13 | PASS | 4/4 | Serving captions cached; 22 recorded-transition chapters validated and read back exactly from YouTube. See chapters-review.md. Caption text itself was not edited. |
| P14 | PASS | 3/3 | YouTube, X and LinkedIn covered; Reddit and Shorts explicitly deferred. |
| P15 | PASS | 2/2 | `1d2a49a` compiled and ran to epoch 5 loss 0.0510026 and 93.65% (1873/2000), matching the recording; pushed, README links it. |
| P16 | PASS | 2/2 | Separate supported fields; inspect dry run before applying upload. |
| P17 | PASS | 2/2 | All IDs covered with pending evidence distinguished. |
| P18 | PASS | 2/2 | Concrete upload ledger and public-release follow-through above. |

## Critique

The strongest remaining gaps are release gates, not copy. The thumbnail does not exist, the final file has not been played in full, 2160p playback and the end screen are unchecked, and the video is private, so the announcement link will not open for anyone until release. The X and LinkedIn research records lack account analytics and live search evidence, so the copy choices are reasoned from the series' own previous posts only. Two figures in the posts (SGD 91.3% and Adam without the step count at 0.134 and 91.15%) come from the verified run of the same code rather than from the recorded frames; the video says "91% or something" for SGD, and the ASR garbles the Adam loss. Repair: read those two values from the recording during the playback review. The posts carry their own limit (single runs, one seed), which matches the evidence: the later batch-size experiments show comparisons flip with epoch budget, so no winner is claimed.

## Final score

77/100 for the private upload plus X and LinkedIn drafts, reviewed November 16, 2026. Decision: hold public release. Blockers: thumbnail, full playback, 2160p and end-screen checks, composer previews, X and LinkedIn account evidence. The code checkpoint is no longer a blocker.
