from fastapi import HTTPException, status

from app.common.utils.generate_password import generate_password
from app.core.mailer import send_email
from app.core.security import (
    create_access_token,
    create_reset_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.modules.users.models import User, UserRole


class UserService:
    def __init__(self, repo):
        self.repo = repo

    async def create_admin(self, email: str):
        password = generate_password()

        user = User(
            email=email,
            password_hash=hash_password(password),
            role=UserRole.ADMIN,
        )

        user = await self.repo.create(user)

        await send_email(
            to=email,
            subject="Вы добавлены как администратор",
            body=f"""
    Вы были добавлены как администратор.

    Email: {email}
    Пароль: {password}

    Рекомендуем сменить пароль после входа.
                """,
        )

        return user

    async def create_super_admin(self, email: str, password: str):
        user = User(
            email=email,
            password_hash=hash_password(password),
            role=UserRole.SUPERADMIN,
        )

        user = await self.repo.create(user)

        await send_email(
            to=email,
            subject="Вы добавлены как супер-администратор",
            body=f"""
    Вы были добавлены как супер-администратор.

    Email: {email}
    Пароль: {password}

    Рекомендуем сменить пароль после входа.
                """,
        )

        return user

    async def authenticate(self, email: str, password: str):
        user = await self.repo.get_by_email(email)

        if not user or not verify_password(password, user.password_hash):
            return None

        return user

    def create_token(self, user):
        return create_access_token(
            data={
                "sub": str(user.id),
                "role": UserRole.normalize(user.role),
            }
        )

    async def get_users(self):
        return await self.repo.get_all()

    async def get_user(self, user_id: int):
        user = await self.repo.get_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден",
            )

        return user

    async def change_password(self, current_user, old_password: str, new_password: str):
        if not verify_password(old_password, current_user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Неверный текущий пароль",
            )

        current_user.password_hash = hash_password(new_password)
        await self.repo.session.commit()

    async def request_password_reset(self, email: str):
        user = await self.repo.get_by_email(email)

        if not user:
            return

        token = create_reset_token(user.id)

        reset_link = f"http://localhost:8000/reset-password?token={token}"

        await send_email(
            to=email,
            subject="Сброс пароля",
            body=f"""
    Перейдите по ссылке для сброса пароля:

    {reset_link}

    Ссылка действует 30 минут.
            """,
        )

    async def confirm_password_reset(self, token: str, new_password: str):
        payload = decode_token(token)

        if not payload:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Недействительный или истёкший токен",
            )

        if payload.get("type") != "password_reset":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Неверный тип токена",
            )

        user_id = int(payload.get("sub"))

        user = await self.repo.get_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден",
            )

        user.password_hash = hash_password(new_password)
        await self.repo.session.commit()

    async def admin_change_password(
        self, current_user, target_user_id: int, new_password: str
    ):
        if UserRole.normalize(current_user.role) != UserRole.SUPERADMIN.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Только супер-администратор может менять чужие пароли",
            )

        target = await self.repo.get_by_id(target_user_id)

        if not target:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден",
            )

        target.password_hash = hash_password(new_password)
        await self.repo.session.commit()

    async def delete_user(self, current_user, target_user_id: int):
        target = await self.repo.get_by_id(target_user_id)

        if not target:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден",
            )

        if (
            current_user.id == target.id
            and UserRole.normalize(current_user.role) == UserRole.SUPERADMIN.value
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Супер-администратор не может удалить сам себя",
            )

        if (
            UserRole.normalize(current_user.role) == UserRole.ADMIN.value
            and current_user.id != target.id
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Администратор может удалить только себя",
            )

        await self.repo.delete(target)

    async def transfer_superadmin(self, current_user, target_user_id: int):
        if UserRole.normalize(current_user.role) != UserRole.SUPERADMIN.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Только супер-администратор может передать права",
            )

        target = await self.repo.get_by_id(target_user_id)

        if not target:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден",
            )

        target.role = UserRole.SUPERADMIN.value
        current_user.role = UserRole.ADMIN.value

        await self.repo.session.commit()
