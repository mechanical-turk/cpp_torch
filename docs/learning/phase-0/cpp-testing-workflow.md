# C++ Testing Workflow

## Milestone connection

- Phase 0 — Engineering baseline
- Milestone 0.2 — Testing Workflow and Test Design Foundations
- Status: passed

## Concrete model

```text
CTest
└── cpp_torch_tests executable
    ├── cpp_torch library
    ├── GTest::gtest_main
    └── GoogleTest test cases
```

- GoogleTest supplies test-definition/assertion machinery and a reusable test
  `main`.
- The test source is compiled into an ordinary executable target.
- `gtest_discover_tests` queries the built executable and registers individual
  cases with CTest.
- CTest orchestrates project-level tests and is the stable layer later used by
  CI, regardless of how many test executables exist.

## Dependency integration

GoogleTest v1.17.0 was pinned by its exact release commit and made available at
configure time with `FetchContent`. Its imported target carries its own include,
compile, and link usage requirements. Linking `GTest::gtest_main` therefore does
more than append a filename: it propagates the configuration needed to compile
the test and supplies `main()`.

Reconfiguring updated `compile_commands.json`, allowing `clangd` to resolve
`<gtest/gtest.h>` with the same include paths used by the real test build.

## Demonstrated evidence

- Direct listing and execution of `MathTest.AddTwoIntegers`
- Passing CTest discovery/execution
- Structured expected-versus-actual failure observation
- Successful restoration to a passing test
- Test-free configuration using `BUILD_TESTING=OFF`

## Deferred retrieval

- `EXPECT_*` versus `ASSERT_*` control flow
- Fixtures and lifetime behavior
- Value/type-parameterized tests
- Matchers and floating-point assertions
- Death tests
- GoogleMock and whether mocking improves or damages a particular design
- Unit versus integration boundaries as tensors acquire storage and ownership

