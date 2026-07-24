#pragma once
#include <memory>

namespace cpp_torch::autograd::detail {
struct Node;
}

namespace cpp_torch::autograd {

class Value {
public:
  explicit Value(double data);

  [[nodiscard]] double data() const;

  [[nodiscard]] double grad() const;

  Value operator*(const Value& other) const;

  Value operator+(const Value& other) const;

  Value operator-(const Value& other) const;

  Value square() const;

  void backward();

  void zero_grad();

private:
  explicit Value(std::shared_ptr<detail::Node> node);

  std::shared_ptr<detail::Node> node_;
};

} // namespace cpp_torch::autograd
