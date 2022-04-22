#!/usr/bin/env python
# (c)2022, Karneliuk.com
# Modules
import logging


# Local artefacts
import bin.helper_functions as hf
from bin.static_exporter import StaticTargetExporter
from bin.dynamic_exporter import DynamicTargetExporter


# Variables
exporter_port = 9089
path_default_page = "./templates/index.j2"


# Logger
logging.basicConfig(format="%(asctime)s %(message)s")
log = logging.getLogger(__name__)


# Body
if __name__ == "__main__":
    # Get instruction
    args = hf.get_instructions()

    # Start Prometheus exporter
    if args.dynamic:
        exporter = DynamicTargetExporter(args=args, application_port=exporter_port,
                                         path_default_page=path_default_page)

    else:
        exporter = StaticTargetExporter(args=args, application_port=exporter_port,
                                        path_default_page=path_default_page)

    exporter.start()
