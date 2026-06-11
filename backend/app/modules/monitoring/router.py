from fastapi import APIRouter, Depends, Form, Request, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse

from app.core.database import get_db
from app.core.dependencies import require_admin
from app.core.monitoring import build_metrics_response
from app.modules.monitoring.schemas import GrafanaSessionRead
from app.modules.monitoring.service import MonitoringService
from app.modules.users.repository import UserRepository

router = APIRouter()

GRAFANA_SESSION_COOKIE = "grafana_session"
DEFAULT_GRAFANA_PATH = "/grafana/"


def get_service(db=Depends(get_db)):
    return MonitoringService(UserRepository(db))


def _build_grafana_login_html(*, next_url: str, error: str | None = None) -> str:
    error_block = (
        f'<p style="color:#b42318;margin:0 0 16px;">{error}</p>' if error else ""
    )
    return f"""<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Вход в Grafana</title>
  <style>
    body {{
      margin: 0;
      min-height: 100vh;
      display: grid;
      place-items: center;
      font-family: Arial, sans-serif;
      background: linear-gradient(135deg, #111827, #1f2937);
      color: #111827;
    }}
    .card {{
      width: min(420px, calc(100vw - 32px));
      background: #fff;
      border-radius: 16px;
      padding: 32px;
      box-shadow: 0 20px 60px rgba(0, 0, 0, 0.25);
    }}
    h1 {{
      margin: 0 0 12px;
      font-size: 28px;
    }}
    p {{
      margin: 0 0 24px;
      color: #4b5563;
    }}
    label {{
      display: block;
      margin-bottom: 8px;
      font-size: 14px;
      font-weight: 600;
    }}
    input {{
      width: 100%;
      box-sizing: border-box;
      border: 1px solid #d1d5db;
      border-radius: 10px;
      padding: 12px 14px;
      margin-bottom: 16px;
      font-size: 16px;
    }}
    button {{
      width: 100%;
      border: 0;
      border-radius: 10px;
      background: #111827;
      color: #fff;
      padding: 12px 16px;
      font-size: 16px;
      cursor: pointer;
    }}
  </style>
</head>
<body>
  <div class="card">
    <h1>Вход в Grafana</h1>
    <p>Доступ открыт только для администратора или суперадмина.</p>
    {error_block}
    <form method="post" action="/api/v1/monitoring/grafana/login">
      <input type="hidden" name="next_url" value="{next_url}">
      <label for="email">Email</label>
      <input id="email" name="email" type="email" autocomplete="username" required>
      <label for="password">Пароль</label>
      <input
        id="password"
        name="password"
        type="password"
        autocomplete="current-password"
        required
      >
      <button type="submit">Войти в Grafana</button>
    </form>
  </div>
</body>
</html>"""


@router.get(
    "/metrics",
    include_in_schema=False,
)
async def get_metrics():
    return build_metrics_response()


@router.get(
    "/grafana/login",
    response_class=HTMLResponse,
    include_in_schema=False,
)
async def grafana_login_page(
    next_url: str = DEFAULT_GRAFANA_PATH,
    error: str | None = None,
):
    return HTMLResponse(
        _build_grafana_login_html(
            next_url=next_url or DEFAULT_GRAFANA_PATH,
            error=error,
        )
    )


@router.post(
    "/grafana/login",
    include_in_schema=False,
)
async def grafana_login_submit(
    response: Response,
    service=Depends(get_service),
    email: str = Form(...),
    password: str = Form(...),
    next_url: str = Form(DEFAULT_GRAFANA_PATH),
):
    user = await service.authenticate_admin(email=email, password=password)
    if user is None:
        return HTMLResponse(
            _build_grafana_login_html(
                next_url=next_url or DEFAULT_GRAFANA_PATH,
                error="Неверные учетные данные или недостаточно прав.",
            ),
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    redirect = RedirectResponse(
        url=next_url or DEFAULT_GRAFANA_PATH,
        status_code=status.HTTP_303_SEE_OTHER,
    )
    token = service.create_grafana_session_token(user)
    redirect.set_cookie(
        key=GRAFANA_SESSION_COOKIE,
        value=token,
        max_age=60 * 60 * 8,
        httponly=True,
        samesite="lax",
        secure=True,
        path="/grafana",
    )
    return redirect


@router.post(
    "/grafana/session",
    response_model=GrafanaSessionRead,
    status_code=status.HTTP_200_OK,
    summary="Создать Grafana-сессию для администратора",
)
async def create_grafana_session(
    response: Response,
    service=Depends(get_service),
    user=Depends(require_admin),
):
    token = service.create_grafana_session_token(user)
    response.set_cookie(
        key=GRAFANA_SESSION_COOKIE,
        value=token,
        max_age=60 * 60 * 8,
        httponly=True,
        samesite="lax",
        secure=True,
        path="/grafana",
    )
    return GrafanaSessionRead(grafana_url="/grafana/")


@router.delete(
    "/grafana/session",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Завершить Grafana-сессию",
)
async def delete_grafana_session(response: Response):
    response.delete_cookie(
        key=GRAFANA_SESSION_COOKIE,
        path="/grafana",
    )


@router.get(
    "/grafana/auth",
    include_in_schema=False,
)
async def grafana_auth(
    request: Request,
    response: Response,
    service=Depends(get_service),
):
    token = request.cookies.get(GRAFANA_SESSION_COOKIE)
    if not token:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return

    payload = service.validate_grafana_session_token(token)
    response.status_code = status.HTTP_204_NO_CONTENT
    response.headers["X-Grafana-User"] = str(payload["sub"])
    response.headers["X-Grafana-Email"] = str(payload.get("email", ""))
