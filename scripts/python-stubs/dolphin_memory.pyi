"""Module for interacting with the emulated machine's memory."""


def read_u8(addr: int, /) -> int:
    """
    Reads 1 byte as an unsigned integer.

    :param addr: memory address to read from
    :return: value as integer
    """


def read_u16(addr: int, /) -> int:
    """
    Reads 2 bytes as an unsigned integer.

    :param addr: memory address to read from
    :return: value as integer
    """


def read_u32(addr: int, /) -> int:
    """
    Reads 4 bytes as an unsigned integer.

    :param addr: memory address to read from
    :return: value as integer
    """


def read_u64(addr: int, /) -> int:
    """
    Reads 8 bytes as an unsigned integer.

    :param addr: memory address to read from
    :return: value as integer
    """


def read_s8(addr: int, /) -> int:
    """
    Reads 1 byte as a signed integer.

    :param addr: memory address to read from
    :return: value as integer
    """


def read_s16(addr: int, /) -> int:
    """
    Reads 2 bytes as a signed integer.

    :param addr: memory address to read from
    :return: value as integer
    """


def read_s32(addr: int, /) -> int:
    """
    Reads 4 bytes as a signed integer.

    :param addr: memory address to read from
    :return: value as integer
    """


def read_s64(addr: int, /) -> int:
    """
    Reads 8 bytes as a signed integer.

    :param addr: memory address to read from
    :return: value as integer
    """


def read_f32(addr: int, /) -> float:
    """
    Reads 4 bytes as a floating point number.

    :param addr: memory address to read from
    :return: value as floating point number
    """


def read_f64(addr: int, /) -> float:
    """
    Reads 8 bytes as a floating point number.

    :param addr: memory address to read from
    :return: value as floating point number
    """


def read_bytes(addr: int, size: int, /) -> bytearray:
    """
    Reads size bytes and outputs a bytearray of length size.
    
    :param addr: memory address to start reading from
    :param size: number of bytes to read
    :return: bytearray containing the read bytes
    """


def invalidate_icache(addr: int, size: int, /) -> None:
    """
    Invalidates JIT cached code between the address and address + size, \
        forcing the JIT to refetch instructions instead of executing from its cache.

    :param addr: memory address to start invalidation at
    :param size: size of the cache as integer
    """


def write_u8(addr: int, value: int, /) -> None:
    """
    Writes an unsigned integer to 1 byte.
    Overflowing values are truncated.

    :param addr: memory address to read from
    :param value: value as integer
    """


def write_u16(addr: int, value: int, /) -> None:
    """
    Writes an unsigned integer to 2 bytes.
    Overflowing values are truncated.

    :param addr: memory address to read from
    :param value: value as integer
    """


def write_u32(addr: int, value: int, /) -> None:
    """
    Writes an unsigned integer to 4 bytes.
    Overflowing values are truncated.

    :param addr: memory address to read from
    :param value: value as integer
    """


def write_u64(addr: int, value: int, /) -> None:
    """
    Writes an unsigned integer to 8 bytes.
    Overflowing values are truncated.

    :param addr: memory address to read from
    :param value: value as integer
    """


def write_s8(addr: int, value: int, /) -> None:
    """
    Writes a signed integer to 1 byte.
    Overflowing values are truncated.

    :param addr: memory address to read from
    :param value: value as integer
    """


def write_s16(addr: int, value: int, /) -> None:
    """
    Writes a signed integer to 2 bytes.
    Overflowing values are truncated.

    :param addr: memory address to read from
    :param value: value as integer
    """


def write_s32(addr: int, value: int, /) -> None:
    """
    Writes a signed integer to 4 bytes.
    Overflowing values are truncated.

    :param addr: memory address to read from
    :param value: value as integer
    """


def write_s64(addr: int, value: int, /) -> None:
    """
    Writes a signed integer to 8 bytes.
    Overflowing values are truncated.

    :param addr: memory address to read from
    :param value: value as integer
    """


def write_f32(addr: int, value: float, /) -> None:
    """
    Writes a floating point number to 4 bytes.
    Overflowing values are truncated.

    :param addr: memory address to read from
    :param value: value as floating point number
    """


def write_f64(addr: int, value: float, /) -> None:
    """
    Writes a floating point number to 8 bytes.
    Overflowing values are truncated.

    :param addr: memory address to read from
    :param value: value as floating point number
    """
    
    
def write_bytes(addr: int, bytes: bytearray, /) -> None:
    """
    Writes each byte from the provided bytearray,
    starting from addr.
    
    :param addr: memory address to start writing to
    :param bytes: bytearray of bytes to write
    """

def is_memory_accessible() -> bool:
	"""
	Return a boolean value corresponding to
	the state of the memory.
	True means the memory is accessible,
	False means the memory isn't accessible.
	Trying to read/write the memory while it's not accessible
	may result in Dolphin crashing
	"""