#include <cpp_torch/tensor.hpp>

#include <gtest/gtest.h>

#include <array>
#include <cstddef>
#include <limits>
#include <stdexcept>
#include <utility>

namespace {

using cpp_torch::Tensor;

TEST(TensorTest, PreservesShapeRankAndElementCount) {
  const Tensor tensor({2, 3}, {1.0, 2.0, 3.0, 4.0, 5.0, 6.0});

  EXPECT_EQ(tensor.shape(), (std::vector<std::size_t> {2, 3}));
  EXPECT_EQ(tensor.rank(), 2);
  EXPECT_EQ(tensor.numel(), 6);
}

TEST(TensorTest, SupportsCheckedReadAndMutation) {
  Tensor tensor({2, 3}, {1.0, 2.0, 3.0, 4.0, 5.0, 6.0});

  EXPECT_DOUBLE_EQ(tensor.at({{0, 0}}), 1.0);
  EXPECT_DOUBLE_EQ(tensor.at({{1, 2}}), 6.0);

  tensor.at({{1, 2}}) = 42.0;
  EXPECT_DOUBLE_EQ(tensor.at({{1, 2}}), 42.0);
}

TEST(TensorTest, EnforcesConstructionAndIndexingContracts) {
  EXPECT_THROW((Tensor({2, 3}, {1.0})), std::invalid_argument);
  EXPECT_THROW(
      (Tensor({std::numeric_limits<std::size_t>::max(), 2}, {})),
      std::overflow_error
  );

  const Tensor tensor({2, 3}, {1.0, 2.0, 3.0, 4.0, 5.0, 6.0});
  EXPECT_THROW(tensor.at({{0}}), std::invalid_argument);
  EXPECT_THROW(tensor.at({{0, 3}}), std::out_of_range);
}

TEST(TensorTest, DistinguishesScalarSingletonAndEmptyShapes) {
  const Tensor scalar({}, {7.0});
  const Tensor singleton({1}, {8.0});
  const Tensor empty({0}, {});

  EXPECT_EQ(scalar.rank(), 0);
  EXPECT_EQ(scalar.numel(), 1);
  EXPECT_DOUBLE_EQ(scalar.at({}), 7.0);

  EXPECT_EQ(singleton.rank(), 1);
  EXPECT_EQ(singleton.numel(), 1);
  EXPECT_DOUBLE_EQ(singleton.at({{0}}), 8.0);

  EXPECT_EQ(empty.rank(), 1);
  EXPECT_EQ(empty.numel(), 0);
  EXPECT_THROW(empty.at({{0}}), std::out_of_range);
  EXPECT_DOUBLE_EQ(empty.sum().at({}), 0.0);
}

TEST(TensorTest, CopiesIndependentlyAndCanReuseMovedFromObject) {
  Tensor original({2}, {10.0, 20.0});
  Tensor copy = original;
  copy.at({{0}}) = 99.0;

  EXPECT_DOUBLE_EQ(original.at({{0}}), 10.0);
  EXPECT_DOUBLE_EQ(copy.at({{0}}), 99.0);

  Tensor destination = std::move(original);
  EXPECT_DOUBLE_EQ(destination.at({{1}}), 20.0);

  original = Tensor({1}, {15.0});
  EXPECT_DOUBLE_EQ(original.at({{0}}), 15.0);
}

TEST(TensorTest, CopyAssignmentProducesIndependentStorage) {
  Tensor source({2}, {10.0, 20.0});
  Tensor assigned({1}, {-1.0});

  assigned = source;
  assigned.at({{0}}) = 99.0;

  EXPECT_EQ(assigned.shape(), source.shape());
  EXPECT_DOUBLE_EQ(source.at({{0}}), 10.0);
  EXPECT_DOUBLE_EQ(assigned.at({{0}}), 99.0);
}

TEST(TensorTest, TransposeMapsCoordinatesWithoutCopyingStorage) {
  Tensor original({2, 3}, {1.0, 2.0, 3.0, 4.0, 5.0, 6.0});
  Tensor transposed = original.T();

  EXPECT_EQ(transposed.shape(), (std::vector<std::size_t> {3, 2}));
  EXPECT_DOUBLE_EQ(transposed.at({{0, 0}}), 1.0);
  EXPECT_DOUBLE_EQ(transposed.at({{0, 1}}), 4.0);
  EXPECT_DOUBLE_EQ(transposed.at({{2, 1}}), 6.0);

  transposed.at({{1, 0}}) = 99.0;
  EXPECT_DOUBLE_EQ(original.at({{0, 1}}), 99.0);

  original.at({{1, 2}}) = 42.0;
  EXPECT_DOUBLE_EQ(transposed.at({{2, 1}}), 42.0);
}

TEST(TensorTest, CopyingTransposeMaterializesIndependentLogicalValues) {
  Tensor original({2, 3}, {1.0, 2.0, 3.0, 4.0, 5.0, 6.0});
  Tensor transposed = original.T();
  Tensor copy = transposed;

  EXPECT_EQ(copy.shape(), (std::vector<std::size_t> {3, 2}));
  EXPECT_DOUBLE_EQ(copy.at({{0, 0}}), 1.0);
  EXPECT_DOUBLE_EQ(copy.at({{0, 1}}), 4.0);
  EXPECT_DOUBLE_EQ(copy.at({{2, 1}}), 6.0);

  copy.at({{0, 1}}) = 99.0;
  EXPECT_DOUBLE_EQ(transposed.at({{0, 1}}), 4.0);
  EXPECT_DOUBLE_EQ(original.at({{1, 0}}), 4.0);
}

TEST(TensorTest, RejectsTransposeOutsideRankTwo) {
  const Tensor vector({2}, {1.0, 2.0});

  EXPECT_THROW(vector.T(), std::invalid_argument);
}

TEST(TensorTest, ComputesElementwiseOperationsInLogicalViewOrder) {
  const Tensor left({2, 3}, {1.0, 2.0, 3.0, 4.0, 5.0, 6.0});
  const Tensor right({2, 3}, {10.0, 20.0, 30.0, 40.0, 50.0, 60.0});

  const Tensor sum = left.T() + right.T();
  EXPECT_EQ(sum.shape(), (std::vector<std::size_t> {3, 2}));
  EXPECT_DOUBLE_EQ(sum.at({{0, 0}}), 11.0);
  EXPECT_DOUBLE_EQ(sum.at({{0, 1}}), 44.0);
  EXPECT_DOUBLE_EQ(sum.at({{1, 0}}), 22.0);
  EXPECT_DOUBLE_EQ(sum.at({{1, 1}}), 55.0);
  EXPECT_DOUBLE_EQ(sum.at({{2, 0}}), 33.0);
  EXPECT_DOUBLE_EQ(sum.at({{2, 1}}), 66.0);

  const Tensor product = left.T() * right.T();
  EXPECT_DOUBLE_EQ(product.at({{0, 1}}), 160.0);
  EXPECT_DOUBLE_EQ(product.at({{2, 0}}), 90.0);
}

TEST(TensorTest, SelectCreatesAliasingSubsetViewsAcrossAxes) {
  Tensor tensor(
      {2, 3, 4},
      {
          0.0,
          1.0,
          2.0,
          3.0,
          4.0,
          5.0,
          6.0,
          7.0,
          8.0,
          9.0,
          10.0,
          11.0,
          12.0,
          13.0,
          14.0,
          15.0,
          16.0,
          17.0,
          18.0,
          19.0,
          20.0,
          21.0,
          22.0,
          23.0,
      }
  );

  Tensor middle_axis = tensor.select(1, 2);
  EXPECT_EQ(middle_axis.shape(), (std::vector<std::size_t> {2, 4}));
  EXPECT_DOUBLE_EQ(middle_axis.at({{0, 0}}), 8.0);
  EXPECT_DOUBLE_EQ(middle_axis.at({{1, 3}}), 23.0);

  Tensor last_axis = tensor.select(2, 1);
  EXPECT_EQ(last_axis.shape(), (std::vector<std::size_t> {2, 3}));
  EXPECT_DOUBLE_EQ(last_axis.at({{0, 0}}), 1.0);
  EXPECT_DOUBLE_EQ(last_axis.at({{0, 2}}), 9.0);
  EXPECT_DOUBLE_EQ(last_axis.at({{1, 2}}), 21.0);

  middle_axis.at({{1, 3}}) = 99.0;
  EXPECT_DOUBLE_EQ(tensor.at({{1, 2, 3}}), 99.0);
}

TEST(TensorTest, SelectSupportsSubsetComputationAndScalarResults) {
  const Tensor left({2, 3}, {1.0, 2.0, 3.0, 4.0, 5.0, 6.0});
  const Tensor right({2, 3}, {10.0, 20.0, 30.0, 40.0, 50.0, 60.0});

  const Tensor left_column = left.select(1, 1);
  const Tensor right_column = right.select(1, 1);
  EXPECT_DOUBLE_EQ(left_column.sum().at({}), 7.0);

  const Tensor column_sum = left_column + right_column;
  EXPECT_EQ(column_sum.shape(), (std::vector<std::size_t> {2}));
  EXPECT_DOUBLE_EQ(column_sum.at({{0}}), 22.0);
  EXPECT_DOUBLE_EQ(column_sum.at({{1}}), 55.0);

  const Tensor scalar = left.select(0, 1).select(0, 2);
  EXPECT_EQ(scalar.shape(), (std::vector<std::size_t> {}));
  EXPECT_DOUBLE_EQ(scalar.at({}), 6.0);
}

TEST(TensorTest, SelectRejectsInvalidAxisAndIndex) {
  const Tensor tensor({2, 3}, {1.0, 2.0, 3.0, 4.0, 5.0, 6.0});
  const Tensor scalar({}, {1.0});

  EXPECT_THROW(tensor.select(2, 0), std::invalid_argument);
  EXPECT_THROW(tensor.select(1, 3), std::invalid_argument);
  EXPECT_THROW(scalar.select(0, 0), std::invalid_argument);
}

TEST(TensorTest, IdentifiesContiguousAndNonContiguousLayouts) {
  const Tensor tensor({2, 3}, {1.0, 2.0, 3.0, 4.0, 5.0, 6.0});

  EXPECT_TRUE(tensor.is_contiguous());
  EXPECT_FALSE(tensor.T().is_contiguous());
  EXPECT_TRUE(tensor.select(0, 1).is_contiguous());
  EXPECT_FALSE(tensor.select(1, 1).is_contiguous());

  const Tensor size_one_axis({1, 3}, {1.0, 2.0, 3.0});
  EXPECT_TRUE(size_one_axis.T().is_contiguous());

  const Tensor scalar({}, {1.0});
  const Tensor empty({2, 0, 3}, {});
  EXPECT_TRUE(scalar.is_contiguous());
  EXPECT_TRUE(empty.is_contiguous());
}

TEST(TensorTest, ComputesRectangularMatrixMultiplication) {
  const Tensor left({2, 3}, {1.0, 2.0, 3.0, 4.0, 5.0, 6.0});
  const Tensor right(
      {3, 4},
      {
          1.0,
          2.0,
          3.0,
          4.0,
          5.0,
          6.0,
          7.0,
          8.0,
          9.0,
          10.0,
          11.0,
          12.0,
      }
  );

  const Tensor result = left.matmul(right);

  EXPECT_EQ(result.shape(), (std::vector<std::size_t> {2, 4}));
  EXPECT_DOUBLE_EQ(result.at({{0, 0}}), 38.0);
  EXPECT_DOUBLE_EQ(result.at({{0, 1}}), 44.0);
  EXPECT_DOUBLE_EQ(result.at({{0, 2}}), 50.0);
  EXPECT_DOUBLE_EQ(result.at({{0, 3}}), 56.0);
  EXPECT_DOUBLE_EQ(result.at({{1, 0}}), 83.0);
  EXPECT_DOUBLE_EQ(result.at({{1, 1}}), 98.0);
  EXPECT_DOUBLE_EQ(result.at({{1, 2}}), 113.0);
  EXPECT_DOUBLE_EQ(result.at({{1, 3}}), 128.0);
}

TEST(TensorTest, MatrixMultiplicationSupportsNonContiguousInputs) {
  const Tensor left_source({3, 2}, {1.0, 4.0, 2.0, 5.0, 3.0, 6.0});
  const Tensor right_source({2, 3}, {7.0, 9.0, 11.0, 8.0, 10.0, 12.0});

  const Tensor result = left_source.T().matmul(right_source.T());

  EXPECT_EQ(result.shape(), (std::vector<std::size_t> {2, 2}));
  EXPECT_DOUBLE_EQ(result.at({{0, 0}}), 58.0);
  EXPECT_DOUBLE_EQ(result.at({{0, 1}}), 64.0);
  EXPECT_DOUBLE_EQ(result.at({{1, 0}}), 139.0);
  EXPECT_DOUBLE_EQ(result.at({{1, 1}}), 154.0);
}

TEST(TensorTest, MatrixMultiplicationHandlesZeroSizedDimensions) {
  const Tensor zero_inner_left({2, 0}, {});
  const Tensor zero_inner_right({0, 4}, {});
  const Tensor zero_inner_result = zero_inner_left.matmul(zero_inner_right);

  EXPECT_EQ(zero_inner_result.shape(), (std::vector<std::size_t> {2, 4}));
  EXPECT_EQ(zero_inner_result.numel(), 8);
  for (std::size_t row = 0; row < 2; ++row) {
    for (std::size_t column = 0; column < 4; ++column) {
      EXPECT_DOUBLE_EQ(zero_inner_result.at({{row, column}}), 0.0);
    }
  }

  const Tensor zero_rows({0, 3}, {});
  const Tensor right({3, 4}, std::vector<double>(12, 1.0));
  const Tensor zero_row_result = zero_rows.matmul(right);
  EXPECT_EQ(zero_row_result.shape(), (std::vector<std::size_t> {0, 4}));
  EXPECT_EQ(zero_row_result.numel(), 0);

  const Tensor left({2, 3}, std::vector<double>(6, 1.0));
  const Tensor zero_columns({3, 0}, {});
  const Tensor zero_column_result = left.matmul(zero_columns);
  EXPECT_EQ(zero_column_result.shape(), (std::vector<std::size_t> {2, 0}));
  EXPECT_EQ(zero_column_result.numel(), 0);
}

TEST(TensorTest, MatrixMultiplicationRejectsInvalidInputsAndOutputOverflow) {
  const Tensor vector({3}, {1.0, 2.0, 3.0});
  const Tensor matrix({3, 2}, {1.0, 2.0, 3.0, 4.0, 5.0, 6.0});
  const Tensor incompatible({4, 2}, std::vector<double>(8, 1.0));

  EXPECT_THROW(vector.matmul(matrix), std::invalid_argument);
  EXPECT_THROW(matrix.matmul(incompatible), std::invalid_argument);

  const Tensor huge_zero_inner(
      {std::numeric_limits<std::size_t>::max(), 0},
      {}
  );
  const Tensor two_output_columns({0, 2}, {});
  EXPECT_THROW(
      huge_zero_inner.matmul(two_output_columns),
      std::overflow_error
  );
}

TEST(TensorTest, ComputesReferenceElementwiseAndReductionOperations) {
  const Tensor left({2}, {2.0, 3.0});
  const Tensor right({2}, {1.0, 4.0});

  const Tensor sum = left + right;
  EXPECT_DOUBLE_EQ(sum.at({{0}}), 3.0);
  EXPECT_DOUBLE_EQ(sum.at({{1}}), 7.0);

  const Tensor product = left * right;
  EXPECT_DOUBLE_EQ(product.at({{0}}), 2.0);
  EXPECT_DOUBLE_EQ(product.at({{1}}), 12.0);

  EXPECT_DOUBLE_EQ(left.sum().at({}), 5.0);
  EXPECT_DOUBLE_EQ(left.dot(right).at({}), 14.0);
}

TEST(TensorTest, BroadcastsTrailingAndSizeOneDimensions) {
  const Tensor matrix({2, 3}, {1.0, 2.0, 3.0, 4.0, 5.0, 6.0});
  const Tensor bias({3}, {10.0, 20.0, 30.0});

  const Tensor biased = matrix + bias;
  EXPECT_EQ(biased.shape(), (std::vector<std::size_t> {2, 3}));
  EXPECT_DOUBLE_EQ(biased.at({{0, 0}}), 11.0);
  EXPECT_DOUBLE_EQ(biased.at({{0, 2}}), 33.0);
  EXPECT_DOUBLE_EQ(biased.at({{1, 0}}), 14.0);
  EXPECT_DOUBLE_EQ(biased.at({{1, 2}}), 36.0);

  const Tensor rank_three(
      {2, 3, 2},
      {
          0.0,
          1.0,
          2.0,
          3.0,
          4.0,
          5.0,
          6.0,
          7.0,
          8.0,
          9.0,
          10.0,
          11.0,
      }
  );
  const Tensor column({3, 1}, {10.0, 20.0, 30.0});

  const Tensor broadcast = rank_three + column;
  EXPECT_EQ(broadcast.shape(), (std::vector<std::size_t> {2, 3, 2}));
  EXPECT_DOUBLE_EQ(broadcast.at({{0, 0, 1}}), 11.0);
  EXPECT_DOUBLE_EQ(broadcast.at({{0, 1, 1}}), 23.0);
  EXPECT_DOUBLE_EQ(broadcast.at({{1, 2, 0}}), 40.0);
  EXPECT_DOUBLE_EQ(broadcast.at({{1, 2, 1}}), 41.0);
}

TEST(TensorTest, BroadcastsScalarsViewsAndEmptyDimensions) {
  const Tensor scalar({}, {2.0});
  const Tensor matrix({2, 2}, {1.0, 2.0, 3.0, 4.0});

  const Tensor scaled = scalar * matrix;
  EXPECT_EQ(scaled.shape(), (std::vector<std::size_t> {2, 2}));
  EXPECT_DOUBLE_EQ(scaled.at({{0, 1}}), 4.0);
  EXPECT_DOUBLE_EQ(scaled.at({{1, 1}}), 8.0);

  const Tensor source({2, 3}, {1.0, 2.0, 3.0, 4.0, 5.0, 6.0});
  const Tensor bias({2}, {10.0, 20.0});
  const Tensor view_result = source.T() + bias;
  EXPECT_EQ(view_result.shape(), (std::vector<std::size_t> {3, 2}));
  EXPECT_DOUBLE_EQ(view_result.at({{0, 0}}), 11.0);
  EXPECT_DOUBLE_EQ(view_result.at({{0, 1}}), 24.0);
  EXPECT_DOUBLE_EQ(view_result.at({{2, 0}}), 13.0);
  EXPECT_DOUBLE_EQ(view_result.at({{2, 1}}), 26.0);

  const Tensor empty({2, 0, 3}, {});
  const Tensor trailing({1, 3}, {10.0, 20.0, 30.0});
  const Tensor empty_result = empty + trailing;
  EXPECT_EQ(empty_result.shape(), (std::vector<std::size_t> {2, 0, 3}));
  EXPECT_EQ(empty_result.numel(), 0);
}

TEST(TensorTest, RejectsInvalidElementwiseAndDotOperands) {
  const Tensor vector({2}, {1.0, 2.0});
  const Tensor incompatible({3}, {1.0, 2.0, 3.0});
  const Tensor matrix({1, 2}, {1.0, 2.0});

  EXPECT_THROW(vector + incompatible, std::invalid_argument);
  EXPECT_THROW(vector * incompatible, std::invalid_argument);
  EXPECT_THROW(matrix.dot(matrix), std::invalid_argument);
}

} // namespace
