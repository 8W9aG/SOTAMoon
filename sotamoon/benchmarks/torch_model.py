"""The torch model class."""
import torch
import numpy as np

from .model import Model


class TorchModel(Model):
    """The model class for torch models."""
    def __init__(self, model_path: str):
        super().__init__(model_path)
        self.model = torch.jit.load(model_path)

    def infer(self, x: np.array) -> np.array:
        """Run inference on a piece of data."""
        with torch.no_grad():
            return self.model(x).numpy()
