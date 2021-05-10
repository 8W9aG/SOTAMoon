"""The main runner."""
import argparse
import time
import sys
import json

from .chain import Chain
from .block import Block


CHAIN = Chain()


def main() -> None:
    """Run SOTAMoon."""
    print("--- SOTAMoon ---")
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--generate_blocks', type=int, default=1, help="The number of blocks to generate")
    args = parser.parse_args()
    while len(CHAIN.chain) < args.generate_blocks:
        block = Block(len(CHAIN.chain), [], time.time(), CHAIN.last_block.hash)
        CHAIN.add_block(block, CHAIN.proof_of_work(block))
    chain_data = []
    for block in CHAIN.chain:
        chain_data.append(block.__dict__)
    print(json.dumps({"length": len(chain_data), "chain": chain_data}))


if __name__ == "__main__":
    main()  # pragma: no cover
