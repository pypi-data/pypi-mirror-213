from med.constants import (
    DEFAULT_MAX_LENGTH,
    DEFAULT_MIN_LENGTH,
    MIN_PROBABILITY_FLOAT,
    MAX_PROBABILITY_FLOAT,
)


def test_constants():
    assert DEFAULT_MAX_LENGTH == 100
    assert DEFAULT_MIN_LENGTH == 1
    assert MIN_PROBABILITY_FLOAT == 0.0
    assert MAX_PROBABILITY_FLOAT == 1.0
