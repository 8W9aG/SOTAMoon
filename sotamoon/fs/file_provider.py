"""The class used for providing files on the local filesystem."""
import typing
from pathlib import Path
import hashlib
import os
import shutil

from .provider import Provider
from ..network.node import Node


def hash_of_file(file_path: str) -> str:
    """Compute the hash of a file."""
    with open(file_path, "rb") as f:
        readable_hash = hashlib.sha256(f.read()).hexdigest()
        return readable_hash

def file_path_for_file_hash(file_hash: str, folder: str) -> typing.Optional[str]:
    """Find the file path given a file hash in a folder."""
    sub_folder = os.path.join(folder, file_hash)
    if not os.path.exists(sub_folder):
        return None
    for child in Path(sub_folder).iterdir():
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
        super().__init__("file", folder)

    def path(self, file_hash: str, link: str = None, skip_check: bool = False) -> typing.Optional[str]:
        """Find the path for the file hash."""
        return file_path_for_file_hash(file_hash, self.cache_folder)

    def distribute(self, _: str) -> typing.Optional[str]:
        """We are already distributed locally on the file provider."""
        return None

    def write(self, file_name: str, content: bytes) -> typing.Optional[str]:
        """Writes contents to a file hash."""
        file_hash = hashlib.sha256(content).hexdigest()
        sub_folder = os.path.join(self.cache_folder, file_hash)
        os.makedirs(sub_folder, exist_ok=True)
        with open(os.path.join(sub_folder, file_name), "wb") as file_handle:
            file_handle.write(content)
        return file_hash

    def copy(self, file_path: str) -> typing.Optional[str]:
        """Copy file to the cache."""
        file_hash = hash_of_file(file_path)
        sub_folder = os.path.join(self.cache_folder, file_hash)
        os.makedirs(sub_folder, exist_ok=True)
        new_file_path = os.path.join(sub_folder, os.path.basename(file_path))
        shutil.copy(file_path, new_file_path)
        return new_file_path

    def nodes(self, port: int) -> typing.Set[Node]:
        """Report all the nodes the provider is connected to."""
        return set()
