"""The signed transaction class."""
import typing
import json

from .transaction import Transaction, transaction_from_dict


TRANSACTION_KEY = "transaction"
SIGNATURE_KEY = "signature"


class SignedTransaction:
    def __init__(self, transaction: Transaction, signature: str):
        self.transaction = transaction
        self.signature = signature

    def verify(self) -> bool:
        """Verify the signed transaction."""
        return self.transaction.sender.verify(str(self.transaction), self.signature)

    def __str__(self) -> str:
        return json.dumps(dict(self), sort_keys=True)

    def __iter__(self):
        yield TRANSACTION_KEY, dict(self.transaction)
        yield SIGNATURE_KEY, self.signature


def signed_transaction_from_dict(signed_transaction_dict: typing.Dict[str, typing.Any]) -> SignedTransaction:
    """Deserialise a signed transaction from a dictionary."""
    return SignedTransaction(
        transaction_from_dict(signed_transaction_dict[TRANSACTION_KEY]),
        signed_transaction_dict[SIGNATURE_KEY])
