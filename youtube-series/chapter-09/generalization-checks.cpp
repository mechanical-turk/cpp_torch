// Verification only: exercise the batch-only model with several feature counts.
void generalization_checks() {
  const auto near = [](double actual, double expected) {
    assert(std::isfinite(actual));
    assert(std::abs(actual - expected) < 1e-7 * (1.0 + std::abs(expected)));
  };

  for (std::size_t features : {1, 3, 5}) {
    const std::size_t rows = std::size_t{1} << features;
    std::vector<double> input_data, target_data, coefficients;

    for (std::size_t feature = 0; feature < features; ++feature)
      coefficients.push_back((feature % 2 ? -1.0 : 1.0) * (feature + 1));

    for (std::size_t row = 0; row < rows; ++row) {
      double target = 0.75;
      for (std::size_t feature = 0; feature < features; ++feature) {
        const double input = row & (std::size_t{1} << feature) ? 1.0 : -1.0;
        input_data.push_back(input);
        target += input * coefficients[feature];
      }
      target_data.push_back(target);
    }

    const Tensor inputs({rows, features}, input_data);
    const Tensor targets({rows, 1}, target_data);
    Tensor weights({features, 1}, std::vector<double>(features, 0.0));
    Tensor bias({}, {0.0});

    train_linear_regression(inputs, targets, weights, bias, 500, 0.05);

    const Tensor predictions = linear_forward(inputs, weights, bias);
    for (std::size_t row = 0; row < rows; ++row)
      near(predictions.at({row, 0}), target_data[row]);
    for (std::size_t feature = 0; feature < features; ++feature)
      near(weights.at({feature, 0}), coefficients[feature]);
    near(bias.at({}), 0.75);
  }

  bool rejected = false;
  try {
    static_cast<void>(linear_forward(
      Tensor({2, 3}, {1, 2, 3, 4, 5, 6}),
      Tensor({2, 1}, {1, 2}),
      Tensor({}, {0})
    ));
  } catch (const std::invalid_argument&) {
    rejected = true;
  }
  assert(rejected);

  std::cout << "Batch model generalization with 1, 3 and 5 features: PASS\n";
}
