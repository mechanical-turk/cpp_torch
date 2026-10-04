import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const here=path.dirname(fileURLToPath(import.meta.url));
const r=JSON.parse(fs.readFileSync(path.join(here,'results.json'),'utf8'));
if(!r.finished)throw Error('Comparison still running; final report not ready');
const f=(n,d=2)=>Number(n).toFixed(d);
const lines=[
  '# MNIST MLP comparison: measured results', '',
  'Seven configurations, 15 epochs, 10,000 training images and 2,000 validation images.',
  'Validation records come from the original training split. No official test data was used for selection.', '',
  '## Main comparison', '',
  'Initialization seed 42. All reported train/validation metrics use the final epoch-15 weights.', '',
  '| Hidden layers | Activation | LR | Shuffle | Parameters | Train accuracy | Validation accuracy | Gap (pp) | Train loss | Validation loss | Seconds |',
  '| --- | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |'
];
for(const row of r.records.filter(x=>x.seed===42 && x.epoch===15)){
  const c=r.configs.find(c=>c[0]===row.name);
  lines.push(`| ${c[1].replaceAll(',', ' + ')} | ${c[2]} | ${c[3]} | ${c[4]==='1'?'Yes':'No'} | ${row.parameters.toLocaleString('en-US')} | ${f(row.train_accuracy)}% | ${f(row.validation_accuracy)}% | ${f(row.train_accuracy-row.validation_accuracy)} | ${f(row.train_loss,4)} | ${f(row.validation_loss,4)} | ${f(row.elapsed_seconds,1)} |`);
}
lines.push('', 'The gap is train accuracy minus validation accuracy. Timing includes evaluation and is not a clean performance benchmark.', '',
  '## Initialization sensitivity', '',
  `Selected by lowest epoch-15 validation loss in the initial sweep: **${r.selected}**.`,
  'Only the baseline and selected model were repeated with seed 43.', '',
  '| Model | Seed | Train accuracy | Validation accuracy | Gap (pp) | Validation loss |',
  '| --- | ---: | ---: | ---: | ---: | ---: |');
for(const row of r.records.filter(x=>x.epoch===15 && [r.configs[0][0],r.selected].includes(x.name)))
  lines.push(`| ${row.name} | ${row.seed} | ${f(row.train_accuracy)}% | ${f(row.validation_accuracy)}% | ${f(row.train_accuracy-row.validation_accuracy)} | ${f(row.validation_loss,4)} |`);
lines.push('', '## Learning checkpoints', '',
  'Training loss is evaluated after the epoch at fixed weights, not averaged while the weights change.', '',
  '| Model | Seed | Epoch | Train loss | Validation loss | Train accuracy | Validation accuracy |',
  '| --- | ---: | ---: | ---: | ---: | ---: | ---: |');
for(const row of r.records)
  lines.push(`| ${row.name} | ${row.seed} | ${row.epoch} | ${f(row.train_loss,4)} | ${f(row.validation_loss,4)} | ${f(row.train_accuracy)}% | ${f(row.validation_accuracy)}% |`);
lines.push('', '## Boundaries', '',
  '- These are validation results, not the earlier 88.2% test-subset result.',
  '- More training data, other initializers, Adam, momentum, regularization and augmentation were not compared.',
  '- One split and limited seed repeats do not establish a universal architecture ranking.',
  '- An accuracy gap alone does not demonstrate deterioration from overfitting. Inspect whether validation loss rises as training loss falls.',
  '- All experiments use the actual C++ Tensor/autograd engine with normal -O2.',
  '', '[Protocol and source context](README.md) · [Raw measurements](results.json)', '');
fs.writeFileSync(path.join(here,'results.md'),lines.join('\n'));
console.log(lines.slice(0,26).join('\n'));
