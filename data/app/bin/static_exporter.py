# (c)2022, Karneliuk.com

# Local artefacts
from bin.traceroute import TracerouteCollecter
import logging
from prometheus_client import start_http_server, Gauge
import time


# Logger
logging.basicConfig(format="%(asctime)s %(message)s")
log = logging.getLogger(__name__)


# Classes
class StaticTargetExporter(object):
    def __init__(self, args, application_port: int, path_default_page: str):
        self._args = args
        self._application_port = application_port
        self._path_default_page = path_default_page

        # Static vars
        self._measure_interval: int = 60

        # Create traceroute collector
        self._tracerouter = TracerouteCollecter(workers=args.workers)

    def start(self):
        self._exporter_logic()

    def _exporter_logic(self):
        # Non-exporter mode: Test run of traceroutes to test reachability
        if self._args.once:
            measurements = self._tracerouter.run()
            log.info(measurements)

        # Exporter mode
        else:
            start_http_server(port=self._application_port)

            while True:
                time_start = time.time()
                measurements = self._tracerouter.run()

                for measurement in measurements:
                    try:
                        exported_metrics.labels(measurement[0]).set(value=measurement[1])
                        collection_duration.set(value=(time.time() - time_start))

                    except (KeyError, UnboundLocalError):
                        # Add traceroute counts
                        exported_metrics = Gauge("traceroute_hop_count",
                                                 "number of hops towards destination host",
                                                 ["target"])
                        exported_metrics.labels(measurement[0]).set(value=measurement[1])

                        # Add traceroute collection duration
                        collection_duration = Gauge("traceroute_duration_seconds",
                                                    "duration of the collection of all traceroutes")
                        collection_duration.set(value=(time.time() - time_start))

                time_sleep = time_start + self._measure_interval - time.time()

                if time_sleep > 0:
                    log.info(f"Sleeping for {time_sleep} till next measurement.")
                    time.sleep(time_sleep)
