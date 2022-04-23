# Pure Python Traceroute Exporter for Prometheus
This repostitory contains Python implementation of the traceroute exproter for Prometheus. The exporter operate in two modes:
- static targets exporter
- dynamic targets exporter

Static targets exporter is a default way for operation.

## Usage
### Static Targets Exporter
#### Description
In this mode you define which targets (i.e., destinations for traceroute) shall be monitored at the moment you start exporter. You define them using arguments together with some other optional parameters:
- targets to run traceroute against (e.g., `--targets=karneliuk.com,github.com,nokia.com`). There is no default value.
- polling interval (e.g., `--interval=30`). The default value is `60`.
- number of threads needed for threaded execution (e.g., `--workers=5`). The default value is `10`.

To collect the values, the value from such an exporter working in a such a mode, add the following configuration to your `prometheus.yaml` file:
```
---
global:
  scrape_interval: 1m
  scrape_timeout: 20s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'prometheus-traceroute-exporter'
    honor_labels: true
    static_configs:
      - targets:
        - 192.168.51.72:9101
...
```

Such mode may be useful, if you want to collect information from an exporter to multiple Prometheus. To a degree, the operation is like a combination of traceroute script with a Prometheus Pushgateway with as an exception, that you don't need to setup separate Pushgateway.

#### Docker-compose file
The following `docker-compose.yaml` shall be used for a static targets exporter:
```
---
version: "3.9"
services:
  traceroute_exporter:
    image: "ghcr.io/akarneliuk/traceroute-exporter:${PLATFORM}"
    privileged: true
    healthcheck:
      test:
        - "CMD"
        - "curl"
        - "-f"
        - "http://localhost:9101"
      interval: 1m
      timeout: 10s
      retries: 3
      start_period: 30s
    ports:
      - "9101:9101"
    command:
      - "--targets=karneliuk.com,github.com,nokia.com"
      - "--workers=5"
      - "--interval=30"
...
```

### Dynamic Targets Exporter
In this mode you define which targets (i.e., destinations for traceroute) shall be monitored at a Prometheus side. You just need to launch a Prometheus traceroute exporter in a dynamic mode using a single argument:
- `--dynamic`

To collect the values, the value from such an exporter working in a such a mode, add the following configuration to your `prometheus.yaml` file:
```
---
global:
  scrape_interval: 1m
  scrape_timeout: 20s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'prometheus-traceroute-exporter'
    metrics_path: /probe
    static_configs:
      - targets:
        - nokia.com
        - github.com
        - thghosting.com
    relabel_configs:
      - source_labels: [__address__]
        target_label: __param_target
      - source_labels: [__param_target]
        target_label: instance
      - target_label: __address__
        replacement: 192.168.51.72:9101
...
```

Such a mode is useful, if you want dynamically control the targets from the Prometheus instance to reduce the operational overhead. The user experience is similar to Prometheus own blackbox exporter, which is missing traceroute functionality.

#### Docker-compose file
The following `docker-compose.yaml` shall be used for a static targets exporter:
```
---
version: "3.9"
services:
  traceroute_exporter:
    image: "ghcr.io/akarneliuk/traceroute-exporter:${PLATFORM}"
    privileged: true
    healthcheck:
      test:
        - "CMD"
        - "curl"
        - "-f"
        - "http://localhost:9101"
      interval: 1m
      timeout: 10s
      retries: 3
      start_period: 30s
    ports:
      - "9101:9101"
    command:
      - "--dynamic"
...
```

## Docker Image
You can pull the pre-build image of the Python tracroute exporter for Prometheus from the GitHub Container Registry (`x86_64` and `armv7l` ):
```
docker pull ghcr.io/akarneliuk/traceroute-exporter:$(uname -m)
```

Once pulled, launch it in the background as:
```
docker container run -d -p 9101:9101 --privileged ghcr.io/akarneliuk/traceroute-exporter:$(uname -m) --targets=xxx1,xxx2
```
where `xxx1` and `xxx2` are the IP addresses or FQDNs of the target nodes

Alternatievly, as described above, launch the provided `docker-compose` file incorporating system architecture type (see example attached):
```
PLATFORM=$(uname -m) docker-compose up -d
```

## More details
This repository supports our blog [Karneliuk.com](https://karneliuk.com). Find the corresponding blogposts explaing these files.

## Want to be Automation Expert?
[Enroll to our Zero-To-Hero Network Automation Training](https://training.karneliuk.com/forms/). Study in online groups or in a self-paced mode.

## Need Help?
[Contact us](https://karneliuk.com/contact/) with your request and we will find the most suitable solution for you.

(c)2022, Karneliuk.com