"""The class used for providing files over multiple systems."""
import typing
from pathlib import Path

from .provider import Provider
from .file_provider import FileProvider


class JointProvider(Provider):
    """The class for combining two or more providers."""
    def __init__(self):
        super().__init__("joint")
        self.providers = [
            FileProvider(Path(__file__).parent.parent.absolute()),  # Search for models packaged with the program
            FileProvider("results"),
        ]

    def path(self, file_hash: str) -> typing.Optional[str]:
        """Fetch the path for reading the file."""
        for provider in self.providers:
            provider_path = provider.path(file_hash)
            if provider_path is not None:
                return provider_path
        return None
