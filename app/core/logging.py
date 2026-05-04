import logging
from uuid import uuid4

from fastapi import Request

from app.core.config import settings


def configure_logging() -> None:
    sql_log_level = logging.INFO if settings.LOG_SQL_QUERIES else logging.WARNING
    for logger_name in ("sqlalchemy.engine", "sqlalchemy.pool", "aiosqlite"):
        logging.getLogger(logger_name).setLevel(sql_log_level)


async def attach_request_id(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID") or uuid4().hex
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response
