import io
import zipfile
from typing import Mapping

import pytest

from netzip import ZipReader


def dict_to_zipbuf(d: Mapping[bytes, bytes]) -> io.BytesIO:
    """Create a ZIP archive in memory from a filename-content mapping."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, mode="w") as zf:
        for name, data in d.items():
            zf.writestr(name.decode("ascii"), data)
    return buf


@pytest.fixture
def zip_reader():
    d = {b"spam.txt": b"SPAM!", b"eggs/ham.bin": b"\xDE\xAD\xBE\xEF"}
    return ZipReader(dict_to_zipbuf(d))


def test_getitem(zip_reader):
    assert zip_reader[b"spam.txt"] == b"SPAM!"
    assert zip_reader[b"eggs/ham.bin"] == b"\xDE\xAD\xBE\xEF"


def test_iter(zip_reader):
    assert set(zip_reader) == {b"spam.txt", b"eggs/ham.bin"}


def test_len(zip_reader):
    assert len(zip_reader) == 2


def test_size(zip_reader):
    assert zip_reader.size(b"spam.txt") == 5
    assert zip_reader.size(b"eggs/ham.bin") == 4
