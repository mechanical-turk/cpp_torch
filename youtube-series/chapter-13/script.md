# Refactoring Our C++ Deep Learning Library: CMake and GoogleTest | Deep Learning, All the Way Down #13

MP4 filename: `cpp-deep-learning-library-refactor-cmake-googletest-episode-13.mp4`

Start in the recorded Episode 12 `main.cpp`. Keep the working refactor checkout as a reference, not the starting file. Expand a mechanical-move panel only when performing that move; its code is part of the recording guide, not a separate lecture. Keep unchanged function bodies when moving them.

## A. Keep each input with its broadcast mapping

Open `elementwise_binary()` at the result construction. Highlight the parent list and the two stride assignments together.

> Our C++ deep learning code trains a digit classifier, but every operation has to assemble its graph by hand. Let's fix that before splitting the library into files.

> These strides describe how each input was broadcast. We'll put each mapping beside the input it belongs to.

Location: `main.cpp`.

<!-- edit: parent-record file: main.cpp -->
**Before**
```cpp
struct TensorNode {
  std::vector<std::size_t> shape;
  std::vector<double> data;
  std::vector<double> grad;

  Operation operation = Operation::leaf;
  std::vector<std::shared_ptr<TensorNode>> parents;

  std::vector<std::size_t> left_strides;
  std::vector<std::size_t> right_strides;
};
```

**After**
```cpp
struct TensorNode;

struct Parent {
  std::shared_ptr<TensorNode> node;
  std::vector<std::size_t> broadcast_strides;
};

struct TensorNode {
  std::vector<std::size_t> shape;
  std::vector<double> data;
  std::vector<double> grad;

  Operation operation = Operation::leaf;
  std::vector<Parent> parents;
};
```

While writing `Parent`, point from `node` to `broadcast_strides`. This multi-edit migration is incomplete until A ends; do not compile halfway through it.

> A parent now contains both pieces. The vector still lets an operation have several inputs, but we no longer need separate left and right fields on the result.

Location: `main.cpp`.

<!-- edit: binary-parent-mappings file: main.cpp -->
**Before**
```cpp
    result.node_->parents = {node_, other.node_};
    result.node_->left_strides = std::move(left_strides);
    result.node_->right_strides = std::move(right_strides);
```

**After**
```cpp
    result.node_->parents = {
      {node_, std::move(left_strides)},
      {other.node_, std::move(right_strides)}
    };
```

> The first entry holds the left input and its mapping; the second holds the right. Matrix multiplication and reductions use different backward rules, so their parent entries leave these strides empty.

Location: `main.cpp`.

<!-- edit: column-sum-parent file: main.cpp -->
**Before**
```cpp
    result.node_->operation = Operation::sum_columns;
    result.node_->parents = {node_};
```

**After**
```cpp
    result.node_->operation = Operation::sum_columns;
    result.node_->parents = {{node_, {}}};
```

Location: `main.cpp`.

<!-- edit: sum-parent file: main.cpp -->
**Before**
```cpp
    output.node_->operation = Operation::sum;
    output.node_->parents = {node_};
```

**After**
```cpp
    output.node_->operation = Operation::sum;
    output.node_->parents = {{node_, {}}};
```

Location: `main.cpp`.

<!-- edit: matmul-parents file: main.cpp -->
**Before**
```cpp
    result.node_->operation = Operation::matmul;
    result.node_->parents = {node_, other.node_};
```

**After**
```cpp
    result.node_->operation = Operation::matmul;
    result.node_->parents = {{node_, {}}, {other.node_, {}}};
```

Location: `main.cpp`.

<!-- edit: unary-parent file: main.cpp -->
**Before**
```cpp
    result.node_->operation = kind;
    result.node_->parents = {node_};
```

**After**
```cpp
    result.node_->operation = kind;
    result.node_->parents = {{node_, {}}};
```

> Backward still needs the same input values. We’ll reach them through the node inside each parent, and read the broadcast mapping beside it.

<details>
<summary>Exact code: elementwise-backward-parents</summary>

Location: `main.cpp`.

<!-- edit: elementwise-backward-parents file: main.cpp -->
**Before**
```cpp
  static void backward_elementwise(
    TensorNode* output,
    const auto& local_derivatives
  ) {
    TensorNode* left = output->parents[0].get();
    TensorNode* right = output->parents[1].get();

    std::vector<std::size_t> coordinate(output->shape.size(), 0);

    for (std::size_t flat = 0; flat < output->data.size(); ++flat) {
      const std::size_t left_index = stride_offset(coordinate, output->left_strides);
      const std::size_t right_index = stride_offset(coordinate, output->right_strides);

      const double gradient = output->grad[flat];

      const auto [left_derivative, right_derivative] = 
        local_derivatives(left->data[left_index], right->data[right_index]);

      left->grad[left_index] += gradient * left_derivative;
      right->grad[right_index] += gradient * right_derivative;
        
      advance_coordinate(coordinate, output->shape);


    }

  }
```

**After**
```cpp
  static void backward_elementwise(
    TensorNode* output,
    const auto& local_derivatives
  ) {
    TensorNode* left = output->parents[0].node.get();
    TensorNode* right = output->parents[1].node.get();

    std::vector<std::size_t> coordinate(output->shape.size(), 0);

    for (std::size_t flat = 0; flat < output->data.size(); ++flat) {
      const std::size_t left_index = stride_offset(coordinate, output->parents[0].broadcast_strides);
      const std::size_t right_index = stride_offset(coordinate, output->parents[1].broadcast_strides);

      const double gradient = output->grad[flat];

      const auto [left_derivative, right_derivative] = 
        local_derivatives(left->data[left_index], right->data[right_index]);

      left->grad[left_index] += gradient * left_derivative;
      right->grad[right_index] += gradient * right_derivative;
        
      advance_coordinate(coordinate, output->shape);


    }

  }
```

</details>

<details>
<summary>Exact code: unary-backward-parent</summary>

Location: `main.cpp`.

<!-- edit: unary-backward-parent file: main.cpp -->
**Before**
```cpp
  static void backward_unary(
    TensorNode* output,
    const auto& local_derivative
  ) {
    TensorNode* input = output->parents[0].get();

    for (std::size_t index = 0; index < output->data.size(); ++index) {
      input->grad[index] +=
        output->grad[index] *
        local_derivative(input->data[index], output->data[index]);
    }

  }
```

**After**
```cpp
  static void backward_unary(
    TensorNode* output,
    const auto& local_derivative
  ) {
    TensorNode* input = output->parents[0].node.get();

    for (std::size_t index = 0; index < output->data.size(); ++index) {
      input->grad[index] +=
        output->grad[index] *
        local_derivative(input->data[index], output->data[index]);
    }

  }
```

</details>

In `backward()`, update these three input lookups. The numerical rules stay unchanged.

Location: `main.cpp`.

<!-- edit: sum_columns-backward-parent file: main.cpp -->
**Before**
```cpp
        case Operation::sum_columns: {
          TensorNode* input = output->parents[0].get();
```

**After**
```cpp
        case Operation::sum_columns: {
          TensorNode* input = output->parents[0].node.get();
```

Location: `main.cpp`.

<!-- edit: matmul-backward-parent file: main.cpp -->
**Before**
```cpp
        case Operation::matmul: {
          TensorNode* left = output->parents[0].get();
          TensorNode* right = output->parents[1].get();
```

**After**
```cpp
        case Operation::matmul: {
          TensorNode* left = output->parents[0].node.get();
          TensorNode* right = output->parents[1].node.get();
```

Location: `main.cpp`.

<!-- edit: sum-backward-parent file: main.cpp -->
**Before**
```cpp
        case Operation::sum: {
          TensorNode* input = output->parents[0].get();
```

**After**
```cpp
        case Operation::sum: {
          TensorNode* input = output->parents[0].node.get();
```

> The graph walk also follows these records now. We only follow the node pointer here; the strides belong to the operation that calculates the gradients.

Location: `main.cpp`.

<!-- edit: topology-parent file: main.cpp -->
**Before**
```cpp
    for (const auto& parent : node->parents) {
      build_topology(parent.get(), visited, topology);
    }
```

**After**
```cpp
    for (const auto& parent : node->parents) {
      build_topology(parent.node.get(), visited, topology);
    }
```

<!-- checkpoint: parent-mapping-complete -->

Compile checkpoint, without replaying the training log on camera:

```sh
clang++ -std=c++23 -O2 main.cpp -o main
```

## B. Let construction finish the node

> The inputs and their mappings are together, but we’re still adding them after constructing the result. The node owns this information, so its constructor should receive it along with the shape and data.

Open `TensorNode` and the current `Tensor` constructor beside it. Move the existing validation; do not invent a second version. The next two edits belong together and are not a runnable midpoint.

Location: `main.cpp`.

<!-- edit: node-constructor file: main.cpp -->
**Before**
```cpp
struct TensorNode {
  std::vector<std::size_t> shape;
  std::vector<double> data;
  std::vector<double> grad;

  Operation operation = Operation::leaf;
  std::vector<Parent> parents;
};
```

**After**
```cpp
struct TensorNode {
  TensorNode(std::vector<std::size_t> shape,
                                std::vector<double> data, Operation operation = Operation::leaf,
                                std::vector<Parent> parents = {})
      : shape(std::move(shape)), data(std::move(data)),
        grad(this->data.size(), 0.0), operation(operation),
        parents(std::move(parents)) {
    std::size_t expected_elements;

    bool has_zero_dims = false;

    for (const std::size_t dimension : this->shape) {
      if (dimension == 0) {
        has_zero_dims = true;
        expected_elements = 0;
        break;
      }
    }

    if (!has_zero_dims) {
      expected_elements = 1;
      for (const std::size_t dimension : this->shape) {
        if (expected_elements > std::numeric_limits<std::size_t>::max() / dimension) {
          throw std::overflow_error("tensor element count overflows size_t");
        }

        expected_elements *= dimension;
      }
    }

    if (expected_elements != this->data.size()) {
      throw std::invalid_argument("tensor shape does not match its data");
    }
  }

  std::vector<std::size_t> shape;
  std::vector<double> data;
  std::vector<double> grad;

  Operation operation;
  std::vector<Parent> parents;
};
```

While writing the initializer list:

> Shape and data move into the node. Its gradient vector gets one zero for every stored value. The operation defaults to leaf and the parent list defaults to empty, so ordinary inputs need no graph arguments.

Point to `this->data`, then the member declarations.

> Here, data names the parameter; this arrow data names the stored member. We declare data before grad, so the gradient size comes from the vector we’ve already moved into the node. The shape checks below stay the same.

> Tensor can now pass shape and data straight to that constructor. This keeps the public call unchanged while giving the node responsibility for checking and initializing its storage.

Location: `main.cpp`.

<!-- edit: leaf-construction file: main.cpp -->
**Before**
```cpp
  Tensor(
    std::vector<std::size_t> shape,
    std::vector<double> data
  ) : node_(std::make_shared<TensorNode>()) {
    node_->shape = std::move(shape);
    node_->data = std::move(data);
    std::size_t expected_elements;

    bool has_zero_dims = false;

    for (const std::size_t dimension: node_->shape) {
      if (dimension == 0) {
        has_zero_dims = true;
        expected_elements = 0;
        break;
      }
    }

    if (!has_zero_dims) {
      expected_elements = 1;
      for (const std::size_t dimension: node_->shape) {
        if (expected_elements > std::numeric_limits<std::size_t>::max() / dimension) {
          throw std::overflow_error("tensor element count overflows size_t");
        }

        expected_elements *= dimension;
      }
    }

    if (expected_elements != node_->data.size()) {
      throw std::invalid_argument("tensor shape does not match its data");
    }
    node_->grad.assign(numel(), 0.0);
  }
```

**After**
```cpp
  Tensor(
    std::vector<std::size_t> shape,
    std::vector<double> data
  ) : node_(std::make_shared<TensorNode>(
        std::move(shape), std::move(data)
      )) {}
```

<!-- checkpoint: node-constructor-complete -->

> For an operation, we’ll supply its history too. We need one private Tensor constructor to hold the completed node. Keeping it private means callers still work with tensors, not graph internals.

Location: `main.cpp`.

<!-- edit: private-node-handle file: main.cpp -->
**Before**
```cpp
private:
  std::shared_ptr<TensorNode> node_;
```

**After**
```cpp
private:
  explicit Tensor(std::shared_ptr<TensorNode> node)
    : node_(std::move(node)) {
    if (!node_) {
      throw std::invalid_argument("tensor requires a non-null node");
    }
  }

  std::shared_ptr<TensorNode> node_;
```

> Let’s use it in sum first. We have one scalar result and one input. We’ll construct the node with both, then return a Tensor holding it. There’s nothing left to attach afterward.

Location: `main.cpp`.

<!-- edit: complete-sum-node file: main.cpp -->
**Before**
```cpp
    Tensor output({}, {result});

    output.node_->operation = Operation::sum;
    output.node_->parents = {{node_, {}}};

    return output;
```

**After**
```cpp
    return Tensor(std::make_shared<TensorNode>(
      std::vector<std::size_t>{},
      std::vector<double>{result},
      Operation::sum,
      std::vector<Parent>{{node_, {}}}
    ));
```

> Elementwise arithmetic also needs the broadcast mappings. They go inside the two parent entries, so the node constructor still takes just shape, data, operation and parents.

Location: `main.cpp`.

<!-- edit: complete-binary-node file: main.cpp -->
**Before**
```cpp
    Tensor result(std::move(result_shape), std::move(result_data));

    result.node_->operation = kind;
    result.node_->parents = {
      {node_, std::move(left_strides)},
      {other.node_, std::move(right_strides)}
    };

    return result;
```

**After**
```cpp
    return Tensor(std::make_shared<TensorNode>(
      std::move(result_shape),
      std::move(result_data),
      kind,
      std::vector<Parent>{
        {node_, std::move(left_strides)},
        {other.node_, std::move(right_strides)}
      }
    ));
```

> The remaining result builders use the same constructor. A unary operation and a column sum each pass one parent. Matrix multiplication passes two, without broadcast strides.

Location: `main.cpp`.

<!-- edit: complete-unary-node file: main.cpp -->
**Before**
```cpp
    Tensor result(node_->shape, std::move(result_data));
    result.node_->operation = kind;
    result.node_->parents = {{node_, {}}};
    return result;
```

**After**
```cpp
    return Tensor(std::make_shared<TensorNode>(
      node_->shape, std::move(result_data), kind,
      std::vector<Parent>{{node_, {}}}
    ));
```

Location: `main.cpp`.

<!-- edit: complete-column-sum-node file: main.cpp -->
**Before**
```cpp
    Tensor result({rows, 1}, std::move(totals));
    result.node_->operation = Operation::sum_columns;
    result.node_->parents = {{node_, {}}};
    return result;
```

**After**
```cpp
    return Tensor(std::make_shared<TensorNode>(
      std::vector<std::size_t>{rows, 1}, std::move(totals),
      Operation::sum_columns, std::vector<Parent>{{node_, {}}}
    ));
```

Location: `main.cpp`.

<!-- edit: movable-matmul-shape file: main.cpp -->
**Before**
```cpp
    const std::vector<std::size_t> result_shape{
      left_rows,
      right_cols
    };
```

**After**
```cpp
    std::vector<std::size_t> result_shape{
      left_rows,
      right_cols
    };
```

At `result_shape`, remove `const` so moving the vector can transfer its storage.

Location: `main.cpp`.

<!-- edit: complete-matmul-node file: main.cpp -->
**Before**
```cpp
    Tensor result(
      std::move(result_shape),
      std::move(result_data)
    );

    result.node_->operation = Operation::matmul;
    result.node_->parents = {{node_, {}}, {other.node_, {}}};

    return result;
```

**After**
```cpp
    return Tensor(std::make_shared<TensorNode>(
      std::move(result_shape), std::move(result_data),
      Operation::matmul, std::vector<Parent>{{node_, {}}, {other.node_, {}}}
    ));
```

<!-- checkpoint: logical-migration-complete -->

> Every result now leaves construction with its history attached. We haven’t changed the calculations, so the existing assertions and training should still give the same answers. Let’s check that before moving any files.

```sh
clang++ -std=c++23 -O2 main.cpp -o main
./main
```

Keep the start and final result in the edit; do not narrate a training wait. Expected local reference:

```text
Test accuracy: 88.2% (1764/2000)
Success!
```

Use the actual run if compiler or platform differences change the result.

## C. Separate the library without changing the calculations

> With the graph changes working, we can separate the files without changing their behavior at the same time. Training code needs the Tensor interface, but it doesn’t need to see its graph storage or the implementation of every operation.

Create `include/dlatwd`, `src`, `examples`, and `tests`. Keep `main.cpp` open as the source of the moves. C1-C4 form one file-split checkpoint; do not compile between incomplete moves.

> The public declarations will live under include. The operation labels and parent records stay under src because only the implementation uses them. I’ll put the library in the dlatwd namespace to keep its names separate from the application.

### C1. Move the graph types and separate the Tensor interface

<details>
<summary>Exact code: remove-graph-types-from-main</summary>

