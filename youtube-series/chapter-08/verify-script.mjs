// Replay literal Before/After pairs. No hidden source migration.
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {execFileSync} from 'node:child_process';
import {createHash} from 'node:crypto';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '../..');
const script = fs.readFileSync(path.join(here, 'script.md'), 'utf8');
const sourcePath = path.join(root, 'aliases/02-screen-long-form/main.cpp');
const scalarPath = path.join(root, 'aliases/02-screen-long-form/scalar_autograd.cpp');
const workingSource = fs.readFileSync(sourcePath, 'utf8');
const baseRef = process.env.SCRIPT_BASE_REF;
const continueFrom = process.env.SCRIPT_CONTINUE_FROM;
if (baseRef && continueFrom) throw Error('Choose a baseline or a live continuation, not both');
const original = baseRef
  ? execFileSync('git', ['show', `${baseRef}:main.cpp`], {cwd:path.dirname(sourcePath), encoding:'utf8'})
  : workingSource;
if (baseRef) console.log('Replaying main.cpp from checkpoint: '+baseRef);
const scalar = fs.readFileSync(scalarPath, 'utf8');
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'dlatwd-episode08-'));
const compiler = process.env.CXX || 'clang++';
const pattern = /<!-- edit: ([\w-]+) -->\s*\*\*Before\*\*\s*\x60{3}cpp\n([\s\S]*?)\n\x60{3}\s*\*\*After\*\*\s*\x60{3}cpp\n([\s\S]*?)\n\x60{3}|<!-- checkpoint: ([\w-]+) -->/g;
const steps = [...script.matchAll(pattern)].map(m => m[4] ? {checkpoint:m[4]} : {id:m[1],before:m[2],after:m[3]});
if (steps.filter(s=>s.id).length !== [...script.matchAll(/<!-- edit:/g)].length) throw Error('Unparsed edit pair');
const seen = new Set();
for (const s of steps.filter(s=>s.id)) {
  if (seen.has(s.id)) throw Error('Duplicate edit: '+s.id);
  seen.add(s.id);
}
const appendix = steps.findIndex(s=>s.id==='prep-zero');
if (appendix<0) throw Error('Missing preparation');
const start = continueFrom ? steps.findIndex(s=>s.id===continueFrom) : 0;
if (start < 0 || start >= appendix) throw Error('Invalid continuation edit');
const ordered = [...steps.slice(appendix), ...steps.slice(start,appendix)];
if (continueFrom) console.log('Continuing current working source from: '+continueFrom);
let code = original;
const run = (name, text, expected = []) => {
  const file = path.join(tmp, name+'.cpp'), exe = path.join(tmp,name);
  fs.writeFileSync(file,text);
  execFileSync(compiler,['-std=c++23','-O0','-g','-fsanitize=address,undefined',file,'-o',exe],{stdio:'pipe'});
  const output = execFileSync(exe,[],{encoding:'utf8'});
  const lines = output.trim().split('\n').map(l=>l.trim());
  for(const wanted of expected) if(!lines.includes(wanted)) throw Error(name+': missing '+wanted);
  console.log(name+': PASS');
  for(const l of lines.filter(l=>l.startsWith('Gradient regressions passed'))) console.log(l);
};
const success = '  std::cout << "Success!\\n";';
function probe(text) {
  if(!code.includes(success))throw Error('Missing probe anchor');
  return code.replace(success,text+'\n'+success);
}
run('baseline-tensor',original);
run('baseline-scalar',scalar);
for(const step of ordered) {
  if(step.id) {
    const first = code.indexOf(step.before);
    if(first<0 || first!==code.lastIndexOf(step.before)) throw Error('Before is absent or ambiguous: '+step.id);
    if(step.before===step.after) throw Error('No-op edit '+step.id);
    code = code.slice(0,first)+step.after+code.slice(first+step.before.length);
    continue;
  }
  const name=step.checkpoint;
  run(name,code);
  if(name==='E-addition') run('scalar-addition-backward',probe([
    '{',
    'Tensor left({}, {3.5});',
    'Tensor right({}, {0.5});',
    'Tensor output = left + right;',
    'output.backward();',
    'assert(output.at({}) == 4.0);',
    'assert(left.grad()[0] == 1.0);',
    'assert(right.grad()[0] == 1.0);',
    '}'].join('\n')));
  if(name==='A2-gradient-storage') run('gradient-storage-contract',probe([
    '{',
    'const Tensor predictions({2, 1}, {3.5, 0.0});',
    'const Tensor alias = predictions;',
    'assert(&alias.grad() == &predictions.grad());',
    'assert((predictions.grad() == std::vector<double>{0, 0}));',
    '}'].join('\n')));
}
const extra=fs.readFileSync(path.join(here,'gradient-checks.cpp'),'utf8');
const helperStart = code.indexOf('static void backward_elementwise(');
const helperEnd = code.indexOf('[[nodiscard]] Tensor elementwise_binary(', helperStart);
const helper = code.slice(helperStart, helperEnd);
if (helperStart < 0 || helperEnd < 0 || /switch\s*\(|output->operation/.test(helper)) {
  throw Error('Operation dispatch must stay outside backward_elementwise');
}
console.log('No operation dispatch inside coordinate helper: PASS');
run('gradient-regressions',code.replace('int main() {',extra+'\nint main() {\n  gradient_checks();'));
for(const [file,text] of [[sourcePath,workingSource],[scalarPath,scalar]]) {
  if(fs.readFileSync(file,'utf8')!==text)throw Error('Source repository changed');
  console.log(path.basename(file)+' SHA-256: '+createHash('sha256').update(text).digest('hex'));
}
console.log('Literal edit pairs verified: '+ordered.filter(s=>s.id).length);
console.log('Verified artifacts: '+tmp+'\nSource repo untouched.');
