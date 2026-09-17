# Episode 13: migration order

Creator direction: teach the logical migrations before the file migrations.
Do not combine a graph representation change with moving its implementation
to a different file. The first recording draft is now in `script.md`; creator
approval and a timing rehearsal are still pending.

Proposed step-by-step sequence from the recorded Episode 12 checkpoint:

1. Show the existing result construction: create a Tensor, then assign its
   operation, parents, and broadcast strides. Establish why a constructor
   should finish initialization before returning the object.
2. Introduce `Parent`, pairing a parent node with its broadcast strides.
   Migrate every graph-building call site, backward input lookup, and topology
   traversal together. Explain that the strides map output coordinates to that
   particular input. Non-broadcast operations leave the mapping empty.
3. Give `TensorNode` a constructor. Move shape/storage validation and zeroed
   gradient initialization into it. Default operation to leaf and parents to
   empty. Preserve public `Tensor(shape, data)` convenience.
4. Add the private `Tensor(shared_ptr<TensorNode>)` constructor, then migrate
   operation results to complete node construction. Include the mappings in
   each Parent at construction, rather than attaching metadata afterward.
   Show all affected sites explicitly, with exact Before/After code.
5. Verify preserved forward values and gradients, including broadcasting and
   repeated use of one parent. Keep incomplete multi-edit stages labeled;
   do not manufacture broken runs for the lesson.
6. Only then separate headers, implementations, examples, and GoogleTest tests,
   and introduce their CMake targets. File relocation must not silently change
   algorithms or ownership behavior.

Use connected narration before and during each edit. Reassess scope against
the 10-15 minute target before drafting; split the work if necessary rather
than compressing away the reasoning.

Implementation review checkout:
`/Users/keremkazan/Documents/Projects/deep-learning-all-the-way-down-ep13`

Branch: `refactor/episode-13-library`. The pre-parent-migration comparison
checkpoint is `dec0a9c`. This note supplements the long-form playbook; the
eventual script still requires its keyword research and separate review file.
