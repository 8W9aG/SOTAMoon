"""The benchmark class."""
import typing

from .model import Model
from ..fs.provider import Provider

class Benchmark:
    """The benchmark base class."""
    def __init__(self, identifier: str, provider: Provider):
        self.identifier = identifier
        self.provider = provider
        self.download()

    def download(self) -> None:
        raise Exception("download not implemented")

    def evaluate(self, _: Model) -> float:
        raise Exception("evaluate not implemented")

    def mine(self, _: float) -> typing.Tuple[str, float]:
        raise Exception("mine not implemented")
