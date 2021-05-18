"""The main runner."""
import argparse
import logging
import asyncio

from .chain import Chain
from .wallet import Wallet
from .opened_wallet import generate_wallet
from .miner import Miner
from .block import create_genesis_block
from .fs.joint_provider import JointProvider
from .benchmarks.factory import BenchmarkFactory
from .network.tracker import Tracker


WALLET_1 = generate_wallet()
WALLET_2 = Wallet(generate_wallet().identity)
PROVIDER = JointProvider()
BENCHMARK_FACTORY = BenchmarkFactory(PROVIDER)
CHAIN = Chain([create_genesis_block(WALLET_1, PROVIDER)], PROVIDER, BENCHMARK_FACTORY)
MINER = Miner(WALLET_1, CHAIN, PROVIDER, BENCHMARK_FACTORY)


async def async_main(loop) -> None:
    """Run SOTAMoon."""
    print("--- SOTAMoon ---")
    logging.basicConfig(level=logging.INFO)
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--generate_blocks', type=int, default=1, help="The number of blocks to generate")
    args = parser.parse_args()
    # Start mining
    MINER.mine(CHAIN.last_block, CHAIN.last_block)
    # Start networking
    tracker = Tracker(loop, CHAIN, MINER, PROVIDER)
    await tracker.server()

def main() -> None:
    """Run the async main."""
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_main(loop))
    loop.run_forever()

if __name__ == "__main__":
    main()
