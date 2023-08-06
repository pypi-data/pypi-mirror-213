# Copyright 2016-present MongoDB, Inc.
# Copyright 2023 @masaccio
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Forked from PyMongo at version 4.3.3

"""Tools for working with the BSON decimal128 type.
"""

import decimal
import struct

from struct import pack, unpack
from typing import Any, Sequence, Tuple, Type, Union

_EXPONENT_MASK = 3 << 61
_EXPONENT_BIAS = 6176
_EXPONENT_MAX = 6144
_EXPONENT_MIN = -6143
_MAX_DIGITS = 34

_INF = 0x7800000000000000
_NAN = 0x7C00000000000000
_SNAN = 0x7E00000000000000
_SIGN = 0x8000000000000000

_NINF = (_INF + _SIGN, 0)
_PINF = (_INF, 0)
_NNAN = (_NAN + _SIGN, 0)
_PNAN = (_NAN, 0)
_NSNAN = (_SNAN + _SIGN, 0)
_PSNAN = (_SNAN, 0)

_DECIMAL128_CTX_OPTIONS = {
    "prec": _MAX_DIGITS,
    "rounding": decimal.ROUND_HALF_EVEN,
    "Emin": _EXPONENT_MIN,
    "Emax": _EXPONENT_MAX,
    "capitals": 1,
    "flags": [],
    "traps": [],
    # "traps": [decimal.InvalidOperation, decimal.Overflow, decimal.Inexact],
    "clamp": 0,
}

_DECIMAL128_CTX = decimal.Context(**_DECIMAL128_CTX_OPTIONS.copy())
_VALUE_OPTIONS = Union[decimal.Decimal, int, float, str, Tuple[int, Sequence[int], int]]


def create_decimal128_context() -> decimal.Context:
    """Returns an instance of decimal.Context appropriate for
    working with IEEE-754 128-bit decimal floating point values.
    """
    opts = _DECIMAL128_CTX_OPTIONS.copy()
    opts["traps"] = []
    return decimal.Context(**opts)


def _decimal_to_128(value: _VALUE_OPTIONS) -> Tuple[int, int]:
    """Converts a decimal.Decimal to BID (high bits, low bits)."""
    with decimal.localcontext(_DECIMAL128_CTX) as ctx:
        if isinstance(value, str):
            value = value.replace("_", "")

        value = ctx.create_decimal(value)

    if value.is_infinite():
        return _NINF if value.is_signed() else _PINF

    sign, digits, exponent = value.as_tuple()

    if value.is_nan():
        if digits:
            raise ValueError("NaN with debug payload is not supported")
        if value.is_snan():
            return _NSNAN if value.is_signed() else _PSNAN
        return _NNAN if value.is_signed() else _PNAN

    significand = int("".join([str(digit) for digit in digits]))
    bit_length = significand.bit_length()

    high = 0
    low = 0
    for i in range(min(64, bit_length)):
        if significand & (1 << i):
            low |= 1 << i

    for i in range(64, bit_length):
        if significand & (1 << i):
            high |= 1 << (i - 64)

    biased_exponent = exponent + _EXPONENT_BIAS

    if high >> 49 == 1:
        high = high & 0x7FFFFFFFFFFF
        high |= _EXPONENT_MASK
        high |= (biased_exponent & 0x3FFF) << 47
    else:
        high |= biased_exponent << 49

    if sign:
        high |= _SIGN

    return high, low


