#include <array>
#include <gtest/gtest.h>
#include <linear_regression.hpp>
#include <stdexcept>
#include <utility>

TEST(
    ManualLinearRegressionTest,
    CompareNumericVsAnalyticalGradients
) {
  constexpr std::array samples {
    Sample {0.0, 1.0},
    Sample {1.0, 3.0},
    Sample {2.0, 5.0},
  };

  constexpr std::array initial_points {
    std::pair {1.0, 1.0},
    std::pair {2.0, 1.0},
    std::pair {-1.5, 3.0},
  };

  constexpr double tolerance = 1e-8;

  for (const auto& [w, b] : initial_points) {

    const Evaluation analytic = evaluate(samples, w, b);
    const Gradient numeric = numerical_gradient(samples, w, b);

    EXPECT_NEAR(analytic.grad.dw, numeric.dw, tolerance);
    EXPECT_NEAR(analytic.grad.db, numeric.db, tolerance);
  }
}

TEST(
    ManualLinearRegressionTest,
    GradientDescentConvergesToKnownSolution
) {
  double w = 1.0;
  double b = 1.0;
  constexpr GDParams params {
    .epochs = 1000,
    .learning_rate = 0.1,
  };
  constexpr double tolerance {1e-8};

  constexpr std::array samples {
    Sample {0.0, 1.0},
    Sample {1.0, 3.0},
    Sample {2.0, 5.0},
  };

  gd(params, samples, w, b);

  EXPECT_NEAR(w, 2.0, tolerance);
  EXPECT_NEAR(b, 1.0, tolerance);
  EXPECT_NEAR(evaluate(samples, w, b).loss, 0.0, tolerance);
}

TEST(
    ManualLinearRegressionTest,
    ExcessiveLearningRateIncreasesLoss
) {
  double w = 1.0;
  double b = 1.0;
  constexpr GDParams params {
    .epochs = 10,
    .learning_rate = 1.0,
  };

  constexpr std::array samples {
    Sample {0.0, 1.0},
    Sample {1.0, 3.0},
    Sample {2.0, 5.0},
  };

  const double initial_loss = evaluate(samples, w, b).loss;

  gd(params, samples, w, b);

  const double final_loss = evaluate(samples, w, b).loss;

  EXPECT_GT(final_loss, initial_loss);
}

TEST(
    ManualLinearRegressionTest,
    EvaluateRejectsEmptyDataset
) {
  constexpr std::array<Sample, 0> samples {};
  EXPECT_THROW(evaluate(samples, 1.0, 1.0), std::invalid_argument);
}

TEST(
    ManualLinearRegressionTest,
    NumericalGradientRejectsEmptyDataset
) {
  constexpr std::array<Sample, 0> samples {};
  EXPECT_THROW(numerical_gradient(samples, 1.0, 1.0), std::invalid_argument);
}

TEST(
    ManualLinearRegressionTest,
    NumericalGradientRejectsNonPositiveEpsilon
) {
  constexpr std::array samples {
    Sample {0.0, 1.0},
    Sample {1.0, 3.0},
    Sample {2.0, 5.0},
  };
  EXPECT_THROW(
      numerical_gradient(samples, 1.0, 1.0, 0.0), std::invalid_argument
  );
  EXPECT_THROW(
      numerical_gradient(samples, 1.0, 1.0, -1e-5), std::invalid_argument
  );
}

TEST(
    ManualLinearRegressionTest,
    YHatWorks
) {
  constexpr double tolerance {1e-8};
  EXPECT_NEAR(y_hat({2.0, 0.0}, 3.0, -1.0), 5.0, tolerance);
}

TEST(
    ManualLinearRegressionTest,
    EvaluateComputesKnownLossAndGradient
) {
  constexpr std::array samples {
    Sample {0.0, 1.0},
    Sample {1.0, 3.0},
    Sample {2.0, 5.0},
  };
  constexpr double tolerance {1e-8};
  Evaluation e = evaluate(samples, 1.0, 1.0);
  EXPECT_NEAR(e.loss, 5.0 / 3.0, tolerance);
  EXPECT_NEAR(e.grad.dw, -10.0 / 3.0, tolerance);
  EXPECT_NEAR(e.grad.db, -2.0, tolerance);
}
