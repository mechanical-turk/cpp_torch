# Short Upload Gate

Applies to new Shorts, Reels, and TikToks prepared from September 5, 2026
onward, on every selected platform. Complete this gate before approving an
upload or marking its publishing package ready. Review the exact final export —
a script, cover image, editing timeline, or planned effect cannot establish a
pass. This gate supplements the existing copy, technical-accuracy, resolution,
and platform-crop checks.

## Four required checks

1. **The hook works on the first frame.** Inspect the first decoded video frame
   at phone viewing size, with no audio. The image or code, opening caption,
   text callout, and stickers such as red arrows and circles must already be
   visible, readable, and working together to make one hook immediately clear.
   Fail if an essential element arrives later, fades in from blank, competes
   with the others, or is obscured. Check the actual first frame, not a selected
   cover or a frame one second into playback.
2. **Annotations sustain attention throughout.** Review the whole video.
   Stickers, arrows, circles, and highlights must recur through the explanation
   and payoff, directing attention to the relevant code, change, or result.
   An opening-only sticker does not pass. Each annotation needs a clear target
   and must preserve readability.
3. **The complete export is dense, clear, and substantive.** Target 25-30
   seconds, following S14 in the short-form playbook. Measure the actual
   duration with `ffprobe`, including all tails, and review the paced delivery
   and explanation. Fail a rushed, hollow, repetitive, or unnecessarily padded
   edit. An export outside the target requires a recorded pacing rationale, not
   automatic rejection; do not pad a complete shorter lesson.
4. **The presenter keeps the video visually active.** Review motion across the
   entire export, using playback or sufficiently dense sequential frames.
   Purposeful hand gestures and interesting presenter movement must recur
   throughout and support the explanation. A static talking head with only an
   opening gesture does not pass. Annotations alone cannot satisfy this check.

## Benchmark verification prerequisite (blocking)

For a performance Short, the benchmark/production owner must verify the measured
times, ratios, comparison conditions, and attribution before upload approval.
Replace every result placeholder using the actual benchmark record and check
that narration, captions, and visuals agree. Missing or unsupported measurements
hold release, not script approval. Script writers are responsible for accurate
explanations and a clear evidence handoff, not running or verifying benchmarks.

## Audio editing prerequisite (blocking)

Also complete the
[CapCut audio editing checklist](../../youtube-series/production/short-form-playbook.md#capcut-audio-editing-checklist).
Record settings evidence or creator confirmation and the final-export listening
result in `publishing.md`. Unverified settings or audible defects hold upload
approval even when the four visual/duration checks pass. Do not infer editor
settings from exported audio metadata.

## Evidence and decision

Record a `Short upload gate` section in the release's `publishing.md` containing:

- reviewed final-file path, SHA-256, and review date;
- first-frame image reference and readability assessment;
- annotation timecodes spanning the explanation and payoff;
- exact measured export duration;
- gesture and movement timecodes across the video;
- PASS, FAIL, or UNVERIFIED for each of the four checks, with the required fix
  for any failure.

All four checks must be PASS before the upload gate passes. Missing evidence
is UNVERIFIED and holds approval. Never infer visual quality or movement from
file metadata. If the export changes, repeat the gate for the changed file;
an identical file can reuse its recorded review on another platform, alongside
that platform's crop and rendering checks.

After publication, verify the live playback against the reviewed export using
`post-publication-check.md`. Report any missed gate or rendering defect without
silently declaring the release passed or automatically deleting the post.
