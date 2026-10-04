// Research harness only. Not part of the recording script or live main.cpp.
#define main lesson_main
#include "lesson.cpp"
#undef main
#include <chrono>
#include <numeric>
#include <sstream>

struct Candidate {
  std::vector<Linear> layers;
  bool relu;

  Candidate(const std::vector<std::size_t>& widths, bool use_relu, std::mt19937& rng)
    : relu(use_relu) {
    std::size_t previous = 784;
    for (auto width : widths) {
      layers.emplace_back(previous, width, rng);
      previous = width;
    }
    layers.emplace_back(previous, 10, rng);
  }
  Tensor forward(const Tensor& inputs) const {
    Tensor result = inputs;
    for (std::size_t i = 0; i < layers.size(); ++i) {
      result = layers[i].forward(result);
      if (i + 1 < layers.size()) result = relu ? result.relu() : result.tanh();
    }
    return result;
  }
  std::vector<Tensor> parameters() const {
    std::vector<Tensor> result;
    for (const auto& layer : layers) {
      auto values = layer.parameters();
      result.insert(result.end(), values.begin(), values.end());
    }
    return result;
  }
};

struct Metrics { double loss; double accuracy; };

Metrics evaluate(const Candidate& model, const MnistBatch& data) {
  double loss = 0;
  std::size_t correct = 0;
  for (std::size_t start = 0; start < data.labels.size(); start += 64) {
    const auto end = std::min(start + 64, data.labels.size());
    Tensor inputs({end - start, 784},
      std::vector<double>(data.pixels.begin() + start * 784, data.pixels.begin() + end * 784));
    std::vector<std::size_t> labels(data.labels.begin() + start, data.labels.begin() + end);
    Tensor scores = model.forward(inputs);
    loss += cross_entropy_loss(softmax(scores), labels).at({}) * labels.size();
    correct += count_correct(scores, labels);
  }
  return {loss / data.labels.size(), 100.0 * correct / data.labels.size()};
}

int main(int argc, char** argv) {
  if (argc != 8) throw std::invalid_argument("name widths activation lr shuffle seed epochs");
  const std::string name = argv[1];
  std::vector<std::size_t> widths;
  std::stringstream sizes(argv[2]);
  std::string width;
  while (std::getline(sizes, width, ',')) widths.push_back(std::stoul(width));
  const bool relu = std::string(argv[3]) == "relu";
  const double learning_rate = std::stod(argv[4]);
  const bool shuffle = std::stoi(argv[5]);
  const unsigned seed = std::stoul(argv[6]);
  const std::size_t epochs = std::stoul(argv[7]);
  std::mt19937 rng(seed), order_rng(2026);
  Candidate model(widths, relu, rng);
  auto parameters = model.parameters();
  std::size_t parameter_count = 0;
  for (const auto& parameter : parameters) parameter_count += parameter.numel();

  // The official test files are deliberately never opened in this comparison.
  MnistReader reader("train-images-idx3-ubyte", "train-labels-idx1-ubyte");
  const MnistBatch training = reader.read_batch(10000);
  const MnistBatch validation = reader.read_batch(2000);
  if (training.labels.size() != 10000 || validation.labels.size() != 2000)
    throw std::runtime_error("incomplete experiment split");
  std::vector<std::size_t> order(training.labels.size());
  std::iota(order.begin(), order.end(), 0);
  const auto began = std::chrono::steady_clock::now();
  for (std::size_t epoch = 1; epoch <= epochs; ++epoch) {
    if (shuffle) std::shuffle(order.begin(), order.end(), order_rng);
    for (std::size_t start = 0; start < order.size(); start += 64) {
      const auto end = std::min(start + 64, order.size());
      std::vector<double> pixels;
      std::vector<std::size_t> labels;
      pixels.reserve((end - start) * 784);
      for (std::size_t index = start; index < end; ++index) {
        const auto row = order[index];
        pixels.insert(pixels.end(), training.pixels.begin() + row * 784,
                      training.pixels.begin() + (row + 1) * 784);
        labels.push_back(training.labels[row]);
      }
      for (auto& parameter : parameters) parameter.zero_grad();
      const Tensor inputs({labels.size(), 784}, std::move(pixels));
      Tensor loss = cross_entropy_loss(softmax(model.forward(inputs)), labels);
      loss.backward();
      gradient_step(parameters, learning_rate);
    }
    if (epoch != 1 && epoch % 5 != 0 && epoch != epochs) continue;
    const auto train = evaluate(model, training);
    const auto val = evaluate(model, validation);
    const double seconds = std::chrono::duration<double>(
      std::chrono::steady_clock::now() - began).count();
    if (!std::isfinite(train.loss) || !std::isfinite(val.loss))
      throw std::runtime_error("nonfinite loss");
    std::cout << std::setprecision(8)
      << "{\"name\":\"" << name << "\",\"seed\":" << seed
      << ",\"epoch\":" << epoch << ",\"parameters\":" << parameter_count
      << ",\"train_loss\":" << train.loss << ",\"train_accuracy\":" << train.accuracy
      << ",\"validation_loss\":" << val.loss << ",\"validation_accuracy\":" << val.accuracy
      << ",\"elapsed_seconds\":" << seconds << "}" << std::endl;
  }
}
