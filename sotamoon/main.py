"""The main runner."""
import argparse
import time

from .chain import Chain
from .wallet import Wallet
from .transaction import Transaction
from .opened_wallet import generate_wallet
from .signed_transaction import SignedTransaction


WALLET_1 = generate_wallet()
WALLET_2 = Wallet(generate_wallet().identity)
CHAIN = Chain(WALLET_1)


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
        CHAIN.add_new_transaction(signed_transaction)
        CHAIN.mine()
    print(str(CHAIN))
    if not CHAIN.validate_chain():
        print("ERROR: INVALID CHAIN")


if __name__ == "__main__":
    main()  # pragma: no cover
