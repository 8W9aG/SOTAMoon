"""The wallet class."""
import binascii
import typing

from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
from Crypto.Hash.SHA1 import SHA1Hash


IDENTITY_KEY = "identity"


def key_to_str(key: RSA.RsaKey) -> str:
   """Convert a key to a string."""
   return binascii.hexlify(key.exportKey(format='DER')).decode('ascii')


class Wallet:
   def __init__(self, public_key: str):
      self._public_key = RSA.importKey(binascii.unhexlify(public_key))
      self.verifier = PKCS1_v1_5.new(self._public_key)
      self.identity = key_to_str(self._public_key)

   def verify(self, message: str, signature: str) -> bool:
      """Verify a message with its signature."""
      return self.verifier.verify(self._process_message(message), binascii.unhexlify(signature))

   def sign(self, _: str) -> str:
        """Sign a message with the private key."""
        raise Exception("Cannot sign with an unopened wallet")

   def _process_message(self, message: str) -> SHA1Hash:
      """Process a message deterministically."""
      return SHA.new(message.encode('utf8'))

   def __iter__(self):
      yield IDENTITY_KEY, self.identity

   def __eq__(self, other):
      return self.identity == other.identity

def wallet_from_dict(wallet_dict: typing.Dict[str, typing.Any]) -> Wallet:
   """Create a wallet from a dictionary."""
   return Wallet(wallet_dict[IDENTITY_KEY])