Location: `main.cpp`.

<!-- edit: remove-graph-types-from-main file: main.cpp -->
**Before**
```cpp
enum class Operation {
  leaf,
  add,
  subtract,
  multiply,
  divide,
  sum,
  matmul,
  relu,
  sigmoid,
  tanh,
  exp,
  sum_columns,
  log
};

struct TensorNode;

struct Parent {
  std::shared_ptr<TensorNode> node;
  std::vector<std::size_t> broadcast_strides;
};

struct TensorNode {
  TensorNode(std::vector<std::size_t> shape,
                                std::vector<double> data, Operation operation = Operation::leaf,
                                std::vector<Parent> parents = {})
      : shape(std::move(shape)), data(std::move(data)),
        grad(this->data.size(), 0.0), operation(operation),
        parents(std::move(parents)) {
    std::size_t expected_elements;

    bool has_zero_dims = false;

    for (const std::size_t dimension : this->shape) {
      if (dimension == 0) {
        has_zero_dims = true;
        expected_elements = 0;
        break;
      }
    }

    if (!has_zero_dims) {
      expected_elements = 1;
      for (const std::size_t dimension : this->shape) {
        if (expected_elements > std::numeric_limits<std::size_t>::max() / dimension) {
          throw std::overflow_error("tensor element count overflows size_t");
        }

        expected_elements *= dimension;
      }
    }

    if (expected_elements != this->data.size()) {
      throw std::invalid_argument("tensor shape does not match its data");
    }
  }

  std::vector<std::size_t> shape;
  std::vector<double> data;
  std::vector<double> grad;

  Operation operation;
  std::vector<Parent> parents;
};



```

**After**
```cpp

```

</details>

<details>
<summary>Exact code: src-tensor_node-hpp</summary>

Location: `src/tensor_node.hpp`.

<!-- edit: src-tensor_node-hpp file: src/tensor_node.hpp -->
**Before**
```cpp

```

**After**
```cpp
#pragma once
#include <cstddef>
#include <memory>
#include <vector>

namespace dlatwd::detail {
enum class Operation {
  leaf,
  add,
  subtract,
  multiply,
  divide,
  sum,
  matmul,
  relu,
  sigmoid,
  tanh,
  exp,
  sum_columns,
  log
};

struct TensorNode;

struct Parent {
  std::shared_ptr<TensorNode> node;
  // Output-coordinate mapping for elementwise broadcasting; empty otherwise.
  std::vector<std::size_t> broadcast_strides;
};

struct TensorNode {
  TensorNode(std::vector<std::size_t> shape, std::vector<double> data,
             Operation operation = Operation::leaf,
             std::vector<Parent> parents = {});

  std::vector<std::size_t> shape;
  std::vector<double> data;
  std::vector<double> grad;

  Operation operation;
  std::vector<Parent> parents;
};

}  // namespace dlatwd::detail
```

</details>

The node constructor body moves into `src/tensor.cpp` below. Its declaration stays with the struct. Keep member order unchanged: shape, data, grad, operation, parents.

<details>
<summary>Exact code: remove-tensor-from-main</summary>

Location: `main.cpp`.

<!-- edit: remove-tensor-from-main file: main.cpp -->
**Before**
```cpp
class Tensor {
public:
  Tensor(
    std::vector<std::size_t> shape,
    std::vector<double> data
  ) : node_(std::make_shared<TensorNode>(
        std::move(shape), std::move(data)
      )) {}
  
  [[nodiscard]] const std::vector<std::size_t>& shape() const noexcept {
    return node_->shape;
  }

  [[nodiscard]] const std::vector<double>& data() const noexcept {
    return node_->data;
  }

  [[nodiscard]] std::vector<double>& data() noexcept {
    return node_->data;
  }

  [[nodiscard]] const std::vector<double>& grad() const noexcept {
    return node_->grad;
  }

  void zero_grad() {
    std::fill(node_->grad.begin(), node_->grad.end(), 0.0);
  }

  [[nodiscard]] Tensor log() const {
    return elementwise_unary(
      Operation::log,
      [](double value) {
        if (!std::isfinite(value) || value <= 0.0) {
          throw std::domain_error("log requires a positive finite value");
        }
        return std::log(value);
      }
    );
  }

  [[nodiscard]] Tensor sum_columns() const {
    const std::size_t rows = dimension(0);
    const std::size_t cols = dimension(1);

    std::vector<double> totals(rows, 0.0);

    for (std::size_t row = 0; row < rows; ++row) {
      for (std::size_t col = 0; col < cols; ++col) {
        totals[row] += at({row, col});
      }
    }

    return Tensor(std::make_shared<TensorNode>(
      std::vector<std::size_t>{rows, 1}, std::move(totals),
      Operation::sum_columns, std::vector<Parent>{{node_, {}}}
    ));
  }

  [[nodiscard]] Tensor exp() const {
    return elementwise_unary(
      Operation::exp,
      [](double value) {
        return std::exp(value);
      }
    );
  }

  void backward() {
    if (rank() != 0) {
      throw std::invalid_argument("backward requires a scalar loss");
    }

    std::unordered_set<TensorNode*> visited;
    std::vector<TensorNode*> topology;
    build_topology(node_.get(), visited, topology);

    for (TensorNode* node: topology) {
      if (node->operation != Operation::leaf) {
        std::fill(node->grad.begin(), node->grad.end(), 0.0);
      }
    }

    node_->grad[0] = 1.0;

    for (auto it = topology.rbegin(); it != topology.rend(); ++it) {
      TensorNode* output = *it;
      switch (output->operation) {
        case Operation::leaf:
          break;

        case Operation::log: {
          backward_unary(
            output,
            [](double input, double) {
              return 1.0 / input;
            }
          );
          break;
        }

        case Operation::sum_columns: {
          TensorNode* input = output->parents[0].node.get();
          const std::size_t rows = input->shape[0];
          const std::size_t cols = input->shape[1];

          for (std::size_t row = 0; row < rows; ++row) {
            for (std::size_t col = 0; col < cols; ++col) {
              std::size_t index = row * cols + col;
              input->grad[index] += output->grad[row];
            }
          }
          break;
        }

        case Operation::exp:
          backward_unary(
            output,
            [](double, double result) {
              return result;
            }
          );
          break;

        case Operation::add:
          backward_elementwise(
            output,
            [](double, double) {
              return std::pair{1.0, 1.0};
            }
          );
          break;

        case Operation::subtract:
          backward_elementwise(
            output,
            [](double, double) {
              return std::pair{1.0, -1.0};
            }
          );
          break;

        case Operation::multiply:
          backward_elementwise(
            output,
            [](double left, double right) {
              return std::pair{right, left};
            }
          );
          break;

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

        case Operation::matmul: {
          TensorNode* left = output->parents[0].node.get();
          TensorNode* right = output->parents[1].node.get();

          const std::size_t left_rows = left->shape[0];
          const std::size_t left_cols = left->shape[1];
          const std::size_t right_cols = right->shape[1];

          for (std::size_t row = 0; row < left_rows; ++row) {
            for (std::size_t col = 0; col < right_cols; ++col) {
              const std::size_t output_index = row * right_cols + col;

              for (std::size_t index = 0; index < left_cols; ++index) {
                const std::size_t left_index = row * left_cols + index;
                const std::size_t right_index = index * right_cols + col;

                left->grad[left_index] += output->grad[output_index] * right->data[right_index];

                right->grad[right_index] += output->grad[output_index] * left->data[left_index];
              }
            }
          }

          break;
        }

        case Operation::sum: {
          TensorNode* input = output->parents[0].node.get();
          for (double& gradient : input->grad) {
            gradient += output->grad[0];
          }

          break;
        }

        case Operation::relu: {
          backward_unary(
            output,
            [](double input, double) {
              return input > 0.0 ? 1.0 : 0.0;
            }
          );
          break;
        }

        case Operation::sigmoid: {
          backward_unary(
            output, 
            [](double, double result) {
              return result * (1.0 - result);
            }
          );
          break;
        }

        case Operation::tanh: {
          backward_unary(
            output,
            [](double, double result) {
              return 1.0 - result * result;
            }
          );
          break;
        }

        default:
          throw std::logic_error("backward rule not implemented yet");
      
      }
    }

  }

  [[nodiscard]] std::size_t rank() const noexcept {
    return node_->shape.size();
  }

  [[nodiscard]] std::size_t numel() const noexcept {
    return node_->data.size();
  }

  [[nodiscard]] std::size_t dimension(const std::size_t axis) const {
    if (axis >= rank()) {
      throw std::out_of_range("tensor axis is outside its rank");
    }
    return node_->shape[axis];
  }

  double& at(const std::vector<std::size_t>& idx) {
    return node_->data[flat_index(idx)];
  }

  [[nodiscard]] double at(const std::vector<std::size_t>& idx) const {
    return node_->data[flat_index(idx)];
  }

  [[nodiscard]] Tensor sum() const {
    double result = 0.0;
    for (const double value: node_->data) {
      result += value;
    }

    return Tensor(std::make_shared<TensorNode>(
      std::vector<std::size_t>{},
      std::vector<double>{result},
      Operation::sum,
      std::vector<Parent>{{node_, {}}}
    ));
  }

  [[nodiscard]] Tensor relu() const {
    return elementwise_unary(
      Operation::relu,
      [](double value) {
        return std::max(0.0, value);
      }
    );
  }

  [[nodiscard]] Tensor sigmoid() const {
    return elementwise_unary(
      Operation::sigmoid, 
      [](double value) {
        return 1.0 / (1.0 + std::exp(-value));
      }
    );
  }

  [[nodiscard]] Tensor tanh() const {
    return elementwise_unary(
      Operation::tanh,
      [](double value) {
        return std::tanh(value);
      }
    );
  }

  [[nodiscard]] Tensor mean() const {
    if (numel() == 0) {
      throw std::invalid_argument(
        "mean is undefined for an empty tensor"
      );
    }

    return sum() / Tensor({}, {static_cast<double>(numel())});
  }

  [[nodiscard]] Tensor dot(const Tensor& other) const {
    if (rank() != 1 || other.rank() != 1) {
      throw std::invalid_argument("dot requires two rank-one tensors");
    }

    if (node_->shape != other.node_->shape) {
      throw std::invalid_argument("dot requires vectors of equal length");
    }

    // TODO: (performance): Benchmark a fused dot-product kernel that avoids
    // allocating and traversing an intermediate product tensor.

    return (*this * other).sum();
  }

  [[nodiscard]] Tensor operator+(const Tensor& other) const {
    return elementwise_binary(
      other,
      Operation::add,
      [](const double left, const double right) {
        return left + right;
      }
    );
  }

  [[nodiscard]] Tensor operator-(const Tensor& other) const {
    return elementwise_binary(
      other,
      Operation::subtract,
      [](const double left, const double right) {
        return left - right;
      }
    );
  }

  [[nodiscard]] Tensor operator*(const Tensor& other) const {
    return elementwise_binary(
      other,
      Operation::multiply,
      [](const double left, const double right) {
        return left * right;
      }
    );
  }

  [[nodiscard]] Tensor operator/(const Tensor& other) const {
    return elementwise_binary(
      other,
      Operation::divide,
      [](const double left, const double right) {
        if (right == 0.0) {
          throw std::domain_error("division by zero");
        }
        return left / right;
      }
    );
  }

  [[nodiscard]] Tensor matmul(const Tensor& other) const {
    if (rank() != 2 || other.rank() != 2) {
      throw std::invalid_argument("matmul requires two rank-two tensors");
    }

    const std::size_t left_rows = node_->shape[0];
    const std::size_t left_cols = node_->shape[1];
    const std::size_t right_rows = other.node_->shape[0];
    const std::size_t right_cols = other.node_->shape[1];

    if (left_cols != right_rows) {
      throw std::invalid_argument("matmul inner dimensions must match");
    }

    std::vector<std::size_t> result_shape{
      left_rows,
      right_cols
    };

    std::vector<double> result_data(
      left_rows * right_cols,
      0.0
    );

    for (std::size_t row = 0; row < left_rows; ++row) {
      for (std::size_t col = 0; col < right_cols; ++col) {
        double sum = 0.0;
        for (std::size_t index = 0; index < left_cols; ++index) {
          sum += 
            node_->data[row * left_cols + index] * 
            other.node_->data[index * right_cols + col];
        }
        result_data[row * right_cols + col] = sum;
      }
    }

    return Tensor(std::make_shared<TensorNode>(
      std::move(result_shape), std::move(result_data),
      Operation::matmul, std::vector<Parent>{{node_, {}}, {other.node_, {}}}
    ));
  }


private:
  explicit Tensor(std::shared_ptr<TensorNode> node)
    : node_(std::move(node)) {
    if (!node_) {
      throw std::invalid_argument("tensor requires a non-null node");
    }
  }

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
      build_topology(parent.node.get(), visited, topology);
    }

    topology.push_back(node);
  }

  static void backward_elementwise(
    TensorNode* output,
    const auto& local_derivatives
  ) {
    TensorNode* left = output->parents[0].node.get();
    TensorNode* right = output->parents[1].node.get();

    std::vector<std::size_t> coordinate(output->shape.size(), 0);

    for (std::size_t flat = 0; flat < output->data.size(); ++flat) {
      const std::size_t left_index = stride_offset(coordinate, output->parents[0].broadcast_strides);
      const std::size_t right_index = stride_offset(coordinate, output->parents[1].broadcast_strides);

      const double gradient = output->grad[flat];

      const auto [left_derivative, right_derivative] = 
        local_derivatives(left->data[left_index], right->data[right_index]);

      left->grad[left_index] += gradient * left_derivative;
      right->grad[right_index] += gradient * right_derivative;
        
      advance_coordinate(coordinate, output->shape);


    }

  }

  static void backward_unary(
    TensorNode* output,
    const auto& local_derivative
  ) {
    TensorNode* input = output->parents[0].node.get();

    for (std::size_t index = 0; index < output->data.size(); ++index) {
      input->grad[index] +=
        output->grad[index] *
        local_derivative(input->data[index], output->data[index]);
    }

  }


  [[nodiscard]] Tensor elementwise_binary(
    const Tensor& other,
    Operation kind,
    const auto& operation
  ) const {

    std::vector<std::size_t> result_shape = broadcast_shape(
      node_->shape, other.node_->shape
    );

    std::vector<std::size_t> left_strides = effective_strides(
      node_->shape, strides(), result_shape.size()
    );

    std::vector<std::size_t> right_strides = effective_strides(
      other.node_->shape, other.strides(), result_shape.size()
    );

    std::size_t result_numel = 1;
    for (const std::size_t dim: result_shape) {
      result_numel *= dim;
    }

    std::vector<double> result_data(result_numel);
    std::vector<std::size_t> coordinate(result_shape.size(), 0);

    for (std::size_t flat = 0; flat < result_numel; ++flat) {
      const std::size_t left_index = stride_offset(coordinate, left_strides);
      const std::size_t right_index = stride_offset(coordinate, right_strides);

      result_data[flat] = operation(node_->data[left_index], other.node_->data[right_index]);
      advance_coordinate(coordinate, result_shape);
    }

    return Tensor(std::make_shared<TensorNode>(
      std::move(result_shape),
      std::move(result_data),
      kind,
      std::vector<Parent>{
        {node_, std::move(left_strides)},
        {other.node_, std::move(right_strides)}
      }
    ));
  }

  [[nodiscard]] Tensor elementwise_unary(
    Operation kind,
    const auto& operation
  ) const {
    std::vector<double> result_data(numel());
    std::transform(
      node_->data.begin(),
      node_->data.end(),
      result_data.begin(),
      operation
    );
    return Tensor(std::make_shared<TensorNode>(
      node_->shape, std::move(result_data), kind,
      std::vector<Parent>{{node_, {}}}
    ));
  }

  [[nodiscard]] static std::size_t stride_offset(
    const std::vector<std::size_t>& coordinate,
    const std::vector<std::size_t>& effective_strides
  ) {
    std::size_t index = 0;
    for (std::size_t axis = 0; axis < coordinate.size(); ++axis) {
      index += coordinate[axis] * effective_strides[axis];
    }
    return index;
  }

  static void advance_coordinate(
    std::vector<std::size_t>& coordinate,
    const std::vector<std::size_t>& shape
  ) {
    for (std::size_t axis = coordinate.size(); axis-- > 0;) {
      if (++coordinate[axis] < shape[axis]) {
        return;
      }
      coordinate[axis] = 0;
    }
  }

  [[nodiscard]] std::vector<std::size_t> strides() const {
    std::vector<std::size_t> result(node_->shape.size());
    std::size_t stride = 1;

    for (std::size_t axis = rank(); axis-- > 0;) {
      result[axis] = stride;
      stride *= node_->shape[axis];
    }

    return result;
  }

  [[nodiscard]] static std::vector<std::size_t> broadcast_shape(
    const std::vector<std::size_t>& left,
    const std::vector<std::size_t>& right
  ) {

    const std::size_t rank = std::max(left.size(), right.size());
    std::vector<std::size_t> result(rank);

    const std::size_t left_offset = rank - left.size();
    const std::size_t right_offset = rank - right.size();

    for (std::size_t axis = 0; axis < rank; ++axis) {
      const bool left_has_axis = axis >= left_offset;
      const bool right_has_axis = axis >= right_offset;

      std::size_t left_dim = 1;
      if (left_has_axis) {
        const std::size_t left_axis = axis - left_offset;
        left_dim = left[left_axis];
      }

      std::size_t right_dim = 1;
      if (right_has_axis) {
        const std::size_t right_axis = axis - right_offset;
        right_dim = right[right_axis];
      }

      const bool sizes_match = left_dim == right_dim;
      const bool left_can_stretch = left_dim == 1;
      const bool right_can_stretch = right_dim == 1;

      if (!sizes_match && !left_can_stretch && !right_can_stretch) {
        throw std::invalid_argument(
          "cannot broadcast - shape mismatch at dimension " + std::to_string(axis)
        );
      }
      result[axis] = std::max(left_dim, right_dim);
    }

    return result;
  }

  [[nodiscard]] static std::vector<std::size_t> effective_strides(
    const std::vector<std::size_t>& shape,
    const std::vector<std::size_t>& own_strides,
    const std::size_t target_rank
  ) {
    std::vector<std::size_t> result(target_rank, 0);
    const std::size_t offset = target_rank - shape.size();

    for (std::size_t axis = 0; axis < shape.size(); ++axis) {
      if (shape[axis] != 1) {
        result[offset + axis] = own_strides[axis];
      }
    }

    return result;
    
  }

  [[nodiscard]] std::size_t flat_index(const std::vector<std::size_t>& idx) const {
    if (idx.size() != rank()) {
      throw std::invalid_argument("number of indices must match tensor rank");
    }

    for (std::size_t axis = 0; axis < rank(); ++axis) {
      if (idx[axis] >= node_->shape[axis]) {
        throw std::out_of_range("tensor index is outside its dimension");
      }
    }

    std::size_t flat_index = 0;
    std::size_t stride = 1;

    for (std::size_t axis = rank(); axis > 0; --axis) {
      const std::size_t current_axis = axis - 1;
      flat_index += idx[current_axis] * stride;
      stride *= node_->shape[current_axis];
    }

    return flat_index;
  }

};
```

