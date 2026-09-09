# 02: I deleted eight bytes without deleting a field

Proposed MP4: `cpp-struct-padding-field-order-short.mp4`

Status: internal pitch, not recording or upload approval. Target: 18-19 seconds.

## Writer's pitch

Apply P01: the hook names the exact edit's consequence. Replace floating-point bookkeeping with a visible before-and-after byte layout.

### Script gate

Claim: these two field orders occupy 24 and 16 bytes on the tested target. Belief: the fields alone determine an object's size. Expected objection: 'Padding is required; eight bytes is irrelevant unless you have many objects.' Omit: ABI taxonomy, packed structs, serialization. Keep visible: same three fields and measured sizeof results.

### First frame and edit

Frame one: the same three colored field blocks in two arrangements, with 24 bytes on the original and ? on the reordered version. Callout: 'Where did 8 bytes go?' Highlight 'eight bytes' in captions and circle the moved field. 0-5s: drag the double block with a hand sweep. 5-11s: arrows identify empty gaps. 11-15s: close the gaps, reveal 16, point to the difference. 15-19s: gesture toward an array of the smaller objects during the question.

### Narration

> I deleted eight bytes without deleting a field. This C++ object holds two characters and a double. Move the double to the front. The empty gaps shrink, and the object drops from twenty-four bytes to sixteen. Does using less memory make it faster? I'll benchmark an array of these next.

### Technical gate

Verify sizeof and offsetof on the actual target before using these numbers. Alignment can create padding; C++ does not mandate these sizes for every implementation. No measured speedup is implied. This is a layout demonstration, not a recommendation to change a public ABI.

Candidate search language: C++ struct padding, memory alignment, field order. Platform demand and hashtags unresearched.

## Analyst's critique

1. The 24-to-16 result is concrete, but eight bytes may feel trivial before the viewer understands repeated objects. Adding a million-object setup would weaken the short opening.
2. The diagram can accidentally imply fields have been compressed rather than reordered. The double and character blocks must retain identical widths in both layouts.
3. The question about speed is worthwhile, yet this pitch has no speed evidence. Presenting a smaller object as automatically better would overstate the result.
4. E1 favors low opening burden; E2 gives no evidence that field-layout trivia will generate the same participation as a disputed optimization. Strong visual clarity does not establish controversy.
5. Reordering fields can change interfaces and layout contracts. A concise 'local struct' context belongs in the demonstration, while ABI details can stay in discussion.

## Decision and learning

Shortlist for visual simplicity, with target-specific size verification still required. Keep the speed question genuinely open.

P02: Make the benefit meaningful at the shown scale; a striking number alone may not establish why the viewer should care.

