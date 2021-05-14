"""The model class."""
import numpy as np


class Model:
    """The model base class."""
    def __init__(self, model_path: str):
        self.model_path = model_path

    def infer(self, _: np.array) -> np.array:
        raise Exception("infer not implemented")
