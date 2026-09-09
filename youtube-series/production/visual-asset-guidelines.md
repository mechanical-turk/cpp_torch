# Visual Asset Guidelines

These rules govern generated diagrams and lower-screen overlays for *Deep
Learning, All the Way Down*.

For native Blender animations, also read the [Animations Playbook](animations-playbook.md)
for the selected Retro Sunset clay system, reusable assets and pending placement corrections.

## Semantic consistency

- Related concepts must use one consistent visual grammar. Do not vary shape,
  container style, scale, or decoration unless that difference communicates a
  real conceptual distinction.
- Repeated objects must be literal duplicates of one canonical object. Do not
  ask an image model to independently redraw two objects that are intended to
  be identical.
- A singleton vector must not visually imply unused capacity or additional
  hidden elements. Show one element and nothing more.
- When comparing a singleton and an empty vector, use identical vector brackets:
  the singleton contains one element; the empty vector contains none.
- Use brackets to communicate the vector container. A scalar value uses the
  same element glyph without surrounding brackets.

## Overlay construction

- The current `1080 x 1920` vertical layout assigns the top `1080 x 744` region
  to the webcam (`y = 0` through `743`) and the entire remaining `1080 x 1176`
  region to the visual aid (`y = 744` through `1919`).
- Generate final lower-screen visual assets at exactly `1080 x 1176` unless
  that layout is explicitly revised. The asset must occupy the complete
  remaining vertical region, not float inside a smaller source box.
- Design the content for that taller region rather than padding a wide card.
  Distribute notation, labels, metadata, and diagrams across approximately
  ninety percent of the available height while preserving intentional edge
  margins.
- Lower-screen OBS overlays default to a fully opaque, edge-to-edge rectangular
  background with sharp corners.
- Do not rely on transparency, rounded outer corners, or the appearance of the
  source beneath the overlay unless a specific composition requires it.
- Design the overlay as a complete rectangular region that can safely cover
  whatever is beneath it in OBS.
- Freely positioned attention markers, pointers, and similar compositing assets
  are an explicit exception: they require a transparent background so they can
  move across camera and visual-aid regions without bringing a bounding box.
- Keep essential text and diagrams legible at phone size and within the central
  safe area.

## Platform interface safety

- A `1080 x 1920` canvas is not automatically portable across YouTube Shorts,
  TikTok, and Instagram Reels. Each platform overlays different controls,
  captions, account metadata, and navigation on the video.
- Record and export one universal vertical master whose essential content fits
  inside the intersection of all three platforms' safe areas. Do not create a
  separate edit for each platform unless a future platform feature makes that
  unavoidable.
- Treat the right edge, bottom region, and extreme top as interface space. Do
  not place a comparison column, conclusion, label, or other essential content
  beneath interaction controls, captions, account metadata, or navigation.
- Preview the same master inside all three real posting interfaces before its
  first publication. If one interface obscures essential content, correct the
  universal composition and reuse the corrected export everywhere.

## Platform-specific thumbnails and covers

The universal `1080 x 1920` video master does not imply a universal thumbnail.
Generate and inspect a separate cover composition for every platform surface
that accepts one. Preserve the same concept and brand grammar, but reflow the
objects and typography for the destination ratio. Never obtain one platform's
cover by blindly resizing or cropping another platform's file.

- **YouTube long-form:** `16:9`. Use `1280 x 720` at minimum for the current
  workflow; use a larger `16:9` source when available.
- **YouTube Shorts:** `9:16`. Default to `1080 x 1920`; a larger `9:16` source
  may be used. Keep the headline and primary visual near the center because
  YouTube can present vertical content differently across discovery surfaces.
- **Instagram Reels:** compose to Instagram's recommended `420:654` (`1:1.55`)
  cover ratio, but export a higher-resolution equivalent for crisp technical
  graphics. The current default is `1080 x 1682`, not a literal `420 x 654`
  raster. Instagram's desktop profile grid applies a centered `3:4` crop. On a
  `1080 x 1682` cover, treat the middle `1080 x 1440` region as the grid-safe
  area; approximately 121 pixels at both the top and bottom may disappear. All
  headlines, complete diagrams, results, and brand marks must fit inside that
  safe area. Do not reuse the YouTube Shorts `9:16` thumbnail unchanged. Inspect
  the actual profile-grid crop in the upload preview before publishing. For the
  current series treatment, do not place the creator's face on Instagram Reel
  covers unless the learner explicitly asks to restore it; lead with the
  technical visual instead.
- **TikTok:** use the `9:16` master and deliberately select or embed a clean
  cover frame. Inspect its profile-grid preview and keep the primary subject and
  headline centered; do not assume the full frame will be visible everywhere.
- **X native video:** do not assume a separately uploaded custom thumbnail is
  available. Make the selected poster or opening frame legible in the actual X
  composer preview.

Every asset handoff must name both the platform and the intended surface in its
filename, for example `thumbnail-youtube-shorts.png` and
`cover-instagram-reel.png`. Before publication, verify the real composer or
Studio preview rather than approving the source image in isolation.

## Alignment and typography

- Peer headings in comparison columns use one identical font family, size,
  weight, letter spacing, color, and baseline. Determine the shared size from
  the longest heading; do not enlarge shorter headings to fill available space.
- Reserve explicit inner gutters on both sides of every column separator. The
  longest heading must fit inside the padded content width rather than visually
  crowding the divider.
- Prefer contemporary, highly legible technical typefaces such as Helvetica
  Neue. Avoid default textbook-style typography, unintended italic faces, and
  glyph variants such as slashed zero when they make mathematical notation less
  immediately recognizable.
- Repeated metadata rows share exact baselines and column positions.
- Labels align with labels; values align with values. Do not approximate the
  grid separately in each comparison column.
- Preserve exact mathematical notation and verify every number, bracket, and
  label before accepting an asset.
- Prefer restrained technical styling over decorative effects.

## Generation workflow

1. Define one canonical instance of every repeated object.
2. Duplicate that instance for all equivalent uses.
3. When exact typography, alignment, or repeated geometry is required, build
   the final asset in a deterministic vector format such as SVG. Do not rely on
   a raster image generator to independently redraw elements that must match.
4. Verify object dimensions and alignment, not merely visual similarity.
5. Verify the semantic reading of containers, empty states, and values.
6. Export an opaque `1080 x 1176` rectangular PNG for the current OBS layout
   unless different dimensions or transparency were explicitly chosen for a
   concrete reason.
7. Inspect the final file at its intended phone-size scale before recording.
8. Confirm that the composition uses the vertical allowance deliberately and
   does not merely center a shorter legacy asset inside the larger canvas.
9. Export each requested thumbnail or cover at its platform-specific aspect
   ratio and inspect the destination preview for cropping before publication.
