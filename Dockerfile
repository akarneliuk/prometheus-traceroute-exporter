FROM python:alpine

LABEL MAINTAINER="anton@karneliuk.com"
LABEL GITHUB="https://github.com/akarneliuk/prometheus-traceroute-exporter.git"

# Install packages
RUN apk update && apk add curl

# Install dependencies
COPY data/requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

# Copy app
RUN mkdir /etc/traceroute-exporter
COPY data/app /etc/traceroute-exporter

# Run app
WORKDIR /etc/traceroute-exporter
EXPOSE 9101
ENTRYPOINT ["python3", "main.py"]