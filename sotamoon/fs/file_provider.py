"""The class used for providing files on the local filesystem."""
import typing
from pathlib import Path
import hashlib

from .provider import Provider


def hash_of_file(file_path: str) -> str:
    """Compute the hash of a file."""
    with open(file_path, "rb") as f:
        readable_hash = hashlib.sha256(f.read()).hexdigest()
        return readable_hash


class FileProvider(Provider):
    """The class for combining two or more providers."""
    def __init__(self, folder: str):
        super().__init__("file")
        self.folder = folder

    def path(self, file_hash: str) -> typing.Optional[str]:
        """Check whether the file exists."""
        for child in Path(self.folder).iterdir():
            if not child.is_file():
                continue
            file_path = child.absolute()
            readable_hash = hash_of_file(file_path)
            if readable_hash == file_hash:
                return file_path
        return None
