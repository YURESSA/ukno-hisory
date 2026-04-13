from app.modules.users.repository import UserRepository


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def create_user(self, name: str):
        return await self.repo.create(name)

    async def get_users(self):
        return await self.repo.get_all()