"""The model class."""
import enum
import logging

import numpy as np


PARAMETER_SPACE = 10
MAX_LAYERS = 1000
MAX_EPOCHS = 100
OPTIMISER_OFFSET = 2


class ModelType(enum.IntEnum):
    """The type of model that is represented."""
    Torch = 0


def model_type_to_string(model_type: ModelType) -> str:
    """Find a string representation of the model type."""
    return "Torch"


class Model:
    """The model base class."""
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.epochs = 10

    def infer(self, _: np.array) -> np.array:
        raise Exception("infer not implemented")

    def vectorise(self) -> np.array:
        """Produce a vector representing the model."""
        vector = np.zeros(PARAMETER_SPACE)
        vector[0] = float(ModelType.Torch)
        vector[1] = float(self.epochs) / float(MAX_EPOCHS)
        return vector

    def mutate(self, vector: np.array, example_data: np.array, example_output: np.array):
        # Ignore type vector for now since we only have 1 type
        self.epochs = int(vector[1] * MAX_EPOCHS)
        logging.info(f"Mutating model type={model_type_to_string(int(vector[0]))} epochs={self.epochs}")

    def train(self, data: np.array, target: np.array):
        raise Exception("train not implemented")
