"""The provider base class."""
import typing

from ..network.nodes import Nodes


class Provider(Nodes):
    """The class defining the common methods for all file providers."""
    def __init__(self, identifier: str, cache_folder: str):
        self.identifier = identifier
        self.cache_folder = cache_folder

    def exists(self, file_hash: str) -> bool:
        """Checks whether the file hash exists."""
        return self.path(file_hash) is not None

    def path(self, _: str, link: str = None, skip_check: bool = False) -> typing.Optional[str]:
        raise Exception("path not implemented")

    def distribute(self, link: str) -> typing.Optional[str]:
        raise Exception("distribute not implemented")

    def write(self, file_name: str, content: bytes) -> typing.Optional[str]:
        raise Exception("write not implemented")

    def copy(self, file_path: str) -> typing.Optional[str]:
        raise Exception("copy not implemented")
