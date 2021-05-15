"""The provider base class."""
import typing


class Provider:
    """The class defining the common methods for all file providers."""
    def __init__(self, identifier: str):
        self.identifier = identifier

    def exists(self, file_hash: str) -> bool:
        """Checks whether the file hash exists."""
        return self.path(file_hash) is not None

    def path(self, _: str, link: str = None) -> typing.Optional[str]:
        raise Exception("path not implemented")

    def distribute(self, _: str) -> typing.Optional[str]:
        raise Exception("distribute not implemented")
