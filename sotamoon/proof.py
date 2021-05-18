"""The proof class."""
import typing

from .constraints import MAX_STRING_LENGTH
from .benchmarks.factory import BENCHMARK_IDENTIFIERS
from .model import Model, model_from_dict


COMPLETION_KEY = "completion"
BENCHMARK_ID_KEY = "benchmark_id"
CITATION_KEY = "citation"
LICENSE_KEY = "license"
MESSAGE_KEY = "message"
MODEL_KEY = "model"


class Proof:
    """The class representing a SOTA proof."""
    def __init__(self, completion: float, benchmark_id: str, citation: str, license: str, message: str, model: Model):
        self.completion = round(completion, 4)
        self.benchmark_id = benchmark_id
        self.citation = citation
        self.license = license
        self.message = message
        self.model = model

    def valid(self) -> bool:
        """Check whether the proof is valid."""
        if self.benchmark_id not in BENCHMARK_IDENTIFIERS:
            return False
        for i in [self.citation, self.license, self.message]:
            if len(i) >= MAX_STRING_LENGTH:
                return False
        return True

    def __iter__(self):
        yield COMPLETION_KEY, self.completion
        yield BENCHMARK_ID_KEY, self.benchmark_id
        yield CITATION_KEY, self.citation
        yield LICENSE_KEY, self.license
        yield MESSAGE_KEY, self.message
        yield MODEL_KEY, dict(self.model)


def proof_from_dict(proof_dict: typing.Dict[str, typing.Any]) -> Proof:
    """Deserialise a proof from a dictionary."""
    return Proof(
        proof_dict[COMPLETION_KEY],
        proof_dict[BENCHMARK_ID_KEY],
        proof_dict[CITATION_KEY],
        proof_dict[LICENSE_KEY],
        proof_dict[MESSAGE_KEY],
        model_from_dict(proof_dict[MODEL_KEY])
    )
