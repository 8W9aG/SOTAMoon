"""The main runner."""
import argparse
import time
import logging

from .chain import Chain
from .wallet import Wallet
from .transaction import Transaction
from .opened_wallet import generate_wallet
from .signed_transaction import SignedTransaction
from .miner import Miner
from .block import create_genesis_block
from .fs.joint_provider import JointProvider
from .benchmarks.factory import BenchmarkFactory


WALLET_1 = generate_wallet()
WALLET_2 = Wallet(generate_wallet().identity)
PROVIDER = JointProvider()
BENCHMARK_FACTORY = BenchmarkFactory(PROVIDER)
CHAIN = Chain(create_genesis_block(WALLET_1), PROVIDER, BENCHMARK_FACTORY)
MINER = Miner(WALLET_1, CHAIN, PROVIDER, BENCHMARK_FACTORY)


def main() -> None:
    """Run SOTAMoon."""
    print("--- SOTAMoon ---")
    logging.basicConfig(level=logging.INFO)
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--generate_blocks', type=int, default=1, help="The number of blocks to generate")
    args = parser.parse_args()
    while len(CHAIN.chain) < args.generate_blocks:
        print("Generating next block...")
        transaction = Transaction(WALLET_1, WALLET_2, 30.0, time.time(), "Whatever")
        signed_transaction = SignedTransaction(transaction, transaction.sign_transaction())
        if not MINER.add_new_transaction(signed_transaction):
            print(f"INVALID TRANSACTION: {signed_transaction}")
            return
        new_block = MINER.mine(CHAIN.last_block, CHAIN.last_block)
        if new_block is None:
            print("COULD NOT MINE NEW BLOCK")
            return
        if not CHAIN.add_block(new_block):
            print("FAILED TO ADD BLOCK TO CHAIN")
            return
    print(str(CHAIN))
    if not CHAIN.validate_chain():
        print("ERROR: INVALID CHAIN")


if __name__ == "__main__":
    main()  # pragma: no cover
