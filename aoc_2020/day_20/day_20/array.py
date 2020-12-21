"""
This module contains an array and a matrix class.
"""


class Array:
    """
    A simple array that you can add and multiply with other arrays and scalars.
    """

    def __init__(self, *args):
        self._vals = tuple(args)

    def __len__(self):
        return len(self._vals)

    def __getitem__(self, index):
        return self._vals[index]

    def __iter__(self):
        return iter(self._vals)

    def __add__(self, other):
        if isinstance(other, self.__class__):
            assert len(self) == len(other)
            return self.__class__(*[val_1 + val_2 for val_1, val_2 in zip(self, other)])
        if isinstance(other, int):
            return self.__class__(*[val + other for val in self])
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, self.__class__):
            assert len(self) == len(other)
            return self.__class__(*[val_1 * val_2 for val_1, val_2 in zip(self, other)])
        if isinstance(other, int):
            return self.__class__(*[val * other for val in self])
        return NotImplemented

    def __repr__(self):
        return f"{self.__class__.__name__}{self._vals}"

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._vals == other._vals
        raise NotImplemented

    def __hash__(self) -> int:
        return self._vals.__hash__()


class Matrix:
    """
    A 2-dimensional matrix.
    """

    def __init__(self, values):
        self._values = tuple(tuple(val for val in row) for row in values)
        self._shape = len(values[0]), len(values)

    def __getitem__(self, index):
        y, x = index
        item = self._values[y]
        if not isinstance(y, slice):
            return item[x]
        return tuple(tuple(i[x] for i in item))

    def __iter__(self):
        for row in self._values:
            yield row

    @property
    def rows(self):
        return iter(self)

    @property
    def cols(self):
        for i in range(self._shape[1]):
            yield self[:, i]

    def __len__(self):
        return self._shape[0]

    def _rot(self):
        """
        Rotates matrix clockwise by 90 degrees.
        """
        values = tuple(col[::-1] for col in self.cols)
        return self.__class__(values)

    def rot(self, k=1):
        """
        Rotates matrix clockwise by 90 degrees k times.
        """
        k = k % 4
        if not k:
            return deepcopy(self)
        matrix = self._rot()
        for _ in range(1, k):
            matrix = matrix._rot()
        return matrix

    def __repr__(self):
        return f"{self.__class__.__name__}(values={self._values})"

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._values == other._values
