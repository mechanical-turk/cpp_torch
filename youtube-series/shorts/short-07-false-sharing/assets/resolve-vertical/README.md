# Short 07 Resolve setup — incomplete

2026-09-07: Created and saved the local Resolve project `Short 07 - False Sharing - 4K Vertical`. Project settings were visibly set to 2160 × 3840, square pixels, 24 fps.

Media import is blocked: Resolve repeatedly stalls when opening native file dialogs or reading the helper Lua file under Documents. A process sample shows a blocked filesystem call. The internal console executes simple Lua but `Resolve()` returns nil; external scripting also returns no application. No privacy permissions were changed.

2026-09-08: Deleted the unused `short-07-4k-vertical.fcpxml` at the creator's request. It was never verified in Resolve and referenced superseded revision 7 media, dimensions and timing.

Current verified animation clips are in [`../blender-clay-scenes/final-v8/`](../blender-clay-scenes/final-v8/README.md). Each is 2160 × 2300 at 24 fps. The approved composition places the animation at (0, 0), without resizing, in a 2160 × 3840 master, leaving the remaining 1540 pixels below for recording. This placement has not yet been implemented or verified in Resolve.

No media has been imported into the saved Resolve project, and no finished DRP backup exists yet. An accidental empty project whose name begins `UserskeremkazanDocumentsPr` also remains in the local library from an earlier name-field focus error.

## Remaining work

1. Resolve the app's file-access stall and import the six current revision 8 MP4s.
2. Verify 2160 × 3840, 24 fps and the approved 2160 × 2300 top placement without cropping or resizing.
3. Keep the six native scene clips separate; create and label the empty recording video/audio tracks.
4. Save and export a DRP backup into this directory.
