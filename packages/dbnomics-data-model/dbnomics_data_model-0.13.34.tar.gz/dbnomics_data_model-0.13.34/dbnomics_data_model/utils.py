"""Utility functions."""

from typing import Any, Callable, Collection, Iterable, Optional, TypeVar

__all__ = ["find", "find_index", "is_empty_collection"]

K = TypeVar("K")
T = TypeVar("T")
V = TypeVar("V")


def find(predicate: Callable[[T], bool], items: Iterable[T], default=None) -> Optional[T]:
    """Find the first item in ``items`` satisfying ``predicate(item)``.

    Return the found item, or return ``default`` if no item was found.

    >>> find(lambda item: item > 2, [1, 2, 3, 4])
    3
    >>> find(lambda item: item > 10, [1, 2, 3, 4])
    >>> find(lambda item: item > 10, [1, 2, 3, 4], default=42)
    42
    """
    for item in items:
        if predicate(item):
            return item
    return default


def find_index(predicate: Callable[[T], bool], items: Iterable[T], default=None) -> int:
    """Find the index of the first item satisfying the predicate."""
    return next((i for i, item in enumerate(items) if predicate(item)), default)


def is_empty_collection(v: Any) -> bool:
    """Return True if value is an empty collection."""
    if isinstance(v, Collection) and not v:
        return True
    return False
