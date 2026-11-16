MP4 filename: `cpp-momentum-adam-optimizers-from-scratch.mp4`

# Episode 15: Momentum and Adam Optimizers from Scratch in C++

Continue in the same `main.cpp` that ended Episode 14: Tensor, autograd, Layer, Linear, Tanh, ReLU,
Residual, Sequence, `train_mnist` and every example stay. Read only the `>` passages aloud.
Before/After blocks show the exact edits; output blocks and notes are not narration. Settings live as
constants at the top of the training loop, and each run changes only the constants named in its block.

## A. A fair test bench | 0:00-3:30

Frame zero: `main.cpp` open at `train_mnist`, terminal beside it. Show the title "Momentum and Adam
Optimizers from Scratch in C++" over the code for the first five seconds. No separate title card.
Speak immediately.

> Today we add momentum and the Adam optimizer to our MNIST network, and measure how much faster each one trains than plain stochastic gradient descent. Plain gradient descent chooses every step from the slope where it stands, and forgets it right after. Momentum remembers.

Select the model block in `train_mnist`.

> To compare optimizers fairly we need a network that trains in seconds, so let's replace the sixteen residual layers with one hidden layer of 256 ReLU units. hidden_layer takes the activation as a template argument, so ReLU goes in the angle brackets, and the last Linear maps the 256 values to ten digits.

<!-- edit: small-network -->
**Before**
```cpp
    std::mt19937 random(42);
    // MLP model(784, 32, 10, random);

    Sequence model;


    model.push_back(hidden_layer(784, 32, random));

    const int NUM_HIDDEN_LAYERS = 15;
    for (int i = 0; i < NUM_HIDDEN_LAYERS; ++i) {
      model.push_back(Residual(hidden_layer(32, 32, random)));
    }

    model.push_back(Linear(32, 10, random));
```

**After**
```cpp
    std::mt19937 random(42);

    Sequence model;
    model.push_back(hidden_layer<ReLU>(784, 256, random));
    model.push_back(Linear(256, 10, random));
```

Scroll to the epoch loop in `train_mnist`.

> We are going to try a lot of settings, so let's collect them as constants right above the epoch loop: the optimizer, the learning rate, the batch size and the number of epochs. We also drop the learning rate decay, so each method keeps one fixed rate and the comparison stays clean.

<!-- edit: settings-constants -->
**Before**
```cpp
    const std::size_t EPOCHS = 20;
    const double INITIAL_LEARNING_RATE = 0.08;
    const double DECAY_RATE = 0.95;

    double learning_rate = INITIAL_LEARNING_RATE;

    for(std::size_t epoch = 0; epoch < EPOCHS; ++epoch) {
```

**After**
```cpp
    const std::string OPTIMIZER = "sgd";
    const double learning_rate = 1.0;
    const std::size_t BATCH_SIZE = 250;
    const std::size_t EPOCHS = 5;

    for(std::size_t epoch = 0; epoch < EPOCHS; ++epoch) {
```

<!-- edit: settings-batch -->
**Before**
```cpp
          std::min<std::size_t>(64, 10000 - seen)
```

**After**
```cpp
          std::min<std::size_t>(BATCH_SIZE, 10000 - seen)
```

> The optimizer name chooses how we use the gradients. For now there is only plain gradient descent, and any other name stops the program with an error.

<!-- edit: settings-update -->
**Before**
```cpp
          print_trace(trace);
        }
        gradient_step(parameters, learning_rate);
```

**After**
```cpp
          print_trace(trace);
        }
        if (OPTIMIZER == "sgd") {
          gradient_step(parameters, learning_rate);
        } else {
          throw std::invalid_argument("unknown optimizer: " + OPTIMIZER);
        }
```

<!-- edit: settings-decay -->
**Before**
```cpp
      std::cout << "Epoch " << epoch + 1 << " loss: " << total_loss / seen << "\n\n";

      learning_rate *= DECAY_RATE;
    }
```

**After**
```cpp
      std::cout << "Epoch " << epoch + 1 << " loss: " << total_loss / seen << "\n\n";
    }
```

Scroll to the `print_trace` call in the training loop.

> The layer trace prints how big the signal and the gradient are at every layer, but only on the first batch. Let's print it on the last batch too, so each run shows how the network changed.

<!-- edit: trace-end -->
**Before**
```cpp
        if (epoch == 0 && seen == 0) {
          print_trace(trace);
        }
```

