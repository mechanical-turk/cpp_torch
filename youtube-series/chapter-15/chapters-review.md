# Episode 15 chapter review — November 16, 2026

Scope: transcript-derived navigation for https://www.youtube.com/watch?v=wBB9lQnpUNU.
Source: freshly downloaded serving English ASR track, `youtube-generated.en.srt`.
The final upload is 34:09 according to the API; the local master is 34:08.967.

## Boundary evidence

Chapter boundaries use whole seconds at or just before the spoken topic transition. They do not use the script's planned timestamps.

| Chapter | Caption anchor | Evidence |
|---|---|---|
| 00:00 Introduction | 00:00:00.080 | Introduces momentum and Adam on MNIST. |
| 00:22 Smaller MNIST network | 00:00:20.640 | Fair-comparison setup leads into a smaller network at 00:22. |
| 01:01 Training configuration | 00:01:01.120 | Collect settings as constants above the epoch loop. |
| 02:59 How momentum works | 00:02:59.519 | “talk about momentum first” |
| 03:58 Implementing momentum | 00:03:58.720 | Navigate to gradient_step and write momentum_step. |
| 06:44 Momentum in training | 00:06:44.160 | Return to training and initialize velocities and momentum. |
| 08:26 Tracing SGD gradients | 00:08:27.120 | Observe gradients across the training loop; rerun SGD. |
| 10:11 First momentum run | 00:10:11.839 | Switch to momentum and rerun. |
| 11:21 Signals and gradients | 00:11:21.680 | Compare forward-pass signals and backward-pass gradients. |
| 12:40 Lowering the learning rate | 00:12:40.240 | Reduce the learning rate tenfold. |
| 13:58 Why velocity builds up | 00:13:58.320 | Constant-gradient example explains velocity buildup. |
| 14:58 Learning-rate search | 00:14:58.399 | Search between 0.1 and 1 on a log scale. |
| 18:01 How Adam works | 00:18:01.120 | Transition from momentum to Adam and its two memories. |
| 20:19 Adam's second moment | 00:20:19.600 | Second memory is a running average of squared gradients. |
| 21:45 Scaling the update | 00:21:45.039 | Use first moment divided by square root of second moment. |
| 22:41 Avoiding division by zero | 00:22:41.520 | Second moment can be zero; introduce epsilon. |
| 23:25 First Adam run | 00:23:25.520 | Wire the initial Adam implementation into training and run it. |
| 25:14 Zero-initialization bias | 00:25:14.559 | Diagnose early-step behavior using constant gradients and zero initial moments. |
| 27:15 Why bias correction works | 00:27:15.200 | Track steps and derive the correction factors. |
| 28:20 Coding bias correction | 00:28:20.960 | Pass step count and implement the two divisions. |
| 29:57 Comparing Adam and momentum | 00:29:57.039 | Inspect corrected Adam loss and accuracy against momentum. |
| 31:03 Recap | 00:31:03.120 | Wrap up and begin the recap. |

## Script comparison and technical terms

The script planned roughly 12.5 minutes; the final recording lasts 34:09. Momentum begins around 02:59 and Adam around 18:01, with substantial recorded learning-rate investigation and bias-correction explanation. The script's later batch-size-64 comparison is absent from this recording and has no chapter. The recap and next-episode discussion start around 31:03 and remain together under the final Recap chapter.

ASR renders Adam as “atom”, MNIST as “emnest” or “amnest”, ReLU as “rail” or “value”, and stochastic inconsistently. Chapter names use the intended technical spellings supported by the script and recorded implementation context. Numeric ASR errors are not reproduced as chapter claims. The zero-bias, scaling and correction labels describe the recorded lesson without claiming that a single result proves an optimizer is universally better or that lower accuracy alone proves overfitting. No caption text is edited or uploaded in this task.

## Validation

22 chapters; first is `00:00 Introduction`, last is `31:03 Recap`. All timestamps increase, all chapters are at least ten seconds, and every title is at most 28 characters and five words. No chapter exceeds five minutes; the longest interval is 3:03. Final recap lasts about 3:06. Existing description, title, tags and visibility are preserved. Dry-run inspection and live read-back are required before marking application complete.
