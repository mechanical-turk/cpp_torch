// Off-camera verification of Episode 8's supported scalar-root arithmetic.
// Full reduction/broadcast gradient tests are deferred-gradient-checks.cpp.
#include <cmath>
#include <functional>

void gradient_checks() {
  using Data = std::vector<double>;
  const std::vector<std::function<Tensor(const Tensor&, const Tensor&)>> ops{
    [](const Tensor& a, const Tensor& b) { return a + b; },
    [](const Tensor& a, const Tensor& b) { return a - b; },
    [](const Tensor& a, const Tensor& b) { return a * b; },
    [](const Tensor& a, const Tensor& b) { return a / b; }
  };
  std::size_t comparisons = 0;
  for (const auto& op : ops) {
    for (double av : {-2.0, 0.0, 3.5}) {
      for (double bv : {-1.5, 2.0}) {
        Tensor a({}, {av}), b({}, {bv});
        Tensor output = op(a, b);
        output.backward();
        for (int side = 0; side < 2; ++side) {
          auto evaluate = [&](double offset) {
            return op(Tensor({}, {av + (side == 0 ? offset : 0)}),
                      Tensor({}, {bv + (side == 1 ? offset : 0)})).at({});
          };
          const double expected = (evaluate(1e-5) - evaluate(-1e-5)) / 2e-5;
          const double actual = (side == 0 ? a : b).grad()[0];
          assert(std::abs(actual - expected) < 1e-5 * (1 + std::abs(expected)));
          ++comparisons;
        }
      }
    }
  }
  Tensor x({}, {3});
  Tensor output = [&] {
    Tensor square = x * x;
    return (square + square) / Tensor({}, {2}) - x;
  }();
  output.backward();
  assert(x.grad()[0] == 5);
  output.backward();
  assert(x.grad()[0] == 5);
  Tensor alias = x;
  assert(&alias.data() == &x.data());
  assert(&alias.grad() == &x.grad());
  Tensor fresh(x.shape(), x.data());
  assert(&fresh.data() != &x.data());
  assert(fresh.grad()[0] == 0);
  Tensor leaf({}, {7});
  leaf.backward();
  assert(leaf.grad()[0] == 1);

  // Deferred paths fail, but failure does not promise gradient preservation.
  Tensor values({2}, {2, 3});
  Tensor total = values.sum();
  bool rejected = false;
  try { total.backward(); } catch (const std::logic_error&) { rejected = true; }
  assert(rejected);
  Tensor matrix({1, 1}, {2});
  Tensor product = matrix.matmul(matrix);
  rejected = false;
  try { product.backward(); } catch (const std::invalid_argument&) { rejected = true; }
  assert(rejected); // Public scalar-root guard, not a matmul-gradient test.
  for (double zero : {0.0, -0.0}) {
    for (double numerator : {0.0, 2.0}) {
      rejected = false;
      try { static_cast<void>(Tensor({}, {numerator}) / Tensor({}, {zero})); }
      catch (const std::domain_error&) { rejected = true; }
      assert(rejected);
    }
    rejected = false;
    try { static_cast<void>(Tensor({2}, {2, 4}) / Tensor({}, {zero})); }
    catch (const std::domain_error&) { rejected = true; }
    assert(rejected);
  }
  rejected = false;
  try { static_cast<void>(values / Tensor({2}, {1, 0})); }
  catch (const std::domain_error&) { rejected = true; }
  assert(rejected);
  Tensor empty({0, 3}, {});
  assert((empty / Tensor({}, {0})).numel() == 0);
  std::cout << "Gradient regressions passed; finite-difference comparisons: "
            << comparisons << '\n';
}
