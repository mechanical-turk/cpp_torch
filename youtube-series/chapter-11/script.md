MP4 filename: `cpp-neural-network-modules-mlp-xor-from-scratch.mp4`

# Episode 11: Building Our First Neural Network in C++

Continue in the same `main.cpp` used for Episode 10. Keep the existing Tensor,
autograd engine, examples and tests. Read only the `>` passages aloud.
Before/After blocks show the exact edits; checkpoint notes are not narration.

## A. Give a linear layer its own parameters | 0:00-3:30

Frame zero: show the four rows below. Place the matching points on a small
two-dimensional plot, with the two output classes in different colors. Speak
immediately; do not show a title card first.

```text
a b   target
0 0     0
0 1     1
1 0     1
1 1     0
```

> These four rows are XOR: one when the inputs differ, zero when they match. No single straight boundary can separate the ones from the zeros. We're going to train a small neural network in C++ to do this, with layers we can reuse.

Move to the end of `Tensor`, immediately before `mse_loss()`, by about 0:20.
Keep a small `inputs -> Linear -> outputs` sketch beside the code.

> Each linear layer needs its own weights and biases. Let's put them in a class with a forward method, so we can create several layers without passing separate parameters around every time.

<!-- edit: linear-forward -->
**Before**
```cpp
[[nodiscard]] Tensor mse_loss(
```

**After**
```cpp
class Linear {
public:
  [[nodiscard]] Tensor forward(const Tensor& inputs) const {
    return inputs.matmul(weight_) + bias_;
  }

private:
  Tensor weight_;
  Tensor bias_;
};

[[nodiscard]] Tensor mse_loss(
```

While writing `forward()`:

> The calculation stays the same: multiply the inputs by the weights, then add the bias. We'll give the weight matrix one column per output, so this same method can produce several values for each input row.

Show the shape relationship beside the return expression, without leaving code:

```text
inputs [batch, in] @ weights [in, out] + bias [out]
                              -> [batch, out]
```

> Each output gets its own bias, and broadcasting reuses those biases across the batch. For our hidden layer, two input features will become four outputs.

Point to `weight_` and `bias_`.

> To create a layer, we'll supply its input and output sizes. The constructor will allocate the matching Tensors. We'll keep the biases at zero, but identical weights would make the hidden units produce the same values and receive the same updates. We'll give them different random weights so they can learn different features.

At the include list, add the random-number header. Do not narrate the include.

<!-- edit: random-include -->
**Before**
```cpp
#include <unordered_set>
```

**After**
```cpp
#include <unordered_set>
#include <random>
```

Return to the start of `Linear`. The constructor calls the helper implemented
immediately afterward; do not compile between these two edits.

<!-- edit: linear-constructor -->
**Before**
```cpp
class Linear {
public:
  [[nodiscard]] Tensor forward(const Tensor& inputs) const {
    return inputs.matmul(weight_) + bias_;
  }
```

**After**
```cpp
class Linear {
public:
  Linear(
    std::size_t in_features,
    std::size_t out_features,
    std::mt19937& random
  ) : weight_(random_weights(in_features, out_features, random)),
      bias_({out_features}, std::vector<double>(out_features, 0.0)) {}

  [[nodiscard]] Tensor forward(const Tensor& inputs) const {
    return inputs.matmul(weight_) + bias_;
  }
```

While writing the initializer list:

> I'll create the weight matrix with a helper that fills it with random values. The bias only needs one entry per output. We'll pass the random generator in, so creating the next layer continues drawing new values instead of restarting the sequence.

Continue in `Linear`'s private section, below its two Tensor members.

> Let's write that helper now. It needs one value for every input-output connection. We'll sample around zero, with the range scaled by the number of inputs so larger layers don't start with unnecessarily large values.

<!-- edit: random-weights -->
**Before**
```cpp
  Tensor weight_;
  Tensor bias_;
};
```

