"""The class for peer discovery via random IP."""
import typing

from faker import Faker

from .node import Node
from .nodes import Nodes


class Random(Nodes):
    """A class for providing nodes for peer discovery via random IP."""
    def nodes(self, port: int) -> typing.Set[Node]:
        """Find nodes via DNS."""
        ex = Faker()
        return set([Node(ex.ipv6(), port) for x in range(5)])
