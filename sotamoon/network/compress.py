"""Methods to compress and decompress data."""
import typing
import json

import snappy


def compress(data: typing.Dict) -> bytes:
    """Compress a request."""
    return snappy.compress(json.dumps(data).encode())

def decompress(data: bytes) -> typing.Dict:
    """Decompress a request."""
    decompressed_message = snappy.decompress(data)
    return json.loads(decompressed_message)
