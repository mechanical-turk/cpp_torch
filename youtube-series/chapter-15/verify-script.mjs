// Replays script.md against the frozen Episode 14 source (verification/episode-14-baseline.cpp) in a
// temporary directory. Never touches the creator's recording main.cpp.
// Flags: --dump prints each run's real output and skips output matching; --quick skips the table and seed claims.
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {execFileSync, execFile} from 'node:child_process';
import {createHash} from 'node:crypto';

const here = path.dirname(fileURLToPath(import.meta.url));
const script = fs.readFileSync(path.join(here, 'script.md'), 'utf8');
const baseline = fs.readFileSync(path.join(here, 'verification/episode-14-baseline.cpp'), 'utf8');
const repo = '/Users/keremkazan/Documents/Projects/deep-learning-all-the-way-down';
const dump = process.argv.includes('--dump'), quick = process.argv.includes('--quick');
const hash = s => createHash('sha256').update(s).digest('hex');
const problems = [];

// Baseline must equal the checked-in code the recording started from.
const checkedIn = fs.readFileSync(path.join(repo, 'main.cpp'), 'utf8');
if (hash(checkedIn) !== hash(baseline)) console.warn('WARNING: checked-in main.cpp differs from verification/episode-14-baseline.cpp');

// Narration and formatting lint (long-form playbook voice rules).
const narration = script.split('\n').filter(l => l.startsWith('>')).map(l => l.replace(/^>\s?/, '')).join('\n');
const banned = [
  [/—|–/, 'dash character (em or en)'],
  [/ -- /, 'double hyphen used as a dash'],
  [/last episode|last time|previous episode|earlier episode/i, 'reference to a previous episode'],
  [/\bimagine\b|\bpicture this\b/i, 'artificial conversational setup'],
  [/It'?s not [^.]*, it'?s /i, 'canned contrast'],
  [/\bsimply\b|\bjust\b|\bobviously\b/i, 'filler word'],
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

const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'dlatwd-ch15-'));
fs.copyFileSync(path.join(repo, 'mnist_reader.hpp'), path.join(temp, 'mnist_reader.hpp'));
const compiler = process.env.CXX || 'clang++';
const compile = (name, source) => {
  const file = path.join(temp, name + '.cpp'), binary = path.join(temp, name);
  fs.writeFileSync(file, source);
  try { execFileSync(compiler, ['-std=c++23', '-O2', file, '-o', binary], {stdio: 'pipe'}); }
  catch (error) {
    console.error(String(error.stderr).split('\n').filter(l => /error|note: candidate/.test(l)).slice(0, 12).join('\n'));
    throw Error('Compilation failed: ' + name);
  }
  return binary;
};
const runBinary = (binary, args) => new Promise(resolve => execFile(binary, args, {cwd: repo, maxBuffer: 1 << 26, timeout: 900000},
  (error, stdout, stderr) => resolve({code: error ? (error.code ?? 1) : 0, stdout, stderr})));
async function pool(jobs, limit = 8) {
  const out = new Array(jobs.length); let next = 0;
  await Promise.all(Array.from({length: limit}, async () => { for (let i = next++; i < jobs.length; i = next++) out[i] = await jobs[i](); }));
  return out;
}
const lastLoss = o => Number([...o.matchAll(/Epoch \d+ loss: (\S+)/g)].pop()[1]);
const correct = o => Number(o.match(/Test accuracy: \S+% \((\d+)\/2000\)/)[1]);