**After**
```cpp

```

</details>

<details>
<summary>Exact code: include-dlatwd-tensor-hpp</summary>

Location: `include/dlatwd/tensor.hpp`.

<!-- edit: include-dlatwd-tensor-hpp file: include/dlatwd/tensor.hpp -->
**Before**
```cpp

```

**After**
```cpp
#pragma once

#include <cstddef>
#include <memory>
#include <unordered_set>
#include <vector>

namespace dlatwd {
namespace detail {
struct TensorNode;
enum class Operation;
}  // namespace detail

class Tensor {
  using TensorNode = detail::TensorNode;
  using Operation = detail::Operation;

 public:
  Tensor(std::vector<std::size_t> shape, std::vector<double> data);

  // Shape and size
  [[nodiscard]] const std::vector<std::size_t>& shape() const noexcept;
  [[nodiscard]] std::size_t rank() const noexcept;
  [[nodiscard]] std::size_t numel() const noexcept;
  [[nodiscard]] std::size_t dimension(const std::size_t axis) const;

  // Storage and element access
  [[nodiscard]] const std::vector<double>& data() const noexcept;
  [[nodiscard]] std::vector<double>& data() noexcept;
  [[nodiscard]] double at(const std::vector<std::size_t>& idx) const;
  double& at(const std::vector<std::size_t>& idx);

  // Elementwise arithmetic
  [[nodiscard]] Tensor operator+(const Tensor& other) const;
  [[nodiscard]] Tensor operator-(const Tensor& other) const;
  [[nodiscard]] Tensor operator*(const Tensor& other) const;
  [[nodiscard]] Tensor operator/(const Tensor& other) const;

  // Reductions and linear algebra
  [[nodiscard]] Tensor sum() const;
  [[nodiscard]] Tensor mean() const;
  [[nodiscard]] Tensor sum_columns() const;
  [[nodiscard]] Tensor dot(const Tensor& other) const;
  [[nodiscard]] Tensor matmul(const Tensor& other) const;

  // Elementwise functions and activations
  [[nodiscard]] Tensor exp() const;
  [[nodiscard]] Tensor log() const;
  [[nodiscard]] Tensor relu() const;
  [[nodiscard]] Tensor sigmoid() const;
  [[nodiscard]] Tensor tanh() const;

  // Automatic differentiation
  [[nodiscard]] const std::vector<double>& grad() const noexcept;
  void zero_grad();
  void backward();

 private:
  explicit Tensor(std::shared_ptr<TensorNode> node);

  std::shared_ptr<TensorNode> node_;

  // Indexing and coordinate traversal
  [[nodiscard]] std::size_t flat_index(const std::vector<std::size_t>& idx) const;
  [[nodiscard]] std::vector<std::size_t> strides() const;
  [[nodiscard]] static std::size_t stride_offset(
      const std::vector<std::size_t>& coordinate,
      const std::vector<std::size_t>& effective_strides);

  static void advance_coordinate(std::vector<std::size_t>& coordinate,
                                 const std::vector<std::size_t>& shape);

  // Broadcasting
  [[nodiscard]] static std::vector<std::size_t> broadcast_shape(
      const std::vector<std::size_t>& left, const std::vector<std::size_t>& right);

  [[nodiscard]] static std::vector<std::size_t> effective_strides(
      const std::vector<std::size_t>& shape,
      const std::vector<std::size_t>& own_strides, const std::size_t target_rank);

  // Forward operation helpers
  [[nodiscard]] Tensor elementwise_binary(const Tensor& other, Operation kind,
                                          const auto& operation) const;
  [[nodiscard]] Tensor elementwise_unary(Operation kind, const auto& operation) const;

  // Graph traversal and gradient propagation
  static void build_topology(TensorNode* node, std::unordered_set<TensorNode*>& visited,
                             std::vector<TensorNode*>& topology);
  static void backward_elementwise(TensorNode* output, const auto& local_derivatives);
  static void backward_unary(TensorNode* output, const auto& local_derivative);
};

}  // namespace dlatwd
```

</details>

> The header groups the operations we call: shape and storage, arithmetic, reductions, activations, then backward. Its private section holds the node pointer and helper declarations. A forward declaration is enough for the pointer; callers don’t need the node definition.

Before moving the remaining bodies, demonstrate this one declaration/definition split. This is a reference from the move above, not an additional edit.

**Before: inside the class**
```cpp
  [[nodiscard]] std::size_t rank() const noexcept {
    return node_->shape.size();
  }
```

**After: header declaration**
```cpp
  [[nodiscard]] std::size_t rank() const noexcept;
```

**After: source definition**
```cpp
std::size_t Tensor::rank() const noexcept { return node_->shape.size(); }
```

> The declaration keeps the signature. The body moves to the source file, where Tensor double-colon says which class it belongs to. Const and noexcept stay on both. We’re moving the implementation, not rewriting its math.

Use the complete destination below to move each remaining method into its named section. Retain the bodies; apply the shown class qualifiers and namespace. No method is omitted from this code panel.

<details>
<summary>Exact code: src-tensor-cpp</summary>

Location: `src/tensor.cpp`.

<!-- edit: src-tensor-cpp file: src/tensor.cpp -->
**Before**
```cpp

```

**After**
```cpp
#include "dlatwd/tensor.hpp"

#include <algorithm>
#include <cmath>
#include <limits>
#include <stdexcept>
#include <string>
#include <utility>

#include "tensor_node.hpp"

namespace dlatwd {
using detail::Operation;
using detail::TensorNode;

// Construction

Tensor::Tensor(std::vector<std::size_t> shape, std::vector<double> data)
    : Tensor(std::make_shared<TensorNode>(std::move(shape), std::move(data))) {}

Tensor::Tensor(std::shared_ptr<TensorNode> node) : node_(std::move(node)) {
  if (!node_) {
    throw std::invalid_argument("tensor requires a non-null node");
  }
}

detail::TensorNode::TensorNode(std::vector<std::size_t> shape,
                              std::vector<double> data, Operation operation,
                              std::vector<Parent> parents)
    : shape(std::move(shape)), data(std::move(data)),
      grad(this->data.size(), 0.0), operation(operation),
      parents(std::move(parents)) {
  std::size_t expected_elements;

  bool has_zero_dims = false;

  for (const std::size_t dimension : this->shape) {
    if (dimension == 0) {
      has_zero_dims = true;
      expected_elements = 0;
      break;
    }
  }

  if (!has_zero_dims) {
    expected_elements = 1;
    for (const std::size_t dimension : this->shape) {
      if (expected_elements > std::numeric_limits<std::size_t>::max() / dimension) {
        throw std::overflow_error("tensor element count overflows size_t");
      }

      expected_elements *= dimension;
    }
  }

  if (expected_elements != this->data.size()) {
    throw std::invalid_argument("tensor shape does not match its data");
  }
}

// Shape and size

const std::vector<std::size_t>& Tensor::shape() const noexcept { return node_->shape; }

std::size_t Tensor::rank() const noexcept { return node_->shape.size(); }

std::size_t Tensor::numel() const noexcept { return node_->data.size(); }

std::size_t Tensor::dimension(const std::size_t axis) const {
  if (axis >= rank()) {
    throw std::out_of_range("tensor axis is outside its rank");
  }
  return node_->shape[axis];
}

// Storage and element access

const std::vector<double>& Tensor::data() const noexcept { return node_->data; }

std::vector<double>& Tensor::data() noexcept { return node_->data; }

double Tensor::at(const std::vector<std::size_t>& idx) const {
  return node_->data[flat_index(idx)];
}

double& Tensor::at(const std::vector<std::size_t>& idx) {
  return node_->data[flat_index(idx)];
}

// Elementwise arithmetic

Tensor Tensor::elementwise_binary(const Tensor& other, Operation kind,
                                  const auto& operation) const {
  std::vector<std::size_t> result_shape =
      broadcast_shape(node_->shape, other.node_->shape);

  std::vector<std::size_t> left_strides =
      effective_strides(node_->shape, strides(), result_shape.size());

  std::vector<std::size_t> right_strides =
      effective_strides(other.node_->shape, other.strides(), result_shape.size());

  std::size_t result_numel = 1;
  for (const std::size_t dim : result_shape) {
    result_numel *= dim;
  }

  std::vector<double> result_data(result_numel);
  std::vector<std::size_t> coordinate(result_shape.size(), 0);

  for (std::size_t flat = 0; flat < result_numel; ++flat) {
    const std::size_t left_index = stride_offset(coordinate, left_strides);
    const std::size_t right_index = stride_offset(coordinate, right_strides);

    result_data[flat] =
        operation(node_->data[left_index], other.node_->data[right_index]);
    advance_coordinate(coordinate, result_shape);
  }

  return Tensor(std::make_shared<TensorNode>(
      std::move(result_shape), std::move(result_data), kind,
      std::vector<detail::Parent>{{node_, std::move(left_strides)},
                                  {other.node_, std::move(right_strides)}}));
}

Tensor Tensor::operator+(const Tensor& other) const {
  return elementwise_binary(
      other, Operation::add,
      [](const double left, const double right) { return left + right; });
}

Tensor Tensor::operator-(const Tensor& other) const {
  return elementwise_binary(
      other, Operation::subtract,
      [](const double left, const double right) { return left - right; });
}

Tensor Tensor::operator*(const Tensor& other) const {
  return elementwise_binary(
      other, Operation::multiply,
      [](const double left, const double right) { return left * right; });
}

Tensor Tensor::operator/(const Tensor& other) const {
  return elementwise_binary(other, Operation::divide,
                            [](const double left, const double right) {
                              if (right == 0.0) {
                                throw std::domain_error("division by zero");
                              }
                              return left / right;
                            });
}

// Reductions and linear algebra

Tensor Tensor::sum() const {
  double result = 0.0;
  for (const double value : node_->data) {
    result += value;
  }

  return Tensor(std::make_shared<TensorNode>(
      std::vector<std::size_t>{}, std::vector<double>{result}, Operation::sum,
      std::vector<detail::Parent>{{node_, {}}}));
}

Tensor Tensor::mean() const {
  if (numel() == 0) {
    throw std::invalid_argument("mean is undefined for an empty tensor");
  }

  return sum() / Tensor({}, {static_cast<double>(numel())});
}

Tensor Tensor::sum_columns() const {
  const std::size_t rows = dimension(0);
  const std::size_t cols = dimension(1);

  std::vector<double> totals(rows, 0.0);

  for (std::size_t row = 0; row < rows; ++row) {
    for (std::size_t col = 0; col < cols; ++col) {
      totals[row] += at({row, col});
    }
  }

  return Tensor(std::make_shared<TensorNode>(
      std::vector<std::size_t>{rows, 1}, std::move(totals), Operation::sum_columns,
      std::vector<detail::Parent>{{node_, {}}}));
}

Tensor Tensor::dot(const Tensor& other) const {
  if (rank() != 1 || other.rank() != 1) {
    throw std::invalid_argument("dot requires two rank-one tensors");
  }

  if (node_->shape != other.node_->shape) {
    throw std::invalid_argument("dot requires vectors of equal length");
  }

  // TODO: (performance): Benchmark a fused dot-product kernel that avoids
  // allocating and traversing an intermediate product tensor.

  return (*this * other).sum();
}

Tensor Tensor::matmul(const Tensor& other) const {
  if (rank() != 2 || other.rank() != 2) {
    throw std::invalid_argument("matmul requires two rank-two tensors");
  }

  const std::size_t left_rows = node_->shape[0];
  const std::size_t left_cols = node_->shape[1];
  const std::size_t right_rows = other.node_->shape[0];
  const std::size_t right_cols = other.node_->shape[1];

  if (left_cols != right_rows) {
    throw std::invalid_argument("matmul inner dimensions must match");
  }

  std::vector<std::size_t> result_shape{left_rows, right_cols};

  std::vector<double> result_data(left_rows * right_cols, 0.0);

  for (std::size_t row = 0; row < left_rows; ++row) {
    for (std::size_t col = 0; col < right_cols; ++col) {
      double sum = 0.0;
      for (std::size_t index = 0; index < left_cols; ++index) {
        sum += node_->data[row * left_cols + index] *
               other.node_->data[index * right_cols + col];
      }
      result_data[row * right_cols + col] = sum;
    }
  }

  return Tensor(std::make_shared<TensorNode>(
      std::move(result_shape), std::move(result_data), Operation::matmul,
      std::vector<detail::Parent>{{node_, {}}, {other.node_, {}}}));
}

// Elementwise functions and activations

Tensor Tensor::elementwise_unary(Operation kind, const auto& operation) const {
  std::vector<double> result_data(numel());
  std::transform(node_->data.begin(), node_->data.end(), result_data.begin(),
                 operation);
  return Tensor(std::make_shared<TensorNode>(
      node_->shape, std::move(result_data), kind,
      std::vector<detail::Parent>{{node_, {}}}));
}

Tensor Tensor::exp() const {
  return elementwise_unary(Operation::exp,
                           [](double value) { return std::exp(value); });
}

Tensor Tensor::log() const {
  return elementwise_unary(Operation::log, [](double value) {
    if (!std::isfinite(value) || value <= 0.0) {
      throw std::domain_error("log requires a positive finite value");
    }
    return std::log(value);
  });
}

Tensor Tensor::relu() const {
  return elementwise_unary(Operation::relu,
                           [](double value) { return std::max(0.0, value); });
}

Tensor Tensor::sigmoid() const {
  return elementwise_unary(Operation::sigmoid,
                           [](double value) { return 1.0 / (1.0 + std::exp(-value)); });
}

Tensor Tensor::tanh() const {
  return elementwise_unary(Operation::tanh,
                           [](double value) { return std::tanh(value); });
}

// Automatic differentiation

const std::vector<double>& Tensor::grad() const noexcept { return node_->grad; }

void Tensor::zero_grad() { std::fill(node_->grad.begin(), node_->grad.end(), 0.0); }

void Tensor::backward_elementwise(TensorNode* output, const auto& local_derivatives) {
  TensorNode* left = output->parents[0].node.get();
  TensorNode* right = output->parents[1].node.get();

  std::vector<std::size_t> coordinate(output->shape.size(), 0);

  for (std::size_t flat = 0; flat < output->data.size(); ++flat) {
    const std::size_t left_index =
        stride_offset(coordinate, output->parents[0].broadcast_strides);
    const std::size_t right_index =
        stride_offset(coordinate, output->parents[1].broadcast_strides);

    const double gradient = output->grad[flat];

    const auto [left_derivative, right_derivative] =
        local_derivatives(left->data[left_index], right->data[right_index]);

    left->grad[left_index] += gradient * left_derivative;
    right->grad[right_index] += gradient * right_derivative;

    advance_coordinate(coordinate, output->shape);
  }
}

void Tensor::backward_unary(TensorNode* output, const auto& local_derivative) {
  TensorNode* input = output->parents[0].node.get();

  for (std::size_t index = 0; index < output->data.size(); ++index) {
    input->grad[index] +=
        output->grad[index] * local_derivative(input->data[index], output->data[index]);
  }
}

void Tensor::backward() {
  if (rank() != 0) {
    throw std::invalid_argument("backward requires a scalar loss");
  }

  std::unordered_set<TensorNode*> visited;
  std::vector<TensorNode*> topology;
  build_topology(node_.get(), visited, topology);

  for (TensorNode* node : topology) {
    if (node->operation != Operation::leaf) {
      std::fill(node->grad.begin(), node->grad.end(), 0.0);
    }
  }

  node_->grad[0] = 1.0;

  for (auto it = topology.rbegin(); it != topology.rend(); ++it) {
    TensorNode* output = *it;
    switch (output->operation) {
      case Operation::leaf:
        break;

      case Operation::log: {
        backward_unary(output, [](double input, double) { return 1.0 / input; });
        break;
      }

      case Operation::sum_columns: {
        TensorNode* input = output->parents[0].node.get();
        const std::size_t rows = input->shape[0];
        const std::size_t cols = input->shape[1];

        for (std::size_t row = 0; row < rows; ++row) {
          for (std::size_t col = 0; col < cols; ++col) {
            std::size_t index = row * cols + col;
            input->grad[index] += output->grad[row];
          }
        }
        break;
      }

      case Operation::exp:
        backward_unary(output, [](double, double result) { return result; });
        break;

      case Operation::add:
        backward_elementwise(output,
                             [](double, double) { return std::pair{1.0, 1.0}; });
        break;

      case Operation::subtract:
        backward_elementwise(output,
                             [](double, double) { return std::pair{1.0, -1.0}; });
        break;

      case Operation::multiply:
        backward_elementwise(
            output, [](double left, double right) { return std::pair{right, left}; });
        break;

      case Operation::divide:
        backward_elementwise(output, [](double numerator, double denominator) {
          return std::pair{1.0 / denominator, -numerator / (denominator * denominator)};
        });
        break;

      case Operation::matmul: {
        TensorNode* left = output->parents[0].node.get();
        TensorNode* right = output->parents[1].node.get();

        const std::size_t left_rows = left->shape[0];
        const std::size_t left_cols = left->shape[1];
        const std::size_t right_cols = right->shape[1];

        for (std::size_t row = 0; row < left_rows; ++row) {
          for (std::size_t col = 0; col < right_cols; ++col) {
            const std::size_t output_index = row * right_cols + col;

            for (std::size_t index = 0; index < left_cols; ++index) {
              const std::size_t left_index = row * left_cols + index;
              const std::size_t right_index = index * right_cols + col;

              left->grad[left_index] +=
                  output->grad[output_index] * right->data[right_index];

              right->grad[right_index] +=
                  output->grad[output_index] * left->data[left_index];
            }
          }
        }

        break;
      }

      case Operation::sum: {
        TensorNode* input = output->parents[0].node.get();
        for (double& gradient : input->grad) {
          gradient += output->grad[0];
        }

        break;
      }

      case Operation::relu: {
        backward_unary(output,
                       [](double input, double) { return input > 0.0 ? 1.0 : 0.0; });
        break;
      }

      case Operation::sigmoid: {
        backward_unary(output,
                       [](double, double result) { return result * (1.0 - result); });
        break;
      }

      case Operation::tanh: {
        backward_unary(output,
                       [](double, double result) { return 1.0 - result * result; });
        break;
      }

      default:
        throw std::logic_error("backward rule not implemented yet");
    }
  }
}

// Indexing and coordinate traversal

std::size_t Tensor::flat_index(const std::vector<std::size_t>& idx) const {
  if (idx.size() != rank()) {
    throw std::invalid_argument("number of indices must match tensor rank");
  }

  for (std::size_t axis = 0; axis < rank(); ++axis) {
    if (idx[axis] >= node_->shape[axis]) {
      throw std::out_of_range("tensor index is outside its dimension");
    }
  }

  std::size_t flat_index = 0;
  std::size_t stride = 1;

  for (std::size_t axis = rank(); axis > 0; --axis) {
    const std::size_t current_axis = axis - 1;
    flat_index += idx[current_axis] * stride;
    stride *= node_->shape[current_axis];
  }

  return flat_index;
}

std::vector<std::size_t> Tensor::strides() const {
  std::vector<std::size_t> result(node_->shape.size());
  std::size_t stride = 1;

  for (std::size_t axis = rank(); axis-- > 0;) {
    result[axis] = stride;
    stride *= node_->shape[axis];
  }

  return result;
}

std::size_t Tensor::stride_offset(const std::vector<std::size_t>& coordinate,
                                  const std::vector<std::size_t>& effective_strides) {
  std::size_t index = 0;
  for (std::size_t axis = 0; axis < coordinate.size(); ++axis) {
    index += coordinate[axis] * effective_strides[axis];
  }
  return index;
}

void Tensor::advance_coordinate(std::vector<std::size_t>& coordinate,
                                const std::vector<std::size_t>& shape) {
  for (std::size_t axis = coordinate.size(); axis-- > 0;) {
    if (++coordinate[axis] < shape[axis]) {
      return;
    }
    coordinate[axis] = 0;
  }
}

// Broadcasting

std::vector<std::size_t> Tensor::broadcast_shape(
    const std::vector<std::size_t>& left, const std::vector<std::size_t>& right) {
  const std::size_t rank = std::max(left.size(), right.size());
  std::vector<std::size_t> result(rank);

  const std::size_t left_offset = rank - left.size();
  const std::size_t right_offset = rank - right.size();

  for (std::size_t axis = 0; axis < rank; ++axis) {
    const bool left_has_axis = axis >= left_offset;
    const bool right_has_axis = axis >= right_offset;

    std::size_t left_dim = 1;
    if (left_has_axis) {
      const std::size_t left_axis = axis - left_offset;
      left_dim = left[left_axis];
    }

    std::size_t right_dim = 1;
    if (right_has_axis) {
      const std::size_t right_axis = axis - right_offset;
      right_dim = right[right_axis];
    }

    const bool sizes_match = left_dim == right_dim;
    const bool left_can_stretch = left_dim == 1;
    const bool right_can_stretch = right_dim == 1;

    if (!sizes_match && !left_can_stretch && !right_can_stretch) {
      throw std::invalid_argument("cannot broadcast - shape mismatch at dimension " +
                                  std::to_string(axis));
    }
    result[axis] = std::max(left_dim, right_dim);
  }

  return result;
}

std::vector<std::size_t> Tensor::effective_strides(
    const std::vector<std::size_t>& shape, const std::vector<std::size_t>& own_strides,
    const std::size_t target_rank) {
  std::vector<std::size_t> result(target_rank, 0);
  const std::size_t offset = target_rank - shape.size();

  for (std::size_t axis = 0; axis < shape.size(); ++axis) {
    if (shape[axis] != 1) {
      result[offset + axis] = own_strides[axis];
    }
  }

  return result;
}

// Graph traversal

void Tensor::build_topology(TensorNode* node, std::unordered_set<TensorNode*>& visited,
                            std::vector<TensorNode*>& topology) {
  if (!visited.insert(node).second) {
    return;
  }

  for (const auto& parent : node->parents) {
    build_topology(parent.node.get(), visited, topology);
  }

  topology.push_back(node);
}

}  // namespace dlatwd
```

