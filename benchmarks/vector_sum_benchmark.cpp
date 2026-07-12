#include <benchmark/benchmark.h>

#include <cstddef>
#include <cstdint>
#include <numeric>
#include <vector>

static void BM_VectorSum(benchmark::State &state) {
  const auto size = static_cast<std::size_t>(state.range(0));
  const std::vector<double> values(size, 1.0);

  for (auto _ : state) {
    double sum = std::accumulate(values.begin(), values.end(), 0.0);
    benchmark::DoNotOptimize(sum);
  }

  state.SetItemsProcessed(state.iterations() * static_cast<std::int64_t>(size));
}

BENCHMARK(BM_VectorSum)->Arg(1 << 10)->Arg(1 << 20);

static void BM_VectorSum_Unobserved(benchmark::State &state) {
  const auto size = static_cast<std::size_t>(state.range(0));
  const std::vector<double> values(size, 1.0);

  for (auto _ : state) {
    std::accumulate(values.begin(), values.end(), 0.0);
  }
}

BENCHMARK(BM_VectorSum_Unobserved)->Arg(1 << 10)->Arg(1 << 20);
