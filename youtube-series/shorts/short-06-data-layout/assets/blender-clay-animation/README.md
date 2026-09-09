# Short 06 — revised Retro Sunset clay animation

## Pending placement correction — September 6, 2026

The creator reports that TikTok headers still cover the content. Before the next
render, move the **entire foreground down another 100 px** relative to this
15-second version, keeping the canvas and scale unchanged. Preserve dark
background behind the code and recheck the bottom margin and actual platform
placement. This correction is **not implemented in the current scene, sources,
stills or video**; the creator requested a note only, with no new render.
See the [Animations Playbook](../../../../production/animations-playbook.md)
for the authoritative pending correction and reusable production system.

This revision enlarges the code, lowers its placement and the orange background highlight, makes repeated objects uniform, and ends on the benchmark result.

## Deliverables

- `cpp-data-layout-clay-animation.mp4`: native 2360 × 2352, 24 fps, 360 frames, 15 seconds, silent.
- `preview.mp4`: 1180 × 1176 viewing copy.
- `cpp-data-layout-clay-animation.blend`: complete editable sequence with packed fonts.
- `stills/`: opening, code transition, gathering, separated arrays, arrow reveal and final result.
- `scene-verification.json`, `geometry-verification.json`, `export-verification.json`: layout, uniformity, clearance and export evidence.
- `build_animation.py`, `render_layers.py`, `finish.py`, `verify_geometry.py`: editable source and reproduction scripts.

## Requested changes

The code font is exactly 1.5 times its size in the first clay video. Its top origin is 100 pixels below the first enlarged-code preview. The blank gap before the loop is 37 pixels shorter to preserve separation from the models. Across the animation, the visible code/result bounds stay within approximately x=255–2043 and y=348–1037. The orange material highlight moves from y=1818.61 to y=1918.61 while retaining its horizontal center.

All three score assemblies are duplicates of one canonical score assembly; all three history assemblies are duplicates of one canonical history assembly. Their mesh data, local sculpture, component placement, dimensions and scale animation match within each family. Numerals are the only score geometry that differs. The prior independent screen-size adjustments are removed. Perspective and directional lighting still produce natural differences in the visible sides and highlights.

The code declarations visibly flip and slide into place, the scores lift clear of the retained histories and gather into a compact row, and the boxes land with a small bounce. There are three score labels, three history labels and exactly 45 history cards throughout. The clean clay arrow draws on between `4.36 ms` and `0.35 ms`, followed by `12.5× faster`.

The video ends at frame 360 on this benchmark result. There is no return to the code, narration, audio, title banner or added duration. The creator will handle timing in the final edit.

## Rendering and checks

Moving models are native-resolution Cycles renders with 32 maximum samples and denoising. The initial hold uses 96 samples; the settled model hold uses 256. Identical static scene states reuse the same native pixels. The upper 1050 pixels and lower 1302 pixels are rendered separately and assembled without resizing or interpolating motion. Only the viewing copy is downscaled.

The scene audit checks every frame for bounds and matching family scale/depth. Geometry checks compare world dimensions at opening, lift, crossing, gather, landing and settled poses, and check score/history clearance through the movement. The export verifier checks dimensions, frame count, frame rate, duration, audio absence, complete video decoding and the final benchmark state.

Scripts target the production workspace at `/Users/keremkazan/Documents/Codex/2026-09-05/go-t`. Construction starts from `outputs/clay-studio-lighting/retro-sunset-clay-studio.blend`; the saved animation itself is complete and editable. Native PNG caches live in `work/clay-animation-v2`. Metal kernel optimization and MetalRT are disabled for stability on this Blender installation.

This remains the creator's explicitly revised 2360 × 2352 lower visual-aid asset. The final combined vertical edit and platform composer checks are separate production steps.
