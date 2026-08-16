#include <algorithm>
#include <cpp_torch/tensor.hpp>
#include <cstddef>
#include <limits>
#include <memory>
#include <span>
#include <stdexcept>
#include <utility>
#include <vector>

using cpp_torch::Tensor;

namespace {

std::vector<std::size_t> get_output_shape_from_right_aligned_shapes(
    const std::vector<std::size_t>& a,
    const std::vector<std::size_t>& b
) {
  if (a.size() != b.size()) {
    throw std::invalid_argument("right aligned shapes must match");
  }
  std::size_t sz = a.size();
  std::vector<std::size_t> output_shape(sz);
  for (std::size_t i = 0; i < sz; ++i) {
    if (a[i] == 1) {
      output_shape[i] = b[i];
    } else if (b[i] == 1) {
      output_shape[i] = a[i];
    } else if (a[i] == b[i]) {
      output_shape[i] = a[i];
    } else {
      throw std::invalid_argument(
          "incompatible dimensions in right aligned shapes"
      );
    }
  }
  return output_shape;
}

std::vector<std::size_t> get_effective_strides(
    const std::vector<std::size_t>& operand_shape,
    const std::vector<std::size_t>& operand_strides,
    std::size_t output_rank
) {
  if (operand_shape.size() != operand_strides.size()) {
    throw std::invalid_argument(
        "operand shape and strides must have equal rank"
    );
  }
  if (operand_shape.size() > output_rank) {
    throw std::invalid_argument("operand rank cannot exceed output rank");
  }

  std::vector<std::size_t> effective_strides(output_rank, 0);
  const std::size_t leading_padding = output_rank - operand_shape.size();

  for (std::size_t axis = 0; axis < operand_shape.size(); ++axis) {
    if (operand_shape[axis] != 1) {
      effective_strides[leading_padding + axis] = operand_strides[axis];
    }
  }
  return effective_strides;
}

void advance_index(
    std::vector<std::size_t>& idx,
    const std::vector<std::size_t>& shape
) {
  // assuming validated idx and shape size
  // and assuming shape is non scalar
  // and assuming numel != 0
  for (std::size_t i = idx.size(); i > 0; --i) {
    const std::size_t axis = i - 1;
    ++idx[axis];
    if (idx[axis] < shape[axis]) {
      return;
    }
    idx[axis] = 0;
  }
}

std::size_t get_output_size_from_shape(
    const std::vector<std::size_t>& shape
) {
  std::size_t result = 1;
  for (std::size_t dim : shape) {
    if (dim == 0) {
      return 0;
    }
    if (dim > std::numeric_limits<std::size_t>::max() / result) {
      throw std::overflow_error("broadcast output size overflow");
    }
    result *= dim;
  }
  return result;
}

template <typename T>
T dot_(
    const std::vector<T>& a,
    const std::vector<T>& b
) {
  if (a.size() != b.size()) {
    throw std::invalid_argument(
        "dot undefined over vectors of different sizes"
    );
  }
  T result = 0;
  std::size_t sz = a.size();
  for (std::size_t i = 0; i < sz; ++i) {
    result += a[i] * b[i];
  }
  return result;
}

std::pair<std::vector<std::size_t>, std::vector<std::size_t>> right_align(
    const std::vector<std::size_t>& shape_a,
    const std::vector<std::size_t>& shape_b
) {
  std::vector<std::size_t> new_a;
  std::vector<std::size_t> new_b;

  auto it_a = shape_a.rbegin();
  auto it_b = shape_b.rbegin();
  auto end_a = shape_a.rend();
  auto end_b = shape_b.rend();

  while (it_a != end_a || it_b != end_b) {
    std::size_t a_val = 1;
    std::size_t b_val = 1;
    if (it_a != end_a) {
      a_val = *it_a;
      ++it_a;
    }
    if (it_b != end_b) {
      b_val = *it_b;
      ++it_b;
    }
    new_a.push_back(a_val);
    new_b.push_back(b_val);
  }
  std::reverse(new_a.begin(), new_a.end());
  std::reverse(new_b.begin(), new_b.end());

  return {std::move(new_a), std::move(new_b)};
}

std::vector<std::size_t> make_contiguous_strides(
    std::span<const std::size_t> shape
) {
  if (shape.empty()) {
    return {};
  }

  std::vector<std::size_t> strides(shape.size());
  strides.back() = 1;

  for (std::size_t i = shape.size() - 1; i > 0; --i) {
    strides[i - 1] = shape[i] * strides[i];
  }

  return strides;
}

} // namespace

