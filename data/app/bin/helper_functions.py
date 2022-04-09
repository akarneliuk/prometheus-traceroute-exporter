# Modules
from argparse import ArgumentParser
import re
import os
from prometheus_client import start_http_server, Gauge
import time


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

    parser.add_argument(
        "-o", "--once",
        action="store_true",
        default=False,
        help="Specify if you want to run the execution once.",
    )

    args = parser.parse_args()

    if args.targets:
        os.environ["TRACEROUTE_TARGETS"] = args.targets

    return args


def get_targets() -> list:
    try:
        return os.getenv("TRACEROUTE_TARGETS").split(",")

    except:
        return None


def start_exporter(exporter, is_once: bool = False, exporter_port: int = 9101, measure_interval: int = 60) -> None:
    ## Convert seconds to nanoseconds
    measure_interval *= 100000000

    ## Non-exporter mode: Test run of traceroutes to test reachability
    if is_once:
        measurements = exporter.run()
        print(measurements)

    ## Exporter mode
    else:
        start_http_server(port=exporter_port)

        while True:
            time_start = time.time_ns()
            measurements = exporter.run()

            for measurement in measurements:
                try:
                    exported_metrics.labels(measurement[0]).set(value=measurement[1])

                except (KeyError, UnboundLocalError):
                    exported_metrics = Gauge("target_hop_counts", "number of hops towards destination host", ["target"])
                    exported_metrics.labels(measurement[0]).set(value=measurement[1])

            time_sleep = time_start + measure_interval - time.time_ns()

            if time_sleep > 0:
                time.sleep(time_sleep)