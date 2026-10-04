// Replays script.md against the frozen Chapter 12 source in a temporary
// directory. Never touches the creator's recording main.cpp.
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {execFileSync} from 'node:child_process';
import {createHash} from 'node:crypto';

const here = path.dirname(fileURLToPath(import.meta.url));
const script = fs.readFileSync(path.join(here, 'script.md'), 'utf8');
const baseline = fs.readFileSync(path.join(here, 'verification/episode-12-baseline.cpp'), 'utf8');
const recording = path.resolve(here, '../../aliases/02-screen-long-form/main.cpp');
const before = fs.readFileSync(recording, 'utf8');
const recordingMatchesBaseline = before.trimEnd() === baseline.trimEnd();
if (!recordingMatchesBaseline && !process.argv.includes('--frozen-baseline'))
  throw Error('Recording has progressed. Use --frozen-baseline to replay the lesson without changing live code.');

const hash = s => createHash('sha256').update(s).digest('hex');
const problems = [];

// Narration and formatting lint (long-form playbook voice rules).
const narration = script.split('\n').filter(l => l.startsWith('>')).map(l => l.replace(/^>\s?/, '')).join('\n');
const banned = [
  [/—|–/, 'dash character (em or en)'],
  [/ -- /, 'double hyphen used as a dash'],
  [/last episode|last time|previous episode/i, 'reference to a previous episode'],
  [/\bimagine\b|\bpicture this\b/i, 'artificial conversational setup'],
  [/It'?s not [^.]*, it'?s /i, 'canned contrast'],
];
for (const [pattern, label] of banned) {
  if (pattern.test(narration)) problems.push('narration: ' + label);
  if (/—/.test(script)) problems.push('script contains an em dash');
}
script.split('\n').forEach((line, i) => {
  if (/\s+$/.test(line)) problems.push(`trailing whitespace on line ${i + 1}`);
  if (/\t/.test(line)) problems.push(`tab on line ${i + 1}`);
});
const words = narration.split(/\s+/).filter(Boolean).length;
console.log('Narration words: ' + words);
if (problems.length) { console.error(problems.join('\n')); process.exit(1); }

const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'dlatwd-ch13-'));
fs.writeFileSync(path.join(temp, 'mnist_reader.hpp'),
  fs.readFileSync(path.resolve(path.dirname(recording), 'mnist_reader.hpp'), 'utf8'));
const data = path.resolve(process.argv.slice(2).find(a => !a.startsWith('--')) ||
  path.join(path.dirname(recording), 'data'));
const compiler = process.env.CXX || 'clang++';
const results = [];
function run(name, source, flags = ['-O2'], timeout = 300000) {
  const file = path.join(temp, name + '.cpp'), binary = path.join(temp, name);
  fs.writeFileSync(file, source);
  try {
    execFileSync(compiler, ['-std=c++23', ...flags, file, '-o', binary], {stdio: 'pipe'});
  } catch (error) {
    console.error(String(error.stderr).split('\n').filter(l => /error|note: candidate/.test(l)).slice(0, 12).join('\n'));
    throw Error('Compilation failed: ' + name);
  }
  const start = Date.now();
  const output = execFileSync(binary, [], {cwd: path.dirname(data), encoding: 'utf8', timeout});
  results.push({name, flags, elapsedSeconds: (Date.now() - start) / 1000, output});
  console.log(name + ': PASS');
  return output;
}

const pattern = /<!-- edit: ([\w-]+) -->\s*\*\*Before\*\*\s*\x60{3}cpp\n([\s\S]*?)\n\x60{3}\s*\*\*After\*\*\s*\x60{3}cpp\n([\s\S]*?)\n\x60{3}|<!-- checkpoint: ([\w-]+) -->/g;
let source = baseline, count = 0, checkedOutputs = 0;
const seen = new Set();
const matches = [...script.matchAll(pattern)];
for (const m of matches) {
  if (m[1]) {
    const [, id, b, a] = m;
    if (seen.has(id)) throw Error('Duplicate edit id ' + id);
    if (b === a) throw Error('Edit changes nothing: ' + id);
    if (source.indexOf(b) < 0) throw Error('Before block not found in the evolving source: ' + id);
    if (source.indexOf(b) !== source.lastIndexOf(b)) throw Error('Before block is ambiguous: ' + id);
    seen.add(id);
    source = source.replace(b, () => a);
    ++count;
  } else {
    const output = run(m[4], source);
    const rest = script.slice(m.index + m[0].length);
    const next = rest.indexOf('<!-- ');
    const segment = next < 0 ? rest : rest.slice(0, next);
    const block = segment.match(/\x60{3}output\n([\s\S]*?)\n\x60{3}/);
    if (!block) throw Error('Checkpoint has no displayed output block: ' + m[4]);
    const actualLines = output.split('\n');
    for (const line of block[1].split('\n')) {
      if (!actualLines.includes(line))
        throw Error(`Displayed output line not produced by ${m[4]}: "${line}"`);
      ++checkedOutputs;
    }
  }
}
if (count !== [...script.matchAll(/<!-- edit:/g)].length) throw Error('Unparsed edit');
console.log(`${count} edits replayed; ${checkedOutputs} displayed output lines matched real output.`);

