import shutil
from collections.abc import AsyncIterator
from pathlib import Path
from uuid import uuid4

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from app.core.config import settings
from app.core.database import Base, get_db
from app.core.security import hash_password
from app.main import app
from app.modules.users.models import User, UserRole

TEST_DATABASE_URL = "sqlite+aiosqlite://"


@pytest.fixture(autouse=True)
def uploads_dir(monkeypatch: pytest.MonkeyPatch) -> Path:
    uploads_root = Path.cwd() / ".test_uploads"
    uploads_path = uploads_root / uuid4().hex
    uploads_path.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(settings, "UPLOAD_DIR", str(uploads_path))
    try:
        yield uploads_path
    finally:
        shutil.rmtree(uploads_path, ignore_errors=True)


@pytest_asyncio.fixture
async def sent_emails(monkeypatch: pytest.MonkeyPatch) -> list[dict[str, str]]:
    emails: list[dict[str, str]] = []

    async def fake_send_email(to: str, subject: str, body: str) -> None:
        emails.append({"to": to, "subject": subject, "body": body})

    monkeypatch.setattr("app.modules.users.service.send_email", fake_send_email)
    monkeypatch.setattr(
        "app.modules.users.service.generate_password",
        lambda length=10: "AdminPass123",
    )
    return emails


@pytest_asyncio.fixture
async def db_session_factory(
    sent_emails: list[dict[str, str]],
) -> AsyncIterator[async_sessionmaker[AsyncSession]]:
    engine = create_async_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    try:
        yield session_factory
    finally:
        app.dependency_overrides.clear()
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.drop_all)
        await engine.dispose()


@pytest_asyncio.fixture
async def client(
    db_session_factory: async_sessionmaker[AsyncSession],
) -> AsyncIterator[AsyncClient]:
    async def override_get_db() -> AsyncIterator[AsyncSession]:
        async with db_session_factory() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as async_client:
        yield async_client


@pytest.fixture
def create_user(db_session_factory: async_sessionmaker[AsyncSession]):
    async def _create_user(
        *,
        email: str,
        password: str,
        role: UserRole = UserRole.ADMIN,
    ) -> User:
        async with db_session_factory() as session:
            user = User(
                email=email,
                password_hash=hash_password(password),
                role=role.value,
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user

    return _create_user
