import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.main import app
from app.database import Base, get_db


# Test database URL (use separate test database)
TEST_DATABASE_URL = "postgresql+asyncpg://debate_user:debate_pass@localhost:5432/debate_ai_test"

# Create test engine
test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestSessionLocal = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def override_get_db():
    """Override database dependency for tests"""
    async with TestSessionLocal() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session")
async def setup_database():
    """Create test database tables"""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    # Teardown
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def client(setup_database):
    """Create async HTTP client for testing"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    """Test user registration"""
    response = await client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "securepass123"
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"
    assert "id" in data


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient):
    """Test registration with duplicate email"""
    # First registration
    await client.post(
        "/api/auth/register",
        json={
            "email": "duplicate@example.com",
            "username": "user1",
            "password": "pass123"
        }
    )

    # Second registration with same email
    response = await client.post(
        "/api/auth/register",
        json={
            "email": "duplicate@example.com",
            "username": "user2",
            "password": "pass456"
        }
    )

    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient):
    """Test successful login"""
    # Register user first
    await client.post(
        "/api/auth/register",
        json={
            "email": "login@example.com",
            "username": "loginuser",
            "password": "mypassword"
        }
    )

    # Login
    response = await client.post(
        "/api/auth/login",
        data={
            "username": "login@example.com",
            "password": "mypassword"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient):
    """Test login with wrong password"""
    # Register user
    await client.post(
        "/api/auth/register",
        json={
            "email": "wrongpass@example.com",
            "username": "wrongpassuser",
            "password": "correctpass"
        }
    )

    # Try login with wrong password
    response = await client.post(
        "/api/auth/login",
        data={
            "username": "wrongpass@example.com",
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_current_user(client: AsyncClient):
    """Test getting current user info"""
    # Register and login
    await client.post(
        "/api/auth/register",
        json={
            "email": "current@example.com",
            "username": "currentuser",
            "password": "pass123"
        }
    )

    login_response = await client.post(
        "/api/auth/login",
        data={
            "username": "current@example.com",
            "password": "pass123"
        }
    )

    token = login_response.json()["access_token"]

    # Get current user
    response = await client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "current@example.com"
    assert data["username"] == "currentuser"


@pytest.mark.asyncio
async def test_refresh_token(client: AsyncClient):
    """Test token refresh"""
    # Register and login
    await client.post(
        "/api/auth/register",
        json={
            "email": "refresh@example.com",
            "username": "refreshuser",
            "password": "pass123"
        }
    )

    login_response = await client.post(
        "/api/auth/login",
        data={
            "username": "refresh@example.com",
            "password": "pass123"
        }
    )

    refresh_token = login_response.json()["refresh_token"]

    # Refresh token
    response = await client.post(
        "/api/auth/refresh",
        json={"refresh_token": refresh_token}
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data

    # New tokens should be different
    assert data["access_token"] != login_response.json()["access_token"]
    assert data["refresh_token"] != refresh_token


@pytest.mark.asyncio
async def test_unauthorized_access(client: AsyncClient):
    """Test accessing protected route without token"""
    response = await client.get("/api/auth/me")

    assert response.status_code == 401


# Run tests with: pytest tests/ -v -s
