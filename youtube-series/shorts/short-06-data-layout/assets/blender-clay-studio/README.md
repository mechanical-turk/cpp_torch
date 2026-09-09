# Retro Sunset — clay studio lighting revision

A native Blender still revising the near-approved clay scene. Video generation remains paused.

- `retro-sunset-clay-studio.png`: 2360 × 2352 Cycles render.
- `retro-sunset-clay-studio.blend`: editable scene with packed fonts.
- `build.py`: reproducible scene construction and rendering.
- `scene-check.json`: dimensions, model counts, composition and arrow checks.

The arrow is one continuous filled outline with rounded corners and a bevel, replacing the intersecting tube construction. An enlarged native render was inspected; the evaluated geometry forms one closed component with no non-manifold edges.

The studio lighting uses a directional warm rectangular key, a narrow cool rim and restrained neutral front fill. Ambient illumination is reduced, and the clay materials retain their tactile grain while gaining more defined reflections. This produces deeper shadows and clearer separation between lit surfaces and recessed faces.

The camera, canvas, object shapes and positions, result typography, three score labels and three history labels are retained. There are exactly fifteen history cards in each cradle. The prior clay study remains available separately.

The full-size still uses 256 maximum Cycles samples, adaptive threshold 0.004, denoising and a 1-pixel reconstruction filter. The build disables Metal kernel optimization and MetalRT for stability on this Blender installation. All geometry, surfaces and lighting are native Blender; no image plate is used.

Rebuild on the current machine:

```sh
/Users/keremkazan/bin/blender -b --python build.py
```

Use `-- --preview` for a half-resolution preview. Use `-- --output-dir /absolute/output/path` to choose another destination. The source uses macOS Arial fonts; the saved scene packs them. Only one frame is rendered.