**After**
```cpp
        const bool first_batch = epoch == 0 && seen == 0;
        const bool last_batch =
          epoch + 1 == EPOCHS && seen + batch.labels.size() == 10000;
        if (first_batch || last_batch) {
          print_trace(trace);
        }
```

Switch to the terminal.

> Let's run plain stochastic gradient descent with a learning rate of 1.0, batches of 250 images and five epochs, which is what the constants say. I tried seven learning rates for each method and kept the best one after five epochs, and for plain gradient descent that was 1.0.

<!-- run: sgd-baseline -->
```text
$ clang++ -std=c++23 -O2 main.cpp -o main && ./main
```

Show the two layer traces, the last epoch line and the test accuracy; the first lines of output are the sample prediction.

```output
layer  1  Sequence[Linear, ReLU]            signal 1.3e-01  gradient 1.4e-04
layer  2  Linear                            signal 7.3e-02  gradient 1.2e-03
layer  1  Sequence[Linear, ReLU]            signal 4.8e-01  gradient 1.4e-04
layer  2  Linear                            signal 3.8e+00  gradient 3.0e-04
Epoch 5 loss: 0.162037
Test accuracy: 91.3% (1826/2000)
```

> After five epochs the loss is 0.162, and the network gets 1,826 of the 2,000 test images right. That's our baseline. In the traces, the signal out of the last layer grew from 0.073 to 3.8, and its gradient shrank from 1.2e-3 to 3.0e-4. The network's scores grew, and the gradient shrank as the loss fell.

## B. Momentum | 3:30-7:00

Scroll to `gradient_step`.

> Plain gradient descent uses each gradient once and throws it away. Momentum keeps a velocity for every parameter. Each step the velocity becomes ninety percent of its old value plus the new gradient, and the parameter moves along the velocity instead of along the gradient. A direction that keeps showing up builds speed, and gradients that keep flipping sign cancel each other out. Let's write that next to gradient_step.

<!-- edit: momentum-step -->
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

