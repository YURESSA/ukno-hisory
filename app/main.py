from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.v1.router import router as api_v1_router
from app.core.config import settings
from app.core.exception_handlers import (
    unhandled_exception_handler,
    validation_exception_handler,
)
from app.core.logging import attach_request_id, configure_logging

configure_logging()

upload_dir = settings.upload_dir_path
upload_dir.mkdir(parents=True, exist_ok=True)

app = FastAPI(
    title="Исторический API",
    swagger_ui_init_oauth={
        "usePkceWithAuthorizationCodeGrant": True,
    },
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

app.mount(
    settings.UPLOAD_URL_PREFIX,
    StaticFiles(directory=upload_dir),
    name="uploads",
)
app.middleware("http")(attach_request_id)
app.include_router(api_v1_router, prefix="/api/v1")
