#include <array>
#include <cmath>
#include <iostream>
#include <linear_regression.hpp>
#include <span>

void run(
    double w,
    double b
) {
  std::cout << "Starting new run with initial (w,b) = (" << w << ", " << b
            << ")\n";

  constexpr std::array samples {
    Sample {0.0, 1.0},
    Sample {1.0, 3.0},
    Sample {2.0, 5.0},
  };

  constexpr GDParams params {
    .epochs = 10,
    .learning_rate = 0.1,
  };

  const Evaluation analytic = evaluate(samples, w, b);
  const Gradient numeric = numerical_gradient(samples, w, b);

  std::cout << "dL/dw: " << analytic.grad.dw << '\n';
  std::cout << "numeric dL/dw: " << numeric.dw << '\n';
  std::cout << "dL/dw error:" << std::abs(numeric.dw - analytic.grad.dw)
            << '\n';

  std::cout << "dL/db: " << analytic.grad.db << '\n';
  std::cout << "numeric dL/db: " << numeric.db << '\n';
  std::cout << "dL/db error:" << std::abs(numeric.db - analytic.grad.db)
            << '\n';

  gd(params, samples, w, b);

  std::cout << "\n\n\n\n";
}

int main() {
  run(1.0, 1.0);
  run(2.0, 1.0);
  run(-1.5, 3.0);

  return 0;
}