void momentum_step(
  std::vector<Tensor>& parameters,
  std::vector<std::vector<double>>& velocities,
  double learning_rate,
  double momentum
) {
  for (std::size_t slot = 0; slot < parameters.size(); ++slot) {
    Tensor& parameter = parameters[slot];
    for (std::size_t index = 0; index < parameter.numel(); ++index) {
      velocities[slot][index] =
        momentum * velocities[slot][index] + parameter.grad()[index];
      parameter.data()[index] -= learning_rate * velocities[slot][index];
    }
  }
}
```

While writing the body:

> The velocities live outside the function, one list per parameter tensor, because they have to survive from one step to the next. Each element is the momentum times its old velocity plus the current gradient, and the parameter moves by the learning rate times that velocity.

Back in `train_mnist`, above the epoch loop.

> Now train_mnist creates the velocities, all zero to start, and the optimizer name gets a second choice.

<!-- edit: momentum-state -->
**Before**
```cpp
    for(std::size_t epoch = 0; epoch < EPOCHS; ++epoch) {
```

**After**
```cpp
    const double MOMENTUM = 0.9;
    std::vector<std::vector<double>> velocities;
    for (const Tensor& parameter: parameters) {
      velocities.emplace_back(parameter.numel(), 0.0);
    }

    for(std::size_t epoch = 0; epoch < EPOCHS; ++epoch) {
```

<!-- edit: momentum-update -->
**Before**
```cpp
        if (OPTIMIZER == "sgd") {
          gradient_step(parameters, learning_rate);
        } else {
```

**After**
```cpp
        if (OPTIMIZER == "sgd") {
          gradient_step(parameters, learning_rate);
        } else if (OPTIMIZER == "momentum") {
          momentum_step(parameters, velocities, learning_rate, MOMENTUM);
        } else {
```

> First the lazy comparison: the same settings as plain gradient descent, learning rate 1.0, and only the optimizer changes.

<!-- edit: momentum-settings -->
**Before**
```cpp
    const std::string OPTIMIZER = "sgd";
```

**After**
```cpp
    const std::string OPTIMIZER = "momentum";
```

<!-- run: momentum-same-rate -->
```text
$ clang++ -std=c++23 -O2 main.cpp -o main && ./main
```

Show only the layer lines of the last trace, the last epoch line and the test accuracy, here and in the next two runs; the first trace is identical to the baseline's.

```output
layer  1  Sequence[Linear, ReLU]            signal 7.5e-01  gradient 2.4e-03
layer  2  Linear                            signal 1.1e+01  gradient 4.5e-04
Epoch 5 loss: 0.499629
Test accuracy: 82.1% (1642/2000)
```

> Momentum is worse here. The loss is 0.50 and only 1,642 test images are right, against 1,826. In the last trace the first layer's gradient is 2.4e-3, about seventeen times plain gradient descent's 1.4e-4, so this network is being pushed much harder.
>
> Here is why a velocity pushes harder. Say the gradient for one weight is 1 on every step. The velocity is 1 on the first step, then 1.9, then 2.71, and it keeps growing toward 10. So when gradients keep pointing the same way, each step ends up about ten times what plain gradient descent would take with the same rate.
>
> To take about the same size of step as plain gradient descent, let's divide the rate by ten and try 0.1.

<!-- edit: momentum-rate-tenth -->
**Before**
```cpp
    const double learning_rate = 1.0;
```

**After**
```cpp
    const double learning_rate = 0.1;
```

<!-- run: momentum-tenth -->
```text
$ clang++ -std=c++23 -O2 main.cpp -o main && ./main
```

```output
layer  1  Sequence[Linear, ReLU]            signal 5.9e-01  gradient 1.4e-04
layer  2  Linear                            signal 4.8e+00  gradient 3.3e-04
Epoch 5 loss: 0.171738
Test accuracy: 91.6% (1832/2000)
```

> The loss is 0.172 against 0.162, and 1,832 test images are right against 1,826. That's about the same, and the first layer's gradient is back to 1.4e-4. So at the same step size, momentum gives no gain. If it helps, it has to be because it lets us take a bigger step. So let's raise the rate and watch the loss. I'll multiply the rate by 1.78 each time. I picked that spacing so that four steps make a factor of ten, from 0.1 to 1.0, and it is only a convenient spacing, so a rate in between could do slightly better.

Show this on screen as a text overlay. Each entry is the loss after five epochs, batch 250.

```text
learning rate   0.1    0.178  0.316  0.562  1.0
momentum        0.172  0.111  0.077  0.124  0.500
```

> I ran each of these. The loss falls until 0.316 and then rises, and the 1.0 is the run we did a minute ago. So we keep 0.316, the rate with the lowest loss among the ones we tried.

<!-- edit: momentum-rate-best -->
**Before**
```cpp
    const double learning_rate = 0.1;
```

**After**
```cpp
    const double learning_rate = 0.316;
```

<!-- run: momentum-batch-250 -->
```text
$ clang++ -std=c++23 -O2 main.cpp -o main && ./main
```

```output
layer  1  Sequence[Linear, ReLU]            signal 6.4e-01  gradient 1.5e-04
layer  2  Linear                            signal 6.8e+00  gradient 2.1e-04
Epoch 5 loss: 0.0768752
Test accuracy: 93.75% (1875/2000)
```

> At 0.316 the first layer's gradient is 1.5e-4, the same size as plain gradient descent's, while the last layer's signal grew to 6.8. So the warning sign at a rate of 1.0 was that gradient jumping to seventeen times its normal size.
>
> The loss after five epochs is 0.077, less than half of plain gradient descent's 0.162, and the test score goes from 1,826 to 1,875. I repeated this with five other random starting weights, and momentum's loss came out at about half to two thirds of plain gradient descent's every time.

## C. Adam | 7:00-10:00

> Momentum remembers which way we have been going. Adam keeps two memories for every parameter, and it starts out looking a lot like momentum_step, so let's copy momentum_step, paste it below, and rename the copy adam_step.

<!-- edit: adam-copy-momentum -->
**Before**
```cpp
      parameter.data()[index] -= learning_rate * velocities[slot][index];
    }
  }
}
```

**After**
```cpp
      parameter.data()[index] -= learning_rate * velocities[slot][index];
    }
  }
}

