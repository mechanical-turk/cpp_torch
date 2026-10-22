MP4 filename: `cpp-residual-connections-gradient-debugging.mp4`

# Episode 14: Residual Connections and Debugging Gradients in C++

Continue in the same `main.cpp` used for Episode 13. Keep the existing Tensor,
autograd engine, Layer, Linear, Tanh, Sequence and every example.
Read only the `>` passages aloud. Before/After blocks show the exact edits;
checkpoint notes and output blocks are not narration.

## A. Build sixteen layers | 0:00-3:45

Frame zero: `main.cpp` open at `Sequence`, with the terminal beside it. Show
the title "Residual Connections and Debugging Gradients in C++" over the code
for the first five seconds. Do not use a separate title card. Speak immediately.

> When working with deep neural networks, learning slows down. If your learning rate is too low, you're too slow. If it's too high, you ping ping, overcorrect and waste training cycles. You can start high and decay at each epoch - but does that actually scale?
>
> Let's stack it up to sixteen layers, and see what breaks.

Point to `Sequence`, then to `push_back`.

> Sixteen layers means a lot of push_back calls, and each one wraps its layer in make_unique. Let's have push_back take the layer by value and do the make_unique itself.

From here until the sixteen-layer model is written, the program does not compile.

<!-- edit: sequence-by-value -->
**Before**
```cpp
  void push_back(std::unique_ptr<Layer> layer) {
    layers_.push_back(std::move(layer));
  }
```

**After**
```cpp
  template <typename LayerType>
  void push_back(LayerType layer) {
    layers_.push_back(std::make_unique<LayerType>(std::move(layer)));
  }
```

While writing the template line:

> push_back has to accept any kind of layer, a Linear, a Tanh, or something else later, so it's a template, and LayerType stands for whichever type we pass in.

While writing the body:

> We take the layer by value, move it into a new object on the heap with make_unique, and store the pointer. The vector still holds pointers to the Layer base class, because the layers have different types, but the caller no longer has to write make_unique.

Move to the top of `Sequence`.

> A hidden layer is always a Linear followed by a tanh. Sixteen of those written out would be thirty-two lines, so let's treat the pair as one layer. A Sequence already has forward and parameters, so it can be a Layer itself, which means a Sequence can hold other Sequences. We mark it as a Layer and mark both functions as overrides.

<!-- edit: sequence-is-layer -->
**Before**
```cpp
class Sequence {
public:
  template <typename LayerType>
  void push_back(LayerType layer) {
    layers_.push_back(std::make_unique<LayerType>(std::move(layer)));
  }

  [[nodiscard]] Tensor forward(const Tensor& inputs) const {
    Tensor current = inputs;
    for (const auto& layer: layers_) {
      current = layer->forward(current);
    }
    return current;
  }

  [[nodiscard]] std::vector<Tensor> parameters() const {
```

**After**
```cpp
class Sequence : public Layer {
public:
  template <typename LayerType>
  void push_back(LayerType layer) {
    layers_.push_back(std::make_unique<LayerType>(std::move(layer)));
  }

  [[nodiscard]] Tensor forward(const Tensor& inputs) const override {
    Tensor current = inputs;
    for (const auto& layer: layers_) {
      current = layer->forward(current);
    }
    return current;
  }

  [[nodiscard]] std::vector<Tensor> parameters() const override {
```

Move below `Sequence`, above `linear_forward`.

> Then a helper that builds one hidden layer: a Sequence holding a Linear and an activation, which we return by value. The activation is a template parameter that defaults to Tanh, so hidden_layer(32, 32, random) gives a Linear and a tanh, and passing another activation layer as a fourth argument swaps it in.

<!-- edit: hidden-layer -->
**Before**
```cpp
private:
  std::vector<std::unique_ptr<Layer>> layers_;
};

[[nodiscard]] Tensor linear_forward(
```

**After**
```cpp
private:
  std::vector<std::unique_ptr<Layer>> layers_;
};

template <typename ActivationType = Tanh>
[[nodiscard]] Sequence hidden_layer(
  std::size_t in_features,
  std::size_t out_features,
  std::mt19937& random,
  ActivationType activation = ActivationType()
) {
  Sequence layer;
  layer.push_back(Linear(in_features, out_features, random));
  layer.push_back(std::move(activation));
  return layer;
}

[[nodiscard]] Tensor linear_forward(
```

