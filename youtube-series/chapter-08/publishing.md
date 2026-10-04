# Episode 8 Publishing Package

## Checklist plan

Review: September 8, 2026. Stage: post-publication reconciliation and revised
announcement drafts. Platforms: YouTube, X and LinkedIn. Reddit is deferred;
Instagram/TikTok native long-form uploads and a new Short are not part of this
package. This replaces the stale pre-upload draft, not the recorded video.

| ID | Approach and remaining risk |
| --- | --- |
| P01 | Use the uploaded media metadata and downloaded ASR, not the old script's original scope. Elementwise autograd is implemented; sum/matmul backward and training remain deferred. |
| P02 | Research platform wording separately; preserve source and access limitations rather than claim search-volume evidence. |
| P03 | Put broadcasting, autograd, tensor and C++ in the X copy itself. Retain the searchable episode title. |
| P04 | Retain the live, relevant backend tags. No decorative hashtag block. |
| P05 | Match Episode 7's announcement: a direct explanation of the capability, then what I build in this episode. Audit LinkedIn separately. Preserve the live YouTube description as a record, with its weaker introduction flagged. |
| P06 | Preserve series name, episode number and one title separator. |
| P07 | Replace every pending watch URL with the verified Episode 8 URL. Keep secondary links in social replies. |
| P08 | Prepare a storage-copy tradeoff comment, not an answer key. Do not post the candidate without selection. |
| P09 | Record the actual descriptive upload filename and inspected file. |
| P10 | Record the existing uploaded thumbnail, not the old claim that it is missing. Full small-screen audit remains separate. |
| P11 | Record measured 4K master properties; do not invent a full audiovisual playback pass. |
| P12 | Check public status, processing, comments, playlist and end-screen navigation. Keep pending YouTube checks visible. |
| P13 | Use the 17 caption-derived chapters already applied to YouTube. |
| P14 | Base announcement timing on actual 11:30 AM ET publication. No schedule or post is created by this file. |
| P15 | Flag the uncommitted Episode 8 source and Episode 7-only README before promoting the code checkpoint. |
| P16 | Keep copy fields separate and parser-safe. Proposed comment uses a non-parser heading. |
| P17 | Score the reconciled package honestly; distinguish improved text from verified composer previews. |
| P18 | Record external fixes, remaining checks and publication URLs in the timeline. |

## Release facts

September 11 reconciliation: source checkpoint and public README are now
current at Episode 8 checkpoint `7021cfe` and README commit `f24101e`; remote
main agrees and both C++ entry points pass. The older source-pending statements
below are superseded. X/LinkedIn publication remains unconfirmed, not verified
absent. The newer [Reddit draft](../forum-announcements/reddit-episode-08.md)
proposes September 13 at 12:30 PM ET, superseding the earlier defer. Studio
page control remains blocked; no new Checking/end-screen clearance is claimed.
See the [current audit](../analytics/reports/2026-09-11-engine-check.md).

- Public episode: https://www.youtube.com/watch?v=RXCeVnhjHCQ
- Published: **September 8, 2026, 11:30:21 AM ET**, verified by API.
- Exact upload filename: `cpp-tensor-autograd-elementwise-backpropagation.mp4`
- Master: `aliases/04-final-cuts/ep08/cpp-tensor-autograd-elementwise-backpropagation.mp4`
- Local ffprobe: 3840x2160, 30 fps, H.264 video, stereo AAC audio,
  1554.033 seconds (25:54.03), 5,407,370,508 bytes.
- Uploaded filename and byte size match. Studio/API display runtime 25:55.
- Thumbnail: [assets/thumbnail.png](assets/thumbnail.png); custom thumbnail
  visibly present in Studio and on the public upload.
- Processing succeeded; Studio reports 4K complete; public player offers 2160p.
- Comments On, Anyone; Basic moderation preserved. Newest-first sorting saved
  and Studio confirmed Changes saved.
- Main series playlist membership verified. Subscribe and Best for viewer
  existed. The missing complete-series playlist end-screen element was added
  and saved at approximately 25:48 through 25:54.
- **Checking remains unresolved.** Studio says checks are still running and
  results should be ready soon. No specific claim/error appeared in that notice.
  Processing success and public visibility do not establish copyright clearance.
- Master has no verified clean five-second tail after the sign-off. The new
  playlist element overlaps the closing speech; existing elements begin sooner.
  Do not label the clean-tail requirement passed.
