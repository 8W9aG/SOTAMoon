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

def file_path_for_file_hash(file_hash: str, folder: str) -> typing.Optional[str]:
    """Find the file path given a file hash in a folder."""
    for child in Path(folder).iterdir():
        if not child.is_file():
            continue
        file_path = child.absolute()
        readable_hash = hash_of_file(file_path)
        if readable_hash == file_hash:
            return str(file_path)
    return None

class FileProvider(Provider):
    """The class for providing files from the local filesystem."""
    def __init__(self, folder: str):
        super().__init__("file")
        self.folder = folder

    def path(self, file_hash: str, link: str = None) -> typing.Optional[str]:
        """Find the path for the file hash."""
        return file_path_for_file_hash(file_hash, self.folder)

    def distribute(self, _: str) -> typing.Optional[str]:
        """We are already distributed locally on the file provider."""
        return None
