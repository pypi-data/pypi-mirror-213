"""Encoder/decoder for writing and reading BytesIO objects."""
from io import BytesIO
from pathlib import Path


def bytesio_encoder(data: BytesIO) -> bytes:
    """Convert `BytesIO` to `bytes` for writing to a file."""
    if not isinstance(data, BytesIO):
        raise ValueError(f"Input type {type(data)} is not BytesIO")
    return data.read()


def bytesio_decoder(path: Path) -> BytesIO:
    """Read the contents of a file as a `BytesIO` object."""
    with open(path, "rb") as f:
        file_obj = BytesIO(f.read())

    return file_obj
