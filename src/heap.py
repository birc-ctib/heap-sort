"""
Abstract code and helpers for heaps.

The concrete heaps are found in min_heap.py and max_heap.py
"""

from __future__ import annotations
from typing import (
    Protocol, TypeVar, Optional, Generic,
    Callable, Union,
    Any
)
from enum import (
    Enum, auto
)

# == Type stuff ===========================================


class Ordered(Protocol):
    """Types that support < comparison."""

    def __lt__(self, other: Any) -> bool:
        """Determine if self is < other."""
        ...


Ord = TypeVar('Ord', bound=Ordered)


class Order(Enum):
    """In a comparison, should we pick the first or second value."""

    First = auto()
    Second = auto()


# This looks stupid, and it is, but it is a work-around
# for a bug in the mypy type checker
Selector = Union[Callable[[Ord, Ord], Order],
                 Callable[[Ord, Ord], Order]]

# == Helper functions =====================================


def parent(i: int) -> int:
    """Get the parent index of i."""
    return (i - 1) // 2


def left(i: int) -> int:
    """Get the left child of i."""
    return 2 * i + 1


def right(i: int) -> int:
    """Get the right child of i."""
    return 2 * i + 2


def get_optional(x: list[Ord], i: int, n: int) -> Optional[Ord]:
    """Get x[i] if i is a valid index, 0 <= i < n, otherwise None."""
    return x[i] if 0 <= i < n else None


def select_min(a: Ord, b: Ord) -> Order:
    """Pick the smallest element."""
    return Order.First if a < b else Order.Second

# == Generic heap =========================================
# Min and Max heaps look very much alike, so we don't want
# to have duplicated code for them. We abstract away the
# differences--just the comparision--and put the general
# code in a parameterised class. Create a min-heap with
# Heap::min_heap() and a max-heap with Heap::max_heap().


class Heap(Generic[Ord]):
    """
    Abstract interface to a heap.

    Implements heap operations on top of an existing list.

    The list you provide to the constructor is kept as a reference,
    so changes made to it are also reflected in any other reference
    you have to it. We plan to exploit this for sorting lists.

    """

    x: list[Ord]
    _select: Selector

    def __len__(self) -> int:
        """Get the current size of the heap."""
        # FIXME:
        # You can change this if you want the actual list to be
        # longer than the part you consider a heap.
        return len(self.x)

    def __bool__(self) -> int:
        """Return true if there are more elements in the heap."""
        return len(self) > 0

    def __init__(self, x: list[Ord], select: Selector):
        """
        Wrap x as a heap.

        We heapify the list when we get it so it is ready for
        sequences of delete_min().
        """
        self.x = x
        self._select = select
        self._heapify()

    def _heapify(self) -> None:
        """Inplace heapify x."""
        for i in reversed(range(len(self.x))):
            self._fix_down(i)

    def _get_child(self, i: int) -> Optional[int]:
        """Get the index of the optimal child."""
        l, r = left(i), right(i)

        # Get values, and handle out-of-bound at the same time
        l_val = get_optional(self.x, l, len(self))
        if l_val is None:
            return None
        r_val = get_optional(self.x, r, len(self))
        if r_val is None:
            return l

        # We have two values to pick the smallest from
        return l if self._select(l_val, r_val) is Order.First else r

    def _fix_down(self, i: int) -> None:
        """Move the value at x[i] down to its correct location."""
        while i < len(self):
            child = self._get_child(i)
            if child is None or \
                    self._select(self.x[i], self.x[child]) == Order.First:
                break
            self.x[i], self.x[child] = self.x[child], self.x[i]
            i = child

    def pop(self) -> Ord:
        """Remove the smallest value and return it."""
        val = self.x[0]
        self.x[0], self.x[len(self)-1] = self.x[len(self)-1], self.x[0]
        self.x.pop()  # FIXME: Changes the list; maybe you don't want this
        self._fix_down(0)
        return val

    # Static methods for picking min or max heap
    @staticmethod
    def min_heap(x: list[Ord]) -> Heap[Ord]:
        """Create a min-heap."""
        return Heap(x, select_min)


def min_heap_sort(x: list[Ord]) -> list[Ord]:
    """
    Sort x and return the sorted values.

    >>> min_heap_sort([1, 4, 2, 3, 5])
    [1, 2, 3, 4, 5]
    """
    heap = Heap.min_heap(x)
    y = []
    while heap:
        y.append(heap.pop())
    return y


def max_heap_sort(x: list[Ord]) -> list[Ord]:
    """
    Sort x and return the sorted values.

    >>> max_heap_sort([1, 4, 2, 3, 5])
    [1, 2, 3, 4, 5]
    """
    heap = Heap.max_heap(x)
    while heap:
        heap.pop()
    return x
