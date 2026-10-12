from typing import AsyncGenerator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.main import app


@pytest_asyncio.fixture
async def test_engine():
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def client(test_engine) -> AsyncGenerator[AsyncClient, None]:
    session_maker = async_sessionmaker(test_engine, expire_on_commit=False, autoflush=False)

    async def override_get_db():
        async with session_maker() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


async def register(client: AsyncClient, email: str, display_name: str = "Test User", password: str = "SecurePass123!"):
    return await client.post(
        "/api/auth/register",
        json={"email": email, "display_name": display_name, "password": password},
    )


async def auth_headers(client: AsyncClient, email: str, **kwargs) -> dict:
    resp = await register(client, email, **kwargs)
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
