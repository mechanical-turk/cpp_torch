#include "value.hpp"
#include <iostream>
using cpp_torch::autograd::Value;

int main() {

  Value w(1.5);
  Value x(2.0);
  Value b(0.5);
  Value y(5.0);

  Value m = w * x;
  Value p = m + b;
  Value r = p - y;
  Value loss = r.square();

  auto print = [&]() {
    for (const auto& cur : {w, x, b, y, m, p, r, loss}) {

      std::cout << cur.data() << ", " << cur.grad() << "\n";
    }
    std::cout << "\n\n";
  };

  loss.backward();
  print();

  loss.zero_grad();
  loss.backward();
  print();
}
