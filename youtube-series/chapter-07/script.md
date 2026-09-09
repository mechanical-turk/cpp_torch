# Episode 7 - Automatic Differentiation

## Video brief

- Working title: Building Autograd from Scratch in C++ | Deep Learning, All the Way Down #7
- MP4 filename: `cpp-autograd-chain-rule-computation-graph-episode-07.mp4`
- Target runtime: 16 to 21 minutes
- Viewer promise: build a scalar computation graph that can trace one loss backward and calculate every input gradient automatically.
- Starting point: the Episode 6 implementation in `main.cpp`, ending with a rank-zero MSE loss of `1.0`.
- Only code file: `main.cpp`
- In scope: graph nodes, graph ownership, local derivatives, gradient accumulation, reverse topological traversal, and `backward()`.
- Deferred: Tensor integration, tensor-valued gradients, broadcasting backward, `matmul` backward, `requires_grad`, `zero_grad`, optimizers, and training loops.

---

## 00:00-00:55 - A loss cannot improve the model by itself

### Visual

Begin on a dedicated opening visual while speaking immediately.

Asset: `assets/autograd-full-model-opening-v4.png`

The diagram shows the complete known forward calculation. The orange path points
back toward the model parameters, whose gradients remain unknown:

```text
features: [4.0, 3.0, 2.0] --\
                                dot: 3.0 --\
weights:  [0.5, -1.0, 2.0] --/             add --> prediction: 3.5 --\
bias: 0.5 --------------------------------/                            subtract
target: 2.5 ----------------------------------------------------------/       \
                                                                    residual: 1.0
                                                                          |
                                                                        square
                                                                          |
                                                                      loss: 1.0

                                      <---------- backward ----------

∂L / ∂w = ?
∂L / ∂b = ?
```

Keep the layout stable as the narration follows the forward path, then points
back to the two unknown parameter gradients.

### Narration

> Welcome back to Deep Learning, All the Way Down, where we rebuild deep learning from first principles in modern C++.
>
> Our model starts with three features. It combines them with three weights and a bias to produce a prediction of `3.5`. Against a target of `2.5`, that gives us a residual of `1.0` and a squared loss of `1.0`.
>
> We already know how to calculate everything moving from left to right. Training needs us to go back in the other direction and work out how each weight and the bias affected the loss.
>
> Those derivatives are the parameter gradients. They tell us how changing each parameter would change the loss, and right now our code cannot fill in either question mark.
>
> We'll make every scalar operation remember how it was produced, then follow that history backward to recover the gradients automatically.

---

## 00:55-03:55 - Represent the graph as data

### Narration

> To move backward through a calculation, its intermediate results need to preserve how they were produced.
>
> Every node needs four things: its numerical value, its gradient, the operation that created it, and its parent nodes.

### Live coding

Add the required headers:

```cpp
#include <memory>
#include <unordered_set>
#include <utility>
```

Add the operation enum and graph node after `Tensor`:

```cpp
enum class Operation {
  leaf,
  add,
  subtract,
  multiply
};

struct Node {
  double data = 0.0;
  double grad = 0.0;
  Operation operation = Operation::leaf;
  std::vector<std::shared_ptr<Node>> parents;
};
```

### Narration

> A leaf is a value we supplied directly, such as a model parameter, feature, or target. The other enum values identify the operation that created an intermediate result.
>
> `data` stores the forward value. `grad` begins at zero and will eventually store how the final loss changes with respect to this node.
>
> `parents` stores the inputs that produced this node. Shared pointers keep those inputs alive.
>
> Before we build `Value`, let's let each node receive its forward value when it is created.

### Live coding

Add a constructor to `Node`:

```cpp
explicit Node(double value)
    : data(value) {}
```

### Narration

> The value is set immediately. The gradient and operation still use their defaults.
>
> We don't want the rest of our code handling node pointers directly, so we'll hide the pointer inside a `Value` class.

### Live coding

Add the initial `Value` handle:

