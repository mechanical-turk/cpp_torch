# Episode 8 script verification

Verified September 7, 2026 after narrowing the episode to arithmetic backward.
This supersedes the earlier 71-edit sum/MSE verification for the current script.

## Reproduce

From the content repository root:

```sh
SCRIPT_BASE_REF=92aa868 node youtube-series/chapter-08/verify-script.mjs
```

The verifier applies the two explicit preparation fixes first, then replays
all literal edits into a temporary copy. Each Before must match exactly once.
It never edits the demonstration repository. The working source already contains
recording edits, so use the baseline command above, not a fresh replay onto it.

## Results

- 66 literal edit pairs replayed successfully.
- Original tensor and scalar programs passed their assertions.
- All runnable checkpoints through E-elementwise-complete passed.
- 48 central finite-difference comparisons passed: both scalar operands of
  all four arithmetic operations, with positive, negative and zero numerators.
- Shared branches, intermediate lifetime, repeated backward reset, alias identity,
  fresh construction and scalar leaf seeding passed.
- Sum backward throws as unsupported. A matrix result fails the public
  scalar-root check; that check does not verify a matmul backward rule.
- Forward zero-denominator checks passed for signed zero, scalar and broadcast
  division, and an accessed zero element. Empty output accesses no denominator.
- No operation switch or operation-tag access occurs inside the coordinate helper.
- C++23 with ASan/UBSan, assertions enabled; no sanitizer failures observed.

Artifacts: `/var/folders/lg/tchx84rx5xx23zf_4lch60ww0000gn/T/dlatwd-episode08-XQ29cM`

Demonstration files were unchanged by verification:
- main.cpp SHA-256: `d89ad870f4d1733c4b4f15c7ac683b9255169ac5432e996b8a02a31d570b2912`
- scalar_autograd.cpp SHA-256: `345d14d7cd348f4ab651a602cba96a85d0800528c6043c65d46c8c10d013b119`

## Current limits

- Sum and matmul backward are not implemented. Consequently batch MSE, mean
  and composed dot backward are not complete. Their forward paths still exist.
- The general elementwise broadcast mapping remains in the script, but this
  narrowed public API has no reduction backward or non-scalar seed to exercise
  multi-element gradients end to end. Do not claim those tests passed here.
- Default rejection may happen after gradients were reset or partially updated.
  Do not use gradients from failed calls. No preflight preservation is promised.
- Do not mutate participating values between forward and backward. There is no
  mutation guard. Rebuild a forward graph after each future training update.
- Scalar roots only; reachable gradients reset each call; no requires_grad filter.
- No general NaN, infinity, overflow or underflow policy or deep-graph guarantee.
- `deferred-gradient-checks.cpp` preserves the prior broader test draft for
  Episode 9. It is not run here and needs revision for the completed matmul and
  training contracts; its old rejection-before-reset assertion is not a current
  guarantee.
- The recorded opening still promises loss-to-prediction gradients. Trim or
  replace that sentence before release. Tests cannot repair an editorial promise.
- Script audit: 85.5/100, rework. Delivery, first-minute pacing and public keyword
  research remain separate checks. No extra on-camera testing was added.
