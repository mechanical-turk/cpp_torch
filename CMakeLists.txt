cmake_minimum_required(VERSION 3.26)
project(cpp_torch LANGUAGES CXX)

option(
  CPP_TORCH_ENABLE_SANITIZERS
  "Enable AddressSanitizer and UndefinedBehaviorSanitizer"
  OFF
)

include(CTest)

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
target_include_directories(
  cpp_torch
  PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/include
)

if(CPP_TORCH_ENABLE_SANITIZERS)
  target_link_libraries(cpp_torch PUBLIC cpp_torch_sanitizers)
endif()

add_executable(basic_usage examples/basic_usage.cpp)
target_link_libraries(basic_usage PRIVATE cpp_torch)

if(BUILD_TESTING)
  include(FetchContent)

  FetchContent_Declare(
    googletest
    URL
      https://github.com/google/googletest/archive/52eb8108c5bdec04579160ae17225d66034bd723.zip
    DOWNLOAD_EXTRACT_TIMESTAMP TRUE
  )

  FetchContent_MakeAvailable(googletest)

  add_executable(cpp_torch_tests tests/math_test.cpp)

  target_link_libraries(
    cpp_torch_tests
    PRIVATE
      cpp_torch
      GTest::gtest_main
  )

  include(GoogleTest)
  gtest_discover_tests(cpp_torch_tests)
endif()