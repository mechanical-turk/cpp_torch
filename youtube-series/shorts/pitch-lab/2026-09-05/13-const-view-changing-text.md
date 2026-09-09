# 13: This const view changes under your feet

Proposed MP4: `cpp-const-string-view-shared-storage-short.mp4`

Status: internal pitch, not recording or upload approval. Target: 18-19 seconds.

## Writer's pitch

Apply P12: use familiar text changing by one letter instead of an exception-safety model. Keep the ownership question visible.

### Script gate

Claim: a const string_view can observe changes made through the owning string while its own view state remains unchanged. Belief: const means the observed text is frozen. Expected objection: 'Const is not transitive immutability; a view does not own data.' Omit: dangling examples and all const forms. Keep visible: the owning string and the view's shared arrow.

### First frame and edit

Frame one: text='cat', const string_view label, and a shared connection. Callout: 'Const, but changing?' Circle const; highlight 'changes'. 0-5s: one hand holds the owner, the other points to the view. 5-11s: arrow targets text[0], change c to b, then sweep along the same connection. 11-15s: reveal the view prints bat while the view object stays put. 15-19s: hand covers the owner for the lifetime question. Keep strings safely alive in this episode.

### Narration

> This const view changes under your feet. It shows cat. Change the original string, and the same view now shows bat. Const stops us changing the view itself. It doesn't freeze the characters someone else owns. What happens when that owner disappears? I'll test the lifetime next.

### Technical gate

T12. Use a live string with a same-length character mutation, not assignment or growth that could invalidate storage. Compile and print both observations. The view object itself is not modified; narration and animation must not claim const was violated. Lifetime behavior belongs to the follow-up and must use diagnostics rather than promise a specific undefined-behavior output.

Candidate search language: C++ const string_view, non owning views, string lifetime. Platform demand and hashtags unresearched.

## Analyst's critique

1. The visual is simple, but the hook can imply the const object mutates. The distinction between a fixed view and changing referenced storage must land quickly or the controversy becomes misleading.
2. This repeats the broad 'reference-like handle' lesson of round 7. It is a distinct mechanism, but publishing both nearby may feel repetitive.
3. The useful practical risk is lifetime, which this video deliberately does not demonstrate. Viewers could leave with a curiosity rather than a usable decision rule.
4. The shared-arrow animation fits E3 well, but there is no account evidence that a const puzzle converts the recent performance audience.
5. The owner-disappears outro is coherent. It should be a proposed diagnostic test, not a pretext to show an uncontrolled crash as guaranteed behavior.

## Decision and learning

Reserve for an ownership mini-series. Do not follow the performance breakout with several similar language puzzles.

P13: Check novelty against recent and planned content; a different API can repeat the same viewer-level lesson.

