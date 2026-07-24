#include <cpp_torch/tensor.hpp>
#include <iostream>

using cpp_torch::Tensor;

int main() {
  std::cout << "attempting [] with one value";
  Tensor a({}, {1.0});

  std::cout << "attempting [1] with one value";
  Tensor b({1}, {1.0});

  a = b;

  std::cout << "a.rank = " << a.rank() << "\n";
  std::cout << "a.storage = ";
  for (double item : a.storage()) {
    std::cout << item << ", ";
  }
  std::cout << '\n';

  std::cout << "attempting [2, 3] with six values";
  Tensor c(
      {2, 3}, {
                1.0,
                2.0,
                3.0,
                4.0,
                5.0,
                6.0,
              }
  );

  std::cout << "attempting [0] with no values";
  Tensor d({0}, {});

  try {

    std::cout << "attempting [2,3] with five values";
    Tensor e(
        {2, 3}, {
                  1.0,
                  2.0,
                  3.0,
                  4.0,
                  5.0,
                }
    );
  } catch (const std::invalid_argument&) {
    std::cout << "caught\n";
  }

  try {
    std::cout << "attempting overflow with [max_size_t, 2]";
    Tensor f({std::numeric_limits<std::size_t>::max(), 2}, {});
  } catch (const std::overflow_error&) {
    std::cout << "caught\n";
  }

  std::cout << "[max_size_t, 2, 0]";
  Tensor zero_sized({std::numeric_limits<std::size_t>::max(), 2, 0}, {});
  std::cout << zero_sized.numel() << '\n';

  Tensor g(
      {2, 3, 2}, {
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

  std::cout << "g[0, 0, 0] = " << g.at({{0, 0, 0}}) << "\n";
  std::cout << "g[0, 0, 1] = " << g.at({{0, 0, 1}}) << "\n";
  std::cout << "g[0, 1, 1] = " << g.at({{0, 1, 1}}) << "\n";
  std::cout << "g[1, 1, 1] = " << g.at({{1, 1, 1}}) << "\n";

  g.at({{1, 1, 1}}) = 42.0;

  std::cout << "g[1, 1, 1] after reference update = " << g.at({{1, 1, 1}})
            << "\n";

  Tensor original({2}, {10.0, 20.0});
  Tensor copy = original;
  copy.at({{0}}) = 99.0;

  std::cout << copy.at({{0}}) << '\n';

  Tensor source({2}, {10.0, 20.0});
  Tensor destination = std::move(source);
  source = Tensor({2}, {15.0, 20.0});

  std::cout << source.at({{0}});

  return 0;
}
