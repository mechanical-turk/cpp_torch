#pragma once
#include <span>

struct Sample {
  double x;
  double y;
};

struct Gradient {
  double dw;
  double db;
};

struct Evaluation {
  double loss;
  Gradient grad;
};

struct GDParams {
  int epochs;
  double learning_rate;
};

double y_hat(const Sample& sample, double w, double b);

double residual(const Sample& sample, double w, double b);

Evaluation evaluate(std::span<const Sample> samples, double w, double b);

Gradient numerical_gradient(
    std::span<const Sample> samples,
    double w,
    double b,
    double epsilon = 1e-5
);

bool gradients_agree(
    const Gradient& analytic,
    const Gradient& numerical,
    double tolerance = 1e-8
);

void gd(
    const GDParams& params,
    std::span<const Sample> samples,
    double& w,
    double& b
);
