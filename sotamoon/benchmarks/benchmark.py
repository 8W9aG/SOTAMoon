"""The benchmark class."""
import typing
import logging
import sys

import numpy as np
import gym
from stable_baselines3.common.env_checker import check_env
from stable_baselines3 import PPO

from .model import Model
from ..fs.provider import Provider
from .modelenv import ENVIRONMENT_ID


MATING_PARENTS = 5


gym.envs.registration.register(id=ENVIRONMENT_ID, entry_point='sotamoon.benchmarks.modelenv:ModelEnv')


class Benchmark:
    """The benchmark base class."""
    def __init__(self, identifier: str, provider: Provider):
        self.identifier = identifier
        self.provider = provider
        self.download()

    def download(self) -> None:
        raise Exception("download not implemented")

    def evaluate(self, _: Model) -> float:
        raise Exception("evaluate not implemented")

    def example_data(self) -> np.array:
        raise Exception("example_data not implemented")

    def example_output(self) -> np.array:
        raise Exception("example_output not implemented")

    def training_data(self) -> typing.Generator[typing.Tuple[np.array, np.array], None, None]:
        raise Exception("training_data not implemented")

    def train(self, model: Model):
        """Trains a model."""
        logging.info(f"Running model training: {self.identifier}")
        for i in range(model.epochs):
            for data, target in self.training_data():
                model.train(data, target)
            logging.info(f"Epoch {i} {self.evaluate(model)}")

    def step(self, vector: np.array, model: Model) -> float:
        """Step forward with an action space."""
        model.mutate(vector, self.example_data(), self.example_output())
        self.train(model)
        return self.evaluate(model)

    def mine(self, benchmark: float, current_sota_model: Model) -> typing.Tuple[str, float]:
        """Mine a benchmark for a better model."""
        logging.info(f"Beginning to mine: {self.identifier}")
        env = gym.make(
            ENVIRONMENT_ID,
            model = current_sota_model,
            evaluate = lambda vector: self.step(vector, current_sota_model),
            current_sota = benchmark)
        check_env(env)
        env.reset()
        model = PPO("MlpPolicy", env, verbose = 1)
        model.learn(sys.maxsize)
        model.save("model-pp0")
        env.reset()
        new_benchmark = self.evaluate(current_sota_model)
        if new_benchmark <= benchmark:
            raise Exception(f"Could not find better solution for {self.identifier}")
        logging.info(f"Benchmark after mining: {new_benchmark}")
        return current_sota_model.model_path, new_benchmark
