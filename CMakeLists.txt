cmake_minimum_required(VERSION 3.26)
project(cpp_torch LANGUAGES CXX)

add_library(cpp_torch src/math.cpp)
target_compile_features(cpp_torch PUBLIC cxx_std_23)
target_include_directories(
  cpp_torch
  PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/include
)

add_executable(basic_usage examples/basic_usage.cpp)
target_link_libraries(basic_usage PRIVATE cpp_torch)
