"""The class for serialising messages."""
from enum import Enum
from sotamoon.transaction import MESSAGE_KEY
import typing


IDENTIFIER_KEY = "id"
TYPE_KEY = "type"


class MessageType(Enum):
    HANDSHAKE = "handshake"
    NODES = "nodes"
    CHAIN = "chain"
    ADD_TX = "add_tx"
    TX = "tx"
    PING = "ping"


class Message:
    """A class for serialising messages within the SOTAMoon protocol."""
    def __init__(self, identifier: str, message_type: MessageType):
        self.identifier = identifier
        self.message_type = message_type

    def __iter__(self):
        yield IDENTIFIER_KEY, self.identifier
        yield TYPE_KEY, self.message_type.value


def message_from_dict(message_dict: typing.Dict[str, typing.Any]) -> Message:
    """Deserialise a message from a dictionary."""
    return Message(message_dict[MESSAGE_KEY], MessageType[message_dict[TYPE_KEY]])
