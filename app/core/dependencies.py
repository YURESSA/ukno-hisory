from fastapi import Depends, HTTPException
from jose import jwt

from app.core.database import get_db
from app.core.security import ALGORITHM, SECRET_KEY, oauth2_scheme
from app.modules.users.models import UserRole
from app.modules.users.repository import UserRepository


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db=Depends(get_db),
):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    repo = UserRepository(db)
    user = await repo.get_by_id(int(user_id))

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


def require_role(*roles: UserRole):
    allowed_roles = {UserRole.normalize(role) for role in roles}

    def wrapper(user=Depends(get_current_user)):
        if UserRole.normalize(user.role) not in allowed_roles:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user

    return wrapper


require_admin = require_role(UserRole.ADMIN, UserRole.SUPERADMIN)
require_superadmin = require_role(UserRole.SUPERADMIN)
