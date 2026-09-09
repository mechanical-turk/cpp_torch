# Video Resolution Standard

## Required masters

- Episodes 1-5 and Shorts 1-3 retain their original resolutions.
- Episode 6 is the final exception: `2560 x 1440` (`1440p`, `16:9`).
- Every long-form episode after Episode 6: `3840 x 2160` (`2160p`, `16:9`).
- Every Short and other vertical video produced after Episode 6:
  `2160 x 3840` (`2160p`, `9:16`).

Platform covers and thumbnails remain separate assets with their own ratios.
Instagram, TikTok, X, or YouTube may transcode or downscale a submitted master;
that does not change the required source export.

## Release verification

Before upload, record the master dimensions with:

```sh
ffprobe -v error \
  -select_streams v:0 \
  -show_entries stream=width,height,r_frame_rate,codec_name \
  -of default=noprint_wrappers=1 \
  path/to/master.mp4
```

For YouTube, upload privately and do not publish until the watch page offers the
required highest quality: `1440p` for Episode 6 and `2160p` afterward. Check a
code-heavy section at ordinary desktop and mobile playback sizes in addition to
confirming the resolution label.

## Why this is the standard

The purpose is visual quality, especially the legibility of code, formulas, and
diagrams on desktop and TV. It is not treated as a direct recommendation-system
optimization. Track downstream viewer behavior separately from resolution.
