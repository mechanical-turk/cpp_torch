// Generated verification artifacts stay in a temporary directory.
// Never applies the script to the creator's recording main.cpp.
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {execFileSync} from 'node:child_process';
import {createHash} from 'node:crypto';

const here=path.dirname(fileURLToPath(import.meta.url));
const script=fs.readFileSync(path.join(here,'script.md'),'utf8');
const baseline=fs.readFileSync(path.join(here,'verification/episode-11-baseline.cpp'),'utf8');
const recording=path.resolve(here,'../../aliases/02-screen-long-form/main.cpp');
const before=fs.readFileSync(recording,'utf8');
const recordingMatchesBaseline=before.trimEnd()===baseline.trimEnd();
if(!recordingMatchesBaseline && !process.argv.includes('--frozen-baseline'))
  throw Error('Recording has progressed. Use --frozen-baseline to replay the full lesson without changing live code.');
const temp=fs.mkdtempSync(path.join(os.tmpdir(),'dlatwd-ch12-'));
const reader=fs.readFileSync(path.join(here,'mnist_reader.hpp'),'utf8');
fs.writeFileSync(path.join(temp,'mnist_reader.hpp'),reader);
const data=path.resolve(process.argv.slice(2).find(arg=>!arg.startsWith('--'))||path.join(path.dirname(recording),'data'));
const compiler=process.env.CXX||'clang++';
const results=[];
const hash=s=>createHash('sha256').update(s).digest('hex');
function run(name,source,flags=['-O1','-g','-fsanitize=address,undefined']) {
  const file=path.join(temp,name+'.cpp'), binary=path.join(temp,name);
  fs.writeFileSync(file,source);
  execFileSync(compiler,['-std=c++23',...flags,file,'-o',binary],{stdio:'pipe'});
  const start=Date.now();
  const output=execFileSync(binary,[],{cwd:path.dirname(data),encoding:'utf8',timeout:180000});
  results.push({name,flags,elapsedSeconds:(Date.now()-start)/1000,output});
  console.log(name+': PASS');
  if(name==='evaluated-mnist') console.log(output.slice(output.indexOf('digit score probability')));
  return output;
}
run('baseline',baseline);
const pattern=/<!-- edit: ([\w-]+) -->\s*\*\*Before\*\*\s*\x60{3}cpp\n([\s\S]*?)\n\x60{3}\s*\*\*After\*\*\s*\x60{3}cpp\n([\s\S]*?)\n\x60{3}|<!-- checkpoint: ([\w-]+) -->/g;
let source=baseline, count=0;
const seen=new Set();
for(const m of script.matchAll(pattern)) {
  if(m[1]) {
    const [,id,b,a]=m;
    if(seen.has(id)||source.indexOf(b)<0||source.indexOf(b)!==source.lastIndexOf(b))
      throw Error('Ambiguous/missing edit '+id);
    seen.add(id);
    source=source.replace(b,a); ++count;
  } else run(m[4],source,m[4].includes('mnist')?['-O2']:undefined);
}
if(count!==[...script.matchAll(/<!-- edit:/g)].length)throw Error('Unparsed edit');
const nodeDefinition=text=>text.match(/struct TensorNode \{[\s\S]*?\n\};/)[0];
if(nodeDefinition(source)!==nodeDefinition(baseline))
  throw Error('TensorNode must remain unchanged for primitive composition');
