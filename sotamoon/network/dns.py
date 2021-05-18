"""The class for peer discovery via DNS."""
import typing

import dns.resolver

from .node import Node
from .nodes import Nodes


DNS_SEEDS = [
    "seed.sotamoon.com"
]


class DNS(Nodes):
    """A class for providing nodes for peer discovery via DNS."""
    def nodes(self, port: int) -> typing.Set[Node]:
        """Find nodes via DNS."""
        nodes = set()
        for dns_seed in DNS_SEEDS:
            try:
                result = dns.resolver.query(dns_seed, "A")
                nodes |= set([Node(x, port) for x in result])
            except dns.resolver.NXDOMAIN:
                pass
        return nodes