```cpp
class Value {
 public:
  Value(double data)
      : node_(std::make_shared<Node>(data)) {}

  [[nodiscard]] double data() const noexcept {
    return node_->data;
  }

  [[nodiscard]] double grad() const noexcept {
    return node_->grad;
  }

 private:
  std::shared_ptr<Node> node_;
};
```

### Narration

> The public constructor creates a leaf. The accessors return its value and gradient.

---

## 03:55-06:30 - Make arithmetic construct the graph

### Narration

> `Value` can represent a leaf, but it cannot take part in a calculation yet. We'll add addition, subtraction, and multiplication.
>
> Each operator must calculate its result and record how that result was produced. We'll start with addition.

### Live coding

Begin `operator+` with the part we can already write:

```cpp
Value operator+(
    const Value& left,
    const Value& right
) {
  auto node = std::make_shared<Node>(
      left.data() + right.data()
  );
  node->operation = Operation::add;
}
```

### Narration

> We can calculate the result and record the operation with the public interface we already have.
>
> Next, the result must remember its operands. Their node pointers are private, so this free function cannot reach them yet.

### Live coding

Declare `operator+` as a friend in the public section of `Value`:

```cpp
friend Value operator+(
    const Value& left,
    const Value& right
);
```

### Narration

> It remains a free function, but it can now read `node_`.
>
> We can now store both operands as parents.

### Live coding

Add the parents to `operator+`:

```cpp
node->parents = {left.node_, right.node_};
```

### Narration

> The node now has its value, operation, and parents. Its gradient stays at the default of zero.
>
> We still need to return this node as a `Value`. Our public constructor accepts a number and creates a new leaf, which would lose the history we just recorded.

### Live coding

Add a constructor to the private section of `Value`:

```cpp
explicit Value(std::shared_ptr<Node> node)
    : node_(std::move(node)) {}
```

### Narration

> This constructor wraps an existing node. It stays private because only our graph operations should use it. The friend operator can call it.

### Live coding

Finish `operator+`:

```cpp
return Value(std::move(node));
```

### Narration

> We only wrap and return the node after all of its forward-pass information is ready.
>
> Subtraction and multiplication need the same private access, so we'll add their friend declarations before continuing.

### Live coding

Add the remaining friend declarations to `Value`:

```cpp
friend Value operator-(
    const Value& left,
    const Value& right
);

friend Value operator*(
    const Value& left,
    const Value& right
);
```

Continue with subtraction:

```cpp
Value operator-(
    const Value& left,
    const Value& right
) {
  auto node = std::make_shared<Node>(
      left.data() - right.data()
  );
  node->operation = Operation::subtract;
  node->parents = {left.node_, right.node_};

  return Value(std::move(node));
}
```

### Narration

> Subtraction follows the same pattern with a different forward calculation and operation label.

### Live coding

Implement multiplication before moving into the backward pass:

```cpp
Value operator*(
    const Value& left,
    const Value& right
) {
  auto node = std::make_shared<Node>(
      left.data() * right.data()
  );
  node->operation = Operation::multiply;
  node->parents = {left.node_, right.node_};

  return Value(std::move(node));
}
```

### Narration

> Multiplication completes the same pattern. Our forward graph operations are ready. And now we can begin thinking about the backward pass.

---

## 06:30-10:00 - Build a safe backward order

### Visual

```text
forward order

inputs --> intermediates --> loss

backward order

loss --> intermediates --> inputs
```

### Narration

> Backpropagation starts at the loss and moves toward the inputs, but we cannot simply follow one path at a time. Because a value may influence the loss through several later operations. Before that value propagates its gradient to its own parents, it must receive every contribution coming back from its dependents.

### Visual

```text
          --> branch A --\
shared value              --> loss
          --> branch B --/
```

### Narration

> Suppose one value feeds two branches. If we propagate through it after processing only branch A, its gradient is incomplete because branch B has not contributed yet.
>
> We need an order that processes both branches before the shared value. A topological order is an ordering where every input appears before the result that depends on it. Reversing that order guarantees that every result contributes before any of its inputs propagate further.

### Live coding

Add the helper directly to the private section of `Value`:

