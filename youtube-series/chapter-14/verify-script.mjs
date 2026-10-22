// Replays script.md against the frozen Chapter 13 source in a temporary
// directory. Never touches the creator's recording main.cpp.
// Flags: --dump prints each checkpoint's real output and skips output matching.
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {execFileSync} from 'node:child_process';
import {createHash} from 'node:crypto';

const here = path.dirname(fileURLToPath(import.meta.url));
const script = fs.readFileSync(path.join(here, 'script.md'), 'utf8');
const baseline = fs.readFileSync(path.join(here, 'verification/episode-13-baseline.cpp'), 'utf8');
const recording = path.resolve(here, '../../aliases/02-screen-long-form/main.cpp');
const before = fs.readFileSync(recording, 'utf8');
const dump = process.argv.includes('--dump');

const hash = s => createHash('sha256').update(s).digest('hex');
const problems = [];

// Narration and formatting lint (long-form playbook voice rules).
const narration = script.split('\n').filter(l => l.startsWith('>')).map(l => l.replace(/^>\s?/, '')).join('\n');
const banned = [
  [/—|–/, 'dash character (em or en)'],
  [/ -- /, 'double hyphen used as a dash'],
  [/last episode|last time|previous episode|earlier episode/i, 'reference to a previous episode'],
  [/\bimagine\b|\bpicture this\b/i, 'artificial conversational setup'],
  [/It'?s not [^.]*, it'?s /i, 'canned contrast'],
];
for (const [pattern, label] of banned) if (pattern.test(narration)) problems.push('narration: ' + label);
if (/—/.test(script)) problems.push('script contains an em dash');
script.split('\n').forEach((line, i) => {
  if (/\s+$/.test(line)) problems.push(`trailing whitespace on line ${i + 1}`);
  if (/\t/.test(line)) problems.push(`tab on line ${i + 1}`);
});
const words = narration.split(/\s+/).filter(Boolean).length;
console.log('Narration words: ' + words);
if (problems.length) { console.error(problems.join('\n')); process.exit(1); }

const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'dlatwd-ch14-'));
fs.writeFileSync(path.join(temp, 'mnist_reader.hpp'),
  fs.readFileSync(path.resolve(path.dirname(recording), 'mnist_reader.hpp'), 'utf8'));
const data = path.resolve(process.argv.slice(2).find(a => !a.startsWith('--')) ||
  path.join(path.dirname(recording), 'data'));
const compiler = process.env.CXX || 'clang++';
const results = [];
function run(name, source, flags = ['-O2'], timeout = 600000) {
  const file = path.join(temp, name + '.cpp'), binary = path.join(temp, name);
  fs.writeFileSync(file, source);
  try {
    execFileSync(compiler, ['-std=c++23', ...flags, file, '-o', binary], {stdio: 'pipe'});
  } catch (error) {
    console.error(String(error.stderr).split('\n').filter(l => /error|note: candidate/.test(l)).slice(0, 12).join('\n'));
    throw Error('Compilation failed: ' + name);
  }
  const start = Date.now();
  const output = execFileSync(binary, [], {cwd: path.dirname(data), encoding: 'utf8', timeout, maxBuffer: 1 << 26});
  results.push({name, flags, elapsedSeconds: (Date.now() - start) / 1000, output});
  console.log(name + ': PASS (' + ((Date.now() - start) / 1000).toFixed(1) + 's)');
  return output;
}
const lastLoss = output => Number([...output.matchAll(/Epoch \d+ loss: (\S+)/g)].pop()[1]);
const accuracy = output => Number(output.match(/Test accuracy: (\S+)%/)[1]);

