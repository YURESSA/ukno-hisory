from datetime import timedelta

from fastapi import HTTPException, status

from app.core.config import settings
from app.core.security import create_access_token, decode_token, verify_password
from app.modules.users.models import UserRole


class MonitoringService:
    def __init__(self, user_repo=None):
        self.user_repo = user_repo

    async def authenticate_admin(self, email: str, password: str):
        if self.user_repo is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Хранилище пользователей не настроено",
            )

        user = await self.user_repo.get_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            return None

        role = UserRole.normalize(user.role)
        if role not in {UserRole.ADMIN.value, UserRole.SUPERADMIN.value}:
            return None

        return user

    def create_grafana_session_token(self, user) -> str:
        role = UserRole.normalize(user.role)
        if role not in {UserRole.ADMIN.value, UserRole.SUPERADMIN.value}:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав",
            )

        return create_access_token(
            data={
                "sub": str(user.id),
                "role": role,
                "email": user.email,
                "type": "grafana_session",
            },
            expires_delta=timedelta(minutes=settings.GRAFANA_SESSION_EXPIRE_MINUTES),
        )

    def validate_grafana_session_token(self, token: str) -> dict:
        payload = decode_token(token)

        if payload.get("type") != "grafana_session":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Недействительная Grafana-сессия",
            )

        role = UserRole.normalize(payload.get("role", ""))
        if role not in {UserRole.ADMIN.value, UserRole.SUPERADMIN.value}:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав",
            )

        return payload
