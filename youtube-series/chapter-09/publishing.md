# Episode 9 Publishing Package

## Checklist plan

Stage: uploaded and public, post-upload reconciliation. Source of truth:
`chapter-09/script.md` and the recorded `aliases/02-screen-long-form/main.cpp`.
Older alternate drafts are excluded.

| ID | Plan |
| --- | --- |
| P01 | Describe only the recorded ten-value `y = 2x + 1` example, its batched training loop, and its sum and matmul backward rules. |
| P02 | Audit YouTube, X, and LinkedIn search language separately. |
| P03 | Lead with linear regression in C++; use autograd, gradient descent, matrix multiplication, and MSE where accurate. |
| P04 | Use complete YouTube backend tags, including standalone `C++`, `machine learning`, and `linear regression`. |
| P05 | Keep all copy simple, professional, natural, and free of em dashes and canned AI cadence. |
| P06 | Preserve Episode 9, the series name, and exactly one title pipe. |
| P07 | Keep only the YouTube URL in each main announcement. Put GitHub and playlist links in the reply/comment. |
| P08 | Prepare one content-specific YouTube comment about gradient accumulation. |
| P09 | Use the descriptive filename from the script and verify the final export. |
| P10 | Create and inspect a dedicated 3840x2160 thumbnail after editing. |
| P11 | Inspect the exact final video, sound, code legibility, and duration. |
| P12 | Verify 2160p, comments, playlist, and end-screen elements after upload. |
| P13 | Derive chapters from final captions and the edited transitions. |
| P14 | Keep X, LinkedIn, Reddit, and a possible Short as separate distribution decisions. |
| P15 | Synchronize the public source and README with Episode 9 before sharing GitHub. |
| P16 | Keep public fields isolated and parser-safe. |
| P17 | Score only verified evidence. |
| P18 | Run post-publication checks and report every completed action with a direct URL. |

## Release facts

