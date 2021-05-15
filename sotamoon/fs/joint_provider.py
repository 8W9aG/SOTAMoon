"""The class used for providing files over multiple systems."""
import typing
from pathlib import Path

from .provider import Provider
from .file_provider import FileProvider
from .bittorrent_provider import BitTorrentProvider


class JointProvider(Provider):
    """The class for combining two or more providers."""
    def __init__(self):
        super().__init__("joint")
        cache_folder = "results"
        self.providers = [
            FileProvider(Path(__file__).parent.parent.absolute()),  # Search for models packaged with the program
            FileProvider(cache_folder),
            BitTorrentProvider("torrents", cache_folder)
        ]

    def path(self, file_hash: str, link: str = None) -> typing.Optional[str]:
        """Fetch the path for reading the file."""
        for provider in self.providers:
            provider_path = provider.path(file_hash, link=link)
            if provider_path is not None:
                return provider_path
        return None

    def distribute(self, file_hash: str) -> str:
        """Distributes the file throughout the network."""
        for provider in self.providers:
            link = provider.distribute(file_hash)
            if link is not None:
                return link
        return None
