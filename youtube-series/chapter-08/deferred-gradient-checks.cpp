// Deferred Episode 9 test draft. Requires sum backward; not run for Episode 8.
// Extend with matmul gradients and training tests when implementing Episode 9.
// Verification support only, not live-coding content. Included after Tensor/MSE.
#include <cmath>
#include <functional>

void gradient_checks() {
  using Shape = std::vector<std::size_t>;
  using Data = std::vector<double>;
  auto near = [](double a, double b) {
    assert(std::abs(a - b) < 1e-5 * (1.0 + std::abs(b)));
  };
  const std::vector<std::function<Tensor(const Tensor&, const Tensor&)>> ops{
    [](const Tensor& a, const Tensor& b) { return a + b; },
    [](const Tensor& a, const Tensor& b) { return a - b; },
    [](const Tensor& a, const Tensor& b) { return a * b; },
    [](const Tensor& a, const Tensor& b) { return a / b; }
  };
  struct Case { Shape a_shape, b_shape; Data a_data, b_data; };
  const std::vector<Case> cases{
    {{2, 3}, {3}, {1, 2, 3, 4, 5, 6}, {2, 3, 4}},
    {{2, 1}, {1, 3}, {2, 5}, {3, 4, 7}},
    {{}, {2, 2}, {2}, {1, 3, 5, 7}},
    {{2, 2}, {}, {1, 3, 5, 7}, {2}},
    {{2, 2}, {2, 2}, {1, 3, 5, 7}, {2, 4, 6, 8}}
  };
  std::size_t comparisons = 0;
  for (const auto& op : ops) {
    for (const auto& c : cases) {
      Tensor a(c.a_shape, c.a_data), b(c.b_shape, c.b_data);
      Tensor loss = op(a, b).mean();
      loss.backward();
      for (int side = 0; side < 2; ++side) {
        const auto& values = side == 0 ? c.a_data : c.b_data;
        const auto& gradients = side == 0 ? a.grad() : b.grad();
        for (std::size_t i = 0; i < values.size(); ++i) {
          auto evaluate = [&](double offset) {
            Data av = c.a_data, bv = c.b_data;
            (side == 0 ? av : bv)[i] += offset;
            return op(Tensor(c.a_shape, av), Tensor(c.b_shape, bv)).mean().at({});
          };
          near(gradients[i], (evaluate(1e-5) - evaluate(-1e-5)) / 2e-5);
          ++comparisons;
        }
      }
    }
  }
  Tensor x({2}, {2, 3});
  Tensor branch = x * x;
  Tensor joined = (branch + branch).sum();
  joined.backward();
  assert((x.grad() == Data{8, 12}));
  joined.backward();
  assert((x.grad() == Data{8, 12}));
  Tensor alias = x;
  assert(&alias.data() == &x.data());
  assert(&alias.grad() == &x.grad());
  Tensor fresh(x.shape(), x.data());
  assert(&fresh.data() != &x.data());
  assert((fresh.grad() == Data{0, 0}));
  Tensor retained({2}, {2, 3});
  Tensor after_scope = [&] {
    const Tensor local = retained * retained;
    return (local + local).sum();
  }();
  after_scope.backward();
  assert((retained.grad() == Data{8, 12}));
  // The graph owns local's node after the local Tensor handle is destroyed.
  Tensor predictions({2, 1}, {3.5, 0});
  Tensor targets({2, 1}, {2.5, 1});
  Tensor mse = mse_loss(predictions, targets);
  mse.backward();
  assert((predictions.grad() == Data{1, -1}));
  assert((targets.grad() == Data{-1, 1}));
  Tensor perfect = mse_loss(predictions, predictions);
  perfect.backward();
  assert((predictions.grad() == Data{0, 0}));
  Tensor scalar({}, {3});
  Tensor empty({0, 3}, {});
  Tensor empty_result = empty + scalar;
  assert((empty_result.shape() == Shape{0, 3}));
  Tensor empty_sum = empty_result.sum();
  empty_sum.backward();
  assert(scalar.grad()[0] == 0);
  assert(empty.grad().empty());
  Tensor singleton({1, 3}, {1, 2, 3});
  assert((singleton + empty).numel() == 0);
  bool threw = false;
  try { empty.mean(); } catch (const std::invalid_argument&) { threw = true; }
  assert(threw);
  threw = false;
  try { mse_loss(predictions, Tensor({2}, {2.5, 1})); }
  catch (const std::invalid_argument&) { threw = true; }
  assert(threw);
  threw = false;
  try { branch.backward(); } catch (const std::invalid_argument&) { threw = true; }
  assert(threw);
  assert((x.grad() == Data{8, 12}));
  Tensor matrix({1, 1}, {2});
  Tensor prior = (matrix * matrix).sum();
  prior.backward();
  Tensor unsupported = matrix.matmul(matrix).sum();
  threw = false;
  try { unsupported.backward(); } catch (const std::logic_error&) { threw = true; }
  assert(threw);
  assert(matrix.grad()[0] == 4); // Rejection happens before clearing.
  Tensor w({2}, {2, 3}), features({2}, {4, 5});
  Tensor dot = w.dot(features);
  dot.backward();
  assert((w.grad() == Data{4, 5}));
  assert((features.grad() == Data{2, 3}));
  Tensor leaf({}, {7});
  leaf.backward();
  assert(leaf.grad()[0] == 1);
  for (double zero : {0.0, -0.0}) {
    for (double numerator : {0.0, 2.0}) {
      bool rejected = false;
      try {
        static_cast<void>(Tensor({}, {numerator}) / Tensor({}, {zero}));
      } catch (const std::domain_error&) {
        rejected = true;
      }
      assert(rejected);
    }
    bool rejected = false;
    try {
      static_cast<void>(Tensor({2}, {2, 4}) / Tensor({}, {zero}));
    } catch (const std::domain_error&) {
      rejected = true;
    }
    assert(rejected);
  }
  bool rejected_element = false;
  try {
    static_cast<void>(Tensor({2}, {2, 4}) / Tensor({2}, {1, 0}));
  } catch (const std::domain_error&) {
    rejected_element = true;
  }
  assert(rejected_element);
  assert((Tensor({}, {0}) / Tensor({}, {2})).at({}) == 0);
  assert((empty / Tensor({}, {0})).numel() == 0);
  std::cout << "Forward division zero guards passed.\n";
  std::cout << "Gradient regressions passed; finite-difference comparisons: "
            << comparisons << '\n';
}
