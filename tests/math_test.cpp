#include <cpp_torch/math.hpp>

#include <gtest/gtest.h>

TEST(MathTest, AddTwoIntegers) {
  EXPECT_EQ(cpp_torch::add(2, 3), 5);
}