**After**
```cpp
  Tensor weight_;
  Tensor bias_;

  [[nodiscard]] static Tensor random_weights(
    std::size_t in_features,
    std::size_t out_features,
    std::mt19937& random
  ) {
    if (in_features == 0 || out_features == 0 ||
        in_features > std::numeric_limits<std::size_t>::max() / out_features)
      throw std::invalid_argument("invalid linear layer dimensions");

    const double limit = 1.0 / std::sqrt(static_cast<double>(in_features));
    std::uniform_real_distribution<double> distribution(-limit, limit);
    std::vector<double> values(in_features * out_features);
    for (double& value : values)
      value = distribution(random);

    return Tensor({in_features, out_features}, std::move(values));
  }
};
```

While writing the guard and allocation:

> We'll reject zero-sized layers and sizes that would overflow the allocation. Then we can allocate the weights and fill each entry from the distribution.

While returning the Tensor:

> The shape is input features by output features, which matches our matrix multiplication. Each column now starts with a different set of weights.

<!-- checkpoint: linear-module -->

Compile checkpoint for verification; no extra test walkthrough on camera.

## B. Connect the layers into a network | 3:30-6:00

> We can create multiple linear layers now, but stacking them alone still gives us a linear model. We'll put tanh between them. Let's wrap it in the same forward interface so each part of the network takes a Tensor and returns a Tensor.

Immediately after `Linear`, before `mse_loss()`:

<!-- edit: tanh-module -->
**Before**
```cpp
[[nodiscard]] Tensor mse_loss(
```

**After**
```cpp
struct Tanh {
  [[nodiscard]] Tensor forward(const Tensor& inputs) const {
    return inputs.tanh();
  }
};

[[nodiscard]] Tensor mse_loss(
```

While writing the return:

> This module just calls our Tensor's tanh operation. It has no trainable parameters, and the operation already records everything backward needs.

> We can now connect a hidden linear layer, tanh, and an output linear layer. I'll put that combination in an MLP class, short for multilayer perceptron.

Insert `MLP` after `Tanh`, before `mse_loss()`.

<!-- edit: mlp-composition -->
**Before**
```cpp
[[nodiscard]] Tensor mse_loss(
```

**After**
```cpp
class MLP {
public:
  MLP(
    std::size_t in_features,
    std::size_t hidden_features,
    std::size_t out_features,
    std::mt19937& random
  ) : hidden_(in_features, hidden_features, random),
      output_(hidden_features, out_features, random) {}

  [[nodiscard]] Tensor forward(const Tensor& inputs) const {
    const Tensor hidden = activation_.forward(hidden_.forward(inputs));
    return output_.forward(hidden);
  }

private:
  Linear hidden_;
  Tanh activation_;
  Linear output_;
};

[[nodiscard]] Tensor mse_loss(
```

While writing the constructor and members:

> The hidden layer takes the original features and produces the hidden values. The output layer takes those hidden values as its inputs, so the hidden size connects the two layers.

While writing `forward()`, highlight each call in order:

> We'll pass the inputs through the hidden layer, apply tanh, and feed those values into the output layer. We're leaving the final output as a number we can compare with our target using mean squared error.

Keep forward() on screen. Bring back the four XOR input pairs before adding
any shape labels.

> Let's follow our four XOR cases through this function. Each case has two inputs, so we'll pass in a matrix with four rows and two columns. We'll use four hidden units and one output.

Reveal each shape beside its call as it is explained. Label the notation
`[rows, values per row]` so the two dimensions have a clear meaning.

```text
4 input rows: [4, 2]
Linear(2, 4): [4, 4]
Tanh:         [4, 4]
Linear(4, 1): [4, 1]
```

Point to hidden_.forward(inputs), then activation_.forward(), then
output_.forward(hidden).

> The hidden layer turns each pair of inputs into four values. Tanh changes those values without changing their number. Then the output layer combines the four values into one prediction. We keep four rows throughout because each row still represents one XOR case.

<!-- checkpoint: composed-network -->

## C. Let training reach every parameter | 6:00-8:30

Keep the two Linear members of MLP visible, then open Linear and point to
its private weight_ and bias_ members.

