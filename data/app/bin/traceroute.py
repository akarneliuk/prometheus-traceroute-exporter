# (c)2022, Karneliuk.com
# Modules
from concurrent.futures import ThreadPoolExecutor
import icmplib


# Local modules
import bin.helper_functions as hf


# Classes
class TracerouteCollecter(object):
    def __init__(self, workers: int = 10):
        self.workers = workers

    def run(self) -> list:
        # Get targets (done each measurement cycle)
        self.targets = hf.get_targets()

        # Run measurement in a threaded way
        with ThreadPoolExecutor(max_workers=self.workers) as executor:
            results = executor.map(self._traceroute, self.targets)

        return [(entry[0], len(entry[1])) for entry in results]

    def _traceroute(self, target) -> tuple:
        return target, icmplib.traceroute(address=target, count=5)
