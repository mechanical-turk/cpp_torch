Proposed MP4: `cpp-relu-sigmoid-tanh-autograd-activation-functions.mp4`

# Episode 10: Building ReLU, Sigmoid and Tanh in C++

Start in the existing `main.cpp`. Read the `>` passages aloud. Use the Before/After
blocks to locate each edit; the passages marked "While writing" accompany the
named lines as you type them.

## A. Build ReLU in both directions | 0:00-3:45

Frame zero shows inputs passing through two boxes labeled `Linear`, then a
prediction. As the narration explains how the layers combine, collapse the
boxes into one. Show the corresponding calculation underneath:

```text
(xW₁ + b₁)W₂ + b₂

x(W₁W₂) + (b₁W₂ + b₂)
```

Beside the equation, show one straight line missing a curved set of points.
Then transform the same five values used later in code:

```text
[-2, -1, 0, 1, 2]
          ReLU
[ 0,  0, 0, 1, 2]
```

Begin speaking on frame zero. Cut to `main.cpp` around 0:20, during the ReLU
sentence. Start its method by approximately 0:30.

> A deep neural network can still behave like a single linear layer if every layer just multiplies by weights and adds a bias. Because we can just combine those calculations into one. We need nonlinear activation functions for the extra layers to let us model more complex relationships.
>
> We'll build them in C++, starting with ReLU. ReLU keeps positive values and turns negative values into zero.

Show the five-value ReLU transformation while saying what it does. Move directly
to `Operation`, then the public methods of `Tensor` above `sum()`.

> We'll make a method called `relu`, so we can apply it to any Tensor. It also needs an operation label so autograd knows which backward rule to use.

<!-- edit: activation-operation-labels -->
**Before**
```cpp
  divide,
  sum,
  matmul
};
```

**After**
```cpp
  divide,
  sum,
  matmul,
  relu
};
```

<!-- edit: relu-forward -->
**Before**
```cpp
  [[nodiscard]] Tensor sum() const {
```

**After**
```cpp
  [[nodiscard]] Tensor relu() const {
    return elementwise_unary(
      Operation::relu,
      [](double value) {
        return std::max(0.0, value);
      }
    );
  }

  [[nodiscard]] Tensor sum() const {
```

While writing the call and lambda:

> I'll pass the ReLU label and a function that takes the larger of zero and the input. We need to apply it to every element, so I'm putting the loop and graph setup in a helper called `elementwise_unary`. Unary just means it takes one input.

Continue directly to the private section above `elementwise_binary()`. The helper
is the next edit; do not compile this incomplete fragment.

> Let's write the helper we just called. Each input value produces one output value, so we can keep the same shape. We'll fill a new array and connect the result back to this Tensor.

<!-- edit: unary-forward-helper -->
**Before**
```cpp
  [[nodiscard]] Tensor elementwise_binary(
    const Tensor& other,
    Operation kind,
    const auto& operation
  ) const {
```

**After**
```cpp
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

    Tensor result(node_->shape, std::move(result_data));
    result.node_->operation = kind;
    result.node_->parents = {node_};
    return result;
  }

  [[nodiscard]] Tensor elementwise_binary(
    const Tensor& other,
    Operation kind,
    const auto& operation
  ) const {
```

While allocating `result_data` and writing `std::transform`:

> I'll allocate one result slot per element. `std::transform` walks the input array, calls our lambda on each value, and writes into these slots.

While constructing `result` and setting its node fields:

> Now we can move the array into a Tensor with the original shape. I'll save the operation label and this input node as its parent, so backward can follow the connection when it reaches the result.

Move to the private section immediately above `backward_elementwise()`.

> To train through ReLU, we need to send gradients back along that connection. Since we kept every value in the same position, each output gradient goes to the input at the same index. We'll write another helper to do this, with a local derivative supplied by the activation.

<!-- edit: unary-backward-helper -->
**Before**
```cpp
  static void backward_elementwise(
    TensorNode* output,
    const auto& local_derivatives
  ) {
```

