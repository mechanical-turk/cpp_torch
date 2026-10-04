# Edit Playbook: DaVinci Resolve, Speech Cuts, Audio, and 4K Export

Read this when the creator asks to edit recordings, remove silence, improve
dialogue audio, change playback speed, or export a finished Resolve timeline.
This procedure was established while editing Episode 13 on 2026-10-03.
The exact episode results and historical file locations are in the
[Episode 13 editing record](../../docs/logs/ep13-editing-2026-10-03.md).

Read [Video Resolution Standard](video-resolution-standard.md) and
[Visual Asset Guidelines](visual-asset-guidelines.md) for dimensions and upload
filenames. This playbook covers long-form Resolve editing. The separate
[Short-Form Playbook](short-form-playbook.md) owns the creator's CapCut audio
defaults for Shorts; do not silently replace those with these settings.

## 1. Establish the current stage before changing anything

1. Inspect the active Resolve project and timeline. Record their actual names,
   timeline frame rate, start timecode, duration, track count, and media paths.
2. Determine whether this is a fresh assembly, an automatic rough cut awaiting
   review, or the creator's finished manual edit. A finished manual edit is the
   source of truth. Do not regenerate its speech cuts or reorder its clips.
3. Verify the requested source and output folders exist. A folder selected for
   project storage does not necessarily contain a `.drp`: Resolve normally stores
   projects in its project library. Export a `.drp` backup when appropriate and
   record its real location instead of assuming the project is a folder of files.
4. Save the project. Before a replacement timeline or consequential transformation,
   preserve a duplicate timeline or project backup. Use new names for generated
   timelines and XML files. Do not delete a previous project to implement a reset.
5. Record whether speed has already been applied. The Episode 13 final file was
   sped up externally; that does not prove its Resolve timeline was sped up.
6. Do routine authorized work directly. If the creator has finished editing and
   asks for audio cleanup and export, continue from that edit. Do not restart the
   whole workflow or require them to approve each routine step again.

Keep an episode work directory for manifests, XML snapshots, cut decisions,
analysis logs, audio intermediates, and resumable render pieces. Use a real final
output directory for deliverables. Record the chosen paths in the episode record.
Do not hard-code Episode 13's paths or frame counts into a new episode.

## 2. Inspect the original recordings directly

Probe every source used in the edit, rather than inferring media properties from
Resolve's viewer, proxy files, or an XML sequence format:

```sh
ffprobe -v error -show_entries \
  stream=index,codec_type,codec_name,width,height,r_frame_rate,sample_rate,channels,duration:format=duration \
  -of json "$SOURCE"
```

Record resolution, rational frame rate, audio stream count, channels per stream,
and duration. Confirm mixed frame rates or dimensions before assuming one uniform
timeline. Episode 13's raw media was native 3840×2160 at 30 fps even though its
exported XML reported a 1080p sequence. Upscaling a 1080p rendered intermediate
would have discarded the original detail; our export read the original 4K files.

For this recording setup, the original three audio streams were:

| Original Resolve track | Contents | FFmpeg audio selector |
| --- | --- | --- |
| A1 | Combined speech and keyboard | `0:a:0` |
| A2 | Isolated speech | `0:a:1` |
| A3 | Keyboard strokes | `0:a:2` |

Verify this mapping with short listening samples for each new recording setup.
These are zero-based **audio stream** selectors, not absolute stream IDs and not
necessarily the track numbers in an exported XML. One stream can have multiple
channels. Resolve may export misleading `sourcetrack/trackindex` values; in the
Episode 13 final XML they did not reliably identify the isolated voice stream.
We explicitly used `0:a:1` after verifying the original media mapping.

After deleting combined A1, isolated speech becomes timeline A1 and keyboard
becomes timeline A2. The raw file's speech stream remains `0:a:1`. Never select
the combined track merely because the creator now says “first audio track.”
Never sum the combined and isolated speech tracks: that duplicates the voice.

## 3. Assemble a fresh timeline in filesystem date order

