from typing import Union, List, Tuple, Iterable, Optional, TypeVar
from dataclasses import dataclass
import numpy as np

IndexValue = Union[int, slice, Tuple[int]]


def merge_slices(existing_slice: slice, new_slice: slice) -> slice:
    """Compose two slice objects

    Given an iterable x, the following should be equivalent:
    x[existing_slice][new_slice]
    x[merge_slices(existing_slice, new_slice)]

    Args:
        existing_slice (slice): The existing slice to be restricted.
        new_slice (slice): The new slice to be applied to the existing slice.

    Returns:
        slice: the composition of the given slices
    """

    # Combine the steps
    step1 = existing_slice.step if existing_slice.step is not None else 1
    step2 = new_slice.step if new_slice.step is not None else 1
    step = step1 * step2

    # Combine the start points
    start1 = existing_slice.start if existing_slice.start is not None else 0
    start2 = new_slice.start if new_slice.start is not None else 0
    start = start1 + start2 * step1

    # Combine the end points
    stop1 = existing_slice.stop
    stop2 = new_slice.stop

    if stop2 is None:
        stop = stop1
    else:
        stop = start + (stop2 - start2) * step1
        if stop1 is not None:
            stop = min(stop, stop1)

    return slice(start, stop, step)


def slice_at_int(s: slice, i: int):
    """Returns the `i`th element of a slice `s`.

    Examples:
        >>> slice_at_int(slice(None), 10)
        10

        >>> slice_at_int(slice(10, 20, 2), 3)
        16

    Args:
        s (slice): The slice to index into.
        i (int): The integer offset into the slice.

    Returns:
        The index corresponding to the offset into the slice.
    """
    return (s.start or 0) + i * (s.step or 1)


@dataclass
class IndexEntry:
    value: IndexValue = slice(None)

    def __getitem__(self, item: IndexValue):
        """Combines the given `item` and this IndexEntry.
        Returns a new IndexEntry representing the composition of the two.

        Examples:
            >>> IndexEntry()[0:100]
            IndexEntry(slice(0, 100, None))

            >>> IndexEntry()[100:200][5]
            IndexEntry(105)

            >>> IndexEntry()[(0, 1, 2, 3)]
            IndexEntry((0, 1, 2, 3))

            >>> IndexEntry()[1, 2, 3]
            IndexEntry((0, 1, 2, 3))

        Args:
            item: The desired sub-index to be composed with this IndexEntry.
                Can be an int, a slice, or a tuple of ints.

        Returns:
            The new IndexEntry object.

        Raises:
            TypeError: An integer IndexEntry should not be indexed further.
        """

        if not self.subscriptable():
            raise TypeError(
                "Subscripting IndexEntry after 'int' is not allowed. Use Index instead."
            )
        elif isinstance(self.value, slice):
            if isinstance(item, int):
                new_value = slice_at_int(self.value, item)
                return IndexEntry(new_value)
            elif isinstance(item, slice):
                return IndexEntry(merge_slices(self.value, item))
            elif isinstance(item, tuple):
                new_value = tuple(slice_at_int(self.value, idx) for idx in item)
                return IndexEntry(new_value)
        elif isinstance(self.value, tuple):
            if isinstance(item, int) or isinstance(item, slice):
                return IndexEntry(self.value[item])
            elif isinstance(item, tuple):
                new_value = tuple(self.value[idx] for idx in item)
                return IndexEntry(new_value)

        raise TypeError(f"Value {item} is of unrecognized type {type(item)}.")

    def subscriptable(self):
        """Returns whether an IndexEntry can be further subscripted."""
        return not isinstance(self.value, int)

    def indices(self, length: int):
        """Generates the sequence of integer indices for a target of a given length."""
        if isinstance(self.value, int):
            yield self.value
        elif isinstance(self.value, slice):
            start = self.value.start or 0
            stop = min(length, self.value.stop or length)
            step = self.value.step or 1
            yield from range(start, stop, step)
        elif isinstance(self.value, tuple):
            for i in self.value:
                if i >= length:
                    break
                yield i

    def is_trivial(self):
        """Checks if an IndexEntry represents the entire slice"""
        return (
            isinstance(self.value, slice)
            and not self.value.start
            and self.value.stop == None
            and ((self.value.step or 1) == 1)
        )