void adam_step(
  std::vector<Tensor>& parameters,
  std::vector<std::vector<double>>& velocities,
  double learning_rate,
  double momentum
) {
  for (std::size_t slot = 0; slot < parameters.size(); ++slot) {
    Tensor& parameter = parameters[slot];
    for (std::size_t index = 0; index < parameter.numel(); ++index) {
      velocities[slot][index] =
        momentum * velocities[slot][index] + parameter.grad()[index];
      parameter.data()[index] -= learning_rate * velocities[slot][index];
    }
  }
}
```

> The loop is the same: for every weight, update a memory, then move the parameter. Now the changes. The memory becomes a running average of the gradient: ninety percent of the old average plus ten percent of the new gradient. So the new gradient is multiplied by one minus beta1, which keeps the average about the size of a gradient, where momentum's velocity adds them up. The ninety percent moves inside the function as beta1, because we won't tune it. And velocities is renamed first_moments.

<!-- edit: adam-first-moment -->
**Before**
```cpp
void adam_step(
  std::vector<Tensor>& parameters,
  std::vector<std::vector<double>>& velocities,
  double learning_rate,
  double momentum
) {
  for (std::size_t slot = 0; slot < parameters.size(); ++slot) {
    Tensor& parameter = parameters[slot];
    for (std::size_t index = 0; index < parameter.numel(); ++index) {
      velocities[slot][index] =
        momentum * velocities[slot][index] + parameter.grad()[index];
      parameter.data()[index] -= learning_rate * velocities[slot][index];
    }
  }
}
```

**After**
```cpp
void adam_step(
  std::vector<Tensor>& parameters,
  std::vector<std::vector<double>>& first_moments,
  double learning_rate
) {
  const double beta1 = 0.9;
  for (std::size_t slot = 0; slot < parameters.size(); ++slot) {
    Tensor& parameter = parameters[slot];
    for (std::size_t index = 0; index < parameter.numel(); ++index) {
      const double gradient = parameter.grad()[index];
      first_moments[slot][index] =
        beta1 * first_moments[slot][index] + (1.0 - beta1) * gradient;
      parameter.data()[index] -= learning_rate * first_moments[slot][index];
    }
  }
}
```

For the next three blocks, the After block shows the whole function and only the new lines are typed.

> The second memory is a running average of the squared gradient: ninety-nine point nine percent of the old value plus a tenth of a percent of the new squared gradient.

<!-- edit: adam-second-moment -->
**Before**
```cpp
void adam_step(
  std::vector<Tensor>& parameters,
  std::vector<std::vector<double>>& first_moments,
  double learning_rate
) {
  const double beta1 = 0.9;
  for (std::size_t slot = 0; slot < parameters.size(); ++slot) {
    Tensor& parameter = parameters[slot];
    for (std::size_t index = 0; index < parameter.numel(); ++index) {
      const double gradient = parameter.grad()[index];
      first_moments[slot][index] =
        beta1 * first_moments[slot][index] + (1.0 - beta1) * gradient;
      parameter.data()[index] -= learning_rate * first_moments[slot][index];
    }
  }
}
```

**After**
```cpp
void adam_step(
  std::vector<Tensor>& parameters,
  std::vector<std::vector<double>>& first_moments,
  std::vector<std::vector<double>>& second_moments,
  double learning_rate
) {
  const double beta1 = 0.9;
  const double beta2 = 0.999;
  for (std::size_t slot = 0; slot < parameters.size(); ++slot) {
    Tensor& parameter = parameters[slot];
    for (std::size_t index = 0; index < parameter.numel(); ++index) {
      const double gradient = parameter.grad()[index];
      first_moments[slot][index] =
        beta1 * first_moments[slot][index] + (1.0 - beta1) * gradient;
      second_moments[slot][index] =
        beta2 * second_moments[slot][index] + (1.0 - beta2) * gradient * gradient;
      parameter.data()[index] -= learning_rate * first_moments[slot][index];
    }
  }
}
```

> Squaring makes every value positive, so this measures how large this parameter's gradients usually are, whichever way they point.

> Now we use it. The step becomes the average gradient divided by the square root of the average squared gradient. A parameter whose gradients are usually big gets divided by a big number and takes a smaller step, and a parameter with small gradients takes a bigger one. The tiny epsilon only stops a division by zero.

<!-- edit: adam-step-size -->
**Before**
```cpp
void adam_step(
  std::vector<Tensor>& parameters,
  std::vector<std::vector<double>>& first_moments,
  std::vector<std::vector<double>>& second_moments,
  double learning_rate
) {
  const double beta1 = 0.9;
  const double beta2 = 0.999;
  for (std::size_t slot = 0; slot < parameters.size(); ++slot) {
    Tensor& parameter = parameters[slot];
    for (std::size_t index = 0; index < parameter.numel(); ++index) {
      const double gradient = parameter.grad()[index];
      first_moments[slot][index] =
        beta1 * first_moments[slot][index] + (1.0 - beta1) * gradient;
      second_moments[slot][index] =
        beta2 * second_moments[slot][index] + (1.0 - beta2) * gradient * gradient;
      parameter.data()[index] -= learning_rate * first_moments[slot][index];
    }
  }
}
```

**After**
```cpp
void adam_step(
  std::vector<Tensor>& parameters,
  std::vector<std::vector<double>>& first_moments,
  std::vector<std::vector<double>>& second_moments,
  double learning_rate
) {
  const double beta1 = 0.9;
  const double beta2 = 0.999;
  const double epsilon = 1e-8;
  for (std::size_t slot = 0; slot < parameters.size(); ++slot) {
    Tensor& parameter = parameters[slot];
    for (std::size_t index = 0; index < parameter.numel(); ++index) {
      const double gradient = parameter.grad()[index];
      first_moments[slot][index] =
        beta1 * first_moments[slot][index] + (1.0 - beta1) * gradient;
      second_moments[slot][index] =
        beta2 * second_moments[slot][index] + (1.0 - beta2) * gradient * gradient;
      parameter.data()[index] -= learning_rate
        * first_moments[slot][index]
        / (std::sqrt(second_moments[slot][index]) + epsilon);
    }
  }
}
```

Back in `train_mnist`.

> That's the whole update for now. train_mnist needs the two lists, and the optimizer name gets its third choice.

<!-- edit: adam-state -->
**Before**
```cpp
    std::vector<std::vector<double>> velocities;
    for (const Tensor& parameter: parameters) {
      velocities.emplace_back(parameter.numel(), 0.0);
    }
