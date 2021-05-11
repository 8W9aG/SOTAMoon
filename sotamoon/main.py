"""The main runner."""
import argparse
import time
import json

from .chain import Chain
from .block import Block
from .wallet import Wallet
from .transaction import Transaction, GENESIS_SENDER


CHAIN = Chain()
WALLET_1 = Wallet()
WALLET_2 = Wallet()
T0 = Transaction(GENESIS_SENDER, WALLET_1, 500.0)
T0.sign_transaction()
TRANSACTIONS = [T0]


def main() -> None:
    """Run SOTAMoon."""
    print("--- SOTAMoon ---")
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--generate_blocks', type=int, default=1, help="The number of blocks to generate")
    args = parser.parse_args()
    while len(CHAIN.chain) < args.generate_blocks:
        block_transactions = []
        if len(CHAIN.chain) - 1 < len(TRANSACTIONS):
            block_transactions.append(TRANSACTIONS[len(CHAIN.chain) - 1])
        print(block_transactions)
        block = Block(len(CHAIN.chain), block_transactions, time.time(), CHAIN.last_block.hash)
        CHAIN.add_block(block, CHAIN.proof_of_work(block))
    chain_data = []
    for block in CHAIN.chain:
        chain_data.append(block.__dict__)
    print(json.dumps({"length": len(chain_data), "chain": chain_data}))


if __name__ == "__main__":
    main()  # pragma: no cover
