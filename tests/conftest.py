import asyncio
from typing import AsyncGenerator
import pytest
from httpx import ASGITransport, AsyncClient
import pytest_asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from db.database import get_async_session
from db.models import Base, User

DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine_test = create_async_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = async_sessionmaker(
    engine_test
)


@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="session")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with TestingSessionLocal() as session:
        yield session


@pytest_asyncio.fixture(scope="session")
async def client(db_session: AsyncSession):
    app.dependency_overrides[get_async_session] = lambda: db_session

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


USER_DATA = {
    "email": "test@example.com",
    "password": "testPassword"
}


@pytest_asyncio.fixture(scope="session")
async def auth_token(client: AsyncClient) -> str:
    """Login or register once and return JWT token (cached per test session)."""


    login_resp = await client.post(
        "/auth/login",
        data={"username": USER_DATA["email"], "password": USER_DATA["password"]},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    if login_resp.status_code == 200:
        token = login_resp.json().get("access_token")
        if token:
            return token


    reg_resp = await client.post("/auth/register", json=USER_DATA)
    if reg_resp.status_code not in (200, 201):
        pytest.exit(f"Registration failed: {reg_resp.status_code} - {reg_resp.text}")


    login_resp = await client.post(
        "/auth/login",
        data={"username": USER_DATA["email"], "password": USER_DATA["password"]},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    if login_resp.status_code != 200:
        pytest.exit(f"Login after registration failed: {login_resp.status_code} - {login_resp.text}")

    token = login_resp.json().get("access_token")
    if not token:
        pytest.exit("No access_token received")

    return token

    
