MP4 filename: `cpp-mnist-handwritten-digit-recognition-neural-network.mp4`

# Episode 12: Recognizing Handwritten Digits in C++

## A. Give the network an image

Begin in main.cpp, with the existing MLP visible. Stay in this file.

> We'll train our C++ neural network to recognize handwritten digits from MNIST, then test it on images it hasn't seen.

Move to the includes. Keep the helper mention to about ten seconds.

> I've included helpers to download MNIST and read its images and labels. We'll use them here so we can focus on training the network.

Add the include while speaking. Do not open the helper files.

<!-- edit: mnist-reader-include -->
**Before**
```cpp
#include <cstddef>
```

**After**
```cpp
#include "mnist_reader.hpp"

#include <cstddef>
```

Immediately above main(), open the training files and read one image.

> Let's read one image. Its 28 by 28 pixels give us 784 inputs. We'll use thirty-two hidden units and ten outputs, one score per digit.

<!-- edit: mnist-model -->
**Before**
```cpp
int main() {
```

**After**
```cpp
void train_mnist() {
  MnistReader preview("data/train-images-idx3-ubyte", "data/train-labels-idx1-ubyte");
  MnistBatch sample = preview.read_batch(1);
  if (sample.labels.empty()) throw std::runtime_error("empty MNIST dataset");
  const Tensor image({sample.labels.size(), 784}, std::move(sample.pixels));
  std::mt19937 random(42);
  MLP model(784, 32, 10, random);
  std::vector<Tensor> parameters = model.parameters();
  const Tensor scores = model.forward(image);
  std::cout << "Correct digit: " << sample.labels[0] << '\n';
  std::cout << "Untrained digit scores:\n";
  for (std::size_t digit = 0; digit < 10; ++digit)
    std::cout << digit << ": " << scores.at({0, digit}) << '\n';
}

int main() {
```

Keep the shapes beside their corresponding calls:

```text
one image:      [1, 784]
hidden + tanh:  [1, 32]
digit scores:   [1, 10]
```

While constructing image:

> We have one label, so this Tensor has one row. Its 784 columns hold the image's pixels. Reading more images will give us more rows without changing the number of columns.

> Each output column gives a score for one digit. The weights are random, so we're checking that the image goes through the network, not expecting a trained answer yet.

At the end of main(), add the call.

<!-- edit: call-mnist -->
**Before**
```cpp
  train_xor();

  std::cout << "Success!\n";
```

**After**
```cpp
  train_xor();
  train_mnist();

  std::cout << "Success!\n";
```

> We should read a five and get ten output scores. Let's run it.

<!-- checkpoint: image-scores -->

Show the actual scores from the run. Do not interpret the untrained result as
accuracy or claim its largest score is fixed across random initializations.

## B. Give those scores a classification loss

> We can now read a batch of images with their labels. When we pass them through the network, each row will have ten raw scores like the ones we printed earlier. These scores are called logits. To train the model, we need a loss that rewards giving the correct digit a higher score than the alternatives.

Point to the correct digit's column.

> Predicting an eight when the image shows a nine is still the wrong class, so we won't compare digit numbers with squared error. We'll use cross-entropy, which gets smaller as the probability assigned to the correct digit increases.

> Before we write the loss, we need to turn these scores into probabilities. They can be negative, and they don't add up to one. We'll use softmax, starting with exp to make them positive.

Keep the printed score row visible beside main.cpp.

> We'll apply exp to each score using our unary helper, so larger scores still give larger results.

In Operation, add exp. Then use the existing unary helper in Tensor.

<!-- edit: exp-operation -->
**Before**
```cpp
  sigmoid,
  tanh
};
```

**After**
```cpp
  sigmoid,
  tanh,
  exp
};
```

<!-- edit: exp-forward -->
**Before**
```cpp
  void zero_grad() {
```

**After**
```cpp
  [[nodiscard]] Tensor exp() const {
    return elementwise_unary(
      Operation::exp,
      [](double value) {
        return std::exp(value);
      }
    );
  }

  void zero_grad() {
```

While writing the lambda:

> We'll apply exp to each score. Larger scores still give larger results, but negative scores now give positive values too.

Move to Tensor::backward(), immediately before the leaf case.

> We need gradients through this step when we train. The derivative of exp is exp itself, so we can reuse the value we just calculated.