</details>

> The helpers with auto parameters are templates. Their definitions must be available where they’re instantiated, so they stay in this source file before the methods that call them. None are part of the public interface.

### C2. Separate layers and losses

> Tensor no longer shares a file with training. We can give the layers and loss functions the same boundary: declarations for callers, implementations in the library.

<details>
<summary>Exact code: move-linear-out-of-main</summary>

Location: `main.cpp`.

<!-- edit: move-linear-out-of-main file: main.cpp -->
**Before**
```cpp
class Linear {
public:
  Linear(
    std::size_t in_features,
    std::size_t out_features,
    std::mt19937& random
  ): weight_(random_weights(in_features, out_features, random)),
     bias_({out_features}, std::vector<double>(out_features, 0.0)) {}

  [[nodiscard]] Tensor forward(const Tensor& inputs) const {
    return inputs.matmul(weight_) + bias_;
  }

  [[nodiscard]] std::vector<Tensor> parameters() const {
    return {weight_, bias_};
  }

private:
  Tensor weight_;
  Tensor bias_;

  [[nodiscard]] static Tensor random_weights(
    std::size_t in_features,
    std::size_t out_features,
    std::mt19937& random
  ) {
    const double limit = 1.0 / std::sqrt(static_cast<double>(in_features));
    std::uniform_real_distribution<double> distribution(-limit, limit);
    std::vector<double> values(in_features * out_features);
    for (double& value: values) {
      value = distribution(random);
    }
    return Tensor({in_features, out_features}, std::move(values));
  }
};
```

**After**
```cpp

```

</details>

<details>
<summary>Exact code: move-tanh-out-of-main</summary>

Location: `main.cpp`.

<!-- edit: move-tanh-out-of-main file: main.cpp -->
**Before**
```cpp
struct Tanh {
  [[nodiscard]] Tensor forward(const Tensor& inputs) const {
    return inputs.tanh();
  }
};
```

**After**
```cpp

```

</details>

<details>
<summary>Exact code: move-mlp-out-of-main</summary>

Location: `main.cpp`.

<!-- edit: move-mlp-out-of-main file: main.cpp -->
**Before**
```cpp
class MLP {
public:
  MLP(
    std::size_t in_features,
    std::size_t hidden_features,
    std::size_t out_features,
    std::mt19937& random
  ):
    hidden_(in_features, hidden_features, random),
    output_(hidden_features, out_features, random)
   {}

  [[nodiscard]] Tensor forward(const Tensor& inputs) const {
    const Tensor hidden = activation_.forward(
      hidden_.forward(inputs)
    );
    return output_.forward(hidden);
  }

  [[nodiscard]] std::vector<Tensor> parameters() {
    std::vector<Tensor> result = hidden_.parameters();
    const std::vector<Tensor> output = output_.parameters();
    result.insert(result.end(), output.begin(), output.end());
    return result;
  }

private:
  Linear hidden_;
  Tanh activation_;
  Linear output_;
};
```

**After**
```cpp

```

</details>

<details>
<summary>Exact code: move-gradient-step-out-of-main</summary>

Location: `main.cpp`.

<!-- edit: move-gradient-step-out-of-main file: main.cpp -->
**Before**
```cpp
void gradient_step(
  std::vector<Tensor>& parameters,
  double learning_rate
) {
  for(Tensor& parameter: parameters) {
    for (std::size_t index = 0; index < parameter.numel(); ++index) {
      parameter.data()[index] -= learning_rate * parameter.grad()[index];
    }
  }
}
```

**After**
```cpp

```

</details>

<details>
<summary>Exact code: include-dlatwd-nn-hpp</summary>

Location: `include/dlatwd/nn.hpp`.

<!-- edit: include-dlatwd-nn-hpp file: include/dlatwd/nn.hpp -->
**Before**
```cpp

```

**After**
```cpp
#pragma once
#include <random>

#include "dlatwd/tensor.hpp"

namespace dlatwd {
class Linear {
 public:
  Linear(std::size_t in_features, std::size_t out_features, std::mt19937& random);

  [[nodiscard]] Tensor forward(const Tensor& inputs) const;

  [[nodiscard]] std::vector<Tensor> parameters() const;

 private:
  Tensor weight_;

  Tensor bias_;

  [[nodiscard]] static Tensor random_weights(std::size_t in_features,
                                             std::size_t out_features,
                                             std::mt19937& random);
};

struct Tanh {
  [[nodiscard]] Tensor forward(const Tensor& inputs) const;
};

class MLP {
 public:
  MLP(std::size_t in_features, std::size_t hidden_features, std::size_t out_features,
      std::mt19937& random);

  [[nodiscard]] Tensor forward(const Tensor& inputs) const;

  [[nodiscard]] std::vector<Tensor> parameters();

 private:
  Linear hidden_;

  Tanh activation_;

  Linear output_;
};

void gradient_step(std::vector<Tensor>& parameters, double learning_rate);
}  // namespace dlatwd
```

</details>

<details>
<summary>Exact code: src-nn-cpp</summary>

Location: `src/nn.cpp`.

<!-- edit: src-nn-cpp file: src/nn.cpp -->
**Before**
```cpp

```

**After**
```cpp
#include "dlatwd/nn.hpp"

#include <cmath>
#include <utility>

namespace dlatwd {
Linear::Linear(std::size_t in_features, std::size_t out_features, std::mt19937& random)
    : weight_(random_weights(in_features, out_features, random)),
      bias_({out_features}, std::vector<double>(out_features, 0.0)) {}

Tensor Linear::forward(const Tensor& inputs) const {
  return inputs.matmul(weight_) + bias_;
}

std::vector<Tensor> Linear::parameters() const { return {weight_, bias_}; }

Tensor Linear::random_weights(std::size_t in_features, std::size_t out_features,
                              std::mt19937& random) {
  const double limit = 1.0 / std::sqrt(static_cast<double>(in_features));
  std::uniform_real_distribution<double> distribution(-limit, limit);
  std::vector<double> values(in_features * out_features);
  for (double& value : values) {
    value = distribution(random);
  }
  return Tensor({in_features, out_features}, std::move(values));
}

Tensor Tanh::forward(const Tensor& inputs) const { return inputs.tanh(); }

MLP::MLP(std::size_t in_features, std::size_t hidden_features, std::size_t out_features,
         std::mt19937& random)
    : hidden_(in_features, hidden_features, random),
      output_(hidden_features, out_features, random) {}

Tensor MLP::forward(const Tensor& inputs) const {
  const Tensor hidden = activation_.forward(hidden_.forward(inputs));
  return output_.forward(hidden);
}

std::vector<Tensor> MLP::parameters() {
  std::vector<Tensor> result = hidden_.parameters();
  const std::vector<Tensor> output = output_.parameters();
  result.insert(result.end(), output.begin(), output.end());
  return result;
}

void gradient_step(std::vector<Tensor>& parameters, double learning_rate) {
  for (Tensor& parameter : parameters) {
    for (std::size_t index = 0; index < parameter.numel(); ++index) {
      parameter.data()[index] -= learning_rate * parameter.grad()[index];
    }
  }
}
}  // namespace dlatwd
```

</details>

> Linear, Tanh and MLP keep their existing behavior. Gradient descent stays with the neural-network code. The loss functions depend on Tensor, so they get their own header without pulling in the layers.

<details>
<summary>Exact code: move-mse-loss-out-of-main</summary>

Location: `main.cpp`.

<!-- edit: move-mse-loss-out-of-main file: main.cpp -->
**Before**
```cpp
[[nodiscard]] Tensor mse_loss(
  const Tensor& prediction,
  const Tensor& target
) {
  if (prediction.shape() != target.shape()) {
    throw std::invalid_argument("mse loss requires equal shapes");
  }

  Tensor residual = prediction - target;
  return (residual * residual).mean();
}
```

**After**
```cpp

```

</details>

<details>
<summary>Exact code: move-cross-entropy-loss-out-of-main</summary>

Location: `main.cpp`.

<!-- edit: move-cross-entropy-loss-out-of-main file: main.cpp -->
**Before**
```cpp
[[nodiscard]] Tensor cross_entropy_loss(
  const Tensor& probabilities,
  const std::vector<std::size_t>& labels
) {
  Tensor targets(
    probabilities.shape(),
    std::vector<double>(probabilities.numel(), 0.0)
  );
  for (std::size_t row = 0; row < labels.size(); ++row) {
    targets.at({row, labels[row]}) = 1.0;
  }
  const Tensor log_probabilities = probabilities.log();
  const Tensor negative_one({}, {-1.0});
  const Tensor class_losses = log_probabilities * negative_one;
  const Tensor selected_losses = class_losses * targets;
  const Tensor total_loss = selected_losses.sum();

  const double image_count = static_cast<double>(labels.size());
  const Tensor batch_size({}, {image_count});

  const Tensor mean_loss = total_loss / batch_size;
  return mean_loss;
}
```

**After**
```cpp

```

</details>

<details>
<summary>Exact code: move-softmax-out-of-main</summary>

Location: `main.cpp`.

<!-- edit: move-softmax-out-of-main file: main.cpp -->
**Before**
```cpp
[[nodiscard]] Tensor softmax(const Tensor& scores) {
  const Tensor positive = scores.exp();
  const Tensor totals = positive.sum_columns();
  return positive / totals;
}
```

**After**
```cpp

```

</details>

<details>
<summary>Exact code: include-dlatwd-loss-hpp</summary>

Location: `include/dlatwd/loss.hpp`.

<!-- edit: include-dlatwd-loss-hpp file: include/dlatwd/loss.hpp -->
**Before**
```cpp

```