Move to the model in `train_mnist()`.

> Now the first hidden layer takes the 784 pixels in and gives 32 out. The other fifteen all take 32 in and give 32 out, so they go in a loop, and a constant says how many. Then the output layer turns 32 features into 10 scores. That's sixteen hidden layers, and it compiles again.

<!-- edit: sixteen-layers -->
**Before**
```cpp
    Sequence model;
    model.push_back(std::make_unique<Linear>(784, 32, random));
    model.push_back(std::make_unique<Tanh>());
    model.push_back(std::make_unique<Linear>(32, 32, random));
    model.push_back(std::make_unique<Tanh>());
    model.push_back(std::make_unique<Linear>(32, 32, random));
    model.push_back(std::make_unique<Tanh>());
    model.push_back(std::make_unique<Linear>(32, 32, random));
    model.push_back(std::make_unique<Tanh>());
    model.push_back(std::make_unique<Linear>(32, 32, random));
    model.push_back(std::make_unique<Tanh>());
    model.push_back(std::make_unique<Linear>(32, 32, random));
    model.push_back(std::make_unique<Tanh>());
    model.push_back(std::make_unique<Linear>(32, 32, random));
    model.push_back(std::make_unique<Tanh>());
    model.push_back(std::make_unique<Linear>(32, 32, random));
    model.push_back(std::make_unique<Tanh>());
    model.push_back(std::make_unique<Linear>(32, 10, random));
```

**After**
```cpp
    Sequence model;
    model.push_back(hidden_layer(784, 32, random));

    const int NUM_HIDDEN_LAYERS = 15;
    for (int i = 0; i < NUM_HIDDEN_LAYERS; ++i) {
      model.push_back(hidden_layer(32, 32, random));
    }

    model.push_back(Linear(32, 10, random));
```

Move to the training loop.

> We'll train for ten epochs, starting at a learning rate of 0.5, and keep the decay, so we multiply the rate by 0.9 after every epoch.

<!-- edit: training-setup -->
**Before**
```cpp
    double learning_rate = 1.0;

    for(std::size_t epoch = 0; epoch < 5; ++epoch) {
      std::cout << "Training epoch: " << epoch + 1 << "/5\n";
```

**After**
```cpp
    double learning_rate = 0.5;

    for(std::size_t epoch = 0; epoch < 10; ++epoch) {
      std::cout << "Training epoch: " << epoch + 1 << "/10\n";
```

Move to the end of the epoch loop.

<!-- edit: training-decay -->
**Before**
```cpp
      learning_rate *= 0.5;
```

**After**
```cpp
      learning_rate *= 0.9;
```

> Let's run it.

<!-- checkpoint: plain-sixteen -->

Point to the epoch losses, then to the accuracy.

```output
Epoch 1 loss: 2.30346
Epoch 5 loss: 2.30231
Epoch 10 loss: 2.30155
Test accuracy: 11.7% (234/2000)
```

> The loss starts at 2.30 and stays there. That's what guessing gives for ten digits, and accuracy is 11.7 percent. The decay that helped before can't help here, and neither can a different learning rate: starting at 0.1, 0.3 or 1.0, the loss stays at 2.30. So why isn't this network learning anything?

## B. Look inside the network | 3:45-7:45

> To find out, we'll build a tool for debugging gradients. For every layer, it will show how big the layer's output is and how big its gradient is. To read that report, each layer should be able to say what it is, so let's start by giving every Layer a name.

Move to the `Layer` class. From here until all four classes have a `name()`, the program does not compile.

> A Layer gets one more required function, name, that returns a string. Because it's pure virtual, every layer has to provide one, and the compiler will tell us about any that don't.

<!-- edit: name-layer -->
**Before**
```cpp
  virtual ~Layer() = default;

  [[nodiscard]] virtual Tensor forward(const Tensor& inputs) const = 0;
```

**After**
```cpp
  virtual ~Layer() = default;

  [[nodiscard]] virtual std::string name() const = 0;
  [[nodiscard]] virtual Tensor forward(const Tensor& inputs) const = 0;
```

