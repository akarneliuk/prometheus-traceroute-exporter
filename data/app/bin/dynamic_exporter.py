# (c)2022, Karneliuk.com
# Modules
from wsgiref.simple_server import make_server
from urllib.parse import parse_qs
from prometheus_client import make_wsgi_app
from prometheus_client.core import GaugeMetricFamily, REGISTRY
import icmplib
import os
import time
import logging
import jinja2


# Logger
logging.basicConfig(format="%(asctime)s %(message)s")
log = logging.getLogger(__name__)


# Classes
class CustomCollector(object):
    def collect(self):
        # Set target
        target = os.getenv("PROMETHEUS_TARGET") if os.getenv("PROMETHEUS_TARGET") else "localhost"

        # Perfrom measurement
        try:
            timestamp_start = time.time()
            measured_hops = len(icmplib.traceroute(target))
            timestamp_finish = time.time()
            is_successfull = 1

        except icmplib.exceptions.NameLookupError:
            timestamp_finish = time.time()
            measured_hops = 0
            is_successfull = 0

        # Report metrics
        yield GaugeMetricFamily("probe_success",
                                "Result of the probe execution",
                                is_successfull)

        yield GaugeMetricFamily("probe_traceroute_hops_amount",
                                "Amount of hops towards destination host",
                                measured_hops)

        yield GaugeMetricFamily("probe_execution_duration_seconds",
                                "Duration of the measurement",
                                timestamp_finish - timestamp_start)


class DynamicTargetExporter(object):
    def __init__(self, args, application_port: int, path_default_page: str):
        self._args = args
        self._application_port = application_port
        self._path_default_page = path_default_page

        # Prometheus metrics
        self._metrics_app = make_wsgi_app()
        REGISTRY.register(CustomCollector())

    def start(self):
        # WSGI server
        httpd = make_server("", self._application_port, self._middleware_wsgi)
        httpd.serve_forever()

    def _middleware_wsgi(self, environ, start_response):
        if environ["PATH_INFO"] == "/probe":
            query_parameters = parse_qs(environ["QUERY_STRING"])

            if query_parameters:
                try:
                    os.environ["PROMETHEUS_TARGET"] = query_parameters["target"][0]

                except (IndexError, KeyError) as e:
                    print(f"Failed to identify target: {e}. Using 'localhost' as destination.")
                    os.environ["PROMETHEUS_TARGET"] = "localhost"

            return self._metrics_app(environ, start_response)

        template = jinja2.Template(open(self._path_default_page, "r").read())
        rendered_page = template.render(args=self._args)

        response_body = str.encode(rendered_page)

        response_status = "200 OK"
        response_headers = [
            ('Content-Type', 'text/html'),
            ('Content-Length', str(len(response_body)))
        ]

        start_response(response_status, response_headers)
        return [response_body]
