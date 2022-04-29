# Heap sort

You can implement a heap sort using a binary heap where you do not use any extra memory—you can do all the operations in the input list. We are going to do this now, in a few easy steps.

In `src/heap.py` I have put a generic heap--all the operations are there for both a max and min heap--but currently only with support for a min heap.

You can use it to implement a sorting algorithm like this:

```python
def min_heap_sort(x: list[Ord]) -> list[Ord]:
    heap = Heap.min_heap(x)
    y = []
    while heap:
        y.append(heap.pop())
    return y
```

The heap modifies `x` when we give it to it, and it will end up being empty when we are done sort. Instead, the values are moved into `y` in sorted order.

Because we are copying elements to a new list, it isn't exactly in-place, but we will make a similar function that is, that will look like this:

```python
def max_heap_sort(x: list[Ord]) -> list[Ord]:
    heap = Heap.max_heap(x)
    while heap:
        heap.pop()
    return x
```

**Step 1:** Modify the heap so you don't remove elements from the underlying list when you pop. You still need to keep track of how many elements are in the *heap*, but there can be fewer than you have in the list. You use the heap size when you swap elements in `pop()` but not the list size, and you should't pop the last element out of the list. If you do this, the original elements will end up at the back of the list as you pop, and when you are done, you have the elements in reversely sorted order.

**Question:** Why are the elements in reverse order?

**Step 2:** Get a max heap.

The order we pop elements in is determined by a function, which for the min heap is

```python
def select_min(a: Ord, b: Ord) -> Order:
    """Pick the smallest element."""
    return Order.First if a < b else Order.Second
```

and this function is used when making a min-heap

```python
    @staticmethod
    def min_heap(x: list[Ord]) -> Heap[Ord]:
        """Create a min-heap."""
        return Heap(x, select_min)
```

Make a corresponding selection function for a max heap and a corresponding static method for creating max heaps.

If you have done this correctly, the in-place heap sort above will work.
