# Episode 8 - Tensor Autograd

Proposed MP4 filename: `cpp-tensor-autograd-elementwise-backpropagation-episode-08.mp4`

## 1. Checklist plan

| Check | Plan |
| --- | --- |
| L01 | Build tensor graph storage, traversal and the four elementwise backward rules; defer reductions and training to Episode 9. Flag the recorded opening mismatch. |
| L02 | Show the existing result return and name the missing input connection. |
| L03 | Start shared-node edits around 0:15; by 0:30 constructor/storage changes are underway. Estimates only. |
| L04 | Verify shared-copy identity around the first minute; repeated storage edits are the main timing risk. |
| L05 | Storage, gradient buffers, input history, traversal, broadcast mapping and four arithmetic rules. Stop there. |
| L06 | Introduce parents at result creation and saved strides at backward mapping. |
| L07 | Explain whole-tensor nodes, recomputed indices, repeated contributions and the chain rule beside code. |
| L08 | Every edit has exact Before/After source; replay them in order with no hidden replacements. |
| L09 | Keep recorded checks; add no further on-camera tests. Verify the supported code off camera; teach the full test suite next episode. |
| L10 | Point to the current return, mapping or gradient update; no mandatory graphics. |
| L11 | Narrate the next concrete edit before making it, carry the reason across section boundaries, and explain the consequence afterward without repeating the setup. |
| L12 | Close after division. Next episode completes sum and matmul backward, tests them, and trains linear regression. |
| L13 | Itemized recap, follow-up list, standard sign-off and clean tail; no closing Q&A. |
| L14 | One read-aloud track marked with >; exact code pairs stay in the recording guide. |
| L15 | C++ tensor autograd is the candidate primary phrase; publishing-specific keyword research stays pending. |
| L16 | Use long-form evidence for ordering only; do not claim measured pacing, voice approval or predicted retention. |

## 2. Script

### Recording notes (not spoken)

Edit `main.cpp` at checkpoint `92aa868`. Keep `scalar_autograd.cpp` (`e692363`) unchanged as a separate reference program. The Before blocks match the evolving source, including prior edits. Replace each Before region with its After region; unchanged context shows the insertion point. No implied global substitutions, omitted caller updates or placeholder code. Only > paragraphs are spoken. Do not read the headings or display both versions throughout the video.

Complete preparation P.1-P.2 in the appendix before recording. They fix existing forward broadcasting bugs, not autograd; retain them in the eventual public diff. No autograd is built off camera. A.1-A.4 and D.2-E.3 contain intermediate states that are not ready to run. Use the explicit checkpoints.

Scope: scalar-root backward for finite examples, whole-tensor graph nodes, shared-copy semantics, and fresh reachable-gradient reset per call. Do not mutate participating data between forward/backward. No mutation guard, requires_grad filtering, sum backward, matmul backward, optimizer or training loop. Targets and constants may receive gradients.

Continuity note: the recorded opening below promises gradients from loss to predictions.
That full MSE path now belongs to Episode 9 because sum backward is deferred.
Preserve the recording here, but trim that promise or record a pickup before
release. Suggested pickup: "Let's add backpropagation to our tensor, starting
with the four arithmetic operators." No new opening code is needed.

Current boundary: backward accepts scalar roots. Scalar elementwise graphs can
run; batch MSE, mean and dot backward still need sum. The existing default throw
rejects unsupported operations but does not preserve gradients on failure.
Do not treat failed-call gradients as valid. No new live testing section follows
division. Off-camera verification is not part of the recorded lesson.

### Opening

On screen: the current return in `elementwise_binary()`. This is unchanged reference code, not an edit.

```cpp
    return Tensor(std::move(result_shape), std::move(result_data));
```

> Our tensor can calculate the loss. And now let's make it tell us how each prediction needs to change. We'll start here, where we return the result, because we need that result to remember which tensors it came from.

### A. Keep the tensor data alive

Begin the edits immediately. No separate architecture slide. A.1-A.4 are one storage migration; do not compile halfway through.

#### A.1. Includes and the new node above Tensor

Point from the result return to the existing `shape_` and `data_` fields, then introduce the node while speaking. Add the includes without a separate explanation.

> To do that, the result will need to hold on to its inputs, even after we leave the function that created them. Let's move their shape and data into a node that we can share.

<!-- edit: includes -->
**Before**

```cpp
#include <cassert>
```

**After**

```cpp
#include <cassert>
#include <memory>
#include <utility>
```

<!-- edit: node -->
**Before**

```cpp
class Tensor {
```

**After**

```cpp
struct TensorNode {
  std::vector<std::size_t> shape;
  std::vector<double> data;
};

class Tensor {
```

> Notice that I've kept the whole array together, with its shape. We're making one node per tensor. Now we can replace these two fields in Tensor with a pointer to that node.

#### A.2. Private storage

<!-- edit: storage -->
**Before**

```cpp
  std::vector<std::size_t> shape_;
  std::vector<double> data_;
```

**After**

```cpp
  std::shared_ptr<TensorNode> node_;
```

#### A.3. Constructor opening

> With those fields moved, let's fix the constructor. We'll create the node here, then move the shape and data into it.

<!-- edit: constructor -->
**Before**

```cpp
  Tensor(
    std::vector<std::size_t> shape,
    std::vector<double> data
  ) : shape_(std::move(shape)), data_(std::move(data)) {
```

**After**

