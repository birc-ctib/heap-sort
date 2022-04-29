"""Testing min-heap."""

from heap import Heap


def test_min_heap_sort() -> None:
    """Test sorting with a min-heap."""
    x = [1, 6, 3, 7, 8, 3, 5]

    z = x[:]  # get a copy we can sort to compare
    z.sort()

    heap = Heap.min_heap(x)
    y = []
    while heap:
        y.append(heap.pop())

    assert y == z


def test_min_heap_sort_inplace() -> None:
    """Test sorting with a min-heap."""
    x = [1, 6, 3, 7, 8, 3, 5]

    z = x[:]  # get a copy we can sort to compare
    z.sort(reverse=True)

    heap = Heap.min_heap(x)
    while heap:
        heap.pop()

    assert x == z


def test_max_heap_sort() -> None:
    """Test sorting with a max-heap."""
    x = [1, 6, 3, 7, 8, 3, 5]

    z = x[:]  # get a copy we can sort to compare
    z.sort(reverse=True)

    heap = Heap.max_heap(x)
    y = []
    while heap:
        y.append(heap.pop())

    assert y == z


def test_max_heap_sort_inplace() -> None:
    """Test sorting with a max-heap."""
    x = [1, 6, 3, 7, 8, 3, 5]

    z = x[:]  # get a copy we can sort to compare
    z.sort()

    heap = Heap.max_heap(x)
    while heap:
        heap.pop()

    assert x == z
