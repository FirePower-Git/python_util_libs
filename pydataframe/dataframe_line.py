__all__ = ['DataFrameLine']


class DataFrameLine:

    def __init__(self, values: dict, row_index: int):
        self.values: dict = values
        self.row_index: int = row_index

    def __copy__(self):
        return DataFrameLine(self.values.copy(), self.row_index)

    def __eq__(self, other) -> bool:
        return isinstance(other, DataFrameLine) and other.values == self.values

    def __getitem__(self, item):
        if type(item) == int:
            if 0 <= item < len(list(self.values.keys())):
                return self.values[list(self.values.keys())[item]]
        elif type(item) == str:
            if item in self.values.keys():
                return self.values[item]
            else:
                return None
        return None

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __len__(self) -> int:
        return len(list(self.values.keys()))

    def __setitem__(self, key, value) -> None:
        if type(key) == int and 0 <= key < len(list(self.values.keys())):
            self.values[list(self.values.keys())[key]] = value
        elif type(key) == str and key in self.values.keys():
            self.values[key] = value

    def __str__(self) -> str:
        return 'DataFrameLine(index=' + str(self.row_index) + ',values=' + str(self.values) + ')'
