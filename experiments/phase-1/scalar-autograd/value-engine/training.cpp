#include "value.hpp"
#include <array>
#include <iostream>
#include <span>
#include <stdexcept>
using cpp_torch::autograd::Value;

struct Sample {
  Value x;
  Value y;
};

Value yhat(
    const Value& w,
    const Value& b,
    const Sample& sample
) {
  return w * sample.x + b;
}

Value residual(
    const Value& w,
    const Value& b,
    const Sample& sample
) {
  return yhat(w, b, sample) - sample.y;
}

Value loss(
    const Value& w,
    const Value& b,
    const Sample& sample
) {
  Value r = residual(w, b, sample);
  return r * r;
}

Value loss(
    const Value& w,
    const Value& b,
    std::span<const Sample> samples
) {
  if (samples.empty()) {
    throw std::invalid_argument("samples must be non-empty.");
  }
  const double sz = static_cast<double>(samples.size());
  Value sum_loss(0.0);
  for (const Sample& sample : samples) {
    sum_loss = sum_loss + loss(w, b, sample);
  }
  return sum_loss * Value(1.0 / sz);
}

int main() {
  const std::array samples {
    Sample {Value(0.0), Value(1.0)},
    Sample {Value(1.0), Value(3.0)},
    Sample {Value(2.0), Value(5.0)},
  };

  Value w(1.0);
  Value b(1.0);

  static constexpr double LEARNING_RATE = 0.1;

  for (int i = 1; i <= 1000; ++i) {
    Value l = loss(w, b, samples);
    l.backward();
    w = Value(w.data() - LEARNING_RATE * w.grad());
    b = Value(b.data() - LEARNING_RATE * b.grad());
    l.zero_grad();
  }

  Value l = loss(w, b, samples);

  std::cout << "loss = " << l.data() << "\n";
  std::cout << "w = " << w.data() << ", w.grad = " << w.grad() << "\n";
  std::cout << "b = " << b.data() << ", b.grad = " << b.grad() << "\n";

  return 0;
}
