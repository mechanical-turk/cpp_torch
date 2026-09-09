# Episode 7 Publishing Package

## Release target

- **Final edit:** complete
- **Verified final master:**
  `/Users/keremkazan/Documents/Projects/Content HQ/aliases/04-final-cuts/ep07/cpp-autograd-chain-rule-computation-graph.mp4`
- **Upload filename:**
  `cpp-autograd-chain-rule-computation-graph-episode-07.mp4`
- **Media verification:** 3840x2160, 30 fps, H.264 High, Rec.709, AAC stereo,
  23:39 runtime after the 13-second opening trim
- **Thumbnail:** [`assets/thumbnail.png`](assets/thumbnail.png), 1672x941,
  verified at a 320x180 feed-size preview
- **YouTube publication:** Saturday, August 29, 2026 at 11:00 AM ET, provided
  the private-upload checks pass
- **X announcement:** Saturday, August 29 at approximately 12:00 PM ET
- **LinkedIn announcement:** Sunday, August 30 between 9:00 and 10:30 AM ET
- **Native Short:** produce separately rather than clipping the episode

The publication time remains provisional until YouTube completes 4K
processing and every release check below passes.

## Final title

```text
Building Autograd from Scratch in C++ | Deep Learning, All the Way Down #7
```

## YouTube description

```text
Build an autograd engine from scratch in C++ and see how reverse-mode automatic differentiation turns one scalar loss into gradients for every weight and bias.

In Episode 7 of Deep Learning, All the Way Down, we turn ordinary scalar arithmetic into a computation graph. Each Value records the operation and inputs that produced it. backward() then traverses the graph in reverse topological order, applies the chain rule, and accumulates every parameter gradient.

We cover:

• representing scalar calculations as a computation graph
• preserving operation history with graph nodes
• building arithmetic operations that construct the graph
• local derivatives for addition, subtraction, and multiplication
• ordering the graph with a topological traversal
• propagating gradients in reverse topological order
• accumulating contributions from shared paths
• tracing one model loss back to its weights and bias

Source code:
https://github.com/mechanical-turk/deep-learning-all-the-way-down

Complete series:
https://www.youtube.com/playlist?list=PLZSg76FHvdTw
```

The description intentionally contains no chapter block before upload. Generate
caption-derived chapters from the recorded video, keep every label short enough
for YouTube's chapter interface, begin with `Introduction`, and end with
`Recap`.

## Thumbnail

Upload [`assets/thumbnail.png`](assets/thumbnail.png).

The thumbnail is approved for release. At 320x180, the face, `C++`, and
`AUTOGRAD` remain immediately readable. The graph becomes a secondary technical
cue, which is appropriate at feed size.

The source is smaller than the preferred 3840x2160 working canvas, but its
1672x941 resolution exceeds YouTube's minimum and is sufficient for this
release. Do not regenerate or rescale the portrait merely to claim a larger
source resolution.

## Suggested tags

```text
autograd, autograd from scratch, autograd engine, autodiff, automatic differentiation, automatic differentiation from scratch, reverse mode automatic differentiation, reverse mode autodiff, backpropagation, backpropagation from scratch, computation graph, computational graph, chain rule, C++, C plus plus, cpp
```

## Chapter timestamps

Derived from the video's automatic English captions and checked against the
recorded transitions:

```text
00:00 Introduction
01:47 Define graph nodes
03:50 Build Value handles
04:33 Overload arithmetic
06:57 Plan backpropagation
08:20 Build topological order
10:11 Implement backward()
12:37 Apply derivative rules
15:26 Test scalar backprop
17:18 Build the model loss
19:38 Verify model gradients
22:38 Recap
```

## Pinned comment

Post this immediately after the video becomes public. Report the direct comment
URL, then remind the learner once to pin it manually in YouTube Studio.

```text
Answers to the questions at the end:

1. The backward pass begins with loss.grad = 1.0 because the loss is the final output, and the derivative of the loss with respect to itself is 1.

2. A value can affect the loss through several paths. Each path contributes part of its gradient, so parent gradients use += to accumulate every contribution instead of replacing an earlier one.

3. A node must receive every gradient contribution from the results that depend on it before it propagates the total to its own parents. Reverse topological order guarantees that results are processed before their inputs.

Complete playlist:
https://www.youtube.com/playlist?list=PLZSg76FHvdTw
```