Tensor::Tensor(
    std::vector<std::size_t> shape,
    std::vector<double> storage
)
    : shape_(std::move(shape)),
      storage_(std::make_shared<std::vector<double>>(std::move(storage))) {
  if (numel() != storage_->size()) {
    throw std::invalid_argument("storage vector does not match shape");
  }
  strides_ = make_contiguous_strides(shape_);
}

const std::vector<std::size_t>& Tensor::shape() const {
  return shape_;
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
  return (*storage_)[idx];
}

const double& Tensor::at(
    std::span<const std::size_t> indices
) const {
  std::size_t idx = storage_idx(indices);
  return (*storage_)[idx];
}

Tensor Tensor::operator+(
    const Tensor& right
) const {
  auto op = [](double a, double b) { return a + b; };
  return elementwise_binary(right, op);
}

Tensor Tensor::operator*(
    const Tensor& right
) const {
  auto op = [](double a, double b) { return a * b; };
  return elementwise_binary(right, op);
}

Tensor Tensor::sum() const {
  double sum = 0.0;
  std::vector<std::size_t> idx(rank());
  const std::size_t n = numel();
  for (std::size_t i = 0; i < n; ++i) {
    sum += at(idx);
    advance_index(idx, shape_);
  }
  return Tensor({}, {sum});
}

Tensor Tensor::dot(
    const Tensor& right
) const {
  if (rank() != 1) {
    throw std::invalid_argument("dot undefined when rank != 1");
  }
  return (*this * right).sum();
}

Tensor::Tensor(
    const Tensor& other
)
    : Tensor(other.shape_, other.materialize()) {
}
Tensor& Tensor::operator=(
    const Tensor& other
) {
  Tensor copy = other;
  std::swap(*this, copy);
  return *this;
};

Tensor Tensor::T() const {
  if (rank() != 2) {
    throw std::invalid_argument("not implemented when rank != 2");
  }
  return Tensor(
      {{shape_[1], shape_[0]}}, storage_, {{strides_[1], strides_[0]}}, offset_
  );
}

Tensor Tensor::select(
    std::size_t axis,
    std::size_t index
) const {
  std::size_t old_rank = rank();
  if (axis >= old_rank) {
    throw std::invalid_argument("axis must be less than rank");
  }
  if (index >= shape_[axis]) {
    throw std::invalid_argument("index must be less than extent");
  }

  std::vector<std::size_t> new_shape;
  new_shape.reserve(old_rank - 1);
  for (std::size_t r = 0; r < old_rank; ++r) {
    if (r != axis) {
      new_shape.push_back(shape_[r]);
    }
  }

  std::vector<std::size_t> new_strides;
  new_strides.reserve(old_rank - 1);
  for (std::size_t r = 0; r < old_rank; ++r) {
    if (r != axis) {
      new_strides.push_back(strides_[r]);
    }
  }

  std::size_t new_offset = offset_ + index * strides_[axis];

  return Tensor(new_shape, storage_, new_strides, new_offset);
}

[[nodiscard]] bool Tensor::is_contiguous() const {
  std::size_t n = numel();
  if (n <= 1)
    return true;
  std::size_t expected_stride = 1;
  std::size_t r = rank();
  for (std::size_t dim = r; dim > 0; --dim) {
    if (shape_[dim - 1] == 1)
      continue;
    if (strides_[dim - 1] != expected_stride)
      return false;
    expected_stride *= shape_[dim - 1];
  }
  return true;
}