Only perform this section for a fresh assembly or an explicitly requested reset.

1. Inventory all intended recordings and save a manifest with filename, full path,
   modification date, creation date, duration, frame rate, and audio mapping.
2. Sort by filesystem modification time, oldest first, with filename as a stable
   tie-breaker. This was the verified order for Episode 13. Compare creation-date
   order as a cross-check; both agreed for all 95 original clips.
3. If the creator's visible Finder date sort differs, reconcile the actual sort
   column and direction before assembly. Never assume lexical filename order,
   XML file-definition order, or Media Pool insertion order is the requested order.
4. Create a new clearly named Resolve project when requested. Set timeline rate
   from the actual sources and dimensions from the resolution standard.
5. Set timeline start timecode to `00:00:00:00`. Resolve's `01:00:00:00` default is
   a timecode offset, not one hour of empty footage. Check the start timecode in
   the timeline's settings and confirm the first clip begins at frame zero.
6. Place full original clips end-to-end on V1 and align their three audio tracks.
   Keep all three tracks when the creator asks to start with all three. The final
   successful Episode 13 reset did so, superseding earlier attempts to delete A1.
7. Verify the first and last filenames against the manifest, then inspect several
   boundaries in the middle. Assert there are no unintended gaps or overlaps and
   every video/audio boundary aligns. Compare total timeline frames with the sum
   of source clip frame spans.
8. Preserve this uncut timeline before creating the speech-cut version.

For XML assembly, resolve every `<file id="…">` reference from the full file
definitions containing `pathurl`. Decode URL escaping when reading local paths.
Reorder clip instances independently on V1 and each audio track using the same
manifest. Rewrite sequential `start`/`end`, preserve source `in`/`out`, and repair
link references and one-based `clipindex` values. A repeated file reference must
still have an accessible full definition in the generated document.

## 4. Detect speech conservatively, rather than cutting on volume

Amplitude-only auto-editor cuts removed minutes of real, quiet speech during
the earlier attempts. Do not repeat that configuration. Exact digital zero also
proved unusable: the isolated dialogue contained no zero runs lasting one frame.
`0 dBFS` means the digital full-scale ceiling, not silence. A quiet microphone's
noise floor can remain nonzero while nobody speaks.