- The edited runtime exceeds the new 10-15 minute target. Publication is an
  observed creator action, not evidence that runtime or continuity concerns
  disappeared. Do not delete or reschedule this upload automatically.
- Audio track and start of public playback observed. Full playback, subjective
  audio quality and complete caption accuracy remain unverified.

## Final title

```text
Tensor Autograd from Scratch in C++ | Deep Learning, All the Way Down #8
```

## YouTube description

Live description preserved below, including the corrected backward-order line
and caption-derived chapters. This turn does not silently replace the rest of
the already published description. Its abstract opening remains a copy weakness.

```text
Our tensor can already calculate a result. Now it learns how each input needs to change to reduce that result, by building a real autograd engine on top of it in C++.

In Episode 8 of Deep Learning, All the Way Down, we give the tensor a memory of its own history. Every result now records the tensors and operation that produced it, so a backward pass can walk that graph in reverse, apply each operation's local derivative, and accumulate gradients across every path a value took to the output, including the paths created by broadcasting.

We cover:

• keeping tensor data alive across shared copies
• recording operation history as a graph of nodes
• collecting the nodes reachable from a result
• propagating each result's gradient before processing its parents
• starting backpropagation from a scalar root
• the backward rules for addition, subtraction, multiplication, and division
• reducing broadcasted gradients back to their original shape

Sum and matrix multiplication backward, gradient tests, and a linear
regression training loop are next.

Source code:
https://github.com/mechanical-turk/deep-learning-all-the-way-down

Complete series:
https://www.youtube.com/playlist?list=PLZSg76FHvdTw

Chapters:
00:00 Introduction
00:26 Shared tensor nodes
01:58 Check shared copies
02:53 Store gradients
03:45 Record operation history
06:27 Record sum and matmul
07:40 Build topological order
10:29 Start backward
11:37 Reset and seed gradients
12:25 Reverse traversal
14:02 Save broadcast strides
15:58 Write backward helper
18:42 Apply local derivatives
20:52 Addition and subtraction
22:20 Multiplication rule
23:06 Division rule
24:46 Recap
```

## Suggested tags

Existing live metadata, not a newly applied tag set:

```text
tensor autograd, autograd from scratch, tensor autograd from scratch, autograd engine, tensor library, automatic differentiation, backpropagation, backpropagation from scratch, computation graph, reverse mode automatic differentiation, broadcasting, gradient broadcasting, gradient accumulation, chain rule, C++, C plus plus, cpp
```

## First-comment candidate

**Draft only, not posted or selected for automatic application.** No Q&A,
answer-key or automatic pin obligation. A fresh API read found zero comments;
inspect again immediately before any later authorized post.

```text
Tensor b = a now shares the same data and gradient storage. Changing b's data also changes a's data.

I'd keep that cheap shared copy and add an explicit clone() when we need independent storage. Would you expect a C++ tensor library to share storage on a copy, or copy the data?
```

This adds a concrete API-design tradeoff rather than repeating the description.
The episode demonstrates shared copies. clone() is a proposed design, not a
claim that the repository implements it.

## X announcement

Text revised; **not posted**. Fits an ordinary 280-character post with the URL
counted as 23. Names the language, tensor autograd, broadcasting, episode and series.
No machine specifications, corporate preface, em dash or hashtag block.

```text
Our C++ tensor can now track its calculations and work backward through them to compute gradients.

In Episode 8 of Deep Learning, All the Way Down, I add autograd to our tensor library, including gradient accumulation through broadcasting.

https://www.youtube.com/watch?v=RXCeVnhjHCQ
```

### Navigation reply

Post only after the announcement exists; first verify that the public source
checkpoint is current. Inspect existing author replies to avoid duplication.

```text
Complete series:
https://www.youtube.com/playlist?list=PLZSg76FHvdTw

Source code:
https://github.com/mechanical-turk/deep-learning-all-the-way-down
```

The main post contains only the YouTube URL. Its actual composer preview has
not been verified because X search redirected to sign-in.

## LinkedIn announcement

Revised draft, not posted. Corrects the old draft's reversed traversal claim.

```text
When broadcasting reuses one input across a tensor, its gradient has to include every use. We need to collect those contributions without building a separate graph node for every number.

In Episode 8 of Deep Learning, All the Way Down, we add autograd to our C++ tensor from scratch. Each result keeps its input nodes, and the backward pass accumulates gradients for addition, subtraction, multiplication and division.

Sum and matrix multiplication backward come next, followed by gradient tests and a linear regression training loop.

https://www.youtube.com/watch?v=RXCeVnhjHCQ
```

