from __future__ import annotations

from dataclasses import dataclass
from math import atan2, cos, hypot, sin
from numbers import Real
from typing import Iterable, Tuple, Union


NumberLike = Union["ComplexNumber", complex, Real]


@dataclass(frozen=True)
class ComplexNumber:
    """Immutable complex number implementation with common helpers."""

    real: float = 0.0
    imag: float = 0.0

    def __post_init__(self) -> None:
        object.__setattr__(self, "real", float(self.real))
        object.__setattr__(self, "imag", float(self.imag))

    # Construction helpers -------------------------------------------------
    @classmethod
    def from_iterable(cls, values: Iterable[Real]) -> "ComplexNumber":
        real, imag = values
        return cls(real, imag)

    @classmethod
    def from_polar(cls, radius: Real, angle_radians: Real) -> "ComplexNumber":
        return cls(radius * cos(angle_radians), radius * sin(angle_radians))

    # Representation helpers ----------------------------------------------
    def __repr__(self) -> str:  # pragma: no cover - trivial repr
        return f"ComplexNumber(real={self.real}, imag={self.imag})"

    def __str__(self) -> str:
        sign = "+" if self.imag >= 0 else "-"
        imag_val = abs(self.imag)
        return f"{self.real} {sign} {imag_val}i"

    # Dunder protocol helpers ---------------------------------------------
    def __complex__(self) -> complex:
        return complex(self.real, self.imag)

    def __iter__(self):
        yield self.real
        yield self.imag

    def __bool__(self) -> bool:
        return not self.is_zero()

    def __abs__(self) -> float:
        return self.magnitude

    # Comparisons ----------------------------------------------------------
    def __eq__(self, other: object) -> bool:
        if isinstance(other, ComplexNumber):
            return self.real == other.real and self.imag == other.imag
        if isinstance(other, complex):
            return self.real == other.real and self.imag == other.imag
        if isinstance(other, Real):
            return self.imag == 0 and self.real == float(other)
        return NotImplemented

    # Arithmetic operations ------------------------------------------------
    def __add__(self, other: NumberLike) -> "ComplexNumber":
        rhs = self._coerce(other)
        if rhs is NotImplemented:  # pragma: no cover - guard rails
            return NotImplemented
        return ComplexNumber(self.real + rhs.real, self.imag + rhs.imag)

    def __radd__(self, other: NumberLike) -> "ComplexNumber":
        return self.__add__(other)

    def __sub__(self, other: NumberLike) -> "ComplexNumber":
        rhs = self._coerce(other)
        if rhs is NotImplemented:  # pragma: no cover
            return NotImplemented
        return ComplexNumber(self.real - rhs.real, self.imag - rhs.imag)

    def __rsub__(self, other: NumberLike) -> "ComplexNumber":
        rhs = self._coerce(other)
        if rhs is NotImplemented:  # pragma: no cover
            return NotImplemented
        return ComplexNumber(rhs.real - self.real, rhs.imag - self.imag)

    def __mul__(self, other: NumberLike) -> "ComplexNumber":
        rhs = self._coerce(other)
        if rhs is NotImplemented:  # pragma: no cover
            return NotImplemented
        real = self.real * rhs.real - self.imag * rhs.imag
        imag = self.real * rhs.imag + self.imag * rhs.real
        return ComplexNumber(real, imag)

    def __rmul__(self, other: NumberLike) -> "ComplexNumber":
        return self.__mul__(other)

    def __truediv__(self, other: NumberLike) -> "ComplexNumber":
        rhs = self._coerce(other)
        if rhs is NotImplemented:  # pragma: no cover
            return NotImplemented
        denominator = rhs.real ** 2 + rhs.imag ** 2
        if denominator == 0:
            raise ZeroDivisionError("division by zero in ComplexNumber")
        real = (self.real * rhs.real + self.imag * rhs.imag) / denominator
        imag = (self.imag * rhs.real - self.real * rhs.imag) / denominator
        return ComplexNumber(real, imag)

    def __rtruediv__(self, other: NumberLike) -> "ComplexNumber":
        rhs = self._coerce(other)
        if rhs is NotImplemented:  # pragma: no cover
            return NotImplemented
        return rhs.__truediv__(self)

    # Public API -----------------------------------------------------------
    @property
    def magnitude(self) -> float:
        return hypot(self.real, self.imag)

    @property
    def argument(self) -> float:
        return atan2(self.imag, self.real)

    def conjugate(self) -> "ComplexNumber":
        return ComplexNumber(self.real, -self.imag)

    def normalized(self) -> "ComplexNumber":
        if self.is_zero():
            raise ValueError("Cannot normalize the zero complex number.")
        mag = self.magnitude
        return ComplexNumber(self.real / mag, self.imag / mag)

    def is_zero(self, tolerance: float = 0.0) -> bool:
        return abs(self.real) <= tolerance and abs(self.imag) <= tolerance

    def to_polar(self) -> Tuple[float, float]:
        return self.magnitude, self.argument

    def to_tuple(self) -> Tuple[float, float]:
        return self.real, self.imag

    def reciprocal(self) -> "ComplexNumber":
        return ComplexNumber(1.0, 0.0) / self

    # Internal helpers -----------------------------------------------------
    @staticmethod
    def _coerce(value: NumberLike) -> "ComplexNumber | NotImplemented":
        if isinstance(value, ComplexNumber):
            return value
        if isinstance(value, complex):
            return ComplexNumber(value.real, value.imag)
        if isinstance(value, Real):
            return ComplexNumber(float(value), 0.0)
        return NotImplemented
