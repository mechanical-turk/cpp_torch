// Replay Chapter 11 against the frozen, actually recorded Chapter 10 source.
// All generated programs live in a temporary directory, never the recording repo.
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {execFileSync} from 'node:child_process';
import {createHash} from 'node:crypto';

const here = path.dirname(fileURLToPath(import.meta.url));
const script = fs.readFileSync(path.join(here, 'script.md'), 'utf8');
const baseline = fs.readFileSync(path.join(here, 'verification/episode-10-baseline.cpp'), 'utf8');
const recordingPath = path.resolve(here, '../../aliases/02-screen-long-form/main.cpp');
const recordingBefore = fs.readFileSync(recordingPath, 'utf8');
const temporary = fs.mkdtempSync(path.join(os.tmpdir(), 'dlatwd-episode11-'));
const compiler = process.env.CXX || 'clang++';
const hash = value => createHash('sha256').update(value).digest('hex');
const results = [];
const seen = new Set();
const pattern = /<!-- edit: ([\w-]+) -->\s*\*\*Before\*\*\s*\x60{3}cpp\n([\s\S]*?)\n\x60{3}\s*\*\*After\*\*\s*\x60{3}cpp\n([\s\S]*?)\n\x60{3}|<!-- checkpoint: ([\w-]+) -->/g;
const steps = [...script.matchAll(pattern)];
if (steps.filter(x => x[1]).length !== [...script.matchAll(/<!-- edit:/g)].length)
  throw Error('Unparsed edit');

function run(name, source, flags = ['-O1', '-g', '-fsanitize=address,undefined']) {
  const file = path.join(temporary, name + '.cpp');
  const executable = path.join(temporary, name);
  fs.writeFileSync(file, source);
  execFileSync(compiler, ['-std=c++23', ...flags, file, '-o', executable], {stdio: 'pipe'});
  const output = execFileSync(executable, [], {encoding: 'utf8'});
  results.push({name, flags, output});
  console.log(name + ': PASS');
  return output;
}

run('baseline', baseline);
let code = baseline;
for (const match of steps) {
  const [, id, before, after, checkpoint] = match;
  if (id) {
    if (seen.has(id)) throw Error('Duplicate edit: ' + id);
    seen.add(id);
    const index = code.indexOf(before);
    if (index < 0 || index !== code.lastIndexOf(before))
      throw Error('Missing or ambiguous Before: ' + id);
    code = code.slice(0, index) + after + code.slice(index + before.length);
  } else {
    run(checkpoint, code);
  }
}
const optimized = run('final-optimized', code, ['-O2']);
for (const expected of [
  'Loss: 0.779 -> 0.000',
  '0.000 0.000 0.000 0.000',
  '0.000 1.000 1.000 1.000',
  '1.000 0.000 1.000 1.000',
  '1.000 1.000 0.000 0.000'
]) {
  if (!optimized.includes(expected)) throw Error('Unexpected recorded output: ' + expected);
}