> So at this point we can call forward to get predictions. We also know how to calculate a loss, and call backward to compute the gradients. 
>
> But there's still something missing. As you recall, our training loop needs to clear the old gradients with zero_grad before each step, then use gradient_step to update their values afterward. In the previous examples, the specific tensors that needed autograd were hardcoded inside the loops - because we knew exactly what they were - a single weight tensor and a single bias tensor. But that's no longer the case. The particular tensors that require zerograd and the gradient step are buried deep inside these modules that we just created - and we need to make them more discoverable.
>
> So let's give the model a parameters method that returns those Tensors in a list. We can use the same list for both the reset and the update. We'll start with Linear, which returns its weight and bias, then combine the lists from both layers.

In `Linear`, add `parameters()` immediately after `forward()`.

<!-- edit: linear-parameters -->
**Before**
```cpp
  [[nodiscard]] Tensor forward(const Tensor& inputs) const {
    return inputs.matmul(weight_) + bias_;
  }
```

**After**
```cpp
  [[nodiscard]] Tensor forward(const Tensor& inputs) const {
    return inputs.matmul(weight_) + bias_;
  }

  [[nodiscard]] std::vector<Tensor> parameters() {
    return {weight_, bias_};
  }
```

While writing the return:

> I'll return a vector containing weight_ and bias_. Our Tensor copies share their underlying data, so this gives us access to the layer's actual parameters. We won't be training separate copies of the numbers.

Move to `MLP`, immediately after its `forward()`.

> One layer can now give us its weights and biases. Let's do the same for the whole MLP by asking each of its two linear layers for that list and joining them. Tanh has no weights or biases to collect.

<!-- edit: mlp-parameters -->
**Before**
```cpp
  [[nodiscard]] Tensor forward(const Tensor& inputs) const {
    const Tensor hidden = activation_.forward(hidden_.forward(inputs));
    return output_.forward(hidden);
  }
```

**After**
```cpp
  [[nodiscard]] Tensor forward(const Tensor& inputs) const {
    const Tensor hidden = activation_.forward(hidden_.forward(inputs));
    return output_.forward(hidden);
  }

  [[nodiscard]] std::vector<Tensor> parameters() {
    std::vector<Tensor> result = hidden_.parameters();
    const std::vector<Tensor> output = output_.parameters();
    result.insert(result.end(), output.begin(), output.end());
    return result;
  }
```

While writing the two calls and insert:

> I'll start with the hidden layer's parameters, then append the output layer's parameters. The returned list contains four Tensors: the weights and biases from each layer.

Move to the existing gradient_step() and point to its weight-column loop
and scalar-bias update before returning to Tensor::data().

Keep the existing gradient_step() visible for this explanation. Point to its
weights and bias arguments, then their two update statements.

> Let's use this list to update the model. Here's our current gradient_step: it takes the weights and bias separately, and updates each one. With two layers, we have four Tensors to update, so we'll add a version that accepts the whole list.

Insert the new overload immediately above the existing gradient_step(). Keep
the old function for the regression examples. Write the signature and outer
loop first; the body will be filled in below. Do not run this unfinished step.

<!-- edit: parameter-update-loop -->
**Before**
```cpp
void gradient_step(
  Tensor& weights,
```

**After**
```cpp
void gradient_step(
  std::vector<Tensor>& parameters,
  double learning_rate
) {
  for (Tensor& parameter : parameters) {
  }
}

void gradient_step(
  Tensor& weights,
```

While writing the argument and outer loop:

> On the first pass, parameter refers to the hidden layer's weight matrix. We need to update every weight in that matrix before the loop moves on to the biases, then the output layer's weights and biases.

At the empty loop body, point to the old function's two update statements.

> Here, we update weights and biases separately, but both lines subtract the gradient times the learning rate. So we can use one inner loop to apply that update to every value in whichever Tensor we're visiting. Each Tensor already stores its values in a flat vector; let's use data to reach them.

Open Tensor::data() and point to the const in its return type.

