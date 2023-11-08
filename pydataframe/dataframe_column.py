__all__ = ['DataFrameColumn']

from .dataframe_line import DataFrameLine


def get_none_value(t: type = None):
    """
    Get the Null value from the selected type
    :param t:
    :return:
    """
    if t == int:
        return 0
    elif t == float:
        return 0.0
    elif t == str:
        return ''
    elif t == list:
        return []
    else:
        return None


class DataFrameColumn:
    """
    Object to represent a database/dataframe column
    """

    def __init__(self, values: list, name: str, index: list = None, dtype: type = None):
        """
        Constructor of the DataFrameColumn object
        :param values: Values of the column
        :param name: Name of the data column
        :param index: row indexes
        :param dtype: data type of the column (int, float, str)
        """

        self.values: list = values
        self.index: list = (index if index is not None else [i for i in range(len(values))])
        self.name: str = name
        self.dtype: type = dtype
        self.size: int = len(values)

    def __add__(self, other):
        """
        Add values or column to the current column
        :param other:
        :return:
        """

        if type(other) == self.dtype:
            return DataFrameColumn(self.values + [other], self.name, self.index + [self.size], self.dtype)
        elif type(other) == list:
            return DataFrameColumn(self.values + other, self.name, dtype=self.dtype)
        elif isinstance(other, DataFrameLine) and type(other.values[self.name]) == self.dtype:
            return self.__add__(other.values[self.name])
        elif isinstance(other, DataFrameColumn) and self.dtype == other.dtype:
            return DataFrameColumn(self.values + other.values, self.name, dtype=self.dtype)

    def __and__(self, other):
        if not isinstance(other, DataFrameColumn):
            return DataFrameColumn([], self.name, [], self.dtype)

        index: list = list(set(sorted(self.index)) & set(sorted(other.index)))

        return self.__getitem__(index)

    def __copy__(self):
        return DataFrameColumn(self.values.copy(), self.name, self.index.copy(), self.dtype)

    def __eq__(self, other):
        if isinstance(other, DataFrameColumn):
            return self.inter(other)
        elif type(other) == tuple:
            return self.__eq__(list(other))
        elif type(other) == list:
            return self.filter(lambda e: e in other)
        else:
            return self.filter(lambda e: e == other)

    def __ge__(self, other):
        return self.filter(lambda e: e >= other)

    def __getitem__(self, item):
        if type(item) == int and 0 <= item < self.size:
            return DataFrameColumn(self.values[item], self.name, [item], self.dtype)
        elif type(item) == slice:
            if 0 <= item.start < self.size and 0 <= item.stop < self.size:
                return DataFrameColumn(self.values[item], self.name, list(range(item.start, item.stop, item.step)),
                                       self.dtype)
            else:
                return DataFrameColumn([get_none_value(self.dtype)], self.name, [0], self.dtype)
        elif type(item) == tuple:
            return self.__getitem__(list(item))
        elif type(item) == list:
            l_int, l_other = [], []

            for e in item:
                if type(e) == int:
                    l_int.append(e)
                else:
                    l_other.append(e)

            l_v, l_i = [], []
            for e in l_int:
                if 0 <= e < self.size:
                    l_v.append(self.values[e])
                    l_i.append(e)

            dc = DataFrameColumn(l_v, self.name, l_i, self.dtype)
            for e in l_other:
                dc = dc.union(self.__getitem__(e))

            return dc
        elif isinstance(item, DataFrameColumn):
            return self.__getitem__(item.index)

    def __gt__(self, other):
        return self.filter(lambda e: e > other)

    def __le__(self, other):
        return self.filter(lambda e: e <= other)

    def __iter__(self):
        return self.values.copy()

    def __lt__(self, other):
        return self.filter(lambda e: e < other)

    def __ne__(self, other):
        if isinstance(other, DataFrameColumn):
            return self.outer(other)
        elif type(other) == tuple:
            return self.__ne__(list(other))
        elif type(other) == list:
            return self.filter(lambda e: e not in other)
        else:
            return self.filter(lambda e: e != other)

    def __len__(self) -> int:
        return self.size

    def __or__(self, other):
        if not isinstance(other, DataFrameColumn):
            return DataFrameColumn([], self.name, [], self.dtype)

        index: list = list(set(sorted(self.index)) & set(sorted(other.index)))

        return self.__getitem__(index)

    def __setitem__(self, key, value) -> None:
        if type(key) == int and 0 <= key < self.size:
            self.values[key] = value
        elif type(key) == slice:
            self.__setitem__(list(range(key.start, key.stop, key.step)), value)
        elif type(key) == tuple:
            self.__setitem__(list(key), value)
        elif type(key) == list:
            for e in key:
                if type(e) == int:
                    self.values[e] = value
                else:
                    self.__setitem__(e, value)

        elif isinstance(key, DataFrameColumn):
            self.__setitem__(key.index, value)

    def __str__(self):
        return 'DataFrameColumn(name=' + self.name + ',size=' + str(self.size) + ',dtype=' + str(self.dtype) + ')'

    def avg(self):
        if self.dtype not in [float, int] or self.size == 0:
            return 0

        return sum(self.values) / self.size

    def filter(self, f):
        l: list = []
        index: list = []

        for i in range(self.size):
            o = self.values[i]
            if f(o):
                l.append(o)
                index.append(i)

        return DataFrameColumn(l, self.name, index, self.dtype)

    def inter(self, dc):
        return self.__and__(dc)

    def map_column(self, f):
        return DataFrameColumn([f(e) for e in self.values], self.name, self.index.copy(), self.dtype)

    def mean(self):
        # TODO
        pass

    def outer(self, dc):
        if not isinstance(dc, DataFrameColumn):
            return self.__copy__()

        index: list = list(set(sorted(self.index)) - set(sorted(dc.index)))

        return self.__getitem__(index)

    def sort_by_value(self, reverse: bool = False):
        d: dict = {self.index[i]: self.values[i] for i in range(self.size)}
        d = {k: d[k] for k in sorted(d.keys(), key=d.__getitem__, reverse=reverse)}

        self.values: list = list(d.values())
        self.index: list = list(d.keys())

        return self

    def sort_by_index(self, reverse: bool = False):
        d: dict = {self.index[i]: self.values[i] for i in range(self.size)}
        d = {k: d[k] for k in sorted(d.keys())}

        self.values: list = list(d.values())
        self.index: list = list(d.keys())

        return self

    def summary(self, n_rows: int = 10):
        return (self.name + '\n' +
                ''.join(['-' for i in range(len(self.name))]) +
                ''.join(['\n' + str(self.values[i]) for i in range(min(self.size, n_rows))]))

    def to_list(self):
        return self.__iter__()

    def union(self, dc):
        return self.__or__(dc)

    def unique(self):
        """
        Get unique values of a column
        :return: a DataFrameColumn object
        """
        return DataFrameColumn(list(set(self.values)), self.name, dtype=self.dtype)