Do not add the source repository to this comment.

## YouTube upload settings

- Visibility during upload: **Private**
- Playlist: **Deep Learning, All the Way Down | From First Principles in C++**
- Category: **Science & Technology**
- Language: **English**
- Audience: **No, it is not made for kids**
- Comments: **On**
- Comment sorting: **Newest** where the publisher setting is available
- Embedding: **On**
- Thumbnail: [`assets/thumbnail.png`](assets/thumbnail.png)
- End screen: **Subscribe** plus the **complete series playlist** over only the
  clean final tail
- Captions: review the automatic English captions, especially `autograd`,
  `backward`, `computation graph`, `topological`, `shared_ptr`, `gradient`, and
  `C++`

Do not make the video public until:

- [x] The final file is present at the recorded path.
- [x] The master is 3840x2160, 30 fps, H.264 High, Rec.709, and AAC stereo.
- [x] The final runtime is recorded as 23:39 after the 13-second opening trim.
- [x] The thumbnail is 16:9 and passes the 320x180 legibility check.
- [ ] The file uploaded to YouTube has the descriptive Episode 7 filename.
- [ ] YouTube finishes processing the 4K version.
- [ ] YouTube reports no copyright, visibility, or processing restriction.
- [ ] The opening, a graph-construction section, `backward()`, and the final
      gradient assertions play correctly.
- [ ] Audio is present, synchronized, and free of clipping.
- [ ] Code and mathematical notation are legible at ordinary playback sizes.
- [ ] Every closing question remains visible before the end-screen elements.
- [ ] The final five-second tail contains only Subscribe and the complete-series
      playlist.
- [ ] The title, description, thumbnail, tags, playlist, category, language,
      audience setting, comments, and embedding settings match this package.
- [ ] Automatic captions are reviewed and caption-derived chapters are added.

## X announcement

### Timing

Publish Saturday, August 29 at approximately 12:00 PM ET, around one hour after
the YouTube release.

### Main post

```text
Automatic differentiation gives us the gradient of one loss with respect to every weight and bias.

In Episode 7 of Deep Learning, All the Way Down, I build an autograd engine from scratch in C++ and trace that loss through the computation graph.

https://www.youtube.com/watch?v=QEZvHrZDSdw
```

### Navigation reply

```text
Complete playlist:
https://www.youtube.com/playlist?list=PLZSg76FHvdTw

Source code:
https://github.com/mechanical-turk/deep-learning-all-the-way-down
```

### X checks

- The main post must contain no externally previewable URL other than the
  episode's YouTube watch URL.
- Confirm that the YouTube preview represents Episode 7 before publishing.
- If X serves an unusably compact player card, remove the card and attach the
  approved thumbnail directly while keeping the visible YouTube URL.
- Publish the navigation reply immediately and record both direct URLs.
- Remain available for substantive replies during the first hour.

## LinkedIn announcement

### Timing

Publish Sunday, August 30 between 9:00 and 10:30 AM ET.

### Main post

```text
Automatic differentiation is how a training loop works backward from one loss to every weight and bias.

In Episode 7 of Deep Learning, All the Way Down, I build a scalar automatic differentiation engine in C++.

Each value records the operation that produced it. The backward pass then follows that computation graph in reverse, applies the local derivative at each operation, and accumulates every gradient contribution before continuing toward the model parameters.

The episode covers:

• computation graphs and operation history
• graph ownership with shared pointers
• local derivatives for scalar arithmetic
• reverse topological traversal
• gradient accumulation across shared paths
• a complete backward() pass from loss to weights and bias

Watch Episode 7:
https://www.youtube.com/watch?v=QEZvHrZDSdw
```

### First author comment

```text
Source code:
https://github.com/mechanical-turk/deep-learning-all-the-way-down

Complete series:
https://www.youtube.com/playlist?list=PLZSg76FHvdTw
```

### LinkedIn checks

- Keep the main post limited to the episode's YouTube URL so its preview wins.
- Confirm the large YouTube preview before publishing.
- Add the source and playlist only in the first author comment.
- Record the direct post URL in the distribution timeline.

## Reddit decision

