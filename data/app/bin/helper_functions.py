# (c)2022, Karneliuk.com
# Modules
from argparse import ArgumentParser
import re
import os
import logging


# Logger
logging.basicConfig(format="%(asctime)s %(message)s")
log = logging.getLogger(__name__)


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
        "-D", "--dynamic",
        action="store_true",
        default=False,
        help="Start exporter in a mode retrieving targets from Prometheus.",
    )

    parser.add_argument(
        "-i", "--interval",
        type=int,
        default=60,
        required=False,
        help="Time interval between consequent measurements.",
    )

    parser.add_argument(
        "-o", "--once",
        action="store_true",
        default=False,
        help="Specify if you want to run the execution once.",
    )

    parser.add_argument(
        "-t", "--targets",
        type=str,
        required=False,
        help="Comma-separted list of targets to run tracroute against.",
    )

    parser.add_argument(
        "-w", "--workers",
        type=int,
        default=10,
        required=False,
        help="Amount of workers for threaded traceroute collector.",
    )

    args = parser.parse_args()

    if args.targets:
        os.environ["TRACEROUTE_TARGETS"] = re.sub(r'^\s+(\S+)$', r'\1',
                                                  args.targets)

    return args