```cpp
Tensor(
    std::vector<std::size_t> shape,
    std::vector<double> data
) : node_(std::make_shared<TensorNode>()) {
  node_->shape = std::move(shape);
  node_->data = std::move(data);
```

#### A.4. Existing reads and writes

Each pair below is an exact replacement. These edits only redirect storage access. Keep the numerical work unchanged; show the edits without reading each repeated pointer expression aloud.

> The rest of the class still uses the old fields, so let's update those accesses too. That includes the constructor checks. The calculations stay as they are; we're just reaching the same values through node now.

<!-- edit: storage-read-1 -->
**Before**

```cpp

    for (const std::size_t dimension: shape_) {
      if (dimension == 0) {
```

**After**

```cpp

    for (const std::size_t dimension: node_->shape) {
      if (dimension == 0) {
```

<!-- edit: storage-read-2 -->
**Before**

```cpp
      for (const std::size_t dimension: shape_) {
```

**After**

```cpp
      for (const std::size_t dimension: node_->shape) {
```

<!-- edit: storage-read-3 -->
**Before**

```cpp
    if (expected_elements != data_.size()) {
```

**After**

```cpp
    if (expected_elements != node_->data.size()) {
```

<!-- edit: storage-read-4 -->
**Before**

```cpp
    return shape_;
```

**After**

```cpp
    return node_->shape;
```

<!-- edit: storage-read-5 -->
**Before**

```cpp
    return data_;
```

**After**

```cpp
    return node_->data;
```

<!-- edit: storage-read-6 -->
**Before**

```cpp
    return shape_.size();
```

**After**

```cpp
    return node_->shape.size();
```

<!-- edit: storage-read-7 -->
**Before**

```cpp
    return data_.size();
```

**After**

```cpp
    return node_->data.size();
```

<!-- edit: storage-read-8 -->
**Before**

```cpp
    return shape_[axis];
```

**After**

```cpp
    return node_->shape[axis];
```

<!-- edit: storage-read-9 -->
**Before**

```cpp
  double& at(const std::vector<std::size_t>& idx) {
    return data_[flat_index(idx)];
  }
```

**After**

```cpp
  double& at(const std::vector<std::size_t>& idx) {
    return node_->data[flat_index(idx)];
  }
```

<!-- edit: storage-read-10 -->
**Before**

```cpp
    return data_[flat_index(idx)];
```

**After**

```cpp
    return node_->data[flat_index(idx)];
```

<!-- edit: storage-read-11 -->
**Before**

```cpp
    for (const double value: data_) {
```

**After**

```cpp
    for (const double value: node_->data) {
```

<!-- edit: storage-read-12 -->
**Before**

```cpp
    if (shape_ != other.shape_) {
```

**After**

```cpp
    if (node_->shape != other.node_->shape) {
```

<!-- edit: storage-read-13 -->
**Before**

```cpp
    const std::size_t left_rows = shape_[0];
```

**After**

```cpp
    const std::size_t left_rows = node_->shape[0];
```

<!-- edit: storage-read-14 -->
**Before**

```cpp
    const std::size_t left_cols = shape_[1];
```

**After**

```cpp
    const std::size_t left_cols = node_->shape[1];
```

<!-- edit: storage-read-15 -->
**Before**

```cpp
    const std::size_t right_rows = other.shape_[0];
```

**After**

```cpp
    const std::size_t right_rows = other.node_->shape[0];
```

<!-- edit: storage-read-16 -->
**Before**

```cpp
    const std::size_t right_cols = other.shape_[1];
```

**After**

```cpp
    const std::size_t right_cols = other.node_->shape[1];
```

<!-- edit: storage-read-17 -->
**Before**

```cpp
            data_[row * left_cols + index] * 
```

**After**

```cpp
            node_->data[row * left_cols + index] * 
```

<!-- edit: storage-read-18 -->
**Before**

```cpp
            other.data_[index * right_cols + col];
```

**After**

```cpp
            other.node_->data[index * right_cols + col];
```

<!-- edit: storage-read-19 -->
**Before**

```cpp
      shape_, other.shape_
```

**After**

```cpp
      node_->shape, other.node_->shape
```

<!-- edit: storage-read-20 -->
**Before**

```cpp
      shape_, strides(), result_shape.size()
```

**After**

```cpp
      node_->shape, strides(), result_shape.size()
```

<!-- edit: storage-read-21 -->
**Before**

```cpp
      other.shape_, other.strides(), result_shape.size()
```

**After**

```cpp
      other.node_->shape, other.strides(), result_shape.size()
```

<!-- edit: storage-read-22 -->
**Before**

```cpp
      result_data[flat] = operation(data_[left_index], other.data_[right_index]);
```

**After**

```cpp
      result_data[flat] = operation(node_->data[left_index], other.node_->data[right_index]);
```

<!-- edit: storage-read-23 -->
**Before**

```cpp
    std::vector<std::size_t> result(shape_.size());
```

**After**

```cpp
    std::vector<std::size_t> result(node_->shape.size());
```

<!-- edit: storage-read-24 -->
**Before**

```cpp
      stride *= shape_[axis];
```

**After**

```cpp
      stride *= node_->shape[axis];
```

<!-- edit: storage-read-25 -->
**Before**

```cpp
      if (idx[axis] >= shape_[axis]) {
```

**After**

```cpp
      if (idx[axis] >= node_->shape[axis]) {
```