```

**After**
```cpp
    std::vector<std::vector<double>> velocities;
    std::vector<std::vector<double>> first_moments;
    std::vector<std::vector<double>> second_moments;
    for (const Tensor& parameter: parameters) {
      velocities.emplace_back(parameter.numel(), 0.0);
      first_moments.emplace_back(parameter.numel(), 0.0);
      second_moments.emplace_back(parameter.numel(), 0.0);
    }
```

<!-- edit: adam-update -->
**Before**
```cpp
        } else if (OPTIMIZER == "momentum") {
          momentum_step(parameters, velocities, learning_rate, MOMENTUM);
        } else {
```

**After**
```cpp
        } else if (OPTIMIZER == "momentum") {
          momentum_step(parameters, velocities, learning_rate, MOMENTUM);
        } else if (OPTIMIZER == "adam") {
          adam_step(parameters, first_moments, second_moments, learning_rate);
        } else {
```

> Adam's best learning rate is much smaller, 0.01. Same batch size, same five epochs. Let's run it exactly as we wrote it.

<!-- edit: adam-settings -->
**Before**
```cpp
    const std::string OPTIMIZER = "momentum";
    const double learning_rate = 0.316;
```

**After**
```cpp
    const std::string OPTIMIZER = "adam";
    const double learning_rate = 0.01;
```

<!-- run: adam-no-correction -->
```text
$ clang++ -std=c++23 -O2 main.cpp -o main && ./main
```

```output
Epoch 1 loss: 1.18179
Epoch 5 loss: 0.134096
Test accuracy: 91.15% (1823/2000)
```

> After the first epoch the loss is 1.18, and after five epochs it is 0.134 with 1,823 test images right. That's worse than momentum's 0.077, and the first epoch is where it goes wrong. To see why, first remember what Adam is aiming for. It divides the average gradient by the typical size of the gradient. When a gradient keeps the same size, the average gradient has that size, and so does the typical size, so the ratio is 1 and the weight moves by exactly the learning rate. That is the point of the division: whether a weight's gradients are big or small, the learning rate sets how far it moves on each step.
>
> Let's check that with a made-up example: a weight whose gradient is exactly 1 on every step. Adam should move it by the learning rate every time.

Show this on screen as a text overlay, and reveal it one row at a time while the narration reaches each row.

```text
step                         1       2       3
first average                0.1     0.19    0.271
second average               0.001   0.002   0.003
sqrt(second)                 0.0316  0.0447  0.0547
first / sqrt(second)         3.16    4.25    4.95
```

> Both averages start at zero. The first one is a running average of the gradient, so it should be 1. After the first step it is only 0.1, because ninety percent of it is still the zero we started with. After the second step it is 0.19, after the third 0.271, and it climbs toward 1 slowly.
>
> The second average has the same problem, and a worse one. It should be 1 too, but it only takes a tenth of a percent of each new squared gradient, so it is 0.001 after the first step, 0.002 after the second, and 0.003 after the third.
>
> Adam divides the first average by the square root of the second, which is the new row: 0.0316, 0.0447, 0.0547. After the first step that is 0.1 divided by 0.0316, which is 3.16. After the second step it is 0.19 divided by 0.0447, which is 4.25, and after the third 0.271 divided by 0.0547, which is 4.95. We wanted 1 each time. The second average is too small by a much bigger factor than the first one, so the division makes the steps too big, and the first epoch suffers for it.
>
> The fix is to keep track of how many steps we have taken. Call it the step number. After that many steps, the part of an average that comes from real gradients is one minus beta to the power of the step number. For the first average that is 0.1, then 0.19, then 0.271, exactly the values we saw. For the second average it is 0.001, 0.002, 0.003.
>
> So we divide each average by that part. The first average comes back to 1, the second comes back to 1, and the step is exactly the learning rate.

Show one more row under the table.

```text
after dividing by that part  1.00    1.00    1.00
```

> As the step number grows, beta to the power of the step number shrinks toward zero, that part approaches 1, and the division stops changing anything. For the first average that takes about fifty steps. The second average takes thousands, and our five epochs are only 200 steps, so in this run the division matters the whole way through.
>
> So we pass the step number into adam_step, and write the two divisions.

<!-- edit: adam-bias-correction -->
**Before**
```cpp
void adam_step(
  std::vector<Tensor>& parameters,
  std::vector<std::vector<double>>& first_moments,
  std::vector<std::vector<double>>& second_moments,
  double learning_rate
) {
  const double beta1 = 0.9;
  const double beta2 = 0.999;
  const double epsilon = 1e-8;
  for (std::size_t slot = 0; slot < parameters.size(); ++slot) {
    Tensor& parameter = parameters[slot];
    for (std::size_t index = 0; index < parameter.numel(); ++index) {
      const double gradient = parameter.grad()[index];
      first_moments[slot][index] =
        beta1 * first_moments[slot][index] + (1.0 - beta1) * gradient;
      second_moments[slot][index] =
        beta2 * second_moments[slot][index] + (1.0 - beta2) * gradient * gradient;
      parameter.data()[index] -= learning_rate
        * first_moments[slot][index]
        / (std::sqrt(second_moments[slot][index]) + epsilon);
    }
  }
}
```

**After**
```cpp
void adam_step(
  std::vector<Tensor>& parameters,
  std::vector<std::vector<double>>& first_moments,
  std::vector<std::vector<double>>& second_moments,
  std::size_t step_count,
  double learning_rate
) {
  const double beta1 = 0.9;
  const double beta2 = 0.999;
  const double epsilon = 1e-8;
  const double correction1 = 1.0 - std::pow(beta1, static_cast<double>(step_count));
  const double correction2 = 1.0 - std::pow(beta2, static_cast<double>(step_count));
  for (std::size_t slot = 0; slot < parameters.size(); ++slot) {
    Tensor& parameter = parameters[slot];
    for (std::size_t index = 0; index < parameter.numel(); ++index) {
      const double gradient = parameter.grad()[index];
      first_moments[slot][index] =
        beta1 * first_moments[slot][index] + (1.0 - beta1) * gradient;
      second_moments[slot][index] =
        beta2 * second_moments[slot][index] + (1.0 - beta2) * gradient * gradient;
      parameter.data()[index] -= learning_rate
        * (first_moments[slot][index] / correction1)
        / (std::sqrt(second_moments[slot][index] / correction2) + epsilon);
    }
  }
}
```

> And train_mnist counts the steps.

<!-- edit: adam-step-count-state -->
**Before**
```cpp
      second_moments.emplace_back(parameter.numel(), 0.0);
    }
