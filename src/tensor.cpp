#include <cpp_torch/tensor.hpp>
#include <cstddef>
#include <limits>
#include <span>
#include <stdexcept>
#include <utility>
#include <vector>

using cpp_torch::Tensor;

Tensor::Tensor(
    std::vector<std::size_t> shape,
    std::vector<double> storage
)
    : shape_(std::move(shape)), storage_(std::move(storage)) {
  if (numel() != storage_.size()) {
    throw std::invalid_argument("storage vector does not match shape");
  }
}

const std::vector<std::size_t>& Tensor::shape() const {
  return shape_;
}

const std::vector<double>& Tensor::storage() const {
  return storage_;
}

std::size_t Tensor::numel() const {
  for (std::size_t dim : shape_) {
    if (dim == 0)
      return 0;
  }

  std::size_t num = 1;

  for (std::size_t dim : shape_) {
    if (dim > std::numeric_limits<std::size_t>::max() / num) {
      throw std::overflow_error("numel overflow");
    }
    num *= dim;
  }

  return num;
}

std::size_t Tensor::rank() const {
  return shape_.size();
}

double& Tensor::at(
    std::span<const std::size_t> indices
) {
  std::size_t idx = storage_idx(indices);
  return storage_[idx];
}

const double& Tensor::at(
    std::span<const std::size_t> indices
) const {
  std::size_t idx = storage_idx(indices);
  return storage_[idx];
}

const std::vector<std::size_t> Tensor::strides() const {
  const std::size_t sz = rank();
  if (sz == 0)
    return {};

  std::vector<std::size_t> result(rank());
  result[sz - 1] = 1;

  for (std::size_t i = sz - 1; i > 0; --i) {
    result[i - 1] = shape_[i] * result[i];
  }
  return result;
}

std::size_t Tensor::storage_idx(
    std::span<const std::size_t> indices
) const {
  std::size_t r = rank();
  if (indices.size() != r) {
    throw std::invalid_argument("indices must match rank");
  }
  std::vector<std::size_t> s = strides();
  std::size_t ans = 0;
  for (std::size_t i = 0; i < r; ++i) {
    if (indices[i] >= shape_[i]) {
      throw std::out_of_range("indices don't match shape");
    }
    ans += indices[i] * s[i];
  }
  return ans;
}
