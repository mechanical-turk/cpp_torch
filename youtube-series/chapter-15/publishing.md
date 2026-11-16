# Episode 15 — YouTube private upload

## Checklist plan

YouTube long-form only, reviewed November 14, 2026. Stage: final export verified and uploaded privately, unscheduled. No public release or other-platform announcement is scheduled.

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
| P14 | YouTube private upload only. Defer X, LinkedIn, Reddit and Shorts; no release-time recommendation. |
| P15 | Public Episode 15 code checkpoint remains unverified; do not claim code availability. |
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

## Settings and follow-through

Private, unscheduled; English audio and metadata; Education (27); not made for kids; embedding enabled. The complete-series playlist ID was verified from the owned account, and Episode 15 membership is verified. Comment moderation, end screen and 2160p playback are unverified. Custom thumbnail remains pending. On November 16, downloaded the serving English captions and added 22 transcript-derived chapters. Boundary evidence, technical-term corrections in labels and script deviations are recorded in chapters-review.md. The raw automatic caption track itself was not edited. Verify public source checkpoint separately; no repository push is authorized here.

No public date, X or LinkedIn announcement, Reddit post or separate Short is planned in this YouTube-only scope. After upload, record the direct URL and actual privacy/processing status. Publication requires a separate release decision and the automatic post-publication check. A private upload does not establish public readiness.

## Checklist audit

| Item | Status | Points | Evidence or remaining repair |
|---|---|---:|---|
| P01 | PARTIAL | 5/10 | Timeline and recorded optimizer experiments inspected; captions reviewed for chapter boundaries; full subjective final playback pending. No numerical performance claims. |
| P02 | PASS | 15/15 | Dated YouTube searches, linked results and explicit unavailable evidence above. |
| P03 | PASS | 10/10 | Accurate subject in title and opening; supporting terms in description. |
| P04 | PASS | 8/8 | Relevant backend tags; reasoned omission of visible hashtags. |
| P05 | PASS | 10/10 | All copy and candidate comment use plain, specific English. |
| P06 | PASS | 5/5 | One separator, correct identity, title under 100 characters. |
| P07 | PASS | 5/5 | Complete-series destination returned by owned playlists.list. |
| P08 | PASS | 5/5 | Specific comparison limitation candidate prepared; posting explicitly pending. |
| P09 | PASS | 4/4 | Completed file, exact path, size and SHA-256 recorded above. |
| P10 | UNVERIFIED | 0/4 | Thumbnail and destination preview pending. |
| P11 | PARTIAL | 3/6 | Approved timeline known; final-file technical checks passed; full subjective playback remains pending. |
| P12 | PARTIAL | 1.5/3 | Concrete upload settings; processing, navigation and Studio-only checks pending. |
| P13 | PASS | 4/4 | Serving captions cached; 22 recorded-transition chapters validated and read back exactly from YouTube. See chapters-review.md. Caption text itself was not edited. |
| P14 | PASS | 3/3 | YouTube-only private scope; other destinations explicitly deferred. |
| P15 | UNVERIFIED | 0/2 | Episode code checkpoint/public state not established. |
| P16 | PASS | 2/2 | Separate supported fields; inspect dry run before applying upload. |
| P17 | PASS | 2/2 | All IDs covered with pending evidence distinguished. |
| P18 | PASS | 2/2 | Concrete upload ledger and public-release follow-through above. |

## Critique

This is a conservative private-upload package. The strongest remaining gaps are final-file playback, a verified thumbnail and the public code checkpoint. These limit public readiness; they do not justify inventing chapter timestamps or benchmark conclusions. Technical export checks passed before the private upload. Public release still requires the pending checks above.

## Final score

84.5/100 (84.5 / 100 x 100), limited chapter update reviewed November 16; other audit items retain their prior evidence. The creator-authorized upload completed; API read-back verified private and unscheduled. The local export passed technical verification; YouTube API processing has succeeded; 2160p playback is still unverified. Public release is not scheduled; the outstanding media, thumbnail and end-screen checks remain open.
