"""The factory class."""
from .benchmark import Benchmark
from .mnist import MNIST_BENCHMARK_IDENTIFIER, MNISTBenchmark
from ..fs.provider import Provider


BENCHMARK_IDENTIFIERS = {
    MNIST_BENCHMARK_IDENTIFIER: MNISTBenchmark
}


class BenchmarkFactory:
    """The class for creating benchmarks."""
    def __init__(self, provider: Provider):
        self.provider = provider

    def create_benchmark(self, identifier: str) -> Benchmark:
        """Creates a benchmark from an identifier."""
        return BENCHMARK_IDENTIFIERS[identifier](self.provider)
