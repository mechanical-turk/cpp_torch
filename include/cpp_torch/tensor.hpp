#pragma once

#include <cstddef>
#include <span>
#include <vector>

namespace cpp_torch {
class Tensor {
public:
  Tensor(std::vector<std::size_t> shape, std::vector<double> storage);

  [[nodiscard]] const std::vector<std::size_t>& shape() const;

  [[nodiscard]] const std::vector<double>& storage() const;

  [[nodiscard]] std::size_t numel() const;

  [[nodiscard]] std::size_t rank() const;

  double& at(std::span<const std::size_t> indices);

  const double& at(std::span<const std::size_t> indices) const;

  const std::vector<std::size_t> strides() const;

private:
  std::vector<std::size_t> shape_;
  std::vector<double> storage_;

  std::size_t storage_idx(std::span<const std::size_t> indices) const;
};

}; // namespace cpp_torch
