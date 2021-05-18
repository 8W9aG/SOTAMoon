"""The class for peer discovery via zeroconf."""
import typing
import socket

from zeroconf import IPVersion, ServiceBrowser, ServiceStateChange, Zeroconf, ServiceInfo

from .node import Node
from .nodes import Nodes


ZEROCONF_SERVICES = ["_sotamoon._udp.local."]


class ZeroConf(Nodes):
    """A class for peer discovery on local networks."""
    def __init__(self, port: int) -> None:
        self.tracked_nodes = {}
        self.zeroconf = Zeroconf()
        for service in ZEROCONF_SERVICES:
            self.zeroconf.register_service(ServiceInfo(
                service,
                socket.gethostname() + "." + service,
                addresses=[socket.inet_aton("127.0.0.1")],
                port=port,
                properties={},
                server=socket.gethostname(),
            ))
        self.browser = ServiceBrowser(self.zeroconf, ZEROCONF_SERVICES, handlers=[self.service_changed])

    def service_changed(self, zeroconf: Zeroconf, service_type: str, name: str, state_change: ServiceStateChange):
        """Called when a local service changes."""
        key = service_type + "-" + name
        nodes = self.tracked_nodes.get(key, set())
        if state_change == ServiceStateChange.Added:
            info = zeroconf.get_service_info(service_type, name)
            for addr in info.parsed_addresses:
                ip_address, port = addr
                nodes.add(Node(ip_address, port))
        elif state_change == ServiceStateChange.Removed:
            nodes = set()
        self.tracked_nodes[key] = nodes

    def nodes(self, _: int) -> typing.Set[Node]:
        """Report the nodes currently tracked by zeroconf."""
        nodes = set()
        for node_key in self.tracked_nodes:
            nodes |= self.tracked_nodes[node_key]
        return nodes
