# Short 06: mechanical data-layout animation

An editable Blender scene and a rendered lower-screen animation for the accepted
hook: “This struct is killing performance.”

## Files

- `cpp-data-layout-mechanical-assembly.blend`: editable scene, packed fonts,
  named collections, camera, lights, models, text, and animated timeline markers.
- `cpp-data-layout-animation.mp4`: native 2160 x 2352 animation with the snap sound.
- `preview.mp4`: 720 x 784 viewing copy of the same animation.
- `score-snap-sfx.wav`: separate original sound stem, 48 kHz mono, 19 seconds.
- `stills/`: six full-resolution key frames and the render manifest.
- `storyboard.jpg`: six-frame overview.
- `build_scene.py` and `render_animation.py`: reproducible scene and render scripts.

## Placement and editing

The lower-screen render is opaque and fills 2160 x 2352 pixels. Place it at
**x=0, y=1488** in the project's **2160 x 3840** vertical composition. The upper
2160 x 1488 region is reserved for the presenter. The video contains no narrator
or presenter recording. Its duration is exactly **19 seconds at 24 fps**.

Use the Blender timeline markers to retime beats to the actual delivery.
Collections separate the player assemblies, studio, typography/evidence, and
selection/spacing annotations. Score/history parents carry the animation;
their children retain the physical geometry and labels. Font files are packed.

## Voice and gesture guide

| Frames | Time | Suggested delivery | Action |
| --- | --- | --- | --- |
| 1–60 | 0–2.50 s | This struct is killing performance. | Point to the circled history field; the first history lifts. |
| 61–112 | 2.50–4.67 s | We only need the scores. | Scores 7 and 9 are selected. |
| 113–166 | 4.67–6.92 s | Look how far apart they are. | Spread hands with the red bracket. |
| 167–241 | 6.92–10.04 s | Put them in their own array. | Bring hands together with all three scores; contact at frame 230. |
| 242–288 | 10.04–12.00 s | The histories stay over here. | Point to the retained history row. |
| 289–360 | 12.00–15.00 s | Same lookups, now under half a millisecond. | Hold on the complete measured result. |
| 361–456 | 15.00–19.00 s | But what if we need both fields? That's what I'm testing next. | Both fields for players 0 and 2 light up; cut. |

These are pacing cues for recording, not a measured narrator read. The current
repository script still contains the earlier rejected Round 10; this asset
package follows the subsequent hook and animation discussion.

## Evidence and model meaning

Three schematic players retain scores 7, 2, and 9 and all fifteen history plates
each. IDs 0 and 2 select 7 and 9 in both layouts, giving the same score sum, 16.
All three scores move into one array; all three histories remain in another.
The object proportions are schematic, not a literal byte scale. The bracket
shows selected-score separation, not memory traffic or a measured cache miss.

Displayed evidence comes from `/Users/keremkazan/code/data-layout/LOOKUP-RESULTS.md`:
4.355233 ms versus 0.347342 ms, approximately 12.54x, for 1,048,576 ordered IDs
among 4,194,304 players. The result card displays rounded times with workload
and normal -O3 / both-scalar conditions. It is static evidence, not a live timer.
The final score-plus-history question is an unmeasured next experiment.

## Rebuild

Built with Blender 5.1.2 and EEVEE, using 32 render samples. The builder expects
the standard macOS Arial and Menlo font paths. The saved blend itself is portable
because those fonts are packed. A copy of this guide is embedded in the blend
as `START HERE • animation guide`.

```sh
blender -b --python build_scene.py -- --out /absolute/output/directory
blender -b /absolute/output/directory/cpp-data-layout-mechanical-assembly.blend \
  --python render_animation.py -- --frames /absolute/scratch/frames \
  --stills /absolute/output/directory/stills
```

Every moving frame is rendered at native resolution. Exact static holds reuse
identical frames; no optical-flow interpolation or image upscaling is used.
The render manifest records that mapping. New movements or timing changes
require updating the hold mapping, or rendering the complete Blender timeline.
