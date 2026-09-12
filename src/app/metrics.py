import time

import psutil
from flask import Response, request
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Gauge, generate_latest


# Application metrics
REQUEST_COUNT = Counter(
    "inframonitor_http_requests_total",
    "Total number of HTTP requests received by InfraMonitor",
    ["method", "endpoint", "status"],
)

REQUEST_LATENCY = Gauge(
    "inframonitor_http_request_latency_seconds",
    "Time taken to process the latest HTTP request",
)

CPU_USAGE = Gauge(
    "inframonitor_cpu_usage_percent",
    "Current CPU usage of the system in percent",
)

MEMORY_USAGE = Gauge(
    "inframonitor_memory_usage_percent",
    "Current memory usage of the system in percent",
)

DISK_USAGE = Gauge(
    "inframonitor_disk_usage_percent",
    "Current disk usage of the root filesystem in percent",
)

PROCESS_COUNT = Gauge(
    "inframonitor_process_count",
    "Number of running processes on the system",
)


def register_metrics(app):
    @app.before_request
    def start_timer():
        request.start_time = time.time()

    @app.after_request
    def record_request(response):
        elapsed = time.time() - request.start_time

        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.endpoint or "unknown",
            status=response.status_code,
        ).inc()

        REQUEST_LATENCY.set(elapsed)

        return response

    @app.route("/metrics")
    def metrics():
        CPU_USAGE.set(psutil.cpu_percent(interval=0.1))
        MEMORY_USAGE.set(psutil.virtual_memory().percent)
        DISK_USAGE.set(psutil.disk_usage("/").percent)
        PROCESS_COUNT.set(len(psutil.pids()))

        return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)
