// Replays every literal Chapter 10 edit without changing the recording source.
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {execFileSync} from 'node:child_process';
import {createHash} from 'node:crypto';

const here = path.dirname(fileURLToPath(import.meta.url));
const repo = path.resolve(here, '../../aliases/02-screen-long-form');
const sourcePath = path.join(repo, 'main.cpp');
const source = fs.readFileSync(sourcePath, 'utf8');
const script = fs.readFileSync(path.join(here, 'script.md'), 'utf8');
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'dlatwd-episode10-'));
const compiler = process.env.CXX || 'clang++';
const expectedSourceSha256 =
  '9884bdafa86a39e330fa8581879001fcd226a25396f4112e919f8576d995a125';
const sourceSha256 = createHash('sha256').update(source).digest('hex');

if (sourceSha256 !== expectedSourceSha256)
  throw Error(`Starting source changed: ${sourceSha256}`);

const pattern = /<!-- edit: ([\w-]+) -->\s*\*\*Before\*\*\s*\x60{3}cpp\n([\s\S]*?)\n\x60{3}\s*\*\*After\*\*\s*\x60{3}cpp\n([\s\S]*?)\n\x60{3}|<!-- checkpoint: ([\w-]+) -->/g;
const steps = [...script.matchAll(pattern)];
const editCount = [...script.matchAll(/<!-- edit:/g)].length;

if (steps.filter(match => match[1]).length !== editCount)
  throw Error('One or more edit blocks could not be parsed');

const results = [];
const seen = new Set();

function compileAndRun(name, code, extraFlags = []) {
  const file = path.join(tmp, `${name}.cpp`);
  const executable = path.join(tmp, name);
  fs.writeFileSync(file, code);
  execFileSync(compiler, [
    '-std=c++23', '-O1', '-g', '-fsanitize=address,undefined',
    ...extraFlags, file, '-o', executable
  ], {stdio: 'pipe'});
  const output = execFileSync(executable, [], {encoding: 'utf8'});
  results.push({name, output});
  console.log(`${name}: PASS`);
  return output;
}

compileAndRun('baseline', source);
let code = source;

for (const match of steps) {
  const [, id, before, after, checkpoint] = match;
  if (id) {
    if (seen.has(id)) throw Error(`Duplicate edit: ${id}`);
    seen.add(id);
    const index = code.indexOf(before);
    if (index < 0 || index !== code.lastIndexOf(before))
      throw Error(`Missing or ambiguous Before block: ${id}`);
    code = code.slice(0, index) + after + code.slice(index + before.length);
    continue;
  }

  compileAndRun(checkpoint, code);
}

const output = results.at(-1)?.output ?? '';
for (const expected of [
  'x relu sigmoid tanh',
  '-2 0 0.119203 -0.964028',
  'Weight: 2',
  'Bias: 1'
]) {
  if (!output.includes(expected))
    throw Error(`Final output is missing: ${expected}`);
}

const finalPath = path.join(tmp, 'episode10-final.cpp');
fs.writeFileSync(finalPath, code);
const escapedPath = finalPath.replaceAll('\\', '\\\\').replaceAll('"', '\\"');
const checks = `
#define main episode10_program_main
#include "${escapedPath}"
#undef main

#include <cmath>
#include <iostream>

void expect_close(double actual, double expected, double tolerance = 1e-5) {
  if (std::abs(actual - expected) > tolerance)
    throw std::runtime_error("activation gradient check failed");
}

double gradient_of(const Tensor& input, const auto& activation) {
  Tensor value = input;
  Tensor output = activation(value);
  Tensor loss = output.sum();
  loss.backward();
  return value.grad()[0];
}

int main() {
  expect_close(gradient_of(Tensor({}, {-1.0}), [](const Tensor& x) { return x.relu(); }), 0.0);
  expect_close(gradient_of(Tensor({}, {0.0}), [](const Tensor& x) { return x.relu(); }), 0.0);
  expect_close(gradient_of(Tensor({}, {1.0}), [](const Tensor& x) { return x.relu(); }), 1.0);
  expect_close(gradient_of(Tensor({}, {0.0}), [](const Tensor& x) { return x.sigmoid(); }), 0.25);
  expect_close(gradient_of(Tensor({}, {0.0}), [](const Tensor& x) { return x.tanh(); }), 1.0);

  const double epsilon = 1e-6;
  for (double x : {-2.0, -0.5, 0.5, 2.0}) {
    const double sigmoid_numeric =
      ((1.0 / (1.0 + std::exp(-(x + epsilon)))) -
       (1.0 / (1.0 + std::exp(-(x - epsilon))))) / (2.0 * epsilon);
    expect_close(
      gradient_of(Tensor({}, {x}), [](const Tensor& value) { return value.sigmoid(); }),
      sigmoid_numeric
    );

    const double tanh_numeric =
      (std::tanh(x + epsilon) - std::tanh(x - epsilon)) / (2.0 * epsilon);
    expect_close(
      gradient_of(Tensor({}, {x}), [](const Tensor& value) { return value.tanh(); }),
      tanh_numeric
    );
  }

  std::cout << "activation gradient checks: PASS\\n";
}
`;

compileAndRun('activation-gradient-checks', checks);

if (fs.readFileSync(sourcePath, 'utf8') !== source)
  throw Error('The recording source changed during verification');

const report = {
  startingSourceSha256: sourceSha256,
  scriptSha256: createHash('sha256').update(script).digest('hex'),
  replaySha256: createHash('sha256').update(code).digest('hex'),
  edits: seen.size,
  checkpoints: results.map(result => ({name: result.name, output: result.output}))
};

fs.writeFileSync(
  path.join(here, 'verification-run.json'),
  `${JSON.stringify(report, null, 2)}\n`
);

console.log(`Literal edits: ${seen.size}; recording source unchanged.`);
console.log(`Artifacts: ${tmp}`);
