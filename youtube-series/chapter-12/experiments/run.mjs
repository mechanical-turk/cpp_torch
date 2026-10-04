import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {execFileSync, spawn} from 'node:child_process';
import {createHash} from 'node:crypto';

const here = path.dirname(fileURLToPath(import.meta.url));
const chapter = path.dirname(here);
const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'mnist-model-comparison-'));
const script = fs.readFileSync(path.join(chapter, 'script.md'), 'utf8');
let source = fs.readFileSync(path.join(chapter, 'verification/episode-11-baseline.cpp'), 'utf8');
const edits = /<!-- edit: ([\w-]+) -->\s*\*\*Before\*\*\s*`{3}cpp\n([\s\S]*?)\n`{3}\s*\*\*After\*\*\s*`{3}cpp\n([\s\S]*?)\n`{3}/g;
for (const [, id, before, after] of script.matchAll(edits)) {
  if (!source.includes(before) || source.indexOf(before) !== source.lastIndexOf(before))
    throw Error('Ambiguous edit: ' + id);
  source = source.replace(before, after);
}
fs.writeFileSync(path.join(temp, 'lesson.cpp'), source);
fs.copyFileSync(path.join(chapter, 'mnist_reader.hpp'), path.join(temp, 'mnist_reader.hpp'));
const compiler = process.env.CXX || 'clang++';
execFileSync(compiler, ['-std=c++23', '-O2', '-I', temp, path.join(here, 'compare.cpp'), '-o', path.join(temp, 'compare')]);
const configs = [
  ['baseline-32-tanh', '32', 'tanh', '0.1', '0'],
  ['shuffle-32-tanh', '32', 'tanh', '0.1', '1'],
  ['wide-128-tanh', '128', 'tanh', '0.1', '1'],
  ['wide-128-tanh-lr003', '128', 'tanh', '0.03', '1'],
  ['wide-128-relu', '128', 'relu', '0.1', '1'],
  ['deep-128-64-relu', '128,64', 'relu', '0.1', '1'],
  ['deep-128-64-tanh', '128,64', 'tanh', '0.1', '1'],
];
const data = path.resolve(chapter, '../../aliases/02-screen-long-form/data');
const report = {
  started: new Date().toISOString(), compiler: execFileSync(compiler, ['--version'], {encoding:'utf8'}).split('\n')[0],
  flags: ['-std=c++23', '-O2'], scriptSha256: createHash('sha256').update(script).digest('hex'),
  split: {training:'official training rows [0,10000)', validation:'official training rows [10000,12000)', test:'never opened'},
  normalization:'pixel / 255', batchSize:64, initialization:'existing Linear uniform +/- 1/sqrt(fan_in), zero bias',
  optimizer:'SGD, no momentum/weight decay/dropout', orderSeed:2026, epochs:15, configs, records:[]
};
function save() {fs.writeFileSync(path.join(here, 'results.json'), JSON.stringify(report,null,2)+'\n');}
async function run(config, seed) {
  console.log('Running ' + config[0] + ', seed ' + seed);
  await new Promise((resolve,reject) => {
    const child = spawn(path.join(temp,'compare'), [...config, String(seed), String(report.epochs)], {cwd:data});
    let pending='', errors='';
    child.stdout.on('data', data => {
      pending += data;
      let split;
      while ((split=pending.indexOf('\n'))>=0) {
        const line=pending.slice(0,split); pending=pending.slice(split+1);
        if(!line)continue;
        const row=JSON.parse(line); report.records.push(row); save();
        console.log(`${row.name} seed=${seed} epoch=${row.epoch}: train=${row.train_accuracy}% val=${row.validation_accuracy}% val_loss=${row.validation_loss}`);
      }
    });
    child.stderr.on('data',data=>errors+=data);
    child.on('error',reject);
    child.on('close',code=>code===0?resolve():reject(Error(errors || 'exit '+code)));
  });
}
save();
for(const config of configs) await run(config,42);
// Repeat baseline and validation-loss winner to expose initialization sensitivity.
const eligible=report.records.filter(r=>r.epoch===15);
const winner=eligible.reduce((a,b)=>a.validation_loss<b.validation_loss?a:b);
report.confirmationSelection='lowest epoch-15 validation cross-entropy, seed 42; repeat alongside baseline';
report.selected=winner.name;save();
await run(configs[0],43);
if(winner.name!==configs[0][0]) await run(configs.find(c=>c[0]===winner.name),43);
report.finished=new Date().toISOString();save();
console.log('Saved '+path.join(here,'results.json'));
