# Does Adam still help at batch 64? Script network (784-256-10 ReLU, raw pixels, cross-entropy), first 10,000 images.
# Settings from argv: <optimizer> <lr> <batch> <epochs> <seed>. Writes runs.json.
import json, os, re, subprocess, concurrent.futures as cf
here = os.path.dirname(os.path.abspath(__file__))
repo = '/Users/keremkazan/Documents/Projects/deep-learning-all-the-way-down'
s = open(os.path.join(here, '../../chapter-15/verification/episode-15-final.cpp')).read()
for pat, to in [(r'const std::string OPTIMIZER = "[^"]*";', 'const std::string OPTIMIZER = g_args[0];'),
                (r'const double learning_rate = [^;]+;', 'const double learning_rate = std::stod(g_args[1]);'),
                (r'const std::size_t BATCH_SIZE = [^;]+;', 'const std::size_t BATCH_SIZE = std::stoul(g_args[2]);'),
                (r'const std::size_t EPOCHS = [^;]+;', 'const std::size_t EPOCHS = std::stoul(g_args[3]);')]:
    assert re.search(pat, s), pat
    s = re.sub(pat, to, s)
s = s.replace('void train_mnist() {', 'std::vector<std::string> g_args;\n\nvoid train_mnist() {', 1)
s = s.replace('int main() {', 'int main(int argc, char** argv) {\n  for (int i = 1; i < argc; ++i) g_args.push_back(argv[i]);', 1)
anchor = 'std::mt19937 random(42);\n\n    Sequence model;\n    model.push_back(hidden_layer<ReLU>'
assert s.count(anchor) == 1
s = s.replace(anchor, anchor.replace('random(42)', 'random(std::stoul(g_args[4]))'))
open(os.path.join(here, 'build/small.cpp'), 'w').write(s)
r = subprocess.run(['clang++', '-std=c++23', '-O2', os.path.join(here, 'build/small.cpp'), '-o', os.path.join(here, 'build/small')], capture_output=True, text=True)
if r.returncode: raise SystemExit(r.stderr[:1500])
def run(job):
    opt, lr, batch, epochs, seed = job
    p = subprocess.run([os.path.join(here, 'build/small'), opt, lr, str(batch), str(epochs), str(seed)], cwd=repo, capture_output=True, text=True, timeout=1800)
    m = re.search(r'Test accuracy: \S+% \((\d+)/2000\)', p.stdout)
    return {'opt': opt, 'lr': lr, 'batch': batch, 'epochs': epochs, 'seed': seed, 'code': p.returncode,
            'epoch_loss': [float(x) for x in re.findall(r'Epoch \d+ loss: (\S+)', p.stdout)], 'correct': int(m.group(1)) if m else None}
if __name__ == '__main__':
    seeds = [42, 1, 2, 3, 4]
    jobs = [('adam', lr, 64, 2, s) for lr in ['0.0018', '0.0032', '0.0056', '0.01', '0.018', '0.032'] for s in seeds]
    jobs += [('sgd', '0.562', 64, 2, s) for s in seeds] + [('momentum', '0.1', 64, 2, s) for s in seeds]
    with cf.ThreadPoolExecutor(8) as ex:
        res = list(ex.map(run, jobs))
    json.dump(res, open(os.path.join(here, 'runs.json'), 'w'), indent=1)
    print('done', len(res))
