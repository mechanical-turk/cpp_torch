# 06: Sorting made this loop faster

Proposed MP4: `cpp-sorted-data-branch-prediction-short.mp4`

Status: internal pitch, not recording or upload approval. Target: 18-19 seconds.

## Writer's pitch

Apply P05: compare two legitimate input orders with the same work, not a gratuitously bad API call. Preserve the cost boundary in the image.

### Script gate

Claim: this sorted-data scan beats the shuffled-data scan on the verified branch-containing build. Belief: the same if and same number of values should cost the same. Expected objection: 'You excluded sorting; my compiler removes that branch.' Omit: predictor architecture, SIMD tutorial, all distributions. Keep visible: 'Scan time only', same multiset and predicate, setup excluded for both.

### First frame and edit

Frame one: the same if line over shuffled versus grouped color blocks, callout 'Order changes speed?' A red circle encloses the changing yes/no pattern; hook captions emphasize 'sorting' and 'faster'. 0-5s: shuffle gesture. 5-11s: arrows follow unpredictable then grouped outcomes, with a repeated hand beat for the latter. 11-15s: reveal measured scan medians. 15-19s: point to a separate sorting-cost block for the next test.

### Narration

> Sorting made this loop faster. Both arrays contain the same numbers. Both run the same check. In this build, the sorted data makes the branch easier to predict, and the scan finishes sooner. These times exclude sorting. How many scans pay for that sort? I'll measure that next.

### Technical gate

T6 warns that if-conversion and vectorization may eliminate the premise. Inspect optimized assembly and branch-miss evidence on the recording target; do not secretly disable optimization to obtain a familiar result. Keep sum arithmetic safe, equal outputs, comparable cache state and input distribution. Record total cost separately. No validated benchmark exists in this pitch.

Candidate search language: C++ branch prediction, sorted array performance, CPU branches. Platform demand and hashtags unresearched.

## Analyst's critique

1. The result sounds practical, but hiding sorting cost would reverse the impression of total speed. The visible and spoken timing boundary is essential, not optional nuance.
2. The strongest result may disappear under the user's normal compiler. A familiar internet example is not evidence that it works on this recording setup.
3. Colors can make prediction intuitive, but viewers must still connect array order to machine branches. This is a second conceptual layer beyond the one-line change.
4. The footer 'Scan time only' competes with captions and two input strips. Safe-area readability needs a real composition test.
5. The break-even question is excellent because it challenges the demonstrated win on its own terms. Nevertheless, E1 cannot tell us whether viewers will stay through the setup needed to earn it.

## Decision and learning

Hold for a normal-build result with branch evidence. Reject if it requires a misleading setup to reproduce the expected story.

P06: Show the comparison's decisive cost boundary; excluding setup is acceptable only when the claim clearly names what was timed.