> Here's data, returning a reference to the stored vector. The const here prevents us from changing its entries, which we'll need to do when we update the weights. We'll keep this read-only version and add another overload that lets us write to the vector.

Return to `Tensor::data()`. Add a mutable overload directly above the existing
const overload; preserve the const version.

<!-- edit: mutable-data -->
**Before**
```cpp
  [[nodiscard]] const std::vector<double>& data() const noexcept {
    return node_->data;
  }
```

**After**
```cpp
  [[nodiscard]] std::vector<double>& data() noexcept {
    return node_->data;
  }

  [[nodiscard]] const std::vector<double>& data() const noexcept {
    return node_->data;
  }
```

While writing the overload:

> I'll keep the read-only version and add this one for a Tensor we can modify. Returning a reference lets us change its stored values directly.

Recording constraint: the update below changes entries only. Never resize the
returned vector; its size must continue to match the Tensor's shape.

Return to the empty loop in the new gradient_step(). Fill in the element update.

> Back in our loop, we can now change those entries. We'll go from the first value to the last, using numel for the number of values in this Tensor.

<!-- edit: general-gradient-step -->
**Before**
```cpp
  for (Tensor& parameter : parameters) {
  }
```

**After**
```cpp
  for (Tensor& parameter : parameters) {
    for (std::size_t index = 0; index < parameter.numel(); ++index)
      parameter.data()[index] -= learning_rate * parameter.grad()[index];
  }
```

While writing the assignment:

> The data and gradient arrays use the same order, so index selects a value and its matching gradient. We multiply the gradient by the learning rate and subtract it from the value. After the inner loop finishes, the outer loop moves on to the next Tensor.

After completing the function:

> These are the same Tensors our layers use, so the next prediction will use the updated weights and biases.

<!-- checkpoint: parameter-updates -->

## D. Train the network on XOR | 8:30-12:30

Move immediately above `main()`.

> Let's use this update to train our network on XOR. We'll put the example in train_xor, starting with the four input pairs and the answer we want for each one.

<!-- edit: xor-setup -->
**Before**
```cpp
int main() {
```

**After**
```cpp
void train_xor() {
  const Tensor inputs({4, 2}, {
    0.0, 0.0,
    0.0, 1.0,
    1.0, 0.0,
    1.0, 1.0
  });
  const Tensor targets({4, 1}, {0.0, 1.0, 1.0, 0.0});

}

int main() {
```

While entering the four rows and targets:

> Each row holds one input pair, and the targets follow the same row order. Equal inputs should produce zero; different inputs should produce one.

Immediately after targets, create the model and collect its parameters.

> We have the examples to learn from. Let's create our two-input network with four hidden units and one output, then get its parameters for training.

<!-- edit: xor-model -->
**Before**
```cpp
  const Tensor targets({4, 1}, {0.0, 1.0, 1.0, 0.0});

}
```

**After**
```cpp
  const Tensor targets({4, 1}, {0.0, 1.0, 1.0, 0.0});

  std::mt19937 random(42);
  MLP model(2, 4, 1, random);
  std::vector<Tensor> parameters = model.parameters();
}
```

While creating the generator and model:

> The random generator supplies the starting weights. I'll fix its seed so we can repeat the run, then call parameters to collect the weights and biases from both layers. We only need to collect them once; training changes their values, not which Tensors belong to the model.

At the end of `train_xor()`, after collecting `parameters`:

> Before we change any weights, let's record the loss so we can compare it with the trained result. Then we'll repeat the training step five thousand times, using all four examples each time.

<!-- edit: xor-training -->
**Before**
```cpp
  std::vector<Tensor> parameters = model.parameters();
}
```

**After**
```cpp
  std::vector<Tensor> parameters = model.parameters();

  const double initial_loss = mse_loss(model.forward(inputs), targets).at({});
  for (std::size_t step = 0; step < 5000; ++step) {
    for (Tensor& parameter : parameters)
      parameter.zero_grad();

    const Tensor predictions = model.forward(inputs);
    Tensor loss = mse_loss(predictions, targets);
    loss.backward();
    gradient_step(parameters, 0.1);
  }
}
```