const pattern = /<!-- edit: ([\w-]+) -->\s*\*\*Before\*\*\s*\x60{3}cpp\n([\s\S]*?)\n\x60{3}\s*\*\*After\*\*\s*\x60{3}cpp\n([\s\S]*?)\n\x60{3}|<!-- checkpoint: ([\w-]+) -->/g;
let source = baseline, count = 0, checkedOutputs = 0;
const seen = new Set(), sources = {};
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
    sources[m[4]] = source;
    const output = run(m[4], source);
    if (dump) { console.log('----- ' + m[4] + '\n' + output + '-----'); continue; }
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
if (nodeDefinition(source) !== nodeDefinition(baseline)) throw Error('TensorNode must remain unchanged');
const file = path.join(temp, 'final.cpp');
fs.writeFileSync(file, source);
fs.writeFileSync(path.join(here, 'verification/episode-14-final.cpp'), source);

// Claims spoken in the narration that the displayed runs do not show.
const claims = [];
for (const rate of ['0.1', '0.3', '1.0']) {
  const variant = sources['plain-sixteen'].replace('double learning_rate = 0.5;', `double learning_rate = ${rate};`);
  if (variant === sources['plain-sixteen']) throw Error('learning rate variant did not apply');
  const out = run('plain-sixteen-rate-' + rate, variant);
  if (lastLoss(out) < 2.29 || accuracy(out) > 20) throw Error('plain sixteen layers should stay stuck at rate ' + rate);
  claims.push({claim: `plain sixteen layers stays at guessing loss with starting rate ${rate} and decay 0.9`, lastLoss: lastLoss(out), accuracy: accuracy(out)});
}
{
  // Spoken: training the unscaled residual network four times as long at rate 0.5 reaches only about 64%.
  const longer = sources['residual-sixteen'].replace('epoch < 10;', 'epoch < 40;').replace('"/10\\n"', '"/40\\n"');
  if (longer === sources['residual-sixteen']) throw Error('forty-epoch rate 0.5 variant did not apply');
  const out = run('residual-forty-epochs-rate-0.5', longer);
  if (Math.round(accuracy(out)) !== 64) throw Error('forty epochs at rate 0.5 should reach about 64%');
  claims.push({claim: 'residual network, 40 epochs, rate 0.5, decay 0.9: about 64%', lastLoss: lastLoss(out), accuracy: accuracy(out)});
}
{
  const long = source.replace('double learning_rate = 0.1;', 'double learning_rate = 0.05;')
    .replace('learning_rate *= 0.9;', 'learning_rate *= 1.0;')
    .replace('epoch < 10;', 'epoch < 40;').replace('"/10\\n"', '"/40\\n"');
  const out = run('residual-forty-epochs', long);
  if (!(lastLoss(out) < 0.002 && accuracy(out) >= 92 && accuracy(out) <= 94)) throw Error('forty-epoch claim failed');
  claims.push({claim: 'residual network, 40 epochs, rate 0.05, no decay: training loss about 0.001, accuracy about 93%', lastLoss: lastLoss(out), accuracy: accuracy(out)});
}

