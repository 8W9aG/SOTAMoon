"""The block class."""
from hashlib import sha256
import json
import typing
import time

from .signed_transaction import SignedTransaction
from .wallet import Wallet


INDEX_KEY = "index"
TRANSACTIONS_KEY = "transactions"
TIMESTAMP_KEY = "timestamp"
PREVIOUS_HASH_KEY = "previous_hash"
NONCE_KEY = "nonce"
MINER_WALLET_KEY = "miner_wallet"


class Block:
    """A class that represents a transaction block."""
    def __init__(
        self,
        index: int,
        transactions: typing.List[SignedTransaction],
        timestamp: float,
        previous_hash: str,
        miner_wallet: Wallet,
        nonce: int = 0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.miner_wallet = miner_wallet

    def __str__(self) -> str:
        return json.dumps(dict(self), sort_keys=True)

    def __iter__(self):
        yield INDEX_KEY, self.index
        yield TRANSACTIONS_KEY, [dict(x) for x in self.transactions]
        yield TIMESTAMP_KEY, self.timestamp
        yield PREVIOUS_HASH_KEY, self.previous_hash
        yield NONCE_KEY, self.nonce
        yield MINER_WALLET_KEY, dict(self.miner_wallet)

    def compute_hash(self):
        return sha256(str(self).encode()).hexdigest()


def create_genesis_block(miner_wallet: Wallet) -> Block:
    """Create the first block of the block chain."""
    return Block(0, [], time.time(), "0", miner_wallet)