### First author comment

Verify the public source checkpoint before using this navigation comment:

```text
Source code:
https://github.com/mechanical-turk/deep-learning-all-the-way-down

Complete series:
https://www.youtube.com/playlist?list=PLZSg76FHvdTw
```

## Keyword and hashtag research

Research date: September 8, 2026. These records establish terminology and fit,
not search volume or predicted engagement.

### YouTube

- Evidence: the channel's actual Episode 7 and 8 titles; current Episode 8
  captions; earlier package research referencing
  [tensor-grad](https://github.com/r-gould/tensor-grad) and
  [microtensor](https://github.com/jeffbaumes/microtensor). Those external
  references are retained prior research, not newly inspected source code.
- Current web query for YouTube autograd-from-scratch videos produced no useful
  comparable result. Owned Episode 7 Studio showed 3.9% thumbnail CTR, but
  that is not query-level demand evidence.
- Candidates: tensor autograd, autograd from scratch, automatic differentiation,
  broadcasting gradients, C++ tensor library.
- Primary: tensor autograd from scratch in C++. Supporting: backpropagation,
  computation graph, gradient accumulation, broadcasting.
- Backend tags cover the language (including C++/cpp spellings), general
  technique and specific mechanism. No standalone training, CUDA or PyTorch
  implementation claim; no visible hashtags.
- Unknown: current autocomplete, per-query demand and incremental tag benefit.
  The prior draft's description of Episode 7's phrase as “validated” was too
  strong; a previous title is not validation.

### X

- Current checks: web search restricted to X for C++/autograd returned no useful
  comparable posts. Native X search redirected to sign-in.
- Broader language source:
  [X Engineering: Autograd for Torch](https://blog.x.com/engineering/en_us/topics/infrastructure/2015/autograd-for-torch)
  establishes autograd/gradients as technical terminology, but is old and does
  not establish current X-post demand or C++ popularity.
- Candidates: C++ autograd, tensor autograd, broadcasting gradients,
  automatic differentiation.
- Editorial reference: reread the saved Episode 3-7 announcements. Match
  Episode 7's direct capability statement followed by a first-person account
  of the implementation. Do not turn this into a speculative hook question.
- Primary: C++ tensor autograd. Supporting: tensor library, gradients,
  gradient accumulation and broadcasting. These appear in the announcement.
- Hashtags: none retained. No evidence justifies spending space on a hashtag
  block instead of the implementation detail and searchable plain text.
- Owned per-post/query evidence: not pulled; default X access is follower-only.
- **Limit:** relevance and wording audited; platform-demand research and the
  actual YouTube card preview remain unverified. Do not claim a complete SEO
  gate pass from keyword placement alone.

### LinkedIn

- Current independently searched comparable posts:
  [Building Autograd Engine in C++](https://www.linkedin.com/posts/nishchit-bhandari_this-valentines-i-was-a-little-too-free-activity-7429581680597721088-neDt)
  and
  [Building CUDA-GPT Autograd Engine](https://www.linkedin.com/posts/gaurang-gupta-0b70062a1_github-gaurang-2005cudagptcpp-activity-7478412323917910016-fSKo).
  Indexed text uses C++, autograd engine and automatic differentiation for
  tensor operations. This supports terminology, not their promotional cadence
  or claims of ranking success.
- Candidates: C++ tensor autograd, autograd engine, automatic differentiation,
  gradient accumulation.
- Primary: C++ tensor autograd. Supporting: broadcasting, backward pass,
  gradient accumulation. The copy explains the specific implementation.
- Hashtags: none; retain precise language without an unresearched generic block.
- Unknown: owned query data, search volume, comparable-post conversion and the
  live composer preview.

## Distribution and follow-through

- YouTube is already public; do not wait for the obsolete pre-upload draft.
- X: same day after public playback checks, normally about one hour after
  release. Proposed September 8 around 12:30 PM ET, or when the creator is
  available after that. This file does not schedule or publish it.
- LinkedIn: proposed Thursday September 10, 9:30 AM ET. This preserves the
  standing morning window and at least 24 hours after a Tuesday afternoon X
  announcement. Adjust if the actual X publication differs.
- Reddit: defer a new episode-only post. Revisit a substantive project milestone
  once the public code and gradient/training demonstration are ready. Check
  community rules before selecting a submission; no duplicate launch post.
- A separate Short is not commissioned by this package. Current Short 7
  recording remains a separate production task.
- Public GitHub: main.cpp has user edits; README still describes the previous
  checkpoint. Do not claim Episode 8 code is pushed or stage/commit user work
  as a side effect of updating this package.
- Capture 24-hour, 72-hour and seven-day long-form metrics separately from
  Shorts, including CTR, traffic mix, retention at 15/30/60 seconds, average
  duration and subscribers. No background job was created.
- Public chapters, complete playback and author-comment selection remain
  follow-ups. The creator paused browser work and set the Checking status
  aside for this handoff. No further browser checks were attempted.
  Record every later social post/comment with its direct URL.

## Checklist audit

| ID | Status | Points | Evidence / repair |
| --- | --- | ---: | --- |
| P01 | PARTIAL | 5/10 | ASR supports elementwise scope. Recorded opening promises more than the implemented endpoint; public introduction is imprecise. No training claim in revised social copy. |
| P02 | PARTIAL | 7.5/15 | Separate records exist. LinkedIn terminology has current indexed examples; YouTube query evidence is limited and X native research is login-blocked. |
| P03 | PASS | 10/10 | X now explicitly contains broadcasting, autograd, tensor, gradients and C++. LinkedIn names the same demonstrated mechanism. |
| P04 | PASS | 8/8 | Existing language/method/mechanism tag groups documented; visible hashtags intentionally omitted. No ranking benefit claimed. |
| P05 | PARTIAL | 5/10 | X and LinkedIn revised for concrete, connected language. Live YouTube opening preserved but remains abstract. |
| P06 | PASS | 5/5 | Correct series identity and #8, one title separator; X fits an ordinary post. |
| P07 | PARTIAL | 2.5/5 | All watch placeholders replaced; one main-post URL. X/LinkedIn composer cards still unverified. |
| P08 | PASS | 5/5 | Concrete first-comment candidate and navigation replies; draft status, duplicate check and no pin obligation explicit. |
| P09 | PASS | 4/4 | Real filename, upload byte-size match and local media properties recorded. |
| P10 | PARTIAL | 2/4 | Uploaded thumbnail exists and renders in Studio; a full small-screen/crop audit was not performed. |
| P11 | PARTIAL | 3/6 | Master/processing verified; no complete subjective audiovisual review. |
| P12 | PARTIAL | 1.5/3 | Public, 2160p, playlist, comments/Newest and required end-screen elements verified. Checking unresolved; no clean end-screen tail. |
| P13 | PARTIAL | 2/4 | Downloaded ASR and 17 valid chapters applied. Full caption-word audit and chapter-player rendering remain open. |
| P14 | PASS | 3/3 | Dated proposal derives from actual publication; no fabricated scheduled announcements. |
| P15 | PASS | 2/2 | September 11: public Episode 8 checkpoint 7021cfe and README f24101e are synchronized with remote main; both entry points compile and pass. Unpublished Episode 9 examples stay separate. |
| P16 | PASS | 2/2 | Known URLs, plain-text blocks, preserved parser headings and non-parser comment candidate. |
| P17 | PASS | 2/2 | Every item scored against evidence; unknowns not treated as completed. |
| P18 | PASS | 2/2 | Checks and follow-through recorded; no implied automatic social posts. |

## Critique

The X announcement now follows Episode 7's structure and includes the missing
C++/tensor-autograd search terms. It is a text improvement, not proof of a fully
passed discovery gate: native X research and composer preview remain blocked.

The public code checkpoint is now synchronized. YouTube checks are
recorded as unresolved, but the creator has set them aside for this copy
handoff. The 25:54 edit also still exceeds our new target. Narrow
future lessons before recording rather than rushing explanations. These facts
do not justify deleting a working public upload.

## Final score

**Score: 71.5/100 (71.5/100 applicable). Decision: copy handoff complete; full package clearance remains partial.**

Limited September 11 re-audit: P15 gained two points for the verified public
source/README correction. Other preparation scores are retained, not freshly
revalidated against Studio or social composers.

X/LinkedIn text revised; research/preview follow-ups remain. YouTube is already
public, not “waiting for an upload.” No announcement or first-comment candidate
was posted by this package update.
