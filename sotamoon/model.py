"""The model class."""
import typing


MODEL_HASH_KEY = "model_hash"
MAGNET_LINK_KEY = "magnet_link"


class Model:
    """The class representing a SOTA model."""
    def __init__(self, model_hash: str, magnet_link: str):
        self.model_hash = model_hash
        self.magnet_link = magnet_link

    def __iter__(self):
        yield MODEL_HASH_KEY, self.model_hash
        yield MAGNET_LINK_KEY, self.magnet_link


def model_from_dict(model_dict: typing.Dict[str, typing.Any]) -> Model:
    """Deserialise a model from a dictionary."""
    return Model(
        model_dict[MODEL_HASH_KEY],
        model_dict[MAGNET_LINK_KEY],
    )
