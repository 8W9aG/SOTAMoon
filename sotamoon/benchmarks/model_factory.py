"""The model factory class."""
import pathlib
import typing

from .model import Model
from .torch.torch_model import TorchModel


MODEL_EXTENSIONS = {
    ".pt": TorchModel,
    ".pth": TorchModel
}


def create_model(model_path: str) -> typing.Optional[Model]:
    """Creates a model from the path."""
    suffix = pathlib.Path(model_path).suffix
    if MODEL_EXTENSIONS[suffix] == TorchModel:
        return MODEL_EXTENSIONS[suffix](model_path)
    return None
