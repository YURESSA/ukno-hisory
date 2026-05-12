import argparse
import asyncio

from app.core.database import AsyncSessionLocal
from app.modules.users.repository import UserRepository
from app.modules.users.service import UserService


async def create_superadmin(email: str, password: str):
    async with AsyncSessionLocal() as db:
        repo = UserRepository(db)
        service = UserService(repo)

        existing = await repo.get_by_email(email)
        if existing:
            print("User already exists")
            return

        await service.create_super_admin(email=email, password=password)

        print("Superadmin created")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--email", required=True)
    parser.add_argument("--password", required=True)

    args = parser.parse_args()

    asyncio.run(create_superadmin(args.email, args.password))
