"""ZIP file reader optimized for network access.

See https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT
for the ZIP file format specification.
"""

import collections.abc
import io
import struct
import zlib
from dataclasses import dataclass
from typing import ClassVar, Dict, Iterable, Tuple

_MULTI_DISK_ERROR = ValueError("multi-disk ZIP archives are not supported")
_ENCRYPTED_ERROR = ValueError("encrypted ZIP archives are not supported")
_COMPRESSED_ERROR = ValueError("compressed ZIP archives are not supported")
_ZIP64_ERROR = NotImplementedError("ZIP64 archives are not implemented yet")


def _validate_signature(name: str, *, want: bytes, got: bytes) -> None:
    """Validate a ZIP file signature."""
    if want != got:
        raise ValueError(f"invalid {name} signature: want {want}, got {got}")


def _fullread(buf, size: int = -1) -> bytes:
    """Read exactly `size` bytes from `buf`, or raise EOFError.

    If size is negative, read until EOF.
    """
    data = buf.read(size)
    if size >= 0 and len(data) != size:
        raise EOFError(f"requested {size} bytes, got {len(data)}")
    return data


def _unpackbuf(format, buf) -> Tuple:
    """Unpack a struct from buffer.

    Read the required number of bytes from `buf` and unpack them according to `format`.
    """
    return struct.unpack(format, _fullread(buf, struct.calcsize(format)))


# region File format data structures


## Fields in the following data structures are separated into two groups:
## fixed-size and variable-size ones.


@dataclass
class _EocdRecord:
    """End of central directory record."""

    signature: bytes = b""
    this_disk_number: int = 0
    start_disk_number: int = 0
    this_record_count: int = 0
    total_record_count: int = 0
    central_directory_size: int = 0
    central_directory_offset: int = 0
    comment_size: int = 0

    comment: bytes = b""

    SIGNATURE: ClassVar[bytes] = b"PK\x05\x06"
    STRUCT_FORMAT: ClassVar[str] = "<4s4H2LH"
    MAX_SIZE: ClassVar[int] = struct.calcsize(STRUCT_FORMAT) + 0xFFFF

    @classmethod
    def read(cls, buf) -> "_EocdRecord":
        """Read an end of central directory record from `buf`."""
        inst = cls(*_unpackbuf(cls.STRUCT_FORMAT, buf))
        inst.comment = _fullread(buf, inst.comment_size)
        inst.validate()
        return inst

    def validate(self) -> None:
        _validate_signature(
            "end of central directory", want=self.SIGNATURE, got=self.signature
        )
        if (
            self.this_disk_number != 0
            or self.start_disk_number != 0
            or self.this_record_count != self.total_record_count
        ):
            raise _MULTI_DISK_ERROR
        if (
            self.total_record_count == 0xFFFF
            or self.central_directory_size == 0xFFFFFFFF
            or self.central_directory_offset == 0xFFFFFFFF
        ):
            raise _ZIP64_ERROR


@dataclass
class _CdFileHeader:
    """File metadata that is stored in the central directory."""

    signature: bytes = b""
    version_created: int = 0
    version_needed: int = 0
    flags: int = 0
    compression_method: int = 0
    last_mod_time: int = 0
    last_mod_date: int = 0
    crc32: int = 0
    compressed_size: int = 0
    uncompressed_size: int = 0
    filename_size: int = 0
    extra_size: int = 0
    comment_size: int = 0
    disk_number: int = 0
    internal_file_attributes: int = 0
    external_file_attributes: int = 0
    local_header_offset: int = 0

    filename: bytes = b""
    comment: bytes = b""

    SIGNATURE: ClassVar[bytes] = b"PK\x01\x02"
    STRUCT_FORMAT: ClassVar[str] = "<4s6H3L5H2L"

    @classmethod
    def read(cls, buf) -> "_CdFileHeader":
        inst = cls(*_unpackbuf(cls.STRUCT_FORMAT, buf))
        inst.filename = _fullread(buf, inst.filename_size)
        _fullread(buf, inst.extra_size)
        inst.comment = _fullread(buf, inst.comment_size)
        inst.validate()
        return inst

    def validate(self) -> None:
        _validate_signature(
            "central directory ", want=self.SIGNATURE, got=self.signature
        )
        if self.flags & 0x0001:
            raise _ENCRYPTED_ERROR
        if (
            self.compression_method != 0
            or self.compressed_size != self.uncompressed_size
        ):
            raise _COMPRESSED_ERROR
        if self.disk_number != 0:
            raise _MULTI_DISK_ERROR
        if (
            self.uncompressed_size == 0xFFFFFFFF
            or self.local_header_offset == 0xFFFFFFFF
        ):
            raise _ZIP64_ERROR