Move to `Linear`.

> Linear and Tanh just return their own names.

<!-- edit: name-linear -->
**Before**
```cpp
     bias_({out_features}, std::vector<double>(out_features, 0.0)) {}

  [[nodiscard]] Tensor forward(const Tensor& inputs) const override {
    return inputs.matmul(weight_) + bias_;
```

**After**
```cpp
     bias_({out_features}, std::vector<double>(out_features, 0.0)) {}

  [[nodiscard]] std::string name() const override {
    return "Linear";
  }

  [[nodiscard]] Tensor forward(const Tensor& inputs) const override {
    return inputs.matmul(weight_) + bias_;
```

Move to `Tanh`.

<!-- edit: name-tanh -->
**Before**
```cpp
struct Tanh : public Layer {
  [[nodiscard]] Tensor forward(const Tensor& inputs) const override {
    return inputs.tanh();
```

**After**
```cpp
struct Tanh : public Layer {
  [[nodiscard]] std::string name() const override {
    return "Tanh";
  }

  [[nodiscard]] Tensor forward(const Tensor& inputs) const override {
    return inputs.tanh();
```

Move to `Sequence`, below `push_back`.

> A Sequence's name lists the names of the layers inside it, so a hidden layer will read Sequence, then Linear and Tanh in brackets.

<!-- edit: name-sequence -->
**Before**
```cpp
    layers_.push_back(std::make_unique<LayerType>(std::move(layer)));
  }

  [[nodiscard]] Tensor forward(const Tensor& inputs) const override {
```

**After**
```cpp
    layers_.push_back(std::make_unique<LayerType>(std::move(layer)));
  }

  [[nodiscard]] std::string name() const override {
    std::string result = "Sequence[";
    for (std::size_t index = 0; index < layers_.size(); ++index) {
      if (index > 0) {
        result += ", ";
      }
      result += layers_[index]->name();
    }
    return result + "]";
  }

  [[nodiscard]] Tensor forward(const Tensor& inputs) const override {
```

> Next, a Sequence hands back only the final scores, and we need every layer's output with its name. So let's add a version of forward that keeps them.

Move to the end of `Sequence`, below `parameters`.

<!-- edit: trace-forward -->
**Before**
```cpp
    return result;
  }

private:
  std::vector<std::unique_ptr<Layer>> layers_;
};
```

**After**
```cpp
    return result;
  }

  struct TracedOutput {
    std::string name;
    Tensor output;
  };

  [[nodiscard]] std::vector<TracedOutput> forward_traced(const Tensor& inputs) const {
    std::vector<TracedOutput> outputs;
    Tensor current = inputs;
    for (const auto& layer: layers_) {
      current = layer->forward(current);
      outputs.push_back({layer->name(), current});
    }
    return outputs;
  }

private:
  std::vector<std::unique_ptr<Layer>> layers_;
};
```

> It's the same loop as forward, except each output also goes into the list, together with the layer's name, before we move on.

> Let's try it on the sample image the program already loads, before any training. A small function will print one row per layer: its number, its name, and how many values its output has. We'll format the rows with the format library, so this include comes first.

Move to the top of `main.cpp`, below the other includes.

<!-- edit: format-include -->
**Before**
```cpp
#include <utility>
#include <unordered_set>
```

**After**
```cpp
#include <utility>
#include <unordered_set>
#include <format>
```

Move directly above `train_mnist()`.

<!-- edit: print-trace -->
**Before**
```cpp
void train_mnist() {
```

**After**
```cpp
void print_trace(const std::vector<Sequence::TracedOutput>& trace) {
  for (std::size_t layer = 0; layer < trace.size(); ++layer) {
    std::cout << std::format(
      "layer {:2}  {:<32}  {} values\n",
      layer + 1,
      trace[layer].name,
      trace[layer].output.numel()
    );
  }
}

void train_mnist() {
```

Move to the sample image in `train_mnist()`, where the first forward pass happens.

> Here the sample image goes through forward. We'll use forward_traced instead, print the trace, and take the scores from the last entry, so everything after this stays the same.

<!-- edit: trace-sample -->
**Before**
```cpp
    const Tensor scores = model.forward(image);
    const Tensor probabilities = softmax(scores);
```

