# Short 07 benchmark handoff

September 7, 2026. The code and evidence are in
[the Shorts workspace](../../../aliases/01-screen-short-form/short-07-false-sharing/README.md).

## Result for the animation

Two independent final runs, each with fifteen repetitions and 20 million relaxed
atomic updates per counter, measured:

| Run | Packed | Separated | Ratio |
| --- | ---: | ---: | ---: |
| 03 | 253.019 ms | 44.168 ms | 5.729x |
| 04 | 244.524 ms | 44.194 ms | 5.533x |

Recommended matched pair: **244.52 ms to 44.19 ms**, **5.5x faster in this test**.
Use both values from run 04. One-worker controls were essentially unchanged:
87.178 ms packed versus 86.985 ms separated in run 04.

Actual cache lines are 128 bytes on the test machine. Packed counter offsets
are 0 and 8; separated offsets are 0 and 128. Runtime checks verify both layouts.
Both call the same scalar `ldadd` loop under normal `-O3`; vectorization was not
disabled. The comparison preserves the number of atomic updates and their
memory ordering. Thread creation, reset, and validation are outside timing.

See the [full results and raw CSV links](../../../aliases/01-screen-short-form/short-07-false-sharing/RESULTS.md)
for measured spans, variation, controls, build configuration, and development
harness corrections. Final release tests and address/undefined/thread sanitizer
checks pass. No core pinning or hardware coherence tracing was performed.

This supplies the script's numerical placeholders. It does not establish
literal animation timing, platform crop safety, or recorded narration duration.
The final-only publication experiment proposed in the outro was not run here.
Script scoring and benchmark verification remain separate responsibilities.

Run again from the Shorts repository root with `make false-sharing`.