**After**
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

  static void backward_elementwise(
    TensorNode* output,
    const auto& local_derivatives
  ) {
```

While retrieving `input` and writing the loop:

> I'll get the input from the parent we saved, then visit each output position. We already know how the loss changes with this output. To work back to the input, we multiply by the activation's slope here. This is the chain rule.

While writing the derivative call and `+=`:

> The derivative function gets the input and output values, so it can use whichever its formula needs. I'll add the contribution to the input's gradient because the same Tensor may also receive gradients through another path.

Move to `backward()` and add the ReLU case immediately above `default`.

> For ReLU, the slope depends on whether the input is positive. Let's give backward a ReLU case that passes this rule to our helper.

<!-- edit: relu-backward -->
**Before**
```cpp
        default:
          throw std::logic_error("backward rule not implemented yet");
```

**After**
```cpp
        case Operation::relu:
          backward_unary(
            output,
            [](double input, double) {
              return input > 0.0 ? 1.0 : 0.0;
            }
          );
          break;

        default:
          throw std::logic_error("backward rule not implemented yet");
```

At the condition:

> On the positive side, increasing the input increases the output by the same amount, so we return one. On the negative side, the output stays at zero, so we return zero. The slope is undefined at the corner itself; we'll use zero there too.

Add a small table immediately below `linear_forward()`. This function remains
in the final program and will gain two more columns later.

> We've added both directions, so let's try ReLU on the five values from the opening. I'll put the input beside the output so we can see exactly which values changed.

<!-- edit: relu-table -->
**Before**
```cpp
[[nodiscard]] Tensor linear_forward(
  const Tensor& inputs,
  const Tensor& weights,
  const Tensor& bias
) {
  return inputs.matmul(weights) + bias;
}

void gradient_step(
```

**After**
```cpp
[[nodiscard]] Tensor linear_forward(
  const Tensor& inputs,
  const Tensor& weights,
  const Tensor& bias
) {
  return inputs.matmul(weights) + bias;
}

void show_activations() {
  const Tensor inputs({5}, {-2.0, -1.0, 0.0, 1.0, 2.0});
  const Tensor relu_outputs = inputs.relu();

  std::cout << "x relu\n";
  for (std::size_t index = 0; index < inputs.numel(); ++index) {
    std::cout
      << inputs.at({index}) << ' '
      << relu_outputs.at({index}) << '\n';
  }
}

void gradient_step(
```

While writing `show_activations()`:

> I'll create the input Tensor, call `relu`, and print the two values at each position. We'll keep this table to compare the other activations as we add them.

Move to the end of `main()`, immediately before the existing training example.

> Let's call it from main so the comparison appears when we run the program.

<!-- edit: call-activation-table -->
**Before**
```cpp
  train_line();

  std::cout << "Success!\n";
```

**After**
```cpp
  show_activations();
  train_line();

  std::cout << "Success!\n";
```

Before running:

> We should get zeros for the first three inputs, then one and two unchanged. Let's run it.

<!-- checkpoint: relu-complete -->

```text
x relu
-2 0
-1 0
0 0
1 1
2 2
```

> So ReLU does what we expected. But sometimes we need more control over the output range. If a model is predicting a probability, for example, we need a value between zero and one. Sigmoid lets us take any real-valued input and map it into that range.

## B. Add sigmoid in both directions | 3:45-6:00

Show `sigmoid(x) = 1 / (1 + exp(-x))` beside the code during the forward edit.

> It does this smoothly. Extremely negative values will tend towards zero, and extremely positive values will tend towards one, and everything in between, will sit somewhere between zero and one. 
> 
> So let's add a `sigmoid` method to our Tensor. We can reuse the helper we just wrote and give it this formula.

Add `<cmath>` for `std::exp`, then the sigmoid operation label. These are part
of the forward edit; continue directly to the public methods above `sum()`.

<!-- edit: include-cmath -->
**Before**
```cpp
#include <cassert>
#include <memory>
```

**After**
```cpp
#include <cassert>
#include <cmath>
#include <memory>
```

<!-- edit: sigmoid-operation-label -->
**Before**
```cpp
  matmul,
  relu
};
```

**After**
```cpp
  matmul,
  relu,
  sigmoid
};
```

<!-- edit: sigmoid-forward -->
**Before**
```cpp
  [[nodiscard]] Tensor relu() const {
    return elementwise_unary(
      Operation::relu,
      [](double value) {
        return std::max(0.0, value);
      }
    );
  }

  [[nodiscard]] Tensor sum() const {
```

**After**
```cpp
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

  [[nodiscard]] Tensor sum() const {
```

While writing the lambda:

> I'll use `std::exp` for the exponential and pass the formula to `elementwise_unary`. The helper will apply it across the Tensor and save the graph connection, just as it does for ReLU.

Add its backward case after ReLU.

> For backward, sigmoid has a useful shortcut. Its derivative is the output times one minus the output, and we've already stored those values. We can use them directly in the new case.

<!-- edit: sigmoid-backward -->
**Before**
```cpp
        case Operation::relu:
          backward_unary(
            output,
            [](double input, double) {
              return input > 0.0 ? 1.0 : 0.0;
            }
          );
          break;

        default:
```

**After**
```cpp
        case Operation::relu:
          backward_unary(
            output,
            [](double input, double) {
              return input > 0.0 ? 1.0 : 0.0;
            }
          );
          break;

        case Operation::sigmoid:
          backward_unary(
            output,
            [](double, double result) {
              return result * (1.0 - result);
            }
          );
          break;

        default:
```

While writing the derivative lambda, keep `y(1 - y)` visible beside it.

> I'll use the second argument, `result`, for the saved output. Returning `result` times `1 - result` gives the helper the local slope; it handles multiplying by the incoming gradient.

Add sigmoid to the table.

> Both sigmoid rules are in place. Let's add its output beside ReLU's so we can compare them on the same inputs.

<!-- edit: sigmoid-table -->
**Before**
```cpp
void show_activations() {
  const Tensor inputs({5}, {-2.0, -1.0, 0.0, 1.0, 2.0});
  const Tensor relu_outputs = inputs.relu();

  std::cout << "x relu\n";
  for (std::size_t index = 0; index < inputs.numel(); ++index) {
    std::cout
      << inputs.at({index}) << ' '
      << relu_outputs.at({index}) << '\n';
  }
}
```

**After**
```cpp
void show_activations() {
  const Tensor inputs({5}, {-2.0, -1.0, 0.0, 1.0, 2.0});
  const Tensor relu_outputs = inputs.relu();
  const Tensor sigmoid_outputs = inputs.sigmoid();

  std::cout << "x relu sigmoid\n";
  for (std::size_t index = 0; index < inputs.numel(); ++index) {
    std::cout
      << inputs.at({index}) << ' '
      << relu_outputs.at({index}) << ' '
      << sigmoid_outputs.at({index}) << '\n';
  }
}
```

While adding the new output and print column:

> I'll call `sigmoid` on the same Tensor and print one more column for each input.

Before running:

> The new column should stay between zero and one, with zero mapping to one half. Let's run it.

<!-- checkpoint: sigmoid-complete -->

```text
x relu sigmoid
-2 0 0.119203
-1 0 0.268941
0 0 0.5
1 1 0.731059
2 2 0.880797
```

> All of these outputs are positive, which makes sense for a probability. But if our model is controlling a steering wheel, we need to represent both directions. We could use negative values for left, positive values for right, and zero for straight ahead. Tanh gives us a smooth curve centered on zero, with outputs between negative one and one.

## C. Add tanh in both directions | 6:00-8:00

> Let's add tanh alongside sigmoid so we can compare them on the same inputs. C++ provides the calculation as `std::tanh`; we'll use it in our forward method, then add the derivative for backward.

Add its operation label, then `tanh()` between `sigmoid()` and `sum()`.

<!-- edit: tanh-operation-label -->
**Before**
```cpp
  relu,
  sigmoid
};
```

**After**
```cpp
  relu,
  sigmoid,
  tanh
};
```

<!-- edit: tanh-forward -->
**Before**
```cpp
  [[nodiscard]] Tensor sigmoid() const {
    return elementwise_unary(
      Operation::sigmoid,
      [](double value) {
        return 1.0 / (1.0 + std::exp(-value));
      }
    );
  }

  [[nodiscard]] Tensor sum() const {
```

**After**
```cpp
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

  [[nodiscard]] Tensor sum() const {
```

While writing the call to `std::tanh`:

> I'll pass each value to `std::tanh` inside the lambda. The helper handles the Tensor and its parent connection, and `Operation::tanh` records which calculation we used.

Add the backward case after sigmoid.

> We've recorded tanh in the graph, so let's give backward a case for it. We can calculate its derivative from the saved output, just as we did for sigmoid. For tanh, it's one minus the output squared.

<!-- edit: tanh-backward -->
**Before**
```cpp
        case Operation::sigmoid:
          backward_unary(
            output,
            [](double, double result) {
              return result * (1.0 - result);
            }
          );
          break;

        default:
```

**After**
```cpp
        case Operation::sigmoid:
          backward_unary(
            output,
            [](double, double result) {
              return result * (1.0 - result);
            }
          );
          break;

        case Operation::tanh:
          backward_unary(
            output,
            [](double, double result) {
              return 1.0 - result * result;
            }
          );
          break;

        default:
```

While writing the derivative, show `1 - y²` beside the lambda and the tanh
curve, highlighting its flatter ends as they are mentioned.

> We'll return one minus `result` squared. Near either end of the curve, the output is close to negative one or one, so its square is close to one and the derivative is small. Moving the input barely changes the output there, which matches the flat ends we can see.

Complete the table.

> Both directions are in place. Let's return to our comparison table and add a tanh column so we can see the difference from sigmoid.

<!-- edit: tanh-table -->
**Before**
```cpp
void show_activations() {
  const Tensor inputs({5}, {-2.0, -1.0, 0.0, 1.0, 2.0});
  const Tensor relu_outputs = inputs.relu();
  const Tensor sigmoid_outputs = inputs.sigmoid();

  std::cout << "x relu sigmoid\n";
  for (std::size_t index = 0; index < inputs.numel(); ++index) {
    std::cout
      << inputs.at({index}) << ' '
      << relu_outputs.at({index}) << ' '
      << sigmoid_outputs.at({index}) << '\n';
  }
}
```

**After**
```cpp
void show_activations() {
  const Tensor inputs({5}, {-2.0, -1.0, 0.0, 1.0, 2.0});
  const Tensor relu_outputs = inputs.relu();
  const Tensor sigmoid_outputs = inputs.sigmoid();
  const Tensor tanh_outputs = inputs.tanh();

  std::cout << "x relu sigmoid tanh\n";
  for (std::size_t index = 0; index < inputs.numel(); ++index) {
    std::cout
      << inputs.at({index}) << ' '
      << relu_outputs.at({index}) << ' '
      << sigmoid_outputs.at({index}) << ' '
      << tanh_outputs.at({index}) << '\n';
  }
}
```

While adding `tanh_outputs` and its print column:

> I'll call tanh on the same inputs and print its values beside sigmoid.

Before running:

> This time, the negative inputs should give negative outputs, and zero should stay at zero. Let's run it.

<!-- checkpoint: activations-complete -->

```text
x relu sigmoid tanh
-2 0 0.119203 -0.964028
-1 0 0.268941 -0.761594
0 0 0.5 0
1 1 0.731059 0.761594
2 2 0.880797 0.964028
```

> We get the signed outputs we wanted, with zero in the middle. So far, we've been feeding numbers straight into these functions. Let's use tanh in a model now and see whether training can fit a curve instead of a straight line.

## D. Train a nonlinear regression | 8:00-12:30

Return to `linear_forward()`.

> Our `linear_forward` function already calculates the weighted inputs plus the bias. If we apply tanh to its result, changing the weight and bias will change the shape and position of the curve. Let's make that change here and rename the function `nonlinear_forward`.

<!-- edit: nonlinear-forward -->
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
[[nodiscard]] Tensor nonlinear_forward(
  const Tensor& inputs,
  const Tensor& weights,
  const Tensor& bias
) {
  return (inputs.matmul(weights) + bias).tanh();
}
```

While changing the name and return expression:

> I'll wrap the existing expression in parentheses so tanh runs after we add the bias. For our one-input example, the prediction is now tanh of weight times input plus bias.

Update the training function to call the nonlinear model.

> To train this version, we need the loop to get its predictions from `nonlinear_forward`. Let's replace the call and rename the training function to `train_nonlinear_regression`.

<!-- edit: nonlinear-training-loop -->
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
    gradient_step(weights, bias, learning_rate);
  }
}
```

**After**
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
    gradient_step(weights, bias, learning_rate);
  }
}
```

While changing the call inside the loop, point to `loss.backward()`:

> We can leave the rest of the loop alone. Mean squared error still measures how far the predictions are from the targets. Backward follows the graph through tanh using the derivative we just added, so it can still calculate the weight and bias gradients for our update.

Replace the existing line example with nine samples from
`y = tanh(2x + 1)`.

> The loop is ready, but our example still contains points on a straight line. Let's replace them with nine points from tanh of two x plus one. We know which weight and bias produced this curve, so we can check whether training learns them from the points.

<!-- edit: nonlinear-example -->
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

  Tensor weight({1, 1}, {0.0});
  Tensor bias({}, {0.0});

  train_nonlinear_regression(inputs, targets, weight, bias, 10000, 0.05);

  std::cout << "Weight: " << weight.at({0, 0}) << " \n";
  std::cout << "Bias: " << bias.at({}) << " \n";
}
```

At the inputs and targets:

> I'll keep one input per row, running from negative one to one. Beside them, we'll put the corresponding targets from our formula. These values are rounded, but they're enough to check the fit without adding any data-loading code.

At the initialization:

> We'll start the weight and bias at zero, so training has to find them. I'll pass both into `train_nonlinear_regression` for ten thousand steps, with a learning rate of point zero five.

While adding the weight and bias output:

> Let's print the learned weight and bias so we can put them back into our formula and see which curve we've fitted.

Update the call in `main()`.

> We've replaced the line example with `train_curve`. Let's update main to call it.

<!-- edit: call-nonlinear-example -->
**Before**
```cpp
  show_activations();
  train_line();

  std::cout << "Success!\n";
