"""The class prototype for providing nodes."""
import typing

from .node import Node


class Nodes:
    """A class for providing nodes for peer discovery."""
    def nodes(self, port: int) -> typing.Set[Node]:
        raise Exception("nodes not implemented")
