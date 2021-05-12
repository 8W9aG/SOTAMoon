"""The block class."""
from hashlib import sha256
import json
import typing

from .signed_transaction import SignedTransaction


INDEX_KEY = "index"
TRANSACTIONS_KEY = "transactions"
TIMESTAMP_KEY = "timestamp"
PREVIOUS_HASH_KEY = "previous_hash"
NONCE_KEY = "nonce"


class Block:
    """A class that represents a transaction block."""
    def __init__(self, index: int, transactions: typing.List[SignedTransaction], timestamp: float, previous_hash: str, nonce: int = 0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce

    def compute_hash(self) -> str:
        """Computes the hash of the JSON block representation."""
        return sha256(str(self).encode()).hexdigest()

    def __str__(self) -> str:
        return json.dumps(dict(self), sort_keys=True)

    def __iter__(self):
        yield INDEX_KEY, self.index
        yield TRANSACTIONS_KEY, [dict(x) for x in self.transactions]
        yield TIMESTAMP_KEY, self.timestamp
        yield PREVIOUS_HASH_KEY, self.previous_hash
        yield NONCE_KEY, self.nonce
