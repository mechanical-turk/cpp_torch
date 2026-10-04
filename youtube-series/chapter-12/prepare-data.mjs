// Internal preparation helper. Viewers only need scripts/download-mnist.sh.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {execFileSync} from 'node:child_process';

const here = path.dirname(fileURLToPath(import.meta.url));
const repo = path.resolve(here, '../../aliases/02-screen-long-form');
execFileSync('bash', [path.join(repo, 'scripts/download-mnist.sh')], {stdio: 'inherit'});
const data = path.join(repo, 'data');
const images = fs.readFileSync(path.join(data, 'train-images-idx3-ubyte'));
fs.writeFileSync(path.join(data, 'example.pgm'), Buffer.concat([
  Buffer.from('P5\n28 28\n255\n'), images.subarray(16, 16 + 784)
]));
console.log('First training image preview: ' + path.join(data, 'example.pgm'));
