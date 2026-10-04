MP4 filename: `cpp-deeper-neural-network-sequence-learning-rate-decay.mp4`

# Episode 13: Deeper Neural Networks and Learning Rate Decay in C++

Continue in the same `main.cpp` used for Episode 12. Keep the existing Tensor,
autograd engine, Linear, MLP, softmax, cross-entropy and every example.
Read only the `>` passages aloud. Before/After blocks show the exact edits;
checkpoint notes and output blocks are not narration.

## A. Build a network from a list of layers | 0:00-4:00

Frame zero: `main.cpp` open at `MLP`, with the terminal beside it showing the
result of the existing program. Show the title "Deeper Neural Networks and
Learning Rate Decay in C++" over the code for the first five seconds. Do not use a
separate title card. Speak immediately.

<!-- checkpoint: baseline-result -->

```output
Epoch 5 loss: 0.271741
Test accuracy: 88.2% (1764/2000)
```

> Our C++ neural network reads handwritten digits from MNIST, and with one hidden layer it gets 88.2 percent right. Let's make it deeper: we'll stack layers, see what breaks, and tame its learning rate with decay.

Point to the accuracy line, then to `MLP`.

> Right now the network is one fixed class. Let's build it from a list of layers instead. Every layer answers the same two questions, forward and parameters, so let's write them down as a base class.

Move directly above `Linear`, below `mse_loss`.

<!-- edit: layer-base -->
**Before**
```cpp
  return (residual * residual).mean();
}

class Linear {
```

**After**
```cpp
  return (residual * residual).mean();
}

class Layer {
public:
  virtual ~Layer() = default;

  [[nodiscard]] virtual Tensor forward(const Tensor& inputs) const = 0;
  [[nodiscard]] virtual std::vector<Tensor> parameters() const = 0;
};

class Linear {
```

While writing the two functions:

> Both functions are pure virtual, so Layer only describes what a layer can do, and each real layer supplies the code. The virtual destructor makes it safe to delete a layer through a Layer pointer.

Move to `Linear`.

> Linear becomes a Layer by inheriting from it.

<!-- edit: linear-inherits -->
**Before**
```cpp
class Linear {
public:
  Linear(
```

**After**
```cpp
class Linear : public Layer {
public:
  Linear(
```

Point to `forward` and `parameters` in `Linear`.

> Its forward and parameters already match the base class, so we only mark them override. That asks the compiler to check that they really do.

<!-- edit: linear-overrides -->
**Before**
```cpp
  [[nodiscard]] Tensor forward(const Tensor& inputs) const {
    return inputs.matmul(weight_) + bias_;
  }

  [[nodiscard]] std::vector<Tensor> parameters() const {
    return {weight_, bias_};
  }
```

**After**
```cpp
  [[nodiscard]] Tensor forward(const Tensor& inputs) const override {
    return inputs.matmul(weight_) + bias_;
  }

  [[nodiscard]] std::vector<Tensor> parameters() const override {
    return {weight_, bias_};
  }
```

Move to `Tanh`.

> Tanh needs the same treatment. It has forward, but no parameters, because it has no weights. As a Layer, it has to answer both, so we'll give it an empty list.

<!-- edit: tanh-layer -->
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
struct Tanh : public Layer {
  [[nodiscard]] Tensor forward(const Tensor& inputs) const override {
    return inputs.tanh();
  }

  [[nodiscard]] std::vector<Tensor> parameters() const override {
    return {};
  }
};
```

Scroll to `MLP`. Point to its three members, then to its `forward` and `parameters`.

> Now that Linear and Tanh are both Layers, look at what MLP does. It holds three layers, passes the input through them in order, and joins their parameters. That is the job we want for any list of layers, not just these three, so we'll repurpose its design. MLP itself stays for the XOR example, and a new class, Sequence, will do the same job for as many layers as we give it.

> The list needs one type that can stand for any layer. A vector of Layer objects can't work, because Layer is abstract and each kind of layer has a different size. A vector of pointers to Layer does work: every pointer is the same size, and each one still leads to the real Linear or Tanh. So Sequence will keep a vector of pointers.

Move to the end of `MLP`, before `linear_forward`.

<!-- edit: sequence -->
**Before**
```cpp
  Linear output_;
};