<!-- edit: exp-backward -->
**Before**
```cpp
        case Operation::leaf:
```

**After**
```cpp
        case Operation::exp:
          backward_unary(
            output,
            [](double, double result) { return result; }
          );
          break;

        case Operation::leaf:
```

Return to the score-printing loop in train_mnist().

> Let's apply exp to the scores we already have and print the results next to them.
>
> The negative scores should now give positive values below one; positive scores should give values above one.

<!-- edit: show-exponentials -->
**Before**
```cpp
  std::cout << "Untrained digit scores:\n";
  for (std::size_t digit = 0; digit < 10; ++digit)
    std::cout << digit << ": " << scores.at({0, digit}) << '\n';
```

**After**
```cpp
  const Tensor positive = scores.exp();
  std::cout << "digit score exp\n";
  for (std::size_t digit = 0; digit < 10; ++digit)
    std::cout << digit << ' ' << scores.at({0, digit}) << ' '
              << positive.at({0, digit}) << '\n';
```

> Let's run it.

<!-- checkpoint: exp-complete -->

Point to one negative score and its exponential, then to the largest score.

> The values are positive now, and the highest score still has the largest value. To turn them into probabilities, we need to divide by their total.

Show the existing Tensor::sum() and its scalar result.

> For this one image, our existing sum would work. But a batch gives us several rows, with one image per row. Calling sum would add all those rows together, so one image's probabilities would depend on the scores for the other images.

> Each row needs its own total, so its ten probabilities add up to one. Let's add sum_columns to add across the digit columns and return one total per image.

Open Operation, then move to Tensor's public methods for the implementation.

Keep the shape change beside the loops: [images, 10] becomes [images, 1].

<!-- edit: column-sum-operation -->
**Before**
```cpp
  tanh,
  exp
};
```

**After**
```cpp
  tanh,
  exp,
  sum_columns
};
```

<!-- edit: column-sum-forward -->
**Before**
```cpp
  void zero_grad() {
```

**After**
```cpp
  [[nodiscard]] Tensor sum_columns() const {
    if (rank() != 2 || dimension(0) == 0 || dimension(1) == 0)
      throw std::invalid_argument("expected a nonempty matrix");

    const std::size_t rows = dimension(0);
    const std::size_t columns = dimension(1);
    std::vector<double> totals(rows, 0.0);
    for (std::size_t row = 0; row < rows; ++row)
      for (std::size_t column = 0; column < columns; ++column)
        totals[row] += at({row, column});

    Tensor result({rows, 1}, std::move(totals));
    result.node_->operation = Operation::sum_columns;
    result.node_->parents = {node_};
    return result;
  }

  void zero_grad() {
```

While writing the loops and result:

> The outer loop picks an image. The inner loop adds its ten values to that image's total. We keep a single column so division can broadcast the total back across the row.

Return to Tensor::backward().

> Every value in a row contributes once to its total. During backward, each one receives the gradient from that row's total. We must keep the rows separate here too.

<!-- edit: column-sum-backward -->
**Before**
```cpp
        case Operation::leaf:
```

**After**
```cpp
        case Operation::sum_columns: {
          TensorNode* input = output->parents[0].get();
          const std::size_t columns = input->shape[1];
          for (std::size_t row = 0; row < input->shape[0]; ++row)
            for (std::size_t column = 0; column < columns; ++column)
              input->grad[row * columns + column] += output->grad[row];
          break;
        }

        case Operation::leaf:
```

Above train_mnist(), write softmax as a free function.

> We can now put the two steps together. Take the exponentials, add across each row, then divide by the row totals. Our existing broadcasting handles the division.

<!-- edit: softmax-function -->
**Before**
```cpp
void train_mnist() {
```

**After**
```cpp
[[nodiscard]] Tensor softmax(const Tensor& scores) {
  const Tensor positive = scores.exp();
  const Tensor totals = positive.sum_columns();
  return positive / totals;
}

void train_mnist() {
```

Return to the preview's score-printing loop in train_mnist().

> Let's apply softmax to the scores we already printed. I'll put the probability next to each score so we can compare them directly.

<!-- edit: show-probabilities -->
**Before**
```cpp
  const Tensor positive = scores.exp();
  std::cout << "digit score exp\n";
  for (std::size_t digit = 0; digit < 10; ++digit)
    std::cout << digit << ' ' << scores.at({0, digit}) << ' '
              << positive.at({0, digit}) << '\n';
```

