"""The transaction class."""
import typing
import json

from .wallet import Wallet, wallet_from_dict
from .constraints import MAX_STRING_LENGTH


SENDER_KEY = "sender"
RECIPIENT_KEY = "recipient"
VALUE_KEY = "value"
TIME_KEY = "time"
MESSAGE_KEY = "message"


class Transaction:
    def __init__(self, sender: Wallet, recipient: Wallet, value: float, transaction_time: float, message: str):
        self.sender = sender
        self.recipient = recipient
        self.value = value
        self.time = transaction_time
        self.message = message

    def sign_transaction(self) -> str:
        """Sign the transaction."""
        return self.sender.sign(str(self))

    def valid(self) -> bool:
        """Check whether the transaction is valid."""
        return self.sender != self.recipient and len(self.message) < MAX_STRING_LENGTH

    def __str__(self) -> str:
        return json.dumps(dict(self), sort_keys=True)

    def __iter__(self):
        yield SENDER_KEY, dict(self.sender)
        yield RECIPIENT_KEY, dict(self.recipient)
        yield VALUE_KEY, self.value
        yield TIME_KEY, self.time
        yield MESSAGE_KEY, self.message


def transaction_from_dict(transaction_dict: typing.Dict[str, typing.Any]) -> Transaction:
    """Deserialise a transaction from a dictionary."""
    return Transaction(
        wallet_from_dict(transaction_dict[SENDER_KEY]),
        wallet_from_dict(transaction_dict[RECIPIENT_KEY]),
        transaction_dict[VALUE_KEY],
        transaction_dict[TIME_KEY],
        transaction_dict[MESSAGE_KEY])
