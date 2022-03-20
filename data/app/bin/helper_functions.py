# Modules
from argparse import ArgumentParser
import json
import sys


# Functions
def get_instructions():
    parser = ArgumentParser()

    parser.add_argument(
        "-d", "--dev",
        action="store_true",
        default=False,
        help="Test execution with predefined test data.",
    )

    parser.add_argument(
        "-t", "--targets",
        type=str,
        required=False,
        help="Comma-separted list of targets to run tracroute against.",
    )

    args = parser.parse_args()

    if args.targets:
        args.targets = args.targets.split(",")

    return args


def load_targets(path: str) -> list:
    try:
        return json.loads(open(file=path, mode="r").read())

    except:
        return None


def get_targets(args) -> list:
    if args.dev and args.targets:
        sys.exit("Too many arguments specified. Choose either '-t' or '-d'.")

    elif args.dev:
        return load_targets(path="./input/test_data.json")

    elif args.targets:
        return args.targets

    else:
        raise NotImplementedError