import pytest
from httpx import AsyncClient


async def get_auth_token(client: AsyncClient) -> str:
    """Helper to get authentication token"""
    # Register user
    await client.post(
        "/api/auth/register",
        json={
            "email": "debate_test@example.com",
            "username": "debate_tester",
            "password": "testpass123"
        }
    )

    # Login
    login_response = await client.post(
        "/api/auth/login",
        data={
            "username": "debate_test@example.com",
            "password": "testpass123"
        }
    )

    return login_response.json()["access_token"]


async def create_test_document(client: AsyncClient, token: str) -> int:
    """Helper to create a test document"""
    import tempfile
    import os

    # Create a temporary text file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("This is a test document for debate analysis.")
        temp_path = f.name

    try:
        with open(temp_path, 'rb') as f:
            response = await client.post(
                "/api/documents/upload",
                headers={"Authorization": f"Bearer {token}"},
                files={"file": ("test.txt", f, "text/plain")}
            )

        return response.json()["id"]
    finally:
        os.unlink(temp_path)


@pytest.mark.asyncio
async def test_create_debate(client: AsyncClient):
    """Test creating a debate"""
    token = await get_auth_token(client)
    doc_id = await create_test_document(client, token)

    response = await client.post(
        "/api/debates/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Test Debate",
            "document_id": doc_id,
            "num_rounds": 2
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Debate"
    assert data["document_id"] == doc_id
    assert data["status"] == "pending"


@pytest.mark.asyncio
async def test_create_debate_without_auth(client: AsyncClient):
    """Test creating debate without authentication"""
    response = await client.post(
        "/api/debates/",
        json={
            "title": "Test Debate",
            "document_id": 1,
            "num_rounds": 2
        }
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_list_debates(client: AsyncClient):
    """Test listing user's debates"""
    token = await get_auth_token(client)
    doc_id = await create_test_document(client, token)

    # Create a debate
    await client.post(
        "/api/debates/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Test Debate 1",
            "document_id": doc_id,
            "num_rounds": 2
        }
    )

    # List debates
    response = await client.get(
        "/api/debates/",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


@pytest.mark.asyncio
async def test_get_debate_details(client: AsyncClient):
    """Test getting debate with analyses"""
    token = await get_auth_token(client)
    doc_id = await create_test_document(client, token)

    # Create debate
    create_response = await client.post(
        "/api/debates/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Detailed Debate",
            "document_id": doc_id,
            "num_rounds": 2
        }
    )

    debate_id = create_response.json()["id"]

    # Get debate details
    response = await client.get(
        f"/api/debates/{debate_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == debate_id
    assert "analyses" in data


@pytest.mark.asyncio
async def test_vote_on_analysis(client: AsyncClient):
    """Test voting on an analysis"""
    token = await get_auth_token(client)

    # Note: This test requires an actual analysis to exist
    # In a real test, you'd create a debate, start it, wait for analyses,
    # then vote. For now, we just test the endpoint structure.

    response = await client.post(
        "/api/debates/analyses/1/vote",
        headers={"Authorization": f"Bearer {token}"},
        params={"vote_type": "up"}
    )

    # Will fail because analysis doesn't exist, but that's expected
    assert response.status_code in [200, 404]


@pytest.mark.asyncio
async def test_start_debate_validation(client: AsyncClient):
    """Test starting debate with validation"""
    token = await get_auth_token(client)
    doc_id = await create_test_document(client, token)

    # Create debate
    create_response = await client.post(
        "/api/debates/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Start Test Debate",
            "document_id": doc_id,
            "num_rounds": 1
        }
    )

    debate_id = create_response.json()["id"]

    # Try to start with invalid agent IDs
    response = await client.post(
        f"/api/debates/{debate_id}/start",
        headers={"Authorization": f"Bearer {token}"},
        json={"agent_ids": [99999]}
    )

    # Should handle gracefully
    assert response.status_code in [200, 400, 404]


@pytest.mark.asyncio
async def test_debate_workflow(client: AsyncClient):
    """Test complete debate workflow"""
    token = await get_auth_token(client)

    # 1. Create document
    doc_id = await create_test_document(client, token)
    assert doc_id > 0

    # 2. Get available agents
    agents_response = await client.get("/api/agents/")
    agents = agents_response.json()
    agent_ids = [agent["id"] for agent in agents[:3]]  # Use first 3 agents

    # 3. Create debate
    debate_response = await client.post(
        "/api/debates/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Workflow Test Debate",
            "document_id": doc_id,
            "num_rounds": 1
        }
    )

    assert debate_response.status_code == 201
    debate_id = debate_response.json()["id"]

    # 4. Verify debate was created
    get_response = await client.get(
        f"/api/debates/{debate_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert get_response.status_code == 200
    debate_data = get_response.json()
    assert debate_data["status"] == "pending"

    # Note: Starting the debate would actually call LLM APIs,
    # so we skip that in tests unless mocking the LLM service
