# Short 07 current production

Revision 8 completed 2026-09-08T19:20:28-04:00 in [`final-v8/`](final-v8/README.md).
All six native clips and six matching previews are verified. It uses the approved
2160 × 2300 canvas, smaller inline `alignas` declarations, the supplied platform
safe-zone check, and the revised clay motion. Native exports are 2160 × 2300,
24 fps and silent, with durations 6 / 6 / 6 / 6 / 4 / 8 seconds. All 864 source
frames pass the placement and structural audit. All twelve exports pass frame
count, duration, dimensions, zero start, audio absence, full decode and hash
checks. The final encoded frame retains the benchmark and active bubbles.
Reports are in `final-v8/export-verification.json` and
`final-v8/_render/pipeline-status.json`. The root MP4s below are the previous revision.

## Previous revision 7

Revision 7 completed 2026-09-07T14:22:02-04:00. All six native clips and six matching previews are verified.

The opening uses a slower pulse arrival → ownership color → tray transfer sequence. The tray repeats its handoffs throughout contention. Rising +1 cues finish across cycle and scene boundaries; independent pulses, visible values and bubbles continue through the benchmark and discussion clips.

Native exports are 2360 × 2352, 24 fps, silent, with zero-based playback. Durations: 8 / 8 / 8 / 6 / 4 / 8 seconds. `export-verification.json` records all twelve successful exports. The packed editable scene and production scripts are in this assets package; previous exports remain in `archive/v6/`.

Local geometry, code placement and native frames were checked. Platform-interface clearance belongs to the complete editorial composite and remains unverified.
