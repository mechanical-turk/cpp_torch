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


// usage: harness2 <sgd|momentum|adam> <lr> <batch> <epochs> <norm> [seed]
int main(int argc, char** argv) {
  if (argc < 6) { std::cerr << "usage\n"; return 2; }
  const std::string opt = argv[1];
  const double lr = std::atof(argv[2]);
  const std::size_t batch = std::atoi(argv[3]), epochs = std::atoi(argv[4]);
  const std::string norm = argv[5];
  const unsigned seed = argc > 6 ? std::atoi(argv[6]) : 42;
  const std::size_t N = 10000;
  MnistReader all("data/train-images-idx3-ubyte", "data/train-labels-idx1-ubyte");
  MnistBatch data = all.read_batch(N);
  std::vector<double> mean(784, 0.0), sd(784, 0.0);
  for (std::size_t n = 0; n < N; ++n) for (std::size_t j = 0; j < 784; ++j) mean[j] += data.pixels[n * 784 + j] / N;
  for (std::size_t n = 0; n < N; ++n) for (std::size_t j = 0; j < 784; ++j) { double d = data.pixels[n * 784 + j] - mean[j]; sd[j] += d * d / N; }
  for (std::size_t j = 0; j < 784; ++j) sd[j] = std::sqrt(sd[j]);
  const bool standardise = norm == "pixel";
  auto prepare = [&](std::vector<double>& pixels) {
    if (!standardise) return;
    for (std::size_t n = 0; n < pixels.size() / 784; ++n) for (std::size_t j = 0; j < 784; ++j)
      pixels[n * 784 + j] = (pixels[n * 784 + j] - mean[j]) / (sd[j] + 0.1);
  };
  prepare(data.pixels);

  std::mt19937 random(seed);
  Sequence model;
  model.push_back(hidden_layer<ReLU>(784, 256, random));
  model.push_back(Linear(256, 10, random));
  std::vector<Tensor> parameters = model.parameters();
  std::vector<std::vector<double>> a, b;
  for (const Tensor& p: parameters) { a.emplace_back(p.numel(), 0.0); b.emplace_back(p.numel(), 0.0); }

  const auto start = std::chrono::steady_clock::now();
  std::size_t t = 0;
  bool diverged = false;
  std::vector<double> epoch_loss;
  for (std::size_t epoch = 0; epoch < epochs && !diverged; ++epoch) {
    double total = 0.0; std::size_t seen = 0;
    while (seen < N) {
      const std::size_t take = std::min(batch, N - seen);
      std::vector<double> pixels(data.pixels.begin() + seen * 784, data.pixels.begin() + (seen + take) * 784);
      std::vector<std::size_t> labels(data.labels.begin() + seen, data.labels.begin() + seen + take);
      for (Tensor& p: parameters) p.zero_grad();
      const Tensor inputs({take, 784}, std::move(pixels));
      double value = 0.0;
      Tensor loss = Tensor({}, {0.0});
      try {
        loss = cross_entropy_loss(softmax(model.forward(inputs)), labels);
        value = loss.at({});
      } catch (const std::domain_error&) { diverged = true; break; }
      if (!std::isfinite(value)) { diverged = true; break; }
      loss.backward();
      ++t;
      if (opt == "sgd") gradient_step(parameters, lr);
      else if (opt == "momentum") momentum_step(parameters, a, lr, 0.9);
      else adam_step(parameters, a, b, t, lr);
      total += value * take; seen += take;
    }
    if (!diverged) epoch_loss.push_back(total / seen);
  }
  std::size_t correct = 0, tested = 0;
  if (!diverged) {
    MnistReader test("data/t10k-images-idx3-ubyte", "data/t10k-labels-idx1-ubyte");
    while (tested < 2000) {
      MnistBatch tb = test.read_batch(std::min<std::size_t>(250, 2000 - tested));
      prepare(tb.pixels);
      const Tensor inputs({tb.labels.size(), 784}, std::move(tb.pixels));
      correct += count_correct(model.forward(inputs), tb.labels);
      tested += tb.labels.size();
    }
  }
  const double secs = std::chrono::duration<double>(std::chrono::steady_clock::now() - start).count();
  std::cout << "RESULT " << opt << " lr " << lr << " batch " << batch << " epochs " << epochs << " norm " << norm << " seed " << seed;
  if (diverged) std::cout << " DIVERGED";
  else { std::cout << " epoch_losses"; for (double l: epoch_loss) std::cout << " " << l; std::cout << " test_correct " << correct << "/" << tested; }
  std::cout << " secs " << secs << "\n";
}