```cpp
static void build_topology(
    Node* node,
    std::unordered_set<Node*>& visited,
    std::vector<Node*>& topology
) {
  if (!visited.insert(node).second) {
    return;
  }

  for (const auto& parent : node->parents) {
    build_topology(
        parent.get(),
        visited,
        topology
    );
  }

  topology.push_back(node);
}
```

### Narration

> The visited set uses raw pointers only as node identities. It does not own or delete anything. Ownership remains with the shared pointers inside the graph.
>
> If a node has already been visited, we stop. This matters for shared subgraphs, including our residual, which appears twice as an input to the same multiplication.
>
> We visit every parent first, then append the current node. The loss therefore ends up at the back of the completed list, ready to be processed first when we traverse it in reverse.

---

## 10:00-14:30 - Implement `backward()`

### Narration

> We now have the graph, the local derivative rules, and a safe execution order. Let's connect them inside `backward()`.

### Live coding

Add the public declaration to `Value`:

```cpp
void backward();
```

### Narration

> `backward()` changes the gradients stored in the graph, so it is a non-const member function.

### Live coding

Build the traversal and leave the local rule as a placeholder:

```cpp
void Value::backward() {
  std::unordered_set<Node*> visited;
  std::vector<Node*> topology;

  build_topology(
      node_.get(),
      visited,
      topology
  );

  node_->grad = 1.0;

  for (
      auto current = topology.rbegin();
      current != topology.rend();
      ++current
  ) {
    Node* output = *current;
    // Apply this operation's local rule.
  }
}
```

### Narration

> We seed the loss gradient with `1.0` because the derivative of the loss with respect to itself is one. A tiny increase in the loss changes the loss by exactly the same amount.
>
> Our topological order stores every parent before the result that uses it. Backpropagation needs the opposite: results must propagate before their parents. That is why we iterate the topological order in reverse. By the time we reach a shared node, it has collected every gradient contribution and can propagate the total to its own parents. A leaf has no parents, so there is nothing left to propagate.
>
> Reverse order controls when a node propagates, but a node may receive gradients through several paths. Each path contributes part of its final gradient, so we must add those contributions together. That is why the rules below use `+=` and `-=`. Assignment would overwrite an earlier contribution.

### Live coding

Replace the placeholder with the operation rules:

```cpp
switch (output->operation) {
  case Operation::leaf:
    break;

  case Operation::add:
    output->parents[0]->grad += output->grad;
    output->parents[1]->grad += output->grad;
    break;

  case Operation::subtract:
    output->parents[0]->grad += output->grad;
    output->parents[1]->grad -= output->grad;
    break;

  case Operation::multiply:
    output->parents[0]->grad +=
        output->parents[1]->data *
        output->grad;

    output->parents[1]->grad +=
        output->parents[0]->data *
        output->grad;
    break;
}
```

### Narration

> Addition passes the arriving gradient to both parents. Subtraction passes it unchanged to the left and negates it for the right.
>
> Multiplication scales the arriving gradient by the other operand's forward value. This is the chain rule in code: the gradient that arrived from later in the graph multiplied by the operation's local derivative.
>
> Every update uses `+=` or `-=` rather than assignment. A node can affect the loss through multiple edges, and its final gradient is the sum of all those contributions.

### Live coding

Build a small loss graph and run the first backward pass:

```cpp
const Value scalar_prediction(3.5);
const Value scalar_target(2.5);
const Value scalar_residual =
    scalar_prediction - scalar_target;
Value scalar_loss =
    scalar_residual * scalar_residual;

scalar_loss.backward();

assert(scalar_loss.grad() == 1.0);
assert(scalar_residual.grad() == 2.0);
assert(scalar_prediction.grad() == 2.0);
assert(scalar_target.grad() == -2.0);
```

### Narration

> The loss gradient begins at `1.0`. The residual was multiplied by itself, so it receives two contributions of `1.0` and ends at `2.0`.
>
> Subtraction then passes that `2.0` to the prediction and `-2.0` to the target. One call to `backward()` recovered every derivative in the expression.
>
> This first version assumes one backward call per graph. We'll establish when gradients should be cleared once the same mechanism is attached to `Tensor` and used across training steps.

