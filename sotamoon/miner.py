"""The miner class."""
import time
import typing

from .wallet import Wallet
from .block import Block
from .signed_transaction import SignedTransaction
from .chain import Chain


class Miner:
    """A class that represents a miner."""
    def __init__(self, miner_wallet: Wallet, chain: Chain):
        self.miner_wallet = miner_wallet
        self.chain = chain
        self.unconfirmed_transactions = []

    def create_genesis_block(self) -> Block:
        """Create the first block of the block chain."""
        return Block(0, [], time.time(), "0", self.miner_wallet)

    def proof_of_work(self, block: Block, difficulty: int = 2):
        """Perform the work needed to make the next block."""
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()

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

    def mine(self, last_block: Block) -> typing.Optional[Block]:
        """Mine a new block for the blockchain."""
        if not self.unconfirmed_transactions:
            return None
        new_block = Block(last_block.index + 1,
                          self.unconfirmed_transactions,
                          time.time(),
                          last_block.compute_hash(),
                          self.miner_wallet)
        self.proof_of_work(new_block)
        self.unconfirmed_transactions = []
        return new_block

    def unconfirmed_balance(self, wallet: Wallet):
        """Determine the balance of the wallet including unconfirmed transactions."""
        balance = self.chain.balance(wallet)
        for signed_transaction in self.unconfirmed_transactions:
            if signed_transaction.transaction.sender == wallet:
                balance -= signed_transaction.value
        return balance