**After**
```cpp
#pragma once
#include "dlatwd/tensor.hpp"

namespace dlatwd {
[[nodiscard]] Tensor mse_loss(const Tensor& prediction, const Tensor& target);

[[nodiscard]] Tensor cross_entropy_loss(const Tensor& probabilities,
                                        const std::vector<std::size_t>& labels);

[[nodiscard]] Tensor softmax(const Tensor& scores);
}  // namespace dlatwd
```

</details>

<details>
<summary>Exact code: src-losses-cpp</summary>

Location: `src/losses.cpp`.

<!-- edit: src-losses-cpp file: src/losses.cpp -->
**Before**
```cpp

```

**After**
```cpp
#include "dlatwd/loss.hpp"

#include <stdexcept>

namespace dlatwd {
[[nodiscard]] Tensor mse_loss(const Tensor& prediction, const Tensor& target) {
  if (prediction.shape() != target.shape()) {
    throw std::invalid_argument("mse loss requires equal shapes");
  }

  Tensor residual = prediction - target;
  return (residual * residual).mean();
}

[[nodiscard]] Tensor cross_entropy_loss(const Tensor& probabilities,
                                        const std::vector<std::size_t>& labels) {
  Tensor targets(probabilities.shape(),
                 std::vector<double>(probabilities.numel(), 0.0));
  for (std::size_t row = 0; row < labels.size(); ++row) {
    targets.at({row, labels[row]}) = 1.0;
  }
  const Tensor log_probabilities = probabilities.log();
  const Tensor negative_one({}, {-1.0});
  const Tensor class_losses = log_probabilities * negative_one;
  const Tensor selected_losses = class_losses * targets;
  const Tensor total_loss = selected_losses.sum();

  const double image_count = static_cast<double>(labels.size());
  const Tensor batch_size({}, {image_count});

  const Tensor mean_loss = total_loss / batch_size;
  return mean_loss;
}

[[nodiscard]] Tensor softmax(const Tensor& scores) {
  const Tensor positive = scores.exp();
  const Tensor totals = positive.sum_columns();
  return positive / totals;
}
}  // namespace dlatwd
```

</details>

### C3. Give each example its own entry point

> Now the application only needs to choose what to run. MNIST, XOR and regression become separate programs, so we won’t keep commenting calls in and out of one main function.

<details>
<summary>Exact code: move-count-correct-out-of-main</summary>

Location: `main.cpp`.

<!-- edit: move-count-correct-out-of-main file: main.cpp -->
**Before**
```cpp
[[nodiscard]] std::size_t count_correct(
  const Tensor& scores,
  const std::vector<std::size_t>& labels
) {
  std::size_t correct = 0;
  for (std::size_t row = 0; row < labels.size(); ++row) {
    std::size_t predicted = 0;
    for (std::size_t digit = 1; digit < 10; ++digit) {
      if (scores.at({row, digit}) > scores.at({row, predicted})) {
        predicted = digit;
      }
    }
    correct += predicted == labels[row];
  }
  return correct;
}
```

**After**
```cpp

```

</details>

<details>
<summary>Exact code: move-train-mnist-out-of-main</summary>

Location: `main.cpp`.

<!-- edit: move-train-mnist-out-of-main file: main.cpp -->
**Before**
```cpp
void train_mnist() {
    MnistReader preview(
      "data/train-images-idx3-ubyte", 
      "data/train-labels-idx1-ubyte"
    );

    MnistBatch sample = preview.read_batch(1);

    // 28 x 28 = 784

    const Tensor image(
      {1, 784}, 
      std::move(sample.pixels)
    );

    std::mt19937 random(42);
    MLP model(784, 32, 10, random);

    const Tensor scores = model.forward(image);
    const Tensor probabilities = softmax(scores);

    std::cout << "Correct digit: " << sample.labels[0] << '\n';
    for (std::size_t digit = 0; digit < 10; ++digit) {
      std::cout << digit << ": " 
        << scores.at({0, digit}) << ", "
        << probabilities.at({0, digit}) 
        << '\n';
    }

    std::cout << "Probability total: " << probabilities.sum().at({}) << " \n";

    std::vector<Tensor> parameters = model.parameters();

    for(std::size_t epoch = 0; epoch < 5; ++epoch) {
      std::cout << "Training epoch: " << epoch + 1 << "/5\n";
      MnistReader training(
        "data/train-images-idx3-ubyte", 
        "data/train-labels-idx1-ubyte"
      );
      double total_loss = 0.0;
      std::size_t seen = 0.0;

      while (seen < 10000) {
        MnistBatch batch = training.read_batch(
          std::min<std::size_t>(64, 10000 - seen)
        );
        const Tensor inputs(
          {batch.labels.size(), 784},
          std::move(batch.pixels)
        );
        for (Tensor& parameter: parameters) {
          parameter.zero_grad();
        }
        const Tensor logits = model.forward(inputs);
        const Tensor probabilities = softmax(logits);
        Tensor loss = cross_entropy_loss(probabilities, batch.labels);
        loss.backward();
        gradient_step(parameters, 0.1);

        total_loss += loss.at({}) * batch.labels.size();
        seen += batch.labels.size();
      }

      std::cout << "Epoch " << epoch + 1 << " loss: " << total_loss / seen << "\n\n";
    }

    MnistReader test(
      "data/t10k-images-idx3-ubyte", 
      "data/t10k-labels-idx1-ubyte"
    );

    std::size_t correct = 0;
    std::size_t tested = 0;

    while (tested < 2000) {
      MnistBatch batch = test.read_batch(
        std::min<std::size_t>(64, 2000 - tested)
      );
      const Tensor inputs(
        {batch.labels.size(), 784},
        std::move(batch.pixels)
      );

      correct += count_correct(
        model.forward(inputs),
        batch.labels
      );
      tested += batch.labels.size();
    }

    std::cout << "Test accuracy: "  << 
      100.0 * correct / tested <<
      "% (" << correct << '/' << tested << ")\n";

}
```

**After**
```cpp

```

</details>

<details>
<summary>Exact code: examples-mnist-cpp</summary>

Location: `examples/mnist.cpp`.

<!-- edit: examples-mnist-cpp file: examples/mnist.cpp -->
**Before**
```cpp

```

**After**
```cpp
#include <iomanip>
#include <iostream>

#include "dlatwd/loss.hpp"
#include "dlatwd/nn.hpp"

using dlatwd::gradient_step;
using dlatwd::MLP;
using dlatwd::mse_loss;
using dlatwd::Tensor;
#include "mnist_reader.hpp"
using dlatwd::cross_entropy_loss;
using dlatwd::softmax;

[[nodiscard]] std::size_t count_correct(const Tensor& scores,
                                        const std::vector<std::size_t>& labels) {
  std::size_t correct = 0;
  for (std::size_t row = 0; row < labels.size(); ++row) {
    std::size_t predicted = 0;
    for (std::size_t digit = 1; digit < 10; ++digit) {
      if (scores.at({row, digit}) > scores.at({row, predicted})) {
        predicted = digit;
      }
    }
    correct += predicted == labels[row];
  }
  return correct;
}

void train_mnist() {
  MnistReader preview("data/train-images-idx3-ubyte", "data/train-labels-idx1-ubyte");

  MnistBatch sample = preview.read_batch(1);

  // 28 x 28 = 784

  const Tensor image({1, 784}, std::move(sample.pixels));

  std::mt19937 random(42);
  MLP model(784, 32, 10, random);

  const Tensor scores = model.forward(image);
  const Tensor probabilities = softmax(scores);

  std::cout << "Correct digit: " << sample.labels[0] << '\n';
  for (std::size_t digit = 0; digit < 10; ++digit) {
    std::cout << digit << ": " << scores.at({0, digit}) << ", "
              << probabilities.at({0, digit}) << '\n';
  }

  std::cout << "Probability total: " << probabilities.sum().at({}) << " \n";

  std::vector<Tensor> parameters = model.parameters();

  for (std::size_t epoch = 0; epoch < 5; ++epoch) {
    std::cout << "Training epoch: " << epoch + 1 << "/5\n";
    MnistReader training("data/train-images-idx3-ubyte",
                         "data/train-labels-idx1-ubyte");
    double total_loss = 0.0;
    std::size_t seen = 0.0;

    while (seen < 10000) {
      MnistBatch batch = training.read_batch(std::min<std::size_t>(64, 10000 - seen));
      const Tensor inputs({batch.labels.size(), 784}, std::move(batch.pixels));
      for (Tensor& parameter : parameters) {
        parameter.zero_grad();
      }
      const Tensor logits = model.forward(inputs);
      const Tensor probabilities = softmax(logits);
      Tensor loss = cross_entropy_loss(probabilities, batch.labels);
      loss.backward();
      gradient_step(parameters, 0.1);

      total_loss += loss.at({}) * batch.labels.size();
      seen += batch.labels.size();
    }

    std::cout << "Epoch " << epoch + 1 << " loss: " << total_loss / seen << "\n\n";
  }

  MnistReader test("data/t10k-images-idx3-ubyte", "data/t10k-labels-idx1-ubyte");

  std::size_t correct = 0;
  std::size_t tested = 0;

  while (tested < 2000) {
    MnistBatch batch = test.read_batch(std::min<std::size_t>(64, 2000 - tested));
    const Tensor inputs({batch.labels.size(), 784}, std::move(batch.pixels));

    correct += count_correct(model.forward(inputs), batch.labels);
    tested += batch.labels.size();
  }

  std::cout << "Test accuracy: " << 100.0 * correct / tested << "% (" << correct << '/'
            << tested << ")\n";
}

int main() { train_mnist(); }
```

</details>

<details>
<summary>Exact code: move-train-xor-out-of-main</summary>

Location: `main.cpp`.

<!-- edit: move-train-xor-out-of-main file: main.cpp -->
**Before**
```cpp
void train_xor() {
  // a b   target
  // 0 0     0
  // 0 1     1
  // 1 0     1
  // 1 1     0
  const Tensor inputs({4, 2}, {
    0.0, 0.0,
    0.0, 1.0,
    1.0, 0.0,
    1.0, 1.0
  });
  const Tensor targets({4, 1}, {0.0, 1.0, 1.0, 0.0});

  std::mt19937 random(42);
  MLP model(2, 4, 1, random);

  std::vector<Tensor> parameters = model.parameters();

  const double initial_loss = mse_loss(model.forward(inputs), targets).at({});

  for (std::size_t step = 0; step < 5000; ++step) {
    for (Tensor& parameter: parameters) {
      parameter.zero_grad();
    }

    const Tensor predictions = model.forward(inputs);
    Tensor loss = mse_loss(predictions, targets);
    loss.backward();
    gradient_step(parameters, 0.1);
  }

  const Tensor predictions = model.forward(inputs);
  std::cout << std::fixed << std::setprecision(3);
  std::cout << "Loss: " << initial_loss << " -> "
            << mse_loss(predictions, targets).at({})
            << '\n';
  
  std::cout << "a b prediction target\n";
  for (std::size_t row = 0; row < inputs.dimension(0); ++row) {
    std::cout << inputs.at({row, 0}) << ' '
              << inputs.at({row, 1}) << ' '
              << predictions.at({row, 0}) << ' '
              << targets.at({row, 0}) << '\n';
  }

}
```

**After**
```cpp

```

</details>

<details>
<summary>Exact code: examples-xor-cpp</summary>

Location: `examples/xor.cpp`.

<!-- edit: examples-xor-cpp file: examples/xor.cpp -->
**Before**
```cpp

```

**After**
```cpp
#include <iomanip>
#include <iostream>

#include "dlatwd/loss.hpp"
#include "dlatwd/nn.hpp"

using dlatwd::gradient_step;
using dlatwd::MLP;
using dlatwd::mse_loss;
using dlatwd::Tensor;

void train_xor() {
  // a b   target
  // 0 0     0
  // 0 1     1
  // 1 0     1
  // 1 1     0
  const Tensor inputs({4, 2}, {0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0});
  const Tensor targets({4, 1}, {0.0, 1.0, 1.0, 0.0});

  std::mt19937 random(42);
  MLP model(2, 4, 1, random);

  std::vector<Tensor> parameters = model.parameters();

  const double initial_loss = mse_loss(model.forward(inputs), targets).at({});

  for (std::size_t step = 0; step < 5000; ++step) {
    for (Tensor& parameter : parameters) {
      parameter.zero_grad();
    }

    const Tensor predictions = model.forward(inputs);
    Tensor loss = mse_loss(predictions, targets);
    loss.backward();
    gradient_step(parameters, 0.1);
  }

  const Tensor predictions = model.forward(inputs);
  std::cout << std::fixed << std::setprecision(3);
  std::cout << "Loss: " << initial_loss << " -> "
            << mse_loss(predictions, targets).at({}) << '\n';

  std::cout << "a b prediction target\n";
  for (std::size_t row = 0; row < inputs.dimension(0); ++row) {
    std::cout << inputs.at({row, 0}) << ' ' << inputs.at({row, 1}) << ' '
              << predictions.at({row, 0}) << ' ' << targets.at({row, 0}) << '\n';
  }
}

int main() { train_xor(); }
```

</details>

<details>
<summary>Exact code: move-linear-forward-out-of-main</summary>

Location: `main.cpp`.

<!-- edit: move-linear-forward-out-of-main file: main.cpp -->
**Before**
```cpp
[[nodiscard]] Tensor linear_forward(
  const Tensor& inputs,
  const Tensor& weights,
  const Tensor& bias
) {
  return inputs.matmul(weights) + bias;
}
```

**After**
```cpp

```

</details>

<details>
<summary>Exact code: move-nonlinear-forward-out-of-main</summary>

Location: `main.cpp`.

<!-- edit: move-nonlinear-forward-out-of-main file: main.cpp -->
**Before**
```cpp
[[nodiscard]] Tensor nonlinear_forward(
  const Tensor& inputs,
  const Tensor& weights,
  const Tensor& bias
) {
  return (inputs.matmul(weights) + bias).tanh();
}
```

**After**
```cpp

```

</details>

<details>
<summary>Exact code: move-show-activations-out-of-main</summary>

Location: `main.cpp`.

<!-- edit: move-show-activations-out-of-main file: main.cpp -->
**Before**
```cpp
void show_activations() {
  const Tensor inputs({5}, {-2.0, -1.0, 0.0, 1.0, 2.0});
  const Tensor relu_outputs = inputs.relu();
  const Tensor sigmoid_outputs = inputs.sigmoid();
  const Tensor tanh_outputs = inputs.tanh();

  std::cout << "x relu sigmoid\n";
  for (std::size_t index = 0; index < inputs.numel(); ++index) {
    std::cout
      << inputs.at({index}) << ' '
      << relu_outputs.at({index}) << ' '
      << sigmoid_outputs.at({index}) << ' '
      << tanh_outputs.at({index}) << '\n';
  }
}
```

**After**
```cpp

```

</details>

<details>
<summary>Exact code: move-train-linear-regression-out-of-main</summary>

Location: `main.cpp`.

<!-- edit: move-train-linear-regression-out-of-main file: main.cpp -->
**Before**
```cpp
void train_linear_regression(
  const Tensor& inputs,
  const Tensor& targets,
  Tensor& weights,
  Tensor& bias,
  std::size_t steps,
  double learning_rate
) {
  for (std::size_t step = 0; step < steps; ++step) {
    weights.zero_grad();
    bias.zero_grad();

    const Tensor predictions = linear_forward(inputs, weights, bias);
    Tensor loss = mse_loss(predictions, targets);
    loss.backward();
    std::vector<Tensor> parameters {weights, bias};
    gradient_step(parameters, learning_rate);
  }
}
```

**After**
```cpp

```

</details>

<details>
<summary>Exact code: move-train-nonlinear-regression-out-of-main</summary>

Location: `main.cpp`.

<!-- edit: move-train-nonlinear-regression-out-of-main file: main.cpp -->
**Before**
```cpp
void train_nonlinear_regression(
  const Tensor& inputs,
  const Tensor& targets,
  Tensor& weights,
  Tensor& bias,
  std::size_t steps,
  double learning_rate
) {
  for (std::size_t step = 0; step < steps; ++step) {
    weights.zero_grad();
    bias.zero_grad();

    const Tensor predictions = nonlinear_forward(inputs, weights, bias);
    Tensor loss = mse_loss(predictions, targets);
    loss.backward();
    std::vector<Tensor> parameters {weights, bias};
    gradient_step(parameters, learning_rate);
  }
}
```

**After**
```cpp

```

</details>

<details>
<summary>Exact code: move-train-line-out-of-main</summary>

Location: `main.cpp`.

<!-- edit: move-train-line-out-of-main file: main.cpp -->
**Before**
```cpp
void train_line() {
  Tensor input(
    {10, 1},
    {
      0.0, 1.0, 2.0, 3.0, 4.0,
      5.0, 6.0, 7.0, 8.0, 9.0
    }
  );

  Tensor targets(
    {10, 1},
    {
      1.0, 3.0, 5.0, 7.0, 9.0,
      11.0, 13.0, 15.0, 17.0, 19.0
    }
  );

  // y = 2x + 1
  
  Tensor weight({1,1}, {0.0});
  Tensor bias({}, {0.0});

  train_linear_regression(input, targets, weight, bias, 10000, 0.01);

  std::cout << "Weight: " << weight.at({0, 0}) << " \n";
  std::cout << "Bias: " << bias.at({}) << " \n";
}
```

