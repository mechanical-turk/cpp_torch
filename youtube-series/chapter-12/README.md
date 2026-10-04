# Chapter 12 recording preparation

[Script](script.md) · [Review](script-review.md) · [Keyword research](keyword-research.md)

Model comparisons and overfitting checks live in [experiments/](experiments/README.md),
separate from the recording lesson. The training script now prints the epoch,
images processed and running mean loss, using one updating progress line.

Continue the recording main.cpp in aliases/02-screen-long-form. Preserve its
current edits; do not replace it with the frozen Chapter 11 verification
baseline. The supplied mnist_reader.hpp sits beside it.

## Data

From the long-form code repository root, viewers run once:

```sh
bash scripts/download-mnist.sh
```

The downloader places real files under data/, checks their SHA-256 hashes,
and leaves the original IDX contents unchanged. No aliases, external cache
directory, Python packages or text conversion are required:

- train-images-idx3-ubyte and train-labels-idx1-ubyte: all 60,000 training records.
- t10k-images-idx3-ubyte and t10k-labels-idx1-ubyte: all 10,000 test records.

Dataset binaries are ignored by Git. Licensing sources disagree, so the public
repo provides the downloader rather than redistributing the files. See
[source attribution and redistribution decision](../../aliases/02-screen-long-form/data/README.md).
The Content HQ helper, `node youtube-series/chapter-12/prepare-data.mjs`, calls
the same downloader and also saves a local first-image preview under data/.

The C++ training loop reads the first 10,000 training records in original file
order on each epoch. Evaluation reads the first 2,000 separate test records.
Neither weight updates nor hyperparameter selection uses the test images.
There is no shuffle. Results refer to these subsets, not the full MNIST splits.

The supplied mnist_reader.hpp reads and validates binary headers, reads matching
pixel/label bytes and normalizes pixels. Mention the supplied download/reading
helpers in about ten seconds while staying in main.cpp. Do not show setup
commands or teach the parsing implementation in this episode. On camera
we construct Tensor rows, implement the loss/backward, train and evaluate.
One reader handles the initial image and later batches. It has no Tensor
dependency and introduces no generic Dataset/DataLoader abstraction.

Compile and run from the long-form repository root:

```sh
clang++ -std=c++23 -O2 main.cpp -o main
./main
```

Run the compiler command from the long-form code repository after live coding.
Normal -O2 optimization; no disabled checks/vectorization or fast-math tricks.
The optional data/example.pgm preview is available for inspection; the script
now opens directly in main.cpp rather than with an image preview.

## Verification

The current lesson builds exp(), sum_columns() and log(), including their
backward rules. Softmax and cross_entropy_loss are free functions composed
from Tensor operations. Labels become an ordinary one-hot target Tensor in
the loss function. TensorNode is unchanged, with no loss-specific fields.

There are separate runnable demonstrations for exponentials and probabilities
before introducing logarithms and the loss. Sum_columns reduces the digit
columns, preserving one total per image: [images, digits] -> [images, 1].

This is the straightforward first pass. Maximum subtraction, log-softmax and
fused losses are deferred. Extreme scores can overflow/underflow exp; log
rejects nonpositive or nonfinite inputs. The verifier checks this limitation
as a rejection, not a claim of numerical equivalence to a stable fused loss.
The measured training recipe stays within the supported numerical range.

From Content HQ:

```sh
node youtube-series/chapter-12/verify-script.mjs --frozen-baseline
```

Replay every literal edit against the frozen Chapter 11 baseline. Compile/run
the initial image, exp, softmax and completed-loss checkpoints, run real training and test
stages with -O2, then run separate ASan/UBSan derivative and parser checks.
The explicit flag allows verification after recording has progressed. It never
replaces live main.cpp; the verifier checks that its contents remain unchanged.

The verified run reached 1,764/2,000 (88.2%) after five epochs. Earlier text-data
results used a different subset and do not apply to this revision.

Source tests do not establish speaking
pace, rendered code legibility or audience retention. No GitHub push, upload
or social publication occurs.