<!-- edit: storage-read-26 -->
**Before**

```cpp
      stride *= shape_[current_axis];
```

**After**

```cpp
      stride *= node_->shape[current_axis];
```

#### A.5. Check shared identity at the end of main()

Stay on the completed storage edits for the first sentence, then move to `main()`. The run checks the refactor, not autograd: existing assertions check the calculations, and the new assertion checks shared storage. Point to the address comparison while explaining it.

> That finishes the storage refactor. Copying a Tensor should now share its node, which is how we'll keep referring to the same tensor through the graph. Let's create a predictions tensor and copy it. We'll compare the arrays' addresses to check that we really are sharing the data.

<!-- edit: storage-demo -->
**Before**

```cpp
  std::cout << "Success!\n";
```

**After**

```cpp
{
  const Tensor predictions({2, 1}, {3.5, 0.0});
  const Tensor alias = predictions;
  assert(&alias.data() == &predictions.data());
}
  std::cout << "Success!\n";
```

> Now let's run it along with our existing tests, to check that the calculations still work too.

<!-- checkpoint: A1-shared-storage -->
Checkpoint: compile and run the existing program. 

> The tests pass, including the address check. So we can reach the same data through either handle.

First payoff: changed copy identity, not working autograd. Aim for about one minute by cutting repeated typing pauses, not explanations. The exact storage edits remain visible in this guide. Timing is unverified.

### B. Add somewhere to collect the gradients

> We want the same thing for gradients: when backward updates a node through the graph, we should be able to read those gradients from our original tensor. So let's put a grad vector in that shared node too, with one entry for each value.

#### B.1. TensorNode

<!-- edit: grad-field -->
**Before**

```cpp
  std::vector<double> data;
```

**After**

```cpp
  std::vector<double> data;
  std::vector<double> grad;
```

#### B.2. Constructor end

> Let's initialize the gradients to zero.

<!-- edit: grad-init -->
**Before**

```cpp
    if (expected_elements != node_->data.size()) {
      throw std::invalid_argument("tensor shape does not match its data");
    }
  }
```

**After**

```cpp
    if (expected_elements != node_->data.size()) {
      throw std::invalid_argument("tensor shape does not match its data");
    }
    node_->grad.assign(numel(), 0.0);
  }
```

#### B.3. Public accessor, after data()

> And add a grad accessor so we can read the gradients.

<!-- edit: grad-accessor -->
**Before**

```cpp
  [[nodiscard]] const std::vector<double>& data() const noexcept {
    return node_->data;
  }
```

**After**

```cpp
  [[nodiscard]] const std::vector<double>& data() const noexcept {
    return node_->data;
  }

[[nodiscard]] const std::vector<double>& grad() const noexcept {
  return node_->grad;
}
```

<!-- checkpoint: A2-gradient-storage -->
Off-camera verification checkpoint: compile and run the existing program. In the recording, continue directly from the accessor to C; no separate test segment here. The no-mutation contract remains in the recording notes.

### C. Record which tensors produced each result

> To calculate these gradients, we need to know how each tensor was produced. So let's record the operation and its inputs in the node too.

#### C.1. Operation tags and parent fields

<!-- edit: operation -->
**Before**

```cpp
struct TensorNode {
```

**After**

```cpp
enum class Operation {
  leaf,
  add,
  subtract,
  multiply,
  divide,
  sum,
  matmul
};

struct TensorNode {
```

<!-- edit: parents -->
**Before**

```cpp
  std::vector<double> grad;
```

**After**

```cpp
  std::vector<double> grad;
  Operation operation = Operation::leaf;
  std::vector<std::shared_ptr<TensorNode>> parents;
```

> A tensor starts as a leaf, with no parents. Let's go to our arithmetic operators and record the parents when we create a result.

#### C.2. Binary helper signature

> They all call elementwise_binary, so we can record the parents in one place. But the helper also needs to know which operation called it. I'll add that as an argument alongside the lambda.

Do not compile until C.3 has updated all four callers.

<!-- edit: binary-signature -->
**Before**

```cpp
  [[nodiscard]] Tensor elementwise_binary(
    const Tensor& other,
    const auto& operation
  ) const {
```

**After**

```cpp
[[nodiscard]] Tensor elementwise_binary(
    const Tensor& other,
    Operation kind,
    const auto& operation
) const {
```

#### C.3. The four callers

> Now each caller can pass its tag: add, subtract, multiply or divide. We'll keep the lambdas doing the actual arithmetic.

Location: `operator+()`.

<!-- edit: caller-add -->
**Before**

```cpp
  [[nodiscard]] Tensor operator+(const Tensor& other) const {
    return elementwise_binary(
      other,
      [](const double left, const double right) {
        return left + right;
      }
    );
  }
```

**After**

```cpp
  [[nodiscard]] Tensor operator+(const Tensor& other) const {
    return elementwise_binary(
      other,
      Operation::add,
      [](const double left, const double right) {
        return left + right;
      }
    );
  }
```

Location: `operator-()`.

<!-- edit: caller-subtract -->
**Before**

```cpp
  [[nodiscard]] Tensor operator-(const Tensor& other) const {
    return elementwise_binary(
      other,
      [](const double left, const double right) {
        return left - right;
      }
    );
  }
```

**After**

```cpp
  [[nodiscard]] Tensor operator-(const Tensor& other) const {
    return elementwise_binary(
      other,
      Operation::subtract,
      [](const double left, const double right) {
        return left - right;
      }
    );
  }
```

