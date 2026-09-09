# Short 07 — revised clay still

Single-image look development, September 8, 2026. This is not a revised animation export.

The requested source first changed from 2360 × 2352 to a proposed 2160 × 2282, preserving the +6% taller aspect ratio at the actual final width. The subsequent request adds another 6% height while retaining width: this still is 2160 × 2420 (rounded to even pixels). Rendered at native dimensions, with no resizing or vertical pixel stretch.

`render_still.py` loads the existing native Blender scene, preserves the worker/counter identities, constructs a larger merged clay pulse, revises the materials and illumination, and reflows the code at 180 font units rather than the previous 105. Typography uses flat camera-facing vector outlines with emission colors and no depth of field, blur, or texture. The visible code bounds are checked against the physical assembly before rendering.

The generated PNG and packed Blender scene live in this directory. Logs and diagnostics stay in `_render/`. Generated files are ignored by Git.

This still depicts a schematic packed-layout request in flight. It can establish texture, lighting, typography, proportions, and pulse form. Momentum, resistance, deforming path motion, final alignment-code reflow, and narration synchronization require the later animation pass and are not verified by a still.

## Height correction

The subsequent request reduces the 2420 px height to 95%, rounded to even video dimensions: **2160 × 2300**. `short-07-clay-study-2160x2300.png` trims 60 background pixels at each vertical edge of the existing native render. All retained RGB pixels match exactly; no GPU rerender or resampling was needed. This is the latest still for review.

## Code clearance correction

The creator approved the 2160 × 2300 canvas and model scale, but supplied `youtube-series/assets/all-platforms-safe-zone-template-1080x1920.png` to correct code clearance. The actual RGBA template is scaled exactly 2× over a 2160 × 3840 master, with the animation at (0, 0), at native size. Its safe rectangle is x=120–1872, y=440–2840. The previous code crossed the top and right boundaries.

`fit_safe_zone.py` changes only the native Blender code: font units 180 → 150 (16.7% smaller), x origin 200, cropped-canvas first baseline 590, row spacing 125. Visible code bounds become x=210.40–1706.46, y=502.69–980.41, leaving about 63 px above and 166 px on the right before the template boundary. The syntax colors, clay geometry, lighting and background setup remain the same.

`compose_safe_zone.py` replaces the upper native render region, applies the approved 60 px top/bottom crop, and verifies that retained lower pixels match the prior approved image exactly. The updated still is `short-07-clay-study-safe-code-2160x2300.png`. `safe-zone-before-2160x3840.png` and `safe-zone-after-2160x3840.png` show the supplied template over the actual master placement; the unused recording region is a neutral placeholder.

The packed `short-07-clay-study-safe-code.blend` preserves the native 2160 × 2420 camera plus explicit delivery-crop metadata; the composition script produces the approved 2160 × 2300 asset without resampling. No revised video has been rendered. This check establishes clearance against the supplied template; actual platform posting-interface review remains separate.
