MP4 filename: `cpp-unordered-set-vs-sort-big-o-performance-short.mp4`

# Short 08: Choosing by Big O

## Visual setup

Use Short 07 final-v9 hand-sculpted clay geometry, matte pigment, rolled rims,
thumb presses and irregular shallow smears. Reuse its studio lighting and
Retro Sunset gradient. Keep the warm orange highlight behind objects and dark
plum behind the unlit syntax-highlighted code. No radial textures or plastic gloss.

Native canvas: 2160 × 2300, placed at (0,0) in a 2160 × 3840 vertical master.
The bottom 1540 px is for the presenter. Keep the camera stable. Check the actual
1080 × 1920 safe-zone template at 2× on the full master. Code guard:
x180–1812, y480–1180; essential physical text: x120–1872, y440–2260.
Use one linked tile master and equal-sized duplicates, with ivory numerals.

Five input values: `3, 1, 3, 2, 1`. Color follows value throughout:
**1 = teal, 2 = cobalt, 3 = raspberry**. Equal values share exactly the same
material. Neutral plum trays distinguish the container from its contents.
Sorting gives `1, 1, 2, 3, 3`; unique retains `1, 2, 3` and excludes two redundant
occurrences. This is a teaching example, not the benchmark duplicate fraction.

Only code, physical data numerals, benchmark figures, units and the speedup
belong in Blender. No floating object/method names, even beneath results.
No Big O badges, captions, callouts, titles or banners.
The code viewport uses prepared working vector `v`. The actual benchmark still
preserves its original input through a copy within the measured sorting method;
that preparation is omitted from the visual viewport, not from the measured
work. Do not animate a second copy tray or imply a newly timed in-place test.

## Scene 01 | Hook — 01-distinct-task.png

> Stop choosing algorithms by Big O alone.

Hold a complete input/output diagram: original hash code above the five-value
input 3,1,3,2,1; a plain downward arrow leads to the three distinct keys 3,1,2.
Both states are visible simultaneously, on aligned rows. No pre-existing set
whose construction the viewer must infer. Point at the input, then the output.

## Scene 02 | Escalation — 02-speedup-tease.png

> In this test, the worse Big O gave me almost ten times the speed.

Same complete task, with one large 9.68× faster above it. Withhold the replacement
and paired timings. No complexity badge or floating method labels.

## Scene 03 | Problem — 03-duplicate-keeps-set.png

> We're counting distinct numbers. This C++ unordered set inserts each value once: expected linear time.
>
> So where's the time going?

Show this illustrative duplicate case as code:

```cpp
unordered_set<Number> distinct;
distinct = {3, 1};
distinct.insert(3);
```

Above the operation arrow, the set contains 3,1. Below it, the set still contains
3,1. Both rows align exactly. The inserted 3 is in the code; no mysterious flying
copy or duplicate box is needed. This proves unchanged membership in one still.
These small example values are not the benchmark input or setup. Keep the actual
benchmark's reserve/input-copy scope unchanged off camera. Face the viewer for
the question. No bucket anatomy, ropes or pretend hardware trace.

## Scene 04 | Replacement — 04-sort.png and 05-unique.png

> I replaced it with sorting and counting the changes. N log N, but it finished in 2.6 seconds instead of 25.

First hold 04-sort.png: sort(v.begin(), v.end()) above aligned five-slot before
and after rows. Input 3,1,3,2,1 becomes 1,1,2,3,3; the arrow connects the states.
Then cut to 05-unique.png: show the actual unique/return expressions. Its upper
row is 1,1,2,3,3; its lower row retains 1,2,3 and two dark unnumbered tail slots.
Neither illustration requires watching movement. Keep allocation and tail values
honest; no cyan divider. Trace corresponding positions with a gesture.

## Scene 05 | Payoff — 06-benchmark.png

On “2.6 seconds instead of 25,” hold the complete result:

```text
25.25 s → 2.61 s
  9.68× faster
```

Retain the established coral/mint/ivory treatment and retained-prefix tray.
No method labels or narration in the image. Use supplied benchmark medians and
speedup; no relationship between diagram timing and the measured performance.

## Scene 06 | Memory — 07-memory-layout.png

> Why does sorting win when it has the worse Big O?
>
> Look at how the two versions use memory.

One still contains both representations. The unordered_set declaration anchors
an aligned row of separated stored nodes above. The sort/unique code anchors a
single vector allocation below, containing retained values and unspecified tail
slots. Code identifies each representation without floating method labels.
Point to the separate entries, then the contiguous row. Allocation gaps are
schematic; this image does not prove locality alone caused the measured ratio.

## Scene 07 | Continuation — 08-flat-table-next.png

> Next, we're testing a flat hash table.

Hold a single directly stored slot layout: 3, empty, 1, empty, 2, with insertion
code above it. No previous benchmark figures, node pedestals or floating name.
This is a schematic preview of an unmeasured implementation, not a hash-function
trace or a result. Introduce it on the spoken cue, then cut.

## Editing and delivery directions

- Spoken words remain locked. This version is a slideshow; use cuts and static
  holds. Each frame contains the complete evidence for its beat.
- Eight independent PNGs are the first deliverable, rendered in Blender at
  216×230 (10% of each native dimension) for composition feedback. Expand
  resolution after review. No animation/video batch runs for this revision.
- Canonical package: assets/blender-clay-scenes/storyboard-v1/ in this episode.
- Retain 2160×2300 native layout at (0,0) in the 2160×3840 master. Safe-zone
  checks apply to the complete master. Tiny proofs do not establish native
  code sharpness or real platform-interface clearance.
- Keep captions as an editing layer. No explanatory prose, titles or extra
  complexity text baked into images. Presenter gestures must not obscure them.
- Natural-read timing determines the still holds. Apply +5 dB once to speech
  and CapCut Enhance voice at 75%; check the complete edited audio before release.