Location: `operator*()`.

<!-- edit: caller-multiply -->
**Before**

```cpp
  [[nodiscard]] Tensor operator*(const Tensor& other) const {
    return elementwise_binary(
      other,
      [](const double left, const double right) {
        return left * right;
      }
    );
  }
```

**After**

```cpp
  [[nodiscard]] Tensor operator*(const Tensor& other) const {
    return elementwise_binary(
      other,
      Operation::multiply,
      [](const double left, const double right) {
        return left * right;
      }
    );
  }
```

Location: `operator/()`.

<!-- edit: caller-divide -->
**Before**

```cpp
  [[nodiscard]] Tensor operator/(const Tensor& other) const {
    return elementwise_binary(
      other,
      [](const double left, const double right) {
        return left / right;
      }
    );
  }
```

**After**

```cpp
  [[nodiscard]] Tensor operator/(const Tensor& other) const {
    return elementwise_binary(
      other,
      Operation::divide,
      [](const double left, const double right) {
        return left / right;
      }
    );
  }
```

#### C.4. Binary helper return

> Back in the helper, let's name the result before we return it. That gives us a chance to attach the operation and both parents.

<!-- edit: binary-result -->
**Before**

```cpp
    return Tensor(std::move(result_shape), std::move(result_data));
```

**After**

```cpp
Tensor result(std::move(result_shape), std::move(result_data));
result.node_->operation = kind;
result.node_->parents = {node_, other.node_};
return result;
```

> The result now points to both input tensors. We'll work out which cells to use when we write the backward rule.

#### C.5. Sum return

> Sum creates a result too, so let's do the same at its return. This time we only need one parent: the tensor we're summing.

<!-- edit: sum-result -->
**Before**

```cpp
    return Tensor({}, {result});
```

**After**

```cpp
Tensor output({}, {result});
output.node_->operation = Operation::sum;
output.node_->parents = {node_};
return output;
```

> We haven't changed the loop that adds the doubles. We're recording that whole sum as a single operation.

#### C.6. Matrix multiplication return

> That leaves matmul. Its backward rule will come later, but we still need to record it. Otherwise we'd reach this result during backward and mistake it for a leaf.

<!-- edit: matmul-result -->
**Before**

```cpp
    return Tensor(
      std::move(result_shape),
      std::move(result_data)
    );
```

**After**

```cpp
Tensor result(std::move(result_shape), std::move(result_data));
result.node_->operation = Operation::matmul;
result.node_->parents = {node_, other.node_};
return result;
```

> We're recording the whole matrix multiplication as one operation, with the two input tensors as parents.

<!-- checkpoint: B-history -->
Checkpoint: compile and run the existing program. 

### Continuation plan (not spoken)

Everything through B-history stays unchanged. From here, explain only what the
viewer can establish from this episode's code. Do not refer to a previous
scalar implementation. The plan at the top still applies; this continuation
adds these recording decisions:

- D: build the node list in three edits, then use it inside backward.
- E: implement addition, subtraction, multiplication and division, in order.
- F: recap and sign-off. Sum, matmul, the test walkthrough and training move to Episode 9.

Explain a line's purpose before or while writing it. Finish a code edit before
announcing a run. Routine verification stays off camera.

### D. Follow the graph

#### D.1. Collect the nodes

Keep the parents field visible, then move to Tensor's private section.

> Now that each result remembers its parents, let's follow those links back from the loss. We'll collect the nodes in a list so we can calculate their gradients in the right order.

Introduce the helper and its two containers while typing the signature. Do not
stop to explain the include.

> We'll put the list in topology. A node can appear in more than one branch, so we'll also keep a visited set to avoid adding it twice.

<!-- edit: unordered-include -->
**Before**

```cpp
#include <memory>
```

**After**

```cpp
#include <memory>
#include <unordered_set>
```

<!-- edit: topology-start -->
**Before**

```cpp
private:
  std::shared_ptr<TensorNode> node_;
```

**After**

```cpp
private:
  std::shared_ptr<TensorNode> node_;

static void build_topology(
    TensorNode* node,
    std::unordered_set<TensorNode*>& visited,
    std::vector<TensorNode*>& topology
) {
}
```

The helper is intentionally incomplete until D.3. Continue typing.

#### D.2. Avoid visiting the same node twice

> Let's check that set first. Insert tells us whether this node is new. If it was already there, we've visited it and can return.

<!-- edit: topology-visited -->
**Before**

```cpp
private:
  std::shared_ptr<TensorNode> node_;

static void build_topology(
    TensorNode* node,
    std::unordered_set<TensorNode*>& visited,
    std::vector<TensorNode*>& topology
) {
}
```

**After**

```cpp
private:
  std::shared_ptr<TensorNode> node_;

static void build_topology(
    TensorNode* node,
    std::unordered_set<TensorNode*>& visited,
    std::vector<TensorNode*>& topology
) {
  if (!visited.insert(node).second) {
    return;
  }
}
```

#### D.3. Visit the parents before adding the result

> Otherwise, we'll visit each parent with another call to this function. Once those calls finish, we add the current node to the list.

<!-- edit: topology-finish -->
**Before**

```cpp
private:
  std::shared_ptr<TensorNode> node_;

static void build_topology(
    TensorNode* node,
    std::unordered_set<TensorNode*>& visited,
    std::vector<TensorNode*>& topology
) {
  if (!visited.insert(node).second) {
    return;
  }
}
```

