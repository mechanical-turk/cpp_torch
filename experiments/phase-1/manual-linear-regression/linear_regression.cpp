#include "linear_regression.hpp"
#include <cmath>
#include <span>

namespace {

bool is_within_tolerance(
    double a,
    double b,
    double tolerance
) {
  return std::abs(a - b) < tolerance;
}

double central_difference(
    double first,
    double second,
    double epsilon
) {
  if (epsilon <= 0.0) {
    throw std::invalid_argument("epsilon must be positive.");
  }

  return (first - second) / (2 * epsilon);
}

Gradient numerical_gradient(
    const Sample& sample,
    double w,
    double b,
    double epsilon
) {
  double rw1 = residual(sample, w + epsilon, b);
  double rw2 = residual(sample, w - epsilon, b);

  double rb1 = residual(sample, w, b + epsilon);
  double rb2 = residual(sample, w, b - epsilon);

  return {
    central_difference(rw1 * rw1, rw2 * rw2, epsilon),
    central_difference(rb1 * rb1, rb2 * rb2, epsilon),
  };
}

Evaluation evaluate(
    const Sample& sample,
    double w,
    double b
) {
  const double r = residual(sample, w, b);
  return Evaluation {
    .loss = r * r,
    .grad = Gradient {
      .dw = 2 * r * sample.x,
      .db = 2 * r,
    }
  };
}
} // namespace

Gradient numerical_gradient(
    std::span<const Sample> samples,
    double w,
    double b,
    double epsilon
) {
  if (samples.empty()) {
    throw std::invalid_argument(
        "cannot compute a numerical gradient for an empty dataset"
    );
  }

  Gradient ans {0.0, 0.0};
  for (const auto& sample : samples) {
    const auto grad = numerical_gradient(sample, w, b, epsilon);
    ans.dw += grad.dw;
    ans.db += grad.db;
  }

  ans.dw /= static_cast<double>(samples.size());
  ans.db /= static_cast<double>(samples.size());

  return ans;
}

bool gradients_agree(
    const Gradient& analytic,
    const Gradient& numerical,
    double tolerance
) {
  return is_within_tolerance(analytic.dw, numerical.dw, tolerance) &&
         is_within_tolerance(analytic.db, numerical.db, tolerance);
}

double y_hat(
    const Sample& sample,
    double w,
    double b
) {

  return w * sample.x + b;
}

double residual(
    const Sample& sample,
    double w,
    double b
) {

  return y_hat(sample, w, b) - sample.y;
}

Evaluation evaluate(
    std::span<const Sample> samples,
    double w,
    double b
) {

  if (samples.empty()) {
    throw std::invalid_argument("cannot evaluate an empty dataset");
  }

  double sum_loss = 0.0;
  double sum_dw = 0.0;
  double sum_db = 0.0;

  for (const auto& sample : samples) {
    auto eval = evaluate(sample, w, b);
    sum_loss += eval.loss;
    sum_dw += eval.grad.dw;
    sum_db += eval.grad.db;
  }

  return Evaluation {
    .loss = sum_loss / static_cast<double>(samples.size()),
    .grad = Gradient {
      .dw = sum_dw / static_cast<double>(samples.size()),
      .db = sum_db / static_cast<double>(samples.size()),
    }
  };
}

void gradient_descent_step(
    std::span<const Sample> samples,
    double learning_rate,
    double& w,
    double& b
) {
  const Evaluation evaluation = evaluate(samples, w, b);
  w -= learning_rate * evaluation.grad.dw;
  b -= learning_rate * evaluation.grad.db;
}

void gd(
    const GDParams& params,
    std::span<const Sample> samples,
    double& w,
    double& b
) {

  for (int i = 1; i <= params.epochs; ++i) {
    gradient_descent_step(samples, params.learning_rate, w, b);
  }
}
