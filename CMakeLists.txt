cmake_minimum_required(VERSION 3.26)
project(cpp_torch LANGUAGES CXX)

option(
  CPP_TORCH_ENABLE_SANITIZERS
  "Enable AddressSanitizer and UndefinedBehaviorSanitizer"
  OFF
)

option(
  CPP_TORCH_WARNINGS_AS_ERRORS
  "Treat cpp_torch project warnings as errors"
  OFF
)

option(
  CPP_TORCH_BUILD_BENCHMARKS
  "Build cpp_torch benchmarks"
  OFF
)

include(CTest)

add_library(cpp_torch_warnings INTERFACE)

target_compile_options(
  cpp_torch_warnings
  INTERFACE
    "$<$<CXX_COMPILER_ID:AppleClang,Clang,GNU>:-Wall;-Wextra;-Wpedantic;-Wconversion;-Wshadow>"
    "$<$<CXX_COMPILER_ID:MSVC>:/W4>"
)

if(CPP_TORCH_WARNINGS_AS_ERRORS)
  target_compile_options(
    cpp_torch_warnings
    INTERFACE
      "$<$<CXX_COMPILER_ID:AppleClang,Clang,GNU>:-Werror>"
      "$<$<CXX_COMPILER_ID:MSVC>:/WX>"
  )
endif()

if(CPP_TORCH_ENABLE_SANITIZERS)
  add_library(cpp_torch_sanitizers INTERFACE)

  target_compile_options(
    cpp_torch_sanitizers
    INTERFACE
      -fsanitize=address,undefined
      -fno-omit-frame-pointer
  )

  target_link_options(
    cpp_torch_sanitizers
    INTERFACE
      -fsanitize=address,undefined
  )
endif()

add_library(cpp_torch src/math.cpp)
target_compile_features(cpp_torch PUBLIC cxx_std_23)
target_link_libraries(cpp_torch PRIVATE cpp_torch_warnings)
target_include_directories(
  cpp_torch
  PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/include
)

if(CPP_TORCH_ENABLE_SANITIZERS)
  target_link_libraries(cpp_torch PUBLIC cpp_torch_sanitizers)
endif()

add_library(
  manual_linear_regression
  experiments/phase-1/manual-linear-regression/linear_regression.cpp
)
target_compile_features(manual_linear_regression PUBLIC cxx_std_23)
target_include_directories(
  manual_linear_regression
  PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/experiments/phase-1/manual-linear-regression/
)
add_executable(
  manual_linear_regression_example
  experiments/phase-1/manual-linear-regression/main.cpp
)
target_link_libraries(
  manual_linear_regression_example
  PRIVATE
    manual_linear_regression
    cpp_torch_warnings
)

add_executable(basic_usage examples/basic_usage.cpp)
target_link_libraries(
  basic_usage
  PRIVATE
    cpp_torch
    cpp_torch_warnings
)

if(BUILD_TESTING)
  include(FetchContent)

  FetchContent_Declare(
    googletest
    URL
      https://github.com/google/googletest/archive/52eb8108c5bdec04579160ae17225d66034bd723.zip
    DOWNLOAD_EXTRACT_TIMESTAMP TRUE
  )

  FetchContent_MakeAvailable(googletest)

  add_executable(cpp_torch_tests tests/math_test.cpp tests/manual_linear_regression_test.cpp)

  target_link_libraries(
    cpp_torch_tests
    PRIVATE
      cpp_torch
      cpp_torch_warnings
      manual_linear_regression
      GTest::gtest_main
  )

  include(GoogleTest)
  gtest_discover_tests(cpp_torch_tests)
endif()

if(CPP_TORCH_BUILD_BENCHMARKS)
  include(FetchContent)

  set(BENCHMARK_ENABLE_TESTING OFF CACHE BOOL "" FORCE)
  set(BENCHMARK_ENABLE_GTEST_TESTS OFF CACHE BOOL "" FORCE)
  set(BENCHMARK_ENABLE_INSTALL OFF CACHE BOOL "" FORCE)

  FetchContent_Declare(
    google_benchmark
    URL
      https://github.com/google/benchmark/archive/192ef10025eb2c4cdd392bc502f0c852196baa48.zip
    DOWNLOAD_EXTRACT_TIMESTAMP TRUE
  )

  FetchContent_MakeAvailable(google_benchmark)

  add_executable(
    cpp_torch_benchmarks
    benchmarks/vector_sum_benchmark.cpp
  )

  target_compile_features(cpp_torch_benchmarks PRIVATE cxx_std_23)

  target_link_libraries(
    cpp_torch_benchmarks
    PRIVATE
      cpp_torch_warnings
      benchmark::benchmark_main
  )
endif()