**After**

```cpp
private:
  std::shared_ptr<TensorNode> node_;

static void build_topology(
    TensorNode* node,
    std::unordered_set<TensorNode*>& visited,
    std::vector<TensorNode*>& topology
) {
  if (!visited.insert(node).second) {
    return;
  }

  for (const auto& parent : node->parents) {
    build_topology(parent.get(), visited, topology);
  }

  topology.push_back(node);
}
```

Point to the recursive call, then the push_back below it.

> Because we add the node after visiting its parents, every input comes before the results that use it. That's a topological order. We'll read it backward when we calculate gradients, so a result can update its inputs before we process them.

<!-- checkpoint: C-traversal -->
Off-camera verification: compile and run. Continue directly to backward in the recording.

#### D.4. Start backward from a scalar

> Let's use this list in a public backward method. Our loss contains one number, so we'll accept a scalar tensor here and collect the nodes connected to it.

<!-- edit: backward-start -->
**Before**

```cpp
[[nodiscard]] const std::vector<double>& grad() const noexcept {
  return node_->grad;
}
```

**After**

```cpp
[[nodiscard]] const std::vector<double>& grad() const noexcept {
  return node_->grad;
}

void backward() {
  if (rank() != 0) {
    throw std::invalid_argument("backward requires a scalar loss");
  }

  std::unordered_set<TensorNode*> visited;
  std::vector<TensorNode*> topology;
  build_topology(node_.get(), visited, topology);
}
```

### Revised continuation notes (not spoken)

Preserve the recorded implementation through D.5. D.6 starts the reverse loop
with leaf. E adds add, subtract, multiply and divide in that order; F closes
the episode. Sum and matmul backward are deferred.

The checkpoints below supersede the earlier broad incomplete-stage warning.
Do not run backward between adding a helper call and finishing its definition.
Scalar addition is checked off camera after E.1. No further on-camera tests
or MSE demonstration follow the arithmetic rules.
The L01-L16 plan at the top still applies; the updated audit addresses this order.

#### D.5. Give the backward pass its starting gradient

Stay in backward(), immediately below build_topology.

> We've collected the nodes. Let's clear their gradients so this call starts from zero, then set the loss gradient to one. The loss changes one-for-one with itself, and that's where we start.

<!-- edit: backward-seed -->
**Before**

```cpp
void backward() {
  if (rank() != 0) {
    throw std::invalid_argument("backward requires a scalar loss");
  }

  std::unordered_set<TensorNode*> visited;
  std::vector<TensorNode*> topology;
  build_topology(node_.get(), visited, topology);
}
```

**After**

```cpp
void backward() {
  if (rank() != 0) {
    throw std::invalid_argument("backward requires a scalar loss");
  }

  std::unordered_set<TensorNode*> visited;
  std::vector<TensorNode*> topology;
  build_topology(node_.get(), visited, topology);

  for (TensorNode* node : topology) {
    std::fill(node->grad.begin(), node->grad.end(), 0.0);
  }
  node_->grad[0] = 1.0;
}
```


#### D.6. Walk backward, starting with leaf

> Let's work through the nodes in reverse and use the operation tag to choose what to do. We'll start with leaf. It has no parents, so we leave its gradient alone and move to the next node.

Write the reverse loop, switch and leaf case in that order. No operation
helper or sum rule is introduced here.

<!-- edit: backward-leaf-walk -->
**Before**

```cpp
void backward() {
  if (rank() != 0) {
    throw std::invalid_argument("backward requires a scalar loss");
  }

  std::unordered_set<TensorNode*> visited;
  std::vector<TensorNode*> topology;
  build_topology(node_.get(), visited, topology);

  for (TensorNode* node : topology) {
    std::fill(node->grad.begin(), node->grad.end(), 0.0);
  }
  node_->grad[0] = 1.0;
}
```

**After**

```cpp
  void backward() {
    if (rank() != 0) {
      throw std::invalid_argument("backward requires a scalar loss");
    }

    std::unordered_set<TensorNode*> visited;
    std::vector<TensorNode*> topology;
    build_topology(node_.get(), visited, topology);

    for (TensorNode* node: topology) {
      std::fill(node->grad.begin(), node->grad.end(), 0.0);
    }

    node_->grad[0] = 1.0;

    for (auto it = topology.rbegin(); it != topology.rend(); ++it) {
      TensorNode* output = *it;
      switch (output->operation) {
        case Operation::leaf:
          break;

        default:
          throw std::logic_error("backward rule not implemented yet");
      
      }
    }

  }
```


Point to break, then to the reverse iterator.

> That break leaves the switch, not the loop. We still need to visit the other nodes. Going in reverse lets every result contribute to its inputs before we process them.

The catch-all throws for operations not implemented yet. Keep typing rather
than adding a separate error-handling segment or a leaf-only demonstration.

### E. Add the arithmetic rules

#### E.1. Addition

> For addition, we do have parents to update. Each output uses one value from each input, so we need to find those two values and add to their gradients.

> We'll put that work in a private helper called backward_elementwise. We'll pass it the result node, and it will update both parents' gradients. The other arithmetic operations will use the same input mapping, so they'll share this helper.

Stay in backward(). Add the case immediately after leaf. The helper does not
exist yet; do not compile until its implementation below is complete.

<!-- edit: dispatch-add -->
**Before**

