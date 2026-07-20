#include <array>
#include <cmath>
#include <fstream>
#include <iostream>
#include <linear_regression.hpp>

int main() {
  const std::array learning_rates = {0.4, (4.0 - std::sqrt(10.0)) / 2.0, 0.43};
  const int epochs = 200;

  constexpr std::array samples {
    Sample {0.0, 1.0},
    Sample {1.0, 3.0},
    Sample {2.0, 5.0},
  };

  std::ofstream output_file("example.csv");

  if (!output_file.is_open()) {
    std::cerr << "Error: Could not open the file.\n";
    return 1;
  }

  output_file << "learning_rate,epoch,w,b,loss\n";

  for (double learning_rate : learning_rates) {
    double w = 1.0;
    double b = 1.0;

    for (int epoch = 0; epoch <= epochs; ++epoch) {
      const Evaluation evaluation = evaluate(samples, w, b);
      output_file << learning_rate << "," << epoch << "," << w << "," << b
                  << "," << evaluation.loss << '\n';

      w -= learning_rate * evaluation.grad.dw;
      b -= learning_rate * evaluation.grad.db;
    }
  }

  output_file.close();
}
