# Decision 0005 — Script Long-Form Chapters for Native Clip Extraction

## Status

Superseded by Decision 0006.

## Context

The video series uses long-form chapters as its primary teaching medium, while
short-form video provides additional discovery and lets individual explanations
stand on their own. Retrofitting arbitrary horizontal footage into vertical
clips can destroy code readability, omit necessary context, or require a second
production pass.

## Decision

Every future chapter script will contain at least one intentional,
self-contained clip module. A module will have its own hook, context,
explanation or demonstration, and conclusion while remaining a natural step in
the chapter's larger story.

Scripts will mark candidate clip boundaries and include vertical-safe production
notes for the relevant segment. The main recording remains a natural 16:9
lesson; only designated clip modules need to keep essential visual information
inside a composition that can be reframed effectively for vertical delivery.

## Consequences

- Short-form material becomes part of instructional design rather than an
  afterthought during editing.
- Long-form coherence and educational depth remain primary constraints.
- Clip modules must provide standalone value rather than functioning as ads.
- Some segments may require larger code, centered diagrams, isolated recording
  tracks, or brief pauses that create clean edit boundaries.
- Not every valuable long-form passage must become a clip.

Every chapter also follows a stable learning loop. A compressed cold open
combines the series identity, only the previous state necessary for continuity,
and the current episode's promise. It is followed by a brisk retrieval section
that answers the previous episode's closing questions without reteaching the
previous chapter. The main lesson then proceeds through concept, code, and
verification. It ends with a review, a concise next-chapter hook, and retrieval
questions that will open the next chapter. This ordering makes the questions
the final spoken content.
Chapter 1 is the natural exception because it has no predecessor.

Separate series-introduction, previous-episode-recap, and current-episode-
introduction sections are explicitly avoided because they repeat context before
the lesson begins.

This structure makes retrieval practice part of the series itself and creates a
concrete continuity bridge between chapters.