**After**
```cpp
    const std::vector<Sequence::TracedOutput> sample_trace = model.forward_traced(image);
    print_trace(sample_trace);
    const Tensor scores = sample_trace.back().output;
    const Tensor probabilities = softmax(scores);
```

> Let's run it.

<!-- checkpoint: trace-run -->

Point to the names, then to the value counts.

```output
layer  1  Sequence[Linear, Tanh]            32 values
layer  2  Sequence[Linear, Tanh]            32 values
layer  3  Sequence[Linear, Tanh]            32 values
layer  4  Sequence[Linear, Tanh]            32 values
layer  5  Sequence[Linear, Tanh]            32 values
layer  6  Sequence[Linear, Tanh]            32 values
layer  7  Sequence[Linear, Tanh]            32 values
layer  8  Sequence[Linear, Tanh]            32 values
layer  9  Sequence[Linear, Tanh]            32 values
layer 10  Sequence[Linear, Tanh]            32 values
layer 11  Sequence[Linear, Tanh]            32 values
layer 12  Sequence[Linear, Tanh]            32 values
layer 13  Sequence[Linear, Tanh]            32 values
layer 14  Sequence[Linear, Tanh]            32 values
layer 15  Sequence[Linear, Tanh]            32 values
layer 16  Sequence[Linear, Tanh]            32 values
layer 17  Linear                            10 values
```

> Sixteen hidden layers, each a Sequence holding a Linear and a tanh, and the output layer last. The first hidden layer turns the 784 pixels into 32 values, every other one keeps 32, and the output layer gives the 10 scores. The names and sizes are right, so now let's measure what's inside them.

Move to `print_trace`, above `train_mnist()`. From here until the new `print_trace` is written, the program does not compile.

> print_trace only counts values, so let's delete it and write the report we need.

<!-- edit: print-trace-remove -->
**Before**
```cpp
void print_trace(const std::vector<Sequence::TracedOutput>& trace) {
  for (std::size_t layer = 0; layer < trace.size(); ++layer) {
    std::cout << std::format(
      "layer {:2}  {:<32}  {} values\n",
      layer + 1,
      trace[layer].name,
      trace[layer].output.numel()
    );
  }
}

void train_mnist() {
```

**After**
```cpp
void train_mnist() {
```

Move directly above `train_mnist()`.

> The new print_trace is for the training loop. Each row will show two numbers instead of a count: how big the layer's output is, which we'll call the signal, and how big the gradient at that output is, meaning how strongly the loss responds to it. A layer's output is a whole list of values, so we need one number for its typical size. An ordinary average won't work, because positive and negative values cancel and the average can sit near zero even when the values are large. So we square each value, which makes them all positive, average the squares, and take the square root to get back to the original scale. That's the root mean square, and it doesn't depend on how many values a layer has, so we can compare a wide layer with a narrow one.

<!-- edit: print-trace-signal -->
**Before**
```cpp
void train_mnist() {
```

**After**
```cpp
[[nodiscard]] double root_mean_square(const std::vector<double>& values) {
  double total = 0.0;
  for (const double value: values) {
    total += value * value;
  }
  return std::sqrt(total / values.size());
}

void print_trace(const std::vector<Sequence::TracedOutput>& trace) {
  for (std::size_t layer = 0; layer < trace.size(); ++layer) {
    std::cout << std::format(
      "layer {:2}  {:<32}  signal {:.1e}  gradient {:.1e}\n",
      layer + 1,
      trace[layer].name,
      root_mean_square(trace[layer].output.data()),
      root_mean_square(trace[layer].output.grad())
    );
  }
}

void train_mnist() {
```

While writing `print_trace`:

> Same name and same row layout as before, with the value count replaced by the size of the output values and the size of the gradient. The gradient only exists after backward, so we'll call it once backward has run, in the training loop.

Move to the sample image in `train_mnist()`, where the first forward pass happens.

> Now the training loop. Three steps, in order. First, take the report out of the sample image, where it started. Second, the forward pass in the loop. Third, the report, which has to come after backward.

> The sample image has no loss and no backward, so there's no gradient for the report to show. Let's delete the print_trace call, and the traced forward with it, and put the plain forward back.

