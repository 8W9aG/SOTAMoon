"""The base class for the underlying protocol."""
import asyncio
import logging
import typing

from .node import Node, node_from_dict
from .message import message_from_dict, Message, MessageType
from .compress import decompress, compress
from .tracker_nodes import TrackerNodes
from .. import __version__
from ..chain import Chain
from ..signed_transaction import signed_transaction_from_dict
from ..miner import Miner


MESSAGE_KEY = "message"
PAYLOAD_KEY = "payload"
ADDRESSES_KEY = "addresses"
LINK_KEY = "link"
TRANSACTIONS_KEY = "txs"


class Protocol(asyncio.DatagramProtocol):
    """A class representing shared protocol functions."""
    def __init__(
        self,
        chain: Chain,
        miner: Miner,
        tracker_nodes: TrackerNodes):
        self.chain = chain
        self.miner = miner
        self.tracker_nodes = tracker_nodes
        self.message_ids = set()

    def connection_made(self, transport):
        """Called when a new connection is made."""
        self.transport = transport
        socket = transport.get_extra_info("socket")
        self.node = Node(transport.get_extra_info("peername"), socket.getsockname()[1])
        if self.tracker_nodes.has_node(self.node):
            self.transport.close()
            return
        self.tracker_nodes.add_node(self.node)

    def error_received(self, exc):
        """Called when there is an error with this connection."""
        logging.warning(f"Error Received: {exc}")

    def connection_lost(self, exc):
        """Called when the connection is closed."""
        logging.warning(f"Connection closed: {exc}")
        self.tracker_nodes.remove_node(self.node)

    def datagram_received(self, data, addr):
        """Called when a UDP packet is received."""
        self.transport.sendto(self.handle_data(data), addr)

    def data_received(self, data):
        """Called when data is generally received."""
        self.transport.send(self.handle_data(data))

    def handle_data(self, data: bytes) -> bytes:
        """Handle raw data."""
        request = decompress(data)
        message = message_from_dict(request[MESSAGE_KEY])
        if message.identifier in self.message_ids:
            self.handle_response(request[PAYLOAD_KEY])
            return
        payload = self.handle_request(request[PAYLOAD_KEY])
        if payload is not None:
            return
        response = {
            MESSAGE_KEY: dict(Message(message.identifier, message.message_type)),
            PAYLOAD_KEY: payload,
        }
        return compress(response)

    def handle_request(self, request: typing.Dict, message: Message) -> typing.Optional[typing.Dict]:
        """Handle a request."""
        if message.message_type == MessageType.HANDSHAKE:
            return self.handle_handshake(request)
        elif message.message_type == MessageType.NODES:
            return self.handle_nodes(request)
        elif message.message_type == MessageType.CHAIN:
            return self.handle_chain(request)
        elif message.message_type == MessageType.ADD_TX:
            return self.handle_transaction(request)
        elif message.message_type == MessageType.TX:
            return self.handle_transactions(request)
        return None

    def handle_handshake(self, request: typing.Dict) -> typing.Dict:
        """Handle a handshake request."""
        version_key = "version"
        version = request[PAYLOAD_KEY][version_key]
        logging.info(f"Connected to {self.node.address}:{self.node.port} {version}")
        return {
            version_key: __version__
        }

    def handle_nodes(self, _: typing.Dict) -> typing.Dict:
        """Handle a nodes request."""
        return {
            ADDRESSES_KEY: [dict(x) for x in self.tracker_nodes.broadcastable_nodes()]
        }

    def handle_chain(self, _: typing.Dict) -> typing.Dict:
        """Handle a chain request."""
        return {
            LINK_KEY: self.chain.magnet_link()
        }

    def handle_transaction(self, request: typing.Dict) -> typing.Dict:
        """Handle a transaction request."""
        signed_transaction = signed_transaction_from_dict(request["tx"])
        return {
            "added": self.miner.add_new_transaction(signed_transaction)
        }

    def handle_transactions(self, _: typing.Dict) -> typing.Dict:
        """Handle a transactions request."""
        return {
            TRANSACTIONS_KEY: [dict(x) for x in self.miner.unconfirmed_transactions]
        }

    def handle_response(self, response: typing.Dict, message: Message):
        """Handle the response to a request."""
        if message.message_type == MessageType.NODES:
            self.handle_nodes_response(response)
        elif message.message_type == MessageType.CHAIN:
            self.handle_chain_response(response)
        elif message.message_type == MessageType.TX:
            self.handle_transactions_response(response)

    def handle_nodes_response(self, response: typing.Dict):
        """Handle a nodes response."""
        for node in [node_from_dict(x) for x in response[ADDRESSES_KEY]]:
            if self.tracker_nodes.has_node(node):
                continue
            self.tracker_nodes.node_add(node)

    def handle_chain_response(self, response: typing.Dict):
        """Handle a chain response."""
        self.chain.resolve_conflict(response[LINK_KEY])

    def handle_transactions_response(self, response: typing.Dict):
        """Handle a transactions response."""
        for transaction in [signed_transaction_from_dict(x) for x in response[TRANSACTIONS_KEY]]:
            self.miner.add_new_transaction(transaction)
