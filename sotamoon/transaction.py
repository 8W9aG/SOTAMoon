"""The transaction class."""
import collections
import binascii
import time

from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA


GENESIS_SENDER = "GENESIS"


class Transaction:
    def __init__(self, sender, recipient, value):
        self.sender = sender
        self.recipient = recipient
        self.value = value
        self.time = time.time()

    def to_dict(self):
        if self.sender == GENESIS_SENDER:
            identity = GENESIS_SENDER
        else:
            identity = self.sender.identity

        return collections.OrderedDict({
            'sender': identity,
            'recipient': self.recipient.identity,
            'value': self.value,
            'time' : self.time
        })

    def sign_transaction(self):
        if self.sender == GENESIS_SENDER:
            return ""
        private_key = self.sender._private_key
        signer = PKCS1_v1_5.new(private_key)
        h = SHA.new(str(self.to_dict()).encode('utf8'))
        return binascii.hexlify(signer.sign(h)).decode('ascii')