Do not submit Episode 7 as a bare video announcement. The current forum rules,
placement decisions, platform-specific drafts, and rollout order are recorded
in [`forums.md`](forums.md).

- Use r/learnmachinelearning for the standalone milestone post.
- Use the current r/cpp monthly Show and Tell thread for a shorter comment.
- Use only the current r/MachineLearning self-promotion thread there.
- Defer Hacker News, Lobsters, and r/deeplearning.

## Native Short plan

Produce a separate 20 to 25 second Short around this question:

```text
Why does every backward pass begin with loss.grad = 1?
```

Show `loss.grad = 1.0`, ask why the gradient is not calculated like the others,
then reveal `dL/dL = 1`. Keep the question and suspicious-looking line visible
inside the first second. Do not extract the segment from the long-form master.

## Keyword, tag, and hashtag research record

### YouTube

- **Research date:** August 28, 2026
- **Tools and surfaces consulted:** live YouTube autocomplete, current YouTube
  results, official YouTube Search and description guidance, official YouTube
  tag and hashtag guidance, the channel's latest local analytics export, and
  the channel's prior search-traffic reports
- **Candidate queries tested:** `autograd`, `autograd from scratch`, `autograd
  C++`, `automatic differentiation`, `automatic differentiation C++`,
  `backpropagation from scratch`, `computation graph`, `reverse mode automatic
  differentiation`, `PyTorch autograd`, `C++ autograd`, `cpp autograd`,
  `autograd in C++`, `autograd engine`, `micrograd C++`, `C++ automatic
  differentiation`, `backpropagation C++`, `autodiff`, `autodiff from scratch`,
  `automatic differentiation engine`, and `scalar autograd`
- **Observed autocomplete evidence:** YouTube suggested `autograd from
  scratch`, `autograd explained`, `autograd engine`, `automatic differentiation
  from scratch`, `automatic differentiation and computational graphs`,
  `backpropagation from scratch`, `computation graph deep learning`, and
  `reverse mode automatic differentiation`. `autodiff` also appeared as a
  direct suggestion. It returned no relevant language-qualified suggestion for
  `C++ autograd`, `cpp autograd`, `autograd in C++`, `micrograd C++`, `C++
  automatic differentiation`, or `backpropagation C++`.
- **Comparable-video evidence:** current results prominently use `PyTorch
  Autograd From Scratch`, `building micrograd`, `PyTorch Autograd Explained`,
  `Build AutoGrad From Scratch`, and `Automatic Differentiation Engine from
  scratch`. Public keyword metadata on the strongest exact comparable includes
  `autograd`, `backpropagation from scratch`, and `chain rule`.
- **Owned-channel evidence:** YouTube search has produced comparatively little
  channel traffic so far, although earlier qualified search views watched well.
  The available export does not provide enough Episode 7 query data to rank
  these terms by channel-specific demand before publication.
- **Primary intent retained:** `autograd from scratch` describes a viewer who
  wants to build the mechanism, not merely use a framework API. The title keeps
  that exact phrase and adds `C++` to qualify the implementation language.
- **Supporting intent retained:** the first description line includes
  `reverse-mode automatic differentiation`, while the body naturally includes
  `computation graph`, `chain rule`, `reverse topological order`, and
  `gradients`. These terms describe material the episode actually teaches.
- **Backend topic tags retained:** `autograd`, `autograd from scratch`,
  `autograd engine`, `autodiff`, `automatic differentiation`, `automatic
  differentiation from scratch`, `reverse mode automatic differentiation`,
  `reverse mode autodiff`, `backpropagation`, `backpropagation from scratch`,
  `computation graph`, `computational graph`, and `chain rule`. Each is either
  demonstrated search language, a standard technical synonym, or an alternate
  spelling of a demonstrated phrase that the episode directly fulfills.
- **Backend language tags retained:** `C++`, `C plus plus`, and `cpp`. `C++` is
  the exact implementation language. The other two cover common text spellings
  because YouTube says tags are most useful for spelling variants and mistakes.
- **Backend tags rejected:** `C++ machine learning` lacked direct evidence;
  standalone `machine learning` was too broad; `PyTorch autograd` and `PyTorch
  internals` imply framework-specific instruction the episode does not provide;
  `gradient accumulation` and `backward pass` remain in the natural description
  but lacked enough search evidence to justify separate backend tags.
