#!/usr/bin/env

# Modules


# Local artefacts
from bin.traceroute import TracerouteCollecter
import bin.helper_functions as hf


# Body
if __name__ == "__main__":
    ## Get instruction
    args = hf.get_instructions()

    ## Get targets
    targets = hf.get_targets(args=args)

    ## Perform measurements
    if targets:
        tracerouter = TracerouteCollecter(targets=targets)
        measurements = tracerouter.run()

        print(measurements)


