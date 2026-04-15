from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.core.database import get_db
from app.modules.users.repository import UserRepository
from app.modules.users.service import UserService

router = APIRouter()


def get_service(db=Depends(get_db)):
    return UserService(UserRepository(db))


@router.post("/login")
async def login(
    form: OAuth2PasswordRequestForm = Depends(),
    service=Depends(get_service),
):
    user = await service.authenticate(form.username, form.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = service.create_token(user)

    return {
        "access_token": token,
        "token_type": "bearer",
    }
