"""Rolling window utilities with optional logging decorators and descriptors."""

from __future__ import annotations

from functools import wraps
from typing import Iterable, Iterator, Optional, Tuple, Union

import math
import time


Number = Union[int, float]


def log_calls(func):
    """Return a decorated function that logs each invocation."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[log] {func.__name__}(args={args[1:]}, kwargs={kwargs})")
        return func(*args, **kwargs)

    return wrapper


def measure_time(func):
    """Return a decorated function that reports execution time in milliseconds."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        t0 = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            dt = (time.perf_counter() - t0) * 1000
            print(f"[time] {func.__name__} took {dt:.2f} ms")

    return wrapper


class PositiveInt:
    """Descriptor that ensures a managed attribute stores a strictly positive int."""

    def __set_name__(self, owner, name):
        """Record the private storage name used on instances."""
        self._storage = f"_{name}"

    def __get__(self, obj, objtype=None) -> int:
        """Return the stored value or the descriptor when accessed on the class."""
        if obj is None:
            return self
        return getattr(obj, self._storage)

    def __set__(self, obj, value) -> None:
        """Validate the incoming value and persist it on the instance."""
        try:
            iv = int(value)
        except Exception as e:
            raise TypeError(f"{self._storage} must be an int") from e
        if iv <= 0:
            raise ValueError(f"{self._storage} must be > 0")
        setattr(obj, self._storage, iv)


class RollingWindow:
    """Fixed-capacity ring buffer that exposes rolling statistics."""

    __slots__ = ("_data", "_head", "_count", "_capacity", "_summary_cached")

    capacity = PositiveInt()

    def __init__(self, capacity: int):
        """Initialize storage arrays and bookkeeping for the requested capacity."""
        self.capacity = capacity
        self._data: list[Number] = [0] * self.capacity
        self._head: int = 0
        self._count: int = 0
        self._summary_cached: Optional[Tuple[float, float, Number, Number]] = None

    def __repr__(self) -> str:
        """Return a helpful string representation for debugging."""
        return f"RollingWindow(capacity={self.capacity}, size={self.size})"

    def __eq__(self, other: object) -> bool:
        """Compare two windows based on their realized sequence of values."""
        if not isinstance(other, RollingWindow):
            return NotImplemented
        return list(self) == list(other)

    def __len__(self) -> int:
        """Return the number of elements currently stored."""
        return self.size

    def __iter__(self) -> Iterator[Number]:
        """Yield elements from oldest to newest."""
        for i in range(self._count):
            yield self._data[(self._head + i) % self._capacity]

    def __getitem__(self, idx):
        """Return items by index or slice, honoring negative indices."""
        if isinstance(idx, slice):
            return list(self)[idx]
        n = self._count
        if n == 0:
            raise IndexError("empty window")
        if idx < 0:
            idx += n
        if not (0 <= idx < n):
            raise IndexError("index out of range")
        return self._data[(self._head + idx) % self._capacity]

    def __contains__(self, x: Number) -> bool:
        """Return True when the value exists in the window."""
        return any(v == x for v in self)

    def __call__(self, x: Number) -> None:
        """Delegate to ``push`` so instances can be invoked like a function."""
        self.push(x)

    @log_calls
    @measure_time
    def push(self, x: Number) -> None:
        """Insert a value, evicting the oldest element when the window is full."""
        tail = (self._head + self._count) % self._capacity
        if self._count < self._capacity:
            self._data[tail] = x
            self._count += 1
        else:
            self._data[self._head] = x
            self._head = (self._head + 1) % self._capacity
        self._summary_cached = None

    @log_calls
    def extend(self, xs: Iterable[Number]) -> None:
        """Push each value from the iterable into the window in order."""
        for x in xs:
            self.push(x)

    def clear(self) -> None:
        """Reset the window to an empty state without reallocating storage."""
        self._head = 0
        self._count = 0
        self._summary_cached = None

    @property
    def size(self) -> int:
        """Number of elements currently stored in the window."""
        return self._count

    @property
    def is_full(self) -> bool:
        """True when the window is at capacity."""
        return self.size == self.capacity

    @property
    def sum(self) -> float:
        """Sum of all values in the window as a float."""
        return float(sum(self))

    @property
    def mean(self) -> float:
        """Arithmetic mean of the window contents."""
        if self._count == 0:
            raise ValueError("mean undefined for empty window")
        return self.sum / self._count

    @property
    def min(self) -> Number:
        """Smallest value stored in the window."""
        if self._count == 0:
            raise ValueError("min undefined for empty window")
        return min(self)

    @property
    def max(self) -> Number:
        """Largest value stored in the window."""
        if self._count == 0:
            raise ValueError("max undefined for empty window")
        return max(self)

    @property
    def values(self) -> list[Number]:
        """Return the current window contents from oldest to newest."""
        return list(self)

    @property
    def summary(self) -> Tuple[float, float, Number, Number]:
        """Return ``(mean, std, min, max)`` caching the result until mutation."""
        if self._summary_cached is not None:
            return self._summary_cached
        if self._count == 0:
            raise ValueError("summary undefined for empty window")

        mu = self.mean
        if self._count == 1:
            std = 0.0
        else:
            acc = 0.0
            for v in self:
                delta = float(v) - mu
                acc += delta * delta
            std = math.sqrt(acc / self._count)
        mn = self.min
        mx = self.max

        self._summary_cached = (mu, std, mn, mx)
        return self._summary_cached

    @classmethod
    def from_iterable(cls, capacity: int, xs: Iterable[Number]) -> "RollingWindow":
        """Create a populated window by pushing each value from an iterable."""
        rw = cls(capacity)
        rw.extend(xs)
        return rw

    @staticmethod
    def zscore(x: Number, mean: float, std: float) -> float:
        """Return the Z-score for ``x`` using the provided mean and std-dev."""
        return 0.0 if std == 0 else (float(x) - mean) / std

    def transaction(self):
        """Provide a context manager that rolls back mutations on exception."""
        rw = self

        class _Txn:
            """Context manager capturing and optionally restoring state."""

            def __enter__(self_):
                """Snapshot the current window state and expose the manager."""
                self_._snapshot = (rw._data[:], rw._head, rw._count, rw._summary_cached)
                return self_

            def __exit__(self_, exc_type, exc, tb):
                """Restore the snapshot when an exception escapes the context."""
                if exc_type is not None:
                    data, head, count, summary = self_._snapshot
                    rw._data = data[:]
                    rw._head = head
                    rw._count = count
                    rw._summary_cached = summary
                return False

        return _Txn()