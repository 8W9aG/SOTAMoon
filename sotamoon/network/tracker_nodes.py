"""The class for holding the currently connected nodes."""
import typing

from .node import Node


class TrackerNodes:
    """A class for keeping track of connected nodes."""
    def __init__(self) -> None:
        self.nodes = set()

    def has_node(self, node: Node) -> bool:
        """Check whether we are currently connected to a node."""
        return node in self.nodes

    def add_node(self, node: Node):
        """Add a node to the pool."""
        self.nodes.add(node)

    def remove_node(self, node: Node):
        """Remove a node from the pool."""
        self.nodes.remove(node)

    def broadcastable_nodes(self) -> typing.Set[Node]:
        """Find nodes that can be broadcast."""
        return {x for x in self.nodes if not x.bluetooth}
