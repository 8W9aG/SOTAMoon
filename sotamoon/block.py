"""The block class."""
from hashlib import sha256
import json

class Block:
    """A class that represents a transaction block."""
    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0):
        self.index = index
        self.transactions = [x.to_dict() for x in transactions]
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce

    def compute_hash(self):
        """Computes the hash of the JSON block representation."""
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()
