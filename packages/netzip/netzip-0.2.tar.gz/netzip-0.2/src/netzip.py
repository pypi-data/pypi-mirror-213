"""ZIP file reader optimized for network access.

See https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT
for the ZIP file format specification.
"""

import collections.abc
import io
import itertools
import struct
import zlib
from dataclasses import dataclass
from typing import Any, ClassVar, Dict, Iterable, Tuple

_MULTI_DISK_ERROR = ValueError("multi-disk ZIP archives are not supported")
_ENCRYPTED_ERROR = ValueError("encrypted ZIP archives are not supported")
_COMPRESSED_ERROR = ValueError("compressed ZIP archives are not supported")


def _validate_signature(name: str, *, want: bytes, got: bytes) -> None:
    """Validate a ZIP file signature."""
    if want != got:
        raise ValueError(f"invalid {name} signature: want {want}, got {got}")


def _fullread(buf, size: int) -> bytes:
    """Read exactly `size` bytes from `buf`, or raise EOFError."""
    data = buf.read(size)
    if len(data) != size:
        raise EOFError(f"requested {size} bytes, got {len(data)}")
    return data


def _unpackbuf(format: str, buf) -> Tuple:
    """Unpack a struct from buffer.

    Read the required number of bytes from `buf` and unpack them according to `format`.
    """
    return struct.unpack(format, _fullread(buf, struct.calcsize(format)))


# region File format data structures


# The following data structures are defined in the ZIP file format specification.

# Some fields are omitted because they are not used by this implementation, and parsing
# them would add extra I/O, which is undesirable for network access.

# Each data structure has a `read` classmethod that reads the structure from a buffer.
# The `validate` method checks that the structure is valid and can be used by this
# implementation.

# Fields in all data structures have default values because they cannot be created
# in a single step: almost all structures contain some variable-length fields.


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
        inst = cls(*_unpackbuf(cls.STRUCT_FORMAT, buf))
        inst.comment = _fullread(buf, inst.comment_size)
        inst.validate()
        return inst

    def validate(self) -> None:
        _validate_signature(
            "end of central directory record", want=self.SIGNATURE, got=self.signature
        )
        if (
            self.this_disk_number != 0
            or self.start_disk_number != 0
            or self.this_record_count != self.total_record_count
        ):
            raise _MULTI_DISK_ERROR

    def is_zip64(self) -> bool:
        return (
            self.this_disk_number == 0xFFFF
            or self.start_disk_number == 0xFFFF
            or self.this_record_count == 0xFFFF
            or self.total_record_count == 0xFFFF
            or self.central_directory_size == 0xFFFFFFFF
            or self.central_directory_offset == 0xFFFFFFFF
        )


@dataclass
class _Zip64EocdRecord:
    """End of central directory record for ZIP64 archives."""

    signature: bytes = b""
    size: int = 0
    version_created: int = 0
    version_needed: int = 0
    this_disk_number: int = 0
    start_disk_number: int = 0
    this_record_count: int = 0
    total_record_count: int = 0
    central_directory_size: int = 0
    central_directory_offset: int = 0

    SIGNATURE: ClassVar[bytes] = b"PK\x06\x06"
    STRUCT_FORMAT: ClassVar[str] = "<4sQ2H2L4Q"
    SIZE: ClassVar[int] = struct.calcsize(STRUCT_FORMAT)

    @classmethod
    def read(cls, buf) -> "_Zip64EocdRecord":
        inst = cls(*_unpackbuf(cls.STRUCT_FORMAT, buf))
        inst.validate()
        return inst

    def validate(self) -> None:
        _validate_signature(
            "ZIP64 end of central directory record",
            want=self.SIGNATURE,
            got=self.signature,
        )
        if (
            self.this_disk_number != 0
            or self.start_disk_number != 0
            or self.this_record_count != self.total_record_count
        ):
            raise _MULTI_DISK_ERROR


