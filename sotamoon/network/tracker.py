"""The class for tracking open connections."""
import asyncio
import socket

import bluetooth

from .node import Node
from .protocol import Protocol
from .tracker_nodes import TrackerNodes
from .dns import DNS
from .ip import IP
from .bluetooth import Bluetooth
from .zeroconf import ZeroConf
from .random import Random
from ..chain import Chain
from ..miner import Miner
from ..fs.provider import Provider


STANDARD_SOTAMOON_PORT = 29636
IP_SEEDS = []


class Tracker:
    """A class for keeping track of open connections."""
    def __init__(self, loop: asyncio.BaseEventLoop, chain: Chain, miner: Miner, provider: Provider) -> None:
        self.loop = loop
        self.chain = chain
        self.miner = miner
        self.nodes = [provider, DNS(), IP(), Bluetooth(), ZeroConf(STANDARD_SOTAMOON_PORT), Random()]
        self.tracker_nodes = TrackerNodes()
        asyncio.ensure_future(self.check_new_nodes())

    async def connect(self, node: Node):
        """Attempt to connect to a node."""
        if self.tracker_nodes.has_node(node):
            return
        if node.bluetooth:
            sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            try:
                sock.connect((node.address, node.port))
            except socket.error as exc:
                return
            await self.loop.connect_accepted_socket(lambda: Protocol(
                self.chain,
                self.miner,
                self.tracker_nodes),
                sock)
            return
        try:
            await self.loop.create_datagram_endpoint(
                lambda: Protocol(
                    self.chain,
                    self.miner,
                    self.tracker_nodes),
                remote_addr=(node.address, node.port))
        except OSError:
            pass

    async def server(self):
        """Boot up the server."""
        await self.loop.create_datagram_endpoint(
            lambda: Protocol(
                self.chain,
                self.miner,
                self.tracker_nodes),
            local_addr=('0.0.0.0', STANDARD_SOTAMOON_PORT))

    async def check_new_nodes(self):
        """Checks various sources for possible new nodes."""
        while True:
            nodes = set()
            for nodes_class in self.nodes:
                nodes |= nodes_class.nodes(STANDARD_SOTAMOON_PORT)
            for node in nodes:
                await self.connect(node)
            await asyncio.sleep(60.0)