**After**
```cpp
  const Tensor probabilities = softmax(scores);
  std::cout << "digit score probability\n";
  for (std::size_t digit = 0; digit < 10; ++digit)
    std::cout << digit << ' ' << scores.at({0, digit}) << ' '
              << probabilities.at({0, digit}) << '\n';
  std::cout << "Probability total: " << probabilities.sum().at({}) << '\n';
```

> The probabilities should be positive and add up to one. The highest score should still have the highest probability. Let's run it.

<!-- checkpoint: softmax-complete -->

Show the actual output. Rounding in the display can affect the apparent sum.

> We now have a probability for each digit instead of an arbitrary score. The network hasn't learned anything new yet; we've only changed how we express its predictions.

## C. Build cross-entropy from the probabilities

Point to the correct digit and its probability in the output.

> Now we can come back to the loss. We want a small penalty when the correct digit has a high probability, and a large penalty when it has a low one. Taking minus the logarithm gives us that behavior.

Show this small reference beside the probability column while speaking:

```text
correct digit probability    loss
1.0                         0.00
0.5                         0.69
0.1                         2.30
```

> As the correct digit's probability approaches one, the loss approaches zero. To calculate it with our Tensors, we need log. We'll add it using the same unary helper.

In Operation and Tensor's public methods:

<!-- edit: log-operation -->
**Before**
```cpp
  exp,
  sum_columns
};
```

**After**
```cpp
  exp,
  sum_columns,
  log
};
```

<!-- edit: log-forward -->
**Before**
```cpp
  void zero_grad() {
```

**After**
```cpp
  [[nodiscard]] Tensor log() const {
    return elementwise_unary(
      Operation::log,
      [](double value) {
        if (!std::isfinite(value) || value <= 0.0)
          throw std::domain_error("log requires a positive finite value");
        return std::log(value);
      }
    );
  }

  void zero_grad() {
```

While writing the lambda:

> Log needs a positive input. We'll check for that, then apply it to each value.

Move to Tensor::backward().

> Its derivative is one divided by the input. The helper multiplies this by the incoming gradient and adds the contribution to the parent.

<!-- edit: log-backward -->
**Before**
```cpp
        case Operation::leaf:
```

**After**
```cpp
        case Operation::log:
          backward_unary(
            output,
            [](double input, double) { return 1.0 / input; }
          );
          break;

        case Operation::leaf:
```

Immediately above softmax(), write cross_entropy_loss().

> We only want the probability of the correct digit in each row. We'll make a target Tensor with a one in that digit's column and zeros elsewhere. Multiplying by it keeps the value we want. This is called a one-hot target.

<!-- edit: composed-cross-entropy -->
**Before**
```cpp
[[nodiscard]] Tensor softmax(const Tensor& scores) {
```

**After**
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

}

