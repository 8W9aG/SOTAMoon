"""The chain class."""
import time
import json

from .block import Block
from .signed_transaction import SignedTransaction
from .wallet import Wallet


MINING_REWARD = 50.0


class Chain:
    """A class that represents a blockchain."""
    def __init__(self, miner_wallet: Wallet):
        self.miner_wallet = miner_wallet
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        """Create the first block of the block chain."""
        genesis_block = Block(0, [], time.time(), "0", self.miner_wallet)
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
        """Add a block to the chain."""
        previous_hash = self.last_block.compute_hash()
        if previous_hash != block.previous_hash:
            return False
        if not self.is_valid_proof(block, proof):
            return False
        self.chain.append(block)
        return True

    def is_valid_proof(self, block, block_hash, difficulty=2):
        """Check whether the hash is valid."""
        return (block_hash.startswith('0' * difficulty) and block_hash == block.compute_hash())

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

    def mine(self):
        """Mine a new block for the blockchain."""
        if not self.unconfirmed_transactions:
            return False
        last_block = self.last_block
        new_block = Block(last_block.index + 1,
                          self.unconfirmed_transactions,
                          time.time(),
                          last_block.hash,
                          self.miner_wallet)
        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)
        self.unconfirmed_transactions = []
        return new_block.index

    def balance(self, wallet: Wallet):
        """Determine the balance of a wallet."""
        balance = 0.0
        for block in self.chain:
            if block.miner_wallet == wallet:
                balance += MINING_REWARD
            for transaction in block.transactions:
                if transaction.sender == wallet:
                    balance -= transaction.value
                elif transaction.recipient == wallet:
                    balance += transaction.value
        return balance

    def unconfirmed_balance(self, wallet: Wallet):
        """Determine the balance of the wallet including unconfirmed transactions."""
        balance = self.balance(wallet)
        for signed_transaction in self.unconfirmed_transactions:
            if signed_transaction.transaction.sender == wallet:
                balance -= signed_transaction.value
        return balance

    def validate_chain(self) -> bool:
        """Check that the entire chain is valid."""
        last_block = None
        balances = {}
        for block in self.chain:
            if last_block is not None:
                if block.previous_hash != last_block.compute_hash():
                    return False
                if not self.is_valid_proof(block, block.compute_hash()):
                    return False
            # Update the balances
            balances[block.miner_wallet.identity] = balances.get(block.miner_wallet.identity, 0.0) + MINING_REWARD
            for signed_transaction in block.transactions:
                balances[signed_transaction.transaction.sender.identity] = balances.get(signed_transaction.transaction.sender.identity, 0.0) - signed_transaction.transaction.value
                balances[signed_transaction.transaction.recipient.identity] = balances.get(signed_transaction.transaction.recipient.identity, 0.0) + signed_transaction.transaction.value
            # Check the balances
            for wallet in balances:
                if balances[wallet] < 0.0:
                    return False
            last_block = block
        return True

    def __str__(self) -> str:
        return json.dumps(list(self), sort_keys=True, indent=4)

    def __iter__(self):
        for block in self.chain:
            yield dict(block)
