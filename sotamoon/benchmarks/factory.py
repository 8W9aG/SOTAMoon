"""The factory class."""
from .benchmark import Benchmark
from .mnist import MNIST_BENCHMARK_IDENTIFIER, MNISTBenchmark


BENCHMARK_IDENTIFIERS = {
    MNIST_BENCHMARK_IDENTIFIER: MNISTBenchmark
}


def create_benchmark(identifier: str) -> Benchmark:
    """Creates a benchmark from an identifier."""
    return BENCHMARK_IDENTIFIERS[identifier]()