- Exact upload filename: `cpp-linear-regression-autograd-gradient-descent.mp4`
- Example: ten inputs from `0` through `9`
- Targets: `y = 2x + 1`
- Forward pass: `inputs.matmul(weights) + bias`
- Loss: mean squared error
- Backward rules added: matrix multiplication and sum
- Training method: full-batch gradient descent
- Initial weight and bias: `0`, `0`
- Verified learned weight and bias: `2`, `1`
- Final export: `aliases/04-final-cuts/ep09/cpp-linear-regression-autograd-gradient-descent.mp4`
- Final export SHA-256: `019c592758824aeb2d94178e8cc587cc0625831ec655dd4dca78db45f6d31e53`
- Final media: 3840x2160, 30 fps, H.264 video, stereo AAC audio, 19:52.46
- Thumbnail: `chapter-09/assets/thumbnail.png`, 1672x941; custom thumbnail confirmed by API
- YouTube URL: https://www.youtube.com/watch?v=h3p_rkzDPys
- Live title: `Linear Regression from Scratch in C++ | Deep Learning, All the Way Down #9`
- Published: September 14, 2026 at 9:00:22 AM ET
- YouTube state: public and processed
- Captions: English automatic track downloaded to `captions.en.srt`; some technical terms, including matmul, are misrecognized
- Chapters: 18 caption-derived timestamps published and read back on September 14; source is `chapters.txt`
- Public source: Episode 9 checkpoint [656f826](https://github.com/mechanical-turk/deep-learning-all-the-way-down/commit/656f826ae857aa45c0f2ee7235f3654aa0597019); README update [2c1b9f9](https://github.com/mechanical-turk/deep-learning-all-the-way-down/commit/2c1b9f9908f37432528681a13c4acac3e4ba0025), both pushed to main
- Studio check: 4K complete; public; no displayed notices; not age-restricted; comments On/Anyone; Basic moderation retained; Newest-first sorting saved
- End screen and public playback: incomplete because Chrome disconnected before the end-screen editor opened

The recorded program compiles, passes its assertions, and learns the expected
weight and bias.

## SEO decisions

Research date: September 13, 2026.

### YouTube

- Primary phrase: `linear regression from scratch in C++`
- Supporting terms: gradient descent, autograd, backpropagation, matrix multiplication, mean squared error, weight, bias
- Comparable wording checked: [Linear Regression From Scratch Using Gradient Descent](https://www.youtube.com/watch?v=vmS3Z70hyyQ) and [Linear Regression FROM SCRATCH](https://www.youtube.com/watch?v=Jj7WD71qQWE)
- Visible hashtags: none
- Unavailable: search volume, autocomplete, and Episode 9 query data

### X

- Primary phrase: `C++ Tensor`
- Supporting terms: linear regression, autograd, matrix multiplication, sum backward, gradient descent
- Evidence: prior series-announcement structure and standard terminology in [Autograd for Torch](https://blog.x.com/engineering/en_us/topics/infrastructure/2015/autograd-for-torch)
- Hashtags: none; the technical terms fit naturally in the post
- Unavailable: useful current comparable X posts and composer-preview evidence

### LinkedIn

- Primary phrase: `C++ linear regression`
- Supporting terms: Tensor, autograd, matrix multiplication, mean squared error, weight, bias
- Comparable wording checked: [Linear Regression from Scratch in Python and C++](https://www.linkedin.com/posts/v-deviprasad-reddy_machinelearning-artificialintelligence-activity-7417090602380574720-46bo) and [Linear Regression in C++ with LibTorch](https://www.linkedin.com/posts/priyanthan-theverasa-632975107_github-priyanthan11simple-lr-model-this-activity-7372128357968359424-AGYM)
- Hashtags retained: `#MachineLearning`, `#CPlusPlus`, `#LinearRegression`
- Rejected: broad `#AI` and large hashtag blocks

## Final title

```text
Linear Regression from Scratch in C++ | Deep Learning, All the Way Down #9
```

## YouTube description

The following description includes the chapters verified against the recorded captions.

```text
Our C++ Tensor can now train a linear regression model from end to end.

In Episode 9 of Deep Learning, All the Way Down, we build a batched linear model with matrix multiplication, calculate mean squared error, run backpropagation, and update the weight and bias with gradient descent.

The example uses ten inputs from 0 through 9. Their targets follow y = 2x + 1. The weight and bias both start at zero, and training recovers a weight of 2 and a bias of 1.

To make the training loop work, we add backward rules for matrix multiplication and sum. We also clear parameter gradients between training steps and rebuild the computation graph after every update.

Covered in this episode:

• batched linear regression in C++
• matrix multiplication for the forward pass
• mean squared error
• gradient descent
• autograd and backpropagation
• matrix multiplication backward
• sum backward
• updating the weight and bias

Source code:
https://github.com/mechanical-turk/deep-learning-all-the-way-down

Complete series:
https://www.youtube.com/playlist?list=PLZSg76FHvdTw

Chapters:
00:00 Introduction
00:18 Linear forward pass
01:14 Training and gradients
02:21 Reset parameter gradients
03:13 Preserve leaf gradients
04:41 Gradient descent step
05:54 Index the weight column
06:44 Update weights and bias
07:33 Build the training loop
09:32 Matmul backward
10:33 Parents and dimensions
11:28 Map matrix indices
12:44 Dot products and gradients
14:31 Apply the product rule
15:53 Sum backward
16:52 Fit a straight line
18:38 Run linear regression
19:14 Recap
```

The source link now points to a public repository containing Episode 9's code and README entry.

## Suggested tags

```text
linear regression, linear regression from scratch, C++ linear regression, linear regression in C++, C++, C plus plus, cpp, machine learning, C++ machine learning, gradient descent, gradient descent from scratch, autograd, autograd from scratch, automatic differentiation, automatic differentiation in C++, backpropagation, matrix multiplication, matmul backward, sum backward, mean squared error, MSE loss, tensor library, deep learning from scratch
```

Tag length: 449 characters.

## YouTube first-comment candidate

Draft only. The September 14 API check found no comments. No comment was posted;
repeat the duplicate check if this candidate is selected for publication.

```text
The easy mistake in matrix multiplication backward is replacing a gradient instead of adding to it. One matrix value can contribute to several outputs, so every path back to that value has to count. That is why both updates use +=.

Once transpose exists, would you keep these explicit loops for clarity or rewrite the rule as two matrix multiplications?
```

No GitHub link. No answer key. No automatic pin requirement.

## X announcement

```text
Our C++ Tensor can finally train a model.

In Episode 9 of Deep Learning, All the Way Down, I add backward rules for matrix multiplication and sum. Then I start the weight and bias at zero and use gradient descent to recover y = 2x + 1.

https://www.youtube.com/watch?v=h3p_rkzDPys
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
Our C++ Tensor can now train a linear regression model from end to end.

In Episode 9 of Deep Learning, All the Way Down, I connect the complete training loop to our autograd engine. Matrix multiplication produces the predictions, mean squared error gives us one loss, and backpropagation sends gradients back to the weight and bias.

The example starts with both parameters at zero and learns the line y = 2x + 1 from ten simple values.

https://www.youtube.com/watch?v=h3p_rkzDPys

#MachineLearning #CPlusPlus #LinearRegression
```

### LinkedIn first author comment

```text
Source code:
https://github.com/mechanical-turk/deep-learning-all-the-way-down

Complete series:
https://www.youtube.com/playlist?list=PLZSg76FHvdTw
```

## Reddit decision

Prepare a separate milestone post after the Episode 9 source is public. Do not
paste the YouTube announcement into Reddit. Lead with the first complete model
trained by the C++ Tensor and autograd engine, put GitHub before YouTube, and
end with one concrete implementation question. Recheck the chosen subreddit's
rules before posting.

## Separate Shorts plan

Do not crop this episode into a Short. Our current Shorts track focuses on
performance, hardware, systems, and benchmarks. Any autograd Short needs its
own hook, script, vertical visual, and upload gate.

## Settings and release checks

- Public, not made for kids
- English; Science & Technology
- Comments On for Anyone
- Complete-series playlist
- Subscribe plus complete-series playlist end-screen elements
- Approximately five clean seconds after the sign-off
- Dedicated 3840x2160 thumbnail checked at feed size
- Public 2160p playback before release
- Generated captions reviewed for technical terms
- Chapters derived from final captions; begin `00:00 Introduction` and end `Recap`
- X and LinkedIn composer previews verified before posting

## Short upload gate

N/A. This package covers long-form video only.

## Distribution and follow-through

- YouTube: public since September 14, 2026 at 9:00:22 AM ET
- X: publish after checking the YouTube composer card; the normal one-hour window has passed, so do not delay it for a new arbitrary slot
- LinkedIn: next weekday from 9:00 to 10:30 AM ET, at least one day after X
- Reddit: next qualified Sunday window after the source and tailored post are ready
- GitHub: recorded checkpoint and Episode 9 README row/summary are public; Episode 10 is marked Work in progress
- Post-publication: run all checks, avoid duplicate comments and replies, report direct URLs, and update the timeline
- Analytics: capture 24-hour, 72-hour, and seven-day long-form CTR, traffic, retention, watch time, and subscriber data

## Checklist audit

| ID | Status | Points | Remaining work |
| --- | --- | ---: | --- |
| P01 | PASS | 10/10 | Recorded captions confirm the ten-point line, complete training loop, backward rules and recovered parameters; current source reproduces the result. |
| P02 | PARTIAL | 7.5/15 | X platform evidence remains limited. |
| P03 | PASS | 10/10 | Current keywords match the recording. |
| P04 | PASS | 8/8 | Tags and platform hashtag decisions are documented. |
| P05 | PASS | 10/10 | Public copy passes the language rules. |
| P06 | PASS | 5/5 | Correct title and series identity. |
| P07 | PARTIAL | 2.5/5 | The verified watch URL is present; composer previews remain unchecked. |
| P08 | PASS | 5/5 | Useful first comment and navigation replies are prepared. |
| P09 | PASS | 4/4 | The final master exists under the exact filename and has a recorded SHA-256. |
| P10 | PARTIAL | 2/4 | A custom thumbnail is live and its local dimensions are verified; small-screen inspection remains pending. |
| P11 | PARTIAL | 3/6 | Dimensions, duration, codecs, channels, size, and hash are verified; full playback and subjective sound review remain pending. |
| P12 | PARTIAL | 1.5/3 | Public, 4K complete, playlist, comments and audience verified. Newest sorting saved; end screen and public 2160p playback remain unverified after Chrome disconnected. |
| P13 | PARTIAL | 2/4 | Eighteen chapters derived from downloaded captions are live and valid. Automatic captions misrecognize technical terms such as matmul; no caption correction was uploaded. |
| P14 | PASS | 3/3 | Distribution surfaces are separated correctly. |
| P15 | PARTIAL | 1/2 | Recorded code checkpoint 656f826 and README episode row/summary 2c1b9f9 are pushed; both programs pass. Older Implementation status/Direction prose still describes earlier milestones, preserved under the narrow README-update rule. |
| P16 | PASS | 2/2 | The verified watch URL replaced every public placeholder. |
| P17 | PASS | 2/2 | Unknowns remain unverified. |
| P18 | PASS | 2/2 | The post-publication handoff is explicit. |

## Critique

The copy now matches the episode that was actually recorded: ten simple input
values, `y = 2x + 1`, a batched linear model, sum backward, matrix multiplication
backward, gradient descent, and the recovered weight and bias.

The remaining checks are technical caption corrections, end-screen elements,
public 2160p playback, composer previews and full audiovisual review. The
19:52 runtime exceeds the standing 10-15 minute target. The public source,
chapter block, playlist, metadata and comment settings are verified.

## Final score

- Score: 80.5/100
- Stage: uploaded and public, post-upload reconciliation
- Copy: aligned with the current script and updated with the verified watch URL
- Upload: complete; post-upload verification remains partial
- Next action: reopen Chrome and Codex to verify the end screen and public playback; confirm existing announcement URLs before posting duplicates

**Decision: public upload confirmed; complete the remaining post-upload checks.**