```

**After**
```cpp
      second_moments.emplace_back(parameter.numel(), 0.0);
    }
    std::size_t step_count = 0;
```

<!-- edit: adam-step-count-update -->
**Before**
```cpp
        } else if (OPTIMIZER == "adam") {
          adam_step(parameters, first_moments, second_moments, learning_rate);
```

**After**
```cpp
        } else if (OPTIMIZER == "adam") {
          ++step_count;
          adam_step(parameters, first_moments, second_moments, step_count, learning_rate);
```

<!-- run: adam-batch-250 -->
```text
$ clang++ -std=c++23 -O2 main.cpp -o main && ./main
```

```output
Epoch 1 loss: 0.550623
Epoch 5 loss: 0.0510026
Test accuracy: 93.65% (1873/2000)
```

> With the step number, the first epoch's loss is 0.55 instead of 1.18, and the final loss is 0.051 instead of 0.134. I tried six random starting weights, and without the step number the final loss was worse every time: 0.087 to 0.134, against 0.050 to 0.056. At rates of 0.056 and 0.1 the version without it stopped with an error on all six starts. The loss of 0.051 is lower than momentum's 0.077 and about a third of plain gradient descent's. The test score is 1,873, about the same as momentum's 1,875. Across my other starting weights Adam's loss was about six to seven tenths of momentum's.

Show this table on screen as a text overlay. Each entry is the loss after five epochs, batch 250, for the learning rate in its column; "stops" means the loss became infinite and the program stopped.

```text
learning rate   0.178  0.316  0.562  1.0    1.78   3.16   5.62
plain SGD       0.334  0.276  0.205  0.162  2.143  stops  stops

learning rate   0.056  0.1    0.178  0.316  0.562  1.0    1.78
momentum        0.237  0.172  0.111  0.077  0.124  0.500  2.329

learning rate   0.0032 0.0056 0.01   0.018  0.032  0.056  0.1
Adam            0.125  0.078  0.051  0.061  0.074  0.154  0.522
```

> This is how I picked the three rates. Plain gradient descent has a narrow window: a rate of 1.0 gives 0.162, 1.78 already gives 2.14, and 3.16 stops the program. Adam kept its loss under 0.08 for four of the seven rates I tried, which is a gentler search.

## D. Where momentum stops helping | 10:00-11:30

> Everything so far used batches of 250 images, but this series has trained with batches of 64, so let's try that. I found the best rates the same way: 0.562 for plain gradient descent, and 0.1 for momentum. Two epochs each.

<!-- edit: sgd-batch-64-settings -->
**Before**
```cpp
    const std::string OPTIMIZER = "adam";
    const double learning_rate = 0.01;
    const std::size_t BATCH_SIZE = 250;
    const std::size_t EPOCHS = 5;
```

**After**
```cpp
    const std::string OPTIMIZER = "sgd";
    const double learning_rate = 0.562;
    const std::size_t BATCH_SIZE = 64;
    const std::size_t EPOCHS = 2;
```

<!-- run: sgd-batch-64 -->
```text
$ clang++ -std=c++23 -O2 main.cpp -o main && ./main
```

```output
Epoch 2 loss: 0.218582
Test accuracy: 91.65% (1833/2000)
```

<!-- edit: momentum-batch-64-settings -->
**Before**
```cpp
    const std::string OPTIMIZER = "sgd";
    const double learning_rate = 0.562;
```

**After**
```cpp
    const std::string OPTIMIZER = "momentum";
    const double learning_rate = 0.1;
```

<!-- run: momentum-batch-64 -->
```text
$ clang++ -std=c++23 -O2 main.cpp -o main && ./main
```

```output
Epoch 2 loss: 0.208776
Test accuracy: 89.25% (1785/2000)
```

> At batch size 64, momentum's loss is 0.209 against 0.219, barely lower, and it gets fewer test images right, 1,785 against 1,833. I saw the same on all six random starts I tried. A common explanation is that small batches make each gradient noisy, so there is less steady direction to remember. We haven't tested that here, so take it as a guess.

## E. Recap and what's next | 11:30-12:30

> Let's recap. Momentum keeps a velocity for every parameter, and with batches of 250 it reached about half of plain gradient descent's loss after five epochs. Adam keeps a running average of the gradient and of its square, and it reached a lower loss than momentum. Each method needed its own learning rate, and plain gradient descent had the narrowest window. With batches of 64, momentum barely helped.

On screen, as a short list:

```text
Next episode
- Training on more data
- Whether these gaps hold as the data grows
- Ways to stop the network memorising its training images
```

> Next, we'll train on more data, check whether these gaps hold as the data grows, and look at ways to stop the network memorising its training images.

> That brings us to the end of this episode. Thanks for watching, and I will see you next time.

Hold about five clean seconds for the Subscribe and playlist end-screen elements.
