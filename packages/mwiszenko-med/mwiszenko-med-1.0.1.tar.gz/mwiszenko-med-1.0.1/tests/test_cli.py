import argparse
import pytest

from med.cli import (
    non_negative_int,
    probability_float,
)


def test_positive_int():
    assert non_negative_int("2") == 2
    with pytest.raises(argparse.ArgumentTypeError):
        non_negative_int("-2")
    with pytest.raises(argparse.ArgumentTypeError):
        non_negative_int("0.5")
    with pytest.raises(argparse.ArgumentTypeError):
        non_negative_int("invalid")


def test_min_support_percentage_type():
    assert probability_float("0.5") == 0.5
    with pytest.raises(argparse.ArgumentTypeError):
        probability_float("2")
    with pytest.raises(argparse.ArgumentTypeError):
        probability_float("invalid")