Tensor Tensor::matmul(
    const Tensor& right
) const {
  if (rank() != 2 || right.rank() != 2) {
    throw std::invalid_argument("matmul is only defined for rank 2 tensors");
  }
  if (shape_[1] != right.shape_[0]) {
    throw std::invalid_argument("mismatched number of rows and columns");
  }

  std::size_t rows = shape_[0];
  std::size_t cols = right.shape_[1];
  if (rows != 0 && cols > std::numeric_limits<std::size_t>::max() / rows) {
    throw std::overflow_error("matmul output size overflow");
  }
  std::vector<double> new_storage(rows * cols, 0);
  std::vector<std::size_t> new_shape = {rows, cols};
  for (std::size_t i = 0; i < rows; ++i) {
    for (std::size_t j = 0; j < cols; ++j) {
      double sum = 0;
      for (std::size_t k = 0; k < shape_[1]; ++k) {
        sum += at({{i, k}}) * right.at({{k, j}});
      }
      new_storage[i * cols + j] = sum;
    }
  }
  return Tensor(new_shape, new_storage);
}

// private

std::size_t Tensor::storage_idx(
    std::span<const std::size_t> indices
) const {
  std::size_t r = rank();
  if (indices.size() != r) {
    throw std::invalid_argument("indices must match rank");
  }
  std::size_t ans = 0;
  for (std::size_t i = 0; i < r; ++i) {
    if (indices[i] >= shape_[i]) {
      throw std::out_of_range("indices don't match shape");
    }
    ans += indices[i] * strides_[i];
  }
  return offset_ + ans;
}

std::vector<double> Tensor::materialize() const {
  std::size_t n = numel();
  if (n == 0) {
    return {};
  }
  std::vector<double> result(n);
  std::vector<std::size_t> idx(rank());
  for (std::size_t i = 0; i < n; ++i) {
    result[i] = this->at(idx);
    advance_index(idx, shape_);
  }
  return result;
}

Tensor Tensor::elementwise_binary(
    const Tensor& right,
    auto operation
) const {
  const auto& [aligned_shape_left, aligned_shape_right] =
      right_align(shape_, right.shape_);

  std::vector<std::size_t> output_shape =
      get_output_shape_from_right_aligned_shapes(
          aligned_shape_left, aligned_shape_right
      );

  const std::vector<std::size_t>& effective_stride_left =
      get_effective_strides(shape_, strides_, output_shape.size());

  const std::vector<std::size_t>& effective_stride_right =
      get_effective_strides(right.shape_, right.strides_, output_shape.size());

  std::size_t output_sz = get_output_size_from_shape(output_shape);
  std::vector<double> output_storage(output_sz);
  std::vector<std::size_t> output_logical_idx(output_shape.size());

  for (std::size_t i = 0; i < output_sz; ++i) {
    std::size_t left_index =
        offset_ + dot_(output_logical_idx, effective_stride_left);
    std::size_t right_index =
        right.offset_ + dot_(output_logical_idx, effective_stride_right);

    output_storage[i] =
        operation((*storage_)[left_index], (*right.storage_)[right_index]);
    advance_index(output_logical_idx, output_shape);
  }

  return Tensor(std::move(output_shape), std::move(output_storage));
}

Tensor::Tensor(
    std::vector<std::size_t> shape,
    std::shared_ptr<std::vector<double>> storage,
    std::vector<std::size_t> strides,
    std::size_t offset
)
    : shape_(std::move(shape)), strides_(std::move(strides)),
      storage_(std::move(storage)), offset_(offset) {
  if (shape_.size() != strides_.size()) {
    throw std::invalid_argument("shape and strides must have equal rank");
  }
  if (!storage_) {
    throw std::invalid_argument("storage can't be null");
  }
  if (numel() == 0) {
    if (offset_ > storage_->size()) {
      throw std::invalid_argument("invalid offset");
    }
    return;
  }
  if (offset_ >= storage_->size()) {
    throw std::invalid_argument("invalid offset");
  }
  std::size_t budget = (storage_->size() - 1) - offset_;
  std::size_t r = rank();
  for (std::size_t idx = 0; idx < r; ++idx) {
    std::size_t d = shape_[idx];
    if (d == 0 || strides_[idx] == 0)
      continue;
    if ((d - 1) > budget / strides_[idx]) {
      throw std::invalid_argument("invalid view");
    }
    budget -= (d - 1) * strides_[idx];
  }
}
