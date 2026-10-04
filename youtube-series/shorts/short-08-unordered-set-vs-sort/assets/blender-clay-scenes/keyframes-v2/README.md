# Short 08 — Revision 2, seven review keyframes

**Stills only. Await creator review before building/rendering any full video.**
Previous final-v1 was stopped and its render approval revoked.

The revised viewport operates directly on v. Its working-vector setup stays
off camera; the measured benchmark still includes the original copy. No new
in-place timing is asserted. No Big O labels, count labels, captions or banners.

Five values: 3,1,3,2,1. Sorted: 1,1,2,3,3. Retained: 1,2,3. Exactly two redundant
occurrences are excluded. Color is value identity: 1 teal, 2 cobalt, 3 raspberry.
The tray is neutral plum to separate pigment from the warm background. The
approved sculpted meshes, material construction, lighting and gradient remain.

Native source 2160×2300, placed at (0,0) in 2160×3840. Same source resolution,
font size and platform-template workflow. No animation frames are rendered.

1. 01-opening.png — hash code, five colored inputs, duplicate request in flight.
2. 02-speedup-tease.png — 9.68×, replacement hidden.
3. 03-duplicate-insertion.png — repeat 1 meets the existing teal 1.
4. 04-sort-before-unique.png — direct v code and the sorted five-value array.
5. 05-deduplicated-result.png — three retained values, two inactive tail slots,
   paired measured timings and 9.68×.
6. 06-memory-layout.png — separate node storage and contiguous retained range.
7. 07-flat-table-next.png — next flat-table layout, with no invented new timing.

build.py constructs exactly seven constant review poses from the approved
Short 07 native source, packs fonts and checks visible text bounds. It does
not render. render_keyframes.py is a finite still-only OptiX renderer, running
on the creator-authorized Omarchy worker. It converts glyphs to mesh only in
the render session. Native FONT data remains editable in the .blend.

Remote: gpu-worker:~/Projects/content-hq-render-worker/short-08/keyframes-v2/
Only this package's packed asset, script and manifests are transferred. The
Content HQ episode assets directory remains the review/delivery location;
remote rendering is explicitly authorized for this task. No secrets or whole
repository are mirrored. The remote workspace is a disposable render mirror.

The worker currently runs Arch Blender 5.2.1 LTS; the Mac source builder is
5.1.2. Inspect actual output across that version/backend difference. Completed
render timings and device information are recorded in render-report.json.