[[nodiscard]] Tensor softmax(const Tensor& scores) {
```

While filling targets:

> Each label gives us the column to mark in its row. For a five, we put one in column five and leave the other columns at zero.

Keep the function open. Complete the following edits before running.

> We have a one in the correct digit's column. Now let's calculate minus log of each probability. This gives us the loss we'd assign if each digit were the correct answer. Then we'll use our target to keep only the one we need.

After the target-filling loop, calculate these per-digit losses.

<!-- edit: per-class-losses -->
**Before**
```cpp
    targets.at({row, labels[row]}) = 1.0;
  }

}
```

**After**
```cpp
    targets.at({row, labels[row]}) = 1.0;
  }

  const Tensor log_probabilities = probabilities.log();
  const Tensor negative_one({}, {-1.0});
  const Tensor class_losses = log_probabilities * negative_one;
}
```

While writing the three lines:

> First we take the logs. Then we multiply by minus one to change their signs. Each column now holds a possible loss; we still need to select the correct digit's column.

Show one illustrative row beside targets and class_losses. Column 1 is the
correct class in this three-class example.

```text
probabilities   0.20   0.50   0.30
class losses    1.61   0.69   1.20
targets         0      1      0
selected        0     0.69    0
```

> Multiplying by one keeps the correct digit's loss. Multiplying by zero clears the other columns. We're multiplying matching entries, so every image keeps its own correct answer.

Add the elementwise selection after class_losses.

<!-- edit: select-class-losses -->
**Before**
```cpp
  const Tensor class_losses = log_probabilities * negative_one;
}
```

**After**
```cpp
  const Tensor class_losses = log_probabilities * negative_one;
  const Tensor selected_losses = class_losses * targets;
}
```

> Each row now has its correct digit's loss and zeros everywhere else. We can sum the whole Tensor to get the total loss for the batch, then divide by the number of images to get the average.

Add the sum and average after selected_losses.

<!-- edit: average-class-losses -->
**Before**
```cpp
  const Tensor selected_losses = class_losses * targets;
}
```

**After**
```cpp
  const Tensor selected_losses = class_losses * targets;
  const Tensor total_loss = selected_losses.sum();

  const double image_count = static_cast<double>(labels.size());
  const Tensor batch_size({}, {image_count});
  const Tensor mean_loss = total_loss / batch_size;
  return mean_loss;
}
```

While writing batch_size and mean_loss:

> We'll put the image count in a scalar Tensor so we can use our existing division operator. We divide by the number of images, not the number of columns, because we selected one loss per image.

Point to the existing multiply, sum and division calls.

> Cross-entropy is now built from smaller operations, just like our mean squared error. Their backward rules will carry the gradients through the loss and softmax into the network.

<!-- checkpoint: loss-complete -->

No run of an unfinished forward/backward implementation. Full numerical checks
stay in the verification workflow.

## D. Train with mini-batches

Return to train_mnist(), below the preview's score loop.

> We can turn scores into probabilities and calculate a loss from the correct labels. Let's put those functions into the training loop. We'll read sixty-four images, make predictions, and update the model before reading the next batch.

> We'll use the first ten thousand training images and go through them five times. Each pass is an epoch, so the outer loop will reopen the file at the start of each epoch.

Add the training loop below the preview.

<!-- edit: train-batches -->
**Before**
```cpp
    std::cout << digit << ' ' << scores.at({0, digit}) << ' '
              << probabilities.at({0, digit}) << '\n';
  std::cout << "Probability total: " << probabilities.sum().at({}) << '\n';
}
```

**After**
```cpp
    std::cout << digit << ' ' << scores.at({0, digit}) << ' '
              << probabilities.at({0, digit}) << '\n';
  std::cout << "Probability total: " << probabilities.sum().at({}) << '\n';

  for (std::size_t epoch = 0; epoch < 5; ++epoch) {
    std::cout << "Training epoch " << epoch + 1 << "/5\n" << std::flush;
    MnistReader training("data/train-images-idx3-ubyte", "data/train-labels-idx1-ubyte");
    double total_loss = 0.0;
    std::size_t seen = 0;

    while (seen < 10000) {
      MnistBatch batch = training.read_batch(std::min<std::size_t>(64, 10000 - seen));
      if (batch.labels.empty()) break;
      const Tensor inputs({batch.labels.size(), 784}, std::move(batch.pixels));
      for (Tensor& parameter : parameters)
        parameter.zero_grad();

      const Tensor logits = model.forward(inputs);
      const Tensor probabilities = softmax(logits);
      Tensor loss = cross_entropy_loss(probabilities, batch.labels);
      loss.backward();
      gradient_step(parameters, 0.1);

      total_loss += loss.at({}) * batch.labels.size();
      seen += batch.labels.size();
      if (seen % 2048 == 0 || seen == 10000)
        std::cout << "\r  " << seen << "/10000 images | mean loss: "
                  << total_loss / seen << "    " << std::flush;
    }
    if (seen == 0) throw std::runtime_error("empty training data");
    std::cout << '\n';
    std::cout << "Epoch " << epoch + 1 << " loss: "
              << total_loss / seen << std::endl;
  }
}
```

While writing the batch read and gradient reset:

> The reader gives us pixels and labels for the next batch. We'll put the pixels into a Tensor, then clear the parameter gradients before making new predictions.

At forward, loss, backward and update:

> The model gives us scores, softmax converts them to probabilities, and cross_entropy_loss uses the labels to measure the error. Calling backward follows the operations we just built; gradient_step then updates the model's parameters.

At total_loss and seen:

> To report an average for the epoch, we'll add up the losses from all its images. Our function returns a batch average, so we multiply by the batch size before adding it to the total.

At the progress output:

> We'll print progress every couple of thousand images. Using a carriage return updates the same line, so we can follow the image count and average loss without filling the terminal.

Before running:

> We should see the average loss fall as training progresses. Each epoch's number includes predictions made throughout that pass, while the weights were changing. Let's run it.

<!-- checkpoint: trained-mnist -->

Epoch summaries from the measured local run; the live progress line updates
between these summaries:

```text
Epoch 1 loss: 0.994
Epoch 2 loss: 0.427
Epoch 3 loss: 0.340
Epoch 4 loss: 0.299
Epoch 5 loss: 0.272
```

Training time is a wait to cut from the edit, not a real-time training promise.
Initialization and final values can differ across standard libraries.

## E. Check images the network hasn't seen

> The training loss has fallen, but these are images the model has already practiced on. Let's check two thousand images from the separate test set and count how many digits it gets right.

Above train_mnist(), add count_correct.

> For each image, we'll choose the digit with the highest score and compare it with the label. We saw that softmax preserves the order of the scores, so we can choose the answer directly from the model's output.

<!-- edit: count-correct -->
**Before**
```cpp
void train_mnist() {
```

**After**
```cpp
[[nodiscard]] std::size_t count_correct(
  const Tensor& scores,
  const std::vector<std::size_t>& labels
) {
  if (scores.rank() != 2 || scores.dimension(0) != labels.size() ||
      scores.dimension(1) != 10)
    throw std::invalid_argument("expected ten scores per image");
  std::size_t correct = 0;
  for (std::size_t row = 0; row < labels.size(); ++row) {
    std::size_t predicted = 0;
    for (std::size_t digit = 1; digit < 10; ++digit)
      if (scores.at({row, digit}) > scores.at({row, predicted}))
        predicted = digit;
    correct += predicted == labels[row];
  }
  return correct;
}

void train_mnist() {
```

While writing the two loops:

> For each row, we'll keep the column of the highest score we've found. After checking all ten digits, we'll add one to the count if our choice matches the label.

Return to the end of train_mnist(). Read test batches and report accuracy.

> Now we'll call this function on batches from the test file. We're measuring the trained model here, so we'll leave its weights alone and only count predictions.

<!-- edit: test-accuracy -->
**Before**
```cpp
              << total_loss / seen << std::endl;
  }
}
```

**After**
```cpp
              << total_loss / seen << std::endl;
  }

  MnistReader test("data/t10k-images-idx3-ubyte", "data/t10k-labels-idx1-ubyte");
  std::size_t correct = 0;
  std::size_t tested = 0;
  while (tested < 2000) {
    MnistBatch batch = test.read_batch(std::min<std::size_t>(64, 2000 - tested));
    if (batch.labels.empty()) break;
    const Tensor inputs({batch.labels.size(), 784}, std::move(batch.pixels));
    correct += count_correct(model.forward(inputs), batch.labels);
    tested += batch.labels.size();
  }
  if (tested == 0) throw std::runtime_error("empty test data");
  std::cout << "Test accuracy: " << 100.0 * correct / tested
            << "% (" << correct << '/' << tested << ")\n";
}
```

While writing the final line:

> We've counted the correct answers and the total images. Dividing those counts gives our accuracy; multiplying by a hundred displays it as a percentage.

> Let's run it and check the test accuracy.

<!-- checkpoint: evaluated-mnist -->

Measured local output:

```text
Test accuracy: 88.200% (1764/2000)
```

Report the actual recording run if it differs. This is the 2,000-image subset,
not the full MNIST test set.

> We trained on ten thousand images and measured this accuracy on two thousand different ones. The image data, predictions, loss and gradients are now all connected through our C++ implementation.


## G. Recap

```text
Recap

- Images as Tensor rows
- Ten digit scores per image
- Exp, log and column sums
- Softmax and cross-entropy from Tensor operations
- Mini-batch gradient descent
- Accuracy on unseen images
- Comparing network setups
```

> We added exp, log and a column reduction, then used them to build softmax and cross-entropy. With those functions, our MLP can learn from image batches and we can measure its accuracy on unseen digits.

Replace the recap with:

```text
Next steps

- Save trained weights
- Load the model without retraining
- Inspect individual predictions
```

> That brings us to the end of this episode. Thanks for watching, and I will see you next time.

Leave approximately five clean seconds for Subscribe and the complete-series
playlist end-screen elements.