{
  // Aside tables: every cell is recomputed from the definition of the loss.
  const first = script.match(/\x60{3}text\nloss for one image = -ln\(probability given to the correct digit\)\n\nprobability   loss\n([\s\S]*?)\n\x60{3}/);
  if (!first) throw Error('aside table is missing');
  const rows1 = first[1].split('\n');
  if (rows1.length !== 6) throw Error('aside table has the wrong number of rows');
  for (const row of rows1) {
    const [probability, shown] = row.trim().split(/\s+/);
    if (shown !== (-Math.log(Number(probability))).toFixed(2)) throw Error('probability table row is wrong: ' + row);
  }
  // Spoken: the epoch-1 loss of 52 means about 2e-23, which is 22 zeros after the decimal point.
  const epochOne = Number(results.find(r => r.name === 'residual-sixteen').output.match(/Epoch 1 loss: (\S+)/)[1]);
  if (Math.abs(Math.log10(2e-23) - Math.log10(Math.exp(-epochOne))) > 0.01) throw Error('epoch 1 loss does not correspond to about 2e-23');
  if (!/^0\.0{22}2/.test((2e-23).toFixed(24))) throw Error('2e-23 should have 22 zeros after the decimal point');
  console.log('aside table: 6 rows match their definition');

  // Spoken: during the first epoch at rate 0.5 the scores reach the hundreds, the loss is about the size of the
  // score gap, and the accuracy over those first batches stays near chance.
  const probe = sources['residual-sixteen'];
  const printing = `        if (epoch == 0 && seen / 64 < 12) {
          double top = 0, gap = 0;
          std::size_t right = 0;
          for (const double value: logits.data()) top = std::max(top, std::abs(value));
          for (std::size_t row = 0; row < batch.labels.size(); ++row) {
            std::size_t best = 0;
            for (std::size_t digit = 1; digit < 10; ++digit) {
              if (logits.at({row, digit}) > logits.at({row, best})) best = digit;
            }
            right += best == batch.labels[row];
            gap += logits.at({row, best}) - logits.at({row, batch.labels[row]});
          }
          std::cout << "BATCH " << top << " " << right << " " << batch.labels.size() << " "
            << loss.at({}) << " " << gap / batch.labels.size() << "\\n";
        }
        if (epoch == 0 && seen == 0) {`;
  const instrumented = probe.replace('        if (epoch == 0 && seen == 0) {', printing).replace('epoch < 10;', 'epoch < 1;');
  if (instrumented === probe) throw Error('first-epoch probe did not apply');
  const out = run('residual-first-epoch', instrumented);
  const batches = out.split('\n').filter(l => l.startsWith('BATCH ')).map(l => l.split(' ').slice(1).map(Number));
  if (batches.length !== 12) throw Error('expected twelve probed batches');
  const top = Math.max(...batches.map(b => b[0]));
  const right = batches.reduce((t, b) => t + b[1], 0), images = batches.reduce((t, b) => t + b[2], 0);
  if (!(top >= 100)) throw Error('scores should reach the hundreds in the first epoch');
  if (!(Math.max(...batches.map(b => b[3])) >= 50)) throw Error('some first-epoch batch loss should exceed 50');
  for (const [, , , loss, gap] of batches) {
    if (!(loss - gap > -1e-9 && loss - gap < Math.log(10) + 1e-9)) throw Error('loss must be within ln(10) of the mean score gap');
  }
  if (!(right / images < 0.15)) throw Error('accuracy over the first batches should stay near chance');
  claims.push({claim: 'first twelve batches at rate 0.5: largest score, loss within ln(10) of the mean score gap, accuracy near chance', largestScore: top, accuracy: right / images});
}

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

static_assert(std::is_base_of_v<Layer, Sequence>, "Sequence must be a Layer");
static_assert(std::is_base_of_v<Layer, Residual>, "Residual must be a Layer");
static_assert(!std::is_abstract_v<Residual>, "Residual must be concrete");
static_assert(!std::is_abstract_v<Sequence>, "Sequence must be concrete");
static_assert(std::is_move_constructible_v<Sequence>, "hidden_layer returns a Sequence by value");
static_assert(std::is_move_constructible_v<Residual>, "Residual can be pushed back by value");

Sequence flat_model(std::mt19937& random, int hidden) {
  Sequence model;
  model.push_back(Linear(784, 32, random));
  model.push_back(Tanh());
  for (int i = 1; i < hidden; ++i) {
    model.push_back(Linear(32, 32, random));
    model.push_back(Tanh());
  }
  model.push_back(Linear(32, 10, random));
  return model;
}
Sequence plain_model(std::mt19937& random, int hidden) {
  Sequence model;
  model.push_back(hidden_layer(784, 32, random));
  for (int i = 1; i < hidden; ++i) model.push_back(hidden_layer(32, 32, random));
  model.push_back(Linear(32, 10, random));
  return model;
}
Sequence residual_model(std::mt19937& random, int hidden) {
  Sequence model;
  model.push_back(hidden_layer(784, 32, random));
  for (int i = 1; i < hidden; ++i) model.push_back(Residual(hidden_layer(32, 32, random)));
  model.push_back(Linear(32, 10, random));
  return model;
}

