"""The opened wallet class."""
import binascii

import Crypto
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA

from .wallet import Wallet, key_to_str


class OpenedWallet(Wallet):
    def __init__(self, public_key: str, private_key: str):
        super().__init__(public_key)
        self._private_key = RSA.importKey(binascii.unhexlify(private_key))
        self._signer = PKCS1_v1_5.new(self._private_key)

    def sign(self, message: str) -> str:
        """Sign a message with the private key."""
        return binascii.hexlify(self._signer.sign(self._process_message(message))).decode('ascii')


def generate_wallet() -> OpenedWallet:
    """Generate a new wallet."""
    random = Crypto.Random.new().read
    private_key = RSA.generate(1024, random)
    return OpenedWallet(key_to_str(private_key.publickey()), key_to_str(private_key))