const pattern = /<!-- edit: ([\w-]+) -->\s*\*\*Before\*\*\s*\x60{3}cpp\n([\s\S]*?)\n\x60{3}\s*\*\*After\*\*\s*\x60{3}cpp\n([\s\S]*?)\n\x60{3}|<!-- run: ([\w-]+) -->/g;
let source = baseline, edits = 0, checked = 0;
const seen = new Set(), snapshots = {}, runOutputs = {};
for (const m of [...script.matchAll(pattern)]) {
  if (m[1]) {
    const [, id, b, a] = m;
    if (seen.has(id)) throw Error('Duplicate edit id ' + id);
    if (b === a) throw Error('Edit changes nothing: ' + id);
    if (source.indexOf(b) < 0) throw Error('Before block not found in the evolving source: ' + id);
    if (source.indexOf(b) !== source.lastIndexOf(b)) throw Error('Before block is ambiguous: ' + id);
    seen.add(id); source = source.replace(b, () => a); ++edits;
  } else {
    const id = m[4], args = '(constants set by the edits above)';
    const binary = compile(id, source);
    const result = await runBinary(binary, []);
    if (result.code !== 0) throw Error(`Run ${id} (${args}) exited with ${result.code}: ${result.stderr.slice(0, 300)}`);
    snapshots[id] = source; runOutputs[id] = result.stdout;
    console.log(`${id}: PASS  (${args})`);
    if (dump) { console.log(result.stdout.split('\n').filter(l => /^layer|^Epoch \d+ loss|^Test accuracy/.test(l)).join('\n')); continue; }
    const rest = script.slice(m.index + m[0].length), next = rest.indexOf('<!-- ');
    const segment = next < 0 ? rest : rest.slice(0, next);
    const block = segment.match(/\x60{3}output\n([\s\S]*?)\n\x60{3}/);
    if (!block) throw Error('Run has no displayed output block: ' + id);
    const actual = result.stdout.split('\n');
    for (const line of block[1].split('\n')) {
      if (!actual.includes(line)) throw Error(`Displayed output line not produced by ${id}: "${line}"`);
      ++checked;
    }
  }
}
if (edits !== [...script.matchAll(/<!-- edit:/g)].length) throw Error('Unparsed edit');
console.log(`${edits} edits replayed; ${checked} displayed output lines matched real output.`);
const nodeDefinition = t => t.match(/struct TensorNode \{[\s\S]*?\n\};/)[0];
if (nodeDefinition(source) !== nodeDefinition(baseline)) throw Error('TensorNode must remain unchanged');
fs.writeFileSync(path.join(here, 'verification/episode-15-final.cpp'), source);
if (quick || dump) process.exit(0);

