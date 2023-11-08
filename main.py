# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from pydataframe import DataFrameColumn

d: DataFrameColumn = (DataFrameColumn(['a', 'b', 'c', 'd', 'e'], 'ggggggggggg', dtype=str) != 'a')
print(d.summary())