<!-- edit: trace-sample-cleanup -->
**Before**
```cpp
    const std::vector<Sequence::TracedOutput> sample_trace = model.forward_traced(image);
    print_trace(sample_trace);
    const Tensor scores = sample_trace.back().output;
    const Tensor probabilities = softmax(scores);
```

**After**
```cpp
    const Tensor scores = model.forward(image);
    const Tensor probabilities = softmax(scores);
```

Move to the batch loop in `train_mnist()`. Point to the forward pass.

> First the forward pass. It's the same swap we just undid on the sample image: forward_traced instead of forward. The scores are the last entry of the trace, so logits becomes a reference to that entry, and softmax and the loss below it don't change.

<!-- edit: trace-training-forward -->
**Before**
```cpp
        const Tensor logits = model.forward(inputs);
        const Tensor probabilities = softmax(logits);
```

**After**
```cpp
        const std::vector<Sequence::TracedOutput> trace = model.forward_traced(inputs);
        const Tensor& logits = trace.back().output;
        const Tensor probabilities = softmax(logits);
```

Point to `loss.backward()`.

> The trace holds the same tensors the loss was built from, so when backward runs, it fills in the gradient of every output in the list. That's why the report goes right after backward, and before the weights change. We only need one look, so we print on the first batch of the first epoch: epoch is zero, and seen, the number of images used so far, is still zero.

<!-- edit: trace-training-report -->
**Before**
```cpp
        loss.backward();
        gradient_step(parameters, learning_rate);
```

**After**
```cpp
        loss.backward();
        if (epoch == 0 && seen == 0) {
          print_trace(trace);
        }
        gradient_step(parameters, learning_rate);
```

> One batch is enough to see the pattern. This is the same sixteen-layer network. Each row is one layer: the sixteen hidden layers, each a Sequence of a Linear and a tanh, then the output layer. Let's run it.

<!-- checkpoint: plain-signal -->

Point to the signal column from row 1 to row 17, then to the gradient column.

```output
layer  1  Sequence[Linear, Tanh]            signal 1.8e-01  gradient 3.2e-07
layer  2  Sequence[Linear, Tanh]            signal 1.0e-01  gradient 5.6e-07
layer  3  Sequence[Linear, Tanh]            signal 6.2e-02  gradient 1.0e-06
layer  4  Sequence[Linear, Tanh]            signal 3.1e-02  gradient 1.8e-06
layer  5  Sequence[Linear, Tanh]            signal 1.7e-02  gradient 3.3e-06
layer  6  Sequence[Linear, Tanh]            signal 8.7e-03  gradient 6.8e-06
layer  7  Sequence[Linear, Tanh]            signal 5.0e-03  gradient 1.2e-05
layer  8  Sequence[Linear, Tanh]            signal 2.7e-03  gradient 2.0e-05
layer  9  Sequence[Linear, Tanh]            signal 1.7e-03  gradient 3.3e-05
layer 10  Sequence[Linear, Tanh]            signal 9.5e-04  gradient 5.4e-05
layer 11  Sequence[Linear, Tanh]            signal 5.8e-04  gradient 9.6e-05
layer 12  Sequence[Linear, Tanh]            signal 3.3e-04  gradient 1.7e-04
layer 13  Sequence[Linear, Tanh]            signal 1.8e-04  gradient 3.1e-04
layer 14  Sequence[Linear, Tanh]            signal 9.2e-05  gradient 5.6e-04
layer 15  Sequence[Linear, Tanh]            signal 4.6e-05  gradient 8.8e-04
layer 16  Sequence[Linear, Tanh]            signal 2.7e-05  gradient 1.6e-03
layer 17  Linear                            signal 1.9e-05  gradient 4.7e-03
```

> Look at the signal first. It starts at 0.18, and by the last hidden layer it's 2.7e-5, more than six thousand times smaller. Every layer returns a little more than half of what it was given. The gradient does the same thing going backward. It's biggest at the output, and at the first layer it's about fifteen thousand times smaller. A layer's weights can only change as much as the gradient at its output allows, so the early layers barely move, and sixteen layers compound the shrinking. This is the vanishing gradient problem, and it leaves us with a network that can't learn. We need layers that don't shrink what they're given.

