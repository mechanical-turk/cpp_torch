# 19: Removing this if made the loop slower

Proposed MP4: `cpp-branchless-filter-extra-work-performance-short.mp4`

Status: internal pitch, not recording or upload approval. Target: 18-19 seconds.

## Writer's pitch

Apply P18: inspect both generated loops rather than assume removing source syntax changes the branch behavior. The central comparison uses equal outputs and different optional computation.

### Script gate

Claim: this verified unconditional-score-and-mask rewrite loses to skipping rejected inputs. Belief: branchless code is automatically faster. Expected objection: 'That is a bad branchless rewrite; SIMD can reverse this.' Omit: predictor internals and a full branchless catalogue. Keep visible: most inputs rejected, score computation valid for all inputs, unchanged mathematical result.

### First frame and edit

Frame one: 'if (keep(x)) total += score(x);' above the mask version and callout 'Branchless loses?' Circle the deleted condition; highlight 'slower'. 0-5s: hand waves away rejected inputs. 5-11s: arrows show the mask version still calculating scores for them, with extra hand beats. 11-15s: show equal results and measured median times; point to the still-present work. 15-19s: move a slider for accepted-input percentage. Keep score's actual compact kernel available, not a mysterious black box.

### Narration

> Removing this if made the loop slower. Most inputs fail the check, so the original skips their scores. My branchless version calculates every score, then masks out the unwanted ones. Same answer, more work. What happens when most inputs pass? I'll change that mix and test again.

### Technical gate

T6. Use a pure, defined unsigned score kernel, same data and acceptance mask, and correct equal outputs. Do not evaluate an invalid operation such as division by zero in the unconditional version. Measure optimized code, inspect if-conversion and SIMD, and do not prevent legitimate compiler improvements secretly. The losing rewrite is only a candidate result until verified.

Candidate search language: C++ branchless programming, conditional computation, CPU optimization. Platform demand and hashtags unresearched.

## Analyst's critique

1. The engineering disagreement is substantive, but a costly score function can make the answer obvious. The kernel must be simple and representative enough that the comparison feels fair.
2. The phrase 'branchless version' is a machine-code claim, not a property of source code. The compiler might emit a branch or transform both forms into the same loop.
3. Showing both code variants and the hidden extra computation can become too dense for the first frame. Use one edit and a stable work-flow visual.
4. The acceptance-rate question creates an excellent continuation with one variable changed. Yet a later SIMD win would not contradict this result; explain that consistently in discussion.
5. E2 supports debate about compiler transformations. It does not justify engineering a poor rewrite merely to solicit 'bad optimization' comments.

## Decision and learning

Conditional benchmark candidate, below hot/cold layout. Reject if the observed contrast depends on an implausible kernel or hidden compiler restrictions.

P19: Verify what the compiler emitted before calling code branchless, vectorized, inlined, or optimized.