@dataclass
class _LocalFileHeader:
    """File metadata that precedes the actual file data."""

    signature: bytes = b""
    version_needed: int = 0
    flags: int = 0
    compression_method: int = 0
    last_mod_time: int = 0
    last_mod_date: int = 0
    crc32: int = 0
    compressed_size: int = 0
    uncompressed_size: int = 0
    filename_size: int = 0
    extra_size: int = 0

    filename: bytes = b""

    SIGNATURE: ClassVar[bytes] = b"PK\x03\x04"
    STRUCT_FORMAT: ClassVar[str] = "<4s5H3L2H"
    MAX_SIZE: ClassVar[int] = struct.calcsize(STRUCT_FORMAT) + 2 * 0xFFFF

    @classmethod
    def read(cls, buf) -> "_LocalFileHeader":
        inst = cls(*_unpackbuf(cls.STRUCT_FORMAT, buf))
        inst.filename = _fullread(buf, inst.filename_size)
        _fullread(buf, inst.extra_size)
        inst.validate()
        return inst

    def validate(self) -> None:
        _validate_signature(
            "local file header", want=self.SIGNATURE, got=self.signature
        )
        if self.flags & 0x0001:
            raise _ENCRYPTED_ERROR
        if (
            self.compression_method != 0
            or self.compressed_size != self.uncompressed_size
        ):
            raise _COMPRESSED_ERROR
        if self.uncompressed_size == 0xFFFFFFFF:
            raise _ZIP64_ERROR


# endregion


@dataclass
class _FileInfo:
    """Minimal necessary file metadata required for `ZipReader`."""

    offset: int
    size: int
    crc32: int

    @property
    def max_block_size(self) -> int:
        """Return the maximum possible size of local file header + payload block."""
        return _LocalFileHeader.MAX_SIZE + self.size

    @classmethod
    def readmany(cls, buf, count: int) -> Dict[bytes, "_FileInfo"]:
        """Read multiple file info records from a buffer.

        Buffer must contain exactly `count` well-formed records.
        """
        d = {}
        for _ in range(count):
            header = _CdFileHeader.read(buf)
            if header.filename in d:
                raise ValueError(f"duplicate filename {header.filename}")
            d[header.filename] = cls(
                offset=header.local_header_offset,
                size=header.uncompressed_size,
                crc32=header.crc32,
            )
        if buf.read(1):
            raise ValueError("central directory contains more data than expected")
        return d

    def validate_header(self, header: _LocalFileHeader) -> None:
        """Validate against local file header."""
        if self.size != header.uncompressed_size:
            raise ValueError("size mismatch")
        if self.crc32 != header.crc32:
            raise ValueError("CRC32 mismatch")

    def validate_payload(self, payload: bytes) -> None:
        """Validate against file payload."""
        if self.size != len(payload):
            raise ValueError("size mismatch")
        if self.crc32 != zlib.crc32(payload):
            raise ValueError("CRC32 mismatch")


def _read_metadata(source: io.BufferedIOBase) -> Dict[bytes, _FileInfo]:
    """Parse ZIP metadata from source.

    Returns:
        Mapping of file names to file info records.
    """
    source.seek(-_EocdRecord.MAX_SIZE, io.SEEK_END)
    eocd_block = source.read()

    eocd_start = eocd_block.rfind(_EocdRecord.SIGNATURE)
    if eocd_start < 0:
        raise ValueError("end of central directory record not found")
    eocd = _EocdRecord.read(io.BytesIO(eocd_block[eocd_start:]))

    source.seek(eocd.central_directory_offset)
    cd_block = source.read(eocd.central_directory_size)

    return _FileInfo.readmany(io.BytesIO(cd_block), eocd.total_record_count)


class ZipReader(collections.abc.Mapping):
    """ZIP archive reader that minimizes the number of I/O calls."""

    def __init__(self, source) -> None:
        """Initialize the reader by reading and parsing ZIP metadata from source.

        The source should be opened in binary mode and support random access reads.
        Also, source must not be closed while this object is in use.
        """
        self._source = source
        self._files = _read_metadata(source)

    def __getitem__(self, name: bytes) -> bytes:
        """Return contents of a file with the given name."""
        info = self._files[name]

        self._source.seek(info.offset)
        buf = io.BytesIO(self._source.read(info.max_block_size))

        info.validate_header(_LocalFileHeader.read(buf))
        data = buf.read(info.size)
        info.validate_payload(data)
        return data

    def __iter__(self) -> Iterable[bytes]:
        """Return file names in this archive, in unspecified order."""
        return iter(self._files)

    def __len__(self) -> int:
        """Return the number of files in this archive."""
        return len(self._files)

    def size(self, name: bytes) -> int:
        """Return the size of a file with the given name."""
        return self._files[name].size
