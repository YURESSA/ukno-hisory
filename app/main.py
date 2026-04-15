from fastapi import FastAPI

from app.api.v1.router import router as api_v1_router

app = FastAPI(
    title="History API",
    swagger_ui_init_oauth={
        "usePkceWithAuthorizationCodeGrant": True,
    },
)

app.include_router(api_v1_router, prefix="/api/v1")