---

## 14:30-18:30 - Trace a model loss back to its parameters

### Narration

> Our small example proves the backward pass, but the real purpose is to reach model parameters. Let's rebuild one complete linear prediction with `Value` objects.

### Live coding

Build one prediction and loss in `main()`:

```cpp
const Value x1(4.0);
const Value x2(3.0);
const Value x3(2.0);

const Value w1(0.5);
const Value w2(-1.0);
const Value w3(2.0);
const Value model_bias(0.5);
const Value model_target(2.5);

const Value model_prediction =
    w1 * x1 +
    w2 * x2 +
    w3 * x3 +
    model_bias;

const Value model_residual =
    model_prediction - model_target;

Value model_loss =
    model_residual * model_residual;
```

### Narration

> This is the complete calculation from our opening visual. Each operator builds another piece of the graph, and `model_loss` holds the path back to every feature, weight, the bias, and the target.

### Live coding

Verify the forward values, then run the backward pass:

```cpp
assert(model_prediction.data() == 3.5);
assert(model_residual.data() == 1.0);
assert(model_loss.data() == 1.0);

model_loss.backward();
```

### Narration

> The prediction is `3.5`, so the residual is `1.0` and the squared loss is also `1.0`. Now we can follow its gradient backward.

### Live coding

Trace the gradient to the bias:

```cpp
assert(model_loss.grad() == 1.0);
assert(model_residual.grad() == 2.0);
assert(model_prediction.grad() == 2.0);
assert(model_bias.grad() == 2.0);
```

### Narration

> The loss starts at `1.0`. The residual appears on both sides of the multiplication, so its two contributions add to `2.0`. Subtraction passes that `2.0` to the prediction, and the final addition passes it unchanged to the bias.

### Live coding

Verify the weight gradients:

```cpp
assert(w1.grad() == 8.0);
assert(w2.grad() == 6.0);
assert(w3.grad() == 4.0);
```

### On screen

```text
prediction = 3.5
loss       = 1.0

loss.grad       = 1.0
residual.grad   = 2.0
prediction.grad = 2.0
bias.grad       = 2.0

d loss / d w1   = 8.0
d loss / d w2   = 6.0
d loss / d w3   = 4.0
```

### Narration

> The same gradient reaches each multiplication. Multiplication then scales it by the corresponding input, giving us `8.0`, `6.0`, and `4.0` for the three weights.
>
> We did not derive or hard-code a formula for this particular model. The graph recovered those gradients from the same small derivative rules we implemented for its individual operations.
>
> We have not trained the model yet, and this engine only handles scalar values. But for the first time, our C++ program can calculate how every parameter contributed to a loss automatically.

---

## 18:30-19:30 - Recap

### On screen

```text
What we covered

- graph nodes and operation history
- local derivative rules
- reverse topological traversal
- accumulated gradient contributions
- a working scalar backward() pass
```

### Narration

> We represented scalar calculations as a graph, encoded the local derivatives for each operation, ordered the graph for a safe backward traversal, accumulated gradients from shared paths, and built a working scalar `backward()` pass.

Replace the recap with:

```text
Next episode

- attach graph history to Tensor
- store tensor gradients
- differentiate MSE
```

### Narration

> Next, we'll carry this mechanism into `Tensor`, store gradients with tensor shapes, and differentiate the mean squared error we built earlier.

---

## Questions

### On screen

```text
1. Why must the loss gradient
   begin at 1.0?

2. Why do parent gradients use +=
   instead of assignment?

3. Why does backpropagation use
   reverse topological order?
```

### Narration

> Now, as always, I'll share a few questions for you to ponder before the next episode. You can read the answers in the pinned comment.
>
> First, why must the loss gradient begin at `1.0`?
>
> Second, why do parent gradients use `+=` instead of assignment?
>
> And third, why does backpropagation use reverse topological order?

### Sign-off

> That brings us to the end of this episode. Thanks for watching, and I will see you next time.

Replace the questions with a clean end-screen background and hold it for approximately five seconds. Place the YouTube Subscribe and complete-series-playlist elements only over this tail.
