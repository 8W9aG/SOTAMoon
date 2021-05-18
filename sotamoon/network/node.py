"""The class representing a node."""
import typing
import json


ADDRESS_KEY = "address"
PORT_KEY = "port"


class Node:
    """The class representing a node."""
    def __init__(self, address: str, port: int, bluetooth: bool = False):
        self.address = address
        self.port = port
        self.bluetooth = bluetooth

    def __iter__(self):
        yield ADDRESS_KEY, self.address
        yield PORT_KEY, self.port

    def __str__(self):
        return json.dumps(dict(self), sort_keys=True)

    def __hash__(self) -> int:
        return hash(str(self))

def node_from_dict(node_dict: typing.Dict[str, typing.Any]) -> Node:
    """Deserialise a message from a dictionary."""
    return Node(node_dict[ADDRESS_KEY], node_dict[PORT_KEY])