[[nodiscard]] Tensor linear_forward(
```

**After**
```cpp
  Linear output_;
};

class Sequence {
public:
  void push_back(std::unique_ptr<Layer> layer) {
    layers_.push_back(std::move(layer));
  }

  [[nodiscard]] Tensor forward(const Tensor& inputs) const {
    Tensor current = inputs;
    for (const auto& layer: layers_) {
      current = layer->forward(current);
    }
    return current;
  }

  [[nodiscard]] std::vector<Tensor> parameters() const {
    std::vector<Tensor> result;
    for (const auto& layer: layers_) {
      const std::vector<Tensor> layer_parameters = layer->parameters();
      result.insert(result.end(), layer_parameters.begin(), layer_parameters.end());
    }
    return result;
  }

private:
  std::vector<std::unique_ptr<Layer>> layers_;
};

[[nodiscard]] Tensor linear_forward(
```

While writing `push_back`:

> Push_back takes a unique_ptr, so the Sequence owns every layer it holds and frees it when the Sequence goes away.

While writing `forward`:

> Forward passes the input through each layer in order, so one layer's output becomes the next layer's input.

While writing `parameters`:

> Its parameters are every layer's list joined together, the way MLP joined its two.

## B. Stack the layers | 4:00-5:30

Return to `train_mnist()` and point to the `MLP model` line.

> Let's rebuild our current network from these pieces, by adding its layers in order: a Linear layer with 32 features, tanh, and a Linear layer for the ten digit scores. We create each one with make_unique, which builds the layer on the heap and hands the Sequence a pointer to it. Sequence has the same forward and parameters as MLP, so the rest of train_mnist doesn't change. This changes how the network is built, not what it computes, so we should get exactly the numbers we had before. Let's run it.

<!-- edit: stack-model -->
**Before**
```cpp
    std::mt19937 random(42);
    MLP model(784, 32, 10, random);
```

**After**
```cpp
    std::mt19937 random(42);
    Sequence model;
    model.push_back(std::make_unique<Linear>(784, 32, random));
    model.push_back(std::make_unique<Tanh>());
    model.push_back(std::make_unique<Linear>(32, 10, random));
```

<!-- checkpoint: sequence-matches-mlp -->

The terminal also prints a "Training epoch" line and a blank line around each
epoch. Keep those on screen, and point to the lines below.

```output
Epoch 1 loss: 0.993942
Epoch 2 loss: 0.427191
Epoch 3 loss: 0.339903
Epoch 4 loss: 0.29868
Epoch 5 loss: 0.271741
Test accuracy: 88.2% (1764/2000)
```

> Every loss and the accuracy match, so a list of layers computes exactly what MLP did. Now we can change the network by changing the list.

## C. Make it deeper | 5:30-8:15

Point to the last two `push_back` lines.

> Let's make it deeper. We'll add three more hidden layers after the first one, each a Linear layer with 32 features followed by tanh, for four hidden layers in total. Let's run it.

<!-- edit: deeper-four -->
**Before**
```cpp
    model.push_back(std::make_unique<Tanh>());
    model.push_back(std::make_unique<Linear>(32, 10, random));
```

**After**
```cpp
    model.push_back(std::make_unique<Tanh>());
    model.push_back(std::make_unique<Linear>(32, 32, random));
    model.push_back(std::make_unique<Tanh>());
    model.push_back(std::make_unique<Linear>(32, 32, random));
    model.push_back(std::make_unique<Tanh>());
    model.push_back(std::make_unique<Linear>(32, 32, random));
    model.push_back(std::make_unique<Tanh>());
    model.push_back(std::make_unique<Linear>(32, 10, random));
```

<!-- checkpoint: deeper-four -->

Point to the accuracy, then to the first epoch line.

```output
Epoch 1 loss: 1.777
Epoch 2 loss: 0.741658
Epoch 3 loss: 0.450117
Epoch 4 loss: 0.342193
Epoch 5 loss: 0.278237
Test accuracy: 89.25% (1785/2000)
```

> Eighty-nine point two five percent, up from 88.2. The extra layers helped a little. The first epoch starts slower, though: its loss is 1.78, against 0.99 with one hidden layer. More layers helped, so let's try twice as many.

Point to the same two `push_back` lines at the end of the list.

> We'll add four more hidden layers, each a Linear layer with 32 features followed by tanh, for eight in total. Let's run it.

<!-- edit: deeper-eight -->
**Before**
```cpp
    model.push_back(std::make_unique<Tanh>());
    model.push_back(std::make_unique<Linear>(32, 10, random));
```

**After**
```cpp
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

<!-- checkpoint: deep-plain -->

Point to the first two epoch lines, then to the accuracy.

```output
Epoch 1 loss: 2.30029
Epoch 2 loss: 2.24043
Epoch 3 loss: 1.64858
Epoch 4 loss: 1.22419
Epoch 5 loss: 1.03331
Test accuracy: 63.85% (1277/2000)
```

> Sixty-three point eight five percent, worse than where we started. And look at the first two epochs: the loss stays near 2.3. A loss of 2.3 is pure guessing, one tenth for every digit, so the network learned almost nothing for two full epochs. Doubling the layers made it much worse. Why is it stuck?

## D. Give the optimizer a memory | 8:15-13:45

Keep the failed output visible. Open `gradient_step` and keep it on screen.

> At the start, every layer makes what passes through it smaller. Going forward, the values shrink at each layer, and going backward, so does the gradient. Together, they leave the weight gradients more than fifty times smaller than in our one-hidden-layer network, so each step barely moves anything. This is called the vanishing gradient problem.

> The steps are too small, so the obvious fix is bigger steps. Let's double the learning rate, from 0.1 to 0.2, and run it again.

Move to `train_mnist()`, to the update inside the batch loop.

<!-- edit: lr-double -->
**Before**
```cpp
        loss.backward();
        gradient_step(parameters, 0.1);

        total_loss += loss.at({}) * batch.labels.size();
```

**After**
```cpp
        loss.backward();
        gradient_step(parameters, 0.2);

        total_loss += loss.at({}) * batch.labels.size();
```

<!-- checkpoint: deep-lr-double -->

Point to the accuracy.

```output
Epoch 1 loss: 2.2759
Epoch 2 loss: 1.55947
Epoch 3 loss: 1.15181
Epoch 4 loss: 0.808903
Epoch 5 loss: 0.617169
Test accuracy: 82.9% (1658/2000)
```

> Eighty-two point nine percent, up from 63.85, and the loss starts falling in the second epoch instead of the third. So the slow progress really was the problem: bigger steps help. Why not keep going? Let's try ten times the original, a learning rate of 1.0.

<!-- edit: lr-large -->
**Before**
```cpp
        loss.backward();
        gradient_step(parameters, 0.2);

        total_loss += loss.at({}) * batch.labels.size();
```

**After**
```cpp
        loss.backward();
        gradient_step(parameters, 1.0);

        total_loss += loss.at({}) * batch.labels.size();
```

<!-- checkpoint: deep-lr-large -->

Point to the epoch losses, then to the accuracy.

```output
Epoch 1 loss: 2.06921
Epoch 2 loss: 1.75652
Epoch 3 loss: 1.74619
Epoch 4 loss: 1.95282
Epoch 5 loss: 2.25084
Test accuracy: 10.45% (209/2000)
```

> The loss stops falling after the second epoch and then climbs back up, and accuracy is back to guessing. A step this big overshoots: it jumps past the good weights, lands somewhere worse, and then jumps past again. So a bigger learning rate speeds up every step, including the ones that point the wrong way.

> A big step helps when we're far from a good answer, and hurts when we're close. So let's start big and shrink the step as we go. That's learning rate decay. We'll start at 1.0, the rate that just blew up, and halve it after every epoch, so the epochs use 1.0, 0.5, 0.25, and so on.

Move to `train_mnist()`, below `std::vector<Tensor> parameters = model.parameters();`.

> First, the learning rate becomes a variable we can change, starting at 1.0.

<!-- edit: decay-variable -->
**Before**
```cpp
    std::vector<Tensor> parameters = model.parameters();

    for(std::size_t epoch = 0; epoch < 5; ++epoch) {
```

**After**
```cpp
    std::vector<Tensor> parameters = model.parameters();
    double learning_rate = 1.0;

    for(std::size_t epoch = 0; epoch < 5; ++epoch) {
```

Move to the update inside the batch loop.

> The update now reads the variable instead of the fixed number.

<!-- edit: decay-use -->
**Before**
```cpp
        loss.backward();
        gradient_step(parameters, 1.0);

        total_loss += loss.at({}) * batch.labels.size();
```

**After**
```cpp
        loss.backward();
        gradient_step(parameters, learning_rate);

        total_loss += loss.at({}) * batch.labels.size();
```

Move to the end of the epoch loop, below the loss print.

> And once an epoch is finished, we halve the learning rate for the next one.

<!-- edit: decay-halve -->
**Before**
```cpp
      std::cout << "Epoch " << epoch + 1 << " loss: " << total_loss / seen << "\n\n";
```

**After**
```cpp
      std::cout << "Epoch " << epoch + 1 << " loss: " << total_loss / seen << "\n\n";
      learning_rate *= 0.5;
```

> Same network, same data, and the same starting rate that failed. Let's run it.

<!-- checkpoint: deep-decay -->

Point to the epoch losses, then to the accuracy.

```output
Epoch 1 loss: 2.06921
Epoch 2 loss: 1.47342
Epoch 3 loss: 1.06257
Epoch 4 loss: 0.862743
Epoch 5 loss: 0.757728
Test accuracy: 70.35% (1407/2000)
```

> The first epoch is the same as before, 2.07, because the rate is still 1.0. But now the loss keeps falling every epoch instead of climbing back up, and accuracy is 70.35 percent instead of 10.45. The rate that was too big now trains, because it shrinks before it can overshoot for long.

> It's still below the 82.9 percent from a steady 0.2, and below the 89.25 percent of our four-layer network. Decay shrinks every step, including those of weights that are still crawling toward a good answer. Speeding those up without overshooting takes a different idea, and we'll build it in a later episode.

## E. Recap | 13:45-14:45

```text
Recap

- Layer and Sequence: any layers in one list
- Four hidden layers: 89.25%
- Eight hidden layers: 63.85%
- Learning rate 0.2: 82.9%
- Learning rate 1.0: 10.45%
- Learning rate 1.0, halved every epoch: 70.35%
```

> We built a Sequence that can hold any layer. Four hidden layers raised accuracy a little, to 89.25 percent, but at eight layers training stalled and accuracy fell to 63.85 percent. Doubling the learning rate got it moving, to 82.9 percent, but a rate of 1.0 overshot and fell to 10.45. Halving the rate every epoch tamed that overshoot, and the same starting rate trained to 70.35 percent. The eight-layer network still trails the shallower ones.

Replace the recap with:

```text
Next episode

- Why signals shrink in deep networks
- Residual connections
- Momentum and velocity
```

> Next, we'll look at why the signal shrinks through so many layers, add residual connections to give it a way around them, and give the optimizer a memory with momentum and velocity.

> That brings us to the end of this episode. Thanks for watching, and I will see you next time.

Leave approximately five clean seconds for the Subscribe and complete-series
playlist end-screen elements.
