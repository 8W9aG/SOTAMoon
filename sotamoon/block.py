"""The block class."""
from hashlib import sha256
import json
import typing
import time

from .signed_transaction import SignedTransaction
from .wallet import Wallet
from .proof import Proof
from .benchmarks.mnist import MNIST_BENCHMARK_IDENTIFIER
from .model import Model


TRANSACTIONS_KEY = "transactions"
TIMESTAMP_KEY = "timestamp"
PREVIOUS_HASH_KEY = "previous_hash"
MINER_WALLET_KEY = "miner_wallet"
PROOF_KEY = "proof"


class Block:
    """A class that represents a transaction block."""
    def __init__(
        self,
        transactions: typing.List[SignedTransaction],
        timestamp: float,
        previous_hash: str,
        miner_wallet: Wallet,
        proof: Proof):
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.miner_wallet = miner_wallet
        self.proof = proof

    def valid(self) -> bool:
        """Checks whether the block is valid."""
        return self.proof.valid()

    def __str__(self) -> str:
        return json.dumps(dict(self), sort_keys=True)

    def __iter__(self):
        yield TRANSACTIONS_KEY, [dict(x) for x in self.transactions]
        yield TIMESTAMP_KEY, self.timestamp
        yield PREVIOUS_HASH_KEY, self.previous_hash
        yield MINER_WALLET_KEY, dict(self.miner_wallet)
        yield PROOF_KEY, dict(self.proof)

    def compute_hash(self):
        return sha256(str(self).encode()).hexdigest()


def create_genesis_block(miner_wallet: Wallet) -> Block:
    """Create the first block of the block chain."""
    return Block(
        [],
        time.time(),
        "0",
        miner_wallet,
        Proof(
            94.24,
            MNIST_BENCHMARK_IDENTIFIER,
            "",
            "",
            "",
            Model("18ed48295aa46270de8d4bb6974599becfd3f8c6cc5efb4d62956ae364992628", "")))