const finalPath = path.join(temporary, 'final.cpp');
fs.writeFileSync(finalPath, code);
const tests = `
#define main recorded_main
#include "${finalPath}"
#undef main

void require(bool condition, const char* message) {
  if (!condition) throw std::runtime_error(message);
}
void close(double actual, double expected, double tolerance = 1e-5) {
  require(std::isfinite(actual) && std::abs(actual - expected) < tolerance, "numeric mismatch");
}
int main() {
  const Tensor inputs({4, 2}, {0,0, 0,1, 1,0, 1,1});
  const Tensor targets({4, 1}, {0,1,1,0});
  std::mt19937 random(42);
  Linear layer(2, 3, random);
  auto layer_parameters = layer.parameters();
  require(layer_parameters[0].shape() == std::vector<std::size_t>({2,3}), "weight layout");
  require(layer_parameters[1].shape() == std::vector<std::size_t>({3}), "bias layout");
  Tensor layer_result = layer.forward(inputs);
  require(layer_result.shape() == std::vector<std::size_t>({4,3}), "forward shape");
  Tensor sum = layer_result.sum();
  sum.backward();
  for (double gradient : layer_parameters[0].grad()) close(gradient, 2.0);
  for (double gradient : layer_parameters[1].grad()) close(gradient, 4.0);

  for (const auto& sizes : {std::pair<std::size_t,std::size_t>{0,3}, {2,0},
       {std::numeric_limits<std::size_t>::max(),2}}) {
    bool rejected = false;
    try { Linear invalid(sizes.first, sizes.second, random); }
    catch (const std::invalid_argument&) { rejected = true; }
    require(rejected, "invalid size accepted");
  }

  MLP model(2, 4, 1, random);
  auto parameters = model.parameters();
  require(parameters.size() == 4, "parameter count");
  std::size_t values = 0;
  for (const auto& p : parameters) values += p.numel();
  require(values == 17, "scalar parameter count");
  auto second_handles = model.parameters();
  for (std::size_t i = 0; i < parameters.size(); ++i) {
    require(&parameters[i].data() == &second_handles[i].data(), "parameter copy lost sharing");
    for (std::size_t j = 0; j < i; ++j)
      require(&parameters[i].data() != &parameters[j].data(), "unexpected shared parameter");
  }
  Tensor loss = mse_loss(model.forward(inputs), targets);
  loss.backward();
  const double epsilon = 1e-6;
  std::size_t checks = 0;
  for (Tensor& parameter : parameters) {
    for (std::size_t i = 0; i < parameter.numel(); ++i) {
      const double original = parameter.data()[i];
      const double analytic = parameter.grad()[i];
      parameter.data()[i] = original + epsilon;
      const double plus = mse_loss(model.forward(inputs), targets).at({});
      parameter.data()[i] = original - epsilon;
      const double minus = mse_loss(model.forward(inputs), targets).at({});
      parameter.data()[i] = original;
      close(analytic, (plus - minus) / (2 * epsilon));
      ++checks;
    }
  }
  const auto before = parameters[0].data();
  const auto gradients = parameters[0].grad();
  gradient_step(parameters, 0.1);
  for (std::size_t i = 0; i < before.size(); ++i)
    close(model.parameters()[0].data()[i], before[i] - 0.1 * gradients[i]);

  for (unsigned seed = 0; seed < 10; ++seed) {
    std::mt19937 generator(seed);
    MLP network(2, 4, 1, generator);
    auto trainable = network.parameters();
    for (std::size_t step = 0; step < 5000; ++step) {
      for (Tensor& parameter : trainable) parameter.zero_grad();
      Tensor current_loss = mse_loss(network.forward(inputs), targets);
      current_loss.backward();
      gradient_step(trainable, 0.1);
    }
    const Tensor prediction = network.forward(inputs);
    const double error = mse_loss(prediction, targets).at({});
    require(std::isfinite(error) && error < 0.001, "XOR failed across seeds");
    for (std::size_t row = 0; row < 4; ++row)
      require((prediction.at({row,0}) > 0.5) == (targets.at({row,0}) == 1.0), "XOR classification");
    std::cout << "seed " << seed << ": loss " << error << '\\n';
  }
  std::cout << checks << " finite-difference parameter checks: PASS\\n";
  std::cout << "layout, broadcasting, shared handles, updates, invalid sizes: PASS\\n";
}
`;
run('module-and-training-checks', tests);
if (fs.readFileSync(recordingPath, 'utf8') !== recordingBefore)
  throw Error('Recording source changed during verification');
const report = {
  baselineSha256: hash(baseline),
  recordingSha256: hash(recordingBefore),
  recordingMatchesBaseline: recordingBefore.trimEnd() === baseline.trimEnd(),
  scriptSha256: hash(script),
  resultSha256: hash(code),
  literalEdits: seen.size,
  compiler: execFileSync(compiler, ['--version'], {encoding:'utf8'}).split('\n')[0],
  results
};
fs.writeFileSync(path.join(here, 'verification-run.json'), JSON.stringify(report, null, 2) + '\n');
console.log('Edits: ' + seen.size + '; recording source unchanged; artifacts: ' + temporary);

