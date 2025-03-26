import pytest
from httpx import AsyncClient
from appFastapi import app

@pytest.mark.asyncio
async def test_receive_optitracking_data():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/Optitracking_data", json={"data": {"x": 10, "y": 20}})
    assert response.status_code == 200
    assert response.json()["status"] == "success"

@pytest.mark.asyncio
async def test_get_optitracking_data():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/Optitracking_data_forward")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_make_speed():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/speed", json={"speed": 50})
    assert response.status_code == 200
    assert response.json()["speed"] == 50

@pytest.mark.asyncio
async def test_get_current_speed():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/current_speed")
    assert response.status_code == 200
    assert response.json()["speed"] == 50

@pytest.mark.asyncio
async def test_move_robot():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/move", json={"direction": "up"})
    assert response.status_code == 200
    assert response.json()["direction"] == "up"

@pytest.mark.asyncio
async def test_get_current_direction():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/current_direction")
    assert response.status_code == 200
    assert response.json()["direction"] == "up"

@pytest.mark.asyncio
async def test_clear_locations():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.delete("/clear")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_receive_position():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/position", json={"x": 5, "y": 10})
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_get_locations():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/locations")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_receive_distance():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/distance", json={"distance": 30.5})
    assert response.status_code == 200
    assert response.json()["distance"] == 30.5

@pytest.mark.asyncio
async def test_get_current_distance():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/current_distance")
    assert response.status_code == 200
    assert response.json()["distance"] == 30.5
