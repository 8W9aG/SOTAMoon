"""The model class."""
from .constraints import MAX_STRING_LENGTH


MODEL_HASH_KEY = "model_hash"
MAGNET_LINK_KEY = "magnet_link"


# TODO: Can we sign the model from a specific miner?
class Model:
    """The class representing a SOTA model."""
    def __init__(self, model_hash: str, magnet_link: str):
        self.model_hash = model_hash
        self.magnet_link = magnet_link

    def __iter__(self):
        yield MODEL_HASH_KEY, self.model_hash
        yield MAGNET_LINK_KEY, self.magnet_link
