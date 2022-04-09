#!/usr/bin/env python

# Local artefacts
from bin.traceroute import TracerouteCollecter
import bin.helper_functions as hf


# Body
if __name__ == "__main__":
    ## Get instruction
    args = hf.get_instructions()

    ## Create traceroute collector
    tracerouter = TracerouteCollecter()
    
    ## Start exporter
    hf.start_exporter(exporter=tracerouter, is_once=args.once)