```cpp
switch (output->operation) {
        case Operation::leaf:
          break;

        default:
          throw std::logic_error("backward rule not implemented yet");
      
      }
```

**After**

```cpp
switch (output->operation) {
        case Operation::leaf:
          break;

        case Operation::add:
          backward_elementwise(output);
          break;

        default:
          throw std::logic_error("backward rule not implemented yet");
      
      }
```


> Before we write the helper's loop, let's go to elementwise_binary and look at how the forward loop finds those input cells.

Location: Tensor::elementwise_binary(), inside its existing forward loop.
Point to the two stride_offset calls. Unchanged reference code:

```cpp
const std::size_t left_index = stride_offset(coordinate, left_strides);
const std::size_t right_index = stride_offset(coordinate, right_strides);
```

> These strides give us the input indices, including when an input is broadcast. They're local to this function, though, so backward won't have them. Let's store them on the result node.

> Let's go up to TensorNode and add left_strides and right_strides just below parents.

Location: TensorNode, above class Tensor. Add the fields here, not inside
backward_elementwise or the Tensor handle.

<!-- edit: stride-fields -->
**Before**

```cpp
  std::vector<std::shared_ptr<TensorNode>> parents;
```

**After**

```cpp
  std::vector<std::shared_ptr<TensorNode>> parents;
  std::vector<std::size_t> left_strides;
  std::vector<std::size_t> right_strides;
```

> Now return to elementwise_binary, where we attach the result's parents. We'll copy the two stride vectors into that same node before returning it.

Location: the end of Tensor::elementwise_binary(), immediately before return result.

Recording reconciliation, not new narration: the presenter already removed
const from these locals and moved them into the result. These pairs document
that recorded change for full-source replay.

<!-- edit: recorded-left-strides -->
**Before**

```cpp
    const std::vector<std::size_t> left_strides = effective_strides(
```

**After**

```cpp
    std::vector<std::size_t> left_strides = effective_strides(
```
<!-- edit: recorded-right-strides -->
**Before**

```cpp
    const std::vector<std::size_t> right_strides = effective_strides(
```

**After**

```cpp
    std::vector<std::size_t> right_strides = effective_strides(
```

<!-- edit: save-strides -->
**Before**

```cpp
Tensor result(std::move(result_shape), std::move(result_data));
result.node_->operation = kind;
result.node_->parents = {node_, other.node_};
return result;
```

**After**

```cpp
Tensor result(std::move(result_shape), std::move(result_data));
result.node_->operation = kind;
result.node_->parents = {node_, other.node_};
result.node_->left_strides = std::move(left_strides);
result.node_->right_strides = std::move(right_strides);
return result;
```


> The result now keeps everything the helper needs. Let's write backward_elementwise in Tensor's private section, just below build_topology.

Location: inside class Tensor, under private:, immediately after the complete
build_topology definition. Keep that existing function unchanged.

> We'll take the two parents from the result node, then loop over its output values. For each one, the saved strides give us the input indices, and grad gives us the gradient to pass back.

<!-- edit: elementwise-map -->
**Before**

```cpp
static void build_topology(
    TensorNode* node,
    std::unordered_set<TensorNode*>& visited,
    std::vector<TensorNode*>& topology
) {
  if (!visited.insert(node).second) {
    return;
  }

  for (const auto& parent : node->parents) {
    build_topology(parent.get(), visited, topology);
  }

  topology.push_back(node);
}
```

**After**

```cpp
static void build_topology(
    TensorNode* node,
    std::unordered_set<TensorNode*>& visited,
    std::vector<TensorNode*>& topology
) {
  if (!visited.insert(node).second) {
    return;
  }

  for (const auto& parent : node->parents) {
    build_topology(parent.get(), visited, topology);
  }

  topology.push_back(node);
}

  static void backward_elementwise(TensorNode* output) {
    TensorNode* left = output->parents[0].get();
    TensorNode* right = output->parents[1].get();

    std::vector<std::size_t> coordinate(output->shape.size(), 0);

    for (std::size_t flat = 0; flat < output->data.size(); ++flat) {
      const std::size_t left_index = stride_offset(coordinate, output->left_strides);
      const std::size_t right_index = stride_offset(coordinate, output->right_strides);

      const double gradient = output->grad[flat];
      advance_coordinate(coordinate, output->shape);
    }

  }
```


### Continue from the recorded line

Already spoken, retained here only to locate the pickup:

> So, right now, we can actually begin implementing the specific operation based local derivative rules as we propagate the gradient.

Pickup plan (not spoken): keep the mapping loop exactly as recorded. Choose
the derivative rule in backward's existing switch and pass it into the helper.
The helper applies that rule to each pair of input values; it does not inspect
the operation tag. Leaf is already complete; continue with addition,
subtraction, multiplication and division, then wrap up. Do not repeat the
stride explanation or record an inner switch only to remove it.

#### E.1.a. Accept the derivative rule

> We'll pass that rule into this helper, so let's add a parameter for it. It will take the two input values and return their local derivatives.

Stay at the backward_elementwise signature in Tensor's private section.
Keep the existing parents, coordinate and loop body in place. The caller
will be fixed after the loop updates below; do not compile between these edits.

<!-- edit: derivative-parameter -->
**Before**

```cpp
static void backward_elementwise(TensorNode* output) {
```

**After**

