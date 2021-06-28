"""The model environment class."""
import typing

import gym
from gym import spaces
import numpy as np
from torchinfo import summary

from .model import Model, PARAMETER_SPACE


ENVIRONMENT_ID = "ModelEnv-v1"


class ModelEnv(gym.Env):
    """The environment representing a model."""

    def __init__(
        self,
        model: typing.Optional[Model] = None,
        evaluate: typing.Optional[typing.Callable[[np.array], float]] = None,
        current_sota: float = 0.0):
        super(ModelEnv, self).__init__()
        self.model = model
        self.evaluate = evaluate
        self.current_sota = current_sota
        self.action_space = spaces.Box(
            low=np.zeros(PARAMETER_SPACE),
            high=np.ones(PARAMETER_SPACE),
        )
        self.observation_space = spaces.Box(
            low=np.zeros(PARAMETER_SPACE),
            high=np.ones(PARAMETER_SPACE),
        )
        self.reset()

    def reset(self):
        """Reset the state of the environment."""
        self._step = 0
        self.state = self.model.vectorise()
        return self.state

    def step(self, action: np.array):
        """Take an action in the environment and advance to the next state."""
        self._step += 1
        reward = self.evaluate(action)
        self.state = self.model.vectorise()
        return self.state, reward, reward > self.current_sota, {}

    def render(self, mode = "human", close = False):
        """Render the current state."""
        summary(self.model)
