"""The main runner."""
import argparse
import time

from .chain import Chain
from .wallet import Wallet
from .transaction import Transaction
from .opened_wallet import generate_wallet
from .signed_transaction import SignedTransaction
from .miner import Miner
from .block import create_genesis_block


WALLET_1 = generate_wallet()
WALLET_2 = Wallet(generate_wallet().identity)
CHAIN = Chain(create_genesis_block(WALLET_1))
MINER = Miner(WALLET_1, CHAIN)


def main() -> None:
    """Run SOTAMoon."""
    print("--- SOTAMoon ---")
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--generate_blocks', type=int, default=1, help="The number of blocks to generate")
    args = parser.parse_args()
    while len(CHAIN.chain) < args.generate_blocks:
        transaction = Transaction(WALLET_1, WALLET_2, 30.0, time.time())
        signed_transaction = SignedTransaction(transaction, transaction.sign_transaction())
        if not MINER.add_new_transaction(signed_transaction):
            print(f"INVALID TRANSACTION: {signed_transaction}")
            return
        new_block = MINER.mine(CHAIN.last_block)
        if new_block is None:
            print("COULD NOT MINE NEW BLOCK")
            return
        CHAIN.add_block(new_block)
    print(str(CHAIN))
    if not CHAIN.validate_chain():
        print("ERROR: INVALID CHAIN")


if __name__ == "__main__":
    main()  # pragma: no cover
