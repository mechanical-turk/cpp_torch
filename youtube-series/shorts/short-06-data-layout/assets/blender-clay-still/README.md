# Retro Sunset — native Blender clay still

Single-frame look development for Short 06, rebuilt from the selected clay hero reference. Video generation is paused. This still is a new review point, not a replacement for the approved animation.

- `retro-sunset-clay-still.png`: 2360 × 2352 native Cycles render.
- `retro-sunset-clay-still.blend`: editable scene with packed fonts and procedural materials.
- `build.py`: scene construction and single-frame rendering script.
- `scene-check.json`: rendered dimensions, label/card counts, and scene checks.

The gold tiles have continuous rounded shells and physically recessed amber faces. The navy cradles hold three sets of fifteen cobalt cards, with ivory `history` labels on the front. The perspective camera, broad studio lights, textured burgundy-to-peach ground, and restrained surface irregularity were developed together against the reference. The result typography retains only the timings, arrow and multiplier.

All visible geometry, lighting and surfaces are native Blender. The reference image is not used as a texture, background plate, or composited substitute. The generated reference's illustrative card count is corrected to fifteen per player here.

Rebuild on the current machine:

```sh
/Users/keremkazan/bin/blender -b --python build.py
```

Use `-- --preview` for a 50% preview, or `-- --output-dir /absolute/output/path` to choose another destination. The build script uses installed macOS Arial fonts; the saved `.blend` packs them. The final render uses Cycles with 192 maximum samples, adaptive sampling, denoising, and Khronos PBR Neutral color management. No animation render is performed.

The build disables Metal kernel optimization and MetalRT to avoid a shader-compiler crash encountered in this Blender 5.1.2 installation. The full-size GPU render then completed successfully.