// Learning-rate table: every cell recomputed from a real run of the final code.
// Bulk runs need many settings, so they use a copy whose four settings constants (and the standardise flag)
// are read from the command line; the displayed runs above used the unmodified edited code.
const hooked = src => {
  const o = [/const std::string OPTIMIZER = "[^"]*";/, 'const std::string OPTIMIZER = g_args[0];'],
    l = [/const double learning_rate = [^;]+;/, 'const double learning_rate = std::stod(g_args[1]);'],
    b = [/const std::size_t BATCH_SIZE = [^;]+;/, 'const std::size_t BATCH_SIZE = std::stoul(g_args[2]);'],
    e = [/const std::size_t EPOCHS = [^;]+;/, 'const std::size_t EPOCHS = std::stoul(g_args[3]);'];
  for (const [re, to] of [o, l, b, e]) { if (!re.test(src)) throw Error('constant not found: ' + re); src = src.replace(re, to); }
  src = src.replace('void train_mnist() {', 'std::vector<std::string> g_args;\n\nvoid train_mnist() {');
  if (!/int main\(\) \{/.test(src)) throw Error('main not found');
  return src.replace('int main() {', 'int main(int argc, char** argv) {\n  for (int i = 1; i < argc; ++i) g_args.push_back(argv[i]);');
};
const finalBinary = compile('final', hooked(source));
const table = script.match(/\x60{3}text\nlearning rate {3}0\.178[\s\S]*?\x60{3}/)[0].split('\n');
const rows = [];
for (let i = 0; i < table.length; ++i) {
  const head = table[i].match(/^learning rate\s+(.*)$/);
  if (head) {
    const rates = head[1].trim().split(/\s+/), data = table[i + 1].trim().split(/\s+/);
    const optimizer = /^plain/.test(data[0]) ? 'sgd' : data[0] === 'momentum' ? 'momentum' : 'adam';
    const values = data.slice(optimizer === 'sgd' ? 2 : 1);
    if (values.length !== rates.length) throw Error('table row width mismatch: ' + table[i + 1]);
    rates.forEach((rate, k) => rows.push({optimizer, rate, shown: values[k]}));
  }
}
if (rows.length !== 21) throw Error('expected 21 table cells, found ' + rows.length);
const tableRuns = await pool(rows.map(r => async () => runBinary(finalBinary, [r.optimizer, r.rate, '250', '5'])));
let tableFailures = 0;
rows.forEach((r, k) => {
  const res = tableRuns[k];
  const actual = res.code !== 0 ? 'stops' : lastLoss(res.stdout).toFixed(3);
  if (res.code !== 0 && !/log requires a positive finite value|terminat/.test(res.stderr)) throw Error(`unexpected failure for ${r.optimizer} ${r.rate}: ${res.stderr.slice(0, 200)}`);
  if (actual !== r.shown) { console.error(`table cell wrong: ${r.optimizer} ${r.rate} shows ${r.shown}, real ${actual}`); ++tableFailures; }
});
if (tableFailures) throw Error(tableFailures + ' table cells do not match real runs');
console.log('Learning-rate table: 21 cells match real runs.');
const cell = (opt, rate) => lastLoss(tableRuns[rows.findIndex(r => r.optimizer === opt && r.rate === rate)].stdout);
const adamUnder = ['0.0032', '0.0056', '0.01', '0.018', '0.032', '0.056', '0.1'].filter(r => cell('adam', r) < 0.08).length;
if (adamUnder !== 4) throw Error('narration says Adam stays under 0.08 for four of seven rates, found ' + adamUnder);

// Seed claims spoken in the narration, replayed with the final code and other starting weights.
const seedLine = 'std::mt19937 random(42);\n\n    Sequence model;\n    model.push_back(hidden_layer<ReLU>(784, 256, random));';
if (source.split(seedLine).length !== 2) throw Error('seed line not unique');
const seeds = [1, 2, 3, 4, 5];
const seedBins = seeds.map(s => compile('seed' + s, hooked(source.replace(seedLine, seedLine.replace('(42)', `(${s})`)))));
const jobs = [];
for (const [k, s] of seeds.entries()) for (const cfg of [['sgd', '1.0', '250', '5'], ['momentum', '0.316', '250', '5'], ['adam', '0.01', '250', '5'], ['sgd', '0.562', '64', '2'], ['momentum', '0.1', '64', '2']])
  jobs.push({s, cfg, run: () => runBinary(seedBins[k], cfg)});
const results = await pool(jobs.map(j => j.run));
const get = (s, ...cfg) => { const i = jobs.findIndex(j => j.s === s && j.cfg.join(' ') === cfg.join(' ')); if (results[i].code !== 0) throw Error('seed run failed ' + cfg); return results[i].stdout; };
const ratios1 = seeds.map(s => lastLoss(get(s, 'momentum', '0.316', '250', '5')) / lastLoss(get(s, 'sgd', '1.0', '250', '5')));
const ratios2 = seeds.map(s => lastLoss(get(s, 'adam', '0.01', '250', '5')) / lastLoss(get(s, 'momentum', '0.316', '250', '5')));
const fewer64 = seeds.every(s => correct(get(s, 'momentum', '0.1', '64', '2')) < correct(get(s, 'sgd', '0.562', '64', '2')));
const loose64 = seeds.map(s => lastLoss(get(s, 'momentum', '0.1', '64', '2')) / lastLoss(get(s, 'sgd', '0.562', '64', '2')));
console.log('momentum/SGD loss ratios (batch 250):', ratios1.map(r => r.toFixed(2)).join(' '));
console.log('Adam/momentum loss ratios (batch 250):', ratios2.map(r => r.toFixed(2)).join(' '));
console.log('momentum/SGD loss ratios (batch 64):', loose64.map(r => r.toFixed(2)).join(' '));
if (!ratios1.every(r => r >= 0.45 && r <= 0.68)) throw Error('narration: momentum about half to two thirds of plain SGD fails');
if (!ratios2.every(r => r >= 0.55 && r <= 0.72)) throw Error('narration: Adam about six to seven tenths of momentum fails');
if (!fewer64) throw Error('narration: momentum gets fewer test images right at batch 64 on every seed fails');
const six = [...seeds.map(s => [correct(get(s, 'momentum', '0.1', '64', '2')), correct(get(s, 'sgd', '0.562', '64', '2'))]), [correct(runOutputs['momentum-batch-64']), correct(runOutputs['sgd-batch-64'])]];
if (!six.every(([m, g]) => m < g)) throw Error('narration: momentum gets fewer test images right on all six starts fails');
console.log('batch 64 correct (momentum, SGD) for seeds 1-5 and the shown run:', JSON.stringify(six));
// Step-number claims: first-step arithmetic, and the stored six-seed experiment (experiments/ch15-adam-bias/runs.json).
const factor = t => (1 - 0.9 ** t) / Math.sqrt(1 - 0.999 ** t);
if (!(Math.abs(factor(1) - 3.16) < 0.01 && factor(10) > 6 && factor(100) > 2.9 && factor(100) < 3.5)) throw Error('narration: uncorrected Adam step factors fail');
const biasRuns = JSON.parse(fs.readFileSync(path.join(here, '../experiments/ch15-adam-bias/runs.json'), 'utf8'));
const pick = (lr, corrected) => biasRuns.filter(r => r.lr === lr && r.corrected === corrected);
const end = r => r.epoch_loss[r.epoch_loss.length - 1];
const withFix = pick('0.01', true), without = pick('0.01', false);
if (withFix.length !== 6 || without.length !== 6 || [...withFix, ...without].some(r => r.code !== 0)) throw Error('bias runs incomplete');
if (!without.every(r => end(r) >= 0.087 && end(r) <= 0.1345)) throw Error('narration: without step number 0.087 to 0.134 fails');
if (!withFix.every(r => end(r) >= 0.0495 && end(r) <= 0.0565)) throw Error('narration: with step number 0.050 to 0.056 fails');
if (!withFix.every((r, k) => end(r) < end(without[k]))) throw Error('narration: worse every time fails');
for (const lr of ['0.056', '0.1']) if (!(pick(lr, false).length === 6 && pick(lr, false).every(r => r.code !== 0) && pick(lr, true).every(r => r.code === 0))) throw Error('narration: uncorrected stops at ' + lr + ' fails');
const avg1 = t => 1 - 0.9 ** t, avg2 = t => 1 - 0.999 ** t;
for (const [t, a1, a2, step, root] of [[1, 0.1, 0.001, 3.16, 0.0316], [2, 0.19, 0.002, 4.25, 0.0447], [3, 0.271, 0.003, 4.95, 0.0547]]) {
  if (Math.abs(avg1(t) - a1) > 5e-4 || Math.abs(avg2(t) - a2) > 5e-4 || Math.abs(avg1(t) / Math.sqrt(avg2(t)) - step) > 0.006 || Math.abs(Math.sqrt(avg2(t)) - root) > 5e-5 || Math.abs(a1 / root - step) > 0.01) throw Error('narration: worked example fails at step ' + t);
  if (Math.abs(avg1(t) / avg1(t) - 1) > 1e-12 || Math.abs(avg2(t) / avg2(t) - 1) > 1e-12) throw Error('division example fails');
}
if (!(0.9 ** 50 < 0.006 && 0.999 ** 3000 > 0.04 && factor(200) > 2.3)) throw Error('narration: fifty steps / thousands / 200 steps fail');
console.log('Step-number claims verified (factors at steps 1, 10, 100: ' + [1, 10, 100].map(t => factor(t).toFixed(2)).join(', ') + ').');
fs.writeFileSync(path.join(here, 'verification-run.json'), JSON.stringify({date: new Date().toISOString(), edits, outputLinesMatched: checked, ratios1, ratios2, loose64, narrationWords: words, baselineSha256: hash(baseline), finalSha256: hash(source)}, null, 2));
console.log('All narration claims verified.');
