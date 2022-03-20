# Pure Python Traceroute Exporter for Prometheus
This repostitory contains Python implementation of the traceroute exproter for Prometheus.

## Docker Image
You can pull the pre-build image of the Python tracroute exporter for Prometheus from:
```
docker pull akarneliuk/prometheus-traceroute-exporter:latest
```

Once pulled, launch it in the background as:
```
docker container run -d -p 9016:9016 akarneliuk/prometheus-traceroute-exporter:latest -s
```

Alternatievly, launch the provided `docker-compose` file:
```
docker-compose up -d
```

## More details
This repository supports our blog [Karneliuk.com](https://karneliuk.com). Find the corresponding blogposts explaing these files.

## Want to be Automation Expert?
[Enroll to our Zero-To-Hero Network Automation Training](https://training.karneliuk.com/forms/). Study in online groups or in a self-paced mode.

## Need Help?
[Contact us](https://karneliuk.com/contact/) with your request and we will find the most suitable solution for you.

(c)2022, Karneliuk.com