**After**
```cpp

```

</details>

<details>
<summary>Exact code: move-train-curve-out-of-main</summary>

Location: `main.cpp`.

<!-- edit: move-train-curve-out-of-main file: main.cpp -->
**Before**
```cpp
void train_curve() {
  Tensor inputs(
    {9, 1},
    {
      -1.0, -0.75, -0.5, -0.25, 0.0,
      0.25, 0.5, 0.75, 1.0
    }
  );

  Tensor targets(
    {9, 1},
    {
      -0.761594, -0.462117, 0.0,
      0.462117, 0.761594, 0.905148,
      0.964028, 0.986614, 0.995055
    }
  );

  // y = tanh(2x + 1)

  Tensor weight({1,1}, {0.0});
  Tensor bias({}, {0.0});

  train_nonlinear_regression(inputs, targets, weight, bias, 100000, 0.01);

  std::cout << "Weight: " << weight.at({0, 0}) << " \n";
  std::cout << "Bias: " << bias.at({}) << " \n";

}
```

**After**
```cpp

```

</details>

<details>
<summary>Exact code: examples-regression-cpp</summary>

Location: `examples/regression.cpp`.

<!-- edit: examples-regression-cpp file: examples/regression.cpp -->
**Before**
```cpp

```

**After**
```cpp
#include <iomanip>
#include <iostream>

#include "dlatwd/loss.hpp"
#include "dlatwd/nn.hpp"

using dlatwd::gradient_step;
using dlatwd::MLP;
using dlatwd::mse_loss;
using dlatwd::Tensor;

[[nodiscard]] Tensor linear_forward(const Tensor& inputs, const Tensor& weights,
                                    const Tensor& bias) {
  return inputs.matmul(weights) + bias;
}

[[nodiscard]] Tensor nonlinear_forward(const Tensor& inputs, const Tensor& weights,
                                       const Tensor& bias) {
  return (inputs.matmul(weights) + bias).tanh();
}

void show_activations() {
  const Tensor inputs({5}, {-2.0, -1.0, 0.0, 1.0, 2.0});
  const Tensor relu_outputs = inputs.relu();
  const Tensor sigmoid_outputs = inputs.sigmoid();
  const Tensor tanh_outputs = inputs.tanh();

  std::cout << "x relu sigmoid\n";
  for (std::size_t index = 0; index < inputs.numel(); ++index) {
    std::cout << inputs.at({index}) << ' ' << relu_outputs.at({index}) << ' '
              << sigmoid_outputs.at({index}) << ' ' << tanh_outputs.at({index}) << '\n';
  }
}

void train_linear_regression(const Tensor& inputs, const Tensor& targets,
                             Tensor& weights, Tensor& bias, std::size_t steps,
                             double learning_rate) {
  for (std::size_t step = 0; step < steps; ++step) {
    weights.zero_grad();
    bias.zero_grad();

    const Tensor predictions = linear_forward(inputs, weights, bias);
    Tensor loss = mse_loss(predictions, targets);
    loss.backward();
    std::vector<Tensor> parameters{weights, bias};
    gradient_step(parameters, learning_rate);
  }
}

void train_nonlinear_regression(const Tensor& inputs, const Tensor& targets,
                                Tensor& weights, Tensor& bias, std::size_t steps,
                                double learning_rate) {
  for (std::size_t step = 0; step < steps; ++step) {
    weights.zero_grad();
    bias.zero_grad();

    const Tensor predictions = nonlinear_forward(inputs, weights, bias);
    Tensor loss = mse_loss(predictions, targets);
    loss.backward();
    std::vector<Tensor> parameters{weights, bias};
    gradient_step(parameters, learning_rate);
  }
}

void train_line() {
  Tensor input({10, 1}, {0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0});

  Tensor targets({10, 1}, {1.0, 3.0, 5.0, 7.0, 9.0, 11.0, 13.0, 15.0, 17.0, 19.0});

  // y = 2x + 1

  Tensor weight({1, 1}, {0.0});
  Tensor bias({}, {0.0});

  train_linear_regression(input, targets, weight, bias, 10000, 0.01);

  std::cout << "Weight: " << weight.at({0, 0}) << " \n";
  std::cout << "Bias: " << bias.at({}) << " \n";
}

void train_curve() {
  Tensor inputs({9, 1}, {-1.0, -0.75, -0.5, -0.25, 0.0, 0.25, 0.5, 0.75, 1.0});

  Tensor targets({9, 1}, {-0.761594, -0.462117, 0.0, 0.462117, 0.761594, 0.905148,
                          0.964028, 0.986614, 0.995055});

  // y = tanh(2x + 1)

  Tensor weight({1, 1}, {0.0});
  Tensor bias({}, {0.0});

  train_nonlinear_regression(inputs, targets, weight, bias, 100000, 0.01);

  std::cout << "Weight: " << weight.at({0, 0}) << " \n";
  std::cout << "Bias: " << bias.at({}) << " \n";
}

int main() {
  show_activations();
  train_line();
  train_curve();
}
```

</details>

Move the reader and scalar example without changing their contents:

```sh
mv mnist_reader.hpp examples/mnist_reader.hpp
mv scalar_autograd.cpp examples/scalar_autograd.cpp
```

Run every example from the repository root. MNIST continues to read the existing `data/` directory; no dataset setup changes are part of this lesson.

### C4. Replace main assertions with named tests

> What’s left in main is our test code. It shouldn’t train a model every time we check indexing. We’ll move those checks into GoogleTest, which gives each test a name and reports the values when an expectation fails.

Show the actual migrated sum test below. This is a reference excerpt from the complete test file that follows, not an extra test to add.

```cpp
TEST_F(TensorTest, Sum) {
  EXPECT_TRUE((Tensor({2, 3}, {1, 2, 3, 4, 5, 6}).sum().at({}) == 21.0));
  EXPECT_TRUE((Tensor({}, {7.0}).sum().at({}) == 7.0));
  EXPECT_TRUE((Tensor({1}, {7.0}).sum().at({}) == 7.0));
  EXPECT_TRUE((Tensor({0}, {}).sum().at({}) == 0.0));
  EXPECT_TRUE((Tensor({2, 0, 3}, {}).sum().at({}) == 0.0));
}
```

> These assertions already test sums, including scalars and empty tensors. We keep the checks and give the group a name. TEST underscore F uses a fixture, which gives each test a fresh copy of the shared setup. One test's mutations can't leak into another.

<details>
<summary>Exact code: retire-main-after-test-migration</summary>

Location: `main.cpp`.

<!-- edit: retire-main-after-test-migration file: main.cpp -->
**Before**
```cpp
#include "mnist_reader.hpp"
#include <algorithm>
#include <cmath>
#include <cstddef>
#include <fstream>
#include <iomanip>
#include <ios>
#include <limits>
#include <random>
#include <stdexcept>
#include <string>
#include <vector>
#include <iostream>
#include <cassert>
#include <memory>
#include <utility>
#include <unordered_set>







































int main() {

  std::vector<std::size_t> shape_1 {2, 3};
  std::vector<double> data_1 {0,1,2,3,4,5};

  Tensor t(
    shape_1,
    data_1
  );

  std::cout << "Test 1\n";
  auto& actual_shape_1 = t.shape();
  assert(actual_shape_1 == shape_1);


  std::cout << "Test 2\n";
  auto& actual_data_1 = t.data();
  assert(actual_data_1 == data_1);

 
  std::cout << "Test 3\n";
  std::size_t actual_rank_1 = t.rank();
  assert(actual_rank_1 == 2);

  std::cout << "Test 4\n";
  std::size_t actual_numel_1 = t.numel();
  assert(actual_numel_1 == 6);

  std::cout << "Test 5\n";
  bool test_5_threw = false;
  try {
    Tensor({}, {});
  } catch (std::invalid_argument& error) {
    assert(std::string(error.what()) == "tensor shape does not match its data");
    test_5_threw = true;
  }
  assert(test_5_threw);
  Tensor scalar({}, {5});
  assert(scalar.rank() == 0);
  assert(scalar.numel() == 1);
  assert(scalar.shape() == std::vector<std::size_t>{});

  std::cout << "Test 6\n";
  Tensor empty_matrix({1, 0}, {});
  assert(empty_matrix.rank() == 2);
  assert(empty_matrix.numel() == 0);
  assert((empty_matrix.shape() == std::vector<std::size_t>{1, 0}));

  std::cout << "Test 7\n";
  bool test_7_threw = false;
  try {
    Tensor({2, 3}, {1,2,3});
  } catch (std::invalid_argument& error) {
    assert(std::string(error.what()) == "tensor shape does not match its data");
    test_7_threw = true;
  }
  assert(test_7_threw);

  std::cout << "Test 8\n";
  double val = t.at({1, 1});
  assert(val == 4);

  std::cout << "Test 9\n";
  bool test_9_threw = false;
  try {
    double val_9 = t.at({1,2,3});
  } catch (std::invalid_argument& error) {
    assert(std::string(error.what()) == "number of indices must match tensor rank");
    test_9_threw = true;
  }
  assert(test_9_threw);

  std::cout << "Test 10\n";
  bool test_10_threw = false;
  try {
    double val_10 = t.at({2,3});
  } catch (std::out_of_range& error) {
    assert(std::string(error.what()) == "tensor index is outside its dimension");
    test_10_threw = true;
  }
  assert(test_10_threw);

  std::cout << "Test 11\n";
  bool test_11_threw = false;
  try {
    Tensor overflow({std::numeric_limits<std::size_t>::max(), 2}, {});
  } catch (std::overflow_error& error) {
    assert(std::string(error.what()) == "tensor element count overflows size_t");
    test_11_threw = true;
  }
  assert(test_11_threw);

  std::cout << "Test 12\n";
  Tensor zero_and_max({std::numeric_limits<std::size_t>::max(), 0}, {});
  assert(zero_and_max.rank() == 2);
  assert(zero_and_max.numel() == 0);

  std::cout << "Test 13\n";
  Tensor zero_and_max_3d({std::numeric_limits<std::size_t>::max(), 2, 0}, {});
  assert(zero_and_max_3d.rank() == 3);
  assert(zero_and_max_3d.numel() == 0);

  std::cout << "Test 14\n";
  Tensor dim_test_tensor({2, 0, 3}, {});
  assert(dim_test_tensor.dimension(0) == 2);
  assert(dim_test_tensor.dimension(1) == 0);
  assert(dim_test_tensor.dimension(2) == 3);

  bool rejected_axis = false;
  try {
    auto d = dim_test_tensor.dimension(3);
  } catch(const std::out_of_range&) {
    rejected_axis = true;
  }
  assert(rejected_axis);

  std::cout << "Test 15\n";
  Tensor mutation_tensor({2,3}, {0,1,2,3,4,5});
  assert(mutation_tensor.at({0, 0}) == 0);
  mutation_tensor.at({0, 0}) = 5;
  assert(mutation_tensor.at({0, 0}) == 5);

  std::cout << "Test 16\n";
  Tensor scalar_16({}, {10});
  assert(10 == scalar_16.at({}));

  std::cout << "Test 17\n";
  assert((Tensor({2, 3}, {1,2,3,4,5,6}).sum().at({}) == 21.0));
  assert((Tensor({}, {7.0}).sum().at({}) == 7.0));
  assert((Tensor({1}, {7.0}).sum().at({}) == 7.0));
  assert((Tensor({0}, {}).sum().at({}) == 0.0));
  assert((Tensor({2, 0, 3}, {}).sum().at({}) == 0.0));

  std::cout << "Test 18\n";
  const Tensor left({3}, {1.0, 2.0, 3.0});
  const Tensor right({3}, {10.0, 20.0, 30.0});

  const Tensor added = left + right;
  assert((added.shape() == std::vector<std::size_t>{3}));
  assert((added.data() == std::vector<double>{11.0, 22.0, 33.0}));
  assert((left.data() == std::vector<double>{1.0, 2.0, 3.0}));
  assert((right.data() == std::vector<double>{10.0, 20.0, 30.0}));

  const Tensor scalar_sum = Tensor({}, {2.0}) + Tensor({}, {3.0});
  assert(scalar_sum.rank() == 0);
  assert(scalar_sum.at({}) == 5.0);

  const Tensor empty_sum = Tensor({0}, {}) + Tensor({0}, {});
  assert((empty_sum.shape() == std::vector<std::size_t>{0}));
  assert(empty_sum.numel() == 0);

  std::cout << "Test 19\n";

  bool rejected_mismatched_shapes = false;

  try {
    const auto invalid = Tensor({3}, {1.0, 2.0, 3.0}) + Tensor({1, 2}, {3.0, 4.0});
  } catch (const std::invalid_argument&) {
    rejected_mismatched_shapes = true;
  }
  assert(rejected_mismatched_shapes);

  std::cout << "Test 20\n";

  const Tensor arithmetic_left({3}, {2.0, 3.0, 4.0});
  const Tensor arithmetic_right({3}, {5.0, 6.0, 7.0});

  const Tensor arithmetic_sum = arithmetic_left + arithmetic_right;
  const Tensor arithmetic_sub = arithmetic_left - arithmetic_right;
  const Tensor arithmetic_prod = arithmetic_left * arithmetic_right;

  assert((arithmetic_sum.data() == std::vector<double>{7.0, 9.0, 11.0}));
  assert((arithmetic_sub.data() == std::vector<double>{-3.0, -3.0, -3.0}));
  assert((arithmetic_prod.data() == std::vector<double>{10.0, 18.0, 28.0}));

  std::cout << "Test 21\n";

  const Tensor dot_result = Tensor({3}, {2.0, 3.0, 4.0}).dot(Tensor({3}, {5.0, 6.0, 7.0}));

  assert(dot_result.rank() == 0);
  assert(dot_result.at({}) == 56.0);

  const Tensor empty_dot = Tensor({0}, {}).dot(Tensor({0}, {}));
  assert(empty_dot.rank() == 0);
  assert(empty_dot.at({}) == 0);

  bool rejected_matrix_dot = false;

  try {
    const auto invalid = Tensor({1, 2}, {1.0, 2.0}).dot(Tensor({1, 2}, {3.0, 4.0}));
  } catch (const std::invalid_argument&) {
    rejected_matrix_dot = true;
  }
  assert(rejected_matrix_dot);

  bool rejected_unequal_lengths = false;

  try {
    const auto invalid = Tensor({2}, {1.0, 2.0}).dot(Tensor({3}, {3.0, 4.0, 5.0}));
  } catch (const std::invalid_argument&) {
    rejected_unequal_lengths = true;
  }
  assert(rejected_unequal_lengths);


  // features = [ 4.0, 3.0, 2.0]
  // weights  = [0.5,  -1.0, 2.0]
  // scaled   = [2.0,  -3.0, 4.0]
  // weighted_sum = 3.0
  // bias = 0.5
  // prediction = 3.0 + 0.5 = 3.5
  // pred = weights.dot(features) + bias

  std::cout << "Test 22\n";

  const Tensor features({3}, {4.0, 3.0, 2.0});

  const Tensor weights_({3}, {0.5, -1.0, 2.0});
  const Tensor bias({}, {0.5});

  const Tensor prediction = weights_.dot(features) + bias;
  assert(prediction.rank() == 0);
  assert(prediction.at({}) == 3.5);

  


  
  // 2 observations
  // 3 features 

  // 2x3 matrix

  const Tensor inputs(
    {2, 3},
    {
      4.0, 3.0, 2.0,
      1.0, 2.0, 0.5
    }
  );

  const Tensor weights(
    {3, 1},
    {
      0.5,
      -1.0,
      2.0
    }
  );

  // 3.0
  // -0.5

  std::cout << "Test 23\n";
  const Tensor matmul_23 = inputs.matmul(weights);

  assert((
    matmul_23.shape() == std::vector<std::size_t>{2, 1}
  ));

  assert((
    matmul_23.data() == std::vector<double>{3.0, -0.5}
  ));

  const Tensor pred_23 = matmul_23 + bias;
  assert((
    pred_23.data() == std::vector<double>{3.5, 0.0}
  ));

  const Tensor targets(
    {2,1},
    {
      2.5,
      1.0
    }
  );

  const Tensor residuals = pred_23 - targets;
  assert((residuals.data() == std::vector<double>{1.0, -1.0}));

  const Tensor residuals_total = residuals.sum(); // 1.0 - 1.0 = 0.0

  const Tensor squared_residuals = residuals * residuals;
  assert((squared_residuals.data() == std::vector<double>{1.0, 1.0}));

  const Tensor total_squared_error = squared_residuals.sum();
  assert(total_squared_error.sum().at({}) == 2);

  const Tensor mean_squared_error = squared_residuals.mean();
  assert(mean_squared_error.rank() == 0);
  assert(mean_squared_error.sum().at({}) == 1.0);

  std::cout << "Test 24\n";
  const Tensor loss = mse_loss(pred_23, targets);
  assert(loss.rank() == 0);
  assert(loss.at({}) == 1.0);

  const Tensor perfect_loss = mse_loss(pred_23, pred_23);
  assert(perfect_loss.at({}) == 0.0);

  bool rejected_empty_mean = false;
  try {
    static_cast<void>(Tensor({0}, {}).mean());
  } catch (std::invalid_argument&) {
    rejected_empty_mean = true;
  }
  assert(rejected_empty_mean);


  const Tensor predictions({2, 1}, {3.5, 0.0});
  const Tensor alias = predictions;
  assert(&alias.data() == &predictions.data());


  // train_line();

  // show_activations();

  // train_curve();

  // train_xor();

  train_mnist();

  std::cout << "Success!\n";
  return 0;
}

```

