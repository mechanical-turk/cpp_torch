#include <cpp_torch/tensor.hpp>

#include <benchmark/benchmark.h>

#include <cstddef>
#include <vector>

namespace {

using cpp_torch::Tensor;

Tensor make_square_tensor(
    std::size_t side
) {
  const std::size_t element_count = side * side;
  return Tensor({side, side}, std::vector<double>(element_count, 1.0));
}

void advance_index(
    std::vector<std::size_t>& index,
    const std::vector<std::size_t>& shape
) {
  for (std::size_t i = index.size(); i > 0; --i) {
    const std::size_t axis = i - 1;
    ++index[axis];
    if (index[axis] < shape[axis]) {
      return;
    }
    index[axis] = 0;
  }
}

double sum_raw_layout(
    const std::vector<double>& storage,
    const std::vector<std::size_t>& shape,
    const std::vector<std::size_t>& strides
) {
  std::vector<std::size_t> index(shape.size());
  double result = 0.0;

  for (std::size_t element = 0; element < storage.size(); ++element) {
    std::size_t physical_index = 0;
    for (std::size_t axis = 0; axis < shape.size(); ++axis) {
      physical_index += index[axis] * strides[axis];
    }

    result += storage[physical_index];
    advance_index(index, shape);
  }

  return result;
}

void BM_TensorSumContiguous(
    benchmark::State& state
) {
  const std::size_t side = static_cast<std::size_t>(state.range(0));
  const Tensor tensor = make_square_tensor(side);

  for (auto _ : state) {
    Tensor result = tensor.sum();
    benchmark::DoNotOptimize(result.at({}));
  }
}

void BM_TensorSumTranspose(
    benchmark::State& state
) {
  const std::size_t side = static_cast<std::size_t>(state.range(0));
  const Tensor tensor = make_square_tensor(side);
  const Tensor transpose = tensor.T();

  for (auto _ : state) {
    Tensor result = transpose.sum();
    benchmark::DoNotOptimize(result.at({}));
  }
}

void BM_RawSumContiguous(
    benchmark::State& state
) {
  const std::size_t side = static_cast<std::size_t>(state.range(0));
  const std::size_t element_count = side * side;
  const std::vector<double> storage(element_count, 1.0);
  const std::vector<std::size_t> shape {side, side};
  const std::vector<std::size_t> strides {side, 1};

  for (auto _ : state) {
    double result = sum_raw_layout(storage, shape, strides);
    benchmark::DoNotOptimize(result);
  }
}

void BM_RawSumTranspose(
    benchmark::State& state
) {
  const std::size_t side = static_cast<std::size_t>(state.range(0));
  const std::size_t element_count = side * side;
  const std::vector<double> storage(element_count, 1.0);
  const std::vector<std::size_t> shape {side, side};
  const std::vector<std::size_t> strides {1, side};

  for (auto _ : state) {
    double result = sum_raw_layout(storage, shape, strides);
    benchmark::DoNotOptimize(result);
  }
}

BENCHMARK(BM_TensorSumContiguous)->Arg(16)->Arg(64)->Arg(256)->Arg(1024)->Arg(2048);
BENCHMARK(BM_TensorSumTranspose)->Arg(16)->Arg(64)->Arg(256)->Arg(1024)->Arg(2048);
BENCHMARK(BM_RawSumContiguous)->Arg(16)->Arg(64)->Arg(256)->Arg(1024)->Arg(2048);
BENCHMARK(BM_RawSumTranspose)->Arg(16)->Arg(64)->Arg(256)->Arg(1024)->Arg(2048);

} // namespace