class Index:
    def __init__(
        self,
        item: Union[IndexValue, "Index", List[IndexEntry]] = slice(None),
    ):
        """Initializes an Index from an IndexValue, another Index, or the values from another Index.

        Represents a list of IndexEntry objects corresponding to indexes into each axis of an ndarray.
        """
        if isinstance(item, Index):
            item = item.values

        if not (isinstance(item, list) and isinstance(item[0], IndexEntry)):
            item = [IndexEntry(item)]

        self.values: List[IndexEntry] = item

    def find_axis(self, offset: int = 0):
        """Returns the index for the nth subscriptable axis in the values of an Index.

        Args:
            offset (int): The number of subscriptable axes to skip before returning.
                Defaults to 0, meaning that the first valid axis is returned.

        Returns:
            int: The index of the found axis, or None if no match is found.
        """
        matches = 0
        for idx, entry in enumerate(self.values):
            if entry.subscriptable():
                if matches == offset:
                    return idx
                else:
                    matches += 1
        return None

    def compose_at(self, item: IndexValue, i: Optional[int] = None):
        """Returns a new Index representing the addition of an IndexValue,
        or the composition with a given axis.

        Examples:
            >>> Index([slice(None), slice(None)]).compose_at(5)
            Index([slice(None), slice(None), 5])

            >>> Index([slice(None), slice(5, 10), slice(None)]).compose_at(3, 1)
            Index([slice(None), 8, slice(None)])

        Args:
            item (IndexValue): The value to append or compose with the Index.
            i (int, optional): The axis to compose with the given item.
                Defaults to None, meaning that the item will be appended instead.

        Returns:
            Index: The result of the addition or composition.
        """
        if i is None or i >= len(self.values):
            return Index(self.values + [IndexEntry(item)])
        else:
            new_values = self.values[:i] + [self.values[i][item]] + self.values[i + 1 :]
            return Index(new_values)

    def __getitem__(
        self, item: Union[int, slice, List[int], Tuple[IndexValue], "Index"]
    ):
        """Returns a new Index representing a subscripting with the given item.
        Modeled after NumPy's advanced integer indexing.

        See: https://numpy.org/doc/stable/reference/arrays.indexing.html

        Examples:
            >>> Index([5, slice(None)])[5]
            Index([5, 5])

            >>> Index([5])[5:6]
            Index([5, slice(5, 6)])

            >>> Index()[0, 1, 2:5, 3]
            Index([0, 1, slice(2, 5), 3])

            >>> Index([slice(5, 6)])[(0, 1, 2:5, 3),]
            Index([(5, 1, slice(2, 5), 3)])

        Args:
            item: The contents of the subscript expression to add to this Index.

        Returns:
            Index: The Index representing the result of the subscript operation.

        Raises:
            TypeError: Given item should be another Index,
                or compatible with NumPy's advanced integer indexing.
        """
        if isinstance(item, int) or isinstance(item, slice):
            ax = self.find_axis()
            return self.compose_at(item, ax)
        elif isinstance(item, tuple):
            new_index = self
            for idx, sub_item in enumerate(item):
                ax = new_index.find_axis(offset=idx)
                new_index = new_index.compose_at(sub_item, ax)
            return new_index
        elif isinstance(item, list):
            return self[(tuple(item),)]  # type: ignore
        elif isinstance(item, Index):
            base = self
            for index in item.values:
                value = index.value
                if isinstance(value, tuple):
                    value = (value,)  # type: ignore
                base = base[value]
            return base
        else:
            raise TypeError(f"Value {item} is of unrecognized type {type(item)}.")

    def apply(self, array: np.ndarray):
        """Applies an Index to a batched ndarray with the same number of samples
        as the first entry in the Index.
        """
        index_values = tuple(item.value for item in self.values[1:])
        if not self.values[0].subscriptable():
            array = array[0]  # remove unit batch axis
        else:
            index_values = (slice(None),) + index_values

        return array[index_values]

    def is_trivial(self):
        """Checks if an index is equivalent to the trivial slice `[:]`, aka slice(None)."""
        return (len(self.values) == 1) and self.values[0].is_trivial()

    def __str__(self):
        values = [entry.value for entry in self.values]
        return f"Index({values})"

    def __repr__(self):
        return f"Index(values={self.values})"
