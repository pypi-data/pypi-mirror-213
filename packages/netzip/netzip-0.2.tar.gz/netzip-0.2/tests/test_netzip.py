import io
import zipfile

import pytest

from netzip import ZipReader


class TestZip:
    @pytest.fixture
    def reader(self):
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, mode="w") as zf:
            zf.writestr("spam.txt", b"SPAM!")
            zf.writestr("eggs/ham.bin", b"\xDE\xAD\xBE\xEF")
        return ZipReader(buf)

    def test_getitem(self, reader):
        assert reader[b"spam.txt"] == b"SPAM!"
        assert reader[b"eggs/ham.bin"] == b"\xDE\xAD\xBE\xEF"

    def test_iter(self, reader):
        assert set(reader) == {b"spam.txt", b"eggs/ham.bin"}

    def test_len(self, reader):
        assert len(reader) == 2

    def test_size(self, reader):
        assert reader.size(b"spam.txt") == 5
        assert reader.size(b"eggs/ham.bin") == 4


class TestZip64:
    # Make this fixture class-scoped because it's expensive to create.
    @pytest.fixture(scope="class")
    def reader(self):
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, mode="w") as zf:
            for i in range(0xFFFF + 1):
                zf.writestr(f"spam-{i:04X}.txt", b"SPAM!")
        return ZipReader(buf)

    def test_getitem(self, reader):
        assert reader[b"spam-0000.txt"] == b"SPAM!"
        assert reader[b"spam-FFFF.txt"] == b"SPAM!"

    def test_iter(self, reader):
        assert set(reader) == {f"spam-{i:04X}.txt".encode() for i in range(0xFFFF + 1)}

    def test_len(self, reader):
        assert len(reader) == 0xFFFF + 1

    def test_size(self, reader):
        assert reader.size(b"spam-0000.txt") == 5
        assert reader.size(b"spam-FFFF.txt") == 5
