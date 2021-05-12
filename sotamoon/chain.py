"""The chain class."""
import time
import json

from .block import Block
from .signed_transaction import SignedTransaction
from .wallet import Wallet


class Chain:
    """A class that represents a blockchain."""
    def __init__(self, genesis_wallet: Wallet):
        self.genesis_wallet = genesis_wallet
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        """Create the first block of the block chain."""
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, block, difficulty=2):
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash

    def add_block(self, block, proof):
        previous_hash = self.last_block.hash
        if previous_hash != block.previous_hash:
            return False
        if not self.is_valid_proof(block, proof):
            return False
        block.hash = proof
        self.chain.append(block)
        return True

    def is_valid_proof(self, block, block_hash, difficulty=2):
        return (block_hash.startswith('0' * difficulty) and block_hash == block.compute_hash())

    def add_new_transaction(self, signed_transaction: SignedTransaction) -> bool:
        """Add a new unconfirmed transaction to the chain."""
        if not signed_transaction.verify():
            return False
        self.unconfirmed_transactions.append(signed_transaction)
        return True

    def mine(self):
        """Mine a new block for the blockchain."""
        if not self.unconfirmed_transactions:
            return False
        last_block = self.last_block
        new_block = Block(index=last_block.index + 1,
                          transactions=self.unconfirmed_transactions,
                          timestamp=time.time(),
                          previous_hash=last_block.hash)
        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)
        self.unconfirmed_transactions = []
        return new_block.index

    def __str__(self) -> str:
        return json.dumps(list(self), sort_keys=True, indent=4)

    def __iter__(self):
        for block in self.chain:
            yield dict(block)
