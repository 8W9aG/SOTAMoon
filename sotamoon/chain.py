"""The chain class."""
import json

from .block import Block
from .wallet import Wallet
from .fs.joint_provider import JointProvider
from .benchmarks.factory import create_benchmark
from .benchmarks.model_factory import create_model


MINING_REWARD = 50.0


class Chain:
    """A class that represents a blockchain."""
    def __init__(self, genesis_block: Block):
        self.chain = [genesis_block]
        self.provider = JointProvider()

    @property
    def last_block(self):
        return self.chain[-1]

    def add_block(self, block: Block):
        """Add a block to the chain."""
        previous_hash = self.last_block.compute_hash()
        if previous_hash != block.previous_hash:
            return False
        if not self.verify_block(block):
            return False
        self.chain.append(block)
        return True

    def verify_block(self, block: Block) -> bool:
        """Verifies that the block is valid."""
        if not block.valid():
            return False
        model_path = self.provider.path(block.proof.model_hash)
        if model_path is None:
            return False
        benchmark = create_benchmark(block.proof.benchmark_id)
        model = create_model(model_path)
        completion = benchmark.evaluate(model)
        return completion == block.proof.completion

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

    def validate_chain(self) -> bool:
        """Check that the entire chain is valid."""
        last_block = None
        balances = {}
        for block in self.chain:
            if last_block is not None:
                if block.previous_hash != last_block.compute_hash():
                    return False
                if not self.verify_block(block):
                    return False
            # Update the balances
            balances[block.miner_wallet.identity] = balances.get(block.miner_wallet.identity, 0.0) + MINING_REWARD
            for signed_transaction in block.transactions:
                if not signed_transaction.transaction.valid():
                    return False
                if not signed_transaction.verify():
                    return False
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
