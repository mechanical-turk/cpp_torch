# Milestone 0.6 — GitHub Actions Acceptance Checks

## Motivation

Turn locally demonstrated acceptance configurations into reproducible checks on
every proposed change. CI should detect portability, diagnostics, test, sanitizer,
and optimized-build failures without pretending hosted runners provide stable
performance measurements.

## Dependencies and diagnostic

- Milestones 0.1–0.5 complete
- Public repository: `mechanical-turk/cpp_torch`
- Checked-in CMake presets already define local acceptance behavior
- No existing GitHub Actions workflows

## Learning objectives

- Understand workflow triggers, jobs, steps, matrices, permissions, concurrency,
  and failure propagation.
- Reuse local CMake presets rather than duplicate compiler flags in YAML.
- Exercise GCC, upstream Clang, and Apple Clang early.
- Separate strict correctness checks from sanitizer and optimized-build checks.
- Avoid running performance comparisons on noisy shared CI runners.
- Read a failed Actions log and reproduce the same preset locally.

## Implementation contract

- Add `.github/workflows/ci.yml`.
- Trigger on pushes to `master`, pull requests, and manual dispatch.
- Grant only read access to repository contents.
- Cancel superseded runs for the same branch/PR.
- Run strict build and CTest on:
  - Ubuntu 24.04 with GCC;
  - Ubuntu 24.04 with Clang; and
  - macOS 15 with Apple Clang.
- Run the sanitized preset on Ubuntu Clang.
- Build Release and benchmark presets on Ubuntu without using benchmark timings
  as a gate.

## Acceptance criteria

- Workflow syntax is accepted by GitHub.
- Every job passes on the initial push.
- Matrix logs show the intended compiler identities.
- A deliberate CI-only failure can be reproduced locally through the same preset
  or is documented if runner-specific.
- Branch/PR status exposes distinct strict, sanitizer, and optimized-build checks.
- Final workflow remains focused enough to diagnose failures quickly.

## Evidence, review, mastery, and retrospective

Pending first GitHub run.