```

**After**
```cpp
  show_activations();
  train_curve();

  std::cout << "Success!\n";
```

Before running, keep `y = tanh(weight * x + bias)` visible.

> Let's run it and see where the weight and bias ended up.

<!-- checkpoint: nonlinear-training -->

```text
Weight: 2
Bias: 1
```

Immediately substitute the printed parameters into the formula on screen:

```text
y = tanh(weight * x + bias)
y = tanh(2x + 1)
```

> We got a weight of two and a bias of one, so our fitted curve is tanh of two x plus one. It's the same curve we used to create the targets. Training only had the nine input and target pairs, and it recovered those parameters, to the precision we're printing.

## E. Recap | 12:30-13:05

Show:

```text
Recap

- Unary Tensor operations
- ReLU, sigmoid and tanh
- Activation backward rules
- Nonlinear regression
```

> We built ReLU, sigmoid, and tanh on shared unary helpers, with a backward rule for each one. Then we used tanh in our regression model and trained it on a curved set of points.

Replace the recap with:

```text
Next episode

- Build neural-network modules
- Compose linear and activation layers
- Train our first MLP
```

> One tanh unit can only fit a limited family of curves. To learn more complex patterns, we'll need to combine several units into a network. In the next episode, we'll build linear and activation modules to make those combinations easier to work with, then train our first multilayer perceptron.

> That brings us to the end of this episode. Thanks for watching, and I will see you next time.

Cut to approximately five clean seconds for the Subscribe and complete-series
playlist end-screen elements.