const file=path.join(temp,'final.cpp');
fs.writeFileSync(file,source);
const imageFixture=Buffer.alloc(16+3*784,255);
[2051,3,28,28].forEach((v,i)=>imageFixture.writeUInt32BE(v,i*4));
const labelFixture=Buffer.from([0,0,8,1,0,0,0,3,2,7,1]);
fs.writeFileSync(path.join(temp,'fixture-images'),imageFixture);
fs.writeFileSync(path.join(temp,'fixture-labels'),labelFixture);
const wrongMagic=Buffer.from(imageFixture);wrongMagic.writeUInt32BE(2050,0);
fs.writeFileSync(path.join(temp,'bad-magic'),wrongMagic);
const wrongCount=Buffer.from(imageFixture);wrongCount.writeUInt32BE(4,4);
fs.writeFileSync(path.join(temp,'bad-count'),wrongCount);
fs.writeFileSync(path.join(temp,'truncated'),imageFixture.subarray(0,100));
const wrongLabel=Buffer.from(labelFixture);wrongLabel[8]=10;
fs.writeFileSync(path.join(temp,'bad-label'),wrongLabel);
const harness=`
#define main recorded_main
#include "${file}"
#undef main
#include <sstream>

void require(bool yes, const char* message) {
  if (!yes) throw std::runtime_error(message);
}
void close(double a, double b, double tolerance=1e-5) {
  require(std::isfinite(a) && std::abs(a-b)<tolerance, "numeric mismatch");
}
template<class F> void rejects(F f) {
  bool caught=false;
  try {f();} catch(const std::exception&) {caught=true;}
  require(caught,"expected rejection");
}
Tensor test_loss(const Tensor& scores, const std::vector<std::size_t>& labels) {
  return cross_entropy_loss(softmax(scores),labels);
}
int main() {
  std::size_t checked=0;
  Tensor logits({2,3},{1.0,-2.0,0.5,0.1,0.7,-0.9});
  const std::vector<std::size_t> labels{0,2};
  Tensor loss=test_loss(logits,labels);
  loss.backward();
  for(std::size_t i=0;i<logits.numel();++i) {
    double original=logits.data()[i];
    logits.data()[i]=original+1e-5;
    double plus=test_loss(logits,labels).at({});
    logits.data()[i]=original-1e-5;
    double minus=test_loss(logits,labels).at({});
    logits.data()[i]=original;
    close(logits.grad()[i],(plus-minus)/2e-5); ++checked;
  }
  const auto first=logits.grad();
  // One-hot targets belong to the graph, not to the caller's label vector.
  Tensor retained_scores({2,3},{1.0,-2.0,0.5,0.1,0.7,-0.9});
  Tensor retained_loss=[&]() {
    std::vector<std::size_t> temporary_labels{0,2};
    Tensor result=test_loss(retained_scores,temporary_labels);
    temporary_labels.assign({1,1});
    return result;
  }();
  for(double gradient:retained_scores.grad())close(gradient,0);
  retained_loss.backward();
  for(std::size_t i=0;i<retained_scores.numel();++i)
    close(retained_scores.grad()[i],first[i]);

  Tensor other_scores({2,3},{1.0,-2.0,0.5,0.1,0.7,-0.9});
  Tensor other_loss=test_loss(other_scores,{1,0});other_loss.backward();
  Tensor shared_scores({2,3},{1.0,-2.0,0.5,0.1,0.7,-0.9});
  Tensor combined=test_loss(shared_scores,{0,2})+test_loss(shared_scores,{1,0});
  combined.backward();
  for(std::size_t i=0;i<shared_scores.numel();++i)
    close(shared_scores.grad()[i],first[i]+other_scores.grad()[i]);

  loss.backward();
  for(std::size_t i=0;i<logits.numel();++i)close(logits.grad()[i],2*first[i]);
  logits.zero_grad();
  Tensor scaled=loss*Tensor({}, {3.0});
  scaled.backward();
  for(std::size_t i=0;i<logits.numel();++i)close(logits.grad()[i],3*first[i]);
  close(test_loss(Tensor({1,3},{0,0,0}),{2}).at({}),std::log(3.0));
  // Explicit exp -> normalize -> log is intentionally not the stable fused path.
  rejects([]{test_loss(Tensor({1,2},{1000,-1000}),{1});});
  rejects([]{Tensor({1},{0}).log();});
  rejects([]{Tensor({1},{-1}).log();});
  for(int operation=0;operation<4;++operation) {
    Tensor v({2,3},{0.2,0.7,1.1,0.3,1.3,0.9});
    const Tensor factors({2,3},{1,-2,3,4,0.5,-0.8});
    auto objective=[&]() {
      if(operation==0)return (v.exp()*factors).sum();
      if(operation==1)return (v.log()*factors).sum();
      if(operation==2)return (softmax(v)*factors).sum();
      return (v.sum_columns()*Tensor({2,1},{2,-3})).sum();
    };
    Tensor result=objective();result.backward();
    for(std::size_t i=0;i<v.numel();++i) {
      const double original=v.data()[i];
      v.data()[i]=original+1e-5;const double plus=objective().at({});
      v.data()[i]=original-1e-5;const double minus=objective().at({});
      v.data()[i]=original;
      close(v.grad()[i],(plus-minus)/2e-5);++checked;
    }
  }
  const Tensor totals=Tensor({2,3},{1,2,3,4,5,6}).sum_columns();
  require(totals.shape()==std::vector<std::size_t>({2,1}),"column reduction shape");
  close(totals.at({0,0}),6);close(totals.at({1,0}),15);
  const Tensor normalized=softmax(logits);
  const Tensor probability_totals=normalized.sum_columns();
  close(probability_totals.at({0,0}),1);close(probability_totals.at({1,0}),1);
  for(double value:normalized.data())require(value>0 && value<1,"probability range");
  close(test_loss(Tensor({1,3},{11,8,10.5}),{0}).at({}),
        test_loss(Tensor({1,3},{1,-2,0.5}),{0}).at({}));
  rejects([]{test_loss(Tensor({0,3},{}),{});});
  rejects([]{test_loss(Tensor({1,0},{}),{0});});
  rejects([]{test_loss(Tensor({1},{0}),{0});});
  rejects([]{test_loss(Tensor({1,2},{0,0}),{2});});
  rejects([]{test_loss(Tensor({1,2},{0,0}),{});});
  rejects([]{test_loss(Tensor({1,2},{0,std::numeric_limits<double>::infinity()}),{0});});

  std::mt19937 rng(42);
  MLP model(2,4,3,rng);
  auto parameters=model.parameters();
  const Tensor x({2,2},{0.1,0.7,0.2,-0.5});
  Tensor model_loss=test_loss(model.forward(x),{1,2});
  model_loss.backward();
  for(auto& p:parameters)for(std::size_t i=0;i<p.numel();++i) {
    double original=p.data()[i];
    p.data()[i]=original+1e-5;
    double plus=test_loss(model.forward(x),{1,2}).at({});
    p.data()[i]=original-1e-5;
    double minus=test_loss(model.forward(x),{1,2}).at({});
    p.data()[i]=original;
    close(p.grad()[i],(plus-minus)/2e-5); ++checked;
  }

  MnistReader fixture("${temp}/fixture-images", "${temp}/fixture-labels");
  auto b=fixture.read_batch(2);
  require(b.pixels.size()==2*784,"batch pixel count");
  require(b.labels==std::vector<std::size_t>({2,7}),"labels");
  close(b.pixels[0],1.0);
  b=fixture.read_batch(2);require(b.labels.size()==1,"tail batch");
  b=fixture.read_batch(2);require(b.labels.empty(),"EOF");
  rejects([&]{fixture.read_batch(0);});
  rejects([]{MnistReader bad("missing-images","missing-labels");});
  rejects([]{MnistReader bad("${temp}/bad-magic","${temp}/fixture-labels");});
  rejects([]{MnistReader bad("${temp}/bad-count","${temp}/fixture-labels");});
  rejects([]{MnistReader bad("${temp}/truncated","${temp}/fixture-labels");bad.read_batch(3);});
  rejects([]{MnistReader bad("${temp}/fixture-images","${temp}/bad-label");bad.read_batch(3);});
  Tensor scores({2,10},std::vector<double>(20,0.0));
  scores.at({0,3})=5; scores.at({1,9})=2;
  require(count_correct(scores,{3,9})==2,"argmax");
  require(count_correct(scores,{0,9})==1,"accuracy");
  MnistReader actual("data/train-images-idx3-ubyte","data/train-labels-idx1-ubyte");std::size_t rows=0;
  while(true) {auto batch=actual.read_batch(64);if(batch.labels.empty())break;rows+=batch.labels.size();}
  require(rows==60000,"original training count");
  MnistReader heldout("data/t10k-images-idx3-ubyte","data/t10k-labels-idx1-ubyte");rows=0;
  while(true) {auto batch=heldout.read_batch(64);if(batch.labels.empty())break;rows+=batch.labels.size();}
  require(rows==10000,"original test count");
  std::cout<<checked<<" finite-difference checks; stability, accumulation, batches, data and accuracy: PASS\\n";
}
`;
run('loss-and-batch-checks',harness);
if(fs.readFileSync(recording,'utf8')!==before)throw Error('Recording source changed');
const final=results.find(r=>r.name==='evaluated-mnist').output;
const accuracy=final.match(/Test accuracy: ([\d.]+)% \((\d+)\/(\d+)\)/);
if(!accuracy)throw Error('Missing held-out result');
const manifest={files:['train-images-idx3-ubyte','train-labels-idx1-ubyte','t10k-images-idx3-ubyte','t10k-labels-idx1-ubyte'].map(name=>{
  const bytes=fs.readFileSync(path.join(data,name));return {name,bytes:bytes.length,sha256:hash(bytes)};
})};
const report={date:new Date().toISOString(),compiler:execFileSync(compiler,['--version'],{encoding:'utf8'}).split('\n')[0],
  scriptSha256:hash(script),readerSha256:hash(reader),baselineSha256:hash(baseline),recordingSha256:hash(before),edits:count,
  recordingUnchanged:true,recordingMatchesBaseline,temporary:temp,datasetDirectory:data,
  datasetFiles:manifest.files.map(({selectedIndices,...rest})=>rest),accuracy:accuracy[0],results};
fs.writeFileSync(path.join(here,'verification-run.json'),JSON.stringify(report,null,2)+'\n');
console.log('Complete: '+count+' edits; recording source unchanged.');
