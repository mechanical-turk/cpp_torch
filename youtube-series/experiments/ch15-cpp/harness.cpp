// Experiment harness around the series' own Chapter 14 code (episode-14-baseline.cpp).
// usage: harness <sgd|momentum|adam> <lr> <batch> <max_steps> <norm: none|pixel|global> [target_loss] [print_every]
#define main series_main
#include "episode-14-baseline.cpp"
#undef main
#include <chrono>
#include <cstdlib>

static void momentum_step(std::vector<Tensor>& parameters, std::vector<std::vector<double>>& velocity,
                          double learning_rate, double beta) {
  for (std::size_t p = 0; p < parameters.size(); ++p) {
    Tensor& parameter = parameters[p];
    for (std::size_t i = 0; i < parameter.numel(); ++i) {
      velocity[p][i] = beta * velocity[p][i] + parameter.grad()[i];
      parameter.data()[i] -= learning_rate * velocity[p][i];
    }
  }
}

static void adam_step(std::vector<Tensor>& parameters, std::vector<std::vector<double>>& m1,
                      std::vector<std::vector<double>>& m2, std::size_t t, double learning_rate) {
  const double beta1 = 0.9, beta2 = 0.999, epsilon = 1e-8;
  const double c1 = 1.0 - std::pow(beta1, static_cast<double>(t));
  const double c2 = 1.0 - std::pow(beta2, static_cast<double>(t));
  for (std::size_t p = 0; p < parameters.size(); ++p) {
    Tensor& parameter = parameters[p];
    for (std::size_t i = 0; i < parameter.numel(); ++i) {
      const double g = parameter.grad()[i];
      m1[p][i] = beta1 * m1[p][i] + (1.0 - beta1) * g;
      m2[p][i] = beta2 * m2[p][i] + (1.0 - beta2) * g * g;
      parameter.data()[i] -= learning_rate * (m1[p][i] / c1) / (std::sqrt(m2[p][i] / c2) + epsilon);
    }
  }
}

int main(int argc, char** argv) {
  if (argc < 6) { std::cerr << "usage\n"; return 2; }
  const std::string opt = argv[1];
  const double lr = std::atof(argv[2]);
  const std::size_t batch = std::atoi(argv[3]), max_steps = std::atoi(argv[4]);
  const std::string norm = argv[5];
  const double target = argc > 6 ? std::atof(argv[6]) : 0.1;
  const std::size_t every = argc > 7 ? std::atoi(argv[7]) : 0;
  const std::size_t N = 10000;

  MnistReader all("data/train-images-idx3-ubyte", "data/train-labels-idx1-ubyte");
  MnistBatch data = all.read_batch(N);
  if (norm != "none") {
    std::vector<double> mean(784, 0.0), sd(784, 0.0);
    for (std::size_t n = 0; n < N; ++n) for (std::size_t j = 0; j < 784; ++j) mean[j] += data.pixels[n * 784 + j] / N;
    for (std::size_t n = 0; n < N; ++n) for (std::size_t j = 0; j < 784; ++j) { double d = data.pixels[n * 784 + j] - mean[j]; sd[j] += d * d / N; }
    for (std::size_t j = 0; j < 784; ++j) sd[j] = std::sqrt(sd[j]);
    if (norm == "global") {
      double gm = 0, gs = 0;
      for (double v: data.pixels) gm += v / data.pixels.size();
      for (double v: data.pixels) gs += (v - gm) * (v - gm) / data.pixels.size();
      gs = std::sqrt(gs);
      for (double& v: data.pixels) v = (v - gm) / gs;
    } else {
      for (std::size_t n = 0; n < N; ++n) for (std::size_t j = 0; j < 784; ++j)
        data.pixels[n * 784 + j] = (data.pixels[n * 784 + j] - mean[j]) / (sd[j] + 0.1);
    }
  }

  std::mt19937 random(42);
  Sequence model;
  model.push_back(hidden_layer<ReLU>(784, 256, random));
  model.push_back(Linear(256, 10, random));
  std::vector<Tensor> parameters = model.parameters();
  std::vector<std::vector<double>> a, b;
  for (const Tensor& p: parameters) { a.emplace_back(p.numel(), 0.0); b.emplace_back(p.numel(), 0.0); }

  const auto start = std::chrono::steady_clock::now();
  std::size_t cursor = 0, reached = max_steps + 1;
  for (std::size_t step = 0; step <= max_steps; ++step) {
    const std::size_t take = std::min(batch, N);
    std::vector<double> pixels(take * 784);
    std::vector<std::size_t> labels(take);
    for (std::size_t k = 0; k < take; ++k) {
      const std::size_t n = (cursor + k) % N;
      std::copy(data.pixels.begin() + n * 784, data.pixels.begin() + (n + 1) * 784, pixels.begin() + k * 784);
      labels[k] = data.labels[n];
    }
    cursor = (cursor + take) % N;
    for (Tensor& p: parameters) p.zero_grad();
    const Tensor inputs({take, 784}, std::move(pixels));
    const Tensor logits = model.forward(inputs);
    Tensor loss = cross_entropy_loss(softmax(logits), labels);
    const double value = loss.at({});
    if (every && step % every == 0) std::cout << "step " << step << " loss " << value << "\n";
    if (value <= target && reached > max_steps) { reached = step; if (!every) break; }
    if (!std::isfinite(value)) { std::cout << "diverged at step " << step << "\n"; break; }
    loss.backward();
    if (opt == "sgd") gradient_step(parameters, lr);
    else if (opt == "momentum") momentum_step(parameters, a, lr, 0.9);
    else adam_step(parameters, a, b, step + 1, lr);
  }
  const double secs = std::chrono::duration<double>(std::chrono::steady_clock::now() - start).count();
  if (reached > max_steps) std::cout << "RESULT " << opt << " lr " << lr << " batch " << batch << " norm " << norm << " target " << target << " not reached in " << max_steps << " steps, " << secs << " s\n";
  else std::cout << "RESULT " << opt << " lr " << lr << " batch " << batch << " norm " << norm << " target " << target << " reached at step " << reached << ", " << secs << " s\n";
}
