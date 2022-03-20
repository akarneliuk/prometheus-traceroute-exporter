# Modules
from concurrent.futures import ThreadPoolExecutor
import icmplib


# Classes
class TracerouteCollecter(object):
    def __init__(self, targets: list, workers: int = 10):
        self.targets = targets
        self.workers = workers


    def run(self) -> list:
        with ThreadPoolExecutor(max_workers=self.workers) as executor:
            results = executor.map(self._traceroute, self.targets)

        return [(entry[0], len(entry[1])) for entry in results]


    def _traceroute(self, target) -> tuple:
        return target, icmplib.traceroute(address=target, count=5)