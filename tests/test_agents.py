import pytest
from httpx import AsyncClient
from app.models.agent import AgentPersonality


@pytest.mark.asyncio
async def test_list_agents(client: AsyncClient):
    """Test listing all agents"""
    response = await client.get("/api/agents/")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 5  # We have 5 default agents


@pytest.mark.asyncio
async def test_get_agent_by_id(client: AsyncClient):
    """Test getting a specific agent"""
    # First, get list of agents
    list_response = await client.get("/api/agents/")
    agents = list_response.json()

    if agents:
        agent_id = agents[0]["id"]

        response = await client.get(f"/api/agents/{agent_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == agent_id
        assert "name" in data
        assert "description" in data


@pytest.mark.asyncio
async def test_get_nonexistent_agent(client: AsyncClient):
    """Test getting agent that doesn't exist"""
    response = await client.get("/api/agents/99999")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_agent_without_auth(client: AsyncClient):
    """Test creating agent without authentication"""
    response = await client.post(
        "/api/agents/",
        json={
            "name": "Test Agent",
            "description": "Test description",
            "system_prompt": "Test prompt",
            "temperature": 0.7,
            "max_tokens": 1000
        }
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_agent_personalities_exist(client: AsyncClient):
    """Test that default agent personalities are created"""
    response = await client.get("/api/agents/")
    agents = response.json()

    agent_names = [agent["name"] for agent in agents]

    # Check for default agents
    expected_agents = ["Cético", "Otimista", "Técnico", "Criativo", "Pragmático"]

    for expected_name in expected_agents:
        assert expected_name in agent_names
