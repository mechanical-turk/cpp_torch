#include <cpp_torch/tensor.hpp>

#include <iostream>

int main() {
  cpp_torch::Tensor tensor({2}, {2.0, 3.0});
  std::cout << tensor.at({{0}}) << ' ' << tensor.at({{1}}) << '\n';
}
