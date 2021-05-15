"""The miner class."""
import time
import typing

from .wallet import Wallet
from .block import Block
from .signed_transaction import SignedTransaction
from .chain import Chain
from .proof import Proof
from .benchmarks.factory import create_benchmark
from .fs.file_provider import hash_of_file
from .fs.joint_provider import JointProvider
from .model import Model


MINIMUM_TRANSACTIONS = 1

class Miner:
    """A class that represents a miner."""
    def __init__(self, miner_wallet: Wallet, chain: Chain, provider: JointProvider):
        self.miner_wallet = miner_wallet
        self.chain = chain
        self.provider = provider
        self.unconfirmed_transactions = []

    def proof_of_work(self, block: Block) -> Proof:
        """Perform the work needed to make the next block."""
        benchmark = create_benchmark(block.proof.benchmark_id)
        model_path, completion = benchmark.mine(block.proof.completion)
        model_hash = hash_of_file(model_path)
        model = Model(model_hash, self.provider.distribute(model_hash))
        return Proof(completion, block.proof.benchmark_id, "", "", "", model)

    def is_valid_transaction(self, signed_transaction: SignedTransaction) -> bool:
        """Whether a transaction is valid."""
        if not signed_transaction.transaction.valid():
            return False
        if not signed_transaction.verify():
            return False
        sender_balance = self.unconfirmed_balance(signed_transaction.transaction.sender)
        if sender_balance < signed_transaction.transaction.value:
            return False
        return True

    def add_new_transaction(self, signed_transaction: SignedTransaction) -> bool:
        """Add a new unconfirmed transaction to the chain."""
        if not self.is_valid_transaction(signed_transaction):
            return False
        self.unconfirmed_transactions.append(signed_transaction)
        return True

    def mine(self, last_block: Block, last_benchmark_block: Block) -> typing.Optional[Block]:
        """Mine a new block for the blockchain."""
        if len(self.unconfirmed_transactions) < MINIMUM_TRANSACTIONS:
            return None
        proof = self.proof_of_work(last_benchmark_block)
        new_block = Block(
            self.unconfirmed_transactions,
            time.time(),
            last_block.compute_hash(),
            self.miner_wallet,
            proof)
        self.unconfirmed_transactions = []
        return new_block

    def unconfirmed_balance(self, wallet: Wallet):
        """Determine the balance of the wallet including unconfirmed transactions."""
        balance = self.chain.balance(wallet)
        for signed_transaction in self.unconfirmed_transactions:
            if signed_transaction.transaction.sender == wallet:
                balance -= signed_transaction.value
        return balance
