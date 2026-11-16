# Adam with and without the bias-correction step number, using the Chapter 15 script's final code.
# Usage: python3 run.py   (writes runs.json; compiles into ./build)
import json, os, re, subprocess, itertools, concurrent.futures as cf
here = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(here, '../../chapter-15/verification/episode-15-final.cpp')).read()
repo = '/Users/keremkazan/Documents/Projects/deep-learning-all-the-way-down'
os.makedirs(os.path.join(here, 'build'), exist_ok=True)
import shutil
shutil.copy(os.path.join(repo, 'mnist_reader.hpp'), os.path.join(here, 'build', 'mnist_reader.hpp'))

def variant(seed, corrected):
    s = src
    for pat, to in [(r'const std::string OPTIMIZER = "[^"]*";', 'const std::string OPTIMIZER = "adam";'),
                    (r'const double learning_rate = [^;]+;', 'const double learning_rate = std::stod(g_args[0]);'),
                    (r'const std::size_t BATCH_SIZE = [^;]+;', 'const std::size_t BATCH_SIZE = std::stoul(g_args[1]);'),
                    (r'const std::size_t EPOCHS = [^;]+;', 'const std::size_t EPOCHS = std::stoul(g_args[2]);'),
                    ]:
        assert re.search(pat, s), pat
        s = re.sub(pat, to, s)
    s = s.replace('void train_mnist() {', 'std::vector<std::string> g_args;\n\nvoid train_mnist() {', 1)
    s = s.replace('int main() {', 'int main(int argc, char** argv) {\n  for (int i = 1; i < argc; ++i) g_args.push_back(argv[i]);', 1)
    s = s.replace('std::mt19937 random(42);\n\n    Sequence model;\n    model.push_back(hidden_layer<ReLU>', f'std::mt19937 random({seed});\n\n    Sequence model;\n    model.push_back(hidden_layer<ReLU>', 1)
    assert f'random({seed})' in s
    if not corrected:
        a = 'const double correction1 = 1.0 - std::pow(beta1, static_cast<double>(step_count));'
        b = 'const double correction2 = 1.0 - std::pow(beta2, static_cast<double>(step_count));'
        assert a in s and b in s
        s = s.replace(a, 'const double correction1 = 1.0;').replace(b, 'const double correction2 = 1.0;')
    # per-step loss for the first twenty steps of epoch 1
    hook = 'Tensor loss = cross_entropy_loss(probabilities, batch.labels);\n        loss.backward();\n'
    assert s.count(hook) == 1
    s = s.replace(hook, hook + '        if (epoch == 0 && seen < 20 * BATCH_SIZE) { std::cerr << "step " << seen / BATCH_SIZE + 1 << " loss " << loss.at({}) << "\\n"; }\n', 1)
    name = f'{"c" if corrected else "u"}{seed}'
    file = os.path.join(here, 'build', name + '.cpp')
    open(file, 'w').write(s)
    r = subprocess.run(['clang++', '-std=c++23', '-O2', file, '-o', file[:-4]], capture_output=True, text=True)
    if r.returncode: raise SystemExit(r.stderr[:1500])
    return file[:-4]

def run(binary, args):
    r = subprocess.run([binary] + args, cwd=repo, capture_output=True, text=True, timeout=1800)
    out = {'code': r.returncode}
    out['epoch_loss'] = [float(x) for x in re.findall(r'Epoch \d+ loss: (\S+)', r.stdout)]
    m = re.search(r'Test accuracy: \S+% \((\d+)/2000\)', r.stdout)
    out['correct'] = int(m.group(1)) if m else None
    out['step_loss'] = [float(x) for x in re.findall(r'step \d+ loss (\S+)', r.stderr)]
    return out

if __name__ == '__main__':
    seeds = [1, 2, 3, 4, 5, 42]
    bins = {(s, c): variant(s, c) for s in seeds for c in (True, False)}
    rates = ['0.01', '0.056', '0.1']
    jobs = [(s, c, lr) for s in seeds for c in (True, False) for lr in rates]
    with cf.ThreadPoolExecutor(6) as ex:
        res = list(ex.map(lambda j: run(bins[(j[0], j[1])], [j[2], '250', '5']), jobs))
    json.dump([{'seed': j[0], 'corrected': j[1], 'lr': j[2], **r} for j, r in zip(jobs, res)], open(os.path.join(here, 'runs.json'), 'w'), indent=1)
    print('done', len(jobs))
