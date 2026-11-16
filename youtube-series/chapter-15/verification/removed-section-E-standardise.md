Removed from script.md on 2026-11-12 at the creator's request. The verifier no longer replays it.

## E. A fix on the data side | 11:30-14:00

This section is the first thing to cut if the recording runs long. Its code is the largest edit.

> There is another way to speed things up that changes the data and leaves the optimizer alone. Pixels at the corners of an MNIST image hardly ever change, while pixels in the middle swing between 0 and 1. Let's standardise every pixel: subtract its average and divide by its spread, both measured on the training images.

<!-- edit: standardise-statistics -->
**Before**
```cpp
void train_mnist() {
```

**After**
```cpp
struct PixelStatistics {
  std::vector<double> mean;
  std::vector<double> spread;
};

[[nodiscard]] PixelStatistics measure_pixels(std::size_t count) {
  MnistReader reader(
    "data/train-images-idx3-ubyte",
    "data/train-labels-idx1-ubyte"
  );
  const MnistBatch batch = reader.read_batch(count);
  PixelStatistics statistics{
    std::vector<double>(784, 0.0),
    std::vector<double>(784, 0.0)
  };
  for (std::size_t image = 0; image < count; ++image) {
    for (std::size_t pixel = 0; pixel < 784; ++pixel) {
      statistics.mean[pixel] += batch.pixels[image * 784 + pixel] / count;
    }
  }
  for (std::size_t image = 0; image < count; ++image) {
    for (std::size_t pixel = 0; pixel < 784; ++pixel) {
      const double difference =
        batch.pixels[image * 784 + pixel] - statistics.mean[pixel];
      statistics.spread[pixel] += difference * difference / count;
    }
  }
  for (double& value: statistics.spread) {
    value = std::sqrt(value);
  }
  return statistics;
}

void standardise(
  std::vector<double>& pixels,
  const PixelStatistics& statistics
) {
  for (std::size_t index = 0; index < pixels.size(); ++index) {
    const std::size_t pixel = index % 784;
    pixels[index] =
      (pixels[index] - statistics.mean[pixel]) / (statistics.spread[pixel] + 0.1);
  }
}

void train_mnist() {
```

While writing the second function:

> The spread of a pixel that never changes is zero, so we add 0.1 to it before dividing. That keeps those corner pixels from blowing up.

Back in `train_mnist`.

> train_mnist measures the statistics once, and standardises each batch before it becomes a Tensor, for training and for testing, if the flag is on.

<!-- edit: standardise-statistics-call -->
**Before**
```cpp
    std::vector<Tensor> parameters = model.parameters();
```

**After**
```cpp
    std::vector<Tensor> parameters = model.parameters();

    const PixelStatistics statistics = measure_pixels(10000);
    const bool STANDARDISE = false;
```

<!-- edit: standardise-training -->
**Before**
```cpp
          std::min<std::size_t>(BATCH_SIZE, 10000 - seen)
        );
        const Tensor inputs(
```

**After**
```cpp
          std::min<std::size_t>(BATCH_SIZE, 10000 - seen)
        );
        if (STANDARDISE) {
          standardise(batch.pixels, statistics);
        }
        const Tensor inputs(
```

<!-- edit: standardise-testing -->
**Before**
```cpp
        std::min<std::size_t>(64, 2000 - tested)
      );
      const Tensor inputs(
```

**After**
```cpp
        std::min<std::size_t>(64, 2000 - tested)
      );
      if (STANDARDISE) {
        standardise(batch.pixels, statistics);
      }
      const Tensor inputs(
```

> The flag is one more constant. Let's turn it on, set plain gradient descent back to batch 250, five epochs and its rate of 1.0, and run it.

<!-- edit: standardise-sgd-settings -->
**Before**
```cpp
    const std::string OPTIMIZER = "momentum";
    const double learning_rate = 0.1;
    const std::size_t BATCH_SIZE = 64;
    const std::size_t EPOCHS = 2;
```

**After**
```cpp
    const std::string OPTIMIZER = "sgd";
    const double learning_rate = 1.0;
    const std::size_t BATCH_SIZE = 250;
    const std::size_t EPOCHS = 5;
```

<!-- edit: standardise-flag -->
**Before**
```cpp
    const bool STANDARDISE = false;
```

**After**
```cpp
    const bool STANDARDISE = true;
```

<!-- run: sgd-standardised -->
```text
$ clang++ -std=c++23 -O2 main.cpp -o main && ./main
```

```output
Epoch 5 loss: 0.0518548
Test accuracy: 93.6% (1872/2000)
```

> Plain gradient descent now reaches a loss of 0.052, better than the 0.077 momentum reached on the raw pixels, and better than the 0.162 it reached before. Let's also check momentum on standardised pixels, where its best rate is 0.178.

<!-- edit: momentum-standardised-settings -->
**Before**
```cpp
    const std::string OPTIMIZER = "sgd";
    const double learning_rate = 1.0;
```

**After**
```cpp
    const std::string OPTIMIZER = "momentum";
    const double learning_rate = 0.178;
```

<!-- run: momentum-standardised -->
```text
$ clang++ -std=c++23 -O2 main.cpp -o main && ./main
```

```output
Epoch 5 loss: 0.0306788
Test accuracy: 93.3% (1866/2000)
```

> Momentum still helps on top, 0.031 against 0.052. We measured that this change helps, but not why, so that is something to look into later.