```cpp
static void backward_elementwise(
      TensorNode* output,
      const auto& local_derivatives
  ) {
```

#### E.1.b. Apply the rule inside the loop

> Inside the loop, we've already found the input indices. Let's pass those two values to the rule and unpack the derivatives it returns: left first, then right.

Location: after reading gradient, immediately before advance_coordinate.
Explain the two updates as they appear.

> These derivatives tell us how each input changes this operation's output. But we want to know how it changes the final loss. The incoming gradient tells us how that output affects the loss, so we multiply the two. That's the chain rule.
>
> If an input changes the output twice as much, and that output changes the loss three times as much, the combined effect is six.
>
> We then add that contribution to the input's gradient. Plus-equals keeps the contributions from every use of that input, including broadcasting.

<!-- edit: apply-derivatives -->
**Before**

```cpp
const double gradient = output->grad[flat];
      advance_coordinate(coordinate, output->shape);
```

**After**

```cpp
const double gradient = output->grad[flat];
      const auto [left_derivative, right_derivative] = local_derivatives(
          left->data[left_index],
          right->data[right_index]
      );
      left->grad[left_index] += gradient * left_derivative;
      right->grad[right_index] += gradient * right_derivative;

      advance_coordinate(coordinate, output->shape);
```

#### E.1.c. Fix the addition caller

> The helper now needs a rule, so let's go back to the addition case in backward and pass one in. For addition, both local derivatives are one.

Location: Tensor::backward(), case Operation::add. Replace its existing
one-argument helper call with this call and lambda.

<!-- edit: addition-lambda -->
**Before**

```cpp
backward_elementwise(output);
```

**After**

```cpp
backward_elementwise(
              output,
              [](double, double) {
                return std::pair{1.0, 1.0};
              }
          );
```

> The lambda accepts two input values and returns the two derivatives as a pair. Addition doesn't need the values, but multiplication and division will. Each case will supply its own rule, so we won't need to check the operation inside the coordinate loop.

<!-- checkpoint: E-addition -->
Off-camera verification: compile and check scalar addition backward. No
sum rule is required here. Continue directly to subtraction on camera.

#### E.2. Subtraction

> Next, let's add subtraction. The left derivative is still one, but the right derivative is negative one because increasing the right input decreases the result.

Location: the outer switch in Tensor::backward(), after the addition case.
Replace the catch-all region with the new case followed by the same catch-all.

<!-- edit: subtract-lambda -->
**Before**

```cpp
default:
          throw std::logic_error("backward rule not implemented yet");
```

**After**

```cpp
case Operation::subtract:
          backward_elementwise(
              output,
              [](double, double) {
                return std::pair{1.0, -1.0};
              }
          );
          break;

        default:
          throw std::logic_error("backward rule not implemented yet");
```


#### E.3. Multiplication

> Multiplication needs the input values, so we'll name the lambda's arguments left and right. The left derivative is the value on the right, and the right derivative is the value on the left.

Add this case below subtraction, without leaving backward().

<!-- edit: multiply-lambda -->
**Before**

```cpp
default:
          throw std::logic_error("backward rule not implemented yet");
```

**After**

```cpp
case Operation::multiply:
          backward_elementwise(
              output,
              [](double left, double right) {
                return std::pair{right, left};
              }
          );
          break;

        default:
          throw std::logic_error("backward rule not implemented yet");
```


> If we're squaring a tensor, both inputs point to the same node. The helper's two plus-equals updates then add both contributions to that same gradient entry.

#### E.4. Division

> Before we add the division rule, let's handle a zero denominator in the forward operator. We need to reject it before calculating the result.

Location: Tensor::operator/(), inside its existing arithmetic lambda. Add this
guard before returning left / right. Then return to backward's switch.

<!-- edit: forward-division-zero -->
**Before**

```cpp
      [](const double left, const double right) {
        return left / right;
      }
```

**After**

```cpp
      [](const double left, const double right) {
        if (right == 0.0) {
          throw std::domain_error("division by zero");
        }
        return left / right;
      }
```

> Now the backward rule can assume the denominator isn't zero, as long as we don't change the tensor values between forward and backward.

> For division, we'll name them numerator and denominator. The numerator's derivative is one over the denominator. The denominator's derivative is negative numerator over denominator squared.

Stay in the same switch. Add division below multiplication.

<!-- edit: divide-lambda -->
**Before**

```cpp
default:
          throw std::logic_error("backward rule not implemented yet");
```

**After**

```cpp
case Operation::divide:
          backward_elementwise(
              output,
              [](double numerator, double denominator) {
                return std::pair{
                    1.0 / denominator,
                    -numerator / (denominator * denominator)
                };
              }
          );
          break;

        default:
          throw std::logic_error("backward rule not implemented yet");
```


> That's all four arithmetic rules. Each case picks a lambda once, and the helper uses it throughout the coordinate loop.

Off-camera contract: forward division now rejects an accessed zero denominator,
including negative zero. Do not mutate participating values between forward and
backward. This is not a general NaN, infinity, overflow or underflow policy;
the examples still use finite, well-scaled inputs. This chooses the
rule once per tensor operation, not once per entire graph. Do not claim a
measured speedup or guaranteed machine-code improvement; no benchmark was run.

<!-- checkpoint: E-elementwise-complete -->
Off-camera verification only: compile the completed arithmetic rules. No further
on-camera implementation or test walkthrough in this episode.

### F. Ending

#### Recap

