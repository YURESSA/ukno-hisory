from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.api.v1.router import router as api_v1_router
from app.common.object_storage import image_url
from app.core.config import settings
from app.core.exception_handlers import (
    unhandled_exception_handler,
    validation_exception_handler,
)
from app.core.logging import attach_request_id, configure_logging
from app.core.monitoring import collect_http_metrics

configure_logging()

upload_dir = settings.upload_dir_path
if settings.STORAGE_BACKEND == "local":
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

if settings.STORAGE_BACKEND == "s3":

    @app.get(f"{settings.UPLOAD_URL_PREFIX}/{{path:path}}", include_in_schema=False)
    async def s3_upload(path: str):
        try:
            url = image_url(path)
        except ValueError:
            raise HTTPException(status_code=404, detail="Файл не найден") from None
        return RedirectResponse(
            url, status_code=307, headers={"Cache-Control": "no-store"}
        )

else:
    app.mount(
        settings.UPLOAD_URL_PREFIX, StaticFiles(directory=upload_dir), name="uploads"
    )
app.middleware("http")(collect_http_metrics)
app.middleware("http")(attach_request_id)
app.include_router(api_v1_router, prefix="/api/v1")