struct Rows { std::vector<double> signal, gradient; double loss; };
Rows rows(Sequence& model, const Tensor& inputs, const std::vector<std::size_t>& labels) {
  for (Tensor& p : model.parameters()) p.zero_grad();
  const std::vector<Sequence::TracedOutput> trace = model.forward_traced(inputs);
  Tensor loss = cross_entropy_loss(softmax(trace.back().output), labels);
  loss.backward();
  Rows result{{}, {}, loss.at({})};
  for (const Sequence::TracedOutput& entry : trace) {
    result.signal.push_back(root_mean_square(entry.output.data()));
    result.gradient.push_back(root_mean_square(entry.output.grad()));
  }
  return result;
}

int main() {
  std::size_t checked = 0;

  MnistReader reader("data/train-images-idx3-ubyte", "data/train-labels-idx1-ubyte");
  MnistBatch batch = reader.read_batch(64);
  const std::vector<double> pixels = batch.pixels;
  const std::vector<std::size_t> labels = batch.labels;
  const Tensor inputs({labels.size(), 784}, pixels);

  {  // hidden_layer builds exactly the flat Linear + Tanh list.
    std::mt19937 a(42), b(42);
    Sequence flat = flat_model(a, 8), named = plain_model(b, 8);
    close(cross_entropy_loss(softmax(flat.forward(inputs)), labels).at({}),
          cross_entropy_loss(softmax(named.forward(inputs)), labels).at({}), 1e-12);
    require(flat.parameters().size() == named.parameters().size(), "same parameter count");
    ++checked;
  }
  {  // forward_traced ends with forward's result and records every top-level layer.
    std::mt19937 a(42);
    Sequence model = plain_model(a, 16);
    const std::vector<Sequence::TracedOutput> trace = model.forward_traced(inputs);
    require(trace.size() == 17, "sixteen hidden layers plus the output layer");
    require(trace[0].name == "Sequence[Linear, Tanh]" && trace[16].name == "Linear", "layer names");
    const Tensor direct = model.forward(inputs);
    for (std::size_t i = 0; i < direct.numel(); ++i) close(trace.back().output.data()[i], direct.data()[i], 1e-12);
    ++checked;
  }
  {  // Residual adds the input to the body, and gradients match finite differences.
    const Tensor x({2, 3}, {0.1, -0.4, 0.9, 0.5, 0.2, -0.7});
    std::mt19937 c(7), d(7);
    Residual block(hidden_layer(3, 3, c));
    Sequence body = hidden_layer(3, 3, d);
    const Tensor out = block.forward(x), expected = x + body.forward(x);
    for (std::size_t i = 0; i < out.numel(); ++i) close(out.data()[i], expected.data()[i], 1e-12);
    require(block.parameters().size() == 2, "Residual exposes its body's parameters");
    ++checked;
    const std::vector<Tensor> parameters = block.parameters();
    const Tensor targets({2, 3}, {0.5, -0.2, 0.7, 0.1, 0.3, -0.6});
    for (const Tensor& parameter : parameters) {
      Tensor mutable_parameter = parameter;
      for (std::size_t i = 0; i < mutable_parameter.numel(); ++i) {
        for (const Tensor& p : parameters) { Tensor q = p; q.zero_grad(); }
        Tensor loss = mse_loss(block.forward(x), targets);
        loss.backward();
        const double analytic = mutable_parameter.grad()[i];
        const double original = mutable_parameter.data()[i];
        mutable_parameter.data()[i] = original + 1e-6;
        const double plus = mse_loss(block.forward(x), targets).at({});
        mutable_parameter.data()[i] = original - 1e-6;
        const double minus = mse_loss(block.forward(x), targets).at({});
        mutable_parameter.data()[i] = original;
        close(analytic, (plus - minus) / 2e-6, 1e-6);
        ++checked;
      }
    }
  }
  {  // push_back takes layers by value: the layer is moved in and owned by the Sequence.
    std::mt19937 a(3);
    Sequence outer;
    Linear source(4, 4, a);
    outer.push_back(source);  // a copy shares the same parameter tensors
    outer.push_back(Tanh());
    require(outer.parameters().size() == 2, "by-value push_back keeps parameters");
    close(outer.parameters()[0].data()[0], source.parameters()[0].data()[0], 1e-12);
    ++checked;
  }
  {  // A Sequence can hold a Sequence.
    std::mt19937 a(1);
    Sequence outer;
    outer.push_back(hidden_layer(4, 4, a));
    require(outer.parameters().size() == 2, "nested Sequence parameters");
    const Sequence& read_only = outer;
    require(read_only.parameters().size() == 2, "const parameters");
    ++checked;
  }

  // Signal and gradient measurements on a real MNIST batch at starting weights.
  std::mt19937 plain_random(42), residual_random(42);
  Sequence plain = plain_model(plain_random, 16), residual = residual_model(residual_random, 16);
  const Rows p = rows(plain, inputs, labels), r = rows(residual, inputs, labels);
  const double plain_gradient_ratio = p.gradient[0] / p.gradient[15];
  const double plain_signal_ratio = p.signal[15] / p.signal[0];
  const double per_layer = std::pow(plain_gradient_ratio, 1.0 / 15.0);
  std::cout << "PROBE plain_signal_last_over_first=" << plain_signal_ratio
            << " plain_gradient_first_over_last=" << plain_gradient_ratio
            << " per_layer=" << per_layer
            << " residual_signal_last_over_first=" << r.signal[15] / r.signal[0]
            << " residual_gradient_first_over_last=" << r.gradient[0] / r.gradient[15]
            << " plain_loss=" << p.loss << " residual_loss=" << r.loss << "\\n";
  require(plain_signal_ratio < 1e-3, "plain signal must shrink through sixteen layers");
  require(plain_gradient_ratio < 1e-3, "plain gradient must shrink going backward");
  require(per_layer > 0.4 && per_layer < 0.7, "about half per layer");
  require(plain.parameters().size() == 34 && residual.parameters().size() == 34, "34 parameter tensors");
  require(r.gradient[0] / r.gradient[15] > 6 && r.gradient[0] / r.gradient[15] < 8, "residual gradient grows about seven times toward the input");
  require(r.signal[15] / r.signal[0] > 4, "residual signal grows more than four times");
  require(r.loss > p.loss, "residual starting scores are too large: its starting loss is above guessing");
  require(r.gradient[0] > r.gradient[15], "residual gradient must not vanish toward the input");
  require(r.gradient[0] / p.gradient[0] > 3e4, "residual first-layer gradient must be more than thirty thousand times larger");
  require(p.signal[0] / p.signal[15] > 6e3, "plain signal must be more than six thousand times smaller");
  require(p.gradient[16] / p.gradient[0] > 1.4e4 && p.gradient[16] / p.gradient[0] < 1.6e4, "about fifteen thousand");

  std::cout << checked << " checks; hidden_layer equals the flat list, Residual and traces: PASS\\n";
}
`;
const testOutput = run('layer-checks', harness, ['-O1', '-g', '-fsanitize=address,undefined']);
const probeLine = testOutput.split('\n').find(l => l.startsWith('PROBE')) || '';
console.log(probeLine);
run('final-sanitized', source, ['-O1', '-g', '-fsanitize=address,undefined'], 1800000);
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
  recordingSha256: hash(before), recordingUnchanged: true,
  edits: count, displayedOutputLinesMatched: checkedOutputs, narrationWords: words,
  probe: probeLine, claims, datasetDirectory: data, datasetFiles: manifest, results,
};
if (!dump) fs.writeFileSync(path.join(here, 'verification-run.json'), JSON.stringify(report, null, 2) + '\n');
console.log(`Complete: ${count} edits; recording source unchanged.`);
