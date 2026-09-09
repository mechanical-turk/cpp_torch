# Short 06 — approved Retro Sunset clay animation

The creator approved the clay studio still and authorized this full sequence. The animation uses that editable Blender scene, including its camera, sculpted objects, procedural materials, directional studio lighting and clean ivory arrow.

## Deliverables

- `cpp-data-layout-clay-animation.mp4`: native 2360 × 2352, 24 fps, 456 frames, 19 seconds, silent.
- `preview.mp4`: 1180 × 1176 viewing copy.
- `cpp-data-layout-clay-animation.blend`: complete editable sequence with packed fonts.
- `stills/`: opening, code transition, gathering, separated arrays, arrow reveal, approved result and final code.
- `scene-verification.json`, `export-verification.json`: composition, counts, frame maps and export checks.
- `build_animation.py`, `render_layers.py`, `finish.py`: reproduction scripts.

## Sequence

The opening shows three interleaved score/history pairs. At roughly 6.6 seconds, the changed code declarations flip and slide into place with brief mint underlines. The gold scores lift above the histories, gather into a dense row and settle with a restrained bounce. The navy cradles retain all fifteen cards each. The timing comparison appears at 12 seconds: coral `4.36 ms`, the clean clay arrow drawing on, mint `0.35 ms`, then `12.5× faster`. The updated code returns at 15 seconds.

The final physical arrangement is exactly the approved still's pose. Its original native pixels are reused for the settled model hold and full result hold. There are no title banners, captions, narration or sound. Code uses ivory, lilac, aqua and amber syntax colors.

## Rendering and reproduction

All moving poses are native-resolution Cycles renders. Static holds reuse identical scene states. The upper 1000 pixels and lower 1352 pixels are rendered separately and assembled without resizing or motion interpolation. A transparent code/result layer is composited over the native background. Only the viewing copy is downscaled.

Moving model frames use 32 maximum samples, denoising, a one-pixel filter and reduced ambient-occlusion sampling. Their reference comparison against a 96-sample native render measured approximately 0.60 RGB code values of mean error out of 255; 99% of channel differences were at most three values. The initial hold uses 96 samples, and the approved settled hold retains its original 256-sample render. The editable scene defaults to a conventional full-frame 96-sample rerender.

Scripts currently target the production workspace at `/Users/keremkazan/Documents/Codex/2026-09-05/go-t`. The build starts from `outputs/clay-studio-lighting/retro-sunset-clay-studio.blend`. The layer renderer caches native PNGs in `work/clay-animation`, and the finisher reuses those caches to assemble and verify the exports. Metal kernel optimization and MetalRT are disabled for stability on this Blender installation.

The canvas retains the creator's explicit 2360 × 2352 revision and safe placement. This is the lower visual-aid animation for the final edit. Platform-composer release checks are outside this asset render.