The successful rough cut used the free
[Silero VAD project](https://github.com/snakers4/silero-vad), installed locally,
to classify speech. It was a Python tool, not a plugin installed into Resolve.
It produces speech intervals, not a transcript or an infallible speech boundary.
Technical jargon and quiet delivery still require review.

1. Reconstruct an isolated dialogue WAV in **the assembled timeline's order**.
   Use the verified original speech stream. Extract source ranges using each
   clip's source `in` and timeline duration. Use 48 kHz mono PCM for the assembly.
2. For gaps, insert the exact amount of silence. Pad or truncate each extracted
   audio slice to its exact expected sample count. At 30 fps and 48 kHz there
   are exactly 1,600 samples per frame. For other rates, use cumulative rational
   boundaries so rounding does not accumulate.
3. Resample the assembled dialogue to 16 kHz mono, little-endian float32:

   ```sh
   ffmpeg -v error -i "$SPEECH_WAV" -ac 1 -ar 16000 -f f32le "$SPEECH_F32"
   ```

4. Use an isolated Python environment. Episode 13 used Python 3.12.8,
   `silero-vad==6.2.3`, and installed Torch 2.14.1. Inspect an existing environment
   before installing again. These versions describe the run; verify compatibility
   if recreating the environment later.
5. Call the detector with the exact conservative starting settings below:

   ```python
   import array
   import torch
   from silero_vad import load_silero_vad, get_speech_timestamps

   torch.set_num_threads(1)
   samples = array.array("f")
   with open(speech_f32_path, "rb") as f:
       samples.frombytes(f.read())
   speech = get_speech_timestamps(
       torch.tensor(samples), load_silero_vad(),
       sampling_rate=16000,
       threshold=0.35,
       min_speech_duration_ms=100,
       min_silence_duration_ms=750,
       speech_pad_ms=270,
   )
   ```

6. Save the original detector intervals in sample units. Convert each interval
   to timeline frames: `lo = floor(start_sample / 16000 * fps)` and
   `hi = ceil(end_sample / 16000 * fps)`. Clamp to the original timeline bounds.
   Merge overlapping or touching padded intervals. Preserve their original
   offsets and assign consecutive destination starts.
7. The 750 ms silence setting retains brief pauses; 270 ms padding protects
   word beginnings and endings. Do not lower padding or increase aggressiveness
   just to achieve a target duration. Preserve useful silent visual actions,
   intentional code-reading time, and an end-screen hold through manual review.
8. Report retained/removed duration, number of intervals, and settings. Compare
   against known speech passages, especially soft phrases and word endings.
   A plausible runtime reduction alone does not establish that speech survived.

## 5. Apply the same cut intervals to video and every audio track

For each original clip with timeline range `[a, b)` and source start `cin`, and
each retained interval with original range `[k.offset, k.offset + k.dur)`:

```text
lo = max(a, k.offset)
hi = min(b, k.offset + k.dur)
if hi <= lo: no intersection; skip
new_start = k.start + lo - k.offset
new_end   = new_start + hi - lo
new_in    = cin + lo - a
new_out   = cin + hi - a
```

Clone each intersecting clip and assign those values. Process the same retained
intervals on V1 and all three audio tracks. Generate unique clip IDs, update
every linked clip reference and index, retain full file definitions, and update
sequence name/duration. Import as a new timeline, preserving the uncut version.

Before import, assert all spans are positive, source `out-in` equals timeline
`end-start`, destination clips are contiguous where expected, links resolve,
video/audio boundaries match, and every track reaches the same final frame.
After import, inspect real playback for sync and missing media.

Let the creator finish the editorial pass. Their manual cuts supersede the
automatic cut list. Once they report completion, export a fresh snapshot of
that exact timeline; do not render from the earlier automatic XML.

## 6. Snapshot and validate the creator's finished timeline

1. Save the project and export the active finished timeline as Final Cut Pro 7
   XML (`xmeml`) where supported. Use a descriptive versioned filename.
2. Parse the exported sequence; do not assume the filename proves which timeline
   it contains. Check its name, duration, track count, source ranges, and clip count
   against Resolve. Preserve this snapshot unchanged.
3. Probe every referenced original video source directly again. Do not treat the
   XML's sequence sample-characteristics dimensions as the raw resolution.
4. Verify whether the timeline contains only straight cuts with equal source and
   destination frame spans. The external fallback below was valid for Episode 13's
   straight-cut edit. It does not reproduce arbitrary Resolve grading, titles,
   transitions, transforms, effects, compositing, or retime curves.
5. If those features exist, render through Resolve or a workflow that actually
   preserves them. Do not flatten an XML to source snippets and claim full fidelity.

## 7. Rebuild and improve the final dialogue

1. Read the dialogue track's **finished** clip ranges and order from the latest
   XML. Extract from the verified original isolated speech stream, rather than
   blindly trusting XML source-track numbering.
2. Assemble mono 48 kHz PCM with exact sample alignment as in section 4. Keep an
   unprocessed WAV. The final mix excludes the duplicate combined stream and
   isolated keyboard stream. Removing keyboard A3 cannot remove keyboard leakage
   already recorded in the speech microphone.
3. Check representative audio, original peaks, and loudness. Use conservative
   processing; do not add heavy denoising or a noise gate by default.
4. Episode 13 used this filter chain before normalization:

   ```text
   highpass=f=70,
   acompressor=threshold=0.125:ratio=2:attack=15:release=180:makeup=1
   ```

   The high-pass removes low rumble; the gentle 2:1 compression controls voice
   dynamics. Listen for thin voice, pumping, breath emphasis, and clipped words.
5. Measure this chain plus `loudnorm=I=-16:TP=-1.5:LRA=9:print_format=json` using
   a first pass to a null output. Save stderr's measured JSON:

   ```sh
   ffmpeg -v info -nostats -nostdin -i "$DIALOGUE_WAV" \
     -af 'highpass=f=70,acompressor=threshold=0.125:ratio=2:attack=15:release=180:makeup=1,loudnorm=I=-16:TP=-1.5:LRA=9:print_format=json' \
     -f null - 2> "$ANALYSIS_LOG"
   ```

6. Run the same chain again with the first-pass values inserted into loudnorm:
   `measured_I`, `measured_TP`, `measured_LRA`, `measured_thresh`, and `offset`
   (the analysis's `target_offset`). Episode 13 used `linear=false`, output at
   48 kHz, and `pcm_s24le` for its lossless dialogue master. Never reuse its
   measured values on a different edit or episode.
7. Keep the second-pass log. Requested -16 LUFS is a processing target, not a
   claim about the result. Measure the actual final AAC after export; encoding
   and retiming can change loudness and true peaks.

## 8. Apply 1.07× speed once, with pitch preserved

The creator explicitly requested 107% playback speed. Treat 1.07 as a multiplier,
not a 107% increase. Apply it to the complete finished picture and dialogue
together, maintaining sync. Do not speed up only V1 or leave audio at 1×.

Prefer a verified native Resolve workflow when it preserves the edit and closes
gaps correctly. If applying speed per clip, verify linked audio, pitch correction,
ripple behavior, and boundary continuity. Record native settings only when actual
UI state or playback confirms them.

For the external straight-cut fallback, retime the entire assembled edit:

```text
video: setpts=(PTS-STARTPTS)/1.07,fps=30
audio: atempo=1.07
```

This retains the 30 fps output rate and preserves audio pitch. Expected new
duration is `old_duration / 1.07`, with frame/audio rounding. Calculate and compare
the result before claiming completion. If render must be stopped, stop the actual
render process/job, confirm it has stopped, then correct speed and restart under
a new output filename. Do not leave two competing renders running.

## 9. Export native 4K

For supported long-form sources, use 3840×2160 per the resolution standard.
Episode 13 used MP4, H.264 High profile, yuv420p, 30 fps, AAC mono 48 kHz at
256 kb/s, and `+faststart`. Its VideoToolbox bitrate request was 60 Mb/s; the
measured final average was lower. A requested bitrate is not the measured bitrate.

First try Resolve's native Deliver workflow when reliable. Verify actual saved
output path, filename, dimensions, codec, audio mix, and speed. During Episode 13,
accessibility value changes sometimes appeared in the accessibility tree without
changing the visible Qt controls. Clicking or setting a value is not proof it
took effect. Inspect the real UI and the rendered file.

### External fallback used for Episode 13

This fallback reconstructs a validated straight-cut timeline from original media.
It applies audio processing and speed to the **export**, not necessarily to the
Resolve project. State that distinction in the handoff.

1. Render each V1 clip's exact source range into a numbered native 4K video-only
   MP4. Seek to `source_in / fps`, request exactly `end-start` frames, and use
   matching codec/rate/pixel format/timebase for all pieces. We used two workers,
   `-hwaccel videotoolbox`, `-c:v h264_videotoolbox`, `-b:v 60000000`,
   `-profile:v high`, `-pix_fmt yuv420p`, `-r 30`, and
   `-video_track_timescale 15360`.
2. Count each piece's packets with `ffprobe -count_packets` and require the exact
   requested video-frame count. Reuse an existing piece only if it validates and
   its source/cut/encode settings still match. Invalidate caches after edit changes.
3. One Episode 13 source EOF was one decoded frame short. We added
   `tpad=stop_mode=clone:stop_duration=0.1` before the exact `-frames:v` limit,
   holding the last image when necessary. Document any such repair; it is for a
   known source-end rounding issue, not a way to conceal missing footage.
4. Write a concat-demuxer list in finished timeline order. Each entry names one
   piece, e.g. `file 'render-parts/0000.mp4'`. Handle quoting correctly if paths
   contain apostrophes. Use fixed generated names to simplify the list.
5. Encode the concatenated picture with the processed dialogue and global speed:

   ```sh
   ffmpeg -v error -nostdin -hwaccel videotoolbox \
     -f concat -safe 0 -i "$PARTS_LIST" -i "$DIALOGUE_MASTER" \
     -map 0:v:0 -map 1:a:0 \
     -vf 'setpts=(PTS-STARTPTS)/1.07,fps=30' -af 'atempo=1.07' \
     -c:v h264_videotoolbox -b:v 60000000 -profile:v high -pix_fmt yuv420p \
     -c:a aac -b:a 256k -movflags +faststart \
     -progress "$PROGRESS_LOG" "$OUTPUT_MP4"
   ```

6. Ensure sufficient disk for original-speed pieces, audio, and final MP4. Avoid
   changing encoding strategy mid-render. Poll the progress file, give brief
   updates, wait for exit zero and final mux completion, and then verify the file.
   An output file appearing on disk is not evidence that export finished.

This was a two-encode fallback, not a lossless video workflow. Do not describe
its MP4 as lossless or assume the 60 Mb/s request guarantees visual fidelity.
Review code readability in the actual output.

## 10. Verify and hand off the actual file

1. Probe the completed file:

   ```sh
   ffprobe -v error -show_entries \
     stream=index,codec_name,width,height,r_frame_rate,nb_frames,duration,sample_rate,channels:format=duration,size \
     -of json "$OUTPUT_MP4"
   ```

2. Require the intended dimensions, rate, codecs, audio sample rate and channel
   count. Compare final duration with the latest edit duration divided by 1.07.
   Compare picture/audio durations; investigate drift beyond frame/sample rounding.
3. Measure the final encoded audio, not just its WAV intermediate:

   ```sh
   ffmpeg -v info -nostats -nostdin -i "$OUTPUT_MP4" -vn \
     -af ebur128=peak=true -f null - 2> "$FINAL_AUDIO_LOG"
   ```

   Read the final summary for integrated LUFS, loudness range, and true peak.
   Check for clipping and decode errors. Do not claim perfect subjective sound
   quality from numerical measurements.
4. Preview the start, end, representative quiet and loud dialogue, code-heavy
   sections, and several cut boundaries for word loss, sync, pitch, readable code,
   and artifacts. Record any checks not actually performed as unverified.
5. Report the final path, resolution, speed, runtime, audio work, and material
   limitations. Link the real file using an absolute local path. Reveal it in
   Finder when requested, for example `open -R "$OUTPUT_MP4"` on macOS.
6. Preserve source recordings, latest project/XML snapshot, manifest, cut list,
   and settings logs. Do not delete intermediates before the export is verified.
7. Before an authorized upload, create the descriptive upload filename required
   by the visual-asset standard and update the release package. Export completion
   does not mean upload or publication. Follow the existing publishing gate for
   private upload and required YouTube 2160p processing verification.

## Completion checklist

- [ ] Correct stage and latest creator edit identified; backup preserved.
- [ ] Raw source dimensions/rate and isolated voice stream verified.
- [ ] Fresh assembly uses confirmed filesystem date order and starts at zero.
- [ ] Speech cuts use conservative VAD and preserve synchronization.
- [ ] Creator's final manual cuts are represented in the export snapshot.
- [ ] Duplicate combined speech and keyboard streams excluded from dialogue mix.
- [ ] Audio processing logged; final AAC loudness/peaks measured.
- [ ] 1.07× applied exactly once to picture and audio; pitch preserved.
- [ ] Export finishes successfully; actual 4K/rate/duration/sync verified.
- [ ] Preview checks and evidence limits recorded; actual final file handed off.

Mark irrelevant earlier assembly steps as not applicable when exporting an
already-finished timeline. Do not rerun them merely to complete this checklist.
