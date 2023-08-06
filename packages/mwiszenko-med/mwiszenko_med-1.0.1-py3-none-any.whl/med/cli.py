import argparse
from statistics import mean
from time import time

from tqdm import tqdm

from med.base import DataSet, Sequence, prefix_span, read_sequence_file
from med.constants import (
    DEFAULT_MAX_LENGTH,
    DEFAULT_MIN_LENGTH,
    MAX_PROBABILITY_FLOAT,
    MIN_PROBABILITY_FLOAT,
)


def non_negative_int(arg: str):
    try:
        i = int(arg)
    except ValueError:
        raise argparse.ArgumentTypeError("Must be an integer number")
    if i < 0:
        raise argparse.ArgumentTypeError("Argument must be >= 0")
    return i


def probability_float(arg: str):
    try:
        f = float(arg)
    except ValueError:
        raise argparse.ArgumentTypeError("Must be a floating point number")
    if f < MIN_PROBABILITY_FLOAT or f > MAX_PROBABILITY_FLOAT:
        raise argparse.ArgumentTypeError(
            "Argument must be <= "
            + str(MAX_PROBABILITY_FLOAT)
            + " and >= "
            + str(MIN_PROBABILITY_FLOAT)
        )
    return f


class ModeMapper:
    def __init__(self) -> None:
        pass

    @staticmethod
    def run(args):
        ds: DataSet = read_sequence_file(filename=args.input)
        if len(ds) == 0:
            print("Data could not be loaded properly.")
            exit(1)

        min_sup: float
        if args.min_sup is not None:
            min_sup = args.min_sup
        else:
            min_sup = args.min_sup_percentage * len(ds)
        res: dict[Sequence, int] = prefix_span(
            ds, min_sup, args.min_length, args.max_length
        )
        ordered_res: dict[Sequence, int] = dict(
            sorted(res.items(), key=lambda item: item[1], reverse=True)
        )
        number_of_found_sequences: str = "Number of found sequences: " + str(
            len(ordered_res)
        )
        found_sequences: str = "\n".join(
            "{}: {}".format(k, v) for k, v in ordered_res.items()
        )
        if args.output:
            with open(args.output, "w") as output:
                output.write(str(args))
                output.write("\n\n")
                output.write(number_of_found_sequences)
                output.write("\n\n")
                output.write(found_sequences)
        else:
            print(number_of_found_sequences)
            print(found_sequences)

    @staticmethod
    def test(args):
        ds: DataSet = read_sequence_file(filename=args.input)
        if len(ds) == 0:
            print("Data could not be loaded properly.")
            exit(1)

        min_sup: float
        if args.min_sup is not None:
            min_sup = args.min_sup
        else:
            min_sup = args.min_sup_percentage * len(ds)

        results = []
        for _ in tqdm(range(args.iterations)):
            start_time = time()
            prefix_span(ds, min_sup, args.min_length, args.max_length)
            results.append(time() - start_time)
        print("Average time of execution: {0:.2f} s".format(mean(results)))


def main():  # pragma: no cover
    parser = argparse.ArgumentParser()
    modes = parser.add_subparsers(dest="command", required=True)

    # run mode
    run_mode = modes.add_parser("run")
    run_mode.add_argument("--input", "-i", type=str, required=True)
    run_mode.add_argument("--output", "-o", type=str)
    run_mode.add_argument(
        "--max_length", type=non_negative_int, default=DEFAULT_MAX_LENGTH
    )
    run_mode.add_argument(
        "--min_length", type=non_negative_int, default=DEFAULT_MIN_LENGTH
    )
    run_mode_support = run_mode.add_mutually_exclusive_group(required=True)
    run_mode_support.add_argument("--min_sup", type=non_negative_int)
    run_mode_support.add_argument("--min_sup_percentage", type=probability_float)
    run_mode.set_defaults(func=ModeMapper.run)

    # test mode
    test_mode = modes.add_parser("test")
    test_mode.add_argument("--input", "-i", type=str, required=True)
    test_mode.add_argument(
        "--max_length", type=non_negative_int, default=DEFAULT_MAX_LENGTH
    )
    test_mode.add_argument(
        "--min_length", type=non_negative_int, default=DEFAULT_MIN_LENGTH
    )
    test_mode_support = test_mode.add_mutually_exclusive_group(required=True)
    test_mode_support.add_argument("--min_sup", type=non_negative_int)
    test_mode_support.add_argument("--min_sup_percentage", type=probability_float)
    test_mode.add_argument("--iterations", "-it", type=non_negative_int, default=1)
    test_mode.set_defaults(func=ModeMapper.test)

    args = parser.parse_args()
    args.func(args)
