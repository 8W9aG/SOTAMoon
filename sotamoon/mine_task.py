"""The mining task to run in a thread."""
import typing
from threading import Thread
import _thread
import logging
import traceback

from .fs.joint_provider import JointProvider
from .fs.file_provider import hash_of_file
from .benchmarks.factory import BenchmarkFactory
from .benchmarks.model_factory import create_model
from .proof import Proof
from .block import Block
from .model import Model


class MineTask:
    """A class representing a mining task."""
    def __init__(self, provider: JointProvider, benchmark_factory: BenchmarkFactory, block: Block, callback: typing.Callable[[Proof], None]):
        self.provider = provider
        self.benchmark_factory = benchmark_factory
        self.block = block
        self.callback = callback
        self.process = Thread(target = self.mine)
        self.process.start()

    def mine(self) -> Proof:
        """Perform the work needed to make the next block."""
        try:
            model_path = self.provider.path(self.block.proof.model.model_hash, link=self.block.proof.model.magnet_link)
            benchmark = self.benchmark_factory.create_benchmark(self.block.proof.benchmark_id)
            model_path, completion = benchmark.mine(self.block.proof.completion, create_model(model_path))
            model_hash = hash_of_file(model_path)
            model = Model(model_hash, self.provider.distribute(model_hash))
            proof = Proof(completion, self.block.proof.benchmark_id, "", "", "", model)
            self.callback(proof)
        except Exception as e:
            traceback.print_exc()
            logging.error(f"Mine failed: {e}")
            _thread.interrupt_main()

    def stop(self):
        """Stop the mining execution."""
        self.process.terminate()
        self.process.join()