## C. Residual connections | 7:45-11:45

> Here's what went wrong. Every layer replaces its input with its own output, so going forward and going backward, everything has to pass through all sixteen layers, and each one hands on only about half. So what if a layer didn't replace its input, but added to it?

Show on screen, beside the code:

```text
plain:     output = layer(input)
residual:  output = input + layer(input)
```

> The output would be the input plus whatever the layer computes. Going forward, the input is carried through as it is, and the layer only adds a correction on top.
>
> Going backward, an addition sends the gradient down both of its sides at full size: one copy through the layer, and one straight past it. The path through the layer can still shrink the gradient, but the path straight past it doesn't, and sixteen layers can't shrink what never goes through them. We call this a residual connection.

Move below `hidden_layer`, above `linear_forward`.

> A residual layer is a Layer too, so it can go anywhere a Linear or a Tanh can, including inside a Sequence. Let's start with an empty class that derives from Layer.

<!-- edit: residual-skeleton -->
**Before**
```cpp
  return layer;
}

[[nodiscard]] Tensor linear_forward(
```

**After**
```cpp
  return layer;
}

class Residual : public Layer {
};

[[nodiscard]] Tensor linear_forward(
```

> Layer has three required functions: name, forward and parameters. Until we write all three, we can't create a Residual, so we'll add them one at a time, starting with what it holds.

While writing the constructor:

> A residual layer wraps another layer, which we'll call its body. The constructor takes the body by value and moves it onto the heap, the same trick as push_back, so any layer can go inside.

While writing the member:

> We keep the body as a pointer to Layer, because the body can be a Linear, a Tanh, or a whole Sequence.

<!-- edit: residual-body -->
**Before**
```cpp
class Residual : public Layer {
};
```

**After**
```cpp
class Residual : public Layer {
public:
  template <typename LayerType>
  explicit Residual(LayerType body)
    : body_(std::make_unique<LayerType>(std::move(body))) {}

private:
  std::unique_ptr<Layer> body_;
};
```

Move into `Residual`, below the constructor.

> Now the idea itself. Forward returns the inputs plus whatever the body returns. That's the formula from the screen. Because we add the two, the body has to return the same shape it receives.
>
> And there's no backward to write. The plus is an addition like any other, and the engine already sends the gradient to both of its sides.

<!-- edit: residual-forward -->
**Before**
```cpp
    : body_(std::make_unique<LayerType>(std::move(body))) {}

private:
```

**After**
```cpp
    : body_(std::make_unique<LayerType>(std::move(body))) {}

  [[nodiscard]] Tensor forward(const Tensor& inputs) const override {
    return inputs + body_->forward(inputs);
  }

private:
```

Move below `forward`.

> Next, parameters. Training only updates the tensors a model reports through parameters, and Residual has none of its own, so it returns its body's. If it returned nothing, the weights inside the body would never change.

<!-- edit: residual-parameters -->
**Before**
```cpp
    return inputs + body_->forward(inputs);
  }

private:
```

**After**
```cpp
    return inputs + body_->forward(inputs);
  }

  [[nodiscard]] std::vector<Tensor> parameters() const override {
    return body_->parameters();
  }

private:
```

Move above `forward`, below the constructor.

> Last, the name. It wraps the body's name in parentheses, so the report will show which layers are residual. With all three functions written, Residual is a complete Layer.

<!-- edit: residual-name -->
**Before**
```cpp
    : body_(std::make_unique<LayerType>(std::move(body))) {}

  [[nodiscard]] Tensor forward(const Tensor& inputs) const override {
```

**After**
```cpp
    : body_(std::make_unique<LayerType>(std::move(body))) {}

  [[nodiscard]] std::string name() const override {
    return "Residual(" + body_->name() + ")";
  }

  [[nodiscard]] Tensor forward(const Tensor& inputs) const override {
```

Move to the model in `train_mnist()`.

> Now we wrap the hidden layers in Residual. Not the first one. It takes 784 features in and gives 32 out, and a residual layer adds its input to its output, so the two need the same shape. Nothing in the first layer needs a shortcut either: its input is the image, and there are no layers behind it for a gradient to reach. The fifteen others take 32 in and give 32 out, and they're all in the loop, so wrapping them is one change.

