from fastapi import APIRouter, Depends, HTTPException, status

from app.core.database import get_db
from app.core.dependencies import require_admin, require_superadmin
from app.modules.users.repository import UserRepository
from app.modules.users.schemas import (
    AdminChangePasswordRequest,
    ChangePasswordRequest,
    ConfirmResetPassword,
    LoginRequest,
    ResetPasswordRequest,
    UserCreate,
    UserRead,
)
from app.modules.users.service import UserService

router = APIRouter()


def get_service(db=Depends(get_db)):
    return UserService(UserRepository(db))


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    data: LoginRequest,
    service=Depends(get_service),
):
    user = await service.authenticate(data.email, data.password)

    if not user:
        raise HTTPException(status_code=401, detail="Неверный email или пароль")

    return {
        "access_token": service.create_token(user),
        "token_type": "bearer",
    }


@router.post(
    "/create-admin", response_model=UserRead, status_code=status.HTTP_201_CREATED
)
async def create_admin(
    data: UserCreate,
    service=Depends(get_service),
    _: None = Depends(require_superadmin),
):
    return await service.create_admin(data.email)


@router.get("/users", response_model=list[UserRead], status_code=status.HTTP_200_OK)
async def get_users(
    service=Depends(get_service),
    _: None = Depends(require_admin),
):
    return await service.get_users()


@router.delete("/users/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(
    user_id: int,
    service=Depends(get_service),
    current_user=Depends(require_admin),
):
    await service.delete_user(current_user, user_id)
    return {"detail": "User deleted"}


@router.get("/users/{user_id}", response_model=UserRead)
async def get_user(
    user_id: int,
    service=Depends(get_service),
    _: None = Depends(require_admin),
):
    return await service.get_user(user_id)


@router.post("/change-password", status_code=status.HTTP_200_OK)
async def change_password(
    data: ChangePasswordRequest,
    service=Depends(get_service),
    current_user=Depends(require_admin),
):
    await service.change_password(
        current_user,
        data.old_password,
        data.new_password,
    )
    return {"detail": "Пароль успешно изменён"}


@router.post("/request-password-reset", status_code=status.HTTP_200_OK)
async def request_password_reset(
    data: ResetPasswordRequest,
    service=Depends(get_service),
):
    await service.request_password_reset(data.email)
    return {"detail": "Если пользователь существует, письмо отправлено"}


@router.post("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(
    data: ConfirmResetPassword,
    service=Depends(get_service),
):
    await service.confirm_password_reset(data.token, data.new_password)
    return {"detail": "Пароль успешно сброшен"}


@router.post("/users/{user_id}/change-password", status_code=status.HTTP_200_OK)
async def admin_change_password(
    user_id: int,
    data: AdminChangePasswordRequest,
    service=Depends(get_service),
    current_user=Depends(require_superadmin),
):
    await service.admin_change_password(current_user, user_id, data.new_password)
    return {"detail": "Пароль пользователя обновлён"}


@router.post("/transfer-superadmin/{user_id}", status_code=status.HTTP_200_OK)
async def transfer_superadmin(
    user_id: int,
    service=Depends(get_service),
    current_user=Depends(require_superadmin),
):
    await service.transfer_superadmin(current_user, user_id)
    return {"detail": "Права супер-администратора переданы"}
