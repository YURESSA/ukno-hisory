from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.v1.router import router as api_v1_router
from app.core.config import settings
from app.core.logging import configure_logging, log_request

configure_logging()

upload_dir = settings.upload_dir_path
upload_dir.mkdir(parents=True, exist_ok=True)

app = FastAPI(
    title="History API",
    swagger_ui_init_oauth={
        "usePkceWithAuthorizationCodeGrant": True,
    },
)

app.mount(
    settings.UPLOAD_URL_PREFIX,
    StaticFiles(directory=upload_dir),
    name="uploads",
)
app.middleware("http")(log_request)
app.include_router(api_v1_router, prefix="/api/v1")
