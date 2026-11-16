# Builds the Chapter 15 final code (SGD, momentum, Adam with step number) around the Chapter 14 residual
# network: hidden_layer(784,32) + 15 x Residual(hidden_layer(32,32)) + Linear(32,10), Tanh, series init.
# Settings come from argv: <optimizer> <learning rate> <batch> <epochs> <seed>.
import os, re, subprocess, sys
here = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(here, '../../chapter-15/verification/episode-15-final.cpp')).read()
small = """    model.push_back(hidden_layer<ReLU>(784, 256, random));
    model.push_back(Linear(256, 10, random));"""
residual = """    model.push_back(hidden_layer(784, 32, random));
    for (int i = 0; i < 15; ++i) {
      model.push_back(Residual(hidden_layer(32, 32, random)));
    }
    model.push_back(Linear(32, 10, random));"""
assert src.count(small) == 1
s = src.replace(small, residual)
for pat, to in [(r'const std::string OPTIMIZER = "[^"]*";', 'const std::string OPTIMIZER = g_args[0];'),
                (r'const double learning_rate = [^;]+;', 'const double learning_rate = std::stod(g_args[1]);'),
                (r'const std::size_t BATCH_SIZE = [^;]+;', 'const std::size_t BATCH_SIZE = std::stoul(g_args[2]);'),
                (r'const std::size_t EPOCHS = [^;]+;', 'const std::size_t EPOCHS = std::stoul(g_args[3]);')]:
    assert re.search(pat, s), pat
    s = re.sub(pat, to, s)
s = s.replace('void train_mnist() {', 'std::vector<std::string> g_args;\n\nvoid train_mnist() {', 1)
s = s.replace('int main() {', 'int main(int argc, char** argv) {\n  for (int i = 1; i < argc; ++i) g_args.push_back(argv[i]);', 1)
anchor = 'std::mt19937 random(42);\n\n    Sequence model;\n    model.push_back(hidden_layer(784, 32, random));'
assert s.count(anchor) == 1
s = s.replace(anchor, anchor.replace('random(42)', 'random(std::stoul(g_args[4]))'))
open(os.path.join(here, 'build/residual.cpp'), 'w').write(s)
r = subprocess.run(['clang++', '-std=c++23', '-O2', os.path.join(here, 'build/residual.cpp'), '-o', os.path.join(here, 'build/residual')], capture_output=True, text=True)
if r.returncode: sys.exit(r.stderr[:2000])
print('built')