<!-- edit: residual-model -->
**Before**
```cpp
    for (int i = 0; i < NUM_HIDDEN_LAYERS; ++i) {
      model.push_back(hidden_layer(32, 32, random));
    }
```

**After**
```cpp
    for (int i = 0; i < NUM_HIDDEN_LAYERS; ++i) {
      model.push_back(Residual(hidden_layer(32, 32, random)));
    }
```

> Same network, same data, same learning rate and decay. Let's run it.

<!-- checkpoint: residual-sixteen -->

Point to the gradient column from the bottom row to the top row, then to the signal column from the top row to the bottom row, then to the epoch losses and the accuracy.

```output
layer  1  Sequence[Linear, Tanh]            signal 1.8e-01  gradient 1.1e-02
layer  2  Residual(Sequence[Linear, Tanh])  signal 2.1e-01  gradient 9.6e-03
layer  3  Residual(Sequence[Linear, Tanh])  signal 2.6e-01  gradient 7.9e-03
layer  4  Residual(Sequence[Linear, Tanh])  signal 2.9e-01  gradient 6.6e-03
layer  5  Residual(Sequence[Linear, Tanh])  signal 3.4e-01  gradient 5.7e-03
layer  6  Residual(Sequence[Linear, Tanh])  signal 3.8e-01  gradient 5.5e-03
layer  7  Residual(Sequence[Linear, Tanh])  signal 4.0e-01  gradient 4.9e-03
layer  8  Residual(Sequence[Linear, Tanh])  signal 4.7e-01  gradient 3.9e-03
layer  9  Residual(Sequence[Linear, Tanh])  signal 5.3e-01  gradient 3.7e-03
layer 10  Residual(Sequence[Linear, Tanh])  signal 6.1e-01  gradient 3.2e-03
layer 11  Residual(Sequence[Linear, Tanh])  signal 6.7e-01  gradient 2.8e-03
layer 12  Residual(Sequence[Linear, Tanh])  signal 7.0e-01  gradient 2.4e-03
layer 13  Residual(Sequence[Linear, Tanh])  signal 7.6e-01  gradient 2.1e-03
layer 14  Residual(Sequence[Linear, Tanh])  signal 8.3e-01  gradient 1.9e-03
layer 15  Residual(Sequence[Linear, Tanh])  signal 9.1e-01  gradient 1.7e-03
layer 16  Residual(Sequence[Linear, Tanh])  signal 9.6e-01  gradient 1.6e-03
layer 17  Linear                            signal 5.1e-01  gradient 4.7e-03
Epoch 1 loss: 52.2632
Epoch 2 loss: 24.6807
Epoch 10 loss: 2.44455
Test accuracy: 58.85% (1177/2000)
```

> Let's read the gradient column from the bottom up, the way backward runs. At the output it's 4.7e-3, and at the last residual layer it's 1.6e-3. From there it grows, all the way up to 1.1e-2 at the first layer. That's about seven times bigger than at the last residual layer, and more than thirty thousand times bigger than the first layer had before. So the gradient doesn't vanish anymore.
>
> The signal grows too. It starts at 0.18 and reaches 0.96 at the last residual layer. And the network learns: accuracy is 58.85 percent, up from 11.7. But look at the first epoch. The loss is 52, and guessing gave 2.30. How can a network be worse than guessing? To answer that, we need to look at what the loss measures.

## Aside: What a loss of 52 means | 11:45-13:30

> The loss for one image is the negative log of the probability the network gave to the correct digit.

Show on screen, beside the code:

```text
loss for one image = -ln(probability given to the correct digit)

probability   loss
0.99          0.01
0.5           0.69
0.1           2.30
0.01          4.61
0.000001      13.82
2e-23         52.27
```

Point to the 0.1 row, then to the last row.

> Giving every digit the same probability, 0.1, costs 2.30. That's the loss of knowing nothing. But the loss has no ceiling. A single image with a loss of 52 means the correct digit got a probability around 2e-23. So in that first epoch the network wasn't unsure. It was certain, and wrong.

> It was wrong in a particular way. After the first epoch I scored all 10,000 training images, and every one of them was predicted as a zero, with a probability close to one. During the epoch it was the same story, batch after batch: one digit for nearly every image, and a different digit each time.

