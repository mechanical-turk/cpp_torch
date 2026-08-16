#pragma once

#include <cstddef>
#include <memory>
#include <span>
#include <vector>

namespace cpp_torch {
class Tensor {
public:
  Tensor(std::vector<std::size_t> shape, std::vector<double> storage);

  [[nodiscard]] const std::vector<std::size_t>& shape() const;

  [[nodiscard]] std::size_t numel() const;

  [[nodiscard]] std::size_t rank() const;

  double& at(std::span<const std::size_t> indices);

  const double& at(std::span<const std::size_t> indices) const;

  Tensor operator+(const Tensor& right) const;
  Tensor operator*(const Tensor& right) const;

  Tensor sum() const;
  Tensor dot(const Tensor& right) const;

  Tensor(const Tensor& other);
  Tensor& operator=(const Tensor& other);

  Tensor(Tensor&&) noexcept = default;
  Tensor& operator=(Tensor&&) noexcept = default;

  Tensor T() const;

  Tensor select(std::size_t axis, std::size_t index) const;

  [[nodiscard]] bool is_contiguous() const;

  Tensor matmul(const Tensor& right) const;

private:
  std::vector<std::size_t> shape_;
  std::vector<std::size_t> strides_;
  std::shared_ptr<std::vector<double>> storage_;
  std::size_t offset_ {0};

  Tensor(
      std::vector<std::size_t> shape,
      std::shared_ptr<std::vector<double>> storage,
      std::vector<std::size_t> strides,
      std::size_t offset
  );

  std::size_t storage_idx(std::span<const std::size_t> indices) const;
  Tensor elementwise_binary(const Tensor& right, auto operation) const;

  std::vector<double> materialize() const;
};

}; // namespace cpp_torch
