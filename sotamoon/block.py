"""The block class."""
from hashlib import sha256
import json
import typing
import time
import os

from .signed_transaction import SignedTransaction, signed_transaction_from_dict
from .wallet import Wallet, wallet_from_dict
from .proof import Proof, proof_from_dict
from .benchmarks.mnist import MNIST_BENCHMARK_IDENTIFIER
from .model import Model
from .fs.provider import Provider


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
        """Compute the hash of this block."""
        return sha256(str(self).encode()).hexdigest()


def create_genesis_block(miner_wallet: Wallet, provider: Provider) -> Block:
    """Create the first block of the block chain."""
    model_hash = "18ed48295aa46270de8d4bb6974599becfd3f8c6cc5efb4d62956ae364992628"
    file_path = provider.path(model_hash)
    if file_path is None:
        file_path = provider.copy(os.path.join(os.path.dirname(__file__), "mnist.pth"))
    link = provider.distribute(model_hash)
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
            Model(model_hash, link)))

def block_from_dict(block_dict: typing.Dict[str, typing.Any]) -> Block:
    """Deserialise a block from a dictionary."""
    return Block(
        [signed_transaction_from_dict(x) for x in block_dict[TRANSACTIONS_KEY]],
        block_dict[TIMESTAMP_KEY],
        block_dict[PREVIOUS_HASH_KEY],
        wallet_from_dict(block_dict[MINER_WALLET_KEY]),
        proof_from_dict(block_dict[MINER_WALLET_KEY]),
    )
