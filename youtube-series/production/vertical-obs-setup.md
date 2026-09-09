# Vertical OBS Production Setup

This is the working native-short-form configuration for *Deep Learning, All the
Way Down*.

## OBS separation

- Profile: `Shorts 9x16`
- Scene collection: `Shorts 9x16`
- Base canvas: `2160x3840`
- Output resolution: `2160x3840`
- Frame rate: `30 fps`
- Recording format: MKV, remuxed to MP4 after recording

The long-form profile and scene collection remain separate at `16:9`.

## Vertical region allocation

- Webcam region: `2160 x 1488`, positioned at `x = 0`, `y = 0`.
- Visual-aid region: `2160 x 2352`, positioned at `x = 0`, `y = 1488`.
- Together these regions fill the complete `2160 x 3840` canvas with no gap or
  overlap.
- Visual-aid assets are authored at the native `2160 x 2352` region size and
  occupy that region completely.

## Visual states

```text
Sharp
└── macOS Screen Capture reference

Cam
├── camera
└── X badge

Mic/Aux

Blurred
└── macOS Screen Capture reference
```

- `Sharp` visible: full-frame readable code.
- `Sharp` hidden: camera plus contextual blurred code.
- Composite Blur radius: `4 px`.
- Black dimming overlay: disabled.
- `Sharp` show and hide transitions: Fade, approximately `175 ms`.

The X badge is stored at
[`youtube-series/assets/x-mechaturka-badge.png`](../assets/x-mechaturka-badge.png).

The reusable southeast attention arrow is stored at
[`youtube-series/assets/attention-arrow-southeast.png`](../assets/attention-arrow-southeast.png).
Add it as an OBS Image source above the camera and visual-aid sources, then move,
scale, show, or hide it without changing the underlying scene layout.

## Editor calibration

- Dark theme for recording.
- Font size: `18 px`.
- Line height: `26 px`.
- Target capacity: `44` monospace columns, including indentation.
- Two-space indentation.
- Line numbers, minimap, breadcrumbs, folding controls, scrollbars, title text,
  editor tabs, and other nonessential chrome are hidden.
- Each recorded code shot begins at a deliberate syntactic boundary with one
  line of breathing room above it.

## Recommended hotkeys

Avoid unmodified letters, numbers, and common Command shortcuts because code is
typed during recording. Use Control+Option combinations and keep start and stop
recording distinct.

| Action | Hotkey |
|---|---|
| Start recording | `Control+Option+R` |
| Stop recording | `Control+Option+Shift+R` |
| Pause recording | `Control+Option+P` |
| Resume recording | `Control+Option+Shift+P` |
| Show `Sharp` code state | `Control+Option+C` |
| Hide `Sharp` and reveal face-focus state | `Control+Option+F` |
| Mute microphone | `Control+Option+M` |
| Unmute microphone | `Control+Option+Shift+M` |

Separate show/hide and mute/unmute commands are preferred over toggles because
their outcome does not depend on remembering the current state.

## Final validation

Record and inspect a phone-sized test containing direct-to-camera speech, a
sharp code walkthrough, the blurred face-focus state, terminal compilation, and
the resulting output. Typography and transitions are final only after the
export is immediately readable at normal phone size without zooming.
