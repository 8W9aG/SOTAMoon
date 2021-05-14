"""The proof class."""
from .constraints import MAX_STRING_LENGTH
from .benchmarks.factory import BENCHMARK_IDENTIFIERS


MODEL_HASH_KEY = "model_hash"
COMPLETION_KEY = "completion"
BENCHMARK_ID_KEY = "benchmark_id"
CITATION_KEY = "citation"
LICENSE_KEY = "license"
MESSAGE_KEY = "message"


class Proof:
    """The class representing a SOTA proof."""
    def __init__(self, model_hash: str, completion: float, benchmark_id: str, citation: str, license: str, message: str):
        self.model_hash = model_hash
        self.completion = round(completion, 4)
        self.benchmark_id = benchmark_id
        self.citation = citation
        self.license = license
        self.message = message

    def valid(self) -> bool:
        """Check whether the proof is valid."""
        if self.benchmark_id not in BENCHMARK_IDENTIFIERS:
            return False
        for i in [self.citation, self.license, self.message]:
            if len(i) >= MAX_STRING_LENGTH:
                return False
        return True

    def __iter__(self):
        yield MODEL_HASH_KEY, self.model_hash
        yield COMPLETION_KEY, self.completion
        yield BENCHMARK_ID_KEY, self.benchmark_id
        yield CITATION_KEY, self.citation
        yield LICENSE_KEY, self.license
        yield MESSAGE_KEY, self.message
