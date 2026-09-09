# 16: Copying this pointer updates a shared counter

Proposed MP4: `cpp-shared-ptr-copy-reference-count-performance-short.mp4`

Status: internal pitch, not recording or upload approval. Target: 18-19 seconds.

## Writer's pitch

Apply P15: show the hidden state change rather than merely calling an abstraction expensive. Use one ownership counter as the visual trace.

### Script gate

Claim: copying this shared_ptr adds an owner and updates shared ownership state. Belief: copying a smart pointer costs the same as copying an address. Expected objection: 'Pass by reference; ownership safety can be worth it.' Omit: weak ownership details and exact atomic instruction costs. Keep visible: a genuine shared_ptr copy, object unchanged, owner count changes.

### First frame and edit

Frame one: one pointer becomes two, but a third highlighted box says owners: 1. Callout: 'More than an address?' Circle the ownership box and emphasize 'shared counter'. 0-5s: two fingers indicate the pointers. 5-11s: arrows from both pointers land on the same object while the counter changes. 11-15s: destroy the extra owner, reverse the counter and point to the unchanged object. 15-19s: two hands represent competing workers in the proposed follow-up. No invented timing bars.

### Narration

> Copying this pointer updates a shared counter. Both pointers still point to the same object, but now there are two owners. Destroy the copy, and the count drops again. That ownership tracking is work beyond copying an address. What happens when threads do it together? I'll benchmark that next.

### Technical gate

Verify owner count changes in a single-threaded deterministic example without simultaneous use_count sampling as a synchronization mechanism. Reference-count implementation and atomic costs are library-dependent. For any threaded benchmark, copy distinct shared_ptr handles sharing a control block, not unsynchronized writes to the same handle. Ownership and borrowing are different contracts; do not silently substitute a raw pointer as equivalent.

Candidate search language: C++ shared_ptr overhead, reference counting, shared ownership. Platform demand and hashtags unresearched.

## Analyst's critique

1. The claim is accurate but mostly descriptive. A shared counter changing is less emotionally striking than a loop unexpectedly getting slower or producing a different result.
2. The phrase 'shared counter' introduces jargon in the hook. The ownership diagram may explain it, but the spoken opener does not independently sell a clear consequence.
3. The original promise is satisfied as soon as the counter rises. The destruction beat adds confirmation rather than escalation, risking an empty middle.
4. The interesting contention result is pushed into the next episode. We should not save the strongest available idea for a sequel merely to create follower intent.
5. E2 suggests ownership-versus-borrowing can invite useful debate, but the current short has not yet earned that debate with a consequential result.

## Decision and learning

Do not select this version. Keep the ownership mechanism as a supporting explanation for a future measured contention story.

P16: Do not save the most compelling demonstration for the sequel; the current Short must earn attention on its own.

