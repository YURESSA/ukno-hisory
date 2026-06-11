from collections import defaultdict
from threading import Lock
from time import perf_counter

from fastapi import Request, Response

METRICS_CONTENT_TYPE = "text/plain; version=0.0.4; charset=utf-8"
LATENCY_BUCKETS = (0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0)

_metrics_lock = Lock()
_request_counts: dict[tuple[str, str, str], int] = defaultdict(int)
_request_duration_sums: dict[tuple[str, str], float] = defaultdict(float)
_request_duration_counts: dict[tuple[str, str], int] = defaultdict(int)
_request_duration_buckets: dict[tuple[str, str], dict[float, int]] = defaultdict(
    lambda: defaultdict(int)
)


def _escape_label(value: str) -> str:
    return value.replace("\\", "\\\\").replace("\n", "\\n").replace('"', '\\"')


def build_metrics_response() -> Response:
    with _metrics_lock:
        lines = [
            "# HELP http_requests_total Total HTTP requests",
            "# TYPE http_requests_total counter",
        ]
        for (method, path, status), value in sorted(_request_counts.items()):
            lines.append(
                'http_requests_total{method="%s",path="%s",status="%s"} %s'
                % (
                    _escape_label(method),
                    _escape_label(path),
                    _escape_label(status),
                    value,
                )
            )

        lines.extend(
            [
                "# HELP http_request_duration_seconds HTTP request latency in seconds",
                "# TYPE http_request_duration_seconds histogram",
            ]
        )
        for (method, path), sum_value in sorted(_request_duration_sums.items()):
            cumulative = 0
            for bucket in LATENCY_BUCKETS:
                cumulative += _request_duration_buckets[(method, path)][bucket]
                lines.append(
                    (
                        'http_request_duration_seconds_bucket{method="%s",'
                        'path="%s",le="%s"} %s'
                    )
                    % (
                        _escape_label(method),
                        _escape_label(path),
                        bucket,
                        cumulative,
                    )
                )

            count_value = _request_duration_counts[(method, path)]
            lines.append(
                (
                    'http_request_duration_seconds_bucket{method="%s",'
                    'path="%s",le="+Inf"} %s'
                )
                % (
                    _escape_label(method),
                    _escape_label(path),
                    count_value,
                )
            )
            lines.append(
                'http_request_duration_seconds_sum{method="%s",path="%s"} %.10f'
                % (
                    _escape_label(method),
                    _escape_label(path),
                    sum_value,
                )
            )
            lines.append(
                'http_request_duration_seconds_count{method="%s",path="%s"} %s'
                % (
                    _escape_label(method),
                    _escape_label(path),
                    count_value,
                )
            )

    return Response(
        content="\n".join(lines) + "\n",
        media_type=METRICS_CONTENT_TYPE,
    )


async def collect_http_metrics(request: Request, call_next):
    started_at = perf_counter()
    response = await call_next(request)
    duration = perf_counter() - started_at

    route = request.scope.get("route")
    path = getattr(route, "path", request.url.path)
    method = request.method
    status = str(response.status_code)

    with _metrics_lock:
        _request_counts[(method, path, status)] += 1
        _request_duration_sums[(method, path)] += duration
        _request_duration_counts[(method, path)] += 1
        for bucket in LATENCY_BUCKETS:
            if duration <= bucket:
                _request_duration_buckets[(method, path)][bucket] += 1

    return response