> Here's why. Tanh squashes anything beyond about two or three to plus or minus one. Each unit multiplies its input by its weights and adds a bias, and before training that comes out around 0.3, in the middle of tanh's range. The updates at 0.5 changed the weights so much that by the end of the first epoch they were about eighteen times bigger, and the numbers going into tanh were around 80. At that size, every unit in all fifteen residual layers is stuck at plus or minus one.

> But being stuck doesn't mean the picture is ignored, because the sign could still change from picture to picture. It didn't. Each layer's input had become mostly the same for every image, the same plus and minus ones added by the layers before it, and the part that changes with the picture was only about a tenth of it. After the big weights, the part from the picture was about 2.5, next to 83 from everything else. A number that's 83, give or take 2.5, never changes sign. In a batch of 64 images, not one unit did. So every layer added the same pattern of plus and minus ones to every image, and the only trace of the picture left was a small variation from the first layer.

> A network that barely sees the picture gives one answer to nearly every image. That answer is right for the tenth of the images that have that digit, so accuracy stays near 10 percent, and certain and wrong for the rest, so the loss is enormous. And each update at 0.5 swung that one answer to another digit.

> Then the learning rate keeps decaying. It's 0.5 in the first epoch and 0.19 in the tenth. As the steps shrink, the swings die down. In the first epoch, 131 of the 157 batches got one digit for nearly every image. By the third it's 22, and from the seventh epoch on it's none. The network starts to use the picture again, and by the tenth epoch it predicts seven different digits and gets 58.85 percent of the test images right. The tanh units are still stuck, so only a thin signal from the first layer gets through, and that limits how far it can climb.

## D. Lowering the learning rate | 13:30-15:00

> So the decay was already rescuing the network, slowly. The gradient at the first layer is now more than thirty thousand times bigger than before, which is why a learning rate of 0.5 is too big. You might want to train longer instead. I trained this same network for 40 epochs offline at the same settings, and it reached only 64 percent. So let's start lower.

Move to the training setup.

<!-- edit: residual-lower-rate -->
**Before**
```cpp
    double learning_rate = 0.5;
```

**After**
```cpp
    double learning_rate = 0.1;
```

> Same network, same data, same decay. Let's run it.

<!-- checkpoint: residual-lower-rate -->

Point to the epoch losses, then to the accuracy.

```output
Epoch 1 loss: 3.01616
Epoch 2 loss: 0.410781
Epoch 10 loss: 0.119504
Test accuracy: 91.05% (1821/2000)
```

> The first epoch still starts above 2.30, because the starting scores are too large. By the second epoch the loss is 0.41, and by the tenth it's 0.12. Accuracy is 91 percent, from the same sixteen layers that couldn't leave 2.30.

## E. What is left | 15:00-15:45

> We can push it further. I trained this same network for 40 epochs offline, at a learning rate of 0.05 and without decay. The loss on the training images fell to about 0.001, while accuracy on the test images stopped at about 93 percent. The network fits these 10,000 images better than it handles new ones, so it needs more examples and a faster way to learn from them.

## F. Recap | 15:45-16:30

```text
Recap

- Sequence takes layers by value
- Sixteen plain layers: stuck at 2.30, 11.7%
- Signal and gradient size for every layer
- Gradient at the first layer: 15,000 times smaller
- Residual layer: input plus body, 58.85%
- Lower learning rate: 91%
```

> We made Sequence take its layers by value and built a network of sixteen. Trained the plain way, it never leaves 2.30. A report of the signal and gradient at every layer showed why: the gradient at the first layer is about fifteen thousand times smaller than at the output. A residual connection adds each layer's output to its input and keeps the gradient alive, which took the network to 58.85 percent. It also makes the gradient grow, so the learning rate has to come down, and then the same network reaches 91 percent.

Replace the recap with:

```text
Next episode

- Training on more data
- Momentum and velocity
- The Adam optimizer
```

> Next, we'll give the network more training data, and make learning from it faster with momentum, velocity and Adam.

> That brings us to the end of this episode. Thanks for watching, and I will see you next time.

Leave approximately five clean seconds for the Subscribe and complete-series
playlist end-screen elements.