@dataclass
class _Zip64EocdLocator:
    """Location of the ZIP64 end of central directory."""

    signature: bytes = b""
    eocd_disk_number: int = 0
    eocd_offset: int = 0
    total_disk_count: int = 0

    SIGNATURE: ClassVar[bytes] = b"PK\x06\x07"
    STRUCT_FORMAT: ClassVar[str] = "<4sLQL"
    SIZE: ClassVar[int] = struct.calcsize(STRUCT_FORMAT)

    @classmethod
    def read(cls, buf) -> "_Zip64EocdLocator":
        inst = cls(*_unpackbuf(cls.STRUCT_FORMAT, buf))
        inst.validate()
        return inst

    def validate(self) -> None:
        _validate_signature(
            "ZIP64 end of central directory locator",
            want=self.SIGNATURE,
            got=self.signature,
        )
        if self.eocd_disk_number != 0 or self.total_disk_count != 1:
            raise _MULTI_DISK_ERROR


def _read_zip64_extinfo(block) -> Dict[str, Any]:
    """Read ZIP64 extended information extra field from the 'extra' field block.

    Return dict with values found in the extra block, and keys corresponding
    to field names in _CdFileHeader and _LocalFileHeader.
    """
    buf = io.BytesIO(block)

    while buf.tell() < len(block):
        header, size = _unpackbuf("<2H", buf)
        if header != 0x0001:
            buf.seek(size, io.SEEK_CUR)
            continue

        formats = dict(
            uncompressed_size="<Q",
            compressed_size="<Q",
            local_header_offset="<Q",
            disk_number="<L",
        )
        if size not in itertools.accumulate(map(struct.calcsize, formats.values())):
            raise ValueError("invalid ZIP64 extended information extra field")

        fields = {}
        ext_block = _fullread(buf, size)
        ext_buf = io.BytesIO(ext_block)
        for name, fmt in formats.items():
            if ext_buf.tell() >= len(ext_block):
                break
            fields[name] = _unpackbuf(fmt, ext_buf)[0]
        return fields

    return {}


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
        extra_block = _fullread(buf, inst.extra_size)
        inst.comment = _fullread(buf, inst.comment_size)
        if inst.is_zip64():
            for name, value in _read_zip64_extinfo(extra_block).items():
                setattr(inst, name, value)
        inst.validate()
        return inst

    def validate(self) -> None:
        _validate_signature(
            "central directory file header", want=self.SIGNATURE, got=self.signature
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

    def is_zip64(self) -> bool:
        return (
            self.compressed_size == 0xFFFFFFFF
            or self.uncompressed_size == 0xFFFFFFFF
            or self.disk_number == 0xFFFF
            or self.local_header_offset == 0xFFFFFFFF
        )


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
        extra_block = _fullread(buf, inst.extra_size)
        if inst.is_zip64():
            for name, value in _read_zip64_extinfo(extra_block).items():
                setattr(inst, name, value)
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

    def is_zip64(self) -> bool:
        return (
            self.compressed_size == 0xFFFFFFFF or self.uncompressed_size == 0xFFFFFFFF
        )


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
        if self.size != header.uncompressed_size or self.crc32 != header.crc32:
            raise ValueError(
                "local file header and central directory file header contain different metadata"
            )


def _read_metadata(source: io.BufferedIOBase) -> Dict[bytes, _FileInfo]:
    """Parse ZIP metadata from source.

    Returns:
        Mapping of file names to file info records.
    """
    source.seek(0, io.SEEK_END)
    size = source.tell()

    source.seek(max(0, size - _EocdRecord.MAX_SIZE - _Zip64EocdLocator.SIZE))
    eocd_block = source.read()

    eocd_start = eocd_block.rfind(_EocdRecord.SIGNATURE)
    if eocd_start < 0:
        raise ValueError("end of central directory record not found")
    eocd = _EocdRecord.read(io.BytesIO(eocd_block[eocd_start:]))

    if eocd.is_zip64():
        loc_block = eocd_block[max(0, eocd_start - _Zip64EocdLocator.SIZE) : eocd_start]
        loc = _Zip64EocdLocator.read(io.BytesIO(loc_block))

        source.seek(loc.eocd_offset)
        eocd64_block = source.read(_Zip64EocdRecord.SIZE)
        eocd = _Zip64EocdRecord.read(io.BytesIO(eocd64_block))

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
        data = _fullread(buf, info.size)
        if info.crc32 != zlib.crc32(data):
            raise ValueError("CRC32 mismatch")
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