**After**
```cpp

```

</details>

Delete the now-empty `main.cpp` after the test files below are in place.

<details>
<summary>Exact code: tests-tensor_test-cpp</summary>

Location: `tests/tensor_test.cpp`.

<!-- edit: tests-tensor_test-cpp file: tests/tensor_test.cpp -->
**Before**
```cpp

```

**After**
```cpp
#include "dlatwd/tensor.hpp"

#include <gtest/gtest.h>

#include <limits>
#include <stdexcept>
#include <string>

#include "dlatwd/loss.hpp"

using dlatwd::mse_loss;
using dlatwd::Tensor;

class TensorTest : public testing::Test {
 protected:
  std::vector<std::size_t> shape_1{2, 3};
  std::vector<double> data_1{0, 1, 2, 3, 4, 5};
  Tensor t{shape_1, data_1};
};

TEST_F(TensorTest, Shape) {
  auto& actual_shape_1 = t.shape();
  EXPECT_TRUE(actual_shape_1 == shape_1);
}

TEST_F(TensorTest, Storage) {
  auto& actual_data_1 = t.data();
  EXPECT_TRUE(actual_data_1 == data_1);
}

TEST_F(TensorTest, Rank) {
  std::size_t actual_rank_1 = t.rank();
  EXPECT_TRUE(actual_rank_1 == 2);
}

TEST_F(TensorTest, ElementCount) {
  std::size_t actual_numel_1 = t.numel();
  EXPECT_TRUE(actual_numel_1 == 6);
}

TEST_F(TensorTest, ScalarShape) {
  bool test_5_threw = false;
  try {
    Tensor({}, {});
  } catch (std::invalid_argument& error) {
    EXPECT_TRUE(std::string(error.what()) == "tensor shape does not match its data");
    test_5_threw = true;
  }
  EXPECT_TRUE(test_5_threw);
  Tensor scalar({}, {5});
  EXPECT_TRUE(scalar.rank() == 0);
  EXPECT_TRUE(scalar.numel() == 1);
  EXPECT_TRUE(scalar.shape() == std::vector<std::size_t>{});
}

TEST_F(TensorTest, EmptyTensor) {
  Tensor empty_matrix({1, 0}, {});
  EXPECT_TRUE(empty_matrix.rank() == 2);
  EXPECT_TRUE(empty_matrix.numel() == 0);
  EXPECT_TRUE((empty_matrix.shape() == std::vector<std::size_t>{1, 0}));
}

TEST_F(TensorTest, RejectsWrongStorage) {
  bool test_7_threw = false;
  try {
    Tensor({2, 3}, {1, 2, 3});
  } catch (std::invalid_argument& error) {
    EXPECT_TRUE(std::string(error.what()) == "tensor shape does not match its data");
    test_7_threw = true;
  }
  EXPECT_TRUE(test_7_threw);
}

TEST_F(TensorTest, Indexing) {
  double val = t.at({1, 1});
  EXPECT_TRUE(val == 4);
}

TEST_F(TensorTest, RejectsWrongIndexRank) {
  bool test_9_threw = false;
  try {
    double val_9 = t.at({1, 2, 3});
  } catch (std::invalid_argument& error) {
    EXPECT_TRUE(std::string(error.what()) ==
                "number of indices must match tensor rank");
    test_9_threw = true;
  }
  EXPECT_TRUE(test_9_threw);
}

TEST_F(TensorTest, RejectsOutOfBounds) {
  bool test_10_threw = false;
  try {
    double val_10 = t.at({2, 3});
  } catch (std::out_of_range& error) {
    EXPECT_TRUE(std::string(error.what()) == "tensor index is outside its dimension");
    test_10_threw = true;
  }
  EXPECT_TRUE(test_10_threw);
}

TEST_F(TensorTest, RejectsShapeOverflow) {
  bool test_11_threw = false;
  try {
    Tensor overflow({std::numeric_limits<std::size_t>::max(), 2}, {});
  } catch (std::overflow_error& error) {
    EXPECT_TRUE(std::string(error.what()) == "tensor element count overflows size_t");
    test_11_threw = true;
  }
  EXPECT_TRUE(test_11_threw);
}

TEST_F(TensorTest, ZeroDimensionWithLargeExtent) {
  Tensor zero_and_max({std::numeric_limits<std::size_t>::max(), 0}, {});
  EXPECT_TRUE(zero_and_max.rank() == 2);
  EXPECT_TRUE(zero_and_max.numel() == 0);
}

TEST_F(TensorTest, ZeroDimensionBeforeOverflow) {
  Tensor zero_and_max_3d({std::numeric_limits<std::size_t>::max(), 2, 0}, {});
  EXPECT_TRUE(zero_and_max_3d.rank() == 3);
  EXPECT_TRUE(zero_and_max_3d.numel() == 0);
}

TEST_F(TensorTest, DimensionAccess) {
  Tensor dim_test_tensor({2, 0, 3}, {});
  EXPECT_TRUE(dim_test_tensor.dimension(0) == 2);
  EXPECT_TRUE(dim_test_tensor.dimension(1) == 0);
  EXPECT_TRUE(dim_test_tensor.dimension(2) == 3);

  bool rejected_axis = false;
  try {
    auto d = dim_test_tensor.dimension(3);
  } catch (const std::out_of_range&) {
    rejected_axis = true;
  }
  EXPECT_TRUE(rejected_axis);
}

TEST_F(TensorTest, Mutation) {
  Tensor mutation_tensor({2, 3}, {0, 1, 2, 3, 4, 5});
  EXPECT_TRUE(mutation_tensor.at({0, 0}) == 0);
  mutation_tensor.at({0, 0}) = 5;
  EXPECT_TRUE(mutation_tensor.at({0, 0}) == 5);
}

TEST_F(TensorTest, ScalarIndexing) {
  Tensor scalar_16({}, {10});
  EXPECT_TRUE(10 == scalar_16.at({}));
}

TEST_F(TensorTest, Sum) {
  EXPECT_TRUE((Tensor({2, 3}, {1, 2, 3, 4, 5, 6}).sum().at({}) == 21.0));
  EXPECT_TRUE((Tensor({}, {7.0}).sum().at({}) == 7.0));
  EXPECT_TRUE((Tensor({1}, {7.0}).sum().at({}) == 7.0));
  EXPECT_TRUE((Tensor({0}, {}).sum().at({}) == 0.0));
  EXPECT_TRUE((Tensor({2, 0, 3}, {}).sum().at({}) == 0.0));
}

TEST_F(TensorTest, Addition) {
  const Tensor left({3}, {1.0, 2.0, 3.0});
  const Tensor right({3}, {10.0, 20.0, 30.0});

  const Tensor added = left + right;
  EXPECT_TRUE((added.shape() == std::vector<std::size_t>{3}));
  EXPECT_TRUE((added.data() == std::vector<double>{11.0, 22.0, 33.0}));
  EXPECT_TRUE((left.data() == std::vector<double>{1.0, 2.0, 3.0}));
  EXPECT_TRUE((right.data() == std::vector<double>{10.0, 20.0, 30.0}));

  const Tensor scalar_sum = Tensor({}, {2.0}) + Tensor({}, {3.0});
  EXPECT_TRUE(scalar_sum.rank() == 0);
  EXPECT_TRUE(scalar_sum.at({}) == 5.0);

  const Tensor empty_sum = Tensor({0}, {}) + Tensor({0}, {});
  EXPECT_TRUE((empty_sum.shape() == std::vector<std::size_t>{0}));
  EXPECT_TRUE(empty_sum.numel() == 0);
}

TEST_F(TensorTest, RejectsIncompatibleBroadcast) {
  bool rejected_mismatched_shapes = false;

  try {
    const auto invalid = Tensor({3}, {1.0, 2.0, 3.0}) + Tensor({1, 2}, {3.0, 4.0});
  } catch (const std::invalid_argument&) {
    rejected_mismatched_shapes = true;
  }
  EXPECT_TRUE(rejected_mismatched_shapes);
}

TEST_F(TensorTest, Arithmetic) {
  const Tensor arithmetic_left({3}, {2.0, 3.0, 4.0});
  const Tensor arithmetic_right({3}, {5.0, 6.0, 7.0});

  const Tensor arithmetic_sum = arithmetic_left + arithmetic_right;
  const Tensor arithmetic_sub = arithmetic_left - arithmetic_right;
  const Tensor arithmetic_prod = arithmetic_left * arithmetic_right;

  EXPECT_TRUE((arithmetic_sum.data() == std::vector<double>{7.0, 9.0, 11.0}));
  EXPECT_TRUE((arithmetic_sub.data() == std::vector<double>{-3.0, -3.0, -3.0}));
  EXPECT_TRUE((arithmetic_prod.data() == std::vector<double>{10.0, 18.0, 28.0}));
}

TEST_F(TensorTest, Dot) {
  const Tensor dot_result =
      Tensor({3}, {2.0, 3.0, 4.0}).dot(Tensor({3}, {5.0, 6.0, 7.0}));

  EXPECT_TRUE(dot_result.rank() == 0);
  EXPECT_TRUE(dot_result.at({}) == 56.0);

  const Tensor empty_dot = Tensor({0}, {}).dot(Tensor({0}, {}));
  EXPECT_TRUE(empty_dot.rank() == 0);
  EXPECT_TRUE(empty_dot.at({}) == 0);

  bool rejected_matrix_dot = false;

  try {
    const auto invalid = Tensor({1, 2}, {1.0, 2.0}).dot(Tensor({1, 2}, {3.0, 4.0}));
  } catch (const std::invalid_argument&) {
    rejected_matrix_dot = true;
  }
  EXPECT_TRUE(rejected_matrix_dot);

  bool rejected_unequal_lengths = false;

  try {
    const auto invalid = Tensor({2}, {1.0, 2.0}).dot(Tensor({3}, {3.0, 4.0, 5.0}));
  } catch (const std::invalid_argument&) {
    rejected_unequal_lengths = true;
  }
  EXPECT_TRUE(rejected_unequal_lengths);

  // features = [ 4.0, 3.0, 2.0]
  // weights  = [0.5,  -1.0, 2.0]
  // scaled   = [2.0,  -3.0, 4.0]
  // weighted_sum = 3.0
  // bias = 0.5
  // prediction = 3.0 + 0.5 = 3.5
  // pred = weights.dot(features) + bias
}

TEST_F(TensorTest, LinearPrediction) {
  const Tensor features({3}, {4.0, 3.0, 2.0});

  const Tensor weights_({3}, {0.5, -1.0, 2.0});
  const Tensor bias({}, {0.5});

  const Tensor prediction = weights_.dot(features) + bias;
  EXPECT_TRUE(prediction.rank() == 0);
  EXPECT_TRUE(prediction.at({}) == 3.5);

  // 2 observations
  // 3 features

  // 2x3 matrix

  const Tensor inputs({2, 3}, {4.0, 3.0, 2.0, 1.0, 2.0, 0.5});

  const Tensor weights({3, 1}, {0.5, -1.0, 2.0});

  // 3.0
  // -0.5

  const Tensor matmul_23 = inputs.matmul(weights);

  EXPECT_TRUE((matmul_23.shape() == std::vector<std::size_t>{2, 1}));

  EXPECT_TRUE((matmul_23.data() == std::vector<double>{3.0, -0.5}));

  const Tensor pred_23 = matmul_23 + bias;
  EXPECT_TRUE((pred_23.data() == std::vector<double>{3.5, 0.0}));

  const Tensor targets({2, 1}, {2.5, 1.0});

  const Tensor residuals = pred_23 - targets;
  EXPECT_TRUE((residuals.data() == std::vector<double>{1.0, -1.0}));

  const Tensor residuals_total = residuals.sum();  // 1.0 - 1.0 = 0.0

  const Tensor squared_residuals = residuals * residuals;
  EXPECT_TRUE((squared_residuals.data() == std::vector<double>{1.0, 1.0}));

  const Tensor total_squared_error = squared_residuals.sum();
  EXPECT_TRUE(total_squared_error.sum().at({}) == 2);

  const Tensor mean_squared_error = squared_residuals.mean();
  EXPECT_TRUE(mean_squared_error.rank() == 0);
  EXPECT_TRUE(mean_squared_error.sum().at({}) == 1.0);

  const Tensor loss = mse_loss(pred_23, targets);
  EXPECT_TRUE(loss.rank() == 0);
  EXPECT_TRUE(loss.at({}) == 1.0);

  const Tensor perfect_loss = mse_loss(pred_23, pred_23);
  EXPECT_TRUE(perfect_loss.at({}) == 0.0);

  bool rejected_empty_mean = false;
  try {
    static_cast<void>(Tensor({0}, {}).mean());
  } catch (std::invalid_argument&) {
    rejected_empty_mean = true;
  }
  EXPECT_TRUE(rejected_empty_mean);

  const Tensor predictions({2, 1}, {3.5, 0.0});
  const Tensor alias = predictions;
  EXPECT_TRUE(&alias.data() == &predictions.data());
}
```

</details>

> We also changed the graph’s input connections, so I want a test where the two inputs broadcast along different axes. Correct values alone won’t catch a wrong gradient mapping.

Point to `EachParentKeepsItsOwnMultiAxisBroadcastMapping` in the next file. Trace the left shape `[2,1,2]` and right shape `[1,3,1]` to `[2,3,2]`. Keep this one test in view during the explanation; the other gradient checks need no line-by-line tour.

<details>
<summary>Exact code: tests-autograd_test-cpp</summary>

Location: `tests/autograd_test.cpp`.

<!-- edit: tests-autograd_test-cpp file: tests/autograd_test.cpp -->
**Before**
```cpp

```

