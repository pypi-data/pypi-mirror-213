import pytest

from med.base import (
    DataSet,
    read_sequence_file,
)


DATA_SETS = [
    [read_sequence_file(filename="tests/data/test.txt"), 4],
    [read_sequence_file(filename="tests/data/invalid.txt"), 0],
    [read_sequence_file(filename="tests/data/empty.txt"), 0],
]


@pytest.mark.parametrize("data_set,length", DATA_SETS)
def test_read_sequence_file(data_set: DataSet, length: int):
    assert type(data_set) == DataSet
    assert len(data_set) == length
