# decimal128

[![build:](https://github.com/masaccio/decimal128/actions/workflows/run-all-tests.yml/badge.svg)](https://github.com/masaccio/decimal128/actions/workflows/run-all-tests.yml)
[![codecov](https://codecov.io/gh/masaccio/decimal128/branch/main/graph/badge.svg?token=EKIUFGT05E)](https://codecov.io/gh/masaccio/decimal128)

This package is primarily a fork of the [decimal128 support](https://github.com/mongodb/mongo-python-driver/blob/master/bson/decimal128.py) found in the [MondoDB python driver](https://github.com/mongodb/mongo-python-driver>). The motivation for this project is to provide a standalone package with no dependencies that does not need all of MongoDB's python driver.

## Usage

The `Decimal128` class behaves largely like a standard python [`decimal.Decimal`](https://docs.python.org/3/library/decimal.html#decimal-objects) class. Most arithmetic operators are  included and the package supports a small number of additional init values to allow for conversion from binary integer decimal (BID). `Decimal128` uses an instance of [`decimal.Context`](https://docs.python.org/3/library/decimal.html#decimal.Context) configured for IEEE-754 Decimal128 when validating parameters.

Unlike MongoDB's [`Decimal128`](https://github.com/mongodb/mongo-python-driver/blob/master/bson/decimal128.py), no signals are trapped and as such, exceptions are not raised for  [`decimal.InvalidOperation`](https://docs.python.org/3/library/decimal.html#decimal.InvalidOperation), [`decimal.Inexact`](https://docs.python.org/3/library/decimal.html#decimal.Inexact), or [`decimal.Overflow`](https://docs.python.org/3/library/decimal.html#decimal.Overflow).

Supported init values are `str`, `int`, `float`, standard `decimal.Decimal` objects, BID `tuple`, and using a classmethof for BID `bytes`:

```default
>>> Decimal128("0.0625")
Decimal128('0.0625')
>>> Decimal128(Decimal("0.0625"))
Decimal128('0.0625')
>>> Decimal128(625)
Decimal128('625')
>>> Decimal128(0.0625)
Decimal128('0.0625')
>>> Decimal128((3474527112516337664,625))
Decimal128('0.0625')
>>> Decimal128.from_bid(bytes.fromhex("30380000000000000000000000000271"))
Decimal128('0.0625')
```

### `decimal.Decimal` compatibility

The helper function `create_decimal128_context` creates a `decimal.Context` which ensures that decimals creted by the standard library are identical to those created by `Decimal128`.

```default
>>> import decimal
>>> decimal128_ctx = create_decimal128_context()
>>> with decimal.localcontext(decimal128_ctx) as ctx:
...     Decimal128(ctx.create_decimal(".13.3"))
...
Decimal128('NaN')
>>>
>>> with decimal.localcontext(decimal128_ctx) as ctx:
...     Decimal128(ctx.create_decimal("1E-6177"))
...
Decimal128('0E-6176')
>>>
>>> with decimal.localcontext(decimal128_ctx) as ctx:
...     Decimal128(ctx.create_decimal("1E6145"))
...
Decimal128('Infinity')
```

The `to_decimal()` method returns a `decimal.Decimal` object for the stored value.

### Properties

#### bid(): → [bytes](https://docs.python.org/3/library/stdtypes.html#bytes)

The binary integer decimal (BID) encoding of this instance. BIDs are 16 bytes with the highest bits encoded first:

``` default
>>> Decimal128("999").bid().hex()
'304000000000000000000000000003e7'
>>> Decimal128("NaN").bid().hex()
'7c000000000000000000000000000000'
```

### Methods

#### from_bid(value: [bytes](https://docs.python.org/3/library/stdtypes.html#bytes))

Create an instance of `Decimal128` from binary integer decimal bytes.

**Parameters**:

* `value`: 16 byte string (128-bit IEEE 754-2008 decimal floating point in binary integer decimal (BID) format).

#### is_infinite() → [bool](https://docs.python.org/3/library/stdtypes.html#bool)

Return `True` if self is infinite; otherwise return `False`.

#### is_nan() → [bool](https://docs.python.org/3/library/stdtypes.html#bool)

Return `True` if self is a NaN; otherwise return `False`.

#### is_signed() → [bool](https://docs.python.org/3/library/stdtypes.html#bool)

Return `True` if self is negative; otherwise return `False`.

#### to_decimal() -> [`decimal.Decimal`](https://docs.python.org/3/library/decimal.html#decimal-objects)

Returns an instance of [`decimal.Decimal`](https://docs.python.org/3/library/decimal.html#decimal.Decimal) for this `Decimal128`.

#### to_float() → [float](https://docs.python.org/3/library/stdtypes.html#float)

Returns an instance of float for this `Decimal128`.

## Performance

`Decimal128` is considerably slower than `decimal.Decimal` using native libraries as all arithmetic operations involve creating new objects to perform the operation. Expect performance to be 200-300 times slower than `decimal.Decimal`.

## Credits

`decimal128` was built by [Jon Connell](http://github.com/masaccio) but started as a fork of the [decimal128 support](https://github.com/mongodb/mongo-python-driver/blob/master/bson/decimal128.py) found in the [MondoDB python driver](https://github.com/mongodb/mongo-python-driver).

Tests are adapted from the MongoDB tests for decimal128 and also from [John Dupuy's](https://github.com/JohnAD) Nim [implementation](https://github.com/JohnAD/decimal128) of decimal128.

## License

This project is licensed under the [Apache License 2.0](https://github.com/masaccio/decimal128/blob/main/LICENSE).

Some tests are licensed under the [MIT License]((https://github.com/masaccio/decimal128/blob/main/THIRD-PARTY-NOTICES)) which can be identified in the source comments.