**After**
```cpp
#include <gtest/gtest.h>

#include <cmath>
#include <functional>
#include <stdexcept>

#include "dlatwd/loss.hpp"
#include "dlatwd/tensor.hpp"

using dlatwd::Tensor;

namespace {
using Expression = std::function<Tensor(const Tensor&)>;

void check_gradient(const Tensor& input, const Expression& expression) {
  Tensor variable(input.shape(), input.data());
  Tensor loss = expression(variable);
  loss.backward();
  constexpr double h = 1e-6;
  for (std::size_t i = 0; i < input.numel(); ++i) {
    SCOPED_TRACE(i);
    Tensor plus(input.shape(), input.data());
    Tensor minus(input.shape(), input.data());
    plus.data()[i] += h;
    minus.data()[i] -= h;
    const double numerical =
        (expression(plus).at({}) - expression(minus).at({})) / (2 * h);
    EXPECT_NEAR(variable.grad()[i], numerical, 1e-5 * (1 + std::abs(numerical)));
  }
}
}  // namespace

TEST(AutogradTest, SharedInputReceivesBothContributions) {
  Tensor x({2}, {2.0, 3.0});
  Tensor loss = (x * x + x).sum();
  loss.backward();
  EXPECT_EQ(x.grad(), (std::vector<double>{5.0, 7.0}));
}

TEST(AutogradTest, RepeatedBackwardAccumulatesLeavesAndResetsIntermediates) {
  Tensor x({}, {3.0});
  Tensor loss = x * x;
  loss.backward();
  loss.backward();
  EXPECT_DOUBLE_EQ(x.grad()[0], 12.0);
  x.zero_grad();
  EXPECT_DOUBLE_EQ(x.grad()[0], 0.0);
  loss.backward();
  EXPECT_DOUBLE_EQ(x.grad()[0], 6.0);
}

TEST(AutogradTest, BroadcastColumnAndRowAccumulateReusedEntries) {
  Tensor a({2, 1}, {2.0, 3.0});
  Tensor b({1, 3}, {4.0, 5.0, 6.0});
  Tensor loss = (a * b).sum();
  loss.backward();
  EXPECT_EQ(a.grad(), (std::vector<double>{15.0, 15.0}));
  EXPECT_EQ(b.grad(), (std::vector<double>{5.0, 5.0, 5.0}));
}

TEST(AutogradTest, ScalarBiasReceivesEveryRow) {
  Tensor input({3}, {1.0, 2.0, 3.0});
  Tensor bias({}, {1.0});
  Tensor loss = (input + bias).sum();
  loss.backward();
  EXPECT_DOUBLE_EQ(bias.grad()[0], 3.0);
}

TEST(AutogradTest, RejectsNonScalarRoot) {
  Tensor x({2}, {1.0, 2.0});
  EXPECT_THROW(x.backward(), std::invalid_argument);
}

TEST(AutogradTest, GraphKeepsTemporaryParentsAlive) {
  Tensor x({}, {3.0});
  Tensor loss = (x * Tensor({}, {2.0})).tanh();
  loss.backward();
  EXPECT_NEAR(x.grad()[0], 2.0 * (1.0 - std::pow(std::tanh(6.0), 2)), 1e-12);
}

TEST(AutogradTest, ArithmeticMatchesFiniteDifferences) {
  check_gradient(Tensor({2}, {1.2, 2.4}), [](const Tensor& x) {
    return ((x * x + x - Tensor({}, {0.5})) / (x + Tensor({}, {2.0}))).sum();
  });
}

TEST(AutogradTest, ExpAndLogMatchFiniteDifferences) {
  check_gradient(Tensor({2}, {0.5, 1.2}),
                 [](const Tensor& x) { return (x.exp() + x.log()).sum(); });
}

TEST(AutogradTest, ActivationsMatchFiniteDifferences) {
  check_gradient(Tensor({3}, {-0.7, 0.4, 1.3}), [](const Tensor& x) {
    return (x.relu() + x.sigmoid() + x.tanh()).sum();
  });
}

TEST(AutogradTest, ReductionsMatchFiniteDifferences) {
  check_gradient(Tensor({2, 3}, {1, 2, 3, 4, 5, 6}), [](const Tensor& x) {
    return (x.sum_columns() * x.sum_columns()).mean();
  });
}

TEST(AutogradTest, MatmulBothOperandsMatchFiniteDifferences) {
  Tensor left({2, 3}, {1, 2, 3, 4, 5, 6});
  Tensor right({3, 2}, {0.1, 0.3, 0.5, 0.7, 0.9, 1.1});
  check_gradient(left, [&](const Tensor& x) { return x.matmul(right).sum(); });
  check_gradient(right, [&](const Tensor& x) { return left.matmul(x).sum(); });
}

TEST(AutogradTest, SoftmaxCrossEntropyMatchesFiniteDifferences) {
  check_gradient(Tensor({2, 3}, {0.2, -0.5, 1.1, 0.4, 0.8, -0.1}), [](const Tensor& x) {
    return dlatwd::cross_entropy_loss(dlatwd::softmax(x), {2, 1});
  });
}

TEST(AutogradTest, SoftmaxNormalizesEachRow) {
  auto probabilities = dlatwd::softmax(Tensor({2, 3}, {1, 2, 3, -1, 0, 1}));
  auto totals = probabilities.sum_columns();
  for (double value : totals.data()) EXPECT_NEAR(value, 1.0, 1e-12);
}

TEST(AutogradTest, RejectsInvalidLogAndZeroDivision) {
  EXPECT_THROW((void)Tensor({}, {0.0}).log(), std::domain_error);
  EXPECT_THROW((void)(Tensor({}, {1.0}) / Tensor({}, {0.0})), std::domain_error);
}

TEST(AutogradTest, EachParentKeepsItsOwnMultiAxisBroadcastMapping) {
  Tensor left({2, 1, 2}, {1, 2, 3, 4});
  Tensor right({1, 3, 1}, {10, 20, 30});
  Tensor product = left * right;
  EXPECT_EQ(product.shape(), (std::vector<std::size_t>{2, 3, 2}));
  EXPECT_EQ(product.data(), (std::vector<double>{
      10, 20, 20, 40, 30, 60, 30, 40, 60, 80, 90, 120}));
  product.sum().backward();
  EXPECT_EQ(left.grad(), (std::vector<double>{60, 60, 60, 60}));
  EXPECT_EQ(right.grad(), (std::vector<double>{10, 10, 10}));
}
```

</details>

> Each left value multiplies all three right values, so its gradient is ten plus twenty plus thirty. Each right value multiplies all four left values, so its gradient is ten. This checks both mappings and the accumulation into reused inputs.

The remaining regression checks are included in the exact code below. They verify shared parameter storage, updates, and XOR learning. They are verification coverage, not new model implementation or an extra lesson to narrate.

<details>
<summary>Exact code: tests-training_test-cpp</summary>

Location: `tests/training_test.cpp`.

<!-- edit: tests-training_test-cpp file: tests/training_test.cpp -->
**Before**
```cpp

```

**After**
```cpp
#include <gtest/gtest.h>

#include <random>

#include "dlatwd/loss.hpp"
#include "dlatwd/nn.hpp"

using dlatwd::Tensor;

TEST(TrainingTest, ParametersReferToTheActualLayerStorage) {
  std::mt19937 random(42);
  dlatwd::Linear layer(2, 1, random);
  auto parameters = layer.parameters();
  ASSERT_EQ(parameters.size(), 2);
  EXPECT_EQ(parameters[0].shape(), (std::vector<std::size_t>{2, 1}));
  EXPECT_EQ(parameters[1].shape(), (std::vector<std::size_t>{1}));
  parameters[0].data() = {2, 3};
  parameters[1].data() = {1};
  EXPECT_DOUBLE_EQ(layer.forward(Tensor({1, 2}, {4, 5})).at({0, 0}), 24.0);
}

TEST(TrainingTest, MlpCollectsBothLayers) {
  std::mt19937 random(42);
  dlatwd::MLP model(2, 4, 1, random);
  auto parameters = model.parameters();
  ASSERT_EQ(parameters.size(), 4);
  EXPECT_EQ(parameters[0].shape(), (std::vector<std::size_t>{2, 4}));
  EXPECT_EQ(parameters[1].shape(), (std::vector<std::size_t>{4}));
  EXPECT_EQ(parameters[2].shape(), (std::vector<std::size_t>{4, 1}));
  EXPECT_EQ(parameters[3].shape(), (std::vector<std::size_t>{1}));
}

TEST(TrainingTest, GradientStepUpdatesParameters) {
  Tensor weights({2}, {2, 3});
  Tensor loss = (weights * weights).sum();
  loss.backward();
  std::vector<Tensor> parameters{weights};
  dlatwd::gradient_step(parameters, 0.1);
  EXPECT_NEAR(weights.data()[0], 1.6, 1e-12);
  EXPECT_NEAR(weights.data()[1], 2.4, 1e-12);
}

TEST(TrainingTest, LearnsXorWithoutDatasetFiles) {
  std::mt19937 random(42);
  dlatwd::MLP model(2, 4, 1, random);
  const Tensor inputs({4, 2}, {0, 0, 0, 1, 1, 0, 1, 1});
  const Tensor targets({4, 1}, {0, 1, 1, 0});
  auto parameters = model.parameters();
  for (std::size_t step = 0; step < 5000; ++step) {
    for (auto& parameter : parameters) parameter.zero_grad();
    Tensor loss = dlatwd::mse_loss(model.forward(inputs), targets);
    loss.backward();
    dlatwd::gradient_step(parameters, 0.1);
  }
  const Tensor predictions = model.forward(inputs);
  EXPECT_LT(dlatwd::mse_loss(predictions, targets).at({}), 0.01);
  for (std::size_t i = 0; i < 4; ++i)
    EXPECT_EQ(predictions.data()[i] > 0.5, targets.data()[i] > 0.5);
}
```

</details>

## D. Build the library, examples and tests with CMake

> We now have several source files and several programs that use them. CMake will build the library once, then link each example and the test executable against it.

Create `CMakeLists.txt`. Write the library target first. The empty Before block means a new file.

Location: `CMakeLists.txt`.

<!-- edit: cmake-library file: CMakeLists.txt -->
**Before**
```cpp

```

**After**
```cpp
cmake_minimum_required(VERSION 3.24)
project(dlatwd VERSION 0.1.0 LANGUAGES CXX)

set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
option(DLATWD_BUILD_EXAMPLES "Build the standalone learning examples" ON)
option(DLATWD_SANITIZERS "Enable AddressSanitizer and UndefinedBehaviorSanitizer" OFF)

if(DLATWD_SANITIZERS)
  if(NOT CMAKE_CXX_COMPILER_ID MATCHES "Clang|GNU")
    message(FATAL_ERROR "The sanitizer option requires Clang or GCC")
  endif()
  add_compile_options(-fsanitize=address,undefined -fno-omit-frame-pointer)
  add_link_options(-fsanitize=address,undefined)
endif()

add_library(dlatwd STATIC src/tensor.cpp src/nn.cpp src/losses.cpp)
add_library(dlatwd::dlatwd ALIAS dlatwd)
target_compile_features(dlatwd PUBLIC cxx_std_23)
target_include_directories(dlatwd PUBLIC "${CMAKE_CURRENT_SOURCE_DIR}/include")
if(MSVC)
  target_compile_options(dlatwd PRIVATE /W4)
else()
  target_compile_options(dlatwd PRIVATE -Wall -Wextra -Wpedantic)
endif()
```

> The library target owns the three source files. Public include directories and the C++23 requirement follow it to anything that links against it. GoogleTest will only be a test dependency; the library itself still uses the standard library.

Append the example targets after the warning-options block:

Location: `CMakeLists.txt`.

<!-- edit: cmake-examples file: CMakeLists.txt -->
**Before**
```cpp
if(MSVC)
  target_compile_options(dlatwd PRIVATE /W4)
else()
  target_compile_options(dlatwd PRIVATE -Wall -Wextra -Wpedantic)
endif()
```

**After**
```cpp
if(MSVC)
  target_compile_options(dlatwd PRIVATE /W4)
else()
  target_compile_options(dlatwd PRIVATE -Wall -Wextra -Wpedantic)
endif()

if(DLATWD_BUILD_EXAMPLES)
  foreach(example IN ITEMS mnist xor regression)
    add_executable(${example} examples/${example}.cpp)
    target_link_libraries(${example} PRIVATE dlatwd::dlatwd)
  endforeach()
  # Preserve the independent scalar-autograd lesson, including its assertions.
  add_executable(scalar_autograd examples/scalar_autograd.cpp)
  target_compile_features(scalar_autograd PRIVATE cxx_std_23)
  if(MSVC)
    target_compile_options(scalar_autograd PRIVATE /UNDEBUG)
  else()
    target_compile_options(scalar_autograd PRIVATE -UNDEBUG)
  endif()
endif()
```

> Each example gets its own executable linked to dlatwd. Scalar autograd stays independent, and we keep its original assertions enabled even in Release.

Append the test setup after the examples block:

Location: `CMakeLists.txt`.

<!-- edit: cmake-tests file: CMakeLists.txt -->
**Before**
```cpp
if(DLATWD_BUILD_EXAMPLES)
  foreach(example IN ITEMS mnist xor regression)
    add_executable(${example} examples/${example}.cpp)
    target_link_libraries(${example} PRIVATE dlatwd::dlatwd)
  endforeach()
  # Preserve the independent scalar-autograd lesson, including its assertions.
  add_executable(scalar_autograd examples/scalar_autograd.cpp)
  target_compile_features(scalar_autograd PRIVATE cxx_std_23)
  if(MSVC)
    target_compile_options(scalar_autograd PRIVATE /UNDEBUG)
  else()
    target_compile_options(scalar_autograd PRIVATE -UNDEBUG)
  endif()
endif()
```

**After**
```cpp
if(DLATWD_BUILD_EXAMPLES)
  foreach(example IN ITEMS mnist xor regression)
    add_executable(${example} examples/${example}.cpp)
    target_link_libraries(${example} PRIVATE dlatwd::dlatwd)
  endforeach()
  # Preserve the independent scalar-autograd lesson, including its assertions.
  add_executable(scalar_autograd examples/scalar_autograd.cpp)
  target_compile_features(scalar_autograd PRIVATE cxx_std_23)
  if(MSVC)
    target_compile_options(scalar_autograd PRIVATE /UNDEBUG)
  else()
    target_compile_options(scalar_autograd PRIVATE -UNDEBUG)
  endif()
endif()

include(CTest)
if(BUILD_TESTING)
  include(FetchContent)
  # GoogleTest 1.17.0. Tests only: never linked into the library/examples.
  FetchContent_Declare(googletest
    URL https://github.com/google/googletest/archive/52eb8108c5bdec04579160ae17225d66034bd723.zip
    DOWNLOAD_EXTRACT_TIMESTAMP TRUE)
  set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
  set(BUILD_GMOCK OFF CACHE BOOL "" FORCE)
  set(INSTALL_GTEST OFF CACHE BOOL "" FORCE)
  FetchContent_MakeAvailable(googletest)
  add_executable(dlatwd_tests
    tests/tensor_test.cpp tests/autograd_test.cpp tests/training_test.cpp)
  target_link_libraries(dlatwd_tests PRIVATE dlatwd::dlatwd GTest::gtest_main)
  include(GoogleTest)
  gtest_discover_tests(dlatwd_tests DISCOVERY_MODE PRE_TEST)
endif()
```

> We pin GoogleTest to one revision, link its test runner to our tests, and let CTest discover their names. We can disable tests without downloading GoogleTest at all.

Configure, build, and run the named tests:

> Let’s build this split version and run the tests. We should get the same behavior without starting MNIST training.

```sh
cmake -S . -B build/debug -G Ninja -DCMAKE_BUILD_TYPE=Debug
cmake --build build/debug -j 4
ctest --test-dir build/debug --output-on-failure
```

<!-- checkpoint: split-library-complete -->

Expected test summary on the checked code:

```text
100% tests passed, 0 tests failed out of 41
```

> The tests pass independently now. To check a whole training example, we can run XOR directly from the same build.

```sh
./build/debug/xor
```

Expected local output:

```text
Loss: 0.779 -> 0.000
a b prediction target
0.000 0.000 0.000 0.000
0.000 1.000 1.000 1.000
1.000 0.000 1.000 1.000
1.000 1.000 0.000 0.000
```

## E. Keep the build and editor setup repeatable

> Rather than retype those build options, we’ll save Debug, Release and sanitizer presets. They use separate directories, so an optimized training build won’t replace the one we use for debugging.

<details>
<summary>Exact code: CMakePresets-json</summary>

Location: `CMakePresets.json`.

<!-- edit: CMakePresets-json file: CMakePresets.json -->
**Before**
```cpp

```

**After**
```cpp
{
  "version": 5,
  "cmakeMinimumRequired": { "major": 3, "minor": 24, "patch": 0 },
  "configurePresets": [
    {
      "name": "debug",
      "generator": "Ninja",
      "binaryDir": "${sourceDir}/build/debug",
      "cacheVariables": { "CMAKE_BUILD_TYPE": "Debug", "BUILD_TESTING": "ON" }
    },
    {
      "name": "release",
      "inherits": "debug",
      "binaryDir": "${sourceDir}/build/release",
      "cacheVariables": { "CMAKE_BUILD_TYPE": "Release" }
    },
    {
      "name": "sanitizers",
      "inherits": "debug",
      "binaryDir": "${sourceDir}/build/sanitizers",
      "cacheVariables": { "DLATWD_SANITIZERS": "ON" }
    }
  ],
  "buildPresets": [
    { "name": "debug", "configurePreset": "debug" },
    { "name": "release", "configurePreset": "release" },
    { "name": "sanitizers", "configurePreset": "sanitizers" }
  ],
  "testPresets": [
    { "name": "debug", "configurePreset": "debug", "output": { "outputOnFailure": true } },
    { "name": "release", "configurePreset": "release", "output": { "outputOnFailure": true } },
    { "name": "sanitizers", "configurePreset": "sanitizers", "output": { "outputOnFailure": true } }
  ]
}
```

</details>

Use these equivalent preset commands from now on:

```sh
cmake --preset debug
cmake --build --preset debug -j 4
ctest --preset debug
```

> CMake also writes the compilation database. Linking it at the project root lets clangd find the same include paths and compiler flags as the build.

Create this link once if it does not already exist; then restart clangd in the editor:

```sh
ln -s build/debug/compile_commands.json compile_commands.json
```

In `.gitignore`, extend the first two entries as follows. Preserve any entries
below this block in your checkout.

**Before**

```gitignore
main
scalar_main
```

**After**

```gitignore
main
scalar_main
/build/
/compile_commands.json
/.cache/
```

For the final training check, use Release. Keep only the result on screen if the run takes time:

```sh
cmake --preset release
cmake --build --preset release -j 4
./build/release/mnist
```

<!-- checkpoint: final-release -->

> The MNIST example still reaches the same result on this machine. We’ve changed how the code is organized and initialized, without changing the training calculation.

## F. Recap

Show:

```text
Recap
- Parent nodes carry their broadcast mappings
- Constructors finish node initialization
- Library code is separate from examples
- GoogleTest checks behavior independently
- CMake builds each target
```

> Our tensors now leave construction with their graph history in place, and we can build and test the library without running an entire training example. We have clearer places to add the next operation or layer, and checks to catch regressions when we do.

Replace the recap with:

```text
Next steps
- More flexible layer composition
- Cleaner operation dispatch
- Save and reload model parameters
```

> The next design work can focus on composing layers and adding operations. Saving the trained parameters is still on the list, too.

> That brings us to the end of this episode. Thanks for watching, and I will see you next time.

Leave approximately five clean seconds for the Subscribe and complete-series playlist end-screen elements.