- **Visible hashtag decision:** use no YouTube hashtags. Current evidence did
  not show that `#cpp`, `#autograd`, or `#deeplearning` would add qualified
  discovery beyond the title and description.
- **Rejected terms:** generic `AI`, `LLM`, `transformers`, `CUDA`, and broad
  neural-network training terms because this episode does not deliver them.
- **Primary references:** [YouTube description
  guidance](https://support.google.com/youtube/answer/12948449), [YouTube tag
  guidance](https://support.google.com/youtube/answer/146402), and [YouTube
  Search guidance](https://support.google.com/youtube/answer/9962575)

### X

- **Research date:** August 29, 2026 final re-audit
- **Tools and surfaces consulted:** official X search documentation and the
  account's existing post-performance export. Per-post keyword demand for this
  exact topic is unavailable from the owned analytics export.
- **Candidate phrases:** `automatic differentiation`, `autograd`, `C++`,
  `computation graph`, `gradient`, and `backpropagation`
- **Retained wording:** the opening starts with `Automatic differentiation`
  and explains its purpose in ordinary language. The second paragraph uses the
  exact qualified phrase `autograd engine from scratch in C++`, followed by
  `computation graph`, without mechanically repeating synonyms.
- **Hashtag decision:** use no hashtags. X can match ordinary keywords as well
  as hashtags, and no current account evidence supports spending space on a
  tag for this announcement.
- **Primary reference:** [X Search
  Recommendations](https://help.x.com/en/resources/recommender-systems/search-recommendations)

### LinkedIn

- **Research date:** August 28, 2026
- **Tools and surfaces consulted:** current official LinkedIn guidance on post
  search visibility, first-line keyword use, and hashtags. The owned dashboard
  exposes reach and follower data but not query-level LinkedIn search terms or
  reliable hashtag-attributed discovery.
- **Candidate phrases:** `automatic differentiation`, `autograd engine`, `C++`,
  `computation graph`, `backward pass`, `chain rule`, and `gradient
  accumulation`
- **Retained wording:** the first line begins with `Automatic differentiation`.
  The post then uses the exact implementation terms `autograd engine in C++`,
  `computation graph`, `backward pass`, and `gradient contribution` naturally.
- **Hashtag decision:** use no hashtags for this release. LinkedIn recommends
  testing candidate hashtags in platform search, but no query-level or follower
  evidence was available to justify the previous four-tag block.
- **Primary reference:** [LinkedIn guidance on post search
  visibility](https://www.linkedin.com/business/marketing/blog/ai-search/how-to-maximize-ai-visibility-for-your-linkedin-posts)

### Reddit

- **Research date:** August 28, 2026
- **Decision:** use no hashtags; lead with the C++ learning project and concrete
  milestone
- **Pending evidence:** verify the current r/cpp rules and the available Show
  and Tell surface immediately before any submission

## Immediate launch sequence

1. Rename or copy the final master to the exact upload filename recorded above.
2. Upload privately and wait for 4K processing to finish.
3. Apply the title, description, tags, thumbnail, playlist, language, category,
   audience, comments, and embedding settings.
4. Review the private upload at the opening, graph construction, backward pass,
   final assertions, questions, and clean tail.
5. Review automatic captions and generate concise caption-derived chapters.
6. Add Subscribe plus the complete-series playlist over only the clean tail.
7. Schedule Saturday at 11:00 AM ET only if every gate passes.
8. After publication, post the answer comment, report its direct URL, and remind
   the learner once to pin it manually.
9. Record the video URL, publication time, and comment URL in the distribution
   timeline.
10. Publish the X announcement around noon and add its navigation reply.
11. Publish the LinkedIn announcement Sunday morning and add its first author
    comment.

## Analytics checkpoints

Capture Episode 7 at approximately:

- **24 hours:** impressions, Home and Suggested CTR, views, watch time, opening
  retention, average view duration, subscribers, and traffic sources
- **72 hours:** the same metrics, compared with Episodes 4 through 6 at similar
  ages
- **Seven days:** stable long-form comparison, returning viewers, and subscriber
  conversion

This is the channel's first face-led long-form thumbnail experiment. Record the
thumbnail version and evaluate it against the channel's own object-led history.
Do not attribute performance to the face without sufficient impressions and a
controlled comparison.
