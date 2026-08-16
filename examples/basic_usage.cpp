#include <cpp_torch/tensor.hpp>

#include <iostream>

using cpp_torch::Tensor;

int main() {
  Tensor a({2}, {2.0, 3.0});
  Tensor b({2}, {1.0, 4.0});

  Tensor c = a + b;
  std::cout << c.at({{0}}) << ' ' << c.at({{1}}) << "\n";

  Tensor d = a * b;
  std::cout << d.at({{0}}) << ' ' << d.at({{1}}) << "\n";

  Tensor e = a.dot(b);
  std::cout << e.at({}) << '\n';
}
