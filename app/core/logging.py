import json
import logging
import time
from contextvars import ContextVar
from datetime import UTC, datetime
from uuid import uuid4

from fastapi import Request

from app.core.config import settings

request_id_context: ContextVar[str | None] = ContextVar(
    "request_id",
    default=None,
)


class RequestContextFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id_context.get()
        return True


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, object] = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "request_id": getattr(record, "request_id", None),
        }

        for field in (
            "method",
            "path",
            "query_string",
            "route",
            "status_code",
            "duration_ms",
            "client_ip",
        ):
            value = getattr(record, field, None)
            if value is not None:
                payload[field] = value

        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)

        return json.dumps(payload, ensure_ascii=False)


def configure_logging() -> None:
    root_logger = logging.getLogger()
    level_name = settings.LOG_LEVEL.upper()
    level = getattr(logging, level_name, logging.INFO)

    handler = logging.StreamHandler()
    handler.addFilter(RequestContextFilter())
    if settings.LOG_JSON:
        handler.setFormatter(JsonFormatter())
    else:
        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s %(levelname)s %(name)s [request_id=%(request_id)s] "
                "%(message)s"
            )
        )

    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(level)

    for logger_name in ("uvicorn", "uvicorn.error", "uvicorn.access", "gunicorn.error"):
        logger = logging.getLogger(logger_name)
        logger.handlers.clear()
        logger.propagate = True
        logger.setLevel(level)


async def log_request(request: Request, call_next):
    logger = logging.getLogger("app.request")
    request_id = request.headers.get("X-Request-ID") or uuid4().hex
    request.state.request_id = request_id
    token = request_id_context.set(request_id)
    started_at = time.perf_counter()

    try:
        response = await call_next(request)
    except Exception:
        duration_ms = round((time.perf_counter() - started_at) * 1000, 2)
        logger.exception(
            "Request failed",
            extra=_build_request_log_context(
                request=request,
                status_code=500,
                duration_ms=duration_ms,
            ),
        )
        raise
    else:
        duration_ms = round((time.perf_counter() - started_at) * 1000, 2)
        response.headers["X-Request-ID"] = request_id
        logger.info(
            "Request completed",
            extra=_build_request_log_context(
                request=request,
                status_code=response.status_code,
                duration_ms=duration_ms,
            ),
        )
        return response
    finally:
        request_id_context.reset(token)


def _build_request_log_context(
    *,
    request: Request,
    status_code: int,
    duration_ms: float,
) -> dict[str, object]:
    route = request.scope.get("route")
    path = request.url.path
    if settings.LOG_INCLUDE_QUERY_STRING and request.url.query:
        query_string = request.url.query
    else:
        query_string = None

    return {
        "method": request.method,
        "path": path,
        "query_string": query_string,
        "route": getattr(route, "path", path),
        "status_code": status_code,
        "duration_ms": duration_ms,
        "client_ip": request.client.host if request.client else None,
    }
