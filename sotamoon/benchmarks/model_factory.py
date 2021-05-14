"""The model factory class."""
import pathlib

from .model import Model
from .torch_model import TorchModel


MODEL_EXTENSIONS = {
    ".pt": TorchModel,
    ".pth": TorchModel
}


def create_model(model_path: str) -> Model:
    """Creates a model from the path."""
    return MODEL_EXTENSIONS[pathlib.Path(model_path).suffix](model_path)