class Decimal128:
    """Python Decimal128 type"""

    __slots__ = ("__high", "__low")

    def __init__(self, value: _VALUE_OPTIONS) -> None:
        if isinstance(value, (int, float, str, decimal.Decimal)):
            self.__high, self.__low = _decimal_to_128(value)
        elif isinstance(value, (list, tuple)):
            if len(value) != 2:
                raise ValueError(
                    "Invalid size for creation of Decimal128 "
                    "from list or tuple. Must have exactly 2 "
                    "elements."
                )
            self.__high, self.__low = value
        else:
            raise TypeError(f"Cannot convert {value!r} to Decimal128")

    def to_decimal(self) -> decimal.Decimal:
        """Returns an instance of decimal.Decimal for this Decimal128"""
        high = self.__high
        low = self.__low
        sign = 1 if (high & _SIGN) else 0

        if (high & _SNAN) == _SNAN:
            return decimal.Decimal((sign, (), "N"))
        elif (high & _NAN) == _NAN:
            return decimal.Decimal((sign, (), "n"))
        elif (high & _INF) == _INF:
            return decimal.Decimal((sign, (), "F"))

        if (high & _EXPONENT_MASK) == _EXPONENT_MASK:
            exponent = ((high & 0x1FFFE00000000000) >> 47) - _EXPONENT_BIAS
            return decimal.Decimal((sign, (0,), exponent))
        else:
            exponent = ((high & 0x7FFF800000000000) >> 49) - _EXPONENT_BIAS

        arr = bytearray(15)
        mask = 0x00000000000000FF
        for i in range(14, 6, -1):
            arr[i] = (low & mask) >> ((14 - i) << 3)
            mask = mask << 8

        mask = 0x00000000000000FF
        for i in range(6, 0, -1):
            arr[i] = (high & mask) >> ((6 - i) << 3)
            mask = mask << 8

        mask = 0x0001000000000000
        arr[0] = (high & mask) >> 48

        # cdecimal only accepts a tuple for digits.
        digits = tuple(int(digit) for digit in str(int.from_bytes(arr, "big")))

        with decimal.localcontext(_DECIMAL128_CTX) as ctx:
            return ctx.create_decimal((sign, digits, exponent))

    def to_float(self) -> float:
        """Returns an instance of `float` for this Decimal128."""
        return float(self.to_decimal())

    @classmethod
    def from_bid(cls: Type["Decimal128"], value: bytes) -> "Decimal128":
        """Create an instance of Decimal128 from a binary integer decimal (BID)"""
        if not isinstance(value, bytes):
            raise TypeError("value must be an instance of bytes")
        if len(value) != 16:
            raise ValueError("value must be exactly 16 bytes")
        return cls((unpack(">Q", value[:8])[0], unpack(">Q", value[8:])[0]))

    def bid(self) -> bytes:
        """The binary integer decimal (BID) encoding of this instance."""
        value = pack(">Q", self.__high) + pack(">Q", self.__low)
        return value

    def is_infinite(self) -> bool:
        """Return True if self is infinite; otherwise return False."""
        high = self.__high & ~_SIGN
        return high == _INF

    def is_nan(self) -> bool:
        """Return True if self is a NaN; otherwise return False."""
        high = self.__high & ~_SIGN
        return high == _SNAN or high == _NAN

    def is_signed(self) -> bool:
        """Return True if self is negative; otherwise return False."""
        return self.__high & _SIGN

    def __str__(self) -> str:
        dec = self.to_decimal()
        if dec.is_nan():
            # Required by the drivers spec to match MongoDB behavior.
            return "NaN"
        return str(dec)

    def __repr__(self):
        return f"Decimal128('{str(self)}')"

    def __setstate__(self, value: Tuple[int, int]) -> None:
        self.__high, self.__low = value

    def __getstate__(self) -> Tuple[int, int]:
        return self.__high, self.__low

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Decimal128):
            with decimal.localcontext(_DECIMAL128_CTX) as ctx:
                return self.to_decimal() == other.to_decimal()
        elif isinstance(other, float):
            with decimal.localcontext(_DECIMAL128_CTX) as ctx:
                return self.to_decimal()
        return NotImplemented  # pragma: no cover

    def __ne__(self, other: Any) -> bool:
        return not self == other

    def __abs__(self):
        # Faster than going through Decimal conversion
        self.__high &= ~_SIGN
        return self

    def __add__(self, other):
        with decimal.localcontext(_DECIMAL128_CTX) as ctx:
            if isinstance(other, Decimal128):
                return Decimal128(self.to_decimal() + other.to_decimal())
            else:
                return Decimal128(self.to_decimal() + decimal.Decimal(other))

    def __float__(self):
        with decimal.localcontext(_DECIMAL128_CTX) as ctx:
            return self.to_float()

    def __iadd__(self, other):
        with decimal.localcontext(_DECIMAL128_CTX) as ctx:
            if isinstance(other, Decimal128):
                self = Decimal128(self.to_decimal() + other.to_decimal())
            else:
                self = Decimal128(self.to_decimal() + decimal.Decimal(other))
            return self

    def __int__(self):
        with decimal.localcontext(_DECIMAL128_CTX) as ctx:
            return int(self.to_decimal())

    def __neg__(self):
        # Faster than going through Decimal conversion
        if self.is_signed():
            self.__high &= ~_SIGN
        else:
            self.__high |= _SIGN
        return self

    def __mul__(self, other):
        with decimal.localcontext(_DECIMAL128_CTX) as ctx:
            if isinstance(other, Decimal128):
                return Decimal128(self.to_decimal() * other.to_decimal())
            else:
                return Decimal128(self.to_decimal() * decimal.Decimal(other))

    def __pow__(self, other):
        with decimal.localcontext(_DECIMAL128_CTX) as ctx:
            if isinstance(other, Decimal128):
                return Decimal128(self.to_decimal() ** other.to_decimal())
            else:
                return Decimal128(self.to_decimal() ** decimal.Decimal(other))

    def __sub__(self, other):
        with decimal.localcontext(_DECIMAL128_CTX) as ctx:
            if isinstance(other, Decimal128):
                return Decimal128(self.to_decimal() - other.to_decimal())
            else:
                return Decimal128(self.to_decimal() - decimal.Decimal(other))

    def __truediv__(self, other):
        with decimal.localcontext(_DECIMAL128_CTX) as ctx:
            if isinstance(other, Decimal128):
                return Decimal128(self.to_decimal() / other.to_decimal())
            else:
                return Decimal128(self.to_decimal() / decimal.Decimal(other))