While writing initial_loss, before starting the loop:

> We'll pass the inputs through the model and compare its predictions with the targets using mean squared error. This gives us our starting loss.

While typing the reset loop:

> At the start of each step, we'll loop over our parameter list and call zero_grad on each Tensor. We want the update to use this step's gradients without adding in the ones from the previous step.

While typing predictions and loss:

> Now we'll make predictions with the current weights and calculate their loss. Forward runs both layers and tanh for us, so the training loop doesn't need to call each layer separately.

While typing backward and gradient_step:

> Calling backward computes how each parameter affects this loss. We can then pass our parameter list to gradient_step to apply the updates. On the next pass through the loop, we'll make predictions with the new values.

After the training loop:

> The loop ends with a weight update, so let's make predictions once more to see the result of that final step. We'll print them beside the targets, along with the loss before and after training.

Add the formatting header without a spoken include tour.

<!-- edit: formatting-include -->
**Before**
```cpp
#include <random>
```

**After**
```cpp
#include <random>
#include <iomanip>
```

Back at the end of `train_xor()`:

<!-- edit: xor-result -->
**Before**
```cpp
    gradient_step(parameters, 0.1);
  }
}
```

**After**
```cpp
    gradient_step(parameters, 0.1);
  }

  const Tensor predictions = model.forward(inputs);
  std::cout << std::fixed << std::setprecision(3);
  std::cout << "Loss: " << initial_loss << " -> "
            << mse_loss(predictions, targets).at({}) << '\n';
  std::cout << "a b prediction target\n";
  for (std::size_t row = 0; row < inputs.dimension(0); ++row) {
    std::cout << inputs.at({row, 0}) << ' '
              << inputs.at({row, 1}) << ' '
              << predictions.at({row, 0}) << ' '
              << targets.at({row, 0}) << '\n';
  }
}
```

While adding the output:

> Each output row will show the input pair, our prediction, and the target. I'll use three decimal places to keep the comparison easy to read.

At the end of `main()`, keep the existing calls and add `train_xor()`.

> We can call train_xor from main now and check all four answers.

<!-- edit: call-xor -->
**Before**
```cpp
  train_curve();

  std::cout << "Success!\n";
```

**After**
```cpp
  train_curve();
  train_xor();

  std::cout << "Success!\n";
```

Before running, show the four original cases beside the terminal.

> The predictions should approach zero, one, one, zero, and the loss should fall from its starting value. Let's run it.

<!-- checkpoint: trained-xor -->

The earlier regression and activation output still appears first. Focus the
recording on the new block below. Results shown are from the verified build;
last digits and initialization can differ across standard-library implementations.

```text
Loss: 0.779 -> 0.000
a b prediction target
0.000 0.000 0.000 0.000
0.000 1.000 1.000 1.000
1.000 0.000 1.000 1.000
1.000 1.000 0.000 0.000
```

> The predictions match all four XOR cases. These numbers are rounded to three decimal places, including the loss. Using one half as the cutoff between zero and one, we get every answer right.
>
> We trained on every possible input here. To find out how well a model handles examples it hasn't seen, we'll need a separate set of test data.

## E. Recap | 12:30-13:15

```text
Recap

- Reusable Linear and Tanh modules
- A hidden layer and output layer
- Parameter collection and updates
- An MLP that learns XOR
```

> We've built Linear and Tanh modules, connected them into an MLP, and trained it to learn XOR. Our autograd engine still computes the gradients; the new modules let us assemble the network and collect its parameters for training.

Replace the recap with:

```text
Next episode

- MNIST handwritten digits
- Mini-batches of image data
- Classification loss and accuracy
```

> Next, we'll use MNIST to recognize handwritten digits. We'll feed images into a larger network, train it in mini-batches, and measure its accuracy on separate test examples. We'll also introduce a classification loss for the ten possible digits.

> That brings us to the end of this episode. Thanks for watching, and I will see you next time.

Leave approximately five clean seconds for the Subscribe and complete-series
playlist end-screen elements.
