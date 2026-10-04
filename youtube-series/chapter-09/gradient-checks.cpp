// Off-camera regression coverage, inserted mechanically before replay main().
#include <cmath>
#include <functional>

void gradient_checks() {
  using Shape = std::vector<std::size_t>;
  using Data = std::vector<double>;
  const auto near = [](double actual, double expected) {
    assert(std::isfinite(actual));
    assert(std::abs(actual - expected) < 1e-5 * (1.0 + std::abs(expected)));
  };
  using Binary = std::function<Tensor(const Tensor&, const Tensor&)>;
  const std::vector<Binary> arithmetic{
    [](const Tensor& a, const Tensor& b) { return a + b; },
    [](const Tensor& a, const Tensor& b) { return a - b; },
    [](const Tensor& a, const Tensor& b) { return a * b; },
    [](const Tensor& a, const Tensor& b) { return a / b; }
  };
  struct Case { Shape as, bs; Data av, bv; };
  const std::vector<Case> broadcasts{
    {{2,3}, {3}, {1,2,3,4,5,6}, {2,3,4}},
    {{2,1}, {1,3}, {2,5}, {3,4,7}},
    {{}, {2,2}, {2}, {1,3,5,7}},
    {{2,2}, {}, {1,3,5,7}, {2}},
    {{2,2}, {2,2}, {1,3,5,7}, {2,4,6,8}},
    {{2,1,2}, {1,3,1}, {1,2,3,4}, {2,3,4}}
  };
  std::size_t comparisons = 0;
  const auto check = [&](const Case& c, const Binary& operation) {
    Tensor a(c.as,c.av), b(c.bs,c.bv);
    // Squared output produces nonuniform upstream gradients for matmul too.
    const Tensor output = operation(a,b);
    Tensor loss = (output * output).mean();
    loss.backward();
    for(int side=0; side<2; ++side) {
      const Data gradients = side==0 ? a.grad() : b.grad();
      const Data& values = side==0 ? c.av : c.bv;
      for(std::size_t i=0; i<values.size(); ++i) {
        const auto evaluate = [&](double delta) {
          Data av=c.av, bv=c.bv;
          (side==0 ? av : bv)[i] += delta;
          const Tensor out = operation(Tensor(c.as,av),Tensor(c.bs,bv));
          return (out*out).mean().at({});
        };
        near(gradients[i],(evaluate(1e-5)-evaluate(-1e-5))/2e-5);
        ++comparisons;
      }
    }
  };
  for(const auto& op:arithmetic) for(const auto& c:broadcasts) check(c,op);
  const Binary matmul = [](const Tensor& a,const Tensor& b){return a.matmul(b);};
  for(const auto& c:std::vector<Case>{
    {{2,3},{3,2},{1,-2,3,4,0.5,-1},{2,-1,3,4,-2,0.5}},
    {{3,2},{2,1},{1,2,3,4,5,6},{2,-3}},
    {{1,3},{3,4},{1,-2,3},{1,2,3,4,2,1,-1,3,4,-2,1,2}}
  }) check(c,matmul);

  Tensor shared({2,2},{1,2,3,4});
  Tensor square = shared.matmul(shared).sum();
  square.backward();
  const Data shared_gradient = shared.grad();
  for(std::size_t i=0;i<4;++i) {
    const auto evaluate = [&](double delta) {
      Data data{1,2,3,4}; data[i]+=delta;
      const Tensor value({2,2},data);
      return value.matmul(value).sum().at({});
    };
    near(shared_gradient[i],(evaluate(1e-5)-evaluate(-1e-5))/2e-5);
    ++comparisons;
  }
  square.backward();
  for (std::size_t i = 0; i < shared_gradient.size(); ++i)
    near(shared.grad()[i], 2 * shared_gradient[i]);

  Tensor x({2},{2,3});
  Tensor loss = [&] { const Tensor local=x*x; return (local+local).sum(); }();
  loss.backward();
  assert((x.grad()==Data{8,12}));
  Tensor alias=x;
  assert(&alias.grad()==&x.grad());
  alias.zero_grad();
  assert((x.grad()==Data{0,0}));
  const Tensor features({2},{4,5});
  Tensor dot=x.dot(features); dot.backward();
  assert((x.grad()==Data{4,5}));
  assert((features.grad()==Data{2,3}));
  Tensor empty({0,3},{});
  Tensor empty_sum=empty.sum(); empty_sum.backward();
  assert(empty.grad().empty());
  Tensor zero_left({2,0},{}), zero_right({0,3},{});
  Tensor zero_product=zero_left.matmul(zero_right).sum();
  zero_product.backward();
  assert(zero_product.at({})==0);
  assert(zero_left.grad().empty() && zero_right.grad().empty());
  bool rejected=false;
  try { x.backward(); } catch(const std::invalid_argument&) {rejected=true;}
  assert(rejected);
  for(double zero:{0.0,-0.0}) {
    rejected=false;
    try { static_cast<void>(x/Tensor({}, {zero})); }
    catch(const std::domain_error&) {rejected=true;}
    assert(rejected);
  }

  const Tensor inputs({4,2},{-1,-1,-1,1,1,-1,1,1});
  const Tensor targets({4,1},{2,-4,6,0});
  Tensor weights({2,1},{0,0}), bias({}, {0});
  double previous=15.0;
  for(int step=0;step<100;++step) {
    weights.zero_grad();
    bias.zero_grad();
    Tensor objective=mse_loss(inputs.matmul(weights)+bias,targets);
    const double current=objective.at({});
    assert(current<previous);
    previous=current;
    objective.backward();
    if(step==0) {
      near(current,14);
      near(weights.grad()[0],-4); near(weights.grad()[1],6); near(bias.grad()[0],-2);
    }
    for(std::size_t i=0;i<2;++i) weights.at({i,0})-=0.1*weights.grad()[i];
    bias.at({})-=0.1*bias.grad()[0];
  }
  near(weights.at({0,0}),2); near(weights.at({1,0}),-3); near(bias.at({}),1);
  assert(mse_loss(inputs.matmul(weights)+bias,targets).at({})<1e-15);

  // Known baseline defect: inspect the zero/singleton shape mapping without
  // executing the unsafe elementwise loop. Expose the private shape helper only
  // in a separate test if investigating it; do not manufacture a passing claim here.
  std::cout << "Finite-difference comparisons: " << comparisons << '\n';
  std::cout << "Shared paths, leaf accumulation, explicit zero-grad, lifetime, empty reductions, "
               "zero-inner matmul, validation and 100 training steps: PASS\n";
}
