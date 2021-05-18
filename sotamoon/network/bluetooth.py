"""The class for peer discovery via Bluetooth."""
import typing
import socket

import bluetooth

from .node import Node
from .nodes import Nodes


class Bluetooth(Nodes):
    """A class for providing nodes for peer discovery via DNS."""
    def nodes(self, port: int) -> typing.Set[Node]:
        """Find nodes via Bluetooth."""
        nodes = set()
        try:
            for device in bluetooth.discover_devices(lookup_names = True):
                sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
                try:
                    sock.connect((device, port))
                except socket.error as exc:
                    pass
                nodes.add(Node(device, port, bluetooth = True))
                sock.close()
        except AttributeError:
            pass
        return nodes
