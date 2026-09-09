# 12: This promise stops the copies

Proposed MP4: `cpp-noexcept-move-vector-reallocation-short.mp4`

Status: internal pitch, not recording or upload approval. Target: 18-19 seconds.

## Writer's pitch

Apply P11: show a specific library decision instead of a slogan that noexcept makes everything faster. P04 keeps the proof at copy/move counts.

### Script gate

Claim: marking this genuinely non-throwing move constructor noexcept changes the tested vector reallocation from copies to moves. Belief: a keyword that does not change the function body cannot change the work. Expected objection: 'Only if copying is available; don't lie about noexcept.' Omit: full exception-guarantee taxonomy. Keep visible: valid copy constructor, same non-throwing move body, vector capacity growth.

### First frame and edit

Frame one: a short move-constructor signature and a vector-growth box; callout 'One word, fewer copies?' Circle the position for noexcept and highlight 'promise'. 0-5s: hand points to unchanged body. 5-11s: copy arrows duplicate buffers as capacity grows. 11-15s: add noexcept, rerun, arrows transfer ownership and show actual copy/move counts. 15-19s: point to the copy constructor for the next experiment. Keep the class implementation off the camera viewport.

### Narration

> This promise stops the copies. Our vector needs more space. It copies these objects because moving them might throw. Mark this safe move noexcept, and the next run moves them instead. The function body didn't change. What if copying isn't available? I'll test that case next.

### Technical gate

Verify behavior in the actual standard library with a copyable instrumented type, forced real reallocation and a move body that cannot throw. Isolate relocation counts from construction of the appended item. Do not claim the standard mandates one implementation strategy for all types, or that adding noexcept to a throwing body is safe. Primary evidence: vector.modifiers exception requirements and the library's move-if-noexcept implementation.

Candidate search language: C++ noexcept move constructor, vector reallocation copies, exception safety. Platform demand and hashtags unresearched.

## Analyst's critique

1. 'This promise' is abstract unless noexcept is clearly targeted on frame one. It partly reintroduces the vague-opening problem from round 1.
2. Explaining why rollback matters would require exception safety, moved-from objects, and copying. The current script compresses that into a rule, which is efficient but can feel arbitrary.
3. The counter reveal is strong and measurable, yet showing the type plus vector growth plus two traces risks exceeding the camera area. Only the signature and trace should be visible.
4. The move-only follow-up is legitimate, but the audience may need more background than the question suggests. A technical sequel is not automatically an accessible sequel.
5. The 'just add noexcept' takeaway could be harmful if viewers mark a throwing move. The word 'safe' and visibly unchanged non-throwing body are necessary context, not optional hedging.

## Decision and learning

Good advanced C++ candidate after a simpler copy/move Short. Hold the next-release slot for a lower-prerequisite concept.

P12: Count prerequisite concepts as well as words; a short sentence can still require a long mental explanation.