const nodeDefinition = text => text.match(/struct TensorNode \{[\s\S]*?\n\};/)[0];
if (nodeDefinition(source) !== nodeDefinition(baseline))
  throw Error('TensorNode must remain unchanged');
const file = path.join(temp, 'final.cpp');
fs.writeFileSync(file, source);
fs.writeFileSync(path.join(here, 'verification/episode-13-final.cpp'), source);

const harness = `
#define main recorded_main
#include "${file}"
#undef main
#include <sstream>
#include <type_traits>

void require(bool yes, const char* message) {
  if (!yes) throw std::runtime_error(message);
}
void close(double a, double b, double tolerance = 1e-5) {
  require(std::isfinite(a) && std::abs(a - b) < tolerance, "numeric mismatch");
}
double vector_norm(const std::vector<double>& values) {
  double total = 0.0;
  for (double value : values) total += value * value;
  return std::sqrt(total);
}
double dot(const std::vector<double>& a, const std::vector<double>& b) {
  double total = 0.0;
  for (std::size_t i = 0; i < a.size(); ++i) total += a[i] * b[i];
  return total;
}
double rms(const Tensor& tensor) {
  double total = 0.0;
  for (double value : tensor.data()) total += value * value;
  return std::sqrt(total / tensor.numel());
}

// Written out layer by layer, exactly as the script's final model is.
Sequence deep_model(std::mt19937& random) {
  Sequence model;
  model.push_back(std::make_unique<Linear>(784, 32, random));
  model.push_back(std::make_unique<Tanh>());
  model.push_back(std::make_unique<Linear>(32, 32, random));
  model.push_back(std::make_unique<Tanh>());
  model.push_back(std::make_unique<Linear>(32, 32, random));
  model.push_back(std::make_unique<Tanh>());
  model.push_back(std::make_unique<Linear>(32, 32, random));
  model.push_back(std::make_unique<Tanh>());
  model.push_back(std::make_unique<Linear>(32, 32, random));
  model.push_back(std::make_unique<Tanh>());
  model.push_back(std::make_unique<Linear>(32, 32, random));
  model.push_back(std::make_unique<Tanh>());
  model.push_back(std::make_unique<Linear>(32, 32, random));
  model.push_back(std::make_unique<Tanh>());
  model.push_back(std::make_unique<Linear>(32, 32, random));
  model.push_back(std::make_unique<Tanh>());
  model.push_back(std::make_unique<Linear>(32, 10, random));
  return model;
}

static_assert(std::is_abstract_v<Layer>, "Layer must be abstract");
static_assert(std::has_virtual_destructor_v<Layer>, "Layer needs a virtual destructor");
static_assert(std::is_base_of_v<Layer, Linear>, "Linear must be a Layer");
static_assert(std::is_base_of_v<Layer, Tanh>, "Tanh must be a Layer");
static_assert(!std::is_base_of_v<Layer, MLP>, "MLP is left unchanged");

struct Probe {
  double loss, sequence_loss, activation_ratio, gradient_ratio, per_layer, deep_weight_norm, shallow_weight_norm;
};
// Real MNIST batch, starting weights, eight hidden layers of 32 features.
Probe probe() {
  std::mt19937 random(42);
  std::vector<Linear> layers;
  layers.emplace_back(784, 32, random);
  for (int i = 1; i < 8; ++i) layers.emplace_back(32, 32, random);
  Linear output(32, 10, random);
  Tanh activation;
  MnistReader reader("data/train-images-idx3-ubyte", "data/train-labels-idx1-ubyte");
  MnistBatch batch = reader.read_batch(64);
  const std::vector<double> pixels = batch.pixels;
  const std::vector<std::size_t> labels = batch.labels;
  const Tensor inputs({labels.size(), 784}, pixels);
  std::vector<Tensor> activations;
  Tensor hidden = inputs;
  for (Linear& layer : layers) {
    hidden = activation.forward(layer.forward(hidden));
    activations.push_back(hidden);
  }
  Tensor loss = cross_entropy_loss(softmax(output.forward(hidden)), labels);
  loss.backward();
  double deep_total = vector_norm(output.parameters()[0].grad());
  deep_total *= deep_total;
  for (Linear& layer : layers) {
    const double n = vector_norm(layer.parameters()[0].grad());
    deep_total += n * n;
  }

  std::mt19937 same_seed(42);
  Sequence model = deep_model(same_seed);
  const double sequence_loss = cross_entropy_loss(softmax(model.forward(inputs)), labels).at({});

  std::mt19937 shallow_random(42);
  MLP shallow(784, 32, 10, shallow_random);
  std::vector<Tensor> shallow_parameters = shallow.parameters();
  Tensor shallow_loss = cross_entropy_loss(softmax(shallow.forward(inputs)), labels);
  shallow_loss.backward();
  const double s0 = vector_norm(shallow_parameters[0].grad());
  const double s2 = vector_norm(shallow_parameters[2].grad());

  const double gradient_ratio =
      vector_norm(activations.front().grad()) / vector_norm(activations.back().grad());
  return {loss.at({}), sequence_loss, rms(activations.back()) / rms(activations.front()),
          gradient_ratio, std::pow(gradient_ratio, 1.0 / 7.0), std::sqrt(deep_total),
          std::sqrt(s0 * s0 + s2 * s2)};
}

// Mean cosine between consecutive gradients of the first weight matrix, plain
// gradient descent, first 100 batches.
double gradient_alignment() {
  std::mt19937 random(42);
  Sequence model = deep_model(random);
  std::vector<Tensor> parameters = model.parameters();
  MnistReader reader("data/train-images-idx3-ubyte", "data/train-labels-idx1-ubyte");
  std::vector<double> previous;
  double total = 0.0;
  int count = 0;
  for (int step = 0; step < 100; ++step) {
    MnistBatch batch = reader.read_batch(64);
    const Tensor inputs({batch.labels.size(), 784}, std::move(batch.pixels));
    for (Tensor& parameter : parameters) parameter.zero_grad();
    Tensor loss = cross_entropy_loss(softmax(model.forward(inputs)), batch.labels);
    loss.backward();
    const std::vector<double> gradient = parameters[0].grad();
    if (!previous.empty()) {
      total += dot(gradient, previous) / (vector_norm(gradient) * vector_norm(previous));
      ++count;
    }
    previous = gradient;
    gradient_step(parameters, 0.1);
  }
  return total / count;
}

int main() {
  std::size_t checked = 0;

  {
    Tensor w({2}, {1.0, 2.0});
    Tensor loss = (w * w).sum();
    loss.backward();
    std::vector<Tensor> parameters{w};
    gradient_step(parameters, 0.1);
    close(w.data()[0], 0.8); close(w.data()[1], 1.6);
  }

  {
    std::mt19937 first(42), second(42);
    MLP mlp(3, 4, 2, first);
    Sequence sequence;
    sequence.push_back(std::make_unique<Linear>(3, 4, second));
    sequence.push_back(std::make_unique<Tanh>());
    sequence.push_back(std::make_unique<Linear>(4, 2, second));
    const Tensor x({2, 3}, {0.1, -0.4, 0.9, 0.5, 0.2, -0.7});
    const Tensor from_mlp = mlp.forward(x);
    const Tensor from_sequence = sequence.forward(x);
    require(from_mlp.data() == from_sequence.data(), "Sequence must equal MLP exactly");
    std::vector<Tensor> mp = mlp.parameters(), sp = sequence.parameters();
    require(mp.size() == sp.size(), "same parameter count");
    for (std::size_t i = 0; i < mp.size(); ++i) require(mp[i].data() == sp[i].data(), "same parameters");
  }

  std::mt19937 rng(3);
  Sequence model;
  model.push_back(std::make_unique<Linear>(3, 4, rng));
  model.push_back(std::make_unique<Tanh>());
  model.push_back(std::make_unique<Linear>(4, 4, rng));
  model.push_back(std::make_unique<Tanh>());
  model.push_back(std::make_unique<Linear>(4, 4, rng));
  model.push_back(std::make_unique<Tanh>());
  model.push_back(std::make_unique<Linear>(4, 1, rng));
  std::vector<Tensor> parameters = model.parameters();
  require(parameters.size() == 8, "parameter count");
  const Tensor x({4, 3}, {0.1, 0.7, -0.3, 0.2, -0.5, 0.9, -0.8, 0.4, 0.6, 0.3, 0.3, -0.2});
  const Tensor targets({4, 1}, {0.5, -0.2, 0.7, 0.1});
  require(model.forward(x).shape() == std::vector<std::size_t>({4, 1}), "output shape");
  Tensor loss = mse_loss(model.forward(x), targets);
  loss.backward();
  for (Tensor& parameter : parameters) {
    for (std::size_t i = 0; i < parameter.numel(); ++i) {
      const double original = parameter.data()[i];
      parameter.data()[i] = original + 1e-5;
      const double plus = mse_loss(model.forward(x), targets).at({});
      parameter.data()[i] = original - 1e-5;
      const double minus = mse_loss(model.forward(x), targets).at({});
      parameter.data()[i] = original;
      close(parameter.grad()[i], (plus - minus) / 2e-5); ++checked;
    }
  }
  {
    const double old_value = model.forward(x).at({0, 0});
    parameters[0].data()[0] += 1.0;
    require(std::abs(model.forward(x).at({0, 0}) - old_value) > 1e-6, "parameter handles must reach the model");
    parameters[0].data()[0] -= 1.0;
  }

  {
    Sequence tanh_only;
    tanh_only.push_back(std::make_unique<Tanh>());
    const Tensor input({1, 3}, {-1.0, 0.0, 2.0});
    close(tanh_only.forward(input).at({0, 2}), std::tanh(2.0), 1e-12);
    require(tanh_only.parameters().empty(), "Tanh has no parameters");
    Sequence empty;
    const Tensor same = empty.forward(input);
    for (std::size_t i = 0; i < input.numel(); ++i) close(same.data()[i], input.data()[i], 1e-12);
    require(empty.parameters().empty(), "empty sequence has no parameters");
    std::unique_ptr<Layer> through_base = std::make_unique<Linear>(2, 2, rng);
    require(through_base->forward(Tensor({1, 2}, {1.0, 1.0})).shape() == std::vector<std::size_t>({1, 2}),
            "Linear reached through a Layer pointer");
    require(through_base->parameters().size() == 2, "Linear reports weight and bias through the base");
    std::unique_ptr<Layer> tanh_base = std::make_unique<Tanh>();
    require(tanh_base->parameters().empty(), "Tanh reports no parameters through the base");
    const Sequence& read_only = model;
    require(read_only.parameters().size() == 8, "parameters() works on a const Sequence");
  }

  {
    std::mt19937 shape_rng(42);
    Sequence deep = deep_model(shape_rng);
    require(deep.parameters().size() == 18, "deep model has nine Linear layers");
  }

  const Probe p = probe();
  const double alignment = gradient_alignment();
  std::cout << "PROBE initial_loss=" << p.loss << " ln10=" << std::log(10.0)
            << " activation_last_over_first=" << p.activation_ratio
            << " gradient_first_over_last=" << p.gradient_ratio << " per_layer=" << p.per_layer
            << " weight_gradient_norm_deep=" << p.deep_weight_norm
            << " shallow=" << p.shallow_weight_norm
            << " shallow_over_deep=" << p.shallow_weight_norm / p.deep_weight_norm
            << " consecutive_gradient_cosine=" << alignment << "\\n";
  close(p.loss, std::log(10.0), 0.01);
  close(p.loss, p.sequence_loss, 1e-12);
  require(p.activation_ratio < 0.05, "forward signal must shrink through the stack");
  require(p.gradient_ratio < 0.05, "gradient must shrink going backward");
  require(p.per_layer > 0.4 && p.per_layer < 0.7, "about half per layer");
  require(p.shallow_weight_norm / p.deep_weight_norm > 50.0, "weight gradients must be more than fifty times smaller");

  std::cout << checked << " finite-difference checks; Sequence equals MLP, handles, shapes: PASS\\n";
}
`;
const testOutput = run('sequence-checks', harness, ['-O1', '-g', '-fsanitize=address,undefined']);
const gradientLine = testOutput.split('\n').find(l => l.startsWith('PROBE')) || '';
console.log(gradientLine);
run('final-sanitized', source, ['-O1', '-g', '-fsanitize=address,undefined'], 900000);
if (fs.readFileSync(recording, 'utf8') !== before) throw Error('Recording source changed');

const manifest = ['train-images-idx3-ubyte', 'train-labels-idx1-ubyte', 't10k-images-idx3-ubyte', 't10k-labels-idx1-ubyte']
  .map(name => {
    const bytes = fs.readFileSync(path.join(data, name));
    return {name, bytes: bytes.length, sha256: hash(bytes)};
  });
const report = {
  date: new Date().toISOString(),
  compiler: execFileSync(compiler, ['--version'], {encoding: 'utf8'}).split('\n')[0],
  scriptSha256: hash(script), baselineSha256: hash(baseline), finalSha256: hash(source),
  recordingSha256: hash(before), recordingMatchesBaseline, recordingUnchanged: true,
  edits: count, displayedOutputLinesMatched: checkedOutputs, narrationWords: words,
  gradientProbe: gradientLine, datasetDirectory: data, datasetFiles: manifest, results,
};
fs.writeFileSync(path.join(here, 'verification-run.json'), JSON.stringify(report, null, 2) + '\n');
console.log(`Complete: ${count} edits; recording source unchanged.`);
