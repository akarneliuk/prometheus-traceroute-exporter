# (c)2022, Karneliuk.com
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
        os.environ["TRACEROUTE_TARGETS"] = re.sub(r'^\s+(\S+)$', r'\1', args.targets)

    return args


def get_targets() -> list:
    try:
        return os.getenv("TRACEROUTE_TARGETS").split(",")

    except:
        return None


def start_exporter(exporter, is_once: bool = False, exporter_port: int = 9101, measure_interval: int = 60) -> None:
    ## Non-exporter mode: Test run of traceroutes to test reachability
    if is_once:
        measurements = exporter.run()
        print(measurements)

    ## Exporter mode
    else:
        start_http_server(port=exporter_port)

        while True:
            time_start = time.time()
            measurements = exporter.run()

            for measurement in measurements:
                try:
                    exported_metrics.labels(measurement[0]).set(value=measurement[1])
                    collection_duration.set(value=(time.time() - time_start))

                except (KeyError, UnboundLocalError):
                    ## Add traceroute counts
                    exported_metrics = Gauge("traceroute_hop_count", "number of hops towards destination host", ["target"])
                    exported_metrics.labels(measurement[0]).set(value=measurement[1])

                    ## Add traceroute collection duration
                    collection_duration = Gauge("traceroute_duration_seconds", "duration of the collection of all traceroutes")
                    collection_duration.set(value=(time.time() - time_start))

            time_sleep = time_start + measure_interval - time.time()

            if time_sleep > 0:
                time.sleep(time_sleep)