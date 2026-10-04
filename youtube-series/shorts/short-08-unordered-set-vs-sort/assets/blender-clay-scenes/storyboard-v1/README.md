# Short 08 — Blender slideshow storyboard

Eight independent static diagrams, rendered directly at 216×230 (10% of the
2160×2300 composition). These are small composition proofs; native code
sharpness is a later resolution check. No video, transitions or animation.

| PNG | Narration beat | Complete visual statement |
| --- | --- | --- |
| 01-distinct-task | Stop choosing algorithms by Big O alone. | Five input values → three distinct output keys, with original code. |
| 02-speedup-tease | Almost ten times the speed. | Same task, 9.68× result; replacement still hidden. |
| 03-duplicate-keeps-set | Counting distinct numbers / unordered set. | Initialize {3,1}, insert(3), and show unchanged {3,1} before and after. |
| 04-sort | Replaced it with sorting. | 3,1,3,2,1 → 1,1,2,3,3; all values retained. |
| 05-unique | Counting the changes. | Sorted input → retained 1,2,3 and two unnumbered tail slots. |
| 06-benchmark | 2.6 seconds instead of 25. | 25.25 s → 2.61 s; 9.68×. |
| 07-memory-layout | Look at how the versions use memory. | Code identifies separate nodes and a single contiguous vector. |
| 08-flat-table-next | Next, a flat hash table. | Directly stored keys interspersed with empty slots, no old timing. |

Before/after states coexist in each transformation image. Plain directional
arrows describe the operation, not ropes or physical pointers. No unseen motion
is needed to read the resulting state. Images contain only code, data numerals,
benchmark figures and diagram arrows. All row centers are aligned in projected
camera pixels rather than approximated using floor positions.

The input and unique-tail conventions remain unchanged. Set position/order,
allocation gaps and flat-table slots are schematic, not actual hashes, addresses
or benchmark traffic. The duplicate example is illustrative, not benchmark
setup. It does not depict the entire hash function or bucket implementation.

build.py builds/audits eight static poses using the actual approved clay assets.
render.py renders those poses only. storyboard-manifest.json maps speech to PNGs;
storyboard-verification.json audits alignment, text bounds and physical overlap;
render-verification.json records dimensions and hashes. Prior videos remain
archived in their existing packages and are not reused as this slideshow.
