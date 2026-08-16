#include <cassert>
#include <cstddef>
#include <iostream>
#include <stdexcept>
#include <utility>
#include <vector>

class Tensor {
public:
  Tensor(
      std::vector<std::size_t> shape,
      std::vector<double> data
  )
      : shape_(std::move(shape)), data_(std::move(data)) {
    if (shape_.empty()) {
      throw std::invalid_argument(
          "chapter 1 tensors must have at least one dimension"
      );
    }

    std::size_t expected_elements = 1;
    for (const std::size_t dimension : shape_) {
      if (dimension == 0) {
        throw std::invalid_argument(
            "chapter 1 tensor dimensions must be positive"
        );
      }
      expected_elements *= dimension;
    }

    if (expected_elements != data_.size()) {
      throw std::invalid_argument("tensor shape does not match its data");
    }
  }

  [[nodiscard]] const std::vector<std::size_t>& shape() const noexcept {
    return shape_;
  }

  [[nodiscard]] const std::vector<double>& data() const noexcept {
    return data_;
  }

  [[nodiscard]] std::size_t rank() const noexcept {
    return shape_.size();
  }

  [[nodiscard]] std::size_t numel() const noexcept {
    return data_.size();
  }

  [[nodiscard]] double at(
      const std::vector<std::size_t>& indices
  ) const {
    if (indices.size() != rank()) {
      throw std::invalid_argument("number of indices must match tensor rank");
    }

    std::size_t flat_index = 0;
    std::size_t stride = 1;

    for (std::size_t axis = rank(); axis > 0; --axis) {
      const std::size_t current_axis = axis - 1;
      if (indices[current_axis] >= shape_[current_axis]) {
        throw std::out_of_range("tensor index is outside its dimension");
      }

      flat_index += indices[current_axis] * stride;
      stride *= shape_[current_axis];
    }

    return data_[flat_index];
  }

private:
  std::vector<std::size_t> shape_;
  std::vector<double> data_;
};

void run_tests() {
  const Tensor matrix(
      {2, 3},
      {
          1.0,
          2.0,
          3.0,
          4.0,
          5.0,
          6.0,
      }
  );

  assert(matrix.rank() == 2);
  assert(matrix.numel() == 6);
  assert((matrix.shape() == std::vector<std::size_t> {2, 3}));
  assert(matrix.data()[0] == 1.0);
  assert(matrix.data()[5] == 6.0);
  assert(matrix.at({0, 0}) == 1.0);
  assert(matrix.at({0, 2}) == 3.0);
  assert(matrix.at({1, 0}) == 4.0);
  assert(matrix.at({1, 2}) == 6.0);

  bool rejected_invalid_tensor = false;
  try {
    const Tensor invalid({2, 3}, {1.0, 2.0});
  } catch (const std::invalid_argument&) {
    rejected_invalid_tensor = true;
  }

  assert(rejected_invalid_tensor);

  bool rejected_wrong_index_count = false;
  try {
    static_cast<void>(matrix.at({1}));
  } catch (const std::invalid_argument&) {
    rejected_wrong_index_count = true;
  }
  assert(rejected_wrong_index_count);

  bool rejected_out_of_bounds_index = false;
  try {
    static_cast<void>(matrix.at({2, 0}));
  } catch (const std::out_of_range&) {
    rejected_out_of_bounds_index = true;
  }
  assert(rejected_out_of_bounds_index);

  std::cout << "All assertions passed.\n";
}

int main() {
  run_tests();

  const Tensor matrix(
      {2, 3},
      {
          1.0,
          2.0,
          3.0,
          4.0,
          5.0,
          6.0,
      }
  );

  std::cout << "rank: " << matrix.rank() << '\n';
  std::cout << "elements: " << matrix.numel() << '\n';
  std::cout << "shape: [";

  for (std::size_t axis = 0; axis < matrix.rank(); ++axis) {
    if (axis != 0) {
      std::cout << ", ";
    }
    std::cout << matrix.shape()[axis];
  }

  std::cout << "]\nflat data: ";
  for (const double value : matrix.data()) {
    std::cout << value << ' ';
  }
  std::cout << "\nvalue at [1, 2]: " << matrix.at({1, 2}) << '\n';
}