Keep the completed arithmetic switch visible as the recap appears.

On screen:

```text
Recap

- Shared tensor nodes and gradients
- Calculation history and backward traversal
- Broadcasting and gradient accumulation
- Add, subtract, multiply and divide
```

> We've now connected the arithmetic operators to backward, including how they add up gradients when an input is reused. Let's wrap up here and leave sum and matrix multiplication for the next episode.

#### Next episode

Replace the recap with:

```text
Next episode

- Sum and matmul backward
- Gradient tests
- Train a linear regression model
```

> Once those two rules are in place, we can take the loss all the way back to the weights and bias. We'll test the gradients, then use them in a linear regression loop that actually learns from data.

Production scope for Episode 9: implement sum and matmul backward; test arithmetic,
broadcast reuse, reductions and both matmul inputs; then run a complete linear
regression training loop and show loss decreasing. Rebuild the forward graph
after each parameter update. Do not mutate values still needed by backward.
Choose and verify the data, learning rate and training result while preparing
that episode, not as additional work in this recording.

#### Sign-off

> That brings us to the end of this episode. Thanks for watching, and I will see you next time.

Cut to a clean five-second tail for Subscribe and complete-series playlist
end-screen elements. No closing questions, answer key or answer-comment action.

### Preparation appendix (off camera)

Apply these forward-safety fixes before A, as required by the preserved recording
notes. They remain here for source replay, not as additional on-camera work.

#### P.1. Empty and singleton broadcast dimensions

<!-- edit: prep-zero -->
**Before**

```cpp
      result[axis] = std::max(left_dim, right_dim);
```

**After**

```cpp
result[axis] = left_dim == 1 ? right_dim : left_dim;
```


#### P.2. Checked output allocation

<!-- edit: prep-size -->
**Before**

```cpp
    std::size_t result_numel = 1;
    for (const std::size_t dim: result_shape) {
      result_numel *= dim;
    }
```

**After**

```cpp
std::size_t result_numel = 0;
if (std::find(result_shape.begin(), result_shape.end(), 0)
    == result_shape.end()) {
  result_numel = 1;
  for (const std::size_t dim : result_shape) {
    if (result_numel > std::numeric_limits<std::size_t>::max() / dim) {
      throw std::overflow_error("broadcast result size overflows size_t");
    }
    result_numel *= dim;
  }
}
```


<!-- checkpoint: preparation-forward-safety -->
Off-camera verification: compile and run before recording A.

## 3. Checklist audit

The recorded implementation through E.4 is preserved. This scope revision removes
the remaining implementation and demonstrations, not completed recording work.

| Check | Status | Points | Evidence / remaining repair |
| --- | --- | ---: | --- |
| L01 | PARTIAL | 5 | Arithmetic scope is explicit, but the recorded opening promises the full loss-to-prediction path. Trim it or record the suggested pickup. |
| L02 | PASS | 10 | Existing return and missing graph connection remain the cold opening. |
| L03 | PASS | 8 | Storage edits follow immediately; timing remains an estimate. |
| L04 | PARTIAL | 4 | First shared-copy payoff still needs a paced media check. |
| L05 | PASS | 8 | A-E build storage, history, traversal and the four arithmetic rules; no extra implementation after division. |
| L06 | PASS | 8 | Helper signature, body and caller remain in recording order. Deferred rules are not introduced in another detour. |
| L07 | PASS | 8 | Chain rule, += and broadcast index reuse remain beside the code. No claim that MSE backward is complete. |
| L08 | PASS | 10 | See verification.md for literal replay and the supported scalar-root contract. Default throw retains explicit unsupported-operation failure. |
| L09 | PASS | 6 | Existing recorded checks remain; off-camera checks cover the narrowed scope. Full on-camera tests move to Episode 9. |
| L10 | PASS | 5 | Finish on the arithmetic switch, then readable recap and next-episode lists. |
| L11 | PARTIAL | 2.5 | Closing is concise and connected; actual spoken delivery is not verified. |
| L12 | PARTIAL | 2 | Arithmetic implementation is complete, but the original opening's full loss promise needs the stated continuity repair. Training is explicitly next episode. |
| L13 | PASS | 4 | Itemized recap, next episode, exact sign-off and clean tail; no Q&A. |
| L14 | PASS | 2 | Spoken lines use >; recorded code is preserved and continuity risk is explicit. |
| L15 | PARTIAL | 1 | Proposed filename no longer claims MSE. Platform keyword research and publishing approval remain pending. |
| L16 | PASS | 2 | Scope cut is creator direction, not a measured retention finding. Code checks do not approve voice or publication. |

## 4. Critique

The cut avoids extending a substantial refactor with two more backward rules,
test demonstrations and MSE interpretation. The last useful action is the division
rule; the ending names the remaining work and connects it to training.

The main weakness is continuity: the recorded opening promised a result that now
moves to Episode 9. Repair that sentence during editing. Do not claim this episode
already backpropagates through batch MSE or trains a model. The general broadcast
mapping is implemented, but its end-to-end reduction-based demonstration is
deferred with sum.

Episode 9 now has a concrete outcome: verified gradients powering an actual
linear regression training loop. Keep that outcome central when planning it;
do not turn the tests into a long inventory of obvious assertions.

## 5. Final score

Repair the opening promise before release; check closing delivery in the edit.
Verification does not establish recording pace or publishing readiness.

**Score: 85.5/100. Decision: rework.**
