"""The class for peer discovery via hardcoded IP addresses."""
import typing

from .node import Node
from .nodes import Nodes


IP_SEEDS = []


class IP(Nodes):
    """A class for providing nodes for peer discovery via hardcoded IPs."""
    def nodes(self, port: int) -> typing.Set[Node]:
        """Find nodes via DNS."""
        return set([Node(x, port) for x in IP_SEEDS